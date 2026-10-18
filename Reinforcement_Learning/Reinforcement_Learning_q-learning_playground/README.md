# RL Q-Learning Benchmarks

<p align="center">
  <img src="doc/images/q_learning_cover.svg" alt="Q-Learning Cover" width="45%" />
  <img src="doc/images/dqn_cover.svg" alt="DQN Cover" width="45%" />
</p>

Complete reinforcement learning repository centered on the **Q-Learning family** of methods. The runnable benchmark suite focuses mainly on `CartPole-v1`, and the repository has evolved from tabular Q-Learning and a core DQN baseline into a broader collection of DQN extensions, advanced value-based variants, reporting utilities, and bilingual documentation.

## What this repository contains

| Area | Contents |
|------|----------|
| Benchmark runners | Standalone entry scripts for Q-Learning, DQN, Double DQN, Dueling DQN, Noisy DQN, Prioritized Replay, N-step, C51, QR-DQN, Rainbow, and HER |
| Core implementation package | `benchmarks/` with reusable configs, training loops, replay logic, evaluation helpers, and shared result utilities |
| Comparison tooling | `run_all_comparison.py`, `run_phase1_comparison.py`, and `rl_comparison.py` for orchestrated experiments |
| Reporting scripts | `scripts/aggregate_results.py` and `scripts/generate_aggregate_report.py` for multi-run summaries and charts |
| Reference code | `DQN Extensions/`, `DQN Q-Networks/`, and `Q-learning-Advanced/` with earlier or exploratory implementations |
| Documentation | English and Spanish algorithm notes under `doc/` and `doc/es/` |
| Generated artifacts | Example outputs under `outputs/`, tracked runs under `runs/`, and evaluation recordings under `videos/` |

## Implemented methods

- **Tabular Q-Learning**
- **DQN**
- **Double DQN**
- **Dueling DQN**
- **Noisy DQN**
- **Prioritized Experience Replay**
- **N-step DQN**
- **C51**
- **QR-DQN**
- **Rainbow DQN**
- **HER**

## Installation
Using `uv`:

```bash
uv sync
```

## Run individual benchmarks
Each method has its own top-level script:

```bash
uv run python q_learning_benchmark.py
uv run python dqn_benchmark.py
uv run python dqn_double_benchmark.py
uv run python dqn_dueling_benchmark.py
uv run python dqn_noisy_benchmark.py
uv run python dqn_prio_replay_benchmark.py
uv run python dqn_n_steps_benchmark.py
uv run python dqn_c51_benchmark.py
uv run python dqn_qr_benchmark.py
uv run python dqn_rainbow_benchmark.py
uv run python her_benchmark.py
```

To record evaluation videos or display training plots:

```bash
uv run python dqn_benchmark.py --record-video --plot
```

## Run the full comparison suite
Run all registered methods:

```bash
uv run python run_all_comparison.py
```

Run a selected subset:

```bash
uv run python run_all_comparison.py --methods q_learning dqn dqn_double
```

Stop on the first failure:

```bash
uv run python run_all_comparison.py --strict
```

## Output artifacts
Typical generated files include:

- `outputs/comparison_results.json`
- `outputs/comparison_results.csv`
- `outputs/comparison_errors.json`
- `outputs/aggregate_summary.json`
- `outputs/aggregate_summary.csv`
- `outputs/report/` for generated reports and plots
- `videos/` for recorded evaluations
- `runs/` for stored run data

## Repository layout

- `benchmarks/` — main benchmark implementations used by the root runners
- `scripts/` — result aggregation and reporting helpers
- `doc/` — English algorithm documentation and illustrations
- `doc/es/` — Spanish algorithm documentation
- `DQN Extensions/` — extension-focused reference implementations and small experiments
- `DQN Q-Networks/` — foundational examples including FrozenLake Q-Learning and DQN Pong
- `Q-learning-Advanced/` — advanced or archived experimental material for distributional and Rainbow variants
- `outputs/`, `runs/`, `videos/` — generated experiment artifacts

## Documentation

- English documentation index: [doc/README.md](doc/README.md)
- Spanish documentation index: [doc/es/README.md](doc/es/README.md)
- Spanish root overview: [README_es.md](README_es.md)

## Notes

- All benchmarked methods are connected by the same value-based learning lineage.
- The main comparison workflow is built around reproducible, scriptable benchmark runs and post-run aggregation.
- Besides the benchmark suite, the repository also preserves reference and exploratory implementations from earlier development stages.
