# ⚙️ Source Code Architecture Directory (`src/`)

## Overview
This directory contains the core modular Python application packages following Clean Code and Single Responsibility Principles (SRP).

## Module Manifest
- **`data_loader.py`**: Safe dataset ingestion functions (`load_raw_data`, `load_cleaned_data`, `get_dataset_overview`).
- **`data_auditor.py`**: Automated data quality auditing engine (`DataQualityAuditor`, `generate_text_audit_report`) evaluating missing values, duplicate counts, category variations, out-of-range bounds, and date contradictions.
- **`data_cleaner.py`**: Deterministic, idempotent data cleaning pipeline (`DataCleaner`, `save_cleaned_data`) with comprehensive transformation logging.
- **`feature_engineering.py`**: Commercial feature creation (`add_engineered_features`) adding `Delivery_Days`, `Profit_Margin`, `Revenue_per_Customer`, and temporal tags.
- **`outlier_detector.py`**: Statistical outlier engine (`OutlierDetector`) computing IQR fences ($Q_1 \pm 1.5 \times \text{IQR}$) and Z-scores ($|Z| > 3.0$) with commercial domain classification.
- **`eda_analyzer.py`**: Core EDA calculations (`EDAAnalyzer`) producing descriptive statistics tables, skewness interpretations, categorical proportions, and answers to the 5 core business questions.
- **`visualizer.py`**: High-resolution chart generator (`Visualizer`) exporting 12 publication-ready PNG figures and reactive Plotly objects for Streamlit.
- **`generate_eda_reports.py`**: Automated report runner compiling audit findings and business groupby answers into markdown reports.

## Execution
Modules can be imported programmatically or run via automated scripts:
```python
from src.data_loader import load_raw_data
from src.data_auditor import DataQualityAuditor

df = load_raw_data()
auditor = DataQualityAuditor(df)
results = auditor.run_full_audit()
```
