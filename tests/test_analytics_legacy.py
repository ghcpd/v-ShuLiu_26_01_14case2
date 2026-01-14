"""Test cases for analytics_legacy module.

These tests verify the reference behavior of the analytics module
and ensure that any future changes preserve numerical semantics.
"""

import os
import tempfile
import unittest
import math

from legacy_analytics import summarize_csv


class TestAnalyticsLegacy(unittest.TestCase):
    """Test suite for the legacy analytics module."""

    def setUp(self):
        """Create temporary CSV files for testing."""
        self.temp_files = []

    def tearDown(self):
        """Clean up temporary CSV files."""
        for path in self.temp_files:
            try:
                os.remove(path)
            except OSError:
                pass

    def _create_temp_csv(self, content: str) -> str:
        """Helper method to create a temporary CSV file."""
        fd, path = tempfile.mkstemp(prefix="test_analytics_", suffix=".csv")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self.temp_files.append(path)
        return path

    def test_basic_statistics(self):
        """Test basic statistics on a simple dataset [1, 2, 3, 4, 5]."""
        csv_content = "value\n1\n2\n3\n4\n5\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # Expected values for [1, 2, 3, 4, 5]
        # Mean: (1+2+3+4+5)/5 = 15/5 = 3.0
        self.assertAlmostEqual(stats["mean"], 3.0, places=10)
        
        # Median: middle value = 3.0
        self.assertAlmostEqual(stats["median"], 3.0, places=10)
        
        # Population stdev: sqrt(((1-3)^2 + (2-3)^2 + (3-3)^2 + (4-3)^2 + (5-3)^2) / 5)
        # = sqrt((4 + 1 + 0 + 1 + 4) / 5) = sqrt(10/5) = sqrt(2)
        expected_stdev = math.sqrt(2.0)
        self.assertAlmostEqual(stats["stdev"], expected_stdev, places=10)

    def test_even_length_median(self):
        """Test median calculation for even-length dataset."""
        csv_content = "value\n1\n2\n3\n4\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # For [1, 2, 3, 4], median should be (2 + 3) / 2 = 2.5
        self.assertAlmostEqual(stats["median"], 2.5, places=10)

    def test_single_value(self):
        """Test statistics on a single-value dataset."""
        csv_content = "value\n42.0\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # Mean, median, and stdev should all be predictable
        self.assertAlmostEqual(stats["mean"], 42.0, places=10)
        self.assertAlmostEqual(stats["median"], 42.0, places=10)
        self.assertAlmostEqual(stats["stdev"], 0.0, places=10)

    def test_floating_point_values(self):
        """Test statistics with floating-point values."""
        csv_content = "value\n1.5\n2.5\n3.5\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # Mean: (1.5 + 2.5 + 3.5) / 3 = 7.5 / 3 = 2.5
        self.assertAlmostEqual(stats["mean"], 2.5, places=10)
        
        # Median: 2.5
        self.assertAlmostEqual(stats["median"], 2.5, places=10)

    def test_negative_values(self):
        """Test statistics with negative values."""
        csv_content = "value\n-2\n-1\n0\n1\n2\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # Mean: 0.0
        self.assertAlmostEqual(stats["mean"], 0.0, places=10)
        
        # Median: 0.0
        self.assertAlmostEqual(stats["median"], 0.0, places=10)

    def test_custom_column_name(self):
        """Test reading from a custom column name."""
        csv_content = "custom_col\n10\n20\n30\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path, column="custom_col")
        
        # Mean: 20.0
        self.assertAlmostEqual(stats["mean"], 20.0, places=10)

    def test_missing_column_error(self):
        """Test that missing column raises ValueError."""
        csv_content = "value\n1\n2\n3\n"
        path = self._create_temp_csv(csv_content)
        
        with self.assertRaises(ValueError) as context:
            summarize_csv(path, column="nonexistent")
        
        self.assertIn("missing column", str(context.exception).lower())

    def test_empty_column_error(self):
        """Test that empty column raises ValueError."""
        csv_content = "value\n"
        path = self._create_temp_csv(csv_content)
        
        with self.assertRaises(ValueError) as context:
            summarize_csv(path)
        
        self.assertIn("no data", str(context.exception).lower())

    def test_na_values_ignored(self):
        """Test that NA/NaN values are properly ignored."""
        csv_content = "value\n1\n\n3\n\n5\n"
        path = self._create_temp_csv(csv_content)
        
        stats = summarize_csv(path)
        
        # Should compute on [1, 3, 5], ignoring empty rows
        # Mean: (1+3+5)/3 = 3.0
        self.assertAlmostEqual(stats["mean"], 3.0, places=10)


if __name__ == "__main__":
    unittest.main()
