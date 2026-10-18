# RL Q-Learning — Parte 2: Extensiones de DQN

<p align="center">
  <img src="doc/images/q_learning_cover.svg" alt="Q-Learning Cover" width="45%" />
  <img src="doc/images/dqn_cover.svg" alt="DQN Cover" width="45%" />
</p>

**Parte 2** de la serie Q-Learning. Este documento cubre las cinco extensiones canónicas de DQN — Double DQN, Dueling DQN, Noisy DQN, Prioritized Experience Replay y N-step DQN — su motivación, cómo funcionan y cómo ejecutarlas desde este repositorio.

> **Navegación de la serie**
> - **Parte 1**: Fundamentos de Q-Learning + DQN básico → [README.md](README.md) · [README_es.md](README_es.md)
> - **Parte 2** (este archivo): Extensiones de DQN (Double, Dueling, Noisy, PER, N-step)
> - **Parte 3**: Variantes avanzadas (C51, QR-DQN, Rainbow, HER) → [README_part3_es.md](README_part3_es.md)

---

## Por qué extender DQN?

DQN vanilla funciona, pero tiene cinco debilidades conocidas. Cada extensión en esta parte corrige exactamente una:

| # | Debilidad | Extensión |
|---|-----------|-----------|
| 1 | **Sobreestima valores Q** — el operador `max` introduce sesgo positivo | Double DQN |
| 2 | **Flujo de valor único** — no puede separar "este estado es bueno" de "esta acción es buena" | Dueling DQN |
| 3 | **Exploración burda** — epsilon-greedy explora uniformemente, ignorando el contexto del estado | Noisy DQN |
| 4 | **Replay uniforme** — todas las transiciones se muestrean igual, desperdiciando tiempo en ejemplos fáciles | Prioritized Replay |
| 5 | **Propagación lenta de recompensa** — bootstrap de 1 paso significa que las recompensas viajan un paso por actualización | N-step DQN |

Las extensiones son **ortogonales**: corrigen problemas distintos y pueden combinarse libremente. Rainbow DQN (Parte 3) las combina todas.

---

## Prerequisitos

Esta parte asume familiaridad con los conceptos de la Parte 1:

| Concepto | Resumen en una oración |
|----------|----------------------|
| Ecuación de Bellman | `Q*(s,a) = E[r + γ · max_a' Q*(s',a')]` — la identidad recursiva de valor |
| Red DQN | Red neuronal `Q_θ(s,a)` que aproxima la función Q: estado de entrada, valores Q de salida |
| Replay Buffer | Almacenar transiciones `(s,a,r,s',done)`; muestrear mini-batches aleatorios para romper la correlación |
| Target Network | Copia congelada `Q_θ⁻` actualizada cada N pasos; proporciona targets estables |
| Epsilon-greedy | Explorar con probabilidad ε, explotar con `argmax Q` de lo contrario |
| Función de Pérdida | MSE entre predicción Q actual y target de Bellman: `L = (Q_θ(s,a) − y)²` |

---

## Instalación

```bash
uv sync
```

---

## Extensión 1 — Double DQN

### Qué corrige
El target de Bellman vanilla usa la **misma red** para seleccionar y evaluar la mejor acción siguiente:

```
y = r + γ · max_a' Q_θ⁻(s', a')
```

Cuando las estimaciones Q son ruidosas, `max` elige sistemáticamente acciones cuyos valores Q están sobreestimados por el ruido. A lo largo de muchas actualizaciones, este sesgo se acumula.

### Cómo funciona
Double DQN desacopla selección de evaluación usando **dos redes**:

```
a* = argmax_a' Q_θ(s', a')       ← policy net SELECCIONA
y  = r + γ · Q_θ⁻(s', a*)       ← target net EVALÚA
```

Aunque la policy net elija una acción sobreestimada, la target net proporciona una evaluación independiente, cancelando el sesgo en promedio.

### Cambios en el código — `benchmarks/dqn_double.py`

```python
# DQN vanilla: la misma red selecciona y evalúa
next_q = target_net(b_ns_t).max(1)[0].detach()

# Double DQN: policy net selecciona, target net evalúa
best_actions = policy_net(b_ns_t).argmax(dim=1, keepdim=True)
next_q = target_net(b_ns_t).gather(1, best_actions).squeeze(1).detach()

expected_q = b_r_t + (cfg.gamma * next_q * (1 - b_d_t))
```

### Ejecución

```bash
uv run python dqn_double_benchmark.py --record-video --plot
```

### Cuándo ayuda más
- Espacios de acción grandes — más acciones implica más oportunidades de sobreestimación
- Señales de recompensa ruidosas — mayor ruido magnifica el sesgo
- Es una mejora estricta con coste casi nulo — usarlo siempre

---

## Extensión 2 — Dueling DQN

### Qué corrige
La red Q vanilla fusiona dos conceptos distintos en una sola salida:

- **Valor del estado V(s)**: ¿qué tan bueno es *estar* en este estado, sin importar la acción?
- **Ventaja de acción A(s,a)**: ¿cuánto *mejor* es la acción `a` comparada con la acción promedio en este estado?

