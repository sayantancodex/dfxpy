# dfxpy ⚡

**dfxpy** is a high-performance DataFrame workflow accelerator designed to reduce data preparation and analysis from hours to seconds. It is not a pandas wrapper, but a deterministic system for production-ready data pipelines.

## 🎯 Core Vision

Go from **raw dataset → clean, analyzed, model-ready data** in minimal lines of code.

- **Fast**: Optimized for performance.
- **Deterministic**: No AI randomness.
- **Lightweight**: Minimal dependencies.
- **Self-contained**: No need to import pandas directly for common tasks.

## ✨ Features

- `load()` / `read_csv()`: Load data directly without importing pandas.
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

# 1. Load data directly (no pandas import needed!)
df = dfx.load("data.csv")

# 2. Auto-clean everything
df_clean = dfx.auto(df)

# 3. Get insights
dfx.eda(df_clean)
dfx.audit(df_clean)

# 4. Prepare for ML
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
import pandas as pd
df = pd.read_csv("data.csv")
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
df = dfx.load("data.csv")
df = dfx.auto(df)
X, y = dfx.prepare(df, target='target')
```

## 📄 License

MIT
