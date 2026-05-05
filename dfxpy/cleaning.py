import pandas as pd
import re
from typing import List, Optional

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean column names to snake_case.
    """
    df = df.copy()
    def to_snake(name: str) -> str:
        name = str(name)
        # Replace non-alphanumeric with underscore
        name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        # CamelCase to snake_case
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        # Collapse multiple underscores
        name = re.sub(r'_+', '_', name)
        return name.lower().strip('_')
    
    df.columns = [to_snake(c) for c in df.columns]
    return df

def drop_duplicates(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Drop duplicate rows.
    """
    initial_count = len(df)
    df = df.drop_duplicates()
    final_count = len(df)
    if verbose and initial_count != final_count:
        print(f"Dropped {initial_count - final_count} duplicate rows.")
    return df

def handle_missing(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Handle missing values:
    - Numeric -> median
    - Categorical -> mode
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(exclude=['number']).columns

    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            if verbose:
                print(f"Imputed missing values in '{col}' with median: {median_val}")

    for col in categorical_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
                if verbose:
                    print(f"Imputed missing values in '{col}' with mode: {mode_val[0]}")
            else:
                # If all are NaN, just drop or leave? For auto, we might leave it or drop.
                # Here we leave it to avoid data loss, audit will catch it.
                pass

    return df
