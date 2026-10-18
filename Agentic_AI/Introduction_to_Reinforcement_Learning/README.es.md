# Introducción a Reinforcement Learning

Este repositorio es un proyecto práctico para aprender fundamentos de Reinforcement Learning (RL) mediante tres demos:

- Q-learning tabular en FrozenLake
- REINFORCE (policy gradient) en CartPole
- PPO en CartPole con Stable-Baselines3

El objetivo es conectar teoría y código: leer conceptos, entrenar agentes, evaluar políticas y generar videos de demostración.

## Qué incluye este repositorio

- `demos/q_learning_frozenlake.py`: RL model-free basado en valor con Q-table
- `demos/reinforce_cartpole.py`: optimización directa de política con retornos Monte Carlo
- `demos/gymnasium_ppo_cartpole.py`: flujo práctico de PPO con `stable-baselines3`
- `docs/rl_explanations.md`: explicación completa con referencias al código (EN)
- `docs/rl_explanations.es.md`: explicación completa con referencias al código (ES)
- `videos/`: ejecuciones de evaluación grabadas
- `models/`: artefactos de modelos guardados (PPO)

## Conceptos de RL cubiertos (desde `docs/rl_explanations.md`)

### Fundamentos

- Agente, entorno, estado, acción, recompensa y política
- Objetivo: maximizar el retorno descontado esperado
- RL model-based vs model-free, y por qué aquí se usan métodos model-free

!["Reinforcement Learning Taxonomy"](rl_algorithms_9_15.svg).

### Resumen de Q-learning

Q-learning aprende valores de acción $Q(s,a)$ y deriva una política con `argmax`.

Regla de actualización usada en el demo:

$$
Q(s,a) \leftarrow Q(s,a) + \alpha \left[r + \gamma \max_{a'}Q(s',a') - Q(s,a)\right]
$$

Conceptos implementados:

- Exploración epsilon-greedy con decaimiento de epsilon
- Actualización Bellman/TD
- Manejo de estado terminal (sin bootstrap al terminar)
- Evaluación greedy al final del entrenamiento (tasa de éxito)

### Resumen de REINFORCE

REINFORCE optimiza directamente una política estocástica $\pi_\theta(a|s)$.

Pérdida de entrenamiento (a nivel conceptual):

$$
\mathcal{L}(\theta) = -\sum_t \log \pi_\theta(a_t|s_t) G_t
$$

Conceptos implementados:

- Muestreo de acciones desde una red de política
- Cálculo de retornos descontados
- Normalización de retornos para reducir varianza
- Optimización por policy gradient por episodio

### Resumen de PPO

PPO es un método moderno de optimización de políticas, implementado aquí con `stable-baselines3`.

Flujo implementado en el demo:

- Crear y entrenar un agente PPO (`MlpPolicy`) en CartPole
- Guardar el modelo en `models/`
- Evaluar rendimiento con política determinista
- Render opcional en tiempo real y grabación opcional en video

### Modelo vs política vs función de valor

- **Modelo**: predice dinámica/recompensas del entorno
- **Política**: decide qué acción tomar en cada estado
- **Función de valor**: estima retorno esperado futuro

En este repo:

- Q-learning aprende principalmente una función de valor (`Q-table`)
- REINFORCE/PPO optimizan principalmente una política (PPO además estima valor internamente)

## Inicio rápido

### Prerrequisitos

- Python 3.10 o 3.11
- `uv` instalado

### Instalar dependencias

Desde la raíz del proyecto:

```powershell
uv pip install -r requirements.txt
```

## Ejecutar los demos

### 1) Q-learning (FrozenLake)

```powershell
python demos/q_learning_frozenlake.py
```

Opciones útiles:

```powershell
python demos/q_learning_frozenlake.py --slippery
python demos/q_learning_frozenlake.py --render-eval --render-episodes 5
python demos/q_learning_frozenlake.py --record-video --video-episodes 5 --video-dir videos/q_learning_frozenlake
python demos/q_learning_frozenlake.py --record-and-render --render-episodes 5 --video-episodes 5
```

### 2) REINFORCE (CartPole)

```powershell
python demos/reinforce_cartpole.py
```

Opciones útiles:

```powershell
python demos/reinforce_cartpole.py --episodes 1500 --lr 0.0005 --gamma 0.99
python demos/reinforce_cartpole.py --render-eval --render-episodes 3
python demos/reinforce_cartpole.py --record-video --video-episodes 3 --video-dir videos/reinforce_cartpole
python demos/reinforce_cartpole.py --record-and-render --render-episodes 3 --video-episodes 3
```

### 3) PPO (CartPole)

```powershell
python demos/gymnasium_ppo_cartpole.py
```

Opciones útiles:

```powershell
python demos/gymnasium_ppo_cartpole.py --render-demo
python demos/gymnasium_ppo_cartpole.py --render-eval --render-episodes 3
python demos/gymnasium_ppo_cartpole.py --record-video --video-episodes 3 --video-dir videos/ppo_cartpole
python demos/gymnasium_ppo_cartpole.py --record-and-render --render-episodes 3 --video-episodes 3
```

## Ruta sugerida de aprendizaje / clase (aprox. 60 minutos)

1. Fundamentos de RL + contexto model-free
2. Demo de Q-learning y actualización de Bellman
3. Demo de REINFORCE e intuición de policy gradient
4. Demo de PPO como baseline práctico moderno
5. Cierre: modelo vs política vs función de valor

Para la explicación completa con mapeo a código, revisa `docs/rl_explanations.es.md` y `docs/rl_explanations.md`.
