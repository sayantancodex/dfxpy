import pandas as pd
from typing import Dict, Any, Optional
from .reporting import generate_html_report

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

def report(df: pd.DataFrame, output: str = "report.html", verbose: bool = True) -> str:
    """
    Generate a beautiful HTML EDA report.
    """
    if verbose:
        print(f"Generating HTML report: {output}...")
    
    # Get basic EDA data
    report_data = eda(df, verbose=False)
    
    # Add version info (mocked or from package)
    report_data['version'] = "0.2.6" 
    
    # Generate the file
    path = generate_html_report(df, report_data, output)
    
    if verbose:
        print(f"Report saved to {path}")
    
    return path
