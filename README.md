# 🛍️ Retail Customer Sales — Exploratory Data Analysis & Decision Dashboard System

> **This project focuses on exploratory data analysis of a retail customer sales dataset. The main objective is to identify data quality issues, clean the dataset, perform statistical analysis, detect outliers, create useful features, and generate business insights through visualizations and an interactive dashboard. 
.**  
> **Author:** Ansh Vishnoi (`2026m01410042`)  
> **GitHub Repository:** [https://github.com/anshvishnoi/ansh_vishnoi_2026m01410042/tree/main](https://github.com/anshvishnoi/ansh_data-analytics_project/tree/main/ANSH%20VISHNOI%202026m01410042)  
> **Source Problem Statement:** `Project1_Exploratory_Data_Analysis.docx`  
> **Dataset:** Simulated Retail Customer Sales Dataset (7,084 raw transaction records across 24 columns, 2023–2024)

---

## 🌟 Executive Highlights
- **100% Rubric Compliance:** Fully implements all 6 assessment criteria (Audit, Cleaning, Descriptive Statistics, Outlier Analysis, GroupBy Insights, and Written Report).
- **Zero Missing & Zero Duplicates:** Sanitized from 7,084 raw records with 61 duplicates and multiple data anomalies down to 7,002 clean, verified transaction rows.
- **12 High-Resolution Visualizations (300 DPI):** Standalone publication-grade figures saved in `eda_summary/figures/`.
- **Interactive Multi-Tab Streamlit App:** Production-ready web interface with reactive Plotly charts, audit comparisons, outlier studio, and 1-click dataset exporter.
- **Automated Quality Assurance:** 13 unit & integration tests passing with 100% pass rate in `pytest`.
- **Formal Enterprise Documentation:** Complete IEEE-style SRS, 2–4 page Executive Insights Report, Data Dictionary, and Project Summary.

---

## 🗂️ Complete Project Architecture & Directory Structure

Har component ke liye ek dedicated folder banaya gaya hai. **Har folder ke andar ek detailed `README.md` hai** jo batata hai ki wo folder kya represent karta hai aur uske andar kya hai:

```text
ANSH VISHNOI 2026m01410042/
├── README.md                          # 🌟 Master Project Documentation & Directory Guide
├── requirements.txt                   # All project dependencies (pandas, streamlit, plotly, pytest)
├── pytest.ini                         # Automated test suite configuration
├── run_app.sh                         # 🚀 1-Click script to launch the Streamlit Web Dashboard
├── retail_customer_sales_dataset.csv  # Original source dataset
├── Project1_Exploratory_Data_Analysis.docx # Original problem statement specification
│
├── data/                              # 📊 Dataset Storage Folder
│   ├── README.md                      # Guide to raw vs processed data schemas
│   ├── raw/
│   │   └── retail_customer_sales_dataset.csv     # Raw dataset (7,084 rows, 24 cols)
│   └── processed/
│       └── cleaned_retail_sales_dataset.csv      # Production-grade sanitized dataset (7,002 rows, 35 cols)
│
├── docs/                              # 📄 Formal Documentation & Specification Folder
│   ├── README.md                      # Documentation index and reading guide
│   ├── SRS_Document.md                # IEEE-standard Software Requirements Specification (FR-1 to FR-8)
│   ├── Project_Summary.md             # High-level project summary and objective mapping
│   ├── Business_Insights_Report.md    # 2–4 page formal business insights report for management
│   └── Data_Dictionary.md             # Complete metadata for all 24 raw fields + 10 engineered features
│
├── src/                               # ⚙️ Modular Python Source Code (Clean Architecture)
│   ├── README.md                      # Architecture guide & module usage instructions
│   ├── __init__.py
│   ├── data_loader.py                 # File reading, type parsing & validation
│   ├── data_auditor.py                # Quality auditor (missingness, duplicates, anomalies, date conflicts)
│   ├── data_cleaner.py                # Cleaning logic (standardization, segment imputation, SLA date fix)
│   ├── feature_engineering.py         # Delivery_Days, Profit_Margin, Revenue_per_Customer, temporal metrics
│   ├── outlier_detector.py            # IQR & Z-score extreme value detection & commercial classification
│   ├── eda_analyzer.py                # Descriptive stats, skewness interpretations, 5 business groupby queries
│   ├── visualizer.py                  # Dual visual engine (12 PNG high-res charts + interactive Plotly figures)
│   └── generate_eda_reports.py        # Automated runner generating all markdown summaries
│
├── app/                               # 🌐 Interactive Streamlit Web Application
│   ├── README.md                      # Step-by-step guide to navigating the Streamlit UI
│   └── main.py                        # Multi-tab interactive analytics & audit web dashboard
│
├── eda_summary/                       # 📈 EDA Findings, Tables & Figures
│   ├── README.md                      # Directory overview and chart catalog
│   ├── data_quality_audit_report.md   # Exact missing counts, duplicate counts, and formatting issues
│   ├── cleaning_justifications.md     # Business & mathematical justification for every cleaning step
│   ├── descriptive_statistics.csv     # Complete parametric/non-parametric statistics table (8 variables)
│   ├── business_questions_answers.md  # 5+ Core business questions answered via GroupBy aggregations
│   └── figures/                       # 🎨 12 High-Resolution (300 DPI) Publication Charts
│       ├── 01_missing_values_audit.png
│       ├── 02_sales_distribution_skew.png
│       ├── 03_income_distribution.png
│       ├── 04_age_demographics.png
│       ├── 05_category_and_segment_share.png
│       ├── 06_outliers_boxplots.png
│       ├── 07_sales_vs_profit_outliers.png
│       ├── 08_aov_by_region.png
│       ├── 09_profit_margin_by_category.png
│       ├── 10_return_rate_analysis.png
│       ├── 11_correlation_heatmap.png
│       └── 12_monthly_sales_trend.png
│
├── code_snippets/                     # 💻 Standalone & Documented Code Snippets
│   ├── README.md                      # Catalog of individual standalone scripts
│   ├── 01_data_audit_snippet.py       # Standalone data quality audit script
│   ├── 02_data_cleaning_snippet.py    # Standalone normalization and imputation script
│   ├── 03_feature_engineering_snippet.py # Standalone calculated columns script
│   ├── 04_outlier_detection_snippet.py   # Standalone IQR & Z-score script
│   └── 05_groupby_business_queries.py   # Standalone business query aggregation script
│
├── output_snippets/                   # 🖼️ Verified Execution Logs & Output Previews
│   ├── README.md                      # Output directory index
│   ├── audit_summary_output.txt       # Captured terminal audit results
│   ├── cleaning_log_output.txt        # Captured cleaning execution log
│   ├── outlier_detection_output.txt   # Captured IQR and Z-score calculations
│   ├── groupby_results_output.txt     # Captured business groupby answers
│   └── test_execution_output.txt      # 100% pytest automated test suite run log
│
└── tests/                             # 🧪 Automated Test Suite (Pytest)
    ├── README.md                      # Testing guide & assertions breakdown
    ├── conftest.py                    # Pytest fixtures and mock anomaly data
    ├── test_data_loader.py            # Unit tests for data loading
    ├── test_data_auditor.py           # Unit tests for anomaly detection
    ├── test_data_cleaner.py           # Unit tests for data cleaning & idempotency
    ├── test_feature_engineering.py    # Unit tests for calculated fields
    ├── test_outlier_detector.py       # Unit tests for IQR boundary calculations
    └── test_integration_pipeline.py  # End-to-end integration test (Raw -> Audit -> Clean -> Analytics)
```

---

## 🎯 Problem Statement Compliance Matrix (100% Rubric Coverage)

| Evaluation Rubric | Weight | Implementation Details | Verified Location |
|:---|:---:|:---|:---|
| **1. Data Quality Audit** | **20%** | Detected 6 columns with missing data, 61 exact duplicates, casing variants in Gender/Region, impossible ages (-12, 999), invalid discounts (<0, >0.5), and 55 rows where `Delivery_Date < Order_Date`. | [`src/data_auditor.py`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/src/data_auditor.py), [`eda_summary/data_quality_audit_report.md`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/eda_summary/data_quality_audit_report.md) |
| **2. Cleaning Decisions & Justifications** | **20%** | Justified deduplication, casing mapping, segment-level median imputation for skewed numericals, delivery-mode SLA date imputation, and financial recalculation. | [`src/data_cleaner.py`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/src/data_cleaner.py), [`eda_summary/cleaning_justifications.md`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/eda_summary/cleaning_justifications.md) |
| **3. Descriptive Stats & Univariate Analysis** | **20%** | Mean, Median, Mode, Std, Variance, Q1, Q2, Q3, Min, Max, IQR, and Skewness for all 8 numerical fields. Skewness qualitative explanation for `Sales`, `Income`, `Age`. | [`src/eda_analyzer.py`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/src/eda_analyzer.py), [`eda_summary/descriptive_statistics.csv`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/eda_summary/descriptive_statistics.csv) |
| **4. Outlier Analysis & Business Reasoning** | **15%** | Applied IQR and Z-Score fences to `Sales`, `Profit`, `Income`, `Age`. Justified that extreme sales values (>₹30k) are genuine bulk B2B purchases that must be retained. | [`src/outlier_detector.py`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/src/outlier_detector.py), [`eda_summary/figures/06_outliers_boxplots.png`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/eda_summary/figures/06_outliers_boxplots.png) |
| **5. Calculated Fields & Grouped Insights** | **15%** | Engineered `Delivery_Days`, `Profit_Margin`, `Revenue_per_Customer`, `Discount_Amount`, `Order_YearMonth`. Answered the 5 core business questions with groupby aggregations. | [`src/feature_engineering.py`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/src/feature_engineering.py), [`eda_summary/business_questions_answers.md`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/eda_summary/business_questions_answers.md) |
| **6. Written Report & Business Framing** | **10%** | Comprehensive 2–4 page executive report translating statistical findings into plain-business language for senior leadership. | [`docs/Business_Insights_Report.md`](file:///Users/anshvishnoi/Desktop/ANSH%20VISHNOI%202026m01410042/docs/Business_Insights_Report.md) |

---

## 🚀 Quick Start Guide

### 1. Launch the Interactive Streamlit Web App
Run the 1-click startup script from the project root:
```bash
./run_app.sh
```
Or run directly via the virtual environment:
```bash
.venv/bin/streamlit run app/main.py
```
Open your browser at `http://localhost:8501`.

### 2. Run the Automated Test Suite (13 Tests)
```bash
.venv/bin/pytest tests -v
```

### 3. Re-generate All Figures and Reports
```bash
.venv/bin/python -m src.generate_eda_reports
```

### 4. Run Standalone Code Snippets
```bash
.venv/bin/python code_snippets/01_data_audit_snippet.py
.venv/bin/python code_snippets/05_groupby_business_queries.py
```

---

## 📈 Key Executive Findings Summary

1. **High Skewness in Basket Size:** Sales are strongly right-skewed (skew = +2.05). Median order value is ₹7,925, but top-tier corporate procurement accounts extend up to ₹1,22,950, pulling the mean upward to ₹10,942.
2. **National Footprint Balance:** Demand is uniformly distributed across the 4 Indian zones (~25% in each region: West 25.3%, East 25.1%, South 25.1%, North 24.5%), showing balanced national brand penetration.
3. **Category Profitability:** Electronics drives the highest top-line revenue (₹2.17 Cr) and total cash profit, while Office Supplies and Clothing maintain healthier margin consistency (~33%).
4. **Logistics Speed Drives Satisfaction:** 48-hour delivery SLA orders average **4.1 / 5.0** in rating, while orders delayed $>5$ days suffer from low satisfaction and elevated return rates.
5. **Cleaned Dataset Integrity:** 100% of missing values and duplicate rows resolved, with full audit trail preserved.
