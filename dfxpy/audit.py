import pandas as pd
import numpy as np
from typing import Dict, Any, List

def audit(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze dataset and generate warnings + insights.
    """
    warnings = []
    insights = []
    report = {}

    row_count = len(df)
    
    # 1. ID-like columns
    id_cols = []
    for col in df.columns:
        if df[col].nunique() / row_count > 0.95:
            id_cols.append(col)
            warnings.append(f"Column '{col}' appears to be an identifier (uniqueness > 95%).")
    report["id_like_columns"] = id_cols

    # 2. High missing values (>40%)
    high_missing = []
    missing_pct = df.isnull().mean()
    for col, pct in missing_pct.items():
        if pct > 0.4:
            high_missing.append(col)
            warnings.append(f"Column '{col}' has high missing values ({pct:.1%}). Consider dropping it.")
    report["high_missing_columns"] = high_missing

    # 3. High cardinality categoricals
    high_cardinality = []
    cat_cols = df.select_dtypes(exclude=['number']).columns
    for col in cat_cols:
        nunique = df[col].nunique()
        if nunique > 50 and nunique / row_count > 0.1:
            high_cardinality.append(col)
            warnings.append(f"Column '{col}' has high cardinality ({nunique} unique values).")
    report["high_cardinality_columns"] = high_cardinality

    # 4. Constant / low variance columns
    low_variance = []
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        if df[col].nunique() <= 1:
            low_variance.append(col)
            warnings.append(f"Column '{col}' is constant (no variance).")
    report["low_variance_columns"] = low_variance

    # 5. Strong correlations (>0.9)
    strong_corr = []
    if not num_cols.empty and len(num_cols) > 1:
        corr_matrix = df[num_cols].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        to_drop = [column for column in upper.columns if any(upper[column] > 0.9)]
        for col in to_drop:
            related = upper.index[upper[col] > 0.9].tolist()
            strong_corr.append((col, related))
            warnings.append(f"Column '{col}' is highly correlated with {related} (>0.9). Redundancy detected.")
    report["highly_correlated_pairs"] = strong_corr

    # 6. Skewness
    skewed_cols = []
    for col in num_cols:
        skew_val = df[col].skew()
        if abs(skew_val) > 2:
            skewed_cols.append(col)
            insights.append(f"Column '{col}' is highly skewed (skewness: {skew_val:.2f}).")
    report["skewed_columns"] = skewed_cols

    # Output to console
    print("\n--- DATA AUDIT REPORT ---")
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("No major issues detected.")

    if insights:
        print("\nINSIGHTS:")
        for i in insights:
            print(f"- {i}")
    print("------------------------\n")

    report["warnings"] = warnings
    report["insights"] = insights
    return report
