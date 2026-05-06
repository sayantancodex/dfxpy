import pandas as pd
import numpy as np
from typing import Optional, List

def balance(df: pd.DataFrame, target: str, method: str = 'oversample', verbose: bool = True) -> pd.DataFrame:
    """
    Handle imbalanced datasets using oversampling, undersampling, or a basic SMOTE-like approach.
    """
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    df = df.copy()
    counts = df[target].value_counts()
    
    if len(counts) < 2:
        if verbose: print(f"Target '{target}' has only one class. Nothing to balance.")
        return df

    max_class = counts.idxmax()
    max_count = counts.max()
    
    if verbose:
        print(f"\n--- BALANCING DATASET (Method: {method}) ---")
        print(f"Target: {target}")
        print(f"Original counts:\n{counts.to_string()}")

    result_dfs = [df[df[target] == max_class]]
    
    for cls, count in counts.items():
        if cls == max_class:
            continue
        
        subset = df[df[target] == cls]
        
        if method == 'oversample':
            # Randomly duplicate minority samples
            resampled = subset.sample(n=max_count, replace=True, random_state=42)
            result_dfs.append(resampled)
            
        elif method == 'undersample':
            # This is tricky because we usually undersample the majority. 
            # But here we follow the "bring everything to max_count" or "bring max to min" logic.
            # Usually, undersample means reducing the majority.
            pass # I'll implement a proper undersampling of majority below
            
        elif method == 'smote':
            # Simplified SMOTE: interpolation between minority samples
            # Only works for numeric columns
            num_to_add = max_count - count
            if num_to_add <= 0:
                result_dfs.append(subset)
                continue
                
            numeric_cols = subset.select_dtypes(include=[np.number]).columns
            resampled_data = []
            
            # Simple implementation: pick two random points and interpolate
            data_arr = subset[numeric_cols].values
            if len(data_arr) > 1:
                for _ in range(num_to_add):
                    idx1, idx2 = np.random.choice(len(data_arr), 2, replace=False)
                    ratio = np.random.random()
                    new_point = data_arr[idx1] + ratio * (data_arr[idx2] - data_arr[idx1])
                    resampled_data.append(new_point)
            
            synthetic_df = pd.DataFrame(resampled_data, columns=numeric_cols)
            # Copy non-numeric columns from a random row of subset
            non_numeric_cols = [c for c in subset.columns if c not in numeric_cols and c != target]
            for col in non_numeric_cols:
                synthetic_df[col] = subset[col].iloc[0] # Just take first as placeholder
            
            synthetic_df[target] = cls
            result_dfs.append(subset)
            result_dfs.append(synthetic_df)

    if method == 'undersample':
        # Different logic: Reduce majority to min class count
        min_count = counts.min()
        final_dfs = []
        for cls, count in counts.items():
            subset = df[df[target] == cls]
            final_dfs.append(subset.sample(n=min_count, random_state=42))
        balanced_df = pd.concat(final_dfs).sample(frac=1).reset_index(drop=True)
    else:
        balanced_df = pd.concat(result_dfs).sample(frac=1).reset_index(drop=True)

    if verbose:
        new_counts = balanced_df[target].value_counts()
        print(f"New counts:\n{new_counts.to_string()}")
        print("------------------------------------------\n")

    return balanced_df
