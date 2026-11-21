# 🧪 Automated Test Suite Directory (`tests/`)

## Overview
This directory houses the comprehensive automated test suite for the project, implemented using `pytest`. The suite includes both granular **Unit Tests** for individual modules and end-to-end **Integration Tests** verifying the full data pipeline.

## Test Files Breakdown
- **`conftest.py`**: Defines reusable pytest fixtures and synthetic mock data containing injected anomalies (casing defects, impossible values, conflicting delivery dates, duplicates).
- **`test_data_loader.py`**: Validates file reading, schema verification, and fallbacks.
- **`test_data_auditor.py`**: Validates that all missing values, duplicate records, range errors, and date contradictions are accurately flagged.
- **`test_data_cleaner.py`**: Asserts that cleaning functions are idempotent, imputations are valid, and zero duplicate or contradictory dates remain.
- **`test_feature_engineering.py`**: Asserts correctness of mathematical formulas for `Delivery_Days`, `Profit_Margin`, and customer grouping.
- **`test_outlier_detector.py`**: Asserts boundary math for IQR and Z-scores against analytical edge cases.
- **`test_integration_pipeline.py`**: Executes the entire end-to-end pipeline (Raw Ingestion -> Audit -> Clean -> Feature Engineering -> Statistical & Visual Export) to guarantee end-to-end system cohesion.

## How to Run Tests
From the workspace root directory:
```bash
# Run all tests with verbose output
.venv/bin/pytest tests -v
```
