# Gemma 4 Post-Training Series (Colab Notebooks)

This folder contains a practical 3-notebook sequence to present and run a Gemma 4 post-training workflow in Google Colab:

1. Capabilities baseline (Stage 0)
2. Supervised Fine-Tuning (Stage 1, SFT + QLoRA)
3. Preference + Reasoning RL (Stages 2 and 3, DPO + GRPO)

The notebooks are written with a Hugging Face-first approach and include compatibility guards for common Colab version drift.

## Topic and learning objective

Main topic: how to move from a base instruction-tuned Gemma model to a post-trained policy using the canonical alignment stages.

By the end of this sequence you can:

- Establish a reproducible baseline behavior for Gemma 4.
- Run Stage 1 SFT with LoRA adapters on Colab-friendly hardware.
- Run Stage 2 DPO with preference pairs.
- Run Stage 3 GRPO with programmable rewards for math reasoning.
- Save and compare baseline vs tuned outputs for presentation.

## Notebooks in this folder

### 00_gemma4_family_capabilities_colab_demo.ipynb

Purpose:

- Introduce Gemma 4 model family usage in Colab.
- Produce baseline outputs before any additional fine-tuning.
- Demonstrate text, structured output, optional audio pipeline, and optional multimodal usage.

Key outputs:

- Baseline instruction-following sample.
- JSON/structured generation sample.
- Optional ASR-to-Gemma analysis sample.
- Optional image+text prompt sample.

### 01_gemma4_stage1_sft_qlora.ipynb

Purpose:

- Implement Stage 1 supervised fine-tuning with TRL SFTTrainer and PEFT LoRA.
- Build a reusable Stage 1 adapter artifact for Stage 2 warm-start.

Key outputs:

- Trained SFT adapter saved locally.
- Optional copy to Google Drive.
- Optional W&B model artifact.
- Qualitative post-SFT generation check.

### 02_gemma4_stage2_preference_and_stage3_reasoning_rl.ipynb

Purpose:

- Stage 2: run DPO on a preference dataset.
- Stage 3: run GRPO on GSM8K-style reasoning with format + correctness rewards.
- Save Stage 3 outputs and compare against untuned baseline.

Current status note:

- In the latest Colab runs, GRPO did not consistently outperform baseline on the tiny quick-check set.
- This is a valid intermediate result and should be documented as part of experimental iteration (reward design, train budget, eval set size).

Key outputs:

- DPO/GRPO training logs.
- Saved Stage 3 model artifacts.
- Baseline vs tuned comparison table and accuracy summary.

## References used in this workflow

- Gemma model cards (Hugging Face):
  - https://huggingface.co/google/gemma-4-E2B-it
- Transformers documentation:
  - https://huggingface.co/docs/transformers/index
- TRL documentation (SFT, DPO, GRPO trainers):
  - https://huggingface.co/docs/trl/index
- PEFT documentation (LoRA adapters):
  - https://huggingface.co/docs/peft/index
- Datasets documentation:
  - https://huggingface.co/docs/datasets/index
- Weights and Biases documentation:
  - https://docs.wandb.ai/

Datasets referenced in notebooks:

- Capybara (SFT): trl-lib/Capybara
- UltraFeedback binarized (DPO): trl-lib/ultrafeedback_binarized
- GSM8K (GRPO task): openai/gsm8k (with compatibility fallbacks)

## Suggested run order

1. Run notebook 00 to capture baseline behavior for your slides.
2. Run notebook 01 to produce Stage 1 adapter artifacts.
3. Run notebook 02 for Stage 2 and Stage 3 experiments and final comparison.

## Reproducibility and Colab notes

- If package versions are upgraded in install cells, restart runtime and rerun all cells.
- Keep HF_TOKEN and WANDB_API_KEY in Colab secrets when possible.
- For Stage 2 warm-start from Stage 1, set SFT_ADAPTER_PATH to the saved adapter path.
- Treat GRPO metric changes on very small eval sets as directional, not conclusive.

## Educational script: MoE routing intuition

To illustrate how models can store many total parameters while using only a
subset per token at inference, use:

- `scripts/moe_routing_demo.py`

Example run:

```bash
python scripts/moe_routing_demo.py --tokens 12 --experts 16 --top-k 2
```

This script is a conceptual demo (not a production MoE implementation).

For a heatmap-like token-to-expert table in plain text, use:

- `scripts/moe_routing_heatmap_demo.py`

Example run:

```bash
python scripts/moe_routing_heatmap_demo.py --tokens 8 --experts 12 --top-k 2
```

## Next documentation steps

- Add per-stage experiment logs (hyperparameters + final metrics) to a dedicated report.
- Expand evaluation from 3 quick prompts to a larger held-out set for stronger conclusions.
- Add a short "Known issues and mitigations" section based on Colab compatibility guards.
