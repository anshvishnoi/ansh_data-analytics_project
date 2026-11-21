"""
Pytest Test Fixtures and Configuration
"""

import pandas as pd
import pytest


@pytest.fixture
def mock_raw_dataframe():
    """
    Creates a small controlled DataFrame mimicking raw anomalies.
    """
    data = {
        "Transaction_ID": ["TXN101", "TXN102", "TXN103", "TXN104", "TXN101"],  # Duplicate TXN101
        "Customer_ID": ["CUST1", "CUST2", "CUST1", "CUST3", "CUST1"],
        "Order_Date": ["2023-01-10", "2023-02-15", "2023-03-20", "2023-04-05", "2023-01-10"],
        "Delivery_Date": ["2023-01-08", "2023-02-18", None, "2023-04-10", "2023-01-08"],  # TXN101 delivery < order
        "Age": [28.0, -5.0, 999.0, None, 28.0],  # Anomalous ages
        "Gender": ["Male", "female", "M", "FEMALE", "Male"],  # Casing issues
        "Income": [55000.0, None, 120000.0, 48000.0, 55000.0],
        "Region": ["West", "west", "Nort", "South", "West"],  # Casing/abbreviation issues
        "State": ["Maharashtra", "Maharashtra", "Delhi", "Karnataka", "Maharashtra"],
        "City": ["Mumbai", "Pune", "Delhi", "Bengaluru", "Mumbai"],
        "Customer_Segment": ["Consumer", "Corporate", "Corporate", "Home Office", "Consumer"],
        "Product_Category": ["Electronics", "Clothing", "Office Supplies", "Furniture", "Electronics"],
        "Product": ["Wireless Mouse", "Formal Shirt", "Paper Ream", "Office Chair", "Wireless Mouse"],
        "Quantity": [2, 1, 5, 1, 2],
        "Unit_Price": [1200.0, 2500.0, 400.0, 8500.0, 1200.0],
        "Discount": [0.10, 1.50, -0.10, None, 0.10],  # Out of range discounts
        "Sales": [2160.0, 2500.0, 2000.0, 8500.0, 2160.0],
        "Cost": [1500.0, 1800.0, 1400.0, 6000.0, 1500.0],
        "Profit": [660.0, 700.0, 600.0, 2500.0, 660.0],
        "Payment_Method": ["Credit Card", "UPI", "Debit Card", "Net Banking", "Credit Card"],
        "Delivery_Mode": ["Standard", "Express", "Standard", "Same-Day", "Standard"],
        "Customer_Rating": [4.0, None, 5.0, 2.0, 4.0],
        "Satisfaction_Level": ["High", None, "High", "Low", "High"],
        "Returned": ["No", "No", "No", "Yes", "No"]
    }
    return pd.DataFrame(data)
