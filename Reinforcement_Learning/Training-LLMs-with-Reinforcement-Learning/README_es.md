# Entrenar LLMs con RL — SFT, DPO, ORPO, PPO, GRPO

*[Read in English](README.md)*

> **Sesión 8 del curso de RL.** Las sesiones 1–4 construyeron los algoritmos
> de RL desde cero: MDPs y Bellman, la familia DQN, PPO/A2C/TRPO y los
> actor-critic de control continuo (DDPG / TD3 / SAC). La sesión 7 hizo el
> giro hacia las librerías y un demo aplicado de trading. Esta sesión vuelve
> a girar — de agentes que actúan en *entornos* a **agentes que actúan en
> lenguaje**.

Dos sesiones de 60 minutos cada una:

- **Sesión teórica** — cinco técnicas (SFT, DPO, ORPO, PPO, GRPO), qué hacen,
  cuándo elegir cada una, qué falla. Se sigue con
  [`doc/presentation_guide_theory_60min.md`](doc/presentation_guide_theory_60min.md).
- **Sesión de demo** — cinco notebooks de Colab que entrenan el mismo modelo
  base (`Qwen/Qwen2.5-1.5B-Instruct`) de extremo a extremo con cada técnica,
  todos registrando en un único proyecto de W&B para comparación directa. Se
  sigue con
  [`doc/presentation_guide_demo_60min.md`](doc/presentation_guide_demo_60min.md).

> Las traducciones al español de los deep dives y los presenter guides están
> bajo `doc/es/` (en progreso).

---

## Qué contiene

```
rl_training_llm/
├── doc/
│   ├── 01_sft.md                            ← deep dive SFT
│   ├── 02_dpo.md                            ← deep dive DPO
│   ├── 03_orpo.md                           ← deep dive ORPO
│   ├── 04_ppo.md                            ← deep dive PPO para LLMs
│   ├── 05_grpo.md                           ← deep dive GRPO
│   ├── README.md                            ← índice de doc/
│   ├── HANDOFF.md                           ← convenciones del curso
│   ├── figures/                             ← figuras generadas (HTML + PNG)
│   ├── ppts/
│   │   └── Reinforcement_Learning_Training_LLMs.pptx   ← la presentación
│   └── es/                                  ← réplica en español (en progreso)
│
├── notebooks/                               ← cinco notebooks de Colab
│   ├── 01_sft.ipynb                         ← SFT sobre trl-lib/Capybara
│   ├── 02_dpo.ipynb                         ← DPO sobre UltraFeedback Binarized
│   ├── 03_orpo.ipynb                        ← ORPO sobre UltraFeedback Binarized
│   ├── 04_ppo.ipynb                         ← PPO + reward model deberta-v3 sobre TLDR
│   └── 05_grpo.ipynb                        ← GRPO sobre GSM8K con verificador regex
│
│
├── pyproject.toml                           ← dependencias gestionadas por uv
├── uv.lock
└── README.md / README_es.md                 ← este archivo
```

---

## Inicio rápido

```bash
# 1. Instalar uv si no lo tienes
pip install uv

# 2. Sincronizar el venv con el lockfile
cd rl_training_llm
uv sync

# 3. Regenerar las figuras de framing (3 PNG en doc/figures/)
uv run python scripts/plot_alignment.py


```
Los notebooks corren en **Colab Pro** — la ejecución local no es el objetivo.
Cada notebook instala sus dependencias en la celda 1.

---

## Las cinco técnicas en una frase

- **SFT** (Supervised Fine-Tuning) — enseña al modelo el chat template y a
  seguir instrucciones, mediante cross-entropy sobre pares
  `(prompt, completion)`.
- **DPO** (Direct Preference Optimization) — RLHF en forma cerrada: una
  pérdida de clasificación binaria contra pares `(chosen, rejected)`. Sin
  reward model.
- **ORPO** (Odds-Ratio Preference Optimization) — colapsa SFT y DPO en una
  sola etapa de entrenamiento con un único trainer, sin modelo de referencia.
- **PPO para LLMs** — el pipeline canónico de RLHF: SFT → reward model → PPO
  con anclaje KL contra la referencia. Cuatro modelos en memoria durante el
  entrenamiento.
- **GRPO** (Group Relative Policy Optimization) — PPO sin la value head ni el
  reward model. Genera G completions por prompt, las puntúa con Python y usa
  la normalización dentro del grupo como ventaja. La técnica detrás de
  DeepSeek-R1.

Deep dives completos en [`doc/01_sft.md`](doc/01_sft.md) →
[`doc/05_grpo.md`](doc/05_grpo.md). La guía de decisión y la comparativa lado
a lado viven en
[`doc/presentation_guide_theory_60min.md`](doc/presentation_guide_theory_60min.md).

---

## Logging con W&B

Los cinco notebooks escriben en un único proyecto de W&B (`rl-llm-training`)
con nombres de run `qwen2.5-1.5b-{sft,dpo,orpo,ppo,grpo}`. El script
[`scripts/compare_runs.py`](scripts/compare_runs.py) descarga las historias
de métricas de ese proyecto y produce cinco figuras de comparación entre
técnicas (`doc/figures/compare_*.png`) más una tabla resumen en markdown.

Los notebooks esperan `WANDB_API_KEY` como secreto de Colab (preferido) o
mediante `wandb.login()` interactivo (fallback).

---

## Posición en el curso

| Sesión | Carpeta | Tema |
|--------|---------|------|
| 1 | `Introduction_to_RL` | MDPs, Bellman, funciones de valor |
| 2 | `rl_q_learning` | Q-learning → familia DQN |
| 3 | `rl_policy_optimization` | Gradiente de política, A2C / PPO / TRPO |
| 4 | `rl_hybrid_algorithms` | Control continuo: DDPG, TD3, SAC |
| 7 | `rl_libraries` | Ecosistema de librerías + yfinance aplicado + MuJoCo |
| **8** | **`rl_training_llm`** ← **estás aquí** | **Entrenar LLMs con RL: SFT · DPO · ORPO · PPO · GRPO** |
