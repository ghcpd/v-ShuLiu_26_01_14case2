# Legacy Analytics Tool

This project provides a simple CSV-based analytics tool that computes basic statistics (mean, median, and population standard deviation) for a specified column in a CSV file.

## Business Purpose

The tool is designed for quick statistical analysis of numerical data stored in CSV format. It preserves legacy behavior for consistency with existing business processes.

## Setup

### Prerequisites
- Python 3.8 or higher
- Windows 10 or later

### Virtual Environment Setup
1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running Tests

To run the test suite, use the unified test script:

```
python run_tests.py
```

This script will:
- Use pytest if available for running tests
- Fall back to unittest if pytest is not installed
- Discover and run all tests in the `tests/` directory
- Exit with code 0 if all tests pass, non-zero otherwise

## Dependencies

- pandas: For CSV reading and data manipulation
- numpy: For numerical computations (though not directly used in legacy code)
- pytest: For testing (optional, falls back to unittest)

The legacy analytics behavior is preserved using manual computations to ensure numerical consistency across Python/pandas versions.