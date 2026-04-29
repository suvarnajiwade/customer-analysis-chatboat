"""
data_loader.py
--------------
Handles loading, cleaning, and context preparation of the customer Excel data.
"""

import pandas as pd
import os
from typing import Tuple, Optional
from config import DEFAULT_DATA_FILE, SCHEMA_SAMPLE_ROWS

def load_data(file_path: str = DEFAULT_DATA_FILE) -> pd.DataFrame:
    """
    Loads and cleans the Excel data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    # Load Excel file
    df = pd.read_excel(file_path)

    # Clean column names (remove whitespace, ensure they are strings)
    df.columns = [str(col).strip() for col in df.columns]

    # Clean string data
    for col in df.select_dtypes(include=['object']):
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Optional: Convert dates if needed for time-based queries
    # 'Expected Possession' (e.g., "Jun 2026")
    # 'Last Call Connected Time' (e.g., "28-02-2026 04:50")
    
    return df

def get_dataframe_context(df: pd.DataFrame) -> str:
    """
    Generates a descriptive context of the DataFrame for the LLM.
    Includes columns, data types, and sample rows.
    """
    # Get column names and types
    schema_info = []
    for col, dtype in df.dtypes.items():
        # Get unique values for categorical-like columns to help LLM understand options
        unique_vals = ""
        if df[col].nunique() < 10:
             unique_vals = f" (Unique values: {', '.join(map(str, df[col].unique()))})"
        
        schema_info.append(f"- {col} ({dtype}){unique_vals}")
    
    schema_str = "\n".join(schema_info)
    
    # Get sample data
    sample_data = df.head(SCHEMA_SAMPLE_ROWS).to_string()
    
    context = f"""
TABLE_SCHEMA:
{schema_str}

SAMPLE_ROWS (First {SCHEMA_SAMPLE_ROWS}):
{sample_data}

TOTAL_ROWS: {len(df)}
"""
    return context

if __name__ == "__main__":
    # Test loading
    try:
        data = load_data()
        print("Data Loaded Successfully!")
        print(f"Shape: {data.shape}")
        print("\n--- Model Context Preview ---")
        print(get_dataframe_context(data))
    except Exception as e:
        print(f"Error: {e}")
