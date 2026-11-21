"""
Code Snippet 01: Data Quality Audit
Demonstrates how to audit missing values, duplicates, and categorical inconsistencies.
"""

import pandas as pd

# 1. Load raw dataset
df = pd.read_csv("data/raw/retail_customer_sales_dataset.csv")

print("=== 1. MISSING VALUES AUDIT ===")
nulls = df.isnull().sum()
null_pct = (nulls / len(df)) * 100
missing_report = pd.DataFrame({"Missing_Count": nulls, "Missing_Pct": null_pct.round(2)})
print(missing_report[missing_report["Missing_Count"] > 0])

print("\n=== 2. DUPLICATE ROWS AUDIT ===")
dup_count = df.duplicated().sum()
print(f"Total Duplicate Rows Found: {dup_count} ({(dup_count / len(df)) * 100:.2f}%)")

print("\n=== 3. CATEGORICAL INCONSISTENCIES (GENDER & REGION) ===")
print("Gender Unique Values:")
print(df["Gender"].value_counts(dropna=False))
print("\nRegion Unique Values:")
print(df["Region"].value_counts(dropna=False))
