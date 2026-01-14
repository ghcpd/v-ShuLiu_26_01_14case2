"""Test suite for legacy analytics module.

Tests verify that the core analytics functions (mean, median, stdev)
produce the expected numerical results from test data.
"""

import os
import tempfile
import unittest

from legacy_analytics import summarize_csv


class TestAnalyticsBasic(unittest.TestCase):
    """Tests for basic analytics functionality."""

    @staticmethod
    def _write_temp_csv(content: str) -> str:
        """Helper to write CSV content to a temporary file."""
        fd, path = tempfile.mkstemp(prefix="legacy_analytics_test_", suffix=".csv")
        os.close(fd)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            try:
                os.remove(path)
            except OSError:
                pass
            raise
        return path

    def test_simple_series_1_to_5(self):
        """Test with simple series [1, 2, 3, 4, 5]."""
        csv_content = "value\n1\n2\n3\n4\n5\n"
        path = self._write_temp_csv(csv_content)
        try:
            stats = summarize_csv(path)
            self.assertAlmostEqual(stats["mean"], 3.0, places=5)
            self.assertAlmostEqual(stats["median"], 3.0, places=5)
            # population stdev of [1,2,3,4,5] is sqrt(2.0) ≈ 1.41421
            self.assertAlmostEqual(stats["stdev"], 2.0 ** 0.5, places=5)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_even_length_series(self):
        """Test with even-length series [10, 20, 30, 40]."""
        csv_content = "value\n10\n20\n30\n40\n"
        path = self._write_temp_csv(csv_content)
        try:
            stats = summarize_csv(path)
            self.assertAlmostEqual(stats["mean"], 25.0, places=5)
            # Median of [10, 20, 30, 40] is (20 + 30) / 2 = 25.0
            self.assertAlmostEqual(stats["median"], 25.0, places=5)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_single_value(self):
        """Test with single value."""
        csv_content = "value\n42\n"
        path = self._write_temp_csv(csv_content)
        try:
            stats = summarize_csv(path)
            self.assertAlmostEqual(stats["mean"], 42.0, places=5)
            self.assertAlmostEqual(stats["median"], 42.0, places=5)
            self.assertAlmostEqual(stats["stdev"], 0.0, places=5)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_missing_column_raises_error(self):
        """Test that missing column raises ValueError."""
        csv_content = "value\n1\n2\n3\n"
        path = self._write_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                summarize_csv(path, column="nonexistent")
            self.assertIn("missing column", str(ctx.exception).lower())
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_empty_column_raises_error(self):
        """Test that empty column raises ValueError."""
        csv_content = "value\n"
        path = self._write_temp_csv(csv_content)
        try:
            with self.assertRaises(ValueError) as ctx:
                summarize_csv(path, column="value")
            self.assertIn("no data", str(ctx.exception).lower())
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_custom_column_name(self):
        """Test with custom column name."""
        csv_content = "measurement\n5\n10\n15\n"
        path = self._write_temp_csv(csv_content)
        try:
            stats = summarize_csv(path, column="measurement")
            self.assertAlmostEqual(stats["mean"], 10.0, places=5)
            self.assertAlmostEqual(stats["median"], 10.0, places=5)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass

    def test_floats_in_csv(self):
        """Test with floating-point values."""
        csv_content = "value\n1.5\n2.5\n3.5\n"
        path = self._write_temp_csv(csv_content)
        try:
            stats = summarize_csv(path)
            self.assertAlmostEqual(stats["mean"], 2.5, places=5)
            self.assertAlmostEqual(stats["median"], 2.5, places=5)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()
