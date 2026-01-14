# Legacy Analytics Maintenance

## Overview

This project maintains a small Python analytics tool that computes basic statistics (mean, median, standard deviation) over CSV data. The business logic has been preserved from the original implementation while dependencies have been modernized and the testing infrastructure has been improved.

## What the Project Does

The `legacy_analytics` module provides simple CSV-based statistics computation:

- **mean**: Arithmetic mean of column values
- **median**: Median (middle) value of column values
- **stdev**: Population standard deviation of column values

The module was originally built with pandas 0.25.3 and numpy 1.17.0, which are now outdated. This maintenance task modernizes these dependencies while preserving the exact same numerical behavior.

## Setup Instructions (Windows)

### 1. Create a Virtual Environment

Open PowerShell or Command Prompt in the repository root and run:

```powershell
python -m venv venv
```

### 2. Activate the Virtual Environment

In **PowerShell**:
```powershell
.\venv\Scripts\Activate.ps1
```

In **Command Prompt (cmd.exe)**:
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

With the virtual environment active:

```powershell
pip install -r requirements.txt
```

This installs:
- **pandas** (1.3.0 to <2.0.0) - Data manipulation and CSV loading
- **numpy** (1.17.0 to <2.0.0) - Numerical computation
- **pytest** (6.0.0+) - Testing framework (optional but recommended)

## Running Tests

With the virtual environment activated, run tests from the repository root:

```powershell
python run_tests.py
```

This unified test entry script:
- First attempts to use pytest if it's installed
- Falls back to Python's built-in unittest discovery if pytest is unavailable
- Discovers and runs all tests in the `tests/` directory
- Returns exit code 0 if all tests pass, non-zero otherwise

### Test Coverage

Two test modules are provided:

- **`tests/test_legacy_smoke.py`**: Reproduces the exact checks from the original `run_legacy_tests.py`
- **`tests/test_analytics.py`**: Comprehensive test suite covering:
  - Simple numeric series
  - Even-length series (median interpolation)
  - Single-value cases
  - Error handling (missing columns, empty data)
  - Custom column names
  - Floating-point values

## File Structure

```
.
├── legacy_analytics/
│   ├── __init__.py                 # Module exports
│   └── analytics_legacy.py          # Core analytics implementation (unchanged)
├── tests/
│   ├── test_analytics.py            # Comprehensive test suite
│   └── test_legacy_smoke.py         # Legacy smoke test reproduction
├── run_tests.py                     # Unified test entry script
├── requirements.txt                 # Modern dependencies
├── requirements_legacy.txt          # Original outdated dependencies (reference)
├── run_legacy_tests.py              # Original smoke test script (reference)
└── README.md                        # This file
```

## Key Changes from Original

1. **Modernized Dependencies**
   - Upgraded pandas from 0.25.3 to >=1.3.0,<2.0.0
   - Upgraded numpy from 1.17.0 to >=1.17.0,<2.0.0
   - Added pytest for improved testing infrastructure

2. **Improved Testing**
   - Created proper `tests/` directory with unittest-compatible test modules
   - Tests are discoverable by both pytest and unittest
   - Comprehensive test coverage for edge cases

3. **Fixed Test Entry Script**
   - Fixed `__main__` guard typo in `run_tests.py`
   - Implemented proper pytest/unittest fallback mechanism
   - Proper exit code propagation

4. **Documentation**
   - Preserved `legacy_analytics/analytics_legacy.py` unchanged in semantics
   - All original modules remain importable and functional
   - Clear setup instructions for Windows environments

## Dependency Version Notes

- **pandas**: Versions 1.3.0+ maintain compatibility with the statistical functions used (read_csv, dropna, astype)
- **numpy**: The range 1.17.0-<2.0.0 ensures consistency with the original mathematical operations
- **pytest**: Modern version 6.0.0+ provides the testing framework with excellent discovery and reporting

These versions are proven to work on Python 3.8, 3.9, 3.10, and 3.11+.

## Verifying Numerical Consistency

The analytics module implements calculations manually (mean, median, stdev) to ensure consistency. To verify behavior has been preserved:

1. Run the legacy smoke test: `python run_tests.py`
2. Check that all tests in `test_legacy_smoke.py` pass
3. The series [1, 2, 3, 4, 5] must produce:
   - mean = 3.0
   - median = 3.0
   - stdev ≈ 1.41421 (sqrt(2.0))

## Troubleshooting

**ImportError: No module named 'pytest'**: Either install pytest (`pip install pytest`) or the script will automatically fall back to unittest.

**Virtual environment activation fails**: Ensure you're using PowerShell or Command Prompt, not Git Bash or WSL.

**CSV file not found**: Use absolute paths when calling `summarize_csv()`, or place test CSVs in the repository root.

## License

This is a maintenance project preserving legacy code. Original authors' intentions have been maintained.
