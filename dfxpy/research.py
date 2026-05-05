import pandas as pd
import numpy as np
from scipy import stats
import hashlib
from typing import Dict, Any

def profile_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform rigorous statistical profiling on numeric columns.
    Includes Normality (Shapiro-Wilk), Skewness, and Kurtosis.
    """
    numeric_df = df.select_dtypes(include=[np.number])
    results = []
    
    for col in numeric_df.columns:
        data = numeric_df[col].dropna()
        if len(data) < 3:
            continue
            
        # Shapiro-Wilk Test for Normality
        # Returns (stat, p-value)
        _, p_val = stats.shapiro(data.head(5000)) # Limited to 5000 for performance
        
        results.append({
            "column": col,
            "mean": data.mean(),
            "std": data.std(),
            "skew": data.skew(),
            "kurtosis": data.kurtosis(),
            "normality_p": p_val,
            "is_normal": p_val > 0.05
        })
        
    return pd.DataFrame(results)

def to_latex(df: pd.DataFrame, caption: str = "Data Summary", label: str = "tab:data") -> str:
    """
    Convert a DataFrame to a publication-ready LaTeX table.
    """
    latex_str = df.to_latex(
        index=False,
        caption=caption,
        label=label,
        position='htbp',
        column_format='l' + 'c' * (len(df.columns) - 1)
    )
    return latex_str

def get_lineage_hash(df: pd.DataFrame) -> str:
    """
    Generate a unique SHA-256 fingerprint for the dataset to ensure reproducibility.
    """
    # Convert to string and hash
    return hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def research_report(df: pd.DataFrame, verbose: bool = True):
    """
    Generate a full research-oriented report.
    """
    print("\n--- RESEARCH STATISTICAL PROFILE ---")
    profile = profile_stats(df)
    print(profile.to_string(index=False))
    
    print("\n--- DATA LINEAGE FINGERPRINT ---")
    print(f"SHA-256: {get_lineage_hash(df)}")
    
    return profile
