"""
Unit Tests for Data Cleaner Module
"""

import pytest
from src.data_cleaner import DataCleaner


def test_data_cleaner_pipeline(mock_raw_dataframe):
    cleaner = DataCleaner(mock_raw_dataframe)
    clean_df, log_df = cleaner.clean_dataset()

    # 1. Deduplication
    assert clean_df.duplicated().sum() == 0
    assert len(clean_df) == 4  # 5 rows initial - 1 duplicate = 4 rows

    # 2. Gender & Region standardization
    assert set(clean_df["Gender"].unique()).issubset({"Male", "Female"})
    assert set(clean_df["Region"].unique()).issubset({"North", "South", "East", "West"})

    # 3. Missing values resolved
    assert clean_df["Age"].isna().sum() == 0
    assert clean_df["Income"].isna().sum() == 0
    assert clean_df["Discount"].isna().sum() == 0
    assert clean_df["Satisfaction_Level"].isna().sum() == 0

    # 4. Dates reconciled (No Delivery_Date < Order_Date)
    assert (clean_df["Delivery_Date"] < clean_df["Order_Date"]).sum() == 0

    # 5. Check log records
    assert not log_df.empty
    assert "Step" in log_df.columns
    assert "Justification" in log_df.columns
