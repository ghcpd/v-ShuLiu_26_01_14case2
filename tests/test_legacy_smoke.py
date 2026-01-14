"""Tests verifying legacy smoke test behavior is preserved."""

import os
import tempfile
import unittest

from legacy_analytics import summarize_csv


class TestLegacySmokeTest(unittest.TestCase):
    """Reproduces the original run_legacy_tests.py smoke tests in unittest form."""

    @staticmethod
    def _write_temp_csv() -> str:
        """Create temporary CSV with standard test data."""
        fd, path = tempfile.mkstemp(prefix="legacy_analytics_smoke_", suffix=".csv")
        os.close(fd)
        csv_content = "value\n1\n2\n3\n4\n5\n"
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(csv_content)
        except Exception:
            try:
                os.remove(path)
            except OSError:
                pass
            raise
        return path

    def test_legacy_smoke_test(self):
        """Original legacy smoke test: verify [1,2,3,4,5] statistics."""
        path = self._write_temp_csv()
        try:
            stats = summarize_csv(path)
            # These assertions match the original run_legacy_tests.py exactly
            self.assertEqual(round(stats["mean"], 3), 3.0)
            self.assertEqual(round(stats["median"], 3), 3.0)
            # population stdev of [1,2,3,4,5] is sqrt(2.0)
            self.assertEqual(
                round(stats["stdev"], 3),
                round(2.0 ** 0.5, 3)
            )
        finally:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
