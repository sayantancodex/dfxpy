# Changelog

All notable changes to this project will be documented in this file.

## [0.3.4] - 2026-05-06

### Added
- **Dual-Theme Reports**: `dfx.report()` now features a professional Light theme by default with a button to toggle Dark Mode.
- **Improved UX**: Streamlined sidebar navigation and cleaner typography for a "no headaches" professional UI.

## [0.3.3] - 2026-05-06

### Added
- **Premium Interactive Reports**: Added interactive tabs, missingness maps, and correlation heatmaps to `dfx.report()`.
- **Statistical Profiling**: Added Mean, Median, Std Dev, and Skewness to report details.

## [0.3.2] - 2026-05-06

### Changed
- **Strict Validation**: `dfx.auto()` now raises a `ValueError` for empty DataFrames to fail-fast in pipelines.

## [0.3.1] - 2026-05-06

### Fixed
- **API Consistency**: Fixed missing `columns` parameter in `outliers()` and `threshold` in `suggest_features()`.
- **Pipeline Persistence**: Implemented `save()` and `load()` methods for `Pipeline` objects.
- **De-duplication**: `clean_column_names()` now handles duplicate column names by appending indices.

## [0.3.0] - 2026-05-06

### Added
- **Premium HTML Reports**: `dfx.report()` generates standalone, interactive EDA reports.
- **Explainable Cleaning**: `dfx.analyze_cleaning()` tracks and explains all transformations using `df.attrs`.
- **Advanced Fixing**: `dfx.fix()` intelligently repairs currency, percentages, booleans, and messy dates.
- **Dataset Diffing**: `dfx.compare()` tracks detailed changes between data versions.
- **Imbalanced Data Support**: `dfx.balance()` adds oversampling, undersampling, and synthetic interpolation.
- **Workflow Pipelines**: `dfx.pipeline()` for building reusable cleaning chains.
- **ML Advisor**: `dfx.suggest()` recommends models based on dataset profile.
- **Validation**: `dfx.validate()` enforces data contracts via schemas.
- **Leakage Detection**: `dfx.leakage()` identifies potential target leakage.

## [0.2.0] - 2026-05-05

### Added
- **Smart Type Inference**: Object columns are now automatically converted to Numeric or Datetime where possible.
- **Date Feature Extraction**: Automatically extracts year, month, day, and hour from datetime columns.
- **Categorical Target Handling**: `prepare()` now uses `LabelEncoder` for non-numeric targets.
- **Empty DataFrame Safeguards**: Better error handling for edge-case datasets.

### Fixed
- Fixed Pandas 3.0+ deprecation warnings regarding string dtypes.
- Resolved UnicodeEncodeErrors in Windows consoles by removing emojis from terminal output.

## [0.1.1] - 2026-05-05

### Added
- New IO module: `load()`, `read_csv()`, `read_excel()`, and `DataFrame()` exposed directly via `dfxpy`.
- No longer necessary to `import pandas` for common operations.

## [0.1.0] - 2023-05-05

### Added
- Initial release of **dfxpy**.
- Core modules: `auto`, `eda`, `audit`, `prepare`, `outliers`, `feature_selection`.
- CLI implementation.