Fusionarlos en un único flujo ralentiza el aprendizaje, especialmente en estados donde la elección de acción apenas importa.

### Cómo funciona
La red se divide en dos flujos paralelos que comparten un extractor de características:

```
                +-------------------+
      +---------► Flujo de valor    |──► V(s)         [1 salida]
      |          | (capas FC)       |
Input-+          +-------------------+         ──► Q(s,a) = V(s) + A(s,a) − mean(A)
  s   | caract.           
      | compartidas +------------------+
      +---------► Flujo de ventaja  |──► A(s,a)       [n_acciones salidas]
                | (capas FC)       |
                +-------------------+
```

La sustracción de la media garantiza identificabilidad: `A(s, a*) > 0` para la mejor acción, `A(s, a) < 0` para las peores.

### Cambios en el código — `benchmarks/dqn_dueling.py`

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

### Ejecución

```bash
uv run python dqn_dueling_benchmark.py --record-video --plot
```

### Cuándo ayuda más
- Entornos con muchas acciones de valor similar
- Estados en los que la acción no importa — el flujo de valor los maneja de forma eficiente

---

## Extensión 3 — Noisy DQN

### Qué corrige
La exploración epsilon-greedy es **independiente del estado**: explora con la misma probabilidad sin importar lo que el agente ya sabe sobre el estado actual.  
Esto requiere ajustar `eps_start`, `eps_end` y `eps_decay` — tres hiperparámetros específicos del problema.

### Cómo funciona
Noisy DQN reemplaza epsilon-greedy con **ruido paramétrico aprendido** en los pesos de la red.

Una capa lineal estándar calcula `y = Wx + b`.  
Una capa `NoisyLinear` calcula:

```
y = (μ_w + σ_w · ε_w) · x + (μ_b + σ_b · ε_b)
```

| Componente | Significado |
|------------|-------------|
| `μ_w, μ_b` | Pesos medios aprendibles (como pesos normales) |
| `σ_w, σ_b` | Magnitud de ruido aprendible (entrenada por descenso de gradiente) |
| `ε_w, ε_b` | Ruido aleatorio muestreado en cada forward pass, no entrenado |

La red aprende *cuánto* explorar a través de los parámetros σ. En estados bien explorados, σ se reduce a ~0 (explotar). En estados inciertos, σ se mantiene grande (explorar).

### Cambios en el código — `benchmarks/dqn_noisy.py`

```python
class NoisyLinear(nn.Module):
    def forward(self, x):
        if self.training:          # entrenamiento: pesos ruidosos (explorar)
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias   = self.bias_mu   + self.bias_sigma   * self.bias_epsilon
        else:                      # evaluación: solo pesos medios (explotar)
            weight = self.weight_mu
            bias   = self.bias_mu
        return F.linear(x, weight, bias)
```

Sin epsilon-greedy — la selección de acción es siempre greedy:

```python
action = policy_net(state_t).argmax()
```

### Ejecución

```bash
uv run python dqn_noisy_benchmark.py --record-video --plot
```

### Qué se elimina
`eps_start`, `eps_end`, `eps_decay` — la exploración es completamente automática.

### Cuándo ayuda más
- Tareas que requieren exploración profunda y estructurada
- Cualquier situación donde el schedule de exploración sea difícil de ajustar manualmente

---

## Extensión 4 — Prioritized Experience Replay (PER)

### Qué corrige
DQN vanilla muestrea transiciones uniformemente del replay buffer. Pero no todas son igual de útiles:

- **Transiciones fáciles** (bajo error TD): la red ya las predice bien — muestrearlas desperdicia un paso.
- **Transiciones sorprendentes** (alto error TD): contienen la mayor señal de aprendizaje.

### Cómo funciona
PER asigna a cada transición una **prioridad** basada en su **error TD**:

```
prioridad_i = |error_TD_i| + ε_prio
P(i) = prioridad_i^α / Σ_j prioridad_j^α
```

El muestreo no uniforme introduce **sesgo**, corregido con pesos de importance sampling:

```
w_i = (1 / (N · P(i)))^β
```

`β` se anneala de 0.4 → 1.0 durante el entrenamiento para corregir completamente el sesgo al final.

### Cambios en el código — `benchmarks/dqn_prio_replay.py`

