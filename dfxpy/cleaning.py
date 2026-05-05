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

def infer_types(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Try to infer better data types for object columns.
    """
    df = df.copy()
    obj_cols = df.select_dtypes(include=['object', 'string']).columns
    
    for col in obj_cols:
        # Try numeric
        try:
            temp_col = pd.to_numeric(df[col], errors='raise')
            df[col] = temp_col
            if verbose:
                print(f"Converted '{col}' to numeric.")
            continue
        except (ValueError, TypeError):
            pass
        
        # Try datetime (only if it looks like a date)
        # Simple heuristic: at least 5 chars and has '-' or '/'
        if df[col].dtype == 'object' and df[col].astype(str).str.len().mean() > 5:
            try:
                # Use a small sample to check for date-likeness
                sample = df[col].dropna().head(10).astype(str)
                if sample.str.contains(r'[-/]').any():
                    df[col] = pd.to_datetime(df[col], errors='raise')
                    if verbose:
                        print(f"Converted '{col}' to datetime.")
            except (ValueError, TypeError):
                pass
    
    return df

def handle_missing(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Handle missing values:
    - Numeric -> median
    - Categorical -> mode
    - Date -> most frequent
    - Entirely null -> drop
    """
    df = df.copy()
    
    # Drop columns that are entirely null
    all_null_cols = df.columns[df.isnull().all()].tolist()
    if all_null_cols:
        df = df.drop(columns=all_null_cols)
        if verbose:
            print(f"Dropped entirely empty columns: {all_null_cols}")

    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(include=['object', 'category', 'string', 'bool']).columns
    date_cols = df.select_dtypes(include=['datetime']).columns

    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            if verbose:
                print(f"Imputed '{col}' (numeric) with median: {median_val}")

    for col in categorical_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
                if verbose:
                    print(f"Imputed '{col}' (categorical) with mode: {mode_val[0]}")

    for col in date_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
                if verbose:
                    print(f"Imputed '{col}' (date) with most frequent: {mode_val[0]}")

    return df
