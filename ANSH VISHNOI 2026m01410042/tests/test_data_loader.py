"""
Unit Tests for Data Loader Module
"""

import pytest
import pandas as pd
from src.data_loader import load_raw_data, load_cleaned_data, get_dataset_overview


def test_load_raw_data_success():
    df = load_raw_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) == 24
    assert "Transaction_ID" in df.columns


def test_load_cleaned_data_success():
    df = load_cleaned_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.isnull().sum().sum() == 0
    assert df.duplicated().sum() == 0


def test_get_dataset_overview():
    df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
    overview = get_dataset_overview(df)
    assert overview["total_rows"] == 3
    assert overview["total_columns"] == 2
    assert "A" in overview["columns"]
