#!/usr/bin/env python3
"""
Data Quality Fix Script

This script fixes common data quality issues in parquet files:
- Infinite values (+inf, -inf)
- Negative values in price columns
- Zero values in price columns
- NaN values

Usage:
    python scripts/fix_data_quality.py [--file FILENAME] [--all]
"""

import argparse
import os
import sys
import glob
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from eda import fix_files


def backup_file(file_path):
    """Create a backup of the original file."""
    backup_path = f"{file_path}.bak"
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
    return backup_path


def fix_file_quality(file_path, fix_infs=True, fix_negatives=True, fix_zeros=True, fix_nans=True):
    """Fix data quality issues in a single file."""
    print(f"\nProcessing: {file_path}")
    
    try:
        # Read the file
        df = pd.read_parquet(file_path)
        original_shape = df.shape
        print(f"  Original shape: {original_shape}")
        
        # Create backup
        backup_path = backup_file(file_path)
        
        # Track changes
        changes_made = False
        
        # Fix infinite values
        if fix_infs:
            inf_columns = []
            for col in df.select_dtypes(include=[np.number]).columns:
                if np.isinf(df[col]).any():
                    inf_columns.append(col)
            
            if inf_columns:
                print(f"  Fixing infinite values in columns: {inf_columns}")
                df = fix_files.fix_infs(df)
                changes_made = True
        
        # Fix negative values in price columns
        if fix_negatives:
            price_columns = [col for col in df.columns if any(price in col.lower() for price in ['open', 'high', 'low', 'close', 'price'])]
            negative_columns = []
            
            for col in price_columns:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    if (df[col] < 0).any():
                        negative_columns.append(col)
            
            if negative_columns:
                print(f"  Fixing negative values in price columns: {negative_columns}")
                df = fix_files.fix_negatives(df)
                changes_made = True
        
        # Fix zero values in price columns
        if fix_zeros:
            price_columns = [col for col in df.columns if any(price in col.lower() for price in ['open', 'high', 'low', 'close', 'price'])]
            zero_columns = []
            
            for col in price_columns:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    if (df[col] == 0).any():
                        zero_columns.append(col)
            
            if zero_columns:
                print(f"  Fixing zero values in price columns: {zero_columns}")
                df = fix_files.fix_zeros(df)
                changes_made = True
        
        # Fix NaN values
        if fix_nans:
            nan_columns = [col for col in df.columns if df[col].isna().any()]
            if nan_columns:
                print(f"  Fixing NaN values in columns: {nan_columns}")
                df = fix_files.fix_nan(df)
                changes_made = True
        
        # Save the fixed file
        if changes_made:
            df.to_parquet(file_path, index=False)
            print(f"  Fixed file saved: {file_path}")
            print(f"  Final shape: {df.shape}")
            return True
        else:
            print(f"  No issues found, no changes needed")
            return False
            
    except Exception as e:
        print(f"  Error processing {file_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Fix data quality issues in parquet files')
    parser.add_argument('--file', type=str, help='Fix a specific file')
    parser.add_argument('--all', action='store_true', help='Fix all parquet files in data directory')
    parser.add_argument('--no-infs', action='store_true', help='Skip fixing infinite values')
    parser.add_argument('--no-negatives', action='store_true', help='Skip fixing negative values')
    parser.add_argument('--no-zeros', action='store_true', help='Skip fixing zero values')
    parser.add_argument('--no-nans', action='store_true', help='Skip fixing NaN values')
    
    args = parser.parse_args()
    
    # Determine which fixes to apply
    fix_infs = not args.no_infs
    fix_negatives = not args.no_negatives
    fix_zeros = not args.no_zeros
    fix_nans = not args.no_nans
    
    print("Data Quality Fix Script")
    print("======================")
    print(f"Fixes to apply:")
    print(f"  - Infinite values: {'Yes' if fix_infs else 'No'}")
    print(f"  - Negative values: {'Yes' if fix_negatives else 'No'}")
    print(f"  - Zero values: {'Yes' if fix_zeros else 'No'}")
    print(f"  - NaN values: {'Yes' if fix_nans else 'No'}")
    
    if args.file:
        # Fix specific file
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} not found")
            return 1
        
        success = fix_file_quality(args.file, fix_infs, fix_negatives, fix_zeros, fix_nans)
        return 0 if success else 1
    
    elif args.all:
        # Fix all parquet files
        data_dir = Path('data')
        parquet_files = list(data_dir.rglob('*.parquet'))
        
        if not parquet_files:
            print("No parquet files found in data directory")
            return 1
        
        print(f"\nFound {len(parquet_files)} parquet files")
        
        fixed_count = 0
        total_count = 0
        
        for file_path in parquet_files:
            total_count += 1
            if fix_file_quality(str(file_path), fix_infs, fix_negatives, fix_zeros, fix_nans):
                fixed_count += 1
        
        print(f"\nSummary:")
        print(f"  Total files processed: {total_count}")
        print(f"  Files fixed: {fixed_count}")
        print(f"  Files unchanged: {total_count - fixed_count}")
        
        return 0
    
    else:
        print("Error: Please specify --file or --all")
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
