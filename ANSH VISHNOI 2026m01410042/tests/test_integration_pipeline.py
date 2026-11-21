"""
Integration Tests for End-to-End Pipeline
Verifies the complete execution chain:
Raw Ingestion -> Audit -> Clean -> Feature Engineering -> Statistical Aggregation
"""

import pytest
from src.data_loader import load_raw_data
from src.data_auditor import DataQualityAuditor
from src.data_cleaner import DataCleaner
from src.feature_engineering import add_engineered_features
from src.eda_analyzer import EDAAnalyzer
from src.outlier_detector import OutlierDetector


def test_full_pipeline_integration():
    # 1. Ingestion
    raw_df = load_raw_data()
    assert len(raw_df) > 7000

    # 2. Audit
    auditor = DataQualityAuditor(raw_df)
    audit_results = auditor.run_full_audit()
    assert audit_results["total_records"] == len(raw_df)
    assert audit_results["duplicates"]["duplicate_count"] > 0

    # 3. Clean
    cleaner = DataCleaner(raw_df)
    clean_df, log_df = cleaner.clean_dataset()
    assert clean_df.duplicated().sum() == 0
    assert clean_df.isnull().sum().sum() == 0

    # 4. Feature Engineering
    enriched_df = add_engineered_features(clean_df)
    assert "Delivery_Days" in enriched_df.columns
    assert "Profit_Margin" in enriched_df.columns
    assert "Revenue_per_Customer" in enriched_df.columns

    # 5. Outlier Detection
    detector = OutlierDetector(enriched_df)
    outlier_dict = detector.analyze_all_key_variables()
    assert "Sales" in outlier_dict
    assert "Profit" in outlier_dict

    # 6. EDA Aggregations
    eda = EDAAnalyzer(enriched_df)
    stats_df = eda.compute_descriptive_statistics()
    assert not stats_df.empty
    assert len(stats_df) == 8  # 8 numerical variables

    biz_answers = eda.answer_business_questions()
    assert len(biz_answers) >= 5
