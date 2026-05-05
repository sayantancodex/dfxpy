import pandas as pd
from typing import Union, Tuple, Optional
from .cleaning import clean_column_names, drop_duplicates, handle_missing
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
    if verbose:
        print("\nStarting auto-cleaning workflow...")

    # 1. Clean column names
    df = clean_column_names(df)
    
    # 2. Drop duplicates
    df = drop_duplicates(df, verbose=verbose)
    
    # 3. Handle missing values
    df = handle_missing(df, verbose=verbose)
    
    # 4. One-hot encode categorical variables
    df = one_hot_encode(df, verbose=verbose)

    if verbose:
        print("Auto-cleaning completed.")

    if eda_report:
        report = run_eda(df, verbose=verbose)
        return df, report
    
    return df
