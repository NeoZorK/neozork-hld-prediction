# -*- coding: utf-8 -*-
# src/eda/data_overview.py

import pandas as pd
from typing import Optional, Tuple, List

def load_data(file_path: str, file_type: str = "parquet") -> pd.DataFrame:
    """
    Loads a dataframe from a parquet or csv file.

    Args:
        file_path (str): Path to the file.
        file_type (str): Type of file: 'parquet' or 'csv'.

    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    if file_type == "parquet":
        df = pd.read_parquet(file_path)
    elif file_type == "csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file_type. Use 'parquet' or 'csv'.")
    return df

def show_basic_info(df: pd.DataFrame) -> None:
    """
    Prints basic info about the dataframe: shape, columns, dtypes, memory usage.

    Args:
        df (pd.DataFrame): Dataframe to inspect.
    """
    print("=== DataFrame shape ===")
    print(df.shape)
    print("\n=== DataFrame columns ===")
    print(df.columns.tolist())
    print("\n=== DataFrame dtypes ===")
    print(df.dtypes)
    print("\n=== DataFrame memory usage (MB) ===")
    print(df.memory_usage(deep=True).sum() / 1024 ** 2)

def show_head(df: pd.DataFrame, n: int = 5) -> None:
    """
    Prints first n rows of the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to inspect.
        n (int): Number of rows to show.
    """
    print(f"\n=== First {n} rows ===")
    print(df.head(n))

def check_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Checks for missing values in the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to check.

    Returns:
        pd.Series: Number of missing values per column.
    """
    missing = df.isnull().sum()
    print("\n=== Missing values per column ===")
    print(missing[missing > 0])
    return missing

def check_duplicates(df: pd.DataFrame) -> int:
    """
    Checks for duplicate rows in the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to check.

    Returns:
        int: Number of duplicate rows.
    """
    num_duplicates = df.duplicated().sum()
    print(f"\n=== Number of duplicate rows: {num_duplicates} ===")
    return num_duplicates

def get_column_types(df: pd.DataFrame) -> pd.Series:
    """
    Returns the types of columns in the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to inspect.

    Returns:
        pd.Series: Column types.
    """
    types = df.dtypes
    print("\n=== Column types ===")
    print(types)
    return types

def get_nan_columns(df: pd.DataFrame) -> List[str]:
    """
    Returns a list of columns with missing values.

    Args:
        df (pd.DataFrame): Dataframe to inspect.

    Returns:
        List[str]: List of column names with NaNs.
    """
    nan_cols = df.columns[df.isnull().any()].tolist()
    print("\n=== Columns with NaN values ===")
    print(nan_cols)
    return nan_cols

def get_summary(df: pd.DataFrame) -> None:
    """
    Prints summary statistics for numeric columns.

    Args:
        df (pd.DataFrame): Dataframe to summarize.
    """
    print("\n=== Statistical summary for numeric columns ===")
    print(df.describe())