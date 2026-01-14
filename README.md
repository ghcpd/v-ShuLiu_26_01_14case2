# Legacy Analytics (maintenance)

What this project is
- Small, legacy internal utility that computes basic CSV statistics
  (mean, median, population standard deviation) for a numeric column.
- The implementation in `legacy_analytics/analytics_legacy.py` is the
  behavioral reference and must not change.

Quick setup (Windows PowerShell, Python 3.8+)
1. Create a virtual environment and activate it:

   python -m venv .venv; .\.venv\Scripts\Activate.ps1

2. Install dependencies:

   python -m pip install --upgrade pip; python -m pip install -r requirements.txt

3. Run the test-suite (unified entry point):

   python run_tests.py

Notes
- Tests are written with `unittest` so they run with or without `pytest`.
  If `pytest` is installed it will be used automatically by
  `run_tests.py` for discovery and nicer output.
- We pinned versions that are known to install on Python 3.8 on Windows
  (see `requirements.txt`).

Preserving semantics
- The numerical behavior of `summarize_csv` is preserved; tests assert
  the same reference values used by the original smoke test.

If you want CI
- CI can run the single command `python run_tests.py` after creating a
  Python 3.8+ environment and installing `requirements.txt`.
