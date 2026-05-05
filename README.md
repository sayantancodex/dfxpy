# dfxpy ⚡

**dfxpy** is a high-performance DataFrame workflow accelerator designed to reduce data preparation and analysis from hours to seconds. It is not a pandas wrapper, but a deterministic system for production-ready data pipelines.

## 🎯 Core Vision

Go from **raw dataset → clean, analyzed, model-ready data** in minimal lines of code.

- **Fast**: Optimized for performance.
- **Deterministic**: No AI randomness.
- **Lightweight**: Minimal dependencies (Pandas, NumPy, Scikit-learn).
- **Production-ready**: Follows PEP8 and best practices.

## ✨ Features

- `auto()`: One-line cleaning, imputation, and encoding.
- `eda()`: Structured, readable exploratory data analysis.
- `audit()`: Intelligent diagnostics (ID detection, multicollinearity, skewness).
- `prepare()`: ML-ready dataset preparation (X, y split, scaling).
- `outliers()`: IQR-based outlier handling (remove or cap).
- `suggest_features()`: Smart feature ranking and redundancy detection.

## 🚀 Quick Start

### Installation

```bash
pip install dfxpy
```

### Basic Usage

```python
import dfxpy as dfx
import pandas as pd

# Load raw data
df = pd.read_csv("data.csv")

# 1. Auto-clean everything
df_clean = dfx.auto(df)

# 2. Get insights
dfx.eda(df_clean)
dfx.audit(df_clean)

# 3. Prepare for ML
X, y = dfx.prepare(df_clean, target="price")
```

## ⚡ CLI

```bash
# Analyze a dataset
dfxpy analyze data.csv

# Prepare for ML
dfxpy prepare data.csv --target price
```

## 🧠 Before vs After

**Before (Standard Pandas):**
```python
df.columns = [c.lower().replace(' ', '_') for c in df.columns]
df = df.drop_duplicates()
df['age'] = df['age'].fillna(df['age'].median())
df['city'] = df['city'].fillna(df['city'].mode()[0])
df = pd.get_dummies(df, columns=['city'])
X = df.drop('target', axis=1)
y = df['target']
```

**After (dfxpy):**
```python
import dfxpy as dfx
df = dfx.auto(df)
X, y = dfx.prepare(df, target='target')
```

## 📄 License

MIT
