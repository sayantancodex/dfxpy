import pandas as pd
from typing import Dict, List, Any

def suggest_features(df: pd.DataFrame, target: str, threshold: float = 0.1) -> Dict[str, Any]:
    """
    Rank features by correlation with target and highlight strong/weak/redundant features.
    """
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in DataFrame.")

    # Only numeric features for correlation
    numeric_df = df.select_dtypes(include=['number'])
    if target not in numeric_df.columns:
        # If target is categorical, we might need different metrics, but keeping it simple as requested
        print(f"Target '{target}' is non-numeric. Skipping correlation-based ranking.")
        return {}

    correlations = numeric_df.corr()[target].abs().sort_values(ascending=False)
    correlations = correlations.drop(target) # Drop target itself

    strong_predictors = correlations[correlations > 0.5].index.tolist()
    weak_features = correlations[correlations < threshold].index.tolist()
    
    print("\n--- FEATURE SUGGESTIONS ---")
    print(f"Target: {target}")
    
    if strong_predictors:
        print("Strong Predictors (Correlation > 0.5):")
        for f in strong_predictors:
            print(f"- {f} ({correlations[f]:.2f})")
    
    if weak_features:
        print(f"Weak Features (Correlation < {threshold}):")
        for f in weak_features:
            print(f"- {f} ({correlations[f]:.2f})")

    # Redundancy check (already in audit, but here for completeness)
    report = {
        "correlations": correlations.to_dict(),
        "strong_predictors": strong_predictors,
        "weak_features": weak_features
    }
    print("---------------------------\n")
    
    return report
