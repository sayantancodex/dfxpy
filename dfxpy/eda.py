import pandas as pd
from typing import Dict, Any

def eda(df: pd.DataFrame, verbose: bool = True) -> Dict[str, Any]:
    """
    Generate structured EDA dictionary and print readable output.
    """
    report = {
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.apply(lambda x: str(x)).to_dict(),
        "unique_counts": df.nunique().to_dict(),
        "correlation_matrix": df.select_dtypes(include=['number']).corr().to_dict() if not df.select_dtypes(include=['number']).empty else {}
    }

    if verbose:
        print("\n--- EDA REPORT ---")
        print(f"Shape: {report['shape']}")
        print("\nData Types:")
        for col, dtype in report['data_types'].items():
            print(f"- {col}: {dtype}")
        
        print("\nMissing Values:")
        for col, count in report['missing_values'].items():
            if count > 0:
                print(f"- {col}: {count}")
        if not any(report['missing_values'].values()):
            print("No missing values detected.")

        print("\nUnique Counts:")
        for col, count in report['unique_counts'].items():
            print(f"- {col}: {count}")
        print("------------------\n")

    return report
