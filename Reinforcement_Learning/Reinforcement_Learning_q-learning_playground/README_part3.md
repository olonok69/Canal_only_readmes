# RL Q-Learning — Part 3: Advanced Value-Based Methods

<p align="center">
  <img src="doc/images/q_learning_cover.svg" alt="Q-Learning Cover" width="45%" />
  <img src="doc/images/dqn_cover.svg" alt="DQN Cover" width="45%" />
</p>

**Part 3** of the Q-Learning series. This document covers the four advanced methods — C51, QR-DQN, Rainbow DQN, and HER — their motivation, how they work, and how to run them from this repository.

> **Series navigation**
> - **Part 1**: Q-Learning fundamentals + vanilla DQN → [README.md](README.md)
> - **Part 2**: DQN Extensions (Double, Dueling, Noisy, PER, N-step) → [README_part2.md](README_part2.md)
> - **Part 3** (this file): Advanced variants (C51, QR-DQN, Rainbow, HER)

---

## Why go beyond the Part 2 extensions?

Part 2 fixed five specific weaknesses of vanilla DQN while still predicting a **single scalar** Q(s,a) per action. Part 3 asks: what if that scalar isn't enough?

| Limitation | What Part 3 adds |
|------------|-----------------|
| **Scalar Q-values lose return shape** — the mean hides variance, bimodality, and tail risk | C51 and QR-DQN learn the full **distribution** of returns, not just its mean |
| **Individual extensions don't stack automatically** — combining them requires care | Rainbow DQN integrates all six orthogonal improvements into one principled agent |
| **Sparse rewards starve the replay buffer** — almost every episode produces reward = 0 | HER relabels failed trajectories with goals the agent actually reached, generating rich training signal |

The key insight shared by C51 and QR-DQN: **action selection does not change** — you still pick `argmax` over expected values. What changes is *how the network is trained*. A distributional target provides 51 gradient signals per update instead of 1, enabling faster and more stable learning.

---

## Prerequisites

This part assumes familiarity with the following concepts from Parts 1 and 2:

| Concept | One-sentence recap |
|---------|-------------------|
| Bellman target | `y = r + γ · bootstrap` is the core TD target |
| DQN loop | replay buffer + target network + online Q-network |
| Double DQN | online net selects the best action, target net evaluates it |
| Dueling DQN | `Q = V + A − mean(A)` separates state value from action advantage |
| Noisy DQN | learned parameter-space noise replaces epsilon-greedy |
| PER | TD-error-weighted sampling; corrected with importance-sampling weights |
| N-step DQN | bootstraps from n steps ahead: `G_t^(n) = r_t + γ·r_{t+1} + ... + γⁿ Q(s_{t+n}, ·)` |

One-line transition from Part 2 to Part 3:
- Part 2 improved **optimization and data usage** for scalar Q-values.
- Part 3 improves **target representation** (distributional RL) and **goal relabeling** (HER).

---

## Installation

```bash
uv sync
```

---

## Method 1 — C51 (Categorical DQN)

### What it improves
Vanilla DQN learns `Q(s,a) = E[G_t | s,a]` — the *expected* return. The mean can hide crucial information about outcome shape.

Consider two actions with the same expected return of 50:
- **Action A**: returns exactly 50 every time — safe and predictable.
- **Action B**: returns 0 in 95% of cases but 1000 in 5% — high-risk, heavy-tailed.

A scalar DQN cannot distinguish them. C51 can, because it learns the full probability distribution over returns, giving the network a much richer training signal.

### How it works
C51 discretizes the return range `[V_min, V_max]` into `N=51` evenly spaced **atoms**:

```
z_i = V_min + i * Δz,   i = 0..50,   Δz = (V_max − V_min) / 50
```

The network outputs **logits** per action per atom, converted to probabilities via softmax:

```
p_i(s,a) = softmax(logits_i)   →   P(Z(s,a) = z_i)
```

Action selection uses the expected value — identical to vanilla DQN:

```
Q(s,a) = Σ_i p_i(s,a) · z_i       argmax over this gives the greedy action
```

