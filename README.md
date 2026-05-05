# dfxpy: The DataFrame Workflow Accelerator ⚡

[![PyPI version](https://img.shields.io/pypi/v/dfxpy.svg?cache=0.2.0)](https://pypi.org/project/dfxpy/)
[![Python versions](https://img.shields.io/pypi/pyversions/dfxpy.svg?cache=0.2.0)](https://pypi.org/project/dfxpy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?cache=0.2.0)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?cache=0.2.0)]()

**dfxpy** is a high-performance Python library designed to reduce the entire data preparation and analysis workflow into a few powerful, deterministic operations. It helps data scientists and engineers go from raw, messy datasets to model-ready features in seconds, not hours.

---

## 🎯 Why dfxpy?

While `pandas` is the industry standard for data manipulation, cleaning a dataset for machine learning often requires writing repetitive boilerplate code. **dfxpy** acts as an accelerator, automating the "grunt work" while providing intelligent diagnostics and insights.

- **Fast & Deterministic**: Optimized operations without the unpredictability of AI.
- **Production-Ready**: Type-hinted, modular, and follows PEP8 standards.
- **Lightweight**: Minimal dependencies—built on top of `pandas`, `numpy`, and `scikit-learn`.
- **Self-Contained**: Load and analyze data without needing to import multiple libraries.

---

## ✨ Key Features

### 🛠️ Auto-Pilot Cleaning (`auto`)
One-line pipeline for column normalization (snake_case), duplicate removal, smart type inference (Object → Numeric/Datetime), and missing value imputation.

### 🔍 Deep Audit (`audit`)
Intelligent dataset diagnostics that detect:
- ID-like columns (uniqueness checks)
- High cardinality categoricals
- Multicollinearity (correlated features)
- Data skewness and low-variance columns

### 🚀 ML Preparation (`prepare`)
Transform your data into `X` and `y` instantly. Automatically handles categorical target encoding (LabelEncoding), feature encoding (One-Hot), and optional scaling.

### 📉 Smart EDA (`eda`)
Generates structured, human-readable summaries of shapes, nulls, unique counts, and correlation matrices.

### 🧹 Outlier Management (`outliers`)
Detect and handle outliers using the IQR (Interquartile Range) method with options to **remove** or **cap**.

---

## 📦 Installation

Install the latest version via pip:

```bash
pip install dfxpy
```

---

## 🚀 Quick Start

### Python API

```python
import dfxpy as dfx

# 1. Load data directly
df = dfx.load("raw_data.csv")

# 2. Run auto-clean (names, types, nulls, encoding)
df_clean = dfx.auto(df)

# 3. Get intelligent insights
dfx.audit(df_clean)

# 4. Prepare for Machine Learning
X, y = dfx.prepare(df_clean, target="outcome")
```

### Command Line Interface (CLI)

```bash
# Analyze a dataset instantly
dfxpy analyze data.csv

# Prepare data for ML via CLI
dfxpy prepare data.csv --target price --output cleaned_features.csv
```

---

## 🧠 Pandas vs. dfxpy

| Task | Standard Pandas | dfxpy |
| :--- | :--- | :--- |
| **Load Data** | `pd.read_csv("data.csv")` | `dfx.load("data.csv")` |
| **Clean Names** | `df.columns = [c.lower().replace(' ', '_') for c in df.columns]` | `dfx.auto(df)` |
| **Handle Nulls** | `df['val'].fillna(df['val'].median())` | `dfx.auto(df)` |
| **ML Prep** | 10+ lines (Split, Encode, Scale) | `dfx.prepare(df, target='y')` |
| **Audit** | Manual inspection | `dfx.audit(df)` |

---

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to submit issues, feature requests, and pull requests.

## 📄 License

**dfxpy** is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <i>Built with ❤️ for the Data Science Community.</i>
</p>
