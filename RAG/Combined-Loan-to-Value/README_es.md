# Herramienta de Análisis CLTV

Una aplicación integral de análisis de préstamos hipotecarios que combina cálculos tradicionales de Combined Loan-to-Value (CLTV) con evaluación de riesgo impulsada por IA y análisis de calificación de prestatarios.

## Visión General

Esta aplicación proporciona a profesionales hipotecarios, underwriters y oficiales de préstamos herramientas avanzadas para analizar perfiles de riesgo de prestatarios, calcular ratios de préstamos y generar recomendaciones integrales de lending. El sistema combina cálculos hipotecarios tradicionales con análisis moderno de IA para proporcionar insights detallados sobre escenarios de calificación de préstamos.

## Características

### Capacidades de Análisis Principal
- **Análisis de Combined Loan-to-Value (CLTV)**: Calcular y evaluar ratios CLTV incluyendo todos los gravámenes contra una propiedad
- **Cálculos de Debt-to-Income (DTI)**: Análisis de DTI front-end y back-end con umbrales específicos por programa de préstamo
- **Puntuación Integral de Prestatario**: Evaluación de riesgo multifactorial combinando CLTV, DTI, credit scores e historial laboral
- **Comparaciones de Escenarios de Préstamo**: Comparar múltiples estructuras de préstamo y escenarios de down payment
- **Análisis PMI/MIP**: Cálculos de Private Mortgage Insurance y cronogramas de eliminación
- **Impacto de Consolidación de Deudas**: Evaluar el efecto de la consolidación de deudas en la calificación de préstamos
- **Calculadora de Capacidad de Compra**: Determinar precio máximo de compra basado en parámetros de ingresos y deudas

### Características Impulsadas por IA
- **Evaluación Inteligente de Riesgo**: Análisis basado en LLM de perfiles de prestatarios
- **Interacción en Lenguaje Natural**: Interfaz de chat para preguntas de lending hipotecario
- **Recomendaciones Automatizadas**: Consejos de lending generados por IA y estrategias de mejora
- **Análisis de Compliance**: Verificación automatizada contra guías de lending y regulaciones

### Soporte de Programas de Préstamo
- Préstamos Convencionales (Fannie Mae/Freddie Mac)
- Préstamos FHA
- Préstamos VA
- Préstamos USDA Rural Development

## Instalación

### Prerrequisitos
- Python 3.12 o superior
- API keys requeridas para características de IA (OpenAI o Google Vertex AI)

### Instrucciones de Configuración

1. **Clonar el Repositorio**
   ```bash
   git clone <repository-url>
   cd cltv
   ```

2. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuración de Entorno**
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   # Elegir tu proveedor de IA
   MODEL_PROVIDER=openai  # o 'vertexai'
   
   # Para OpenAI
   OPENAI_API_KEY=tu_clave_openai_aqui
   
   # Para Google Vertex AI
   GOOGLE_CLOUD_PROJECT=tu_project_id
   # Asegurar que las credenciales de Google Cloud estén configuradas
   ```

4. **Verificar Instalación**
   ```bash
   python basic_analysis.py
   ```

## Uso

### Interfaz de Línea de Comandos

#### Análisis Básico de Prestatario
```bash
python basic_analysis.py
```
Ejecuta un análisis integral de prestatario con parámetros predefinidos.

#### Precalificación Rápida de Préstamo
```bash
python prequalification.py
```
Realiza un análisis de precalificación simplificado.

### Interfaz Web Streamlit

#### Simulador CLTV Mejorado (Recomendado)
```bash
streamlit run cltv_simulator_enhanced.py
```
- Interfaz completa con análisis tradicional e impulsado por IA
- Múltiples modos de análisis y herramientas
- Visualizaciones interactivas y modelado de escenarios

#### Simulador CLTV Tradicional
```bash
streamlit run cltv_simulator.py
```
- Interfaz clásica de calculadora CLTV
- Análisis de escenarios y evaluación de riesgo
- Contenido educativo sobre conceptos CLTV

#### Interfaz de Análisis Impulsada por IA
```bash
streamlit run cltv_simulator_ai.py
```
- Enfocada en capacidades de análisis impulsadas por IA
- Interacción en lenguaje natural
- Evaluación avanzada de riesgo de prestatarios

#### Interfaz de Chat
```bash
streamlit run cltv_chat_interface.py
```
- Chat interactivo con asistente de lending de IA
- Consejos de lending hipotecario en tiempo real
- Prompts de ejemplo e interacciones guiadas

## Referencia de API

### Funciones de Análisis Principal

#### `analyze_borrower_comprehensive()`
Realiza análisis completo de prestatario usando todas las herramientas de evaluación disponibles.

```python
from cltv_ai_agent import analyze_borrower_comprehensive

result = analyze_borrower_comprehensive(
    property_value=500000.0,
    primary_loan_amount=400000.0,
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    proposed_housing_payment=3200.0,
    credit_score=740,
    down_payment=100000.0,
    secondary_loans=[25000.0],
    employment_years=3.5,
    liquid_assets=50000.0,
    loan_type="conventional"
)
```

#### `quick_loan_prequalification()`
Análisis de precalificación simplificado para screening inicial de prestatarios.

```python
from cltv_ai_agent import quick_loan_prequalification

result = quick_loan_prequalification(
    property_value=500000.0,
    down_payment=100000.0,
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    credit_score=740
)
```

### Herramientas de Análisis

#### Herramienta de Análisis CLTV
```python
from cltv_ai_agent import create_cltv_agent
from langchain_core.messages import HumanMessage

