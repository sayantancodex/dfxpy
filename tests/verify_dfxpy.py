import pandas as pd
import numpy as np
import dfxpy as dfx
import os

def create_dummy_data():
    data = {
        'User ID': range(1, 101),
        'Age': [25, 30, np.nan, 35, 40, 200] + [30]*94, # Contains NaN and Outlier (200)
        'Salary': [50000, 60000, 70000, np.nan, 80000] + [60000]*95,
        'City': ['New York', 'London', 'Paris', 'Paris', np.nan] + ['London']*95,
        'Target': [0, 1, 0, 1, 0] + [1]*95
    }
    df = pd.DataFrame(data)
    df.to_csv('dummy_data.csv', index=False)
    return df

def test_workflow():
    print("--- Testing dfxpy workflow ---")
    df = create_dummy_data()
    
    # 1. Test auto()
    print("\nTesting auto()...")
    df_clean = dfx.auto(df, verbose=True)
    print(f"Cleaned columns: {df_clean.columns.tolist()}")
    
    # 2. Test eda()
    print("\nTesting eda()...")
    dfx.eda(df_clean)
    
    # 3. Test audit()
    print("\nTesting audit()...")
    dfx.audit(df_clean)
    
    # 4. Test outliers()
    print("\nTesting outliers()...")
    df_no_outliers = dfx.outliers(df_clean, action="cap")
    
    # 5. Test prepare()
    print("\nTesting prepare()...")
    X, y = dfx.prepare(df, target="Target")
    print(f"X shape: {X.shape}, y shape: {y.shape}")
    
    # 6. Test suggest_features()
    print("\nTesting suggest_features()...")
    dfx.suggest_features(df_clean, target="target")

if __name__ == "__main__":
    test_workflow()
    # Cleanup
    if os.path.exists('dummy_data.csv'):
        os.remove('dummy_data.csv')
