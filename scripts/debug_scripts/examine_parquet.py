#!/usr/bin/env python3

import pandas as pd
import sys

def examine_parquet(file_path):
    try:
        print(f"Reading parquet file: {file_path}")
        df = pd.read_parquet(file_path)
        
        print("\n=== PARQUET FILE STRUCTURE ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        print("\n=== COLUMN TYPES ===")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
        
        print("\n=== FIRST 3 ROWS ===")
        print(df.head(3))
        
        # Identify standard vs non-standard fields
        standard_fields = {'open', 'high', 'low', 'close', 'volume', 'timeseries', 'datetime', 'date', 'time'}
        standard_found = []
        non_standard_found = []
        
        for col in df.columns:
            if col.lower() in standard_fields:
                standard_found.append(col)
            else:
                non_standard_found.append(col)
        
        print("\n=== FIELD CLASSIFICATION ===")
        print(f"Standard fields: {standard_found}")
        print(f"Non-standard fields: {non_standard_found}")
        
        if non_standard_found:
            print("\n=== NON-STANDARD FIELD SAMPLE DATA ===")
            for field in non_standard_found[:5]:  # Show first 5 non-standard fields
                print(f"\n{field}:")
                sample_data = df[field].dropna().head(3)
                print(f"  Sample values: {list(sample_data)}")
                print(f"  Data type: {df[field].dtype}")
                print(f"  Non-null count: {df[field].count()}/{len(df)}")
        
        return standard_found, non_standard_found
        
    except Exception as e:
        print(f"Error reading parquet file: {e}")
        import traceback
        traceback.print_exc()
        return [], []

if __name__ == "__main__":
    file_path = "../../data/cache/csv_converted/CSVExport_GBPUSD_PERIOD_MN1.parquet"
    examine_parquet(file_path)
