import pandas as pd
from typing import Dict, Any, List, Optional

def compare(df1: pd.DataFrame, df2: pd.DataFrame, verbose: bool = True) -> Dict[str, Any]:
    """
    Compare two DataFrames and return a detailed diff report.
    """
    report = {
        "shape_change": (df1.shape, df2.shape),
        "columns_added": list(set(df2.columns) - set(df1.columns)),
        "columns_removed": list(set(df1.columns) - set(df2.columns)),
        "common_columns": list(set(df1.columns) & set(df2.columns)),
        "value_changes": 0
    }

    if verbose:
        print("\n--- DATASET COMPARISON ---")
        print(f"Shape: {df1.shape} -> {df2.shape}")
        
        if report["columns_added"]:
            print(f"Columns Added: {report['columns_added']}")
        if report["columns_removed"]:
            print(f"Columns Removed: {report['columns_removed']}")

    # Cell-level comparison on common columns and common index
    common_cols = report["common_columns"]
    common_index = df1.index.intersection(df2.index)
    
    if not common_cols or common_index.empty:
        if verbose: print("No common columns or index to compare values.")
        return report

    # Compare values
    df1_common = df1.loc[common_index, common_cols]
    df2_common = df2.loc[common_index, common_cols]
    
    # We use .ne(df2_common) and handle NaNs (NaN != NaN is True, so we need to be careful)
    # Filling NaNs with a marker to compare them properly if needed, 
    # but standard pandas comparison might be enough for a summary.
    diff_mask = df1_common.ne(df2_common) & ~(df1_common.isna() & df2_common.isna())
    report["value_changes"] = diff_mask.sum().sum()
    
    if verbose:
        if report["value_changes"] > 0:
            print(f"Total Value Changes (in common cells): {report['value_changes']}")
            # Show top 5 columns with most changes
            changes_per_col = diff_mask.sum().sort_values(ascending=False)
            print("Changes per column (top 5):")
            for col, count in changes_per_col.head(5).items():
                if count > 0:
                    print(f"- {col}: {count} cells changed")
        else:
            print("No value changes detected in common cells.")
        print("--------------------------\n")

    return report
