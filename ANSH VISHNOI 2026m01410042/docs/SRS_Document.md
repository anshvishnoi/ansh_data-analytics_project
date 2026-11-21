# 📋 Software Requirements Specification (SRS)
## Project Title: Retail Customer Sales - Exploratory Data Analysis & Analytics System
**Document Version:** 1.0.0  
**Prepared For:** Academic & Enterprise Production Review  
**Author:** Ansh Vishnoi  
**Standard Compliance:** Tailored IEEE-Std 830-1998  

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to specify the complete functional and non-functional requirements for the **Retail Customer Sales Exploratory Data Analysis (EDA) and Decision Support Dashboard System**. This system ingests simulated multi-year retail transaction data across Indian commercial zones, identifies data quality defects, applies deterministic cleaning rules, engineers business metrics, computes statistical distributions, detects extreme value anomalies, and serves interactive visualizations for operational and managerial decision-making.

### 1.2 Scope of the Software
The software encompasses:
- An automated ingestion and auditing engine (`data_auditor.py`).
- A reproducible, idempotent cleaning and reconciliation pipeline (`data_cleaner.py`).
- A feature engineering module adding derived operational metrics (`feature_engineering.py`).
- A statistical exploratory analysis engine (`eda_analyzer.py`).
- An extreme-value outlier detector leveraging IQR and Z-score criteria (`outlier_detector.py`).
- A dual visualization engine (Matplotlib static high-res exports + dynamic Plotly figures) (`visualizer.py`).
- A production-grade Streamlit web interface (`app/main.py`) providing interactive exploration, KPI cards, visual query filters, and clean data export.

### 1.3 Definitions, Acronyms, and Abbreviations
- **AOV:** Average Order Value ($\text{Total Sales} / \text{Total Orders}$).
- **IQR:** Interquartile Range ($Q_3 - Q_1$).
- **KDE:** Kernel Density Estimation.
- **SLA:** Service Level Agreement (turnaround time for logistics fulfillment).
- **SRS:** Software Requirements Specification.
- **KPI:** Key Performance Indicator.

---

## 2. Overall Description

### 2.1 Product Perspective
The system functions as an end-to-end data processing and decision support platform. It bridges raw e-commerce transaction logs with boardroom-level business intelligence.

```
+-------------------------------------------------------------------+
| Raw CSV Ingestion (7,084 records, 24 features)                    |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| Data Quality Audit Engine (Missingness, Dups, Inconsistencies)    |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| Production Cleaning Pipeline (Imputation, SLA Date Fix, Standard) |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
| Feature Engineering (Delivery_Days, Profit_Margin, Customer_CLV)  |
+-------------------------------------------------------------------+
                                  |
        +-------------------------+-------------------------+
        |                                                   |
        v                                                   v
+-----------------------------+             +-------------------------------+
| Statistical & Outlier Engine|             | Interactive Streamlit Web UI  |
| (Descriptive, Skewness, IQR)|             | (KPIs, Charts, Snippet Viewer)|
+-----------------------------+             +-------------------------------+
```

### 2.2 Product Functions
1. **Quality Audit:** Detect missing fields, duplicate transactions, corrupted date chronologies, casing/spelling variations, and invalid mathematical entries.
2. **Deterministic Data Cleaning:** Standardize categorical entries into canonical sets, execute median-based imputations grouped by customer segment, rectify delivery dates, and drop duplicate records.
3. **Feature Engineering:** Calculate delivery cycle times, profit margins, and cumulative customer lifetime spend.
4. **Statistical Summarization:** Compute comprehensive parametric and non-parametric summary statistics (mean, median, mode, standard deviation, variance, IQR, percentiles, skewness).
5. **Outlier Classification:** Differentiate between enterprise bulk procurement orders and corrupt data entries using IQR fences.
6. **Executive Dashboarding:** Deliver an intuitive web UI allowing stakeholders to interactively filter data, inspect code snippets, view outputs, and download cleaned datasets.

### 2.3 User Classes and Characteristics
- **Business Executives / Store Managers:** Require high-level summary KPIs, regional performance comparisons, category margin insights, and plain-business summaries.
- **Data Analysts / Engineers:** Require statistical distributions, code snippets, reproducible transformation logs, and clean CSV exports.
- **Academic Evaluators:** Require strict adherence to project objectives, rubrics, testing suites, and methodology justifications.

### 2.4 Operating Environment
- **Operating System:** macOS / Linux / Windows.
- **Python Runtime:** Python 3.10 or later (tested on Python 3.14).
- **Core Libraries:** pandas, numpy, matplotlib, seaborn, streamlit, plotly, pytest, openpyxl, tabulate.

---

## 3. Specific Requirements

### 3.1 Functional Requirements

