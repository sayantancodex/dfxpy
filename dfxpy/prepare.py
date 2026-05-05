import pandas as pd
from typing import Tuple, Optional
from .cleaning import clean_column_names, handle_missing
from .encoding import one_hot_encode

def prepare(
    df: pd.DataFrame, 
    target: str, 
    scale: bool = False,
    verbose: bool = True
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    One-line ML-ready dataset preparation.
    """
    df = df.copy()
    
    # 1. Clean names
    df = clean_column_names(df)
    
    # Ensure target is cleaned too if it was original
    # (Note: assume target passed matches cleaned version or we find it)
    if target not in df.columns:
        # Try to find cleaned version of target
        from .cleaning import clean_column_names as ccn
        temp_df = pd.DataFrame(columns=[target])
        target_cleaned = ccn(temp_df).columns[0]
        if target_cleaned in df.columns:
            target = target_cleaned
        else:
            raise ValueError(f"Target column '{target}' not found in cleaned DataFrame.")

    # 2. Drop duplicates
    df = df.drop_duplicates()
    
    # 3. Handle missing
    df = handle_missing(df, verbose=verbose)
    
    # 4. Encode
    df = one_hot_encode(df, verbose=verbose)
    
    # 5. Split X and y
    y = df[target]
    X = df.drop(columns=[target])
    
    # 6. Scaling (Optional)
    if scale:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        numeric_cols = X.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
            if verbose:
                print(f"Applied StandardScaler to: {numeric_cols.tolist()}")

    if verbose:
        print(f"\nPreparation complete. X shape: {X.shape}, y shape: {y.shape}")
        
    return X, y
