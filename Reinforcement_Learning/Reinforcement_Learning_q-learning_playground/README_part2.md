# RL Q-Learning — Part 2: DQN Extensions

<p align="center">
  <img src="doc/images/q_learning_cover.svg" alt="Q-Learning Cover" width="45%" />
  <img src="doc/images/dqn_cover.svg" alt="DQN Cover" width="45%" />
</p>

**Part 2** of the Q-Learning series. This document covers the five canonical DQN extensions — Double DQN, Dueling DQN, Noisy DQN, Prioritized Experience Replay, and N-step DQN — their motivation, how they work, and how to run them from this repository.

> **Series navigation**
> - **Part 1**: Q-Learning fundamentals + vanilla DQN → [README.md](README.md)
> - **Part 2** (this file): DQN Extensions (Double, Dueling, Noisy, PER, N-step)
> - **Part 3**: Advanced variants (C51, QR-DQN, Rainbow, HER) → [README_part3.md](README_part3.md)

---

## Why extend DQN?

Vanilla DQN works, but has five well-known weaknesses. Each extension in this part addresses exactly one:

| # | Weakness | Extension |
|---|----------|-----------|
| 1 | **Overestimates Q-values** — the `max` operator introduces positive bias | Double DQN |
| 2 | **Single value stream** — cannot separate "this state is good" from "this action is good" | Dueling DQN |
| 3 | **Crude exploration** — epsilon-greedy explores uniformly, ignoring state context | Noisy DQN |
| 4 | **Uniform replay** — all transitions sampled equally, wasting time on easy examples | Prioritized Replay |
| 5 | **Slow reward propagation** — 1-step bootstrap means rewards travel one step per update | N-step DQN |

The extensions are **orthogonal**: they fix different problems and can be freely combined. Rainbow DQN (Part 3) combines all of them.

---

## Prerequisites

This part assumes familiarity with the following concepts from Part 1:

| Concept | One-sentence recap |
|---------|-------------------|
| Bellman Equation | `Q*(s,a) = E[r + γ · max_a' Q*(s',a')]` — the recursive value identity |
| DQN Network | Neural network `Q_θ(s,a)` approximates the Q-function: state in, Q-values out |
| Replay Buffer | Store transitions `(s,a,r,s',done)`; sample random mini-batches to break correlation |
| Target Network | Frozen copy `Q_θ⁻` updated every N steps; provides stable training targets |
| Epsilon-greedy | Explore with probability ε, exploit with `argmax Q` otherwise |
| Loss Function | MSE between current Q-prediction and Bellman target: `L = (Q_θ(s,a) − y)²` |

---

## Installation

```bash
uv sync
```

---

## Extension 1 — Double DQN

### What it fixes
The vanilla Bellman target uses the **same network** to both select and evaluate the best next action:

```
y = r + γ · max_a' Q_θ⁻(s', a')
```

When Q-estimates are noisy, `max` consistently picks actions that are overestimated by noise. Over many updates, this bias compounds.

### How it works
Double DQN decouples selection from evaluation using **two networks**:

```
a* = argmax_a' Q_θ(s', a')       ← policy net SELECTS
y  = r + γ · Q_θ⁻(s', a*)       ← target net EVALUATES
```

Even if the policy net selects an overestimated action, the target net provides an independent evaluation, cancelling the bias on average.

### Code changes — `benchmarks/dqn_double.py`

```python
# Vanilla DQN: same network selects and evaluates
next_q = target_net(b_ns_t).max(1)[0].detach()

# Double DQN: policy net selects, target net evaluates
best_actions = policy_net(b_ns_t).argmax(dim=1, keepdim=True)
next_q = target_net(b_ns_t).gather(1, best_actions).squeeze(1).detach()

expected_q = b_r_t + (cfg.gamma * next_q * (1 - b_d_t))
```

### Run it

```bash
uv run python dqn_double_benchmark.py --record-video --plot
```

### When it helps most
- Large action spaces — more actions means more chances for overestimation
- Noisy reward signals — higher noise magnifies the bias
- It is a strict improvement with near-zero cost — use it by default

---

## Extension 2 — Dueling DQN

### What it fixes
The vanilla Q-network fuses two distinct concepts into a single output:

- **State value V(s)**: how good is it to *be* in this state, regardless of action?
- **Action advantage A(s,a)**: how much *better* is action `a` compared to the average action in this state?

Merging them into one stream slows learning, especially in states where the action choice barely matters.

### How it works
The network is split into two parallel streams that share a feature extractor:

