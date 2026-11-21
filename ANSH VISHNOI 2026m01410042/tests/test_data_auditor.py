"""
Unit Tests for Data Quality Auditor
"""

import pytest
from src.data_auditor import DataQualityAuditor


def test_audit_missing_values(mock_raw_dataframe):
    auditor = DataQualityAuditor(mock_raw_dataframe)
    missing_df = auditor.audit_missing_values()
    assert not missing_df.empty
    delivery_missing = missing_df[missing_df["Column"] == "Delivery_Date"]["Missing_Count"].values[0]
    assert delivery_missing == 1


def test_audit_duplicates(mock_raw_dataframe):
    auditor = DataQualityAuditor(mock_raw_dataframe)
    dup_res = auditor.audit_duplicates()
    assert dup_res["duplicate_count"] == 1


def test_audit_categorical_inconsistencies(mock_raw_dataframe):
    auditor = DataQualityAuditor(mock_raw_dataframe)
    cat_res = auditor.audit_categorical_inconsistencies()
    assert "female" in cat_res["gender_anomalies"]
    assert "M" in cat_res["gender_anomalies"]
    assert "west" in cat_res["region_anomalies"]
    assert "Nort" in cat_res["region_anomalies"]


def test_audit_numerical_ranges(mock_raw_dataframe):
    auditor = DataQualityAuditor(mock_raw_dataframe)
    num_res = auditor.audit_numerical_ranges()
    assert num_res["age"]["negative_or_zero_count"] == 1
    assert num_res["age"]["extreme_high_count"] == 1
    assert num_res["discount"]["negative_discount_count"] == 1
    assert num_res["discount"]["exceeds_threshold_count"] == 1


def test_audit_dates(mock_raw_dataframe):
    auditor = DataQualityAuditor(mock_raw_dataframe)
    date_res = auditor.audit_dates()
    # TXN101 has Delivery_Date '2023-01-08' < Order_Date '2023-01-10' (appears twice in mock)
    assert date_res["negative_delivery_duration_count"] == 2
