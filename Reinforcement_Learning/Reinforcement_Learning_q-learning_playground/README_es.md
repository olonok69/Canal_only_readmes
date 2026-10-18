# Benchmarks de RL Q-Learning

<p align="center">
  <img src="doc/images/q_learning_cover.svg" alt="Q-Learning Cover" width="45%" />
  <img src="doc/images/dqn_cover.svg" alt="DQN Cover" width="45%" />
</p>

Repositorio completo de reinforcement learning centrado en la **familia Q-Learning**. La suite principal de benchmarks se ejecuta sobre `CartPole-v1`, y el proyecto ha evolucionado desde Q-Learning tabular y un baseline de DQN hasta una colección más amplia de extensiones de DQN, variantes avanzadas value-based, utilidades de reporting y documentación bilingüe.

## Qué contiene este repositorio

| Área | Contenido |
|------|-----------|
| Runners de benchmark | Scripts independientes para Q-Learning, DQN, Double DQN, Dueling DQN, Noisy DQN, Prioritized Replay, N-step, C51, QR-DQN, Rainbow y HER |
| Paquete principal de implementación | `benchmarks/` con configuraciones reutilizables, loops de entrenamiento, lógica de replay, helpers de evaluación y utilidades compartidas de resultados |
| Herramientas de comparación | `run_all_comparison.py`, `run_phase1_comparison.py` y `rl_comparison.py` para experimentos orquestados |
| Scripts de reporting | `scripts/aggregate_results.py` y `scripts/generate_aggregate_report.py` para resúmenes multi-corrida y gráficos |
| Código de referencia | `DQN Extensions/`, `DQN Q-Networks/` y `Q-learning-Advanced/` con implementaciones anteriores o exploratorias |
| Documentación | Notas de algoritmos en inglés y español bajo `doc/` y `doc/es/` |
| Artefactos generados | Ejemplos de resultados en `outputs/`, corridas guardadas en `runs/` y grabaciones de evaluación en `videos/` |

## Métodos implementados

- **Q-Learning tabular**
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

## Instalación
Usando `uv`:

```bash
uv sync
```

## Ejecutar benchmarks individuales
Cada método tiene su propio script en la raíz:

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

Para grabar videos de evaluación o mostrar curvas de entrenamiento:

```bash
uv run python dqn_benchmark.py --record-video --plot
```

## Ejecutar la suite completa de comparación
Ejecutar todos los métodos registrados:

```bash
uv run python run_all_comparison.py
```

Ejecutar solo un subconjunto:

```bash
uv run python run_all_comparison.py --methods q_learning dqn dqn_double
```

Detener en el primer fallo:

```bash
uv run python run_all_comparison.py --strict
```

## Artefactos de salida
Los archivos generados típicos incluyen:

- `outputs/comparison_results.json`
- `outputs/comparison_results.csv`
- `outputs/comparison_errors.json`
- `outputs/aggregate_summary.json`
- `outputs/aggregate_summary.csv`
- `outputs/report/` para reportes y gráficos generados
- `videos/` para evaluaciones grabadas
- `runs/` para datos de corridas almacenadas

## Estructura del repositorio

- `benchmarks/` — implementaciones principales usadas por los runners de la raíz
- `scripts/` — utilidades para agregación de resultados y reporting
- `doc/` — documentación de algoritmos e ilustraciones en inglés
- `doc/es/` — documentación de algoritmos en español
- `DQN Extensions/` — implementaciones de referencia centradas en extensiones y pequeños experimentos
- `DQN Q-Networks/` — ejemplos base incluyendo Q-Learning en FrozenLake y DQN para Pong
- `Q-learning-Advanced/` — material experimental o archivado para variantes distribucionales y Rainbow
- `outputs/`, `runs/`, `videos/` — artefactos generados por los experimentos

## Documentación

- Índice de documentación en inglés: [doc/README.md](doc/README.md)
- Índice de documentación en español: [doc/es/README.md](doc/es/README.md)
- Resumen principal en inglés: [README.md](README.md)

## Notas

- Todos los métodos benchmarkeados pertenecen a la misma línea de aprendizaje value-based.
- El flujo principal del proyecto está pensado para ejecutar benchmarks reproducibles y luego agregarlos en reportes.
- Además de la suite principal, el repositorio conserva implementaciones de referencia y material exploratorio de etapas anteriores del desarrollo.
