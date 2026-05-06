import pandas as pd
from typing import Dict, Any, List

class ValidationError(Exception):
    """Custom exception for data validation errors."""
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

def validate(df: pd.DataFrame, schema: Dict[str, Dict[str, Any]], verbose: bool = True) -> bool:
    """
    Validate a DataFrame against a schema.
    Example schema:
    {
        'age': {'type': 'int', 'min': 0, 'max': 120},
        'status': {'type': 'string', 'in': ['active', 'inactive']}
    }
    """
    errors = []
    
    for col, constraints in schema.items():
        if col not in df.columns:
            errors.append(f"Column '{col}' missing from DataFrame.")
            continue
            
        series = df[col]
        
        # 1. Type check
        expected_type = constraints.get('type')
        if expected_type:
            if expected_type in ['int', 'float', 'number']:
                if not pd.api.types.is_numeric_dtype(series):
                    errors.append(f"Column '{col}' should be numeric, found {series.dtype}.")
            elif expected_type == 'string':
                if not pd.api.types.is_string_dtype(series) and series.dtype != 'object':
                    errors.append(f"Column '{col}' should be string/object, found {series.dtype}.")
        
        # 2. Min/Max
        if 'min' in constraints:
            if series.min() < constraints['min']:
                errors.append(f"Column '{col}' has values below minimum {constraints['min']}.")
        if 'max' in constraints:
            if series.max() > constraints['max']:
                errors.append(f"Column '{col}' has values above maximum {constraints['max']}.")
                
        # 3. Allowed values (In)
        if 'in' in constraints:
            invalid_values = series[~series.isin(constraints['in'])].dropna().unique()
            if len(invalid_values) > 0:
                errors.append(f"Column '{col}' contains invalid values: {invalid_values[:5]}")

    if errors:
        if verbose:
            print("\n--- VALIDATION FAILED ---")
            for e in errors:
                print(f"- {e}")
            print("------------------------\n")
        raise ValidationError("Dataset failed validation schema.", details=errors)
        
    if verbose:
        print(f"\n--- VALIDATION PASSED ({len(schema)} columns checked) ---\n")
        
    return True