Training uses **categorical projection + cross-entropy**. For each atom `z_i` in the target distribution:
1. **Shift**: `Tz_i = r + γ · z_i`
2. **Clip**: `Tz_i = clip(Tz_i, V_min, V_max)`
3. **Project**: split mass between the two nearest atoms via linear interpolation

Loss:

```
L = −Σ_i target_prob_i · log(predicted_prob_i)
```

This is a 51-dimensional supervision signal instead of a single scalar — the network learns *what it got wrong* along the entire return distribution at every step.

### Code changes — `benchmarks/dqn_c51.py`

```python
class C51Network(nn.Module):
    def forward(self, x):
        logits = self.net(x)
        return logits.view(-1, self.n_actions, self.n_atoms)   # [batch, actions, 51]

def _q_values_from_logits(logits, supports):
    probs = torch.softmax(logits, dim=-1)
    return torch.sum(probs * supports.view(1, 1, -1), dim=-1)  # E[Z] = Q

def _project_distribution(next_probs, rewards, dones, gamma, supports, v_min, v_max):
    # Shift → clip → linear interpolation to neighbors
    ...

# Training loss
pred_log_probs = F.log_softmax(pred_logits[range(batch), b_a_t], dim=-1)
loss = -(target_dist * pred_log_probs).sum(dim=-1).mean()
```

New hyperparameters:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `v_min` | 0 | Minimum return in support |
| `v_max` | 500 | Maximum return in support |
| `n_atoms` | 51 | Number of categorical atoms |

### Run it

```bash
uv run python dqn_c51_benchmark.py --record-video --plot
```

### When it helps most
- Environments with multimodal or heavy-tailed return distributions
- When richer training signal leads to faster convergence
- As a direct distributional upgrade to vanilla DQN

### Tuning tips

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Learning plateau early | `V_min/V_max` too narrow | widen support range |
| Unstable loss | learning rate too high | reduce `learning_rate` |
| Flat policy | atom mass collapses to one spike | inspect logit scale |
| Good training, weak eval | overfitting replay distribution | increase eval cadence, use multiple seeds |

---

## Method 2 — QR-DQN (Quantile Regression DQN)

### What it improves
C51 fixes atom *positions* and learns *probabilities*. QR-DQN inverts this: it fixes equal *probabilities* and learns the *positions* (quantile values). The key practical benefit: **no `V_min`/`V_max` needed** — the network figures out the support range automatically.

### How it works
QR-DQN predicts `N=51` quantile values per action. Each carries equal probability mass `1/N`. The quantile fractions are fixed at midpoints:

```
τ_i = (i + 0.5) / N
```

So `τ_0 ≈ 0.01` is the 1st percentile, `τ_25 ≈ 0.50` is the median, `τ_50 ≈ 0.99` is the 99th percentile.

Action selection is the arithmetic mean of quantiles:

```
Q(s,a) = (1/N) · Σ_i θ_i(s,a)
```

Training uses the **asymmetric quantile Huber loss**. For each pairwise TD error `δ_ij = target_j − pred_i`:

```
ρ_τ(δ) = |τ − I[δ < 0]| · Huber_κ(δ)
```

If quantile `τ=0.9` underestimates (δ>0), weight = `|0.9−0| = 0.9` (strong). If it overestimates (δ<0), weight = `|0.9−1| = 0.1` (weak). This asymmetry pushes the 90th percentile above 90% of target values — exactly the quantile definition.

### Code changes — `benchmarks/dqn_qr.py`

```python
class QRDQN(nn.Module):
    def forward(self, x):
        quantiles = self.net(x)
        return quantiles.view(-1, self.n_actions, self.n_quantiles)  # [batch, actions, 51]

def _q_values_from_quantiles(quantiles):
    return quantiles.mean(dim=-1)   # simple mean — each quantile has equal weight 1/N

def _quantile_huber_loss(pred_quantiles, target_quantiles, taus, kappa):
    td = target_quantiles.unsqueeze(1) - pred_quantiles.unsqueeze(2)  # [batch, N, N]
    huber = torch.where(torch.abs(td) <= kappa,
                        0.5 * td.pow(2),
                        kappa * (torch.abs(td) - 0.5 * kappa))
    quantile_weight = torch.abs(taus.view(1, -1, 1) - (td.detach() < 0).float())
    return (quantile_weight * huber).mean()
```

