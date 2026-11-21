"""
Unit Tests for Outlier Detector Module
"""

import pytest
import pandas as pd
from src.outlier_detector import OutlierDetector


def test_detect_iqr_outliers():
    # Construct series with known outlier
    df = pd.DataFrame({"Values": [10, 12, 11, 13, 12, 11, 10, 100]})  # 100 is an outlier
    detector = OutlierDetector(df)
    res = detector.detect_iqr_outliers("Values")

    assert res["outlier_count"] == 1
    assert res["upper_bound"] < 100
    assert 100 in res["outliers_dataframe"]["Values"].values


def test_detect_zscore_outliers():
    df = pd.DataFrame({"Values": [10, 10, 10, 10, 10, 10, 10, 500]})
    detector = OutlierDetector(df)
    res = detector.detect_zscore_outliers("Values", threshold=2.0)
    assert res["outlier_count"] >= 1
