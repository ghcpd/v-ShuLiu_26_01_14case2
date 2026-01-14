"""Legacy analytics module.

This module implements a very small analytics routine over a CSV file.
The implementation is intentionally simple and slightly old‑fashioned,
but its *behavior* is considered correct and must be preserved.
"""

from __future__ import annotations

import math
from typing import Dict

import pandas as pd


def summarize_csv(path: str, column: str = "value") -> Dict[str, float]:
    """Load a CSV file and compute basic statistics for the given column.

    The function returns a dictionary with three keys:
    - "mean": the arithmetic mean of the column
    - "median": the median value
    - "stdev": the (population) standard deviation

    The exact numerical behavior of this function is considered the
    reference behavior for business users and should not be changed.
    """

    df = pd.read_csv(path)
    if column not in df.columns:
        raise ValueError("missing column: %s" % column)

    series = df[column].dropna().astype(float)
    if len(series) == 0:
        raise ValueError("no data in column: %s" % column)

    values = list(series)
    n = float(len(values))

    # mean
    total = 0.0
    for v in values:
        total += float(v)
    mean = total / n

    # median (simple sorted middle value, no interpolation)
    values_sorted = sorted(values)
    mid = int(len(values_sorted) / 2)
    if len(values_sorted) % 2 == 1:
        median = float(values_sorted[mid])
    else:
        median = float(values_sorted[mid - 1] + values_sorted[mid]) / 2.0

    # population standard deviation
    sq_sum = 0.0
    for v in values:
        sq_sum += (float(v) - mean) ** 2.0
    stdev = math.sqrt(sq_sum / n)

    return {"mean": mean, "median": median, "stdev": stdev}


def print_summary(path: str, column: str = "value") -> None:
    """Print a human‑readable summary for quick manual inspection.

    The format is intentionally simple and free‑form. It is *not*
    designed for machine consumption and is kept here as the legacy
    reference format.
    """

    stats = summarize_csv(path, column=column)
    print("Summary for %s[%s]" % (path, column))
    print("  mean = %.3f" % stats["mean"])
    print("  median = %.3f" % stats["median"])
    print("  stdev = %.3f" % stats["stdev"])
