# Legacy Analytics (maintenance exercise)

A minimal internal analytics utility that computes simple CSV-based
statistics (mean, median, population standard deviation). This repo is
kept as a legacy example; the original business logic in
`legacy_analytics/analytics_legacy.py` is preserved while the
environment and tests were modernized.

## What it does

- Loads a CSV file and computes `mean`, `median`, and population
  `stdev` for a named column (default `value`).

## Setup (Windows, PowerShell)

1. Create a virtual environment:

   python -m venv .venv

2. Activate it in PowerShell:

   .\.venv\Scripts\Activate.ps1

3. Install dependencies:

   pip install -r requirements.txt

## Run tests

Execute the unified test entry script (works with or without pytest):

   python run_tests.py

The runner prefers `pytest` if it is installed; otherwise it falls
back to Python's `unittest` discovery.

## Notes on dependencies

- `requirements.txt` pins modern, compatible releases of `pandas` and
  `numpy` that work on Python 3.8+ and reproduce the original numeric
  behavior.
- The analytics implementation intentionally keeps its original
  algorithms so computed numbers remain unchanged.
