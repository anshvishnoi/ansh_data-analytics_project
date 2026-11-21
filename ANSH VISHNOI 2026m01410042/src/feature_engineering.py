"""
Feature Engineering Module
Creates calculated columns strictly aligned with Project 1 specifications:
- Delivery_Days = Delivery_Date - Order_Date
- Profit_Margin = (Profit / Sales) * 100
- Revenue_per_Customer = Cumulative Sales per Customer_ID
- Discount_Amount = Total money discounted
- Temporal features (Order_Year, Order_Month, Order_Quarter)
- Delivery_Status classification
"""

import pandas as pd


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies feature engineering transformations to the cleaned dataset.
    
    Args:
        df: Cleaned pandas DataFrame with parsed datetime Order_Date and Delivery_Date.
        
    Returns:
        pd.DataFrame: DataFrame augmented with calculated columns.
    """
    df = df.copy()

    # Ensure datetime format
    if not pd.api.types.is_datetime64_any_dtype(df["Order_Date"]):
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="mixed")
    if not pd.api.types.is_datetime64_any_dtype(df["Delivery_Date"]):
        df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"], format="mixed")

    # 1. Delivery_Days (in days)
    df["Delivery_Days"] = (df["Delivery_Date"] - df["Order_Date"]).dt.days
    # Ensure non-negative delivery days
    df["Delivery_Days"] = df["Delivery_Days"].clip(lower=0)

    # 2. Profit_Margin (as percentage)
    # Avoid zero division
    df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, 1e-6)) * 100.0
    df["Profit_Margin"] = df["Profit_Margin"].round(2)

    # 3. Revenue_per_Customer (Customer Lifetime Value / Total Spend)
    customer_revenue = df.groupby("Customer_ID")["Sales"].transform("sum")
    df["Revenue_per_Customer"] = customer_revenue.round(2)

    # 4. Customer_Order_Count (Number of orders placed by customer)
    customer_order_cnt = df.groupby("Customer_ID")["Transaction_ID"].transform("count")
    df["Customer_Order_Count"] = customer_order_cnt

    # 5. Discount_Amount (Total rupee discount given on this order)
    df["Discount_Amount"] = (df["Quantity"] * df["Unit_Price"] * df["Discount"]).round(2)

    # 6. Temporal Features
    df["Order_Year"] = df["Order_Date"].dt.year
    df["Order_Month"] = df["Order_Date"].dt.month
    df["Order_YearMonth"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Order_Quarter"] = "Q" + df["Order_Date"].dt.quarter.astype(str)
    df["Order_DayOfWeek"] = df["Order_Date"].dt.day_name()

    # 7. Delivery SLA Category
    def classify_sla(row):
        days = row["Delivery_Days"]
        mode = row["Delivery_Mode"]
        if mode == "Same-Day":
            return "Met SLA" if days <= 0 else "Delayed"
        elif mode == "Express":
            return "Met SLA" if days <= 2 else "Delayed"
        else:  # Standard
            return "Met SLA" if days <= 5 else "Delayed"

    df["Delivery_SLA_Status"] = df.apply(classify_sla, axis=1)

    return df
