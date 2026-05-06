import pandas as pd
from typing import List, Dict, Any

def log_change(df: pd.DataFrame, action: str):
    """
    Log a cleaning action in the DataFrame's metadata using df.attrs.
    """
    if 'dfx_history' not in df.attrs:
        df.attrs['dfx_history'] = []
    df.attrs['dfx_history'].append(action)

def analyze_cleaning(df: pd.DataFrame, verbose: bool = True) -> List[str]:
    """
    Return a human-readable list of cleaning actions performed on the dataset.
    """
    history = df.attrs.get('dfx_history', [])
    
    if verbose:
        print("\n--- CLEANING ANALYSIS ---")
        if not history:
            print("No recorded cleaning actions found.")
        else:
            for i, action in enumerate(history):
                print(f"{i+1}. {action}")
        print("-------------------------\n")
        
    return history
