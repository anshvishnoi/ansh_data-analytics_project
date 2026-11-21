# 💻 Standalone Code Snippets Directory (`code_snippets/`)

## Overview
This directory contains modular, executable Python code snippets. Each script is self-contained and demonstrates an isolated phase of the EDA and data engineering lifecycle for easy inspection, testing, and presentation.

## Files & Usage

| File | Purpose | Execution Command |
|:---|:---|:---|
| **`01_data_audit_snippet.py`** | Audits raw missingness, duplicate rows, and category casing inconsistencies. | `.venv/bin/python code_snippets/01_data_audit_snippet.py` |
| **`02_data_cleaning_snippet.py`** | Applies normalization, segment-based median imputation, and chronological date fix. | `.venv/bin/python code_snippets/02_data_cleaning_snippet.py` |
| **`03_feature_engineering_snippet.py`** | Demonstrates the engineering of `Delivery_Days`, `Profit_Margin`, and `Revenue_per_Customer`. | `.venv/bin/python code_snippets/03_feature_engineering_snippet.py` |
| **`04_outlier_detection_snippet.py`** | Computes IQR fences and calculates outlier percentages on Sales, Profit, and Income. | `.venv/bin/python code_snippets/04_outlier_detection_snippet.py` |
| **`05_groupby_business_queries.py`** | Runs the 5 essential commercial groupby aggregations answering core business questions. | `.venv/bin/python code_snippets/05_groupby_business_queries.py` |

## How to Run All Snippets
You can execute any snippet individually from the workspace root using the local environment:
```bash
.venv/bin/python code_snippets/01_data_audit_snippet.py
```
