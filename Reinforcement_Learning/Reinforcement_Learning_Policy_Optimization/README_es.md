# Benchmarks de RL Policy Optimization

Suite de benchmarks de reinforcement learning con múltiples algoritmos sobre `CartPole-v1`, con scripts independientes por método y un runner unificado de comparación.

## Serie de presentaciones
Este repositorio está preparado para una **serie de dos presentaciones**:
- **Parte 1**: Introducción detallada a Policy Optimization, Monte Carlo y REINFORCE → [Guía de presentación](doc/presentation_guide_60min_es.md)
- **Parte 2**: A2C, A3C, PPO, TRPO y flujo de comparación → [Guía de presentación](doc/presentation_guide_part2_60min_es.md)

## Alcance
Este repositorio incluye métodos de policy optimization:
- Policy Gradient (REINFORCE)
- A2C
- A3C
- PPO
- TRPO

## Documentación
Guías completas de algoritmos con teoría, walkthrough de implementación y mapa de código:

| Guía | Descripción |
|------|-------------|
| [doc/03_policy_gradient.md](doc/03_policy_gradient.md) | Fundamentos de Policy Gradient (REINFORCE) e implementación |
| [doc/04_a2c.md](doc/04_a2c.md) | Explicación de Advantage Actor-Critic y flujo de entrenamiento |
| [doc/05_a3c.md](doc/05_a3c.md) | Arquitectura asíncrona actor-critic e interacción worker/learner |
| [doc/06_ppo.md](doc/06_ppo.md) | Objetivo con clipping en PPO, GAE y loop de actualización |
| [doc/07_trpo.md](doc/07_trpo.md) | Intuición trust-region de TRPO e integración de benchmark |
| [doc/README.md](doc/README.md) | Índice completo de documentación |

## Documentación basada en libro
Explicaciones detalladas de algoritmos basadas en:
`doc/Deep Reinforcement Learning Hands-On_ Apply modern RL methods to practical problems of chatbots, robotics, discrete optimization, web automation, and more, 2nd Edition-Packt Publishing.pdf`

Ver índice: [doc/README.md](doc/README.md)

## Instalación
Usando `uv`:

```bash
uv sync
```

## Ejecutar un método (independiente)
Cada algoritmo tiene su propio script standalone:

```bash
uv run python policy_gradient_benchmark.py
uv run python a2c_benchmark.py
uv run python a3c_benchmark.py
uv run python ppo_benchmark.py
uv run python trpo_benchmark.py
```

Los scripts también permiten ajustar hiperparámetros. Ejemplo:

```bash
uv run python ppo_benchmark.py --episodes 700 --rollout-steps 2048 --update-epochs 6
uv run python a3c_benchmark.py --episodes 600 --workers 8 --rollout-steps 10
uv run python trpo_benchmark.py --timesteps 200000
```

## Ejecutar todos los métodos juntos
Orquestador unificado:

```bash
uv run python run_all_comparison.py
```

Ejecutar solo métodos seleccionados:

```bash
uv run python run_all_comparison.py --methods policy_gradient ppo trpo
```

Con grabación de video:

```bash
uv run python run_all_comparison.py --methods policy_gradient ppo --record-video --video-dir videos --video-episodes 3
```

También puedes ajustar budget por método desde el orquestador:

```bash
uv run python run_all_comparison.py --methods policy_gradient a2c a3c ppo trpo --policy-gradient-episodes 700 --a2c-episodes 600 --a3c-episodes 600 --ppo-episodes 700 --trpo-timesteps 200000
```

Modo estricto (detener en el primer fallo):

```bash
uv run python run_all_comparison.py --strict
```

## Salidas
`run_all_comparison.py` genera:
- `outputs/comparison_results.json`
- `outputs/comparison_results.csv`
- `outputs/comparison_errors.json`

## Protocolo recomendado de experimentos
Para comparaciones justas y reproducibles entre métodos:

1. **Usar múltiples seeds**
   - Ejecutar cada método con al menos 3-5 seeds distintos.
   - Ejemplo: `--seed 1`, `--seed 2`, `--seed 3`.

2. **Mantener budgets alineados**
   - Igualar el budget de entrenamiento lo máximo posible (episodes o timesteps).
   - Reportar diferencias de budget cuando los métodos requieran estilos de rollout distintos.

3. **Reportar distribución, no una sola corrida**
   - Agregar `max_avg_reward_100` y `final_avg_reward_100` como media ± std entre seeds.
   - Mantener salidas crudas por corrida en `outputs/` para trazabilidad.

4. **Hacer un smoke-test rápido antes de corridas completas**
   - Primero correr un subconjunto de métodos para validar environment/dependencies.
   - Después lanzar la matriz completa de benchmark.

5. **Seguir fallos por separado**
   - Revisar `comparison_errors.json` y no eliminar métodos fallidos de los reportes.

## Agregar resultados multi-seed
Usa el script helper para agregar varias salidas JSON del benchmark en media/std por algoritmo:

```bash
uv run python scripts/aggregate_results.py --inputs outputs/*.json --output-json outputs/aggregate_summary.json --output-csv outputs/aggregate_summary.csv
```

También puedes pasar múltiples archivos explícitos o directorios:

```bash
uv run python scripts/aggregate_results.py --inputs runs/seed1 runs/seed2 outputs/comparison_results.json
```

Generar plots + reporte Markdown desde el resumen agregado:

```bash
uv run python scripts/generate_aggregate_report.py --input outputs/aggregate_summary.json --output-dir outputs/report --title "RL Policy Optimization Aggregate Report"
```

Reporte agregado en español:
- [outputs/report/aggregate_report_es.md](outputs/report/aggregate_report_es.md)

## Archivos principales
- `run_all_comparison.py`: runner unificado de benchmark multi-método
- `rl_comparison.py`: entrypoint de compatibilidad para comparación unificada
- `benchmarks/`: módulos reutilizables de algoritmos y utilidades compartidas de benchmark
- `doc/`: documentación de algoritmos y PDF fuente

## Notas
- TRPO usa la implementación de `sb3-contrib` (`benchmarks/trpo.py`).
- A3C usa multiprocessing y puede consumir CPU de forma significativa.
- Para comparaciones justas, mantener seeds y configuración del environment consistentes.
