# RL Continuous Control: Off-Policy Actor-Critic Methods

> **DDPG · TD3 · SAC** — from the original Lillicrap (2015) baseline to the
> state-of-the-art Haarnoja (2018) entropy-regularised framework, all in one
> self-contained, reproducible benchmark suite.

This repository implements and compares three landmark off-policy, actor-critic
algorithms for **continuous-action reinforcement learning**.  Each algorithm is
documented line-by-line, benchmarked on `Pendulum-v1`, and wired into a shared
toolchain for multi-seed aggregation and automated report generation.

---

## Repository structure

```
rl_hybrid_algorithms/
├── benchmarks/                ← reusable algorithm implementations
│   ├── __init__.py            ← public re-exports
│   ├── common.py              ← BenchmarkResult, metrics, seed control, video helper
│   ├── replay_buffer.py       ← shared off-policy experience buffer (all three algos)
│   ├── ddpg.py                ← DDPGConfig · Actor · Critic · run_ddpg()
│   ├── td3.py                 ← TD3Config  · Actor · TwinCritic · run_td3()
│   └── sac.py                 ← SACConfig  · GaussianActor · TwinCritic · run_sac()
│
├── doc/                       ← algorithm deep-dives and presenter guides
│   ├── 01_ddpg.md             ← DDPG: theory, architecture, key equations
│   ├── 02_td3.md              ← TD3: three fixes explained in depth
│   ├── 03_sac.md              ← SAC: entropy objective, reparameterisation, tanh correction
│   ├── presentation_guide_60min.md    ← 60-min presenter guide (EN)
│   ├── presentation_guide_60min_es.md ← 60-min presenter guide (ES)
│   └── es/                    ← Spanish translations of algorithm deep-dives
│
├── algorithms/                ← reference implementations (original TD3 paper code)
│
├── scripts/
│   ├── aggregate_results.py       ← multi-seed result aggregation
│   └── generate_aggregate_report.py ← plots + Markdown report from aggregated data
│
├── outputs/                   ← benchmark results (auto-created at runtime)
│
├── ddpg_benchmark.py          ← standalone DDPG runner with full CLI
├── td3_benchmark.py           ← standalone TD3 runner with full CLI
├── sac_benchmark.py           ← standalone SAC runner with full CLI
├── rl_comparison.py           ← thin entry point → delegates to run_all_comparison
└── run_all_comparison.py      ← unified comparison orchestrator
```

---

## Algorithms

### DDPG — Deep Deterministic Policy Gradient

