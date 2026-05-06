import pandas as pd
from typing import List, Dict, Any

def suggest(df: pd.DataFrame, target: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Suggest ML models based on dataset characteristics.
    """
    if target not in df.columns:
        raise ValueError(f"Target '{target}' not found.")

    row_count = len(df)
    feature_count = df.shape[1] - 1
    target_type = "classification" if df[target].nunique() < 20 else "regression"
    is_imbalanced = False
    
    if target_type == "classification":
        counts = df[target].value_counts(normalize=True)
        if counts.min() < 0.2:
            is_imbalanced = True

    recommendations = []
    
    if target_type == "classification":
        if row_count < 1000:
            recommendations = [
                {"model": "Logistic Regression", "reason": "Small dataset, needs simple model to avoid overfitting."},
                {"model": "Random Forest", "reason": "Robust for small datasets with non-linear relationships."}
            ]
        elif row_count < 50000:
            recommendations = [
                {"model": "XGBoost", "reason": "Highly efficient for medium-sized tabular data."},
                {"model": "LightGBM", "reason": "Fast and handles large number of features well."}
            ]
        else:
            recommendations = [
                {"model": "LightGBM", "reason": "Scales exceptionally well to large datasets."},
                {"model": "CatBoost", "reason": "Great for large datasets with many categorical features."}
            ]
            
        if is_imbalanced:
            recommendations.append({"note": "Dataset is imbalanced. Consider using SMOTE or adjusting class weights."})
    else:
        # Regression
        recommendations = [
            {"model": "Ridge Regression", "reason": "Good baseline for linear relationships."},
            {"model": "Random Forest Regressor", "reason": "Handles non-linearities and interactions well."}
        ]

    if verbose:
        print(f"\n--- ML MODEL RECOMMENDATIONS ---")
        print(f"Dataset: {row_count:,} rows, {feature_count} features")
        print(f"Problem: {target_type.capitalize()}")
        if is_imbalanced: print("Warning: Imbalanced classes detected.")
        print("\nRecommended Models:")
        for r in recommendations:
            if "model" in r:
                print(f"- {r['model']}: {r['reason']}")
            else:
                print(f"  Note: {r['note']}")
        print("--------------------------------\n")

    return {
        "problem_type": target_type,
        "is_imbalanced": is_imbalanced,
        "recommendations": recommendations
    }
