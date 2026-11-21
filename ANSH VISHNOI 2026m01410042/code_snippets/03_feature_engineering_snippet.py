"""
Code Snippet 03: Feature Engineering
Demonstrates calculation of Delivery_Days, Profit_Margin, and Revenue_per_Customer.
"""

import pandas as pd

# 1. Load cleaned data
df = pd.read_csv("data/processed/cleaned_retail_sales_dataset.csv", parse_dates=["Order_Date", "Delivery_Date"])

# 2. Delivery_Days
df["Delivery_Days"] = (df["Delivery_Date"] - df["Order_Date"]).dt.days
print("Delivery_Days summary:")
print(df["Delivery_Days"].describe())

# 3. Profit_Margin (%)
df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100
print("\nProfit_Margin (%) summary:")
print(df["Profit_Margin"].describe())

# 4. Revenue_per_Customer (Customer Lifetime Value)
df["Revenue_per_Customer"] = df.groupby("Customer_ID")["Sales"].transform("sum")
print("\nRevenue_per_Customer sample:")
print(df[["Customer_ID", "Sales", "Revenue_per_Customer"]].head(5))
