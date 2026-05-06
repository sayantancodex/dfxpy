from .core import auto
from .eda import eda, report
from .audit import audit, leakage
from .prepare import prepare
from .outliers import handle_outliers as outliers
from .feature_selection import suggest_features
from .cleaning import clean_column_names, handle_missing, infer_types, fix
from .io import load, read_csv, read_excel, DataFrame
from .diff import compare
from .sampling import balance
from .validation import validate
from .pipeline import pipeline, Pipeline
from .ml import suggest
from .history import analyze_cleaning
from .research import profile_stats as profile, to_latex, get_lineage_hash as lineage, research_report

__version__ = "0.3.0"
__all__ = [
    "auto",
    "eda",
    "report",
    "audit",
    "leakage",
    "prepare",
    "outliers",
    "suggest_features",
    "clean_column_names",
    "handle_missing",
    "infer_types",
    "fix",
    "load",
    "read_csv",
    "read_excel",
    "DataFrame",
    "compare",
    "balance",
    "validate",
    "pipeline",
    "Pipeline",
    "suggest",
    "analyze_cleaning",
    "profile",
    "to_latex",
    "lineage",
    "research_report"
]
