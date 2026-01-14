"""Tests for legacy analytics module."""

import math
import os
import tempfile
import pytest

from legacy_analytics import summarize_csv


CSV_CONTENT = """value\n1\n2\n3\n4\n5\n"""


@pytest.fixture
def temp_csv():
    """Create a temporary CSV file with test data."""
    fd, path = tempfile.mkstemp(prefix="legacy_analytics_", suffix=".csv")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        f.write(CSV_CONTENT)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


def test_summarize_csv_basic(temp_csv):
    """Test basic statistics computation."""
    stats = summarize_csv(temp_csv)
    assert round(stats["mean"], 3) == 3.0
    assert round(stats["median"], 3) == 3.0
    # population stdev of [1,2,3,4,5] is sqrt(2.0)
    assert round(stats["stdev"], 3) == round(math.sqrt(2.0), 3)