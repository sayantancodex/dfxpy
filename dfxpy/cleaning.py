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
    Try to infer better data types for object/string columns.
    """
    df = df.copy()
    # Check for both object and string dtypes
    obj_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == 'object']
    
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
        
        # Try datetime
        try:
            # Check if it looks like a date (contains '-' or '/')
            sample = df[col].dropna().head(10).astype(str)
            if not sample.empty and sample.str.contains(r'[-/:]').any():
                df[col] = pd.to_datetime(df[col], errors='raise')
                if verbose:
                    print(f"Converted '{col}' to datetime.")
        except (ValueError, TypeError, pd.errors.ParserError):
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
    categorical_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype in ['object', 'category', 'bool']]
    date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns

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
