import pandas as pd
import dfxpy as dfx
import os

# 1. Create a messy dataset
data = {
    'User ID': [1, 2, 2, 3, 4],
    'Price': ['$100', '£50', '£50', '$200', '$150'],
    'Discount%': ['10%', '5%', '5%', '20%', '15%'],
    'Active': ['Yes', 'No', 'No', 'True', 'False'],
    'Date': ['2023-01-01', '10-Jan-2023', '10-Jan-2023', '2023-02-01', '2023-03-01'],
    'Score': [85, 90, 90, None, 75],
    'Target': [1, 0, 0, 1, 1]
}
df = pd.DataFrame(data)

print("Original Data:")
print(df)

# 2. Test dfx.fix()
print("\n--- Testing dfx.fix() ---")
df_fixed = dfx.fix(df)
print(df_fixed.dtypes)
print(df_fixed)

# 3. Test dfx.analyze_cleaning()
print("\n--- Testing dfx.analyze_cleaning() ---")
dfx.analyze_cleaning(df_fixed)

# 4. Test dfx.report()
print("\n--- Testing dfx.report() ---")
dfx.report(df_fixed, output="test_report.html")
print(f"Report exists: {os.path.exists('test_report.html')}")

# 5. Test dfx.compare()
print("\n--- Testing dfx.compare() ---")
df2 = df_fixed.copy()
df2.loc[0, 'score'] = 99
df2['new_col'] = 'test'
dfx.compare(df_fixed, df2)

# 6. Test dfx.balance()
print("\n--- Testing dfx.balance() ---")
df_bal = dfx.balance(df_fixed, target='target', method='oversample')

# 7. Test dfx.validate()
print("\n--- Testing dfx.validate() ---")
schema = {
    'score': {'type': 'number', 'min': 0, 'max': 100},
    'active': {'type': 'boolean'}
}
try:
    dfx.validate(df_fixed, schema)
except Exception as e:
    print(f"Validation Note: {e}")

# 8. Test dfx.pipeline()
print("\n--- Testing dfx.pipeline() ---")
pipe = dfx.pipeline([
    dfx.clean_column_names,
    dfx.handle_missing
])
df_pipe = pipe.run(df)

# 9. Test dfx.suggest()
print("\n--- Testing dfx.suggest() ---")
dfx.suggest(df_fixed, target='target')

# 10. Test dfx.leakage()
print("\n--- Testing dfx.leakage() ---")
dfx.leakage(df_fixed, target='target')

print("\nVerification complete.")