#### FR-1: Data Ingestion and Validation
- **FR-1.1:** The system shall read `retail_customer_sales_dataset.csv` encoding 24 distinct columns.
- **FR-1.2:** The system shall validate column naming and notify when required fields are missing.

#### FR-2: Data Quality Audit
- **FR-2.1:** The system shall quantify missing values per column as both absolute counts and percentages.
- **FR-2.2:** The system shall identify exact duplicate records.
- **FR-2.3:** The system shall flag casing and typographical inconsistencies in `Gender` and `Region`.
- **FR-2.4:** The system shall detect out-of-range numerical values (`Age <= 0` or `Age > 100`, `Discount < 0` or `Discount > 0.50`).
- **FR-2.5:** The system shall identify chronological anomalies where `Delivery_Date < Order_Date`.

#### FR-3: Data Cleaning and Standardization
- **FR-3.1:** The system shall map all variants of Gender to canonical values `Male` or `Female`.
- **FR-3.2:** The system shall map all variants of Region to `North`, `South`, `East`, or `West`.
- **FR-3.3:** The system shall impute missing `Age` and `Income` using the median of the respective `Customer_Segment`.
- **FR-3.4:** The system shall reconcile invalid or missing `Delivery_Date` values using `Order_Date` plus modal delivery turnaround times (Same-Day: 0 days, Express: 2 days, Standard: 5 days).
- **FR-3.5:** The system shall deduplicate transaction records, ensuring unique records in the clean dataset.
- **FR-3.6:** The system shall save the sanitized data to `data/processed/cleaned_retail_sales_dataset.csv`.

#### FR-4: Feature Engineering
- **FR-4.1:** The system shall compute `Delivery_Days = Delivery_Date - Order_Date`.
- **FR-4.2:** The system shall compute `Profit_Margin = (Profit / Sales) * 100`.
- **FR-4.3:** The system shall compute `Revenue_per_Customer` as cumulative spend per `Customer_ID`.
- **FR-4.4:** The system shall derive temporal attributes (`Order_Year`, `Order_Month`, `Order_Quarter`, `Order_DayOfWeek`).

#### FR-5: Statistical & Univariate Analysis
- **FR-5.1:** The system shall compute Mean, Median, Mode, Standard Deviation, Variance, Min, Max, Q1, Q2, Q3, and IQR for all 8 key continuous features.
- **FR-5.2:** The system shall quantify skewness for `Sales`, `Income`, and `Age`, providing automated qualitative business interpretations.
- **FR-5.3:** The system shall compute frequency tables and percentage proportions for all categorical fields.

#### FR-6: Outlier Detection and Classification
- **FR-6.1:** The system shall calculate upper and lower IQR fences ($Q_1 - 1.5 \times \text{IQR}$, $Q_3 + 1.5 \times \text{IQR}$) for `Sales`, `Profit`, `Income`, and `Age`.
- **FR-6.2:** The system shall compute Z-scores ($|Z| > 3.0$) for validation.
- **FR-6.3:** The system shall categorize commercial high-sales orders as legitimate enterprise orders rather than measurement errors.

#### FR-7: Business Query Solutions
- **FR-7.1:** The system shall aggregate and display Regional AOV and revenue.
- **FR-7.2:** The system shall compute product category profitability rankings.
- **FR-7.3:** The system shall compute return rates across segments and shipping modes.
- **FR-7.4:** The system shall analyze the relationship between fulfillment turnaround and satisfaction ratings.

#### FR-8: Interactive Web Application (Streamlit)
- **FR-8.1:** The system shall host an interactive dashboard reachable via local browser.
- **FR-8.2:** The system shall present dynamic KPI metrics, interactive Plotly charts, data audit comparison tables, code snippet inspectors, and clean dataset export.

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements
- Ingestion, audit, cleaning, and metric calculation for 7,000+ records shall complete in under **2.5 seconds** on modern commodity hardware.
- Streamlit dashboard tabs shall render reactively without page freezing.

### 4.2 Reliability & Idempotency
- The cleaning pipeline shall be deterministic and idempotent: running the cleaning script multiple times on the same input must yield identical processed outputs without side-effects.

### 4.3 Maintainability & Modularity
- Source code shall be structured into distinct single-responsibility modules (`data_loader`, `data_auditor`, `data_cleaner`, `feature_engineering`, `outlier_detector`, `eda_analyzer`, `visualizer`).
- Codebase shall adhere to PEP 8 style standards with explicit type annotations and docstrings.

### 4.4 Portability
- The solution shall operate in standard virtual environments without native binary platform locks.

---

## 5. Verification & Acceptance Criteria
- 100% of unit tests and integration tests passing in `pytest`.
- Zero missing values and zero duplicate records in `cleaned_retail_sales_dataset.csv`.
- Generation of 12 distinct 300-DPI visual artifacts in `eda_summary/figures/`.
- Streamlit dashboard operational with zero runtime exceptions.