```
                +-------------------+
      +---------► Value stream      |──► V(s)         [1 output]
      |          | (FC layers)      |
Input-+          +-------------------+          ──► Q(s,a) = V(s) + A(s,a) − mean(A)
  s   | shared                            
      | features +-------------------+
      +---------► Advantage stream  |──► A(s,a)       [n_actions outputs]
                | (FC layers)      |
                +-------------------+
```

The mean subtraction ensures identifiability: `A(s, a*) > 0` for the best action, `A(s, a) < 0` for worse ones.

### Code changes — `benchmarks/dqn_dueling.py`

```python
class DuelingDQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super().__init__()
        self.feature = nn.Sequential(nn.Linear(n_observations, 128), nn.ReLU())
        self.value_stream = nn.Sequential(
            nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, 1))
        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 128), nn.ReLU(), nn.Linear(128, n_actions))

    def forward(self, x):
        features = self.feature(x)
        value = self.value_stream(features)
        advantage = self.advantage_stream(features)
        return value + advantage - advantage.mean(dim=1, keepdim=True)
```

### Run it

```bash
uv run python dqn_dueling_benchmark.py --record-video --plot
```

### When it helps most
- Environments with many actions that have similar values
- States where the action does not matter — the value stream handles those efficiently

---

## Extension 3 — Noisy DQN

### What it fixes
Epsilon-greedy exploration is **state-agnostic**: it explores with the same probability regardless of what the agent already knows about the current state.  
This requires tuning `eps_start`, `eps_end`, and `eps_decay` — three hyperparameters that are problem-specific.

### How it works
Noisy DQN replaces epsilon-greedy with **learned parametric noise** in the network weights.

A standard linear layer computes `y = Wx + b`.  
A `NoisyLinear` layer computes:

```
y = (μ_w + σ_w · ε_w) · x + (μ_b + σ_b · ε_b)
```

| Component | Meaning |
|-----------|---------|
| `μ_w, μ_b` | Learnable mean weights (like normal weights) |
| `σ_w, σ_b` | Learnable noise magnitude (trained by gradient descent) |
| `ε_w, ε_b` | Random noise sampled at each forward pass, not trained |

The network learns *how much* to explore via the σ parameters. In well-explored states σ shrinks to ~0 (exploit). In uncertain states σ stays large (explore).

### Code changes — `benchmarks/dqn_noisy.py`

```python
class NoisyLinear(nn.Module):
    def forward(self, x):
        if self.training:          # training: use noisy weights (explore)
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias   = self.bias_mu   + self.bias_sigma   * self.bias_epsilon
        else:                      # evaluation: use mean weights only (exploit)
            weight = self.weight_mu
            bias   = self.bias_mu
        return F.linear(x, weight, bias)
```

No epsilon-greedy at all — the action selection is always greedy:

```python
action = policy_net(state_t).argmax()
```

### Run it

```bash
uv run python dqn_noisy_benchmark.py --record-video --plot
```

### What is removed
`eps_start`, `eps_end`, `eps_decay` — exploration is fully automatic.

### When it helps most
- Tasks that require deep, structured exploration
- Any situation where the right exploration schedule is hard to tune by hand

---

## Extension 4 — Prioritized Experience Replay (PER)

### What it fixes
Vanilla DQN samples transitions uniformly from the replay buffer. But not all transitions are equally useful:

- **Easy transitions** (low TD error): the network already predicts them well — sampling them wastes a step.
- **Surprising transitions** (high TD error): contain the most learning signal.

### How it works
PER assigns each transition a **priority** based on its **TD error**:

```
priority_i = |TD_error_i| + ε_prio
P(i) = priority_i^α / Σ_j priority_j^α
```

Sampling with non-uniform probabilities introduces **bias**, corrected with importance-sampling weights:

```
w_i = (1 / (N · P(i)))^β
```

`β` is annealed from 0.4 → 1.0 during training to fully correct the bias at the end.

### Code changes — `benchmarks/dqn_prio_replay.py`

```python
class PrioritizedReplayBuffer:
    def push(self, transition):
        max_prio = max(self.priorities) if self.priorities else 1.0
        # New transitions get maximum priority

    def sample(self, batch_size, beta=0.4):
        probs = priorities ** self.alpha / sum(priorities ** self.alpha)
        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        weights = (N * probs[indices]) ** (-beta)
        weights /= weights.max()
        return samples, indices, weights

    def update_priorities(self, indices, td_errors):
        for idx, td_error in zip(indices, td_errors):
            self.priorities[idx] = abs(td_error) + 1e-6
```

New hyperparameters:

| Parameter | Default | Notes |
|-----------|---------|-------|
| `alpha` | 0.6 | Prioritization exponent (0 = uniform, 1 = full priority) |
| `beta_start` | 0.4 | Initial IS correction (annealed to 1.0) |
| `epsilon_prio` | 1e-6 | Prevents zero priority |

