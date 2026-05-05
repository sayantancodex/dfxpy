import pandas as pd
from typing import List, Optional

def one_hot_encode(df: pd.DataFrame, columns: Optional[List[str]] = None, verbose: bool = True) -> pd.DataFrame:
    """
    One-hot encode categorical variables.
    Also extracts features from date columns if present.
    """
    df = df.copy()
    
    # Handle Date Columns
    date_cols = df.select_dtypes(include=['datetime']).columns
    for col in date_cols:
        if verbose:
            print(f"Extracting features from date column: '{col}'")
        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_day"] = df[col].dt.day
        df[f"{col}_hour"] = df[col].dt.hour
        df = df.drop(columns=[col])

    # Handle Categorical Columns
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category', 'string', 'bool']).columns.tolist()
    
    if not columns:
        return df

    if verbose:
        print(f"One-hot encoding columns: {columns}")
    
    return pd.get_dummies(df, columns=columns, drop_first=True)
