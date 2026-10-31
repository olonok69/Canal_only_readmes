# Serie de Post-Training de Gemma 4 (cuadernos de Colab)

Esta carpeta contiene una secuencia practica de 3 cuadernos para presentar y ejecutar un flujo de post-training de Gemma 4 en Google Colab:

1. Baseline de capacidades (Stage 0)
2. Supervised Fine-Tuning (Stage 1, SFT + QLoRA)
3. Preferencias + RL de razonamiento (Stages 2 y 3, DPO + GRPO)

Los cuadernos estan escritos con un enfoque centrado en Hugging Face e incluyen guardas de compatibilidad para desajustes de version habituales en Colab.

## Tema y objetivo de aprendizaje

Tema principal: como pasar de un modelo Gemma base instruction-tuned a una politica post-entrenada usando las etapas canonicas de alineacion.

Al terminar esta secuencia podras:

- Establecer un comportamiento baseline reproducible para Gemma 4.
- Ejecutar Stage 1 SFT con adaptadores LoRA en hardware apto para Colab.
- Ejecutar Stage 2 DPO con pares de preferencias.
- Ejecutar Stage 3 GRPO con recompensas programables para razonamiento matematico.
- Guardar y comparar salidas baseline frente al modelo ajustado para presentacion.

## Cuadernos de esta carpeta

### 00_gemma4_family_capabilities_colab_demo.ipynb

Objetivo:

- Introducir el uso de la familia Gemma 4 en Colab.
- Producir salidas baseline antes de cualquier ajuste fino adicional.
- Demostrar texto, salida estructurada, pipeline opcional de audio y uso multimodal opcional.

Salidas clave:

- Muestra baseline de seguimiento de instrucciones.
- Muestra de generacion JSON/estructurada.
- Muestra opcional de analisis ASR-a-Gemma.
- Muestra opcional de prompt imagen+texto.

### 01_gemma4_stage1_sft_qlora.ipynb

Objetivo:

- Implementar Stage 1 de ajuste fino supervisado con TRL SFTTrainer y PEFT LoRA.
- Construir un artefacto reutilizable de adaptador Stage 1 para warm-start en Stage 2.

Salidas clave:

- Adaptador SFT entrenado y guardado en local.
- Copia opcional en Google Drive.
- Artefacto opcional de modelo en W&B.
- Comprobacion cualitativa de generacion tras SFT.

### 02_gemma4_stage2_preference_and_stage3_reasoning_rl.ipynb

Objetivo:

- Stage 2: ejecutar DPO sobre un conjunto de datos de preferencias.
- Stage 3: ejecutar GRPO sobre razonamiento tipo GSM8K con recompensas de formato + exactitud.
- Guardar salidas de Stage 3 y compararlas con el baseline sin ajuste.

Nota de estado actual:

- En las ultimas ejecuciones de Colab, GRPO no supero de forma consistente al baseline en el conjunto pequeno de comprobacion rapida.
- Este es un resultado intermedio valido y debe documentarse como parte de la iteracion experimental (diseno de recompensas, presupuesto de entrenamiento y tamano del conjunto de evaluacion).

Salidas clave:

- Registros de entrenamiento DPO/GRPO.
- Artefactos de modelo Stage 3 guardados.
- Tabla de comparacion baseline vs tuned y resumen de exactitud.

## Referencias usadas en este flujo

- Model cards de Gemma (Hugging Face):
  - https://huggingface.co/google/gemma-4-E2B-it
- Documentacion de Transformers:
  - https://huggingface.co/docs/transformers/index
- Documentacion de TRL (entrenadores SFT, DPO, GRPO):
  - https://huggingface.co/docs/trl/index
- Documentacion de PEFT (adaptadores LoRA):
  - https://huggingface.co/docs/peft/index
- Documentacion de Datasets:
  - https://huggingface.co/docs/datasets/index
- Documentacion de Weights and Biases:
  - https://docs.wandb.ai/

Conjuntos de datos referenciados en los cuadernos:

- Capybara (SFT): trl-lib/Capybara
- UltraFeedback binarized (DPO): trl-lib/ultrafeedback_binarized
- GSM8K (tarea GRPO): openai/gsm8k (con fallbacks de compatibilidad)

## Orden de ejecucion sugerido

1. Ejecuta el cuaderno 00 para capturar el comportamiento baseline para tus diapositivas.
2. Ejecuta el cuaderno 01 para generar artefactos del adaptador Stage 1.
3. Ejecuta el cuaderno 02 para experimentos de Stage 2 y Stage 3, y comparacion final.

## Reproducibilidad y notas de Colab

- Si se actualizan versiones de paquetes en celdas de instalacion, reinicia runtime y vuelve a ejecutar todas las celdas.
- Manten HF_TOKEN y WANDB_API_KEY en secretos de Colab siempre que sea posible.
- Para warm-start en Stage 2 desde Stage 1, configura SFT_ADAPTER_PATH con la ruta del adaptador guardado.
- Interpreta los cambios de metricas de GRPO en conjuntos de evaluacion muy pequenos como orientativos, no concluyentes.

## Script didactico: intuicion de enrutado MoE

Para ilustrar como un modelo puede almacenar muchos parametros totales y usar
solo un subconjunto por token en inferencia, utiliza:

- `scripts/moe_routing_demo.py`

Ejemplo de ejecucion:

```bash
python scripts/moe_routing_demo.py --tokens 12 --experts 16 --top-k 2
```

Este script es una demo conceptual (no una implementacion MoE de produccion).

Para una tabla tipo heatmap token-a-experto en texto plano, utiliza:

- `scripts/moe_routing_heatmap_demo.py`

Ejemplo de ejecucion:

```bash
python scripts/moe_routing_heatmap_demo.py --tokens 8 --experts 12 --top-k 2
```

## Siguientes pasos de documentacion

- Anadir registros experimentales por etapa (hiperparametros + metricas finales) en un informe dedicado.
- Ampliar la evaluacion de 3 prompts rapidos a un conjunto held-out mayor para obtener conclusiones mas solidas.
- Anadir una seccion breve de "Problemas conocidos y mitigaciones" basada en las guardas de compatibilidad de Colab.
