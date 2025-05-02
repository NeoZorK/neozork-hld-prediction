# -*- coding: utf-8 -*-
# scripts/eda_check_data_overview.py

import os
import pandas as pd
import numpy as np

from src.eda.data_overview import (
    load_data,
    show_basic_info,
    show_head,
    check_missing_values,
    check_duplicates,
    get_column_types,
    get_nan_columns,
    get_summary
)

def main():
    # Create a sample DataFrame
    df = pd.DataFrame({
        "open": [1.1, 2.2, np.nan, 4.4, 5.5],
        "high": [1.3, 2.4, 3.6, 4.9, 5.7],
        "low": [1.0, 2.0, 3.1, 4.2, 5.3],
        "close": [1.2, 2.3, 3.5, np.nan, 5.6],
        "volume": [100, 150, 120, 130, 160],
        "direction": ["up", "down", "up", "down", "up"]
    })

    parquet_path = "test_eda_data.parquet"
    csv_path = "test_eda_data.csv"
    df.to_parquet(parquet_path)
    df.to_csv(csv_path, index=False)

    print("=== PARQUET FILE CHECK ===")
    df_parquet = load_data(parquet_path, file_type="parquet")
    show_basic_info(df_parquet)
    show_head(df_parquet, n=3)
    check_missing_values(df_parquet)
    check_duplicates(df_parquet)
    get_column_types(df_parquet)
    get_nan_columns(df_parquet)
    get_summary(df_parquet)

    print("\n=== CSV FILE CHECK ===")
    df_csv = load_data(csv_path, file_type="csv")
    show_basic_info(df_csv)
    show_head(df_csv, n=3)
    check_missing_values(df_csv)
    check_duplicates(df_csv)
    get_column_types(df_csv)
    get_nan_columns(df_csv)
    get_summary(df_csv)

    # Cleanup
    if os.path.exists(parquet_path):
        os.remove(parquet_path)
    if os.path.exists(csv_path):
        os.remove(csv_path)

if __name__ == "__main__":
    main()