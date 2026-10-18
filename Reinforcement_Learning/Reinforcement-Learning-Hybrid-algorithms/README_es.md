# RL Control Continuo: Métodos Actor-Critic Off-Policy

> **DDPG · TD3 · SAC** — desde el baseline original de Lillicrap (2015) hasta el
> framework de regularización por entropía de Haarnoja (2018), todo en una suite de
> benchmarks reproducible y auto-contenida.

Este repositorio implementa y compara tres algoritmos actor-critic off-policy fundamentales
para **reinforcement learning con espacios de acción continuos**. Cada algoritmo está
documentado línea a línea, evaluado sobre `Pendulum-v1`, e integrado en un toolchain
compartido de agregación multi-seed y generación automática de reportes.

---


## Estructura del repositorio

```
rl_hybrid_algorithms/
├── benchmarks/                ← implementaciones reutilizables de los algoritmos
│   ├── __init__.py            ← re-exports públicos
│   ├── common.py              ← BenchmarkResult, métricas, seed control, helper de video
│   ├── replay_buffer.py       ← experience buffer off-policy compartido (los tres algos)
│   ├── ddpg.py                ← DDPGConfig · Actor · Critic · run_ddpg()
│   ├── td3.py                 ← TD3Config  · Actor · TwinCritic · run_td3()
│   └── sac.py                 ← SACConfig  · GaussianActor · TwinCritic · run_sac()
│
├── doc/                       ← documentación en profundidad de algoritmos y guías
│   ├── 01_ddpg.md             ← DDPG: teoría, arquitectura, ecuaciones clave
│   ├── 02_td3.md              ← TD3: los tres fixes explicados en detalle
│   ├── 03_sac.md              ← SAC: objetivo de entropía, reparametrización, corrección tanh
│   ├── presentation_guide_60min.md    ← guía de presentación 60 min (EN)
│   ├── presentation_guide_60min_es.md ← guía de presentación 60 min (ES)
│   └── es/                    ← traducciones al español de los deep-dives
│
├── algorithms/                ← implementaciones de referencia (código original del paper TD3)
│
├── scripts/
│   ├── aggregate_results.py       ← agregación de resultados multi-seed
│   └── generate_aggregate_report.py ← plots + reporte Markdown desde datos agregados
│
├── outputs/                   ← resultados de benchmark (creado automáticamente en runtime)
│
├── ddpg_benchmark.py          ← runner standalone de DDPG con CLI completo
├── td3_benchmark.py           ← runner standalone de TD3 con CLI completo
├── sac_benchmark.py           ← runner standalone de SAC con CLI completo
├── rl_comparison.py           ← entry point delegante → llama a run_all_comparison
└── run_all_comparison.py      ← orquestador de comparación unificada
```

---

## Algoritmos

### DDPG — Deep Deterministic Policy Gradient

**Paper:** Lillicrap et al. (2015) — [arXiv:1509.02971](https://arxiv.org/abs/1509.02971)  
**Implementación:** [`benchmarks/ddpg.py`](benchmarks/ddpg.py) · **Deep-dive:** [`doc/01_ddpg.md`](doc/01_ddpg.md)

DDPG adapta DQN a espacios de acción continuos usando dos redes:

- **Actor** `μ(s; θ)` — policy determinista que mapea estados a acciones.
- **Critic** `Q(s, a; φ)` — estimador de action-value entrenado con targets de Bellman.

La exploración se añade en tiempo de inferencia inyectando ruido gaussiano sobre la
salida del actor. Un **replay buffer** rompe la correlación temporal, y las **target
networks** (actualizadas con Polyak usando `τ = 0.005`) estabilizan el entrenamiento.

| Componente | Clase / función |
|------------|----------------|
| Hiperparámetros | `DDPGConfig` |
| Red de policy | `Actor` (MLP 2 capas, output `tanh`) |
| Red de valor | `Critic` (MLP 2 capas, entrada estado ‖ acción) |
| Loop de entrenamiento | `run_ddpg(config)` |

---

### TD3 — Twin Delayed Deep Deterministic Policy Gradient

**Paper:** Fujimoto et al. (2018) — [arXiv:1802.09477](https://arxiv.org/abs/1802.09477)  
**Implementación:** [`benchmarks/td3.py`](benchmarks/td3.py) · **Deep-dive:** [`doc/02_td3.md`](doc/02_td3.md)

TD3 mejora DDPG con tres fixes específicos para la sobreestimación del valor Q y la
inestabilidad del par actor-critic:

| Fix | Mecanismo | Campo de config |
|-----|-----------|----------------|
| **1. Clipped double-Q** | Dos critics independientes; el target de Bellman usa `min(Q1, Q2)` | — |
| **2. Delayed actor updates** | Actor y targets se actualizan cada `policy_delay` pasos del critic | `policy_delay=2` |
| **3. Target policy smoothing** | Ruido gaussiano acotado sobre la acción del target actor | `policy_noise=0.2`, `noise_clip=0.5` |

| Componente | Clase / función |
|------------|----------------|
| Hiperparámetros | `TD3Config` |
| Red de policy | `Actor` (misma arquitectura que DDPG) |
| Redes de valor | `TwinCritic` (cabezas Q1 + Q2, `q1_only()` para update del actor) |
| Loop de entrenamiento | `run_td3(config)` |

---

### SAC — Soft Actor-Critic

**Paper:** Haarnoja et al. (2018) — [arXiv:1801.01290](https://arxiv.org/abs/1801.01290)  
**Implementación:** [`benchmarks/sac.py`](benchmarks/sac.py) · **Deep-dive:** [`doc/03_sac.md`](doc/03_sac.md)

SAC maximiza un objetivo **regularizado por entropía**:

$$J = \mathbb{E}\!\left[\sum_t \gamma^t \bigl(r_t + \alpha\,H(\pi(\cdot|s_t))\bigr)\right]$$

La temperatura `α` balancea la maximización del reward con la entropía (exploración).
A diferencia de DDPG/TD3, la policy es **estocástica** — una Gaussiana parametrizada
por media y log-std — lo que regulariza naturalmente la superficie Q y elimina la
necesidad de un target actor o de ruido de exploración explícito.

Diferencias clave de diseño respecto a TD3:

- **Sin target actor** — la policy estocástica se auto-regulariza.
- **Término de entropía en el Bellman backup** — el target incluye `−α * log π(a'|s')`.
- **Actor loss** = `(α * log π(a|s) − min(Q1, Q2)(s, a)).mean()`
- **Corrección tanh del log-prob** — `log π_squashed = log π_Gaussian − Σ log(1 − tanh²(z) + ε)`

| Componente | Clase / función |
|------------|----------------|
| Hiperparámetros | `SACConfig` |
| Red de policy | `GaussianActor` (backbone compartido + cabeza `mean` + cabeza `log_std`) |
| Redes de valor | `TwinCritic` (Q1 + Q2, sin `q1_only`) |
| Loop de entrenamiento | `run_sac(config)` |

---

## Quick start

**Prerequisitos:** Python 3.11+, [`uv`](https://github.com/astral-sh/uv)

```bash
# Instalar dependencias
uv sync
```

### Benchmarks individuales

Cada script expone el conjunto completo de hiperparámetros vía CLI:

```bash
uv run python ddpg_benchmark.py
uv run python td3_benchmark.py
uv run python sac_benchmark.py
```

Ejemplo — sobreescribir episodes y seed:

```bash
uv run python sac_benchmark.py --episodes 200 --seed 1
```

Grabar videos de evaluación tras el entrenamiento:

```bash
uv run python ddpg_benchmark.py --record-video --video-dir videos/ddpg --video-episodes 3
```

### Runner de comparación

Ejecuta los tres algoritmos en secuencia y escribe un archivo de resultados unificado:

```bash
uv run python run_all_comparison.py
# equivalente:
uv run python rl_comparison.py
```

Ejecutar sólo un subconjunto de métodos:

```bash
uv run python run_all_comparison.py --methods td3 sac
```

Opciones comunes:

| Flag | Default | Descripción |
|------|---------|-------------|
| `--seed` | `42` | Seed global aleatorio |
| `--env-name` | `Pendulum-v1` | ID del entorno Gymnasium |
| `--methods` | todos | Lista separada por espacios: `ddpg td3 sac` |
| `--output-dir` | `outputs` | Directorio para los archivos de resultados |
| `--ddpg-episodes` / `--td3-episodes` / `--sac-episodes` | `160` cada uno | Presupuesto de episodes por algoritmo |
| `--max-steps` | `200` | Máximo de steps por episode |
| `--warmup-steps` | `5000` | Steps de acción aleatoria antes del primer update |
| `--batch-size` | `256` | Tamaño del mini-batch |
| `--strict` | off | Detener en el primer fallo de algoritmo |
| `--record-video` | off | Grabar episodes de evaluación |
| `--video-dir` | `videos` | Directorio base para los videos |

Salidas escritas en `--output-dir`:

```
outputs/
├── comparison_results.json   ← lista de dicts BenchmarkResult
├── comparison_results.csv    ← los mismos datos en forma tabular
└── comparison_errors.json    ← algoritmos que lanzaron excepciones
```

---

## Herramientas de post-procesado

### `scripts/aggregate_results.py` — Agregación multi-seed

Lee uno o más archivos `comparison_results.json` (típicamente de diferentes seeds o
ejecuciones), agrupa los registros por algoritmo y calcula **media ± desviación estándar**
entre seeds para todas las métricas: `episodes`, `elapsed_sec`, `max_avg_reward_100`,
`final_avg_reward_100`.

```bash
# Ejecución única
uv run python scripts/aggregate_results.py \
    --inputs outputs/comparison_results.json \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv

# Multi-seed: glob o lista explícita
uv run python scripts/aggregate_results.py \
    --inputs "outputs/seed*/comparison_results.json" \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv
```

| Flag | Default | Descripción |
|------|---------|-------------|
| `--inputs` | requerido | Archivos, directorios o patrones glob |
| `--output-json` | `outputs/aggregate_summary.json` | Salida JSON agregada |
| `--output-csv` | `outputs/aggregate_summary.csv` | Salida CSV agregada |
| `--strict` | off | Fallar si algún input path no se resuelve |

**Schema de salida** (un objeto por algoritmo):

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

### `scripts/generate_aggregate_report.py` — Plots y reporte Markdown

Lee el `aggregate_summary.json` producido por el paso anterior y genera:

- **4 plots** (PNG, 150 dpi): bar chart de max reward, bar chart de final reward, bar
  chart de tiempo transcurrido, scatter de performance vs tiempo.
- **`aggregate_report.md`** — reporte Markdown con tabla de leaderboard, links a los
  plots y observaciones clave.

```bash
uv run python scripts/generate_aggregate_report.py \
    --input     outputs/aggregate_summary.json \
    --output-dir outputs/report \
    --title     "RL Control Continuo — Seed 42"
```

| Flag | Default | Descripción |
|------|---------|-------------|
| `--input` | `outputs/aggregate_summary.json` | JSON de resumen agregado |
| `--output-dir` | `outputs/report` | Directorio de salida para reporte y plots |
| `--title` | `RL Continuous Control Aggregate Report` | Cabecera del reporte |

Layout de salida:

```
outputs/report/
├── aggregate_report.md
└── plots/
    ├── max_avg_reward_100.png
    ├── final_avg_reward_100.png
    ├── elapsed_seconds.png
    └── performance_vs_time.png
```

**Métrica de eficiencia** en el leaderboard = `max_avg_reward_100_mean / elapsed_sec_mean`.
Mayor es mejor: premia al algoritmo que alcanza mejor performance por unidad de tiempo.

---

## Workflow multi-seed

Ejecutar múltiples seeds produce comparaciones estadísticamente significativas. El
patrón recomendado:

```bash
# Ejecutar tres seeds, escribiendo en directorios separados
uv run python run_all_comparison.py --seed 1 --output-dir outputs/seed1
uv run python run_all_comparison.py --seed 2 --output-dir outputs/seed2
uv run python run_all_comparison.py --seed 3 --output-dir outputs/seed3

# Agregar
uv run python scripts/aggregate_results.py \
    --inputs outputs/seed1/comparison_results.json \
             outputs/seed2/comparison_results.json \
             outputs/seed3/comparison_results.json \
    --output-json outputs/aggregate_summary.json \
    --output-csv  outputs/aggregate_summary.csv

# Generar reporte
uv run python scripts/generate_aggregate_report.py \
    --input      outputs/aggregate_summary.json \
    --output-dir outputs/report \
    --title      "DDPG vs TD3 vs SAC — comparación 3 seeds"
```

---

## Comparación de algoritmos

| | DDPG | TD3 | SAC |
|---|---|---|---|
| **Tipo de policy** | Determinista | Determinista | Estocástica (Gaussiana) |
| **Exploración** | Ruido externo (Gaussiano) | Ruido externo | Inherente (entropía) |
| **Critics** | Single Q | Twin Q (min target) | Twin Q (min target) |
| **Target actor** | Sí | Sí | No |
| **Target smoothing** | No | Sí (`policy_noise`) | No (no necesario) |
| **Delayed updates** | No | Sí (`policy_delay=2`) | No |
| **Bonus de entropía** | No | No | Sí (`alpha`) |
| **Sample efficiency** | Moderada | Alta | La más alta |
| **Sensibilidad al tuning** | Alta | Media | Menor |

---

## Documentación

| Archivo | Contenido |
|---------|-----------|
| [`doc/01_ddpg.md`](doc/01_ddpg.md) | DDPG: teoría, arquitectura, loop de entrenamiento anotado |
| [`doc/02_td3.md`](doc/02_td3.md) | TD3: tres fixes explicados con referencias al código |
| [`doc/03_sac.md`](doc/03_sac.md) | SAC: objetivo de entropía, corrección tanh, notas de implementación |
| [`doc/presentation_guide_60min.md`](doc/presentation_guide_60min.md) | Guía de presentación 60 min (EN) — talking points minuto a minuto |
| [`doc/presentation_guide_60min_es.md`](doc/presentation_guide_60min_es.md) | Guía de presentación 60 min (ES) |
| [`benchmarks/README.md`](benchmarks/README.md) | Guía de código del paquete benchmarks |

---

## Referencias

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
