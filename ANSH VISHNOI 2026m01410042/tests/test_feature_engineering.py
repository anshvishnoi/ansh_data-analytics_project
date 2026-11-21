"""
Unit Tests for Feature Engineering Module
"""

import pytest
import pandas as pd
from src.data_cleaner import DataCleaner
from src.feature_engineering import add_engineered_features


def test_add_engineered_features(mock_raw_dataframe):
    cleaner = DataCleaner(mock_raw_dataframe)
    clean_df, _ = cleaner.clean_dataset()
    enriched_df = add_engineered_features(clean_df)

    # 1. Calculated columns existence
    expected_cols = [
        "Delivery_Days", "Profit_Margin", "Revenue_per_Customer",
        "Customer_Order_Count", "Discount_Amount", "Order_Year", "Order_Month", "Delivery_SLA_Status"
    ]
    for col in expected_cols:
        assert col in enriched_df.columns, f"Missing engineered column {col}"

    # 2. Check Delivery_Days is non-negative
    assert (enriched_df["Delivery_Days"] < 0).sum() == 0

    # 3. Profit Margin formula correctness
    for _, row in enriched_df.iterrows():
        expected_margin = round((row["Profit"] / row["Sales"]) * 100, 2)
        assert abs(row["Profit_Margin"] - expected_margin) < 0.1
