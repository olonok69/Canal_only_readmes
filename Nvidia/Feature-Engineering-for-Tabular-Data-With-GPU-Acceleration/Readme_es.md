# Mejores Prácticas en Feature Engineering para Datos Tabulares con Aceleración GPU

## Descripción General

Este repositorio contiene tres notebooks comprensivos que demuestran técnicas avanzadas de feature engineering para datos tabulares usando aceleración GPU con RAPIDS cuDF y cuML. Los notebooks cubren target encoding, count encoding, y entrenamiento de modelos con XGBoost y Support Vector Machines, comparando el rendimiento de CPU vs GPU a lo largo del proceso.

## Tabla de Contenidos

1. [Target Encoding con Aceleración GPU](#target-encoding)
2. [Count Encoding con Aceleración GPU](#count-encoding)
3. [Entrenamiento de Modelos con cuML y XGBoost](#entrenamiento-de-modelos)
4. [Librerías y Tecnologías](#librerías-y-tecnologías)
5. [Comparaciones de Rendimiento](#comparaciones-de-rendimiento)
6. [Instalación y Configuración](#instalación-y-configuración)

## Target Encoding

### Descripción General
Target Encoding (TE) es una técnica avanzada de codificación categórica que reemplaza valores categóricos con agregaciones estadísticas (típicamente la media) de la variable target para cada categoría. Esta técnica es particularmente poderosa para modelos basados en árboles y escenarios con features categóricos de alta cardinalidad.

### Detalles de Implementación

El notebook demuestra tres componentes clave del target encoding robusto:

#### 1. Target Encoding Básico
```python
te = df_train[['brand', 'label']].groupby('brand').mean()
```

**Ventajas:**
- Captura la relación entre features categóricos y el target
- Reduce la dimensionalidad comparado con one-hot encoding
- Particularmente efectivo para features de alta cardinalidad
- Preserva relaciones ordinales basadas en correlación con el target

**Desventajas:**
- Propenso al overfitting, especialmente con categorías de baja frecuencia
- Puede causar target leakage si no se implementa correctamente
- Puede no generalizar bien a categorías no vistas

#### 2. Técnica de Smoothing
Para mitigar el overfitting, la implementación usa smoothing Bayesiano:

```python
smoothed_te = ((category_mean * category_count) + (global_mean * smoothing_weight)) / (category_count + smoothing_weight)
```

**Parámetros:**
- `smoothing_weight (w)`: Controla el balance entre estadísticas específicas de categoría y globales
- Valores más altos llevan las estimaciones hacia la media global para categorías raras
- Rango recomendado: 10-50 dependiendo del tamaño del dataset

#### 3. Out-of-Fold Encoding
Previene target leakage mediante k-fold cross-validation:

```python
def target_encode(train, valid, col, target, kfold=5, smooth=20):
    train['kfold'] = ((train.index) % kfold)
    for i in range(kfold):
        # Usar todos los folds excepto el i-ésimo para codificar el i-ésimo fold
```

**Beneficios:**
- Elimina target leakage en los datos de entrenamiento
- Proporciona estimaciones de rendimiento más realistas
- Mejora la generalización del modelo

### Cuándo Usar Target Encoding

**Recomendado para:**
- Features categóricos de alta cardinalidad (>10 valores únicos)
- Modelos basados en árboles (XGBoost, LightGBM, CatBoost)
- Tareas de clasificación binaria o regresión
- Features con relación clara con la variable target

**Evitar cuando:**
- Features de muy baja cardinalidad (<5 valores únicos)
- Datasets extremadamente pequeños
- Problemas multi-clase con muchas clases
- Cuando la interpretabilidad es crítica

### Resultados de Rendimiento
- **Aceleración GPU:** 20x más rápido comparado con implementación CPU
- **Mejora AUC:** Incremento significativo en scores de validación comparado con label encoding básico

## Count Encoding

### Descripción General
Count Encoding (CE) reemplaza valores categóricos con su frecuencia de ocurrencia en el dataset de entrenamiento. Esta técnica es particularmente útil para capturar la popularidad o rareza de valores categóricos.

### Detalles de Implementación

#### Count Encoding Básico
```python
ce = df_train[col].value_counts().reset_index()
ce.columns = [col, 'CE_' + col]
```

#### Count Encoding por Grupos
```python
ce = df_train[['cat_2', 'brand', 'label']].groupby(['cat_2', 'brand']).count()
```

### Ventajas del Count Encoding

**Fortalezas:**
- Simple e interpretable
- Captura importancia del feature a través de frecuencia
- Bajo riesgo de overfitting
- Efectivo para sistemas de recomendación
- Overhead computacional mínimo

**Aplicaciones:**
- Niveles de actividad de usuario en sistemas de recomendación
- Popularidad de productos en e-commerce
- Detección de fraude (patrones basados en frecuencia)
- Métricas de engagement de contenido

### Desventajas

**Limitaciones:**
- No captura directamente la relación con el target
- Puede no ser efectivo para distribuciones categóricas balanceadas
- Poder predictivo limitado para targets no dependientes de frecuencia
- Puede crear relaciones ordinales artificiales

### Cuándo Usar Count Encoding

**Escenarios ideales:**
- Sistemas de recomendación (popularidad usuario/item)
- Detección de anomalías (eventos raros)
- Features donde la frecuencia se correlaciona con el target
- Como features complementarios junto con otras codificaciones

**Evitar cuando:**
- Los valores categóricos tienen distribución uniforme
- La frecuencia no se relaciona con la variable target
- Restricciones de memoria (crea features adicionales)

### Resultados de Rendimiento
- **Aceleración GPU:** 15x más rápido comparado con CPU
- **Tiempo de Procesamiento:** ~0.5 segundos vs ~7.5 segundos en CPU

## Entrenamiento de Modelos

### Implementación XGBoost

El notebook compara tres enfoques de codificación categórica con XGBoost:

#### 1. Soporte Categórico Built-in
```python
params = {
    'objective': 'binary:logistic',
    'tree_method': 'hist',
    'device': 'cuda',
    'enable_categorical': True
}
```

**Pros:**
- No requiere preprocesamiento
- Maneja valores faltantes automáticamente
- Algoritmos de splitting optimizados para features categóricos

**Contras:**
- Puede hacer overfitting con features de alta cardinalidad
- Control limitado sobre la estrategia de codificación
- Feature más nueva con posibles problemas de estabilidad

#### 2. Label Encoding
```python
LE = LabelEncoder()
train[col] = LE.fit_transform(train[col])
```

**Pros:**
- Implementación simple
- Eficiente en memoria
- Reduce overfitting a través de asignación aleatoria

**Contras:**
- Crea relaciones ordinales artificiales
- Puede no capturar patrones significativos
- El rendimiento depende de la asignación aleatoria de labels

#### 3. Target Encoding + Label Encoding
Enfoque combinado usando ambas técnicas:

**Resultados:**
- Mejor rendimiento: Target + Label Encoding
- Mejora AUC: ~2-3% sobre enfoques básicos
- Tiempo de entrenamiento: ~4 segundos en GPU vs ~32 segundos en CPU

### Implementación Support Vector Machine

#### Feature Engineering para SVM

**1. Preprocesamiento StandardScaler:**
```python
SS = StandardScaler().fit(train[[col]])
train[col] = SS.transform(train[[col]])
```

**Justificación:** SVM requiere features normalizados para rendimiento óptimo

**2. Feature Engineering TF-IDF:**
```python
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=10)
tfidf_features = tfidf.fit_transform(product_text)
```

**Beneficios:**
- Captura patrones textuales en combinaciones categóricas
- Crea representaciones densas de features
- Mejora significativamente el rendimiento del modelo

#### Comparación de Rendimiento
- **SVM con Target Encoding:** Rendimiento baseline
- **SVM con TF-IDF:** Rendimiento superior a través de representación más rica de features
- **GPU vs CPU:** 100x+ speedup para entrenamiento SVM

## Librerías y Tecnologías

### RAPIDS cuDF
**Propósito:** Operaciones DataFrame aceleradas por GPU

**Ventajas:**
- Reemplazo directo para pandas con cero cambios de código
- Mejoras significativas de rendimiento para datasets grandes
- Operaciones GPU eficientes en memoria
- Integración fluida con cuML

**Desventajas:**
- Limitaciones de memoria GPU
- Ecosistema limitado comparado con pandas
- Dependencia de hardware (GPUs NVIDIA requeridas)
- Algunas funcionalidades de pandas aún no soportadas

### RAPIDS cuML
**Propósito:** Algoritmos de machine learning acelerados por GPU

**Componentes Clave Utilizados:**
- `LabelEncoder`: Codificación categórica acelerada por GPU
- `TargetEncoder`: Target encoding built-in con cross-validation
- `StandardScaler`: Normalización de features
- `SVC`: Clasificador Support Vector Machine
- `TfidfVectorizer`: Extracción de features de texto

**Ventajas:**
- API compatible con scikit-learn
- Mejoras masivas de rendimiento
- Gestión built-in de memoria GPU
- Algoritmos optimizados para arquitectura GPU

**Desventajas:**
- Cobertura limitada de algoritmos comparado con scikit-learn
- Restricciones de memoria GPU
- Requerimientos de hardware
- Posibles diferencias numéricas con implementaciones CPU

### Soporte GPU XGBoost
**Configuración:**
```python
params = {
    'device': 'cuda',
    'tree_method': 'hist'
}
```

**Beneficios:**
- 10x+ speedup en entrenamiento
- Soporte built-in para features categóricos
- Utilización eficiente de memoria GPU
- Rendimiento listo para producción

## Comparaciones de Rendimiento

### Rendimiento Target Encoding
- **GPU (cuDF-Pandas):** ~3 segundos
- **CPU (Pandas):** ~60 segundos
- **Speedup:** 20x mejora

### Rendimiento Count Encoding
- **GPU (cuDF-Pandas):** ~0.5 segundos
- **CPU (Pandas):** ~7.5 segundos
- **Speedup:** 15x mejora

### Rendimiento Entrenamiento de Modelos

#### XGBoost
- **GPU:** ~4 segundos
- **CPU:** ~32 segundos
- **Speedup:** 8x mejora

#### Support Vector Machine
- **GPU (cuML):** ~15 segundos
- **CPU (scikit-learn):** >1 hora
- **Speedup:** 100x+ mejora

## Información del Dataset

**Fuente:** Amazon Product Reviews Dataset
- **Tamaño:** 142.8 millones de reviews (Mayo 1996 - Julio 2014)
- **Features:** Metadata de productos, información de usuario, jerarquías categóricas
- **Target:** Clasificación binaria (recomendación de producto)

**Características Clave:**
- Features categóricos de alta cardinalidad
- Distribución desbalanceada del target
- Valores faltantes en columnas categóricas
- Estructura de categorías jerárquica

## Instalación y Configuración

### Requerimientos
```bash
# Instalación RAPIDS (requiere GPU NVIDIA)
conda create -n rapids-env -c rapidsai -c conda-forge -c nvidia \
    rapids=25.04 python=3.11 cudatoolkit=12.0

# XGBoost con soporte GPU
pip install xgboost[gpu]

# Dependencias adicionales
pip install matplotlib scikit-learn
```

### Configuración Docker
```bash
docker run --gpus all --pull always --rm -it \
    --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
    -p 8888:8888 -p 8787:8787 -p 8786:8786 \
    nvcr.io/nvidia/rapidsai/notebooks:25.08-cuda12.9-py3.13
```

## Mejores Prácticas y Recomendaciones

### Estrategia de Feature Engineering
1. **Comenzar Simple:** Empezar con codificaciones básicas (Label, One-Hot)
2. **Agregar Complejidad:** Implementar Target/Count encoding para mejoras
3. **Validar Correctamente:** Usar técnicas out-of-fold para prevenir overfitting
4. **Combinar Técnicas:** Usar múltiples estrategias de codificación juntas
5. **Monitorear Rendimiento:** Trackear tanto métricas de entrenamiento como validación

### Guías de Selección de Modelos

**Usar XGBoost cuando:**
- Datos tabulares con tipos de features mixtos
- Features categóricos de alta cardinalidad
- Necesidad de interpretación de feature importance
- Rendimiento robusto across varios dominios

**Usar SVM cuando:**
- Features con mucho texto se benefician de TF-IDF
- Datasets más pequeños donde el tiempo de entrenamiento es manejable
- Necesidad de clasificación maximum margin
- El feature engineering puede crear representaciones significativas

### Consideraciones de Aceleración GPU

**Cuándo la Aceleración GPU es Más Beneficiosa:**
- Datasets grandes (>100K filas)
- Pipelines complejos de feature engineering
- Workflows de experimentación iterativa
- Ambientes de producción con requerimientos de throughput

**Limitaciones a Considerar:**
- Restricciones de memoria GPU
- Disponibilidad y costo de hardware
- Complejidad de desarrollo para casos edge
- Posibles diferencias de precisión numérica

## Conclusión

Este repositorio demuestra el impacto significativo del feature engineering adecuado y la aceleración GPU en workflows de machine learning. La combinación de técnicas avanzadas de codificación con el ecosistema RAPIDS proporciona tanto mejoras de rendimiento como mejor accuracy del modelo. Los speedups de 10-100x permiten experimentación e iteración rápida, lo cual es crucial para desarrollar modelos de machine learning de alta calidad en ambientes de producción.

Las técnicas presentadas aquí son particularmente valiosas para practicantes trabajando con datos tabulares a gran escala, sistemas de recomendación, y escenarios que requieren ciclos rápidos de desarrollo de modelos.