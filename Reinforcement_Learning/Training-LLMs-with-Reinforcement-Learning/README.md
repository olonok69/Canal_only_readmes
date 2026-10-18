# Training LLMs with RL — SFT, DPO, ORPO, PPO, GRPO

*[Leer en español](README_es.md)*

> **Session 8 of the RL course.** Sessions 1–4 built the RL algorithms from
> first principles: MDPs and Bellman, the DQN family, PPO/A2C/TRPO, and
> continuous-control actor-critics (DDPG / TD3 / SAC). Session 7 pivoted to
> libraries and an applied trading demo. This session pivots again — from
> agents acting in environments to **agents acting in language**.

Two sessions, 60 minutes each:

- **Theory session** — five techniques (SFT, DPO, ORPO, PPO, GRPO), what they
  do, when to reach for which, what fails. Driven by
  [`doc/presentation_guide_theory_60min.md`](doc/presentation_guide_theory_60min.md).
- **Demo session** — five Colab notebooks training the same backbone
  (`Qwen/Qwen2.5-1.5B-Instruct`) end-to-end with each technique, all logging
  to one W&B project for direct comparison. Driven by
  [`doc/presentation_guide_demo_60min.md`](doc/presentation_guide_demo_60min.md).

---


## What's inside

```
rl_training_llm/
├── doc/
│   ├── 01_sft.md                            ← SFT deep dive
│   ├── 02_dpo.md                            ← DPO deep dive
│   ├── 03_orpo.md                           ← ORPO deep dive
│   ├── 04_ppo.md                            ← PPO-for-LLMs deep dive
│   ├── 05_grpo.md                           ← GRPO deep dive
│   ├── README.md                            ← doc index
│   ├── HANDOFF.md                           ← course-wide conventions doc
│   ├── figures/                             ← generated figures (HTML + PNG)
│   ├── ppts/
│   │   └── Reinforcement_Learning_Training_LLMs.pptx   ← the deck
│   └── es/                                  ← Spanish mirror (in progress)
│
├── notebooks/                               ← five Colab notebooks
│   ├── 01_sft.ipynb                         ← SFT on trl-lib/Capybara
│   ├── 02_dpo.ipynb                         ← DPO on UltraFeedback Binarized
│   ├── 03_orpo.ipynb                        ← ORPO on UltraFeedback Binarized
│   ├── 04_ppo.ipynb                         ← PPO + deberta-v3 reward model on TLDR
│   └── 05_grpo.ipynb                        ← GRPO on GSM8K with regex verifier
│

│
├── pyproject.toml                           ← uv-managed deps
├── uv.lock
└── README.md / README_es.md                 ← this file
```

---

## Quick start

```bash
# 1. Install uv if missing
pip install uv

# 2. Sync the virtualenv from the lockfile
cd rl_training_llm
uv sync

# 3. Regenerate the framing figures (3 PNGs in doc/figures/)
uv run python scripts/plot_alignment.py




```

The notebooks themselves run on **Colab Pro** — local execution is not the
target. Each notebook installs its own dependencies in cell 1.

---

## The five techniques in one sentence each

- **SFT** (Supervised Fine-Tuning) — teach the model the chat template and how
  to follow instructions, by cross-entropy on `(prompt, completion)` pairs.
- **DPO** (Direct Preference Optimization) — RLHF in closed form: a binary
  classification loss against `(chosen, rejected)` preference pairs, no reward
  model.
- **ORPO** (Odds-Ratio Preference Optimization) — collapse SFT and DPO into a
  single training stage with one trainer, no reference model.
- **PPO for LLMs** — the canonical RLHF pipeline: SFT → reward model → PPO
  with a KL anchor against the reference. Four models in memory at training
  time.
- **GRPO** (Group Relative Policy Optimization) — PPO with the value head and
  reward model removed. Sample G completions per prompt, score each in Python,
  use within-group reward normalization as the advantage. The DeepSeek-R1
  technique.

Full deep dives in [`doc/01_sft.md`](doc/01_sft.md) →
[`doc/05_grpo.md`](doc/05_grpo.md). Decision guide and side-by-side
comparison live in [`doc/presentation_guide_theory_60min.md`](doc/presentation_guide_theory_60min.md).

---

## W&B logging

All five notebooks log to a single W&B project (`rl-llm-training`) with run
names `qwen2.5-1.5b-{sft,dpo,orpo,ppo,grpo}`. The
[`scripts/compare_runs.py`](scripts/compare_runs.py) script pulls metric
histories from that project and produces five cross-technique comparison
figures (`doc/figures/compare_*.png`) and a markdown summary table.

The notebooks expect `WANDB_API_KEY` either as a Colab secret (preferred)
or via interactive `wandb.login()` (fallback).

---

## Position in the course

| Session | Folder | Topic |
|---------|--------|-------|
| 1 | `Introduction_to_RL` | MDPs, Bellman, value functions |
| 2 | `rl_q_learning` | Q-learning → DQN family |
| 3 | `rl_policy_optimization` | Policy gradient, A2C / PPO / TRPO |
| 4 | `rl_hybrid_algorithms` | Continuous control: DDPG, TD3, SAC |
| 7 | `rl_libraries` | Library ecosystem + applied yfinance + MuJoCo |
| **8** | **`rl_training_llm`** ← **you are here** | **Training LLMs with RL: SFT · DPO · ORPO · PPO · GRPO** |
