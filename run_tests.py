"""Unified test entry script for the legacy analytics maintenance task.

This script is part of the *target* solution for the maintenance
exercise. Test runners for evaluation will call this script from the
repository root using:

    python run_tests.py

Behavior requirements:
- Try to use pytest if it is importable.
- If pytest is not available, fall back to unittest discovery.
- Discover and run all tests under the `tests/` directory.
- Exit with code 0 only when all tests pass; otherwise exit with a
  non-zero code.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _run_pytest() -> int:
    import pytest  # type: ignore[import]

    # Let pytest use its default discovery starting from the tests dir.
    tests_dir = Path(__file__).parent / "tests"
    if tests_dir.is_dir():
        return pytest.main([str(tests_dir)])
    # If tests directory does not exist for some reason, still run
    # pytest default discovery from the repo root.
    return pytest.main([str(Path(__file__).parent)])


def _run_unittest() -> int:
    import unittest

    loader = unittest.defaultTestLoader
    tests_dir = Path(__file__).parent / "tests"
    suite = loader.discover(str(tests_dir))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> None:
    try:
        try:
            import pytest  # noqa: F401
        except Exception:  # pragma: no cover - import guard only
            raise ImportError
        exit_code = _run_pytest()
    except ImportError:
        exit_code = _run_unittest()

    # Propagate exit code according to success / failure.
    if exit_code != 0:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
