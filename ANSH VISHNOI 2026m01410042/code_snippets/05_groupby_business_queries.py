"""
Code Snippet 05: GroupBy Business Queries
Demonstrates answering the 5 business questions using pandas groupby aggregations.
"""

import pandas as pd

df = pd.read_csv("data/processed/cleaned_retail_sales_dataset.csv")

print("=== Q1: Regional Performance & AOV ===")
q1 = df.groupby("Region").agg(
    Total_Sales=("Sales", "sum"),
    Order_Count=("Transaction_ID", "count"),
    Average_Order_Value=("Sales", "mean")
).round(2)
print(q1)

print("\n=== Q2: Category Profit Margins ===")
q2 = df.groupby("Product_Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum")
)
q2["Margin_Pct"] = ((q2["Total_Profit"] / q2["Total_Sales"]) * 100).round(2)
print(q2.sort_values(by="Margin_Pct", ascending=False))

print("\n=== Q3: Customer Segment Lifetime Revenue ===")
q3 = df.groupby("Customer_Segment").agg(
    Customers=("Customer_ID", "nunique"),
    Total_Sales=("Sales", "sum"),
    AOV=("Sales", "mean")
).round(2)
q3["Revenue_per_Customer"] = (q3["Total_Sales"] / q3["Customers"]).round(2)
print(q3)

print("\n=== Q4: Return Rates by Segment and Mode ===")
q4 = df.groupby(["Customer_Segment", "Delivery_Mode"]).agg(
    Total_Orders=("Transaction_ID", "count"),
    Returns=("Returned", lambda x: (x == "Yes").sum())
)
q4["Return_Rate_%"] = ((q4["Returns"] / q4["Total_Orders"]) * 100).round(2)
print(q4)
