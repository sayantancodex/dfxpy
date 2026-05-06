import pandas as pd
import numpy as np
from typing import Literal, List, Optional

def handle_outliers(
    df: pd.DataFrame, 
    method: Literal["iqr"] = "iqr", 
    action: Literal["remove", "cap"] = "cap",
    columns: Optional[List[str]] = None,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Detect and handle outliers.
    """
    df = df.copy()
    num_cols = df.select_dtypes(include=['number']).columns
    if columns:
        num_cols = [c for c in num_cols if c in columns]
    
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outliers_mask.sum()
        
        if outlier_count > 0:
            if action == "remove":
                df = df[~outliers_mask]
                if verbose:
                    print(f"Removed {outlier_count} outliers from '{col}'.")
            elif action == "cap":
                df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
                df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
                if verbose:
                    print(f"Capped {outlier_count} outliers in '{col}'.")
    
    return df
