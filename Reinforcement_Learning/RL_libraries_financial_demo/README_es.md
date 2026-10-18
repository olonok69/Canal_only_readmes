# Librerías de RL: un recorrido por el ecosistema y un agente de trading aplicado

> **Sesión 7 del curso de RL.** Las sesiones anteriores construyeron los algoritmos
> desde cero (MDPs, Q-learning/DQN, gradiente de política / A2C / PPO / TRPO, y la
> familia de control continuo DDPG/TD3/SAC). Esta sesión cambia de la teoría a las
> herramientas: recorremos el ecosistema de RL en Python, luego usamos
> [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) para reconstruir
> un agente de trading bursátil sobre datos en vivo de
> [yfinance](https://github.com/ranaroussi/yfinance) — y cerramos con una demo de
> MuJoCo `HalfCheetah-v5` para engarzar todo el stack.

Material previo del curso: [`Introduction_to_RL`](../Introduction_to_RL),
[`rl_q_learning`](../rl_q_learning),
[`rl_policy_optimization`](../rl_policy_optimization),
[`rl_hybrid_algorithms`](../rl_hybrid_algorithms).

---

## Qué hay dentro

```
rl_libraries/
├── doc/                           ← guía del ponente + análisis profundos (EN + ES)
│   ├── README.md                  ← índice
│   ├── presentation_guide_60min.md
│   ├── presentation_guide_60min_es.md
│   ├── 01_rl_libraries_overview.md
│   ├── 02_sb3_in_depth.md
│   ├── 03_yfinance_trading_env.md
│   └── es/                        ← traducciones al español de los análisis profundos
│
├── lib/
│   ├── environ.py                 ← entorno Gymnasium personalizado (Skip / Buy / Close)
│   ├── yf_data.py                 ← cargador de yfinance con caché Parquet en disco
│   ├── data.py                    ← dataclass Prices + helpers de precios relativos
│   └── models.py                  ← arquitecturas DQN de referencia (usadas en las diapositivas)
│
├── tests/                         ← pruebas unitarias offline (sin llamadas de red)
│
├── train_sb3.py                   ← entrenador PPO / DQN sobre el entorno de trading
├── run_sb3.py                     ← backtest determinista + curva de equity
├── mujoco_demo.py                 ← SAC sobre MuJoCo HalfCheetah-v5 / Walker2d-v5 / Humanoid-v5 + rollout MP4
│
├── legacy/                        ← código DQN original con PTAN/Ignite
│                                    (solo referencia; ya no corre con este venv)
│
├── pyproject.toml                 ← dependencias (gestionadas con uv)
└── uv.lock
```

---

## Inicio rápido

```bash
# 1. Instalar dependencias (usa uv)
uv sync

# 2. Ejecutar las pruebas offline
uv run pytest tests/

# 3. Entrenar PPO sobre AAPL + MSFT + GOOGL
uv run python train_sb3.py --algo ppo \
    --tickers AAPL,MSFT,GOOGL \
    --train-start 2018-01-01 --train-end 2023-01-01 \
    --val-start 2023-01-01 --val-end 2024-01-01 \
    --timesteps 200000 --run-name ppo-tech

# 4. Entrenar DQN con los mismos datos (mismas banderas, un solo cambio)
uv run python train_sb3.py --algo dqn \
    --tickers AAPL,MSFT,GOOGL \
    --train-start 2018-01-01 --train-end 2023-01-01 \
    --val-start 2023-01-01 --val-end 2024-01-01 \
    --timesteps 200000 --run-name dqn-tech

# 5. Visualizar el entrenamiento en TensorBoard
tensorboard --logdir runs/

# 6. Backtest del mejor modelo sobre datos no vistos de 2024
uv run python run_sb3.py --algo ppo \
    --model saves/ppo-tech/best_model.zip \
    --ticker AAPL --start 2024-01-01 --end 2025-01-01 \
    --name ppo_aapl_2024


# 7. Extra: entrenar SAC sobre MuJoCo — elige cualquiera de los tres entornos soportados
uv run python mujoco_demo.py --env HalfCheetah-v5 --timesteps 100000
uv run python mujoco_demo.py --env Walker2d-v5    --timesteps 200000
uv run python mujoco_demo.py --env Humanoid-v5    --timesteps 500000
```

---

## Dónde vive el código interesante

| Aspecto | Archivo | Notas |
|---------|---------|-------|
| Descarga + caché de datos de mercado | [`lib/yf_data.py`](lib/yf_data.py) | Respaldado por Parquet, reproducible offline |
| Entorno de trading | [`lib/environ.py`](lib/environ.py) | Acciones discretas Skip/Buy/Close, observaciones relativas al open |
| Entrenador PPO y DQN | [`train_sb3.py`](train_sb3.py) | VecEnv + EvalCallback + TensorBoard |
| Backtest y curva de equity | [`run_sb3.py`](run_sb3.py) | Rollout determinista vs. línea base buy-and-hold |
| Demo de MuJoCo | [`mujoco_demo.py`](mujoco_demo.py) | SAC sobre HalfCheetah-v5 / Walker2d-v5 / Humanoid-v5 via `--env`, rollout MP4 |

---

## Librerías clave utilizadas

- [Stable-Baselines3](https://stable-baselines3.readthedocs.io/) 2.7.x — librería de RL por defecto
- [SB3-Contrib](https://sb3-contrib.readthedocs.io/) — algoritmos extendidos (TQC, TRPO, QR-DQN, RecurrentPPO, ...)
- [Gymnasium](https://gymnasium.farama.org/) 1.2.x — estándar de entornos
- [MuJoCo](https://mujoco.readthedocs.io/) 3.x — motor físico para HalfCheetah
- [yfinance](https://github.com/ranaroussi/yfinance) — datos OHLCV de Yahoo Finance
- [PyTorch](https://pytorch.org/) 2.x — backend de redes neuronales
- [TensorBoard](https://www.tensorflow.org/tensorboard) — visualización de curvas de entrenamiento

Consulta [`doc/01_rl_libraries_overview.md`](doc/01_rl_libraries_overview.md)
para el mapa completo del ecosistema (o
[`doc/es/01_rl_libraries_overview.md`](doc/es/01_rl_libraries_overview.md)
para la versión en español).

---

## Documentación

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

## Licencia

Este repositorio es el material de curso del autor y se distribuye bajo los
mismos términos que los demás repositorios hermanos del curso.
