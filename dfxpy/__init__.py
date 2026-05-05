from .core import auto
from .eda import eda
from .audit import audit
from .prepare import prepare
from .outliers import handle_outliers as outliers
from .feature_selection import suggest_features
from .cleaning import clean_column_names, handle_missing

__version__ = "0.1.0"
__all__ = [
    "auto",
    "eda",
    "audit",
    "prepare",
    "outliers",
    "suggest_features",
    "clean_column_names",
    "handle_missing"
]
