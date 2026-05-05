import pandas as pd
from typing import List, Optional

def one_hot_encode(df: pd.DataFrame, columns: Optional[List[str]] = None, verbose: bool = True) -> pd.DataFrame:
    """
    One-hot encode categorical variables.
    """
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
    
    if not columns:
        return df

    if verbose:
        print(f"One-hot encoding columns: {columns}")
    
    return pd.get_dummies(df, columns=columns, drop_first=True)
