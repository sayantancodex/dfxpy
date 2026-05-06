# dfxpy API Reference

This document provides a detailed breakdown of the functions and modules available in **dfxpy**.

---

## 🚀 Core Workflows

### `auto(df, verbose=True, eda_report=False)`
The primary entry point for rapid data cleaning.
- **Parameters**:
  - `df` (pd.DataFrame): The input dataset.
  - `verbose` (bool): If True, prints structured logs of cleaning actions.
  - `eda_report` (bool): If True, automatically runs `eda()` after cleaning.
- **Actions**:
  - Cleans column names (snake_case).
  - Drops duplicate rows.
  - Infers smart types (String -> Numeric/Date).
  - Imputes missing values (Median for numeric, Mode for categorical).
  - One-hot encodes categorical variables.
- **Returns**: A cleaned `pd.DataFrame`.

### `fix(df)`
Advanced, multi-pass cleaning and repair tool.
- **Actions**:
  - Cleans column names to snake_case.
  - Drops duplicates.
  - **Advanced Inference**: Detects and converts Currency ($), Percentages (%), Booleans (Yes/No), and complex Date strings.
  - **Auto-Imputation**: Handles missing values based on data type.
- **Returns**: A fully repaired `pd.DataFrame`.

### `prepare(df, target, scale=False, verbose=True)`
Streamlines the path from raw data to machine learning models.
- **Parameters**:
  - `df` (pd.DataFrame): The input dataset.
  - `target` (str): The name of the target column.
  - `scale` (bool): If True, applies StandardScaler to features.
  - `verbose` (bool): If True, prints logs of preparation steps.
- **Actions**:
  - Splits data into features (X) and target (y).
  - Handles target encoding (LabelEncoding for non-numeric targets).
  - Extracts date features.
  - One-hot encodes categorical features.
- **Returns**: `(X, y)` as a tuple of DataFrame and Series.

---

## 🔍 Diagnostics & Insights

### `eda(df)`
Generates a structured Exploratory Data Analysis summary.
- **Output**:
  - Dataset shape.
  - Data types per column.
  - Missing value counts.
  - Unique value counts.

### `report(df, output='report.html')`
Generates a premium, standalone HTML EDA report. Includes histograms and missingness heatmaps.

### `audit(df)`
Performs an automated diagnostic "check-up" of the dataset.
- **Flags**:
  - **IDs**: Detects columns that are likely unique identifiers.
  - **High Cardinality**: Flags categorical columns with too many unique values.
  - **Skewness**: Detects extreme numeric skewness.
  - **Multicollinearity**: Identifies features that are highly correlated with each other.

### `leakage(df, target)`
Detects potential data leakage by identifying features with suspicious predictive power.

### `compare(df1, df2)`
Generates a detailed diff between two DataFrames (columns, rows, and values).

---

## 🔬 Research & Statistics

### `profile(df)`
Performs rigorous statistical profiling on numeric columns.
- **Metrics**: Normality (Shapiro-Wilk $p$-value), Skewness, Kurtosis, Mean, and Std Dev.
- **Use Case**: Critical for academic research to justify statistical assumptions.

### `to_latex(df, caption="Summary", label="tab:summary")`
Converts any DataFrame into a publication-ready LaTeX table.
- **Returns**: A string containing the LaTeX code for a professional table.

### `lineage(df)`
Generates a unique SHA-256 fingerprint for the dataset.
- **Use Case**: Ensuring reproducibility in research papers by hashing the exact data state used.

---

## 🛠️ Feature Engineering

### `outliers(df, method='iqr', action='cap', columns=None)`
Detects and handles numerical outliers.
- **Methods**: `iqr` (Interquartile Range).
- **Actions**:
  - `cap`: Caps values at the lower/upper bounds.
  - `remove`: Drops rows containing outliers.

### `suggest(df, target)`
Recommends specific ML algorithms based on dataset scale and distribution.

### `suggest_features(df, target, threshold=0.1)`
Ranks features based on their correlation with the target variable.
- **Returns**: A list of recommended features that meet the correlation threshold.

### `balance(df, target, method='oversample')`
Balances class distributions using oversampling, undersampling, or synthetic methods.

### `validate(df, schema)`
Validates data against a predefined schema contract.

### `pipeline(steps)`
Creates a reusable `Pipeline` object for chaining transformations.

### `analyze_cleaning(df)`
Explains every cleaning action performed on the dataset by reading its history.

---

## 📥 Data IO

### `load(file_path, **kwargs)`
Smart loader that handles `.csv` and `.xlsx` files without needing to import pandas.

### `DataFrame(data)`
Wrapper for the pandas DataFrame constructor, allowing users to stay within the `dfx` ecosystem.

---

## 💻 CLI Reference

dfxpy comes with a built-in CLI for rapid analysis from the terminal.

### `dfxpy analyze <file>`
Runs a full cleaning and audit pipeline on a local file.

### `dfxpy prepare <file> --target <col>`
Cleans the file and saves a `prepared_data.csv` ready for ML models.

---

## 🧪 Internal Utilities
The following functions are also exposed for modular use:
- `clean_column_names(df)`
- `handle_missing(df)`
- `infer_types(df)`