### Run it

```bash
uv run python dqn_qr_benchmark.py --record-video --plot
```

### C51 vs QR-DQN at a glance

| Aspect | C51 | QR-DQN |
|--------|-----|--------|
| Support positions | Fixed in `[V_min, V_max]` | Learned (free to move anywhere) |
| Probability mass | Learned via softmax | Fixed uniform `1/N` |
| Main sensitivity | Support range clipping | Quantile-loss stability |
| Loss type | Cross-entropy on projected distribution | Asymmetric quantile Huber |
| Key advantage | Simple, stable baseline | No support range needed |

### Tuning tips

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| High variance returns | Too few quantiles | Increase `num_quantiles` |
| Slow convergence | Conservative LR/batch | Tune batch size or LR |
| Loss spikes | Unstable TD pairs | Lower LR, clip gradients |
| Weak gains over C51 | Environment too simple | Expected on easy control tasks |

---

## Method 3 — Rainbow DQN

### What it is
Rainbow is not a new algorithm — it is the answer to: *"What happens if we combine all six orthogonal DQN improvements into one agent?"*

Each component attacks a different failure mode:

| Component | What it fixes | Where it lives |
|-----------|--------------|----------------|
| Double DQN | Overestimation bias from `max` | Target action selection in training loop |
| Dueling architecture | Cannot separate state value from action advantage | `RainbowDQN.forward()` value/advantage streams |
| Noisy layers | Crude epsilon-greedy exploration | `NoisyLinear` replaces `nn.Linear` |
| Prioritized replay | Uniform sampling wastes time on easy transitions | `PrioritizedReplayBuffer` |
| N-step returns | Slow reward propagation | `nstep_buffer` in training loop |
| C51 distribution | Scalar target discards return shape | Distributional head + `_project_distribution` |

Because these fix *different problems*, their gains stack. The original Rainbow paper (Hessel et al., 2018) showed that removing any single component hurts performance, confirming all six contribute.

### How it works — the network

Rainbow combines dueling, distributional, and noisy in one forward pass:

```python
class RainbowDQN(nn.Module):
    def forward(self, x):
        f = self.feature(x)                                      # shared feature extractor
        adv = self.adv2(F.relu(self.adv1(f)))                    # noisy advantage stream
        val = self.val2(F.relu(self.val1(f)))                    # noisy value stream
        adv = adv.view(-1, self.n_actions, self.n_atoms)
        val = val.view(-1, 1, self.n_atoms)
        return val + adv - adv.mean(dim=1, keepdim=True)         # dueling combination
        # output: [batch, n_actions, n_atoms]  ← same shape as C51
```

### How it works — the training loop

Rainbow's distinctive training signal is a **mixed loss** combining 1-step and n-step distributional targets:

```python
# 1. No epsilon: noisy net provides automatic exploration
action = _q_values_from_logits(policy_net(state_t), supports).argmax(dim=1).item()

# 2. Store 8-tuple: both 1-step and n-step targets from the same transition
memory.add((s, a, r_1, ns_1, d_1, r_n, ns_n, d_n))

# 3. Mixed loss: 1-step (stable) + n-step (fast propagation)
loss_1 = -(target_dist_1step * pred_log_probs).sum(-1)
loss_n = -(target_dist_nstep * pred_log_probs).sum(-1)
per_sample_loss = cfg.one_step_loss_coef * loss_1 + cfg.n_step_loss_coef * loss_n

# 4. IS-weighted by PER, then backprop
loss = (is_weights_t * per_sample_loss).mean()
loss.backward()
torch.nn.utils.clip_grad_norm_(policy_net.parameters(), cfg.grad_clip_norm)

# 5. Update priorities with combined loss
memory.update_priorities(indices, per_sample_loss.detach().cpu().numpy() + 1e-6)
```

