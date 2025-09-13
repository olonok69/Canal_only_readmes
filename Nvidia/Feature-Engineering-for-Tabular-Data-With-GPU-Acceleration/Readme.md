# Best Practices in Feature Engineering for Tabular Data With GPU Acceleration

## Overview

This repository contains three comprehensive notebooks demonstrating advanced feature engineering techniques for tabular data using GPU acceleration with RAPIDS cuDF and cuML. The notebooks cover target encoding, count encoding, and model training with both XGBoost and Support Vector Machines, comparing CPU vs GPU performance throughout.

## Table of Contents

1. [Target Encoding with GPU Acceleration](#target-encoding)
2. [Count Encoding with GPU Acceleration](#count-encoding)
3. [Model Training with cuML and XGBoost](#model-training)
4. [Libraries and Technologies](#libraries-and-technologies)
5. [Performance Comparisons](#performance-comparisons)
6. [Installation and Setup](#installation-and-setup)

## Target Encoding

### Overview
Target Encoding (TE) is an advanced categorical encoding technique that replaces categorical values with statistical aggregations (typically mean) of the target variable for each category. This technique is particularly powerful for tree-based models and scenarios with high-cardinality categorical features.

### Implementation Details

The notebook demonstrates three key components of robust target encoding:

#### 1. Basic Target Encoding
```python
te = df_train[['brand', 'label']].groupby('brand').mean()
```

**Advantages:**
- Captures relationship between categorical features and target
- Reduces dimensionality compared to one-hot encoding
- Particularly effective for high-cardinality features
- Preserves ordinal relationships based on target correlation

**Disadvantages:**
- Prone to overfitting, especially with low-frequency categories
- Can cause target leakage if not properly implemented
- May not generalize well to unseen categories

#### 2. Smoothing Technique
To mitigate overfitting, the implementation uses Bayesian smoothing:

```python
smoothed_te = ((category_mean * category_count) + (global_mean * smoothing_weight)) / (category_count + smoothing_weight)
```

**Parameters:**
- `smoothing_weight (w)`: Controls the balance between category-specific and global statistics
- Higher values pull estimates toward global mean for rare categories
- Recommended range: 10-50 depending on dataset size

#### 3. Out-of-Fold Encoding
Prevents target leakage through k-fold cross-validation:

```python
def target_encode(train, valid, col, target, kfold=5, smooth=20):
    train['kfold'] = ((train.index) % kfold)
    for i in range(kfold):
        # Use all folds except i-th to encode i-th fold
```

**Benefits:**
- Eliminates target leakage in training data
- Provides more realistic performance estimates
- Improves model generalization

### When to Use Target Encoding

**Recommended for:**
- High-cardinality categorical features (>10 unique values)
- Tree-based models (XGBoost, LightGBM, CatBoost)
- Binary or regression tasks
- Features with clear relationship to target variable

**Avoid when:**
- Very low-cardinality features (<5 unique values)
- Extremely small datasets
- Multi-class problems with many classes
- When interpretability is critical

### Performance Results
- **GPU Acceleration:** 20x speedup compared to CPU implementation
- **AUC Improvement:** Significant boost in validation scores compared to basic label encoding

## Count Encoding

### Overview
Count Encoding (CE) replaces categorical values with their frequency of occurrence in the training dataset. This technique is particularly useful for capturing the popularity or rarity of categorical values.

### Implementation Details

#### Basic Count Encoding
```python
ce = df_train[col].value_counts().reset_index()
ce.columns = [col, 'CE_' + col]
```

#### Group-wise Count Encoding
```python
ce = df_train[['cat_2', 'brand', 'label']].groupby(['cat_2', 'brand']).count()
```

### Advantages of Count Encoding

**Strengths:**
- Simple and interpretable
- Captures feature importance through frequency
- Low risk of overfitting
- Effective for recommendation systems
- Minimal computational overhead

**Applications:**
- User activity levels in recommendation systems
- Product popularity in e-commerce
- Fraud detection (frequency-based patterns)
- Content engagement metrics

### Disadvantages

**Limitations:**
- Doesn't capture target relationship directly
- May not be effective for balanced categorical distributions
- Limited predictive power for non-frequency-dependent targets
- Can create artificial ordinal relationships

### When to Use Count Encoding

**Ideal scenarios:**
- Recommendation systems (user/item popularity)
- Anomaly detection (rare events)
- Features where frequency correlates with target
- As complementary features alongside other encodings

**Avoid when:**
- Categorical values have uniform distribution
- Frequency doesn't relate to target variable
- Memory constraints (creates additional features)

### Performance Results
- **GPU Acceleration:** 15x speedup compared to CPU
- **Processing Time:** ~0.5 seconds vs ~7.5 seconds on CPU

## Model Training

### XGBoost Implementation

The notebook compares three categorical encoding approaches with XGBoost:

#### 1. Built-in Categorical Support
```python
params = {
    'objective': 'binary:logistic',
    'tree_method': 'hist',
    'device': 'cuda',
    'enable_categorical': True
}
```

**Pros:**
- No preprocessing required
- Handles missing values automatically
- Optimized splitting algorithms for categorical features

**Cons:**
- May overfit with high-cardinality features
- Limited control over encoding strategy
- Newer feature with potential stability concerns

#### 2. Label Encoding
```python
LE = LabelEncoder()
train[col] = LE.fit_transform(train[col])
```

**Pros:**
- Simple implementation
- Memory efficient
- Reduces overfitting through random assignment

**Cons:**
- Creates artificial ordinal relationships
- May not capture meaningful patterns
- Performance depends on random label assignment

#### 3. Target Encoding + Label Encoding
Combination approach using both techniques:

**Results:**
- Best performance: Target + Label Encoding
- AUC improvement: ~2-3% over basic approaches
- Training time: ~4 seconds on GPU vs ~32 seconds on CPU

### Support Vector Machine Implementation

#### Feature Engineering for SVM

**1. StandardScaler Preprocessing:**
```python
SS = StandardScaler().fit(train[[col]])
train[col] = SS.transform(train[[col]])
```

**Rationale:** SVM requires normalized features for optimal performance

**2. TF-IDF Feature Engineering:**
```python
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=10)
tfidf_features = tfidf.fit_transform(product_text)
```

**Benefits:**
- Captures textual patterns in categorical combinations
- Creates dense feature representations
- Improves model performance significantly

#### Performance Comparison
- **SVM with Target Encoding:** Baseline performance
- **SVM with TF-IDF:** Superior performance through richer feature representation
- **GPU vs CPU:** 100x+ speedup for SVM training

## Libraries and Technologies

### RAPIDS cuDF
**Purpose:** GPU-accelerated DataFrame operations

**Advantages:**
- Drop-in replacement for pandas with zero code changes
- Significant performance improvements for large datasets
- Memory-efficient GPU operations
- Seamless integration with cuML

**Disadvantages:**
- GPU memory limitations
- Limited ecosystem compared to pandas
- Hardware dependency (NVIDIA GPUs required)
- Some pandas functionality not yet supported

### RAPIDS cuML
**Purpose:** GPU-accelerated machine learning algorithms

**Key Components Used:**
- `LabelEncoder`: GPU-accelerated categorical encoding
- `TargetEncoder`: Built-in target encoding with cross-validation
- `StandardScaler`: Feature normalization
- `SVC`: Support Vector Machine classifier
- `TfidfVectorizer`: Text feature extraction

**Advantages:**
- Scikit-learn compatible API
- Massive performance improvements
- Built-in GPU memory management
- Optimized algorithms for GPU architecture

**Disadvantages:**
- Limited algorithm coverage compared to scikit-learn
- GPU memory constraints
- Hardware requirements
- Potential numerical differences from CPU implementations

### XGBoost GPU Support
**Configuration:**
```python
params = {
    'device': 'cuda',
    'tree_method': 'hist'
}
```

**Benefits:**
- 10x+ training speedup
- Built-in categorical feature support
- Efficient GPU memory utilization
- Production-ready performance

## Performance Comparisons

### Target Encoding Performance
- **GPU (cuDF-Pandas):** ~3 seconds
- **CPU (Pandas):** ~60 seconds
- **Speedup:** 20x improvement

### Count Encoding Performance
- **GPU (cuDF-Pandas):** ~0.5 seconds
- **CPU (Pandas):** ~7.5 seconds
- **Speedup:** 15x improvement

### Model Training Performance

#### XGBoost
- **GPU:** ~4 seconds
- **CPU:** ~32 seconds
- **Speedup:** 8x improvement

#### Support Vector Machine
- **GPU (cuML):** ~15 seconds
- **CPU (scikit-learn):** >1 hour
- **Speedup:** 100x+ improvement

## Dataset Information

**Source:** Amazon Product Reviews Dataset
- **Size:** 142.8 million reviews (May 1996 - July 2014)
- **Features:** Product metadata, user information, categorical hierarchies
- **Target:** Binary classification (product recommendation)

**Key Characteristics:**
- High-cardinality categorical features
- Imbalanced target distribution
- Missing values in categorical columns
- Hierarchical category structure

## Installation and Setup

### Requirements
```bash
# RAPIDS installation (requires NVIDIA GPU)
conda create -n rapids-env -c rapidsai -c conda-forge -c nvidia \
    rapids=25.04 python=3.11 cudatoolkit=12.0

# XGBoost with GPU support
pip install xgboost[gpu]

# Additional dependencies
pip install matplotlib scikit-learn
```

### Docker Setup
```bash
docker run --gpus all --pull always --rm -it \
    --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
    -p 8888:8888 -p 8787:8787 -p 8786:8786 \
    nvcr.io/nvidia/rapidsai/notebooks:25.08-cuda12.9-py3.13
```

## Best Practices and Recommendations

### Feature Engineering Strategy
1. **Start Simple:** Begin with basic encodings (Label, One-Hot)
2. **Add Complexity:** Implement Target/Count encoding for improvement
3. **Validate Properly:** Use out-of-fold techniques to prevent overfitting
4. **Combine Techniques:** Use multiple encoding strategies together
5. **Monitor Performance:** Track both training and validation metrics

### Model Selection Guidelines

**Use XGBoost when:**
- Tabular data with mixed feature types
- High-cardinality categorical features
- Need for feature importance interpretation
- Robust performance across various domains

**Use SVM when:**
- Text-heavy features benefit from TF-IDF
- Smaller datasets where training time is manageable
- Need for maximum margin classification
- Feature engineering can create meaningful representations

### GPU Acceleration Considerations

**When GPU Acceleration is Most Beneficial:**
- Large datasets (>100K rows)
- Complex feature engineering pipelines
- Iterative experimentation workflows
- Production environments with throughput requirements

**Limitations to Consider:**
- GPU memory constraints
- Hardware availability and cost
- Development complexity for edge cases
- Potential numerical precision differences

## Conclusion

This repository demonstrates the significant impact of proper feature engineering and GPU acceleration on machine learning workflows. The combination of advanced encoding techniques with RAPIDS ecosystem provides both performance improvements and better model accuracy. The 10-100x speedups enable rapid experimentation and iteration, which is crucial for developing high-quality machine learning models in production environments.

The techniques presented here are particularly valuable for practitioners working with large-scale tabular data, recommendation systems, and scenarios requiring fast model development cycles.