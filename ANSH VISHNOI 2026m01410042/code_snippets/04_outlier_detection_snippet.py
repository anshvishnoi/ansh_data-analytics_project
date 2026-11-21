"""
Code Snippet 04: Outlier Detection (IQR & Z-Score)
Demonstrates statistical outlier fence detection on Sales and Profit.
"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/processed/cleaned_retail_sales_dataset.csv")

def detect_iqr(series, name):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_fence = q1 - (1.5 * iqr)
    upper_fence = q3 + (1.5 * iqr)
    outliers = series[(series < lower_fence) | (series > upper_fence)]
    print(f"=== {name} IQR Outlier Analysis ===")
    print(f"Q1 (25%): ₹{q1:,.2f} | Q3 (75%): ₹{q3:,.2f} | IQR: ₹{iqr:,.2f}")
    print(f"Lower Fence: ₹{lower_fence:,.2f} | Upper Fence: ₹{upper_fence:,.2f}")
    print(f"Outliers Count: {len(outliers)} ({len(outliers) / len(series) * 100:.2f}%)\n")

detect_iqr(df["Sales"], "Sales")
detect_iqr(df["Profit"], "Profit")
detect_iqr(df["Income"], "Income")
