# -*- coding: utf-8 -*-
# src/interactive/eda/duplicates/duplicate_detection.py
#!/usr/bin/env python3
"""
Duplicate Detection module.

This module provides duplicate detection capabilities for financial data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class DuplicateDetection:
    """
    Analyzer for detecting duplicate data in financial datasets.
    
    Features:
    - Exact duplicate detection
    - Timestamp-based duplicate detection
    - OHLCV-based duplicate detection
    - Business logic duplicate detection
    """
    
    def __init__(self):
        """Initialize the DuplicateDetection."""
        pass
    
    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict:
        """
        Analyze duplicate rows in DataFrame with enhanced detection.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dict: Comprehensive duplicate analysis summary
        """
        # Check for exact duplicates
        exact_dupes = df.duplicated()
        exact_dupe_count = exact_dupes.sum()
        
        # Check for duplicates based on key columns (if timestamp exists)
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        # Check for duplicates based on OHLCV columns (common in financial data)
        ohlcv_cols = [col for col in df.columns if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'VOL']]
        
        dupe_summary = {
            'total_duplicates': exact_dupe_count,
            'duplicate_percent': (exact_dupe_count / len(df)) * 100 if len(df) > 0 else 0,
            'exact_duplicates': exact_dupe_count,
            'timestamp_based_duplicates': 0,
            'ohlcv_based_duplicates': 0,
            'key_columns': [],
            'ohlcv_duplicates': []
        }
        
        if exact_dupe_count > 0:
            print(f"   🔄 Found {exact_dupe_count:,} exact duplicate rows ({dupe_summary['duplicate_percent']:.1f}%)")
            
            # Show sample of duplicate rows
            if exact_dupe_count <= 10:
                print(f"   📋 Sample duplicate rows:")
                dupes_df = df[exact_dupes].head(3)
                for idx, row in dupes_df.iterrows():
                    print(f"      Row {idx}: {dict(row.head(3))}")
            else:
                print(f"   📋 Showing first 3 duplicate rows:")
                dupes_df = df[exact_dupes].head(3)
                for idx, row in dupes_df.iterrows():
                    print(f"      Row {idx}: {dict(row.head(3))}")
        else:
            print("   ✅ No exact duplicates found")
        
        # Check timestamp-based duplicates
        if timestamp_cols:
            print(f"   ⏱️  Checking timestamp-based duplicates...")
            for ts_col in timestamp_cols[:3]:  # Check first 3 timestamp columns
                try:
                    ts_dupes = df.duplicated(subset=[ts_col])
                    ts_dupe_count = ts_dupes.sum()
                    if ts_dupe_count > 0:
                        dupe_summary['timestamp_based_duplicates'] += ts_dupe_count
                        dupe_summary['key_columns'].append({
                            'column': ts_col,
                            'duplicate_count': ts_dupe_count,
                            'type': 'timestamp'
                        })
                        print(f"      • {ts_col}: {ts_dupe_count:,} duplicates")
                        
                        # Show sample of timestamp duplicates
                        if ts_dupe_count <= 5:
                            ts_dupes_df = df[ts_dupes].head(2)
                            for idx, row in ts_dupes_df.iterrows():
                                print(f"        Sample: {ts_col}={row[ts_col]}")
                        else:
                            ts_dupes_df = df[ts_dupes].head(2)
                            for idx, row in ts_dupes_df.iterrows():
                                print(f"        Sample: {ts_col}={row[ts_col]}")
                    else:
                        print(f"      • {ts_col}: No duplicates")
                except Exception as e:
                    print(f"      • {ts_col}: Error analyzing - {e}")
                    continue
        
        # Check OHLCV-based duplicates (common in financial data)
        if ohlcv_cols:
            print(f"   📊 Checking OHLCV-based duplicates...")
            for ohlcv_col in ohlcv_cols[:3]:  # Check first 3 OHLCV columns
                try:
                    ohlcv_dupes = df.duplicated(subset=[ohlcv_col])
                    ohlcv_dupe_count = ohlcv_dupes.sum()
                    if ohlcv_dupe_count > 0:
                        dupe_summary['ohlcv_based_duplicates'] += ohlcv_dupe_count
                        dupe_summary['ohlcv_duplicates'].append({
                            'column': ohlcv_col,
                            'duplicate_count': ohlcv_dupe_count,
                            'type': 'ohlcv'
                        })
                        print(f"      • {ohlcv_col}: {ohlcv_dupe_count:,} duplicates")
                    else:
                        print(f"      • {ohlcv_col}: No duplicates")
                except Exception as e:
                    print(f"      • {ohlcv_col}: Error analyzing - {e}")
                    continue
        
        # Check for potential business logic duplicates (timestamp + OHLCV)
        if timestamp_cols and ohlcv_cols:
            print(f"   🔍 Checking business logic duplicates (timestamp + OHLCV)...")
            try:
                # Use first timestamp and first OHLCV column for business logic check
                ts_col = timestamp_cols[0]
                ohlcv_col = ohlcv_cols[0]
                
                business_logic_dupes = df.duplicated(subset=[ts_col, ohlcv_col])
                business_logic_dupe_count = business_logic_dupes.sum()
                
                if business_logic_dupe_count > 0:
                    dupe_summary['key_columns'].append({
                        'column': f"{ts_col}+{ohlcv_col}",
                        'duplicate_count': business_logic_dupe_count,
                        'type': 'business_logic'
                    })
                    print(f"      • {ts_col}+{ohlcv_col}: {business_logic_dupe_count:,} duplicates")
                    
                    # Show sample of business logic duplicates
                    if business_logic_dupe_count <= 3:
                        bl_dupes_df = df[business_logic_dupes].head(2)
                        for idx, row in bl_dupes_df.iterrows():
                            print(f"        Sample: {ts_col}={row[ts_col]}, {ohlcv_col}={row[ohlcv_col]}")
                else:
                    print(f"      • {ts_col}+{ohlcv_col}: No business logic duplicates")
                    
            except Exception as e:
                print(f"      • Business logic check: Error - {e}")
        
        return dupe_summary
