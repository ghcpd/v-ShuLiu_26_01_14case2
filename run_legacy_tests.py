"""Very small legacy smoke test.

This script is intentionally primitive: it just imports the analytics
module and runs a couple of checks. It does not use pytest or unittest
and is part of the "legacy" baseline state.
"""

import os
import tempfile

from legacy_analytics import summarize_csv


CSV_CONTENT = """value\n1\n2\n3\n4\n5\n"""


def _write_temp_csv() -> str:
    fd, path = tempfile.mkstemp(prefix="legacy_analytics_", suffix=".csv")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(CSV_CONTENT)
    return path


def main() -> None:
    path = _write_temp_csv()
    try:
        stats = summarize_csv(path)
        assert round(stats["mean"], 3) == 3.0
        assert round(stats["median"], 3) == 3.0
        # population stdev of [1,2,3,4,5] is sqrt(2.0)
        assert round(stats["stdev"], 3) == round(2.0 ** 0.5, 3)
        print("legacy smoke test passed")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
