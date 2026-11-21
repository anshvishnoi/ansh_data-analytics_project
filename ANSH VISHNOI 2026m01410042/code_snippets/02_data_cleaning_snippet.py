"""
Code Snippet 02: Data Cleaning & Normalization
Demonstrates category mapping, median imputation, and chronological date resolution.
"""

import pandas as pd
import numpy as np

# 1. Load dataset
df = pd.read_csv("data/raw/retail_customer_sales_dataset.csv")

# 2. Drop duplicates
initial_len = len(df)
df = df.drop_duplicates()
print(f"Dropped {initial_len - len(df)} duplicate records.")

# 3. Standardize Gender & Region
gender_map = {
    "Male": "Male", "male": "Male", "MALE": "Male", "M": "Male",
    "Female": "Female", "female": "Female", "FEMALE": "Female", "F": "Female"
}
df["Gender"] = df["Gender"].map(gender_map).fillna(df["Gender"])

region_map = {
    "West": "West", "west": "West", "WEST": "West",
    "East": "East", "east": "East",
    "South": "South", "south": "South", "Sth": "South",
    "North": "North", "north": "North", "NORTH": "North", "Nort": "North"
}
df["Region"] = df["Region"].map(region_map).fillna(df["Region"])

# 4. Correct Impossible Numerical Values
df.loc[(df["Age"] <= 0) | (df["Age"] > 100), "Age"] = np.nan
df.loc[(df["Discount"] < 0) | (df["Discount"] > 0.5), "Discount"] = np.nan

# 5. Median Imputation
df["Age"] = df.groupby("Customer_Segment")["Age"].transform(lambda x: x.fillna(x.median()))
df["Income"] = df.groupby("Customer_Segment")["Income"].transform(lambda x: x.fillna(x.median()))
df["Discount"] = df["Discount"].fillna(df["Discount"].median())

# 6. Parse and Reconcile Dates
df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="mixed")
df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"], format="mixed")

# Fix Delivery_Date < Order_Date
invalid_dates = df["Delivery_Date"].isna() | (df["Delivery_Date"] < df["Order_Date"])
mode_offsets = {"Same-Day": 0, "Express": 2, "Standard": 5}
for mode, days in mode_offsets.items():
    mask = invalid_dates & (df["Delivery_Mode"] == mode)
    df.loc[mask, "Delivery_Date"] = df.loc[mask, "Order_Date"] + pd.Timedelta(days=days)

print(f"Cleaning completed! Clean dataset rows: {len(df)}")
print("Remaining null values across all columns:", df.isnull().sum().sum())
