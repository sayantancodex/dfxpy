import pytest
import pandas as pd
import numpy as np
import dfxpy as dfx

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'User ID': range(10),
        'Age': [25, 30, np.nan, 35, 40, 25, 30, 35, 40, 100], # 100 is outlier
        'City': ['NY', 'LDN', 'PRS', 'PRS', np.nan, 'NY', 'LDN', 'PRS', 'PRS', 'NY'],
        'Salary': [50000, 60000, 70000, 80000, 90000, 50000, 60000, 70000, 80000, 90000],
        'Target': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    })

def test_auto_workflow(sample_df):
    df_clean = dfx.auto(sample_df, verbose=False)
    
    # Check column names
    assert "user_id" in df_clean.columns
    assert "city_PRS" in df_clean.columns # One-hot encoded
    
    # Check missing values handled
    assert df_clean.isnull().sum().sum() == 0
    
    # Check duplicates (none in sample, but logic tested)
    assert len(df_clean) == 10

def test_cleaning_logic(sample_df):
    df = dfx.clean_column_names(sample_df)
    assert "user_id" in df.columns
    assert "city" in df.columns
    
    df_imputed = dfx.handle_missing(df, verbose=False)
    assert df_imputed["age"].isnull().sum() == 0
    assert df_imputed["city"].isnull().sum() == 0

def test_audit_report(sample_df):
    df_clean = dfx.auto(sample_df, verbose=False)
    report = dfx.audit(df_clean)
    
    assert "user_id" in report["id_like_columns"]
    assert len(report["warnings"]) > 0

def test_prepare_ml(sample_df):
    X, y = dfx.prepare(sample_df, target="Target", verbose=False)
    
    assert X.shape == (10, 5) # user_id, age, salary, city_LDN, city_PRS
    assert y.shape == (10,)
    assert "target" not in X.columns

def test_outliers(sample_df):
    df = dfx.clean_column_names(sample_df)
    df_capped = dfx.outliers(df, action="cap", verbose=False)
    
    # IQR for Age [25, 30, 35, 40, 25, 30, 35, 40, 100] (ignoring NaN for now, but handle_missing would run first)
    # With 100, the upper bound is much lower. 
    assert df_capped["age"].max() < 100

def test_feature_suggestions(sample_df):
    df_clean = dfx.auto(sample_df, verbose=False)
    suggestions = dfx.suggest_features(df_clean, target="target")
    
    assert "correlations" in suggestions
