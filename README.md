# Legacy Analytics Tool

## Overview

This project provides a simple CSV-based analytics library for computing basic statistics (mean, median, and population standard deviation) on numerical data. The core analytics logic has been maintained from the original implementation to preserve its correct business behavior while the project infrastructure has been modernized for easier maintenance and deployment.

## Business Purpose

The `legacy_analytics` module processes CSV files containing numerical data and computes three key statistics:

- **Mean**: The arithmetic average of all values
- **Median**: The middle value when data is sorted (with interpolation for even-length datasets)
- **Standard Deviation**: The population standard deviation measuring data spread

This tool is designed for quick statistical analysis of CSV datasets and can be integrated into larger data processing pipelines.

## Project Structure

```
legacy_analytics/
    __init__.py              # Package initialization
    analytics_legacy.py      # Core analytics implementation (preserved semantics)
tests/
    __init__.py              # Tests package initialization
    test_analytics_legacy.py # Comprehensive test suite
run_tests.py                 # Unified test entry point
run_legacy_tests.py          # Original smoke tests (legacy reference)
requirements.txt             # Modern Python dependencies
requirements_legacy.txt      # Original outdated dependencies (reference only)
README.md                    # This file
```

## Setup Instructions (Windows)

### Prerequisites

- Python 3.8 or higher
- Windows 10 or later

### Step 1: Create a Virtual Environment

Open PowerShell or Command Prompt and navigate to the project root directory:

```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

You should see `(venv)` appear in your command prompt, indicating the virtual environment is active.

### Step 2: Install Dependencies

With the virtual environment activated, install the required packages:

```powershell
pip install -r requirements.txt
```

This will install:
- **pandas** (>=1.3.0, <3.0.0): For CSV data manipulation
- **numpy** (>=1.21.0, <3.0.0): For numerical operations
- **pytest** (>=7.0.0, <9.0.0): For running tests (optional but recommended)

### Step 3: Verify Installation

You can verify the installation by running the test suite (see Testing section below).

## Usage

### Basic Usage

```python
from legacy_analytics import summarize_csv

# Analyze a CSV file
stats = summarize_csv("data.csv", column="value")

print(f"Mean: {stats['mean']:.3f}")
print(f"Median: {stats['median']:.3f}")
print(f"Standard Deviation: {stats['stdev']:.3f}")
```

### Print Summary

For quick human-readable output:

```python
from legacy_analytics import print_summary

print_summary("data.csv", column="value")
```

### CSV Format

Your CSV file should have a header row with at least one numerical column:

```csv
value
1.5
2.3
3.7
4.2
5.8
```

## Testing

### Running Tests

The project includes a unified test entry script that automatically uses pytest if available, or falls back to unittest:

```powershell
python run_tests.py
```

This command will:
1. Attempt to use pytest for running tests (if installed)
2. Fall back to unittest if pytest is not available
3. Discover and run all tests in the `tests/` directory
4. Exit with code 0 if all tests pass, non-zero otherwise

### Test Coverage

The test suite (`tests/test_analytics_legacy.py`) includes comprehensive tests for:

- Basic statistics on simple datasets
- Edge cases (single value, empty data, negative numbers)
- Even and odd length datasets (median calculation)
- Floating-point precision
- Custom column names
- Error handling (missing columns, empty data)
- NA/NaN value handling

### Running Legacy Smoke Tests

The original smoke tests are preserved in `run_legacy_tests.py` and can be run directly:

```powershell
python run_legacy_tests.py
```

## Dependency Management

### Modern Dependencies (requirements.txt)

The project now uses modern, actively maintained versions of scientific libraries:

- **pandas >=1.3.0, <3.0.0**: Modern pandas with improved performance and stability
- **numpy >=1.21.0, <3.0.0**: Current numpy with Python 3.8+ compatibility
- **pytest >=7.0.0, <9.0.0**: Modern testing framework

These versions install cleanly on Python 3.8+ and Windows 10+.

### Legacy Dependencies (requirements_legacy.txt)

The original `requirements_legacy.txt` file is preserved for historical reference but is **not recommended** for use:

- pandas==0.25.3 (released 2019, may not install on modern Python)
- numpy==1.17.0 (released 2019, lacks modern security and performance fixes)

### Preserving Analytics Semantics

**Important**: Despite upgrading dependencies, the core analytics behavior remains **identical**. The `legacy_analytics/analytics_legacy.py` module uses basic Python math operations and pandas' stable APIs, ensuring that:

- Mean, median, and standard deviation calculations produce the same numerical results
- Rounding and floating-point behavior is preserved
- Edge case handling remains consistent

The comprehensive test suite verifies this semantic equivalence.

## CI/CD Integration

This project is designed to be easily integrated into continuous integration pipelines. Simply call:

```bash
python run_tests.py
```

The script will exit with code 0 on success and non-zero on failure, making it suitable for automated testing environments.

## Maintenance Notes

### Design Principles

1. **Semantic Preservation**: The original `analytics_legacy.py` module is unchanged in its calculation logic to maintain compatibility with existing business processes.

2. **Dependency Modernization**: Dependencies have been updated to modern, supported versions while ensuring numerical compatibility.

3. **Test Coverage**: Comprehensive tests ensure that future changes don't inadvertently alter analytical results.

4. **Portability**: All scripts use cross-platform Python and are tested on Windows with PowerShell.

### Future Enhancements

Potential improvements for future maintenance cycles:

- Add support for additional statistical measures (variance, quartiles, etc.)
- Implement data validation and type checking
- Add command-line interface for direct CSV processing
- Expand test coverage with property-based testing
- Add performance benchmarks

## Troubleshooting

### Import Errors

If you encounter import errors, ensure:
1. The virtual environment is activated
2. Dependencies are installed via `pip install -r requirements.txt`
3. You're running Python from the project root directory

### Test Failures

If tests fail after upgrading dependencies:
1. Check that you're using Python 3.8 or higher
2. Verify pandas and numpy are properly installed
3. Review test output for specific assertion failures

### Virtual Environment Issues

To recreate the virtual environment:

```powershell
# Deactivate if active
deactivate

# Remove old environment
Remove-Item -Recurse -Force venv

# Create new environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## License

This is an internal tool. Refer to your organization's software licensing policies.

## Contact

For questions or issues related to this analytics tool, contact your development team or project maintainer.
