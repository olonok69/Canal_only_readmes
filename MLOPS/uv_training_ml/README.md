# Repositorio de Entrenamiento de uv

Este repositorio es un espacio práctico para aprender y demostrar el gestor de paquetes de Python uv y su flujo de trabajo.

## Qué hacemos aquí

- Crear y administrar proyectos de Python con uv.
- Agregar, bloquear y sincronizar dependencias.
- Ejecutar scripts de Python en entornos administrados.
- Demostrar dependencias temporales de ejecución usando uv run --with ...
- Practicar flujos básicos de herramientas (por ejemplo, linting con Ruff).

## Estructura del repositorio

- uv_training/: Carpeta principal del proyecto de entrenamiento.
- uv_training/pyproject.toml: Metadatos del proyecto y dependencias.
- uv_training/main.py: Script principal de ejemplo.
- uv_training/demo.py: Script de demostración usado en ejemplos de uv run --with.
- uv_training/example.py: Script de ejemplo adicional.
- uv commands.txt: Hoja de referencia de comandos usada en el entrenamiento.
- uv_presentation_guide.md: Notas y guía para la presentación del entrenamiento.

## Flujo de trabajo típico

1. Instalar uv.
2. Inicializar o abrir un proyecto.
3. Agregar dependencias con uv add.
4. Sincronizar el entorno con uv sync.
5. Ejecutar scripts con uv run.
6. Opcionalmente, ejecutar scripts con dependencias temporales; por ejemplo:
   - uv run --with rich --with requests uv_training/demo.py

## Por qué existe este repositorio

Este repositorio está pensado para aprender, hacer demostraciones y practicar de forma repetible la gestión moderna de dependencias y entornos en Python con uv.
