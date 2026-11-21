# 📖 Data Dictionary & Feature Specification

This document details the metadata, data types, physical constraints, and business descriptions for all attributes present in the Retail Customer Sales dataset (both original raw fields and engineered analytical features).

---

## 1. Raw Dataset Attributes (24 Columns)

| Column Name | Physical Type | Logical Domain | Nullable? | Description & Business Rules |
|:---|:---:|:---:|:---:|:---|
| **`Transaction_ID`** | String | Alphanumeric (e.g. `TXN205933`) | No | Unique identifier for each transaction order. Primary key. |
| **`Customer_ID`** | String | Alphanumeric (e.g. `CUST10816`) | No | Unique customer identifier. Repeats across multiple customer orders. |
| **`Order_Date`** | Datetime | YYYY-MM-DD | No | Date when the customer placed the order (2023–2024). |
| **`Delivery_Date`** | Datetime | YYYY-MM-DD | Reconciled | Date when order was delivered. Must be $\ge$ `Order_Date`. |
| **`Age`** | Float | 18.0 to 80.0 | Imputed | Customer age in years. Outliers (<0 or >100) corrected to median. |
| **`Gender`** | String | `Male`, `Female` | No | Customer gender. Standardized from casing variants. |
| **`Income`** | Float | Positive Currency (₹) | Imputed | Annual income of customer. Right-skewed distribution. |
| **`Region`** | String | `North`, `South`, `East`, `West` | No | Macro-geographical operating zone in India. Standardized from abbreviations. |
| **`State`** | String | Indian State names | No | State corresponding to the customer's shipping address. |
| **`City`** | String | Indian City names | No | City corresponding to the customer's shipping address. |
| **`Customer_Segment`** | String | `Consumer`, `Corporate`, `Home Office` | No | Customer classification based on purchasing profile. |
| **`Product_Category`** | String | 5 Categories | No | `Electronics`, `Grocery`, `Clothing`, `Furniture`, `Office Supplies`. |
| **`Product`** | String | Product Name | No | Specific item purchased within category (e.g. `LED Monitor`, `Honey Jar`). |
| **`Quantity`** | Integer | 1 to 10 units | No | Total quantity of item purchased in this transaction. |
| **`Unit_Price`** | Float | Positive Currency (₹) | No | Base selling price per individual unit. |
| **`Discount`** | Float | 0.00 to 0.50 | Imputed | Promotional discount proportion applied to the order. |
| **`Sales`** | Float | Positive Currency (₹) | No | Final order transaction value: $\text{Quantity} \times \text{Unit\_Price} \times (1 - \text{Discount})$. |
| **`Cost`** | Float | Positive Currency (₹) | No | Direct cost of goods sold (COGS) incurred to supply the order. |
| **`Profit`** | Float | Currency (₹) | No | Net gross profit realized: $\text{Sales} - \text{Cost}$. |
| **`Payment_Method`** | String | 5 Methods | No | `Net Banking`, `Debit Card`, `UPI`, `Cash on Delivery`, `Credit Card`. |
| **`Delivery_Mode`** | String | 3 Modes | No | `Standard`, `Express`, `Same-Day`. Determines transit turnaround. |
| **`Customer_Rating`** | Float | Ordinal (1.0 to 5.0) | Flagged | Numerical review score provided by the customer. |
| **`Satisfaction_Level`**| String | `Low`, `Medium`, `High` | Imputed | Sentiment rating corresponding to review score. |
| **`Returned`** | String | `Yes`, `No` | No | Binary flag indicating if order was subsequently returned. |

---

## 2. Engineered Analytical Features

| Feature Name | Derived Formula | Type | Business Utility |
|:---|:---|:---:|:---|
| **`Delivery_Days`** | `(Delivery_Date - Order_Date).dt.days` | Integer | Measures order fulfillment cycle time and logistics speed. |
| **`Profit_Margin`** | `(Profit / Sales) * 100` | Float (%) | Standardized percentage margin evaluating product capital profitability. |
| **`Revenue_per_Customer`**| `df.groupby('Customer_ID')['Sales'].transform('sum')` | Float (₹) | Cumulative customer lifetime spending value (CLV proxy). |
| **`Customer_Order_Count`**| `df.groupby('Customer_ID')['Transaction_ID'].transform('count')` | Integer | Total order frequency per individual customer. |
| **`Discount_Amount`** | `Quantity * Unit_Price * Discount` | Float (₹) | Exact rupee savings provided to the customer during checkout. |
| **`Order_Year`** | `Order_Date.dt.year` | Integer | Annual temporal cohort indicator (2023 vs 2024). |
| **`Order_Month`** | `Order_Date.dt.month` | Integer | Monthly seasonality tracker (1 to 12). |
| **`Order_YearMonth`** | `Order_Date.dt.to_period('M')` | String | Continuous monthly timeline string for longitudinal analysis. |
| **`Order_Quarter`** | `'Q' + Order_Date.dt.quarter` | String | Fiscal quarterly reporting tag (Q1, Q2, Q3, Q4). |
| **`Delivery_SLA_Status`** | SLA mapping based on `Delivery_Mode` | String | Flags whether shipment arrived within expected delivery window. |