```python
class PrioritizedReplayBuffer:
    def push(self, transition):
        max_prio = max(self.priorities) if self.priorities else 1.0
        # Las nuevas transiciones reciben la prioridad máxima

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

Nuevos hiperparámetros:

| Parámetro | Default | Notas |
|-----------|---------|-------|
| `alpha` | 0.6 | Exponente de priorización (0 = uniforme, 1 = prioridad total) |
| `beta_start` | 0.4 | Corrección IS inicial (se anneala a 1.0) |
| `epsilon_prio` | 1e-6 | Previene prioridad cero |

### Ejecución

```bash
uv run python dqn_prio_replay_benchmark.py --record-video --plot
```

### Cuándo ayuda más
- Entornos con recompensa escasa — las transiciones raras con recompensa se reproducen más
- Buffers de replay grandes donde el muestreo uniforme diluye las transiciones informativas

---

## Extensión 5 — N-step DQN

### Qué corrige
DQN vanilla hace bootstrapping desde **un solo paso**:

```
y = r_t + γ · max_a' Q(s_{t+1}, a')
```

La información viaja **un paso a la vez**. Si una recompensa positiva ocurre en el paso 100, se necesitan ~100 actualizaciones para que esa señal influencie el valor Q en el paso 0.

### Cómo funciona
N-step DQN mira **n pasos adelante** antes de hacer bootstrapping:

```
G_t^(n) = r_t + γ·r_{t+1} + ... + γ^{n-1}·r_{t+n-1} + γ^n · max_a' Q(s_{t+n}, a')
```

Trade-off sesgo–varianza:

| n | Sesgo | Varianza | Velocidad |
|---|-------|----------|-----------|
| 1 (DQN) | Alto | Baja | Propagación lenta |
| 3 (default) | Moderado | Moderada | Buen balance |
| 5–10 | Menor | Mayor | Propagación rápida |
| Episodio completo | Ninguno | Máxima | Inmediata |

### Cambios en el código — `benchmarks/dqn_n_steps.py`

```python
nstep_buffer = collections.deque(maxlen=cfg.n_steps)

if len(nstep_buffer) == cfg.n_steps:
    cum_reward = 0.0
    discount = 1.0
    for _, _, r_i, _, d_i in nstep_buffer:
        cum_reward += discount * r_i
        if d_i: break
        discount *= cfg.gamma
    # Almacenar (s0, a0, cum_reward, s_last, d_last) en replay

# Descuento del target modificado
expected_q = b_r_t + (cfg.gamma ** cfg.n_steps) * next_q * (1 - b_d_t)
```

### Ejecución

```bash
uv run python dqn_n_steps_benchmark.py --record-video --plot
```

### Cuándo ayuda más
- Entornos con recompensas retrasadas
- Cuando la asignación de crédito rápida supera el coste de varianza (entornos de baja estocasticidad)

---

## Ejecutar todas las extensiones juntas

Comparar las cinco extensiones frente a DQN vanilla en una sola ejecución:

```bash
uv run python run_all_comparison.py \
  --methods dqn dqn_double dqn_dueling dqn_noisy dqn_prio_replay dqn_n_steps \
  --record-video
```

Grabar videos y curvas de entrenamiento para cada extensión individualmente:

```bash
uv run python dqn_double_benchmark.py      --record-video --plot
uv run python dqn_dueling_benchmark.py     --record-video --plot
uv run python dqn_noisy_benchmark.py       --record-video --plot
uv run python dqn_prio_replay_benchmark.py --record-video --plot
uv run python dqn_n_steps_benchmark.py     --record-video --plot
```

---

## Tabla resumen de extensiones

| Extensión | Qué cambia | Nuevos hiperparams | Sobrecarga | Mejor para |
|-----------|-----------|-------------------|------------|------------|
| **Double DQN** | Cálculo del target (~2 líneas) | Ninguno | Insignificante | Reducir sobreestimación |
| **Dueling DQN** | Arquitectura de red (~20 líneas) | Ninguno | Mínima | Entornos con muchas acciones |
| **Noisy DQN** | Capas lineales + eliminar ε-greedy (~60 líneas) | `sigma_init` | Moderada | Tareas de exploración profunda |
| **PER** | Buffer de replay + pérdida ponderada (~50 líneas) | `alpha`, `beta` | Moderada | Entornos con recompensa escasa |
| **N-step DQN** | Lógica del buffer + descuento del target (~20 líneas) | `n_steps` | Mínima | Propagación de recompensa retrasada |

Conclusiones clave:
- Cada extensión corrige **una debilidad específica** de DQN vanilla.
- Son **ortogonales** y pueden combinarse libremente.
- **Double DQN** es una mejora estricta sin coste — usarlo siempre.
- **Noisy DQN** elimina completamente el schedule de exploración.
- **PER** tiene mayor impacto en escenarios de recompensa escasa o buffers grandes.

---

## Artefactos generados

Los archivos de salida se escriben en:

| Ruta | Contenido |
|------|-----------|
| `outputs/comparison_results.json/csv` | Métricas por ejecución para todos los métodos |
| `outputs/aggregate_summary.json/csv` | Estadísticas agregadas de múltiples ejecuciones |
| `outputs/report/` | Gráficos generados e informes HTML |
| `videos/` | Episodios de evaluación grabados |
| `runs/` | Datos de ejecución para TensorBoard |

---

## Documentación

- Guía de presentación (español): [doc/presentations/presentation_guide_part2_60min_es.md](doc/presentations/presentation_guide_part2_60min_es.md)
- Guía de presentación (inglés): [doc/presentations/presentation_guide_part2_60min.md](doc/presentations/presentation_guide_part2_60min.md)
- Documentación de algoritmos (español): [doc/es/README.md](doc/es/README.md)
- Documentación de algoritmos (inglés): [doc/README.md](doc/README.md)
- Vista general Parte 1: [README.md](README.md) · [README_es.md](README_es.md)
