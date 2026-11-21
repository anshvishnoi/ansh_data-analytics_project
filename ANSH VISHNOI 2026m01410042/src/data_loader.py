"""
Data Loader Module
Responsible for reading raw and processed datasets with validation.
"""

from pathlib import Path
from typing import Optional, Union
import pandas as pd


def load_raw_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads the raw retail customer sales dataset from disk.
    
    Args:
        filepath: Path to the CSV file. If None, defaults to 'data/raw/retail_customer_sales_dataset.csv'.
        
    Returns:
        pd.DataFrame: Raw uncleaned dataset.
    """
    if filepath is None:
        filepath = Path("data/raw/retail_customer_sales_dataset.csv")
    else:
        filepath = Path(filepath)

    if not filepath.exists():
        # Fallback to local root if running from other directories
        alt_path = Path("retail_customer_sales_dataset.csv")
        if alt_path.exists():
            filepath = alt_path
        else:
            raise FileNotFoundError(f"Dataset file not found at {filepath} or {alt_path}")

    df = pd.read_csv(filepath)
    return df


def load_cleaned_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads the cleaned and feature-engineered dataset.
    
    Args:
        filepath: Path to cleaned CSV file. Defaults to 'data/processed/cleaned_retail_sales_dataset.csv'.
        
    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    if filepath is None:
        filepath = Path("data/processed/cleaned_retail_sales_dataset.csv")
    else:
        filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Cleaned dataset not found at {filepath}. Please run data_cleaner first.")

    df = pd.read_csv(filepath, parse_dates=["Order_Date", "Delivery_Date"])
    return df


def get_dataset_overview(df: pd.DataFrame) -> dict:
    """
    Generates a quick high-level overview dictionary of dataframe characteristics.
    """
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": df.columns.tolist(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "dtypes": df.dtypes.astype(str).to_dict()
    }
