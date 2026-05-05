import pandas as pd
import os
from typing import Optional

def load(filepath: str, **kwargs) -> pd.DataFrame:
    """
    Load data from a file (CSV or Excel) into a DataFrame.
    Automatically detects format based on extension.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.csv':
        return pd.read_csv(filepath, **kwargs)
    elif ext in ['.xls', '.xlsx', '.xlsm']:
        return pd.read_excel(filepath, **kwargs)
    else:
        # Fallback to CSV or try to read it anyway
        try:
            return pd.read_csv(filepath, **kwargs)
        except Exception:
            raise ValueError(f"Unsupported file format: {ext}. Use .csv or .xlsx")

def read_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """Wrapper for pd.read_csv"""
    return pd.read_csv(filepath, **kwargs)

def read_excel(filepath: str, **kwargs) -> pd.DataFrame:
    """Wrapper for pd.read_excel"""
    return pd.read_excel(filepath, **kwargs)

def DataFrame(*args, **kwargs) -> pd.DataFrame:
    """Wrapper for pd.DataFrame"""
    return pd.DataFrame(*args, **kwargs)
