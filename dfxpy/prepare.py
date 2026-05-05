import pandas as pd
from typing import Tuple, Optional
from .cleaning import clean_column_names, handle_missing, infer_types
from .encoding import one_hot_encode

def prepare(
    df: pd.DataFrame, 
    target: str, 
    scale: bool = False,
    verbose: bool = True
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    One-line ML-ready dataset preparation.
    Handles numeric and categorical targets.
    """
    df = df.copy()
    
    # 1. Clean names
    df = clean_column_names(df)
    
    # Resolve target name
    if target not in df.columns:
        from .cleaning import clean_column_names as ccn
        temp_df = pd.DataFrame(columns=[target])
        target_cleaned = ccn(temp_df).columns[0]
        if target_cleaned in df.columns:
            target = target_cleaned
        else:
            raise ValueError(f"Target column '{target}' not found.")

    # 2. Basic cleanup
    df = df.drop_duplicates()
    df = infer_types(df, verbose=verbose)
    df = handle_missing(df, verbose=verbose)
    
    # 3. Handle Target Encoding (if non-numeric)
    y = df[target]
    if not pd.api.types.is_numeric_dtype(y):
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = pd.Series(le.fit_transform(y.astype(str)), name=target, index=df.index)
        if verbose:
            print(f"Target '{target}' is non-numeric. Applied LabelEncoder. Classes: {le.classes_}")
    
    # 4. Feature Encoding
    X = df.drop(columns=[target])
    X = one_hot_encode(X, verbose=verbose)
    
    # 5. Scaling (Optional)
    if scale:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        numeric_cols = X.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
            if verbose:
                print(f"Applied StandardScaler to features.")

    if verbose:
        print(f"\nPreparation complete. X shape: {X.shape}, y shape: {y.shape}")
        
    return X, y
