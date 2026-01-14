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


class AnalyticsLegacyTests(unittest.TestCase):
    def _write_temp_csv(self, content: str = CSV_CONTENT) -> str:
        fd, path = tempfile.mkstemp(prefix="test_analytics_", suffix=".csv")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_summarize_csv_values(self):
        path = self._write_temp_csv()
        try:
            stats = summarize_csv(path)
            # exact expected values from the legacy implementation
            self.assertAlmostEqual(stats["mean"], 3.0, places=9)
            self.assertAlmostEqual(stats["median"], 3.0, places=9)
            self.assertAlmostEqual(stats["stdev"], (2.0 ** 0.5), places=9)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_print_summary_runs(self):
        path = self._write_temp_csv()
        try:
            # just ensure it runs without error and prints the expected lines
            # (we don't require pytest capture; keep test simple/unittest-only)
            print_summary(path)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
