import pandas as pd
from typing import Union, Tuple, Optional
from .cleaning import clean_column_names, drop_duplicates, handle_missing, infer_types
from .encoding import one_hot_encode
from .eda import eda as run_eda

def auto(
    df: pd.DataFrame, 
    verbose: bool = True, 
    eda_report: bool = False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, dict]]:
    """
    Automatically clean and prepare a DataFrame.
    """
    if df.empty:
        if verbose: print("Warning: Empty DataFrame provided.")
        return (df, {}) if eda_report else df

    if verbose:
        print("\nStarting auto-cleaning workflow...")

    # 1. Clean column names
    df = clean_column_names(df)
    
    # 2. Drop duplicates
    df = drop_duplicates(df, verbose=verbose)
    
    # 3. Infer better types (e.g. object -> numeric/date)
    df = infer_types(df, verbose=verbose)
    
    # 4. Handle missing values
    df = handle_missing(df, verbose=verbose)
    
    # 5. One-hot encode categorical variables
    df = one_hot_encode(df, verbose=verbose)

    if verbose:
        print("Auto-cleaning completed.")

    if eda_report:
        report = run_eda(df, verbose=verbose)
        return df, report
    
    return df
