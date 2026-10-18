# RL Libraries: An Ecosystem Tour & an Applied Trading Agent

*[Leer en español](README_es.md)*

> **Session 7 of the RL course.** Previous sessions built the algorithms from
> scratch (MDPs, Q-learning/DQN, policy gradient / A2C / PPO / TRPO, and the
> continuous-control family DDPG/TD3/SAC). This session pivots from theory to
> tooling: we survey the Python RL ecosystem, then use
> [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) to rebuild a
> stock-trading agent on live [yfinance](https://github.com/ranaroussi/yfinance)
> data — and close with a MuJoCo `HalfCheetah-v5` demo to tie the stack together.

Prior course material: [`Introduction_to_RL`](../Introduction_to_RL),
[`rl_q_learning`](../rl_q_learning),
[`rl_policy_optimization`](../rl_policy_optimization),
[`rl_hybrid_algorithms`](../rl_hybrid_algorithms).

---

## What's inside

```
rl_libraries/
├── doc/                           ← presenter guide + deep dives (EN + ES)
│   ├── README.md                  ← index
│   ├── presentation_guide_60min.md
│   ├── presentation_guide_60min_es.md
│   ├── 01_rl_libraries_overview.md
│   ├── 02_sb3_in_depth.md
│   ├── 03_yfinance_trading_env.md
│   └── es/                        ← Spanish translations of deep dives
│
├── lib/
│   ├── environ.py                 ← custom Gymnasium env (Skip / Buy / Close)
│   ├── yf_data.py                 ← yfinance loader with on-disk Parquet cache
│   ├── data.py                    ← Prices dataclass + relative-price helpers
│   └── models.py                  ← reference DQN architectures (used for slides)
│
├── tests/                         ← offline unit tests (no network calls)
│
├── train_sb3.py                   ← PPO / DQN trainer on the trading env
├── run_sb3.py                     ← deterministic backtest + equity curve
├── mujoco_demo.py                 ← SAC on MuJoCo HalfCheetah-v5 / Walker2d-v5 / Humanoid-v5 + MP4 rollout
│
├── legacy/                        ← original PTAN/Ignite DQN code
│                                    (reference only; no longer runs against this venv)
│
├── pyproject.toml                 ← dependencies (uv-managed)
└── uv.lock
```

---

## Quick start

```bash
# 1. Install dependencies (uses uv)
uv sync

# 2. Run the offline tests
uv run pytest tests/

# 3. Train PPO on AAPL + MSFT + GOOGL
uv run python train_sb3.py --algo ppo \
    --tickers AAPL,MSFT,GOOGL \
    --train-start 2018-01-01 --train-end 2023-01-01 \
    --val-start 2023-01-01 --val-end 2024-01-01 \
    --timesteps 200000 --run-name ppo-tech

# 4. Train DQN on the same data (same flags, one switch)
uv run python train_sb3.py --algo dqn \
    --tickers AAPL,MSFT,GOOGL \
    --train-start 2018-01-01 --train-end 2023-01-01 \
    --val-start 2023-01-01 --val-end 2024-01-01 \
    --timesteps 200000 --run-name dqn-tech

# 5. Watch training in TensorBoard
tensorboard --logdir runs/

# 6. Backtest the best model on unseen 2024 data
uv run python run_sb3.py --algo ppo \
    --model saves/ppo-tech/best_model.zip \
    --ticker AAPL --start 2024-01-01 --end 2025-01-01 \
    --name ppo_aapl_2024


# 7. Bonus: train SAC on MuJoCo — pick any of the three supported envs
uv run python mujoco_demo.py --env HalfCheetah-v5 --timesteps 100000
uv run python mujoco_demo.py --env Walker2d-v5    --timesteps 200000
uv run python mujoco_demo.py --env Humanoid-v5    --timesteps 500000
```

---

## Where the interesting code lives

| Concern | File | Notes |
|---------|------|-------|
| Market data download + cache | [`lib/yf_data.py`](lib/yf_data.py) | Parquet-backed, offline-reproducible |
| Trading environment | [`lib/environ.py`](lib/environ.py) | Skip/Buy/Close discrete actions, open-relative observations |
| PPO & DQN trainer | [`train_sb3.py`](train_sb3.py) | VecEnv + EvalCallback + TensorBoard |
| Backtest & equity curve | [`run_sb3.py`](run_sb3.py) | Deterministic rollout vs. buy-and-hold baseline |
| MuJoCo demo | [`mujoco_demo.py`](mujoco_demo.py) | SAC on HalfCheetah-v5 / Walker2d-v5 / Humanoid-v5 via `--env`, MP4 rollout |

---

## Key libraries used

- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) 2.7.x — default RL library
- [SB3-Contrib](https://sb3-contrib.readthedocs.io/) — extended algorithms (TQC, TRPO, QR-DQN, RecurrentPPO, ...)
- [Gymnasium](https://gymnasium.farama.org/) 1.2.x — environment standard
- [MuJoCo](https://mujoco.readthedocs.io/) 3.x — physics engine for HalfCheetah
- [yfinance](https://github.com/ranaroussi/yfinance) — Yahoo Finance OHLCV data
- [PyTorch](https://pytorch.org/) 2.x — neural-net backend
- [TensorBoard](https://www.tensorflow.org/tensorboard) — training-curve visualisation

See [`doc/01_rl_libraries_overview.md`](doc/01_rl_libraries_overview.md)
for the full ecosystem map.

---

## Documentation

English:
- [Presenter guide (60 min)](doc/presentation_guide_60min.md)
- [Deep dive 1: RL library landscape](doc/01_rl_libraries_overview.md)
- [Deep dive 2: Stable-Baselines3 in depth](doc/02_sb3_in_depth.md)
- [Deep dive 3: yfinance trading environment](doc/03_yfinance_trading_env.md)

Español:
- [Guía del ponente (60 min)](doc/presentation_guide_60min_es.md)
- [Profundización 1: panorama de librerías de RL](doc/es/01_rl_libraries_overview.md)
- [Profundización 2: Stable-Baselines3 en profundidad](doc/es/02_sb3_in_depth.md)
- [Profundización 3: entorno de trading con yfinance](doc/es/03_yfinance_trading_env.md)

---

## License

This repository is the author's course material and is distributed under the
same terms as the other sibling repositories in the course.
