# 🌐 Interactive Streamlit Web Application (`app/`)

## Overview
This directory houses the presentation layer of the Retail Customer Sales EDA System. The application provides an interactive decision dashboard, quality audit lab, statistical explorer, outlier isolation studio, and business strategy query tools.

## Architecture & Tabs
1. **📊 Executive Dashboard**: High-level KPIs, 2-year monthly revenue & profit trajectory, regional sales comparison, and customer segment revenue bars.
2. **🔍 Data Quality Audit Lab**: Side-by-side audit comparison between raw (`7,084` rows) and cleaned (`7,002` rows) datasets, missing values audit, category normalization, and justification log.
3. **📈 Statistical & Univariate Explorer**: Tabular summary statistics (mean, median, mode, std, variance, IQR, skewness) and interactive distribution histograms with KDE overlays.
4. **🎯 Outlier Studio**: Interactive IQR and Z-score outlier detection engine with dynamic fences and domain classification of corporate bulk purchases.
5. **💼 Business Questions & GroupBy**: Detailed solutions and executive recommendations for the 5 mandated business questions + interactive custom groupby builder.
6. **⚙️ Feature Engineering & Export**: Live view of calculated columns (`Delivery_Days`, `Profit_Margin`, `Revenue_per_Customer`, etc.) with a 1-click Download button for `cleaned_retail_sales_dataset.csv`.
7. **📄 SRS & Documents**: Embedded live viewer for the formal SRS, Business Insights Report, Project Summary, and Data Dictionary.
8. **💻 Code & Output Snippets**: Code review gallery showing standalone modular scripts alongside their verified terminal execution logs.

## How to Launch the Application
From the workspace root directory:
```bash
./run_app.sh
```
or directly via Streamlit:
```bash
.venv/bin/streamlit run app/main.py
```
