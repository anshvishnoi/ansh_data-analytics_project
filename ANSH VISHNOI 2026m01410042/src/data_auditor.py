"""
Data Quality Auditor Module
Performs comprehensive data health and quality audit strictly aligned with
the specifications in Project 1 Exploratory Data Analysis.
"""

from typing import Any, Dict
import numpy as np
import pandas as pd


class DataQualityAuditor:
    """
    Audits a DataFrame for missing values, duplicates, categorical inconsistencies,
    numerical range anomalies, and date integrity conflicts.
    """

    def __init__(self, df: pd.DataFrame):
        self.raw_df = df.copy()
        self.total_rows = len(df)
        self.audit_results: Dict[str, Any] = {}

    def audit_missing_values(self) -> pd.DataFrame:
        """
        Calculates missing values count and percentage per column.
        """
        missing_count = self.raw_df.isnull().sum()
        missing_pct = (missing_count / self.total_rows) * 100.0
        missing_df = pd.DataFrame({
            "Column": self.raw_df.columns,
            "Missing_Count": missing_count.values,
            "Missing_Percentage": missing_pct.values,
            "Data_Type": [str(t) for t in self.raw_df.dtypes]
        }).sort_values(by="Missing_Count", ascending=False).reset_index(drop=True)
        
        self.audit_results["missing_values"] = missing_df
        return missing_df

    def audit_duplicates(self) -> Dict[str, Any]:
        """
        Identifies full duplicate rows in the dataset.
        """
        dup_mask = self.raw_df.duplicated()
        dup_count = int(dup_mask.sum())
        dup_pct = (dup_count / self.total_rows) * 100.0
        dup_sample = self.raw_df[dup_mask].head(5)
        
        result = {
            "duplicate_count": dup_count,
            "duplicate_percentage": round(dup_pct, 4),
            "sample_duplicates": dup_sample
        }
        self.audit_results["duplicates"] = result
        return result

    def audit_categorical_inconsistencies(self) -> Dict[str, Any]:
        """
        Audits inconsistent category spellings and casing in Gender, Region, etc.
        """
        gender_counts = self.raw_df["Gender"].value_counts(dropna=False).to_dict()
        region_counts = self.raw_df["Region"].value_counts(dropna=False).to_dict()
        
        # Expected canonical values
        canonical_genders = {"Male", "Female"}
        canonical_regions = {"North", "South", "East", "West"}
        
        gender_anomalies = {k: v for k, v in gender_counts.items() if k not in canonical_genders}
        region_anomalies = {k: v for k, v in region_counts.items() if k not in canonical_regions}
        
        result = {
            "gender_counts": gender_counts,
            "gender_anomalies": gender_anomalies,
            "region_counts": region_counts,
            "region_anomalies": region_anomalies,
        }
        self.audit_results["categorical_inconsistencies"] = result
        return result

    def audit_numerical_ranges(self) -> Dict[str, Any]:
        """
        Identifies impossible or out-of-range numerical values:
        - Negative Age or Age > 100
        - Discount < 0 or Discount > 0.5 (as per problem spec: Discount is a proportion 0-0.5)
        - Negative Quantity or Unit_Price
        - Sales calculation mismatch (Sales vs Quantity * Unit_Price * (1 - Discount))
        """
        anomalies = {}
        
        # Age checks
        valid_age_mask = self.raw_df["Age"].notnull()
        neg_age = (self.raw_df.loc[valid_age_mask, "Age"] <= 0).sum()
        extreme_age = (self.raw_df.loc[valid_age_mask, "Age"] > 100).sum()
        anomalies["age"] = {
            "negative_or_zero_count": int(neg_age),
            "extreme_high_count": int(extreme_age),
            "min_found": float(self.raw_df["Age"].min()),
            "max_found": float(self.raw_df["Age"].max()),
        }

        # Discount checks
        valid_disc_mask = self.raw_df["Discount"].notnull()
        neg_disc = (self.raw_df.loc[valid_disc_mask, "Discount"] < 0).sum()
        extreme_disc = (self.raw_df.loc[valid_disc_mask, "Discount"] > 0.5).sum()
        anomalies["discount"] = {
            "negative_discount_count": int(neg_disc),
            "exceeds_threshold_count": int(extreme_disc),
            "min_found": float(self.raw_df["Discount"].min()),
            "max_found": float(self.raw_df["Discount"].max()),
        }

        # Check Sales vs calculated approx
        sales_valid = self.raw_df.dropna(subset=["Quantity", "Unit_Price", "Discount", "Sales"])
        expected_sales = sales_valid["Quantity"] * sales_valid["Unit_Price"] * (1 - sales_valid["Discount"])
        sales_diff = np.abs(sales_valid["Sales"] - expected_sales)
        mismatch_count = (sales_diff > 2.0).sum()
        anomalies["sales_equation"] = {
            "sales_mismatch_count": int(mismatch_count),
            "max_sales_diff": float(sales_diff.max())
        }

        self.audit_results["numerical_ranges"] = anomalies
        return anomalies

    def audit_dates(self) -> Dict[str, Any]:
        """
        Identifies date format inconsistencies and cases where Delivery_Date is earlier than Order_Date.
        """
        # Parse dates with mixed formats
        order_dates = pd.to_datetime(self.raw_df["Order_Date"], format="mixed", errors="coerce")
        delivery_dates = pd.to_datetime(self.raw_df["Delivery_Date"], format="mixed", errors="coerce")

        unparseable_order = int(order_dates.isna().sum())
        unparseable_delivery = int(delivery_dates.isna().sum()) - int(self.raw_df["Delivery_Date"].isna().sum())

        # Contradiction: Delivery_Date < Order_Date
        valid_pair = order_dates.notnull() & delivery_dates.notnull()
        negative_duration_mask = valid_pair & (delivery_dates < order_dates)
        negative_duration_count = int(negative_duration_mask.sum())

        result = {
            "unparseable_order_dates": unparseable_order,
            "unparseable_delivery_dates": unparseable_delivery,
            "negative_delivery_duration_count": negative_duration_count,
            "earliest_order": str(order_dates.min().date()) if not order_dates.empty else None,
            "latest_order": str(order_dates.max().date()) if not order_dates.empty else None,
        }
        self.audit_results["date_integrity"] = result
        return result

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Executes all audit components and aggregates the summary.
        """
        missing_df = self.audit_missing_values()
        duplicates = self.audit_duplicates()
        categoricals = self.audit_categorical_inconsistencies()
        numericals = self.audit_numerical_ranges()
        dates = self.audit_dates()

        return {
            "total_records": self.total_rows,
            "total_columns": len(self.raw_df.columns),
            "missing_values_summary": missing_df[missing_df["Missing_Count"] > 0],
            "duplicates": duplicates,
            "categorical_inconsistencies": categoricals,
            "numerical_range_anomalies": numericals,
            "date_integrity": dates
        }


def generate_text_audit_report(audit_data: Dict[str, Any]) -> str:
    """
    Formats the audit results into a structured text report.
    """
    lines = [
        "=" * 70,
        "RETAIL CUSTOMER SALES DATASET - DATA QUALITY AUDIT REPORT",
        "=" * 70,
        f"Total Records Audited : {audit_data['total_records']}",
        f"Total Columns         : {audit_data['total_columns']}",
        "-" * 70,
        "1. MISSING VALUES AUDIT:",
    ]
    missing_df = audit_data["missing_values_summary"]
    for _, row in missing_df.iterrows():
        lines.append(
            f"   - {row['Column']:<20}: {int(row['Missing_Count']):>5} missing ({row['Missing_Percentage']:>5.2f}%) [{row['Data_Type']}]"
        )

    lines.extend([
        "-" * 70,
        "2. DUPLICATE RECORDS AUDIT:",
        f"   - Total Duplicates Found: {audit_data['duplicates']['duplicate_count']} rows "
        f"({audit_data['duplicates']['duplicate_percentage']:.2f}% of dataset)",
        "-" * 70,
        "3. CATEGORICAL INCONSISTENCY AUDIT:",
        "   - Gender Inconsistencies:",
    ])
    for val, cnt in audit_data["categorical_inconsistencies"]["gender_anomalies"].items():
        lines.append(f"       * '{val}': {cnt} occurrences")
    
    lines.append("   - Region Inconsistencies:")
    for val, cnt in audit_data["categorical_inconsistencies"]["region_anomalies"].items():
        lines.append(f"       * '{val}': {cnt} occurrences")

    lines.extend([
        "-" * 70,
        "4. NUMERICAL RANGE & LOGICAL ANOMALIES:",
        f"   - Age anomalies: {audit_data['numerical_range_anomalies']['age']['negative_or_zero_count']} negative/zero values, "
        f"{audit_data['numerical_range_anomalies']['age']['extreme_high_count']} values > 100 years. Range: [{audit_data['numerical_range_anomalies']['age']['min_found']}, {audit_data['numerical_range_anomalies']['age']['max_found']}]",
        f"   - Discount anomalies: {audit_data['numerical_range_anomalies']['discount']['negative_discount_count']} negative values, "
        f"{audit_data['numerical_range_anomalies']['discount']['exceeds_threshold_count']} values > 0.50. Range: [{audit_data['numerical_range_anomalies']['discount']['min_found']}, {audit_data['numerical_range_anomalies']['discount']['max_found']}]",
        "-" * 70,
        "5. DATE INTEGRITY ANOMALIES:",
        f"   - Delivery Date < Order Date (Negative Duration): {audit_data['date_integrity']['negative_delivery_duration_count']} rows",
        f"   - Order Date Range: {audit_data['date_integrity']['earliest_order']} to {audit_data['date_integrity']['latest_order']}",
        "=" * 70
    ])
    return "\n".join(lines)