**Paper:** Lillicrap et al. (2015) — [arXiv:1509.02971](https://arxiv.org/abs/1509.02971)  
**Implementation:** [`benchmarks/ddpg.py`](benchmarks/ddpg.py) · **Deep-dive:** [`doc/01_ddpg.md`](doc/01_ddpg.md)

DDPG adapts DQN to continuous action spaces using two networks:

- **Actor** `μ(s; θ)` — deterministic policy mapping states to actions.
- **Critic** `Q(s, a; φ)` — action-value estimator trained with Bellman targets.

Exploration is added at inference time by injecting Gaussian noise onto the
actor's output.  A **replay buffer** breaks temporal correlation, and **target
networks** (Polyak-updated with `τ = 0.005`) stabilise training.

| Component | Class / function |
|-----------|-----------------|
| Hyperparameters | `DDPGConfig` |
| Policy network | `Actor` (2-layer MLP, `tanh` output) |
| Value network | `Critic` (2-layer MLP, state ‖ action input) |
| Training loop | `run_ddpg(config)` |

---

### TD3 — Twin Delayed Deep Deterministic Policy Gradient

**Paper:** Fujimoto et al. (2018) — [arXiv:1802.09477](https://arxiv.org/abs/1802.09477)  
**Implementation:** [`benchmarks/td3.py`](benchmarks/td3.py) · **Deep-dive:** [`doc/02_td3.md`](doc/02_td3.md)

TD3 improves DDPG with three targeted fixes for Q-value overestimation and
actor–critic instability:

| Fix | Mechanism | Config field |
|-----|-----------|--------------|
| **1. Clipped double-Q** | Two independent critics; Bellman target uses `min(Q1, Q2)` | — |
| **2. Delayed actor updates** | Actor and targets update every `policy_delay` critic steps | `policy_delay=2` |
| **3. Target policy smoothing** | Clipped Gaussian noise on the target actor's action | `policy_noise=0.2`, `noise_clip=0.5` |

| Component | Class / function |
|-----------|-----------------|
| Hyperparameters | `TD3Config` |
| Policy network | `Actor` (same architecture as DDPG) |
| Value networks | `TwinCritic` (Q1 + Q2 heads, `q1_only()` for actor update) |
| Training loop | `run_td3(config)` |

---

### SAC — Soft Actor-Critic

**Paper:** Haarnoja et al. (2018) — [arXiv:1801.01290](https://arxiv.org/abs/1801.01290)  
**Implementation:** [`benchmarks/sac.py`](benchmarks/sac.py) · **Deep-dive:** [`doc/03_sac.md`](doc/03_sac.md)

SAC maximises a **entropy-regularised** objective:

$$J = \mathbb{E}\!\left[\sum_t \gamma^t \bigl(r_t + \alpha\,H(\pi(\cdot|s_t))\bigr)\right]$$

The temperature `α` balances reward maximisation against entropy (exploration).
Unlike DDPG/TD3, the policy is **stochastic** — a Gaussian parameterised by mean and
log-std — which naturally regularises the Q surface and removes the need for a target
actor or explicit exploration noise.

Key design differences from TD3:

- **No actor target network** — the stochastic policy self-regularises.
- **Entropy term in the Bellman backup** — target includes `−α * log π(a'|s')`.
- **Actor loss** = `(α * log π(a|s) − min(Q1, Q2)(s, a)).mean()`
- **Tanh log-prob correction** — `log π_squashed = log π_Gaussian − Σ log(1 − tanh²(z) + ε)`

| Component | Class / function |
|-----------|-----------------|
| Hyperparameters | `SACConfig` |
| Policy network | `GaussianActor` (shared backbone + `mean` head + `log_std` head) |
| Value networks | `TwinCritic` (Q1 + Q2, no `q1_only`) |
| Training loop | `run_sac(config)` |

---

## Quick start

**Prerequisites:** Python 3.11+, [`uv`](https://github.com/astral-sh/uv)

```bash
# Install dependencies
uv sync
```

### Standalone benchmarks

Each script exposes the full hyperparameter set via CLI:

```bash
uv run python ddpg_benchmark.py
uv run python td3_benchmark.py
uv run python sac_benchmark.py
```

Example — override episodes and seed:

```bash
uv run python sac_benchmark.py --episodes 200 --seed 1
```

Record evaluation videos after training:

```bash
uv run python ddpg_benchmark.py --record-video --video-dir videos/ddpg --video-episodes 3
```

### Comparison runner

Run all three algorithms back-to-back and write a unified result file:

```bash
uv run python run_all_comparison.py
# or equivalently:
uv run python rl_comparison.py
```

Run a subset of methods:

```bash
uv run python run_all_comparison.py --methods td3 sac
```

Common options:

| Flag | Default | Description |
|------|---------|-------------|
| `--seed` | `42` | Global random seed |
| `--env-name` | `Pendulum-v1` | Gymnasium environment ID |
| `--methods` | all | Space-separated list: `ddpg td3 sac` |
| `--output-dir` | `outputs` | Directory for result files |
| `--ddpg-episodes` / `--td3-episodes` / `--sac-episodes` | `160` each | Per-algorithm episode budget |
| `--max-steps` | `200` | Max steps per episode |
| `--warmup-steps` | `5000` | Random-action steps before first update |
| `--batch-size` | `256` | Mini-batch size |
| `--strict` | off | Stop on first algorithm failure |
| `--record-video` | off | Record evaluation episodes |
| `--video-dir` | `videos` | Base directory for videos |

Outputs written to `--output-dir`:

```
outputs/
├── comparison_results.json   ← list of BenchmarkResult dicts
├── comparison_results.csv    ← same data in tabular form
└── comparison_errors.json    ← any algorithms that raised exceptions
```

---

## Post-processing tools

### `scripts/aggregate_results.py` — Multi-seed aggregation

Reads one or more `comparison_results.json` files (typically from different seeds
or runs), groups records by algorithm, and computes **mean ± std** across seeds for
all metrics: `episodes`, `elapsed_sec`, `max_avg_reward_100`, `final_avg_reward_100`.

```bash
# Single run
uv run python scripts/aggregate_results.py \
    --inputs outputs/comparison_results.json \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv

# Multi-seed: glob or explicit list
uv run python scripts/aggregate_results.py \
    --inputs "outputs/seed*/comparison_results.json" \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv
```

| Flag | Default | Description |
|------|---------|-------------|
| `--inputs` | required | Files, directories, or glob patterns |
| `--output-json` | `outputs/aggregate_summary.json` | Aggregated JSON output |
| `--output-csv` | `outputs/aggregate_summary.csv` | Aggregated CSV output |
| `--strict` | off | Fail if any input path does not resolve |

**Output schema** (one object per algorithm):

```json
{
  "algo": "SAC",
  "runs": 3,
  "episodes_mean": 160.0,      "episodes_std": 0.0,
  "elapsed_sec_mean": 42.1,    "elapsed_sec_std": 1.2,
  "max_avg_reward_100_mean": -180.5,  "max_avg_reward_100_std": 8.3,
  "final_avg_reward_100_mean": -210.0, "final_avg_reward_100_std": 12.1
}
```

---

### `scripts/generate_aggregate_report.py` — Plots and Markdown report

Reads the `aggregate_summary.json` produced by the previous step and generates:

- **4 plots** (PNG, 150 dpi): max reward bar chart, final reward bar chart, elapsed-time
  bar chart, performance-vs-time scatter plot.
- **`aggregate_report.md`** — Markdown report with leaderboard table, embedded plot
  links, and key observations.

```bash
uv run python scripts/generate_aggregate_report.py \
    --input     outputs/aggregate_summary.json \
    --output-dir outputs/report \
    --title     "RL Continuous Control — Seed 42"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--input` | `outputs/aggregate_summary.json` | Aggregated summary JSON |
| `--output-dir` | `outputs/report` | Output directory for report and plots |
| `--title` | `RL Continuous Control Aggregate Report` | Report heading |

Output layout:

```
outputs/report/
├── aggregate_report.md
└── plots/
    ├── max_avg_reward_100.png
    ├── final_avg_reward_100.png
    ├── elapsed_seconds.png
    └── performance_vs_time.png
```

**Efficiency metric** in the leaderboard = `max_avg_reward_100_mean / elapsed_sec_mean`.
Higher is better: rewards the algorithm that achieves the best performance per unit time.

---

## Multi-seed workflow

Running multiple seeds produces statistically meaningful comparisons.  The
recommended pattern:

```bash
# Run three seeds, writing to separate directories
uv run python run_all_comparison.py --seed 1 --output-dir outputs/seed1
uv run python run_all_comparison.py --seed 2 --output-dir outputs/seed2
uv run python run_all_comparison.py --seed 3 --output-dir outputs/seed3

# Aggregate
uv run python scripts/aggregate_results.py \
    --inputs outputs/seed1/comparison_results.json \
             outputs/seed2/comparison_results.json \
             outputs/seed3/comparison_results.json \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv

# Report
uv run python scripts/generate_aggregate_report.py \
    --input      outputs/aggregate_summary.json \
    --output-dir outputs/report \
    --title      "DDPG vs TD3 vs SAC — 3-seed comparison"
```

---

## Algorithm comparison

| | DDPG | TD3 | SAC |
|---|---|---|---|
| **Policy type** | Deterministic | Deterministic | Stochastic (Gaussian) |
| **Exploration** | External noise (Gaussian) | External noise | Inherent (entropy) |
| **Critics** | Single Q | Twin Q (min target) | Twin Q (min target) |
| **Actor target** | Yes | Yes | No |
| **Target smoothing** | No | Yes (`policy_noise`) | No (not needed) |
| **Delayed updates** | No | Yes (`policy_delay=2`) | No |
| **Entropy bonus** | No | No | Yes (`alpha`) |
| **Sample efficiency** | Moderate | High | Highest |
| **Tuning sensitivity** | High | Medium | Lower |

---

## Documentation

| File | Contents |
|------|----------|
| [`doc/01_ddpg.md`](doc/01_ddpg.md) | DDPG theory, architecture, training loop annotated |
| [`doc/02_td3.md`](doc/02_td3.md) | TD3 three fixes explained with code references |
| [`doc/03_sac.md`](doc/03_sac.md) | SAC entropy objective, tanh correction, implementation notes |
| [`doc/presentation_guide_60min.md`](doc/presentation_guide_60min.md) | 60-min presenter guide (EN) — minute-by-minute talking points |
| [`doc/presentation_guide_60min_es.md`](doc/presentation_guide_60min_es.md) | 60-min presenter guide (ES) |
| [`benchmarks/README.md`](benchmarks/README.md) | Benchmarks package code guide |

---

## References

### DDPG
- Lillicrap et al. (2015) — *Continuous control with deep reinforcement learning* — [arXiv:1509.02971](https://arxiv.org/abs/1509.02971)
- [OpenAI Spinning Up — DDPG](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)
- [Deep Deterministic Policy Gradients Explained (Towards Data Science)](https://towardsdatascience.com/deep-deterministic-policy-gradients-explained-4643c1f71b2e/)

### TD3
- Fujimoto et al. (2018) — *Addressing Function Approximation Error in Actor-Critic Methods* — [arXiv:1802.09477](https://arxiv.org/abs/1802.09477)
- [OpenAI Spinning Up — TD3](https://spinningup.openai.com/en/latest/algorithms/td3.html)
- [Twin Delayed Deep Deterministic Policy Gradient (TD3) (Medium)](https://medium.com/@heyamit10/twin-delayed-deep-deterministic-policy-gradient-td3-fc8e9950f029)

### SAC
- Haarnoja et al. (2018) — *Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning* — [arXiv:1801.01290](https://arxiv.org/abs/1801.01290)
- [OpenAI Spinning Up — SAC](https://spinningup.openai.com/en/latest/algorithms/sac.html)
- [Soft Actor-Critic Demystified (Towards Data Science)](https://towardsdatascience.com/soft-actor-critic-demystified-b8427df61665/)