### Run it

```bash
uv run python dqn_prio_replay_benchmark.py --record-video --plot
```

### When it helps most
- Sparse reward environments — rare rewarding transitions get replayed more
- Large replay buffers where uniform sampling dilutes informative transitions

---

## Extension 5 — N-step DQN

### What it fixes
Vanilla DQN bootstraps from a **single step**:

```
y = r_t + γ · max_a' Q(s_{t+1}, a')
```

Information travels **one step at a time**. If a positive reward occurs at step 100, it takes ~100 updates for that signal to influence the Q-value at step 0.

### How it works
N-step DQN looks **n steps ahead** before bootstrapping:

```
G_t^(n) = r_t + γ·r_{t+1} + ... + γ^{n-1}·r_{t+n-1} + γ^n · max_a' Q(s_{t+n}, a')
```

Bias–variance trade-off:

| n | Bias | Variance | Speed |
|---|------|----------|-------|
| 1 (DQN) | High | Low | Slow propagation |
| 3 (default) | Moderate | Moderate | Good balance |
| 5–10 | Lower | Higher | Fast propagation |
| Full episode | None | Maximum | Immediate |

### Code changes — `benchmarks/dqn_n_steps.py`

```python
nstep_buffer = collections.deque(maxlen=cfg.n_steps)

if len(nstep_buffer) == cfg.n_steps:
    cum_reward = 0.0
    discount = 1.0
    for _, _, r_i, _, d_i in nstep_buffer:
        cum_reward += discount * r_i
        if d_i: break
        discount *= cfg.gamma
    # Store (s0, a0, cum_reward, s_last, d_last) in replay

# Modified target discount
expected_q = b_r_t + (cfg.gamma ** cfg.n_steps) * next_q * (1 - b_d_t)
```

### Run it

```bash
uv run python dqn_n_steps_benchmark.py --record-video --plot
```

### When it helps most
- Environments with delayed rewards
- When faster credit assignment outweighs the variance cost (low-stochasticity envs)

---

## Running all extensions together

Compare all five extensions against vanilla DQN in a single run:

```bash
uv run python run_all_comparison.py \
  --methods dqn dqn_double dqn_dueling dqn_noisy dqn_prio_replay dqn_n_steps \
  --record-video
```

Record videos and training plots for all extensions individually:

```bash
uv run python dqn_double_benchmark.py      --record-video --plot
uv run python dqn_dueling_benchmark.py     --record-video --plot
uv run python dqn_noisy_benchmark.py       --record-video --plot
uv run python dqn_prio_replay_benchmark.py --record-video --plot
uv run python dqn_n_steps_benchmark.py     --record-video --plot
```

---

## Extension summary

| Extension | What changes | New hyperparams | Overhead | Best for |
|-----------|-------------|-----------------|----------|----------|
| **Double DQN** | Target computation (~2 lines) | None | Negligible | Reducing overestimation |
| **Dueling DQN** | Network architecture (~20 lines) | None | Minimal | Many-action environments |
| **Noisy DQN** | Linear layers + remove ε-greedy (~60 lines) | `sigma_init` | Moderate | Deep exploration tasks |
| **PER** | Replay buffer + weighted loss (~50 lines) | `alpha`, `beta` | Moderate | Sparse reward environments |
| **N-step DQN** | Buffer logic + target discount (~20 lines) | `n_steps` | Minimal | Delayed reward propagation |

Key takeaways:
- Each extension fixes **one specific weakness** of vanilla DQN.
- They are **orthogonal** and can be freely combined.
- **Double DQN** is a free strict improvement — always use it.
- **Noisy DQN** completely eliminates the exploration schedule.
- **PER** has the biggest impact in sparse-reward or large-buffer scenarios.

---

## Output artifacts

Generated files are written to:

| Path | Contents |
|------|----------|
| `outputs/comparison_results.json/csv` | Per-run metrics for all methods |
| `outputs/aggregate_summary.json/csv` | Multi-run aggregated statistics |
| `outputs/report/` | Generated plots and HTML reports |
| `videos/` | Recorded evaluation episodes |
| `runs/` | TensorBoard run data |

---

## Documentation

- Presentation guide (English): [doc/presentations/presentation_guide_part2_60min.md](doc/presentations/presentation_guide_part2_60min.md)
- Presentation guide (Spanish): [doc/presentations/presentation_guide_part2_60min_es.md](doc/presentations/presentation_guide_part2_60min_es.md)
- Algorithm docs (English): [doc/README.md](doc/README.md)
- Algorithm docs (Spanish): [doc/es/README.md](doc/es/README.md)
- Part 1 overview: [README.md](README.md) · [README_es.md](README_es.md)