### Run it

```bash
uv run python dqn_rainbow_benchmark.py --record-video --plot
```

### Tuning playbook — phase by phase

Tune in stages rather than all at once:

1. **Start with defaults** — verify a non-divergent learning curve
2. **Adjust PER** (`alpha`, `beta`) only after the baseline looks healthy
3. **Adjust n-step** horizon and loss coefficients
4. **Finally refine** distributional range (`v_min`, `v_max`) and noisy parameters (`sigma_init`)

```bash
uv run python dqn_rainbow_benchmark.py --device cuda \
    --grad-clip-norm 10 --one-step-loss-coef 1.0 --n-step-loss-coef 1.0
```

### Debugging checklist

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Training diverges late | Aggressive mixed loss or high LR | Lower LR and n-step coefficient |
| Slow learning despite PER | Priorities saturate (all equal) | Inspect `update_priorities()` calls |
| Unstable across seeds | Noisy exploration too strong | Reduce `sigma_init` or warm up longer |
| Slow on CPU | Heavy config | Run `--device cuda` when available |

---

## Method 4 — HER (Hindsight Experience Replay)

### What it fixes
In sparse-goal tasks, the reward is almost always zero. A replay buffer filled with failed episodes provides almost no supervision signal.

**Concrete example**: a robot must place an object at a precise target. Through random exploration it almost never succeeds, so thousands of replay transitions all carry reward = 0. The agent learns nothing.

HER's insight: *"You didn't reach the goal you wanted — but where did you end up?"*

### How it works
After each episode, HER **relabels** transitions from the original (failed) goal to goals the agent *actually achieved*:

```
Original transition:  (s=3, a=right, r=0, s'=4, g=7)   ← failure
Relabeled:            (s=3, a=right, r=1, s'=4, g'=4)  ← success!
```

The physical trajectory is unchanged. Only the goal label is swapped. What was a total failure now contributes a successful supervision signal.

**Step-by-step example** (agent tries to reach position 7, ends at 4):

Original transitions (all reward = 0):
```
(s=0, a=right, r=0, s'=1, g=7)
(s=1, a=right, r=0, s'=2, g=7)
(s=2, a=right, r=0, s'=3, g=7)
(s=3, a=right, r=0, s'=4, g=7)
```

Relabeled transitions (HER pretends goal was 4):
```
(s=0, a=right, r=0, s'=1, g'=4)
(s=1, a=right, r=0, s'=2, g'=4)
(s=2, a=right, r=0, s'=3, g'=4)
(s=3, a=right, r=1, s'=4, g'=4)  ← success!
```

### Data multiplication
A 10-step episode with `her_k=4` generates up to 40 relabeled transitions in addition to the 10 original ones — ~50 total updates from an episode that was nearly useless without HER.

### Code changes — `benchmarks/her.py`

```python
# Goal-conditioned Q-table: Q[position, goal, action]
q_table = np.zeros((grid_size, grid_size, 2), dtype=np.float32)

# Standard Bellman update — math is unchanged, goal is an extra dimension
def _td_update(q_table, state, action, reward, next_state, done, alpha, gamma):
    current_q = q_table[state[0], state[1], action]
    next_best = 0.0 if done else float(np.max(q_table[next_state[0], next_state[1]]))
    target = reward + gamma * next_best
    q_table[state[0], state[1], action] = (1 - alpha) * current_q + alpha * target

# HER relabeling loop — after each episode
for t in range(len(trajectory)):
    s_t, a_t, _, ns_t, _, _ = trajectory[t]
    future_indices = range(t, len(trajectory))
    sampled = random.sample(list(future_indices), k=min(cfg.her_k, len(trajectory) - t))
    for idx in sampled:
        future_goal = trajectory[idx][5]               # achieved goal at future step
        her_state = (s_t[0], future_goal)
        her_next_state = (ns_t[0], future_goal)
        her_done = her_next_state[0] == future_goal
        her_reward = 0.0 if her_done else -1.0
        _td_update(q_table, her_state, a_t, her_reward,
                   her_next_state, her_done, cfg.learning_rate, cfg.gamma)
```

