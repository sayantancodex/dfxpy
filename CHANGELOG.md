# Changelog

All notable changes to this project will be documented in this file.

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
