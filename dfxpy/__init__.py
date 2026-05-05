from .core import auto
from .eda import eda
from .audit import audit
from .prepare import prepare
from .outliers import handle_outliers as outliers
from .feature_selection import suggest_features
from .cleaning import clean_column_names, handle_missing, infer_types
from .io import load, read_csv, read_excel, DataFrame
from .research import profile_stats as profile, to_latex, get_lineage_hash as lineage, research_report

__version__ = "0.2.6"
__all__ = [
    "auto",
    "eda",
    "audit",
    "prepare",
    "outliers",
    "suggest_features",
    "clean_column_names",
    "handle_missing",
    "infer_types",
    "load",
    "read_csv",
    "read_excel",
    "DataFrame",
    "profile",
    "to_latex",
    "lineage",
    "research_report"
]