> **Key insight**: HER changes the **data distribution**, not the Bellman math. The Q-function becomes `Q(s, g, a)` — goal-conditioned. The update rule is identical to vanilla Q-learning. What changes is which transitions are fed into it.

### Run it

```bash
uv run python her_benchmark.py --plot
```

### When it helps most
- Binary or very sparse reward functions where random exploration rarely succeeds
- Goal-conditioned tasks where the agent can achieve nearby goals even when it misses the target
- Any setting where the replay buffer is overwhelmingly filled with reward = 0 transitions

### Tuning tips

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| No HER gain | `her_k` too low | Increase `her_k` (try 8) |
| Unrealistic metrics | Bug in reward recomputation | Verify `her_done` matches relabeled goal |
| Overfitting relabeled goals | Too many hindsight samples | Rebalance original vs HER transitions |
| Task still fails | Exploration too weak | Combine HER with better exploration |
| Q-table too large | `grid_size` too big | Reduce grid or switch to DQN + HER |

---

## Running all Part 3 methods together

Compare all four methods against vanilla DQN in a single run:

```bash
uv run python run_all_comparison.py \
  --methods dqn dqn_c51 dqn_qr dqn_rainbow her
```

Run each method individually with video and plots:

```bash
uv run python dqn_c51_benchmark.py      --record-video --plot
uv run python dqn_qr_benchmark.py       --record-video --plot
uv run python dqn_rainbow_benchmark.py  --record-video --plot
uv run python her_benchmark.py          --plot
```

Generate aggregate reports after running:

```bash
uv run python scripts/aggregate_results.py \
    --inputs outputs/*.json \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv

uv run python scripts/generate_aggregate_report.py \
    --input outputs/aggregate_summary.json \
    --output-dir outputs/report \
    --title "RL Advanced Part 3 Aggregate"
```

---

## Method summary

| Method | What changes | New hyperparams | Overhead | Best for |
|--------|-------------|-----------------|----------|----------|
| **C51** | Output = 51 atoms per action + categorical projection loss | `v_min`, `v_max`, `n_atoms` | Moderate | Stable distributional baseline |
| **QR-DQN** | Output = 51 quantile values per action + asymmetric Huber loss | `num_quantiles`, `kappa` | Moderate | Flexible support, no range needed |
| **Rainbow** | All 6 components combined: noisy + dueling + distributional + PER + n-step + double | Several (see playbook) | High | Default strong value-based agent |
| **HER** | Goal-conditioned Q + relabeling loop after each episode | `her_k` | Low | Sparse-goal tasks |

Key takeaways:
- C51 and QR-DQN both learn **return distributions**, but parameterize them in opposite ways.
- Rainbow stacks all orthogonal improvements — gains multiply because they fix different problems.
- HER improves **data efficiency** by recycling failed episodes; it is complementary to all DQN variants.
- **Double DQN** (from Part 2) is reused inside Rainbow — strictly free improvement, always include it.

---

## Output artifacts

| Path | Contents |
|------|----------|
| `outputs/comparison_results.json/csv` | Per-run metrics for all methods |
| `outputs/aggregate_summary.json/csv` | Multi-run aggregated statistics |
| `outputs/report/` | Generated plots and HTML reports |
| `videos/` | Recorded evaluation episodes |
| `runs/` | TensorBoard run data |

---

## Documentation

- Presentation guide (English): [doc/presentations/presentation_guide_part3_60min.md](doc/presentations/presentation_guide_part3_60min.md)
- Presentation guide (Spanish): [doc/presentations/presentation_guide_part3_60min_es.md](doc/presentations/presentation_guide_part3_60min_es.md)
- Algorithm docs (English): [doc/README.md](doc/README.md)
- Algorithm docs (Spanish): [doc/es/README.md](doc/es/README.md)
- Part 2 (DQN extensions): [README_part2.md](README_part2.md)
- Part 1 (Q-Learning + DQN): [README.md](README.md)
