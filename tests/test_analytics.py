"""Tests for the legacy analytics behavior.

These tests are written with unittest so they can be run by pytest or
by the standard library test runner (unittest) as required.
"""
from __future__ import annotations

import io
import os
import tempfile
import unittest

from legacy_analytics import summarize_csv, print_summary

CSV_CONTENT = """value
1
2
3
4
5
"""


class TestLegacyAnalytics(unittest.TestCase):

    def _write_csv(self, content: str) -> str:
        fd, path = tempfile.mkstemp(prefix="test_analytics_", suffix=".csv")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_summarize_csv_basic(self):
        path = self._write_csv(CSV_CONTENT)
        try:
            stats = summarize_csv(path)
            # match legacy smoke-test expectations (round to 3 decimals)
            self.assertEqual(round(stats["mean"], 3), 3.0)
            self.assertEqual(round(stats["median"], 3), 3.0)
            self.assertEqual(round(stats["stdev"], 3), round(2.0 ** 0.5, 3))
        finally:
            os.remove(path)

    def test_missing_column_raises(self):
        path = self._write_csv("x\n1\n2\n")
        try:
            with self.assertRaises(ValueError):
                summarize_csv(path, column="value")
        finally:
            os.remove(path)

    def test_empty_column_raises(self):
        path = self._write_csv("value\n\n\n")
        try:
            with self.assertRaises(ValueError):
                summarize_csv(path)
        finally:
            os.remove(path)

    def test_print_summary_output(self):
        path = self._write_csv(CSV_CONTENT)
        try:
            buf = io.StringIO()
            # capture printed output
            from contextlib import redirect_stdout

            with redirect_stdout(buf):
                print_summary(path)
            out = buf.getvalue()
            self.assertIn("Summary for", out)
            self.assertIn("mean = 3.000", out)
            self.assertIn("median = 3.000", out)
            self.assertIn("stdev =", out)
        finally:
            os.remove(path)


if __name__ == "__main__":
    unittest.main()
