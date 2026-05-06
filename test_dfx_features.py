import pandas as pd
import dfxpy as dfx
import numpy as np
import os

# 1. Create a "Real-World" Messy Dataset
print("--- Creating messy dataset ---")
data = {
    'Customer Name': ['Alice', 'Bob', 'Bob', 'Charlie', 'David'],
    'Revenue': ['$1,200', '£850', '£850', '$2,400', '$3,100'],
    'Growth Rate': ['12%', '8%', '8%', '15%', '22%'],
    'Is_Active': ['Yes', 'No', 'No', 'True', 'False'],
    'Join Date': ['2023-01-01', '10-Jan-2023', '10-Jan-2023', '2023-02-01', '2023-03-01'],
    'Satisfaction': [8.5, 9.0, 9.0, None, 7.5],
    'Churn': [1, 0, 0, 1, 1]
}
df = pd.DataFrame(data)

# 2. Test dfx.fix() - The Magic Fixer
print("\n--- Testing dfx.fix() ---")
df_fixed = dfx.fix(df)
print("\nCleaned DataFrame Types:")
print(df_fixed.dtypes)
print("\nCleaned Data Preview:")
print(df_fixed.head())

# 3. Test dfx.analyze_cleaning() - The Explainer
print("\n--- Testing dfx.analyze_cleaning() ---")
dfx.analyze_cleaning(df_fixed)

# 4. Test dfx.report() - One-Click HTML EDA
print("\n--- Testing dfx.report() ---")
report_path = "dfx_premium_report.html"
dfx.report(df_fixed, output=report_path)
print(f"--- Report generated: {os.path.abspath(report_path)} ---")

# 5. Test dfx.compare() - Version Tracking
print("\n--- Testing dfx.compare() ---")
df_v2 = df_fixed.copy()
df_v2.loc[0, 'satisfaction'] = 9.9
df_v2['priority'] = 'High'
dfx.compare(df_fixed, df_v2)

# 6. Test dfx.balance() - Handling Imbalance
print("\n--- Testing dfx.balance() ---")
df_balanced = dfx.balance(df_fixed, target='churn', method='oversample')

# 7. Test dfx.validate() - Data Contracts
print("\n--- Testing dfx.validate() ---")
schema = {
    'satisfaction': {'type': 'number', 'min': 0, 'max': 10},
    'is_active': {'type': 'boolean'}
}
try:
    dfx.validate(df_fixed, schema)
    print("--- Validation Passed! ---")
except Exception as e:
    print(f"--- Validation Failed: {e} ---")

# 8. Test dfx.pipeline() - Workflow Automation
print("\n--- Testing dfx.pipeline() ---")
my_pipe = dfx.pipeline([
    dfx.clean_column_names,
    dfx.handle_missing
])
df_processed = my_pipe.run(df)

# 9. Test dfx.suggest() - ML Advisor
print("\n--- Testing dfx.suggest() ---")
dfx.suggest(df_fixed, target='churn')

# 10. Test dfx.leakage() - Security Check
print("\n--- Testing dfx.leakage() ---")
dfx.leakage(df_fixed, target='churn')

print("\n--- All tests completed successfully! ---")
