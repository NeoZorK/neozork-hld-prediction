#!/usr/bin/env python3

import pandas as pd
import sys
import os

def examine_parquet_file(file_path):
    """Examine the structure of a parquet file"""
    try:
        print(f"Examining file: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        print(f"File size: {os.path.getsize(file_path)} bytes")
        
        # Read the parquet file
        df = pd.read_parquet(file_path)
        
        print(f"\n=== PARQUET FILE STRUCTURE ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Column count: {len(df.columns)}")
        
        print(f"\n=== COLUMN DETAILS ===")
        for i, col in enumerate(df.columns):
            print(f"{i+1:2d}. '{col}' ({df[col].dtype})")
        
        print(f"\n=== DATA SAMPLE ===")
        print("First 3 rows:")
        print(df.head(3))
        
        print(f"\n=== INDEX INFO ===")
        print(f"Index type: {type(df.index)}")
        print(f"Index name: {df.index.name}")
        if hasattr(df.index, 'dtype'):
            print(f"Index dtype: {df.index.dtype}")
        
        # Identify standard vs non-standard fields
        standard_fields_lower = ['open', 'high', 'low', 'close', 'volume']
        standard_fields_title = ['Open', 'High', 'Low', 'Close', 'Volume']
        standard_fields_all = standard_fields_lower + standard_fields_title
        
        actual_columns = list(df.columns)
        standard_found = [col for col in actual_columns if col in standard_fields_all]
        non_standard_fields = [col for col in actual_columns if col not in standard_fields_all]
        
        print(f"\n=== FIELD CLASSIFICATION ===")
        print(f"Standard fields found: {standard_found}")
        print(f"Non-standard fields: {non_standard_fields}")
        print(f"Total standard: {len(standard_found)}")
        print(f"Total non-standard: {len(non_standard_fields)}")
        
        return {
            'columns': actual_columns,
            'standard_fields': standard_found,
            'non_standard_fields': non_standard_fields,
            'shape': df.shape,
            'sample_data': df.head(3)
        }
        
    except Exception as e:
        print(f"Error reading parquet file: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Examine both parquet files
    files_to_examine = [
        "data/raw_parquet/binance_BTCUSDT_H1.parquet",
        "data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet"
    ]
    
    for file_path in files_to_examine:
        print("=" * 80)
        result = examine_parquet_file(file_path)
        print()
