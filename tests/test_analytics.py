import io
import math
import os
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout

# If pandas is not installed in the current environment (test runner may
# not have network access), provide a minimal shim that implements the
# small subset of `pandas.read_csv` behavior used by
# `legacy_analytics.analytics_legacy`.
try:
    import pandas  # type: ignore
except Exception:
    def _read_csv(path: str):
        # very small DataFrame-like object
        with open(path, "r", encoding="utf-8") as f:
            lines = [l.rstrip("\n") for l in f]
        header = lines[0].split(",")
        rows = [row.split(",") for row in lines[1:] if row != ""]

        class FakeSeries(list):
            def dropna(self):
                return FakeSeries([v for v in self if v is not None and v != ""])

            def astype(self, _type):
                return [float(v) for v in self]

        class FakeDataFrame:
            def __init__(self, header, rows):
                self.columns = header
                self._data = rows

            def __getitem__(self, key):
                if key not in self.columns:
                    raise KeyError(key)
                idx = self.columns.index(key)
                return FakeSeries([r[idx] for r in self._data])

        return FakeDataFrame(header, rows)

    fake_pd = types.SimpleNamespace(read_csv=_read_csv)
    sys.modules["pandas"] = fake_pd

from legacy_analytics import summarize_csv, print_summary

CSV_CONTENT = """value
1
2
3
4
5
"""


class TestAnalytics(unittest.TestCase):
    def _write_temp_csv(self, content: str) -> str:
        fd, path = tempfile.mkstemp(prefix="test_analytics_", suffix=".csv")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_summarize_csv_basic(self):
        path = self._write_temp_csv(CSV_CONTENT)
        try:
            stats = summarize_csv(path)
            self.assertEqual(round(stats["mean"], 3), 3.0)
            self.assertEqual(round(stats["median"], 3), 3.0)
            self.assertEqual(round(stats["stdev"], 3), round(2.0 ** 0.5, 3))
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_missing_column_raises(self):
        path = self._write_temp_csv("wrong\n1\n")
        try:
            with self.assertRaises(ValueError):
                summarize_csv(path, column="value")
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_empty_column_raises(self):
        path = self._write_temp_csv("value\n\n")
        try:
            with self.assertRaises(ValueError):
                summarize_csv(path)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_print_summary_outputs_formatted(self):
        path = self._write_temp_csv(CSV_CONTENT)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                print_summary(path)
            out = buf.getvalue()
            self.assertIn("mean =", out)
            self.assertIn("median =", out)
            self.assertIn("stdev =", out)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
