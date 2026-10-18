# RL Policy Optimization Benchmarks

Multi-algorithm reinforcement learning benchmark suite on `CartPole-v1`, with independent scripts per method and a unified comparison runner.

## Presentation series
This repository is prepared for a **two-part presentation series**:
- **Part 1**: Detailed introduction to Policy Optimization, Monte Carlo, and REINFORCE → [Presentation guide](doc/presentation_guide_60min.md)
- **Part 2**: A2C, A3C, PPO, TRPO and comparison workflow → [Presentation guide](doc/presentation_guide_part2_60min.md)

## Scope
This repository includes policy-optimization methods:
- Policy Gradient (REINFORCE)
- A2C
- A3C
- PPO
- TRPO

## Documentation
Comprehensive algorithm guides with theory, implementation walkthroughs, and code mapping:

| Guide | Description |
|-------|-------------|
| [doc/03_policy_gradient.md](doc/03_policy_gradient.md) | Policy Gradient (REINFORCE) foundations and implementation details |
| [doc/04_a2c.md](doc/04_a2c.md) | Advantage Actor-Critic explanation and training flow |
| [doc/05_a3c.md](doc/05_a3c.md) | Asynchronous actor-critic architecture and worker/learner interaction |
| [doc/06_ppo.md](doc/06_ppo.md) | PPO clipped objective, GAE, and update loop |
| [doc/07_trpo.md](doc/07_trpo.md) | TRPO trust-region intuition and benchmark integration |
| [doc/README.md](doc/README.md) | Full documentation index |

## Book-based documentation
Detailed algorithm writeups grounded in:
`doc/Deep Reinforcement Learning Hands-On_ Apply modern RL methods to practical problems of chatbots, robotics, discrete optimization, web automation, and more, 2nd Edition-Packt Publishing.pdf`

See the index: [doc/README.md](doc/README.md)

Spanish version of this file: [README_es.md](README_es.md)

## Install
Using `uv`:

```bash
uv sync
```

## Run single method (independent)
Each algorithm has its own standalone script:

```bash
uv run python policy_gradient_benchmark.py
uv run python a2c_benchmark.py
uv run python a3c_benchmark.py
uv run python ppo_benchmark.py
uv run python trpo_benchmark.py
```

Method scripts support configurable hyperparameters. Example:

```bash
uv run python ppo_benchmark.py --episodes 700 --rollout-steps 2048 --update-epochs 6
uv run python a3c_benchmark.py --episodes 600 --workers 8 --rollout-steps 10
uv run python trpo_benchmark.py --timesteps 200000
```

## Run all methods together
Unified orchestrator:

```bash
uv run python run_all_comparison.py
```

Run selected methods only:

```bash
uv run python run_all_comparison.py --methods policy_gradient ppo trpo
```

With video recording:

```bash
uv run python run_all_comparison.py --methods policy_gradient ppo --record-video --video-dir videos --video-episodes 3
```

Override per-method training budgets from the orchestrator:

```bash
uv run python run_all_comparison.py --methods policy_gradient a2c a3c ppo trpo --policy-gradient-episodes 700 --a2c-episodes 600 --a3c-episodes 600 --ppo-episodes 700 --trpo-timesteps 200000
```

Strict mode (stop on first failure):

```bash
uv run python run_all_comparison.py --strict
```

## Outputs
`run_all_comparison.py` writes:
- `outputs/comparison_results.json`
- `outputs/comparison_results.csv`
- `outputs/comparison_errors.json`

## Recommended experiment protocol
For fair and reproducible comparisons across methods:

1. **Use multiple seeds**
   - Run each method with at least 3-5 different seeds.
   - Example: `--seed 1`, `--seed 2`, `--seed 3`.

2. **Keep budgets aligned**
   - Match training budget as closely as possible (episodes or timesteps).
   - Report budget differences explicitly when methods require different rollout styles.

3. **Report distribution, not single runs**
   - Aggregate `max_avg_reward_100` and `final_avg_reward_100` as mean ± std across seeds.
   - Keep raw per-run outputs in `outputs/` for traceability.

4. **Use a quick smoke-test before full runs**
   - First run a small subset of methods to validate environment/dependencies.
   - Then launch the full benchmark matrix.

5. **Track failures separately**
   - Review `comparison_errors.json` and do not silently drop failed methods from reports.

## Aggregate multi-seed results
Use the helper script to aggregate several benchmark JSON outputs into per-algorithm mean/std:

```bash
uv run python scripts/aggregate_results.py --inputs outputs/*.json --output-json outputs/aggregate_summary.json --output-csv outputs/aggregate_summary.csv
```

You can also pass multiple explicit files or directories:

```bash
uv run python scripts/aggregate_results.py --inputs runs/seed1 runs/seed2 outputs/comparison_results.json
```

Generate plots + Markdown report from aggregated summary:

```bash
uv run python scripts/generate_aggregate_report.py --input outputs/aggregate_summary.json --output-dir outputs/report --title "RL Policy Optimization Aggregate Report"
```

## Main files
- `run_all_comparison.py`: unified multi-method benchmark runner
- `rl_comparison.py`: compatibility entrypoint to unified comparison
- `benchmarks/`: reusable algorithm modules and shared benchmark utilities
- `doc/`: algorithm documentation and source PDF

## Spanish documentation
- Root guide (ES): [README_es.md](README_es.md)
- Presentation guide (ES): [doc/presentation_guide_60min_es.md](doc/presentation_guide_60min_es.md)
- Algorithm docs (ES): [doc/es/README.md](doc/es/README.md)

## Notes
- TRPO uses `sb3-contrib` implementation (`benchmarks/trpo.py`).
- A3C uses multiprocessing and can consume significant CPU.
- For fair comparisons, keep seeds and environment settings consistent.
