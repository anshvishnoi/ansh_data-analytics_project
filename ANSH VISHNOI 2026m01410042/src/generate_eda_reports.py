"""
Report Generation Script
Generates markdown documentation for data quality audit, cleaning justifications,
and business groupby answers.
"""

from pathlib import Path
import pandas as pd
from src.data_loader import load_raw_data, load_cleaned_data
from src.data_auditor import DataQualityAuditor
from src.data_cleaner import DataCleaner
from src.eda_analyzer import EDAAnalyzer


def main():
    raw_df = load_raw_data()
    auditor = DataQualityAuditor(raw_df)
    audit_results = auditor.run_full_audit()

    cleaner = DataCleaner(raw_df)
    clean_df, log_df = cleaner.clean_dataset()

    eda = EDAAnalyzer(clean_df)
    biz_answers = eda.answer_business_questions()

    out_dir = Path("eda_summary")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Cleaning Justifications
    with open(out_dir / "cleaning_justifications.md", "w", encoding="utf-8") as f:
        f.write("# 🛠️ Data Cleaning Decisions & Justifications Report\n\n")
        f.write("This document details every cleaning decision executed on `retail_customer_sales_dataset.csv` in strict compliance with Section 3.3 of the Project 1 specification.\n\n")
        f.write("| Step | Action | Business & Mathematical Justification | Records Affected |\n")
        f.write("|:---|:---|:---|:---:|\n")
        for _, row in log_df.iterrows():
            f.write(f"| **{row['Step']}** | {row['Action']} | {row['Justification']} | `{row['Affected_Records']}` |\n")

    # 2. Data Quality Audit Report
    with open(out_dir / "data_quality_audit_report.md", "w", encoding="utf-8") as f:
        f.write("# 🔍 Comprehensive Data Quality Audit Report\n\n")
        f.write(f"**Dataset Analyzed**: `retail_customer_sales_dataset.csv`  \n")
        f.write(f"**Initial Row Count**: {audit_results['total_records']} | **Total Columns**: {audit_results['total_columns']}\n\n")
        f.write("## 1. Missing Values Breakdown\n\n")
        f.write("| Column | Missing Count | Missing Percentage (%) | Stored Type |\n|:---|:---:|:---:|:---:|\n")
        for _, row in audit_results["missing_values_summary"].iterrows():
            f.write(f"| `{row['Column']}` | {row['Missing_Count']} | {row['Missing_Percentage']:.2f}% | `{row['Data_Type']}` |\n")
        f.write("\n## 2. Duplicate Records\n\n")
        f.write(f"- Total duplicate rows found: **{audit_results['duplicates']['duplicate_count']}** ({audit_results['duplicates']['duplicate_percentage']:.2f}% of raw rows)\n")
        f.write("\n## 3. Categorical Inconsistencies\n\n")
        f.write("### Gender Inconsistencies:\n")
        for k, v in audit_results["categorical_inconsistencies"]["gender_anomalies"].items():
            f.write(f"- `{k}`: {v} occurrences\n")
        f.write("\n### Region Inconsistencies:\n")
        for k, v in audit_results["categorical_inconsistencies"]["region_anomalies"].items():
            f.write(f"- `{k}`: {v} occurrences\n")
        f.write("\n## 4. Range and Date Integrity Anomalies\n\n")
        f.write(f"- **Impossible Ages**: {audit_results['numerical_range_anomalies']['age']['negative_or_zero_count']} negative/zero, {audit_results['numerical_range_anomalies']['age']['extreme_high_count']} above 100 yrs (Range: {audit_results['numerical_range_anomalies']['age']['min_found']} to {audit_results['numerical_range_anomalies']['age']['max_found']})\n")
        f.write(f"- **Invalid Discounts**: {audit_results['numerical_range_anomalies']['discount']['negative_discount_count']} negative, {audit_results['numerical_range_anomalies']['discount']['exceeds_threshold_count']} above 0.50 (Range: {audit_results['numerical_range_anomalies']['discount']['min_found']} to {audit_results['numerical_range_anomalies']['discount']['max_found']})\n")
        f.write(f"- **Chronological Inconsistencies**: {audit_results['date_integrity']['negative_delivery_duration_count']} rows where `Delivery_Date < Order_Date`\n")

    # 3. Business Questions Answers
    with open(out_dir / "business_questions_answers.md", "w", encoding="utf-8") as f:
        f.write("# 💼 Core Business Questions Answered via GroupBy Aggregation\n\n")
        for key, q in biz_answers.items():
            f.write(f"## {q['title']}\n\n")
            f.write(f"**Key Analytical Finding**: {q['key_finding']}\n\n")
            f.write(f"**Strategic Recommendation**: {q['strategic_recommendation']}\n\n")
            f.write("### Aggregated Data Table:\n\n")
            f.write(q["data"].to_markdown(index=False))
            f.write("\n\n---\n\n")

    print("Successfully generated all eda_summary reports!")


if __name__ == "__main__":
    main()
