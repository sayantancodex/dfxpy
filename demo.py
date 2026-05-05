import dfxpy as dfx
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run_demo():
    print("=== DFXPY COMPREHENSIVE DEMO ===\n")

    # 1. Create a messy dataset
    print("1. Generating messy dataset...")
    data = {
        'Order_Date': ['2023-01-01', '2023-01-02', '2023-01-02', 'invalid_date', None, '2023-01-05']*2,
        'Price_Paid': ['10.5', '20.0', '20.0', '30.5', '40.0', None]*2,
        'Customer_Segment': ['A', 'B', 'B', 'C', 'A', 'B']*2,
        'Target_Buy': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes']*2,
        'High_Correlation_Feature': [1, 2, 2, 3, 4, 5]*2 
    }
    df_raw = dfx.DataFrame(data)
    print(f"Raw Shape: {df_raw.shape}")

    print("\n" + "-"*30 + "\n")

    # 2. Run Audit
    print("2. Running dfx.audit()...")
    dfx.audit(df_raw)

    print("\n" + "-"*30 + "\n")

    # 3. Run EDA
    print("3. Running dfx.eda()...")
    dfx.eda(df_raw)

    print("\n" + "-"*30 + "\n")

    # 4. Prepare for Machine Learning (BEST WAY)
    print("4. Running dfx.prepare()...")
    # Note: We run prepare() on the raw data. It handles names, types, and encoding automatically.
    X, y = dfx.prepare(df_raw, target='Target_Buy', verbose=True)
    
    print(f"\nFinal ML Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")
    print("\nFirst few rows of X:\n", X.head())
    print("\nFirst few rows of y:\n", y[:5])

    print("\n=== DEMO COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_demo()