graph = create_cltv_agent()
config = {"configurable": {"thread_id": "analysis_session"}}

# Usar herramienta calculate_cltv_analysis
result = graph.invoke({
    "messages": [HumanMessage(content="""
    Usar calculate_cltv_analysis con:
    - Property Value: 500000
    - Primary Loan: 400000
    - Secondary Loans: [25000]
    - Down Payment: 100000
    """)]
}, config)
```

#### Herramienta de Análisis DTI
```python
# Usar herramienta calculate_dti_analysis a través del agente
result = graph.invoke({
    "messages": [HumanMessage(content="""
    Usar calculate_dti_analysis con:
    - Gross Monthly Income: 8000
    - Monthly Debt Payments: 800
    - Proposed Housing Payment: 3200
    - Loan Type: conventional
    """)]
}, config)
```

### Herramientas Avanzadas

#### Análisis PMI
```python
from mortgage_tools import calculate_pmi_analysis

result = calculate_pmi_analysis(
    loan_amount=400000.0,
    property_value=500000.0,
    credit_score=740,
    loan_type="conventional"
)
```

#### Análisis de Consolidación de Deudas
```python
from mortgage_tools import analyze_debt_consolidation_impact

result = analyze_debt_consolidation_impact(
    current_monthly_debts=1200.0,
    debt_balances="[15000, 8000, 12000, 5000]",
    consolidation_amount=40000.0,
    new_payment=800.0,
    gross_monthly_income=8000.0
)
```

#### Calculadora de Capacidad de Compra de Vivienda
```python
from mortgage_tools import calculate_affordability_analysis

result = calculate_affordability_analysis(
    gross_monthly_income=8000.0,
    monthly_debt_payments=800.0,
    down_payment_available=100000.0,
    target_dti=36.0,
    interest_rate=6.5,
    loan_term=30
)
```

## Configuración

### Configuración de Proveedor de IA

#### Configuración OpenAI
```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=sk-tu-clave-aqui
```

#### Configuración Google Vertex AI
```env
MODEL_PROVIDER=vertexai
GOOGLE_CLOUD_PROJECT=tu-project-id
```
Asegurar que Google Cloud SDK esté instalado y autenticado.

### Configuraciones de Aplicación

La aplicación soporta varias opciones de configuración a través de variables de entorno y parámetros de tiempo de ejecución:

- **Proveedor de Modelo**: Elegir entre OpenAI y Google Vertex AI
- **Profundidad de Análisis**: Configurar modos de análisis integral vs. rápido
- **Umbrales de Riesgo**: Personalizar límites de niveles de riesgo CLTV y DTI
- **Parámetros de Programa de Préstamo**: Ajustar guías de lending para diferentes tipos de préstamo

## Estructura del Proyecto

```
cltv/
├── cltv_simulator.py              # Interfaz de calculadora CLTV tradicional
├── cltv_simulator_ai.py           # Interfaz de análisis mejorada con IA
├── cltv_simulator_enhanced.py     # Interfaz mejorada completa
├── cltv_chat_interface.py         # Interfaz de interacción basada en chat
├── cltv_ai_agent.py              # Agente de IA principal y motor de análisis
├── mortgage_tools.py              # Herramientas avanzadas de análisis hipotecario
├── basic_analysis.py              # Script de análisis de línea de comandos
├── prequalification.py            # Script de precalificación rápida
├── requirements.txt               # Dependencias de Python
├── pyproject.toml                # Configuración del proyecto
├── .env                          # Variables de entorno (creado por usuario)
├── .gitignore                    # Patrones de ignore de Git
└── README.md                     # Esta documentación
```

## Manejo de Errores

La aplicación incluye manejo integral de errores para escenarios comunes:

- **API Keys Faltantes**: Degradación elegante a análisis tradicional
- **Parámetros de Entrada Inválidos**: Validación y mensajes de error amigables al usuario
- **Problemas de Conectividad de Red**: Lógica de reintentos y capacidades de modo offline
- **Fallas de API del Modelo**: Respaldo a métodos de análisis alternativos

## Consideraciones de Rendimiento

- **Caching**: Los resultados de análisis de IA se almacenan en cache para mejorar tiempos de respuesta
- **Procesamiento por Lotes**: Múltiples análisis de prestatarios se pueden procesar eficientemente
- **Gestión de Recursos**: El uso de memoria está optimizado para procesamiento a gran escala

## Notas de Seguridad

- Las API keys se almacenan en variables de entorno, no en código
- Los datos sensibles del prestatario se procesan localmente cuando es posible
- Todas las comunicaciones de API externas usan protocolos seguros
- No se almacenan datos del prestatario permanentemente por defecto

## Contribuir

Esta aplicación está diseñada para profesionales de lending hipotecario y puede extenderse con herramientas de análisis adicionales, programas de préstamo o capacidades de IA. La arquitectura modular soporta integración fácil de nuevas características.

## Soporte

Para soporte técnico o solicitudes de características, referirse a la documentación en línea y comentarios del código. La aplicación incluye logging extensivo para propósitos de troubleshooting.

## Descargo de Responsabilidad

Esta herramienta está diseñada para análisis profesional de lending hipotecario y propósitos educativos. Todas las decisiones de lending deben hacerse de acuerdo con regulaciones y guías aplicables. Los usuarios deben verificar cálculos y recomendaciones con estándares de lending actuales y requerimientos legales.