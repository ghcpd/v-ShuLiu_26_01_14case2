# Legacy Analytics (maintenance)

This small project provides a tiny analytics routine that computes basic
statistics (mean, median, population standard deviation) over a CSV file.

## Purpose

This repository preserves the original analytics behavior while improving
reproducibility and adding a simple test workflow.

## Setup (Windows)

1. Create a virtual environment (from repository root):

   ```powershell
   python -m venv .venv
   ```

2. Activate the virtual environment (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   or for cmd.exe:

   ```cmd
   .venv\Scripts\activate.bat
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

Notes: The `requirements.txt` pins modern, installable versions of
`pandas` and `numpy` that are compatible with Python 3.8+. Tests require
`pytest` (installed by `requirements.txt`), but the unified test runner
falls back to `unittest` if `pytest` is not present.

## Running tests

From the repository root run:

```powershell
python run_tests.py
```

This script tries to use `pytest` when available and falls back to the
standard library `unittest` discovery when not. It exits with code `0`
only when all tests pass.

## Notes on preserving semantics

The `legacy_analytics/analytics_legacy.py` file is left intact
semantically — the tests replicate the original smoke checks to ensure
mean / median / stdev values remain unchanged for a canonical sample
input. The test suite and updated runner make it safe to modernize the
environment without altering numeric behavior.
