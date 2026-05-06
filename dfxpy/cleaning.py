import pandas as pd
import re
from typing import List, Optional
from .history import log_change

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
    log_change(df, f"Cleaned column names: {list(df.columns)}")
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
        log_change(df, f"Dropped {initial_count - final_count} duplicate rows.")
    return df

def infer_types(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Try to infer better data types for object/string columns.
    Handles currency ($), percentages (%), and booleans.
    """
    df = df.copy()
    obj_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == 'object']
    
    for col in obj_cols:
        series = df[col].dropna().astype(str).str.strip()
        if series.empty:
            continue

        # 1. Try Booleans
        bool_map = {'true': True, 'false': False, 'yes': True, 'no': False, 't': True, 'f': False, '1': True, '0': False}
        if series.str.lower().isin(bool_map.keys()).all():
            df[col] = series.str.lower().map(bool_map)
            if verbose: print(f"Converted '{col}' to boolean.")
            log_change(df, f"Converted '{col}' to boolean.")
            continue

        # 2. Try Currency ($100, £50)
        if series.str.contains(r'^[£\$€¥]').any() or series.str.contains(r'[£\$€¥]$').any():
            clean_series = series.str.replace(r'[£\$€¥,]', '', regex=True)
            try:
                df[col] = pd.to_numeric(clean_series)
                if verbose: print(f"Converted '{col}' from currency to numeric.")
                log_change(df, f"Converted '{col}' from currency to numeric.")
                continue
            except: pass

        # 3. Try Percentage (10%)
        if series.str.contains(r'%$').any():
            clean_series = series.str.replace('%', '', regex=False)
            try:
                df[col] = pd.to_numeric(clean_series) / 100.0
                if verbose: print(f"Converted '{col}' from percentage to numeric.")
                log_change(df, f"Converted '{col}' from percentage to numeric.")
                continue
            except: pass

        # 4. Try Numeric
        try:
            df[col] = pd.to_numeric(df[col], errors='raise')
            if verbose: print(f"Converted '{col}' to numeric.")
            log_change(df, f"Converted '{col}' to numeric.")
            continue
        except: pass
        
        # 5. Try Datetime
        try:
            # More aggressive date detection
            if series.str.contains(r'[-/:]').any() or series.str.contains(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', case=False, regex=True).any():
                df[col] = pd.to_datetime(df[col], errors='raise')
                if verbose: print(f"Converted '{col}' to datetime.")
                log_change(df, f"Converted '{col}' to datetime.")
        except: pass
    
    return df

def fix(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    One-stop shop for cleaning and fixing a dataset.
    Intelligently detects types, cleans names, and handles duplicates.
    """
    if verbose: print("\n--- FIXING DATASET ---")
    df = clean_column_names(df)
    df = drop_duplicates(df, verbose=verbose)
    df = infer_types(df, verbose=verbose)
    df = handle_missing(df, verbose=verbose)
    if verbose: print("----------------------\n")
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
        log_change(df, f"Dropped empty columns: {all_null_cols}")

    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c]) or df[c].dtype in ['object', 'category', 'bool']]
    date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns

    for col in numeric_cols:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            if verbose:
                print(f"Imputed '{col}' (numeric) with median: {median_val}")
            log_change(df, f"Imputed '{col}' (numeric) with median: {median_val}")

    for col in categorical_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
                if verbose:
                    print(f"Imputed '{col}' (categorical) with mode: {mode_val[0]}")
                log_change(df, f"Imputed '{col}' (categorical) with mode: {mode_val[0]}")

    for col in date_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
                if verbose:
                    print(f"Imputed '{col}' (date) with most frequent: {mode_val[0]}")
                log_change(df, f"Imputed '{col}' (date) with most frequent: {mode_val[0]}")

    return df
