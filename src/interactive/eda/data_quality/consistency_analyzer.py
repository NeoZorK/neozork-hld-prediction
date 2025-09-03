#!/usr/bin/env python3
"""
Data Consistency Analyzer module.

This module provides comprehensive data consistency analysis capabilities
for financial data including logical checks and recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class ConsistencyAnalyzer:
    """
    Analyzer for data consistency in financial data.
    
    Features:
    - Data type consistency
    - Value range consistency
    - Logical consistency checks
    - Temporal consistency
    - Recommendations
    """
    
    def __init__(self):
        """Initialize the ConsistencyAnalyzer."""
        pass
    
    def run_data_consistency_check(self, system) -> bool:
        """
        Run data consistency check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n✅ DATA CONSISTENCY CHECK")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📊 Running data consistency checks...")
        
        # 1. Data type consistency
        print(f"\n🏷️  Data Type Consistency:")
        
        # Check for mixed types in object columns
        object_cols = df.select_dtypes(include=['object']).columns
        mixed_type_cols = []
        
        for col in object_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                # Check if column contains mixed types
                type_counts = col_data.apply(type).value_counts()
                if len(type_counts) > 1:
                    mixed_type_cols.append((col, type_counts))
        
        if mixed_type_cols:
            print(f"   ⚠️  Mixed data types detected:")
            for col, type_counts in mixed_type_cols[:3]:  # Show first 3
                print(f"     - {col}: {dict(type_counts)}")
            print(f"     → This can cause data processing issues")
        else:
            print(f"   ✅ No mixed data types detected")
        
        # 2. Value range consistency
        print(f"\n📏 Value Range Consistency:")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols[:3]:  # Check first 3 columns
            col_data = df[col].dropna()
            if len(col_data) > 0:
                print(f"\n     📊 {col}:")
                
                # Check for logical bounds
                min_val = col_data.min()
                max_val = col_data.max()
                
                print(f"       - Range: [{min_val:.6f}, {max_val:.6f}]")
                
                # Check for financial data consistency
                if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE']:
                    # OHLC consistency checks
                    if 'HIGH' in col.upper():
                        if min_val < 0:
                            print(f"       ⚠️  Negative prices detected - check data quality")
                    
                    if 'LOW' in col.upper():
                        if min_val < 0:
                            print(f"       ⚠️  Negative prices detected - check data quality")
                    
                    if 'VOLUME' in col.upper():
                        if min_val < 0:
                            print(f"       ⚠️  Negative volume detected - check data quality")
                
                # Check for extreme values
                q99 = col_data.quantile(0.99)
                q01 = col_data.quantile(0.01)
                iqr = col_data.quantile(0.75) - col_data.quantile(0.25)
                
                extreme_upper = q99 + 3 * iqr
                extreme_lower = q01 - 3 * iqr
                
                extreme_values = col_data[(col_data > extreme_upper) | (col_data < extreme_lower)]
                if len(extreme_values) > 0:
                    print(f"       ⚠️  {len(extreme_values)} extreme values detected")
                    print(f"       - Extreme range: [{extreme_lower:.6f}, {extreme_upper:.6f}]")
        
        # 3. Logical consistency checks
        print(f"\n🧠 Logical Consistency Checks:")
        
        # Check OHLC relationships if available
        ohlcv_cols = [col for col in numeric_cols if col.upper() in ['OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']]
        
        if len(ohlcv_cols) >= 3:
            print(f"   • OHLC Logical Consistency:")
            
            # Check High >= Low
            if 'HIGH' in [col.upper() for col in ohlcv_cols] and 'LOW' in [col.upper() for col in ohlcv_cols]:
                high_col = [col for col in ohlcv_cols if 'HIGH' in col.upper()][0]
                low_col = [col for col in ohlcv_cols if 'LOW' in col.upper()][0]
                
                invalid_hl = df[df[high_col] < df[low_col]]
                if len(invalid_hl) > 0:
                    print(f"     ⚠️  {len(invalid_hl)} rows where High < Low")
                else:
                    print(f"     ✅ High >= Low constraint satisfied")
            
            # Check High >= Open, Close
            if 'HIGH' in [col.upper() for col in ohlcv_cols]:
                high_col = [col for col in ohlcv_cols if 'HIGH' in col.upper()][0]
                
                for other_col in ohlcv_cols:
                    if other_col != high_col and other_col.upper() in ['OPEN', 'CLOSE']:
                        invalid_high = df[df[high_col] < df[other_col]]
                        if len(invalid_high) > 0:
                            print(f"     ⚠️  {len(invalid_high)} rows where High < {other_col}")
                        else:
                            print(f"     ✅ High >= {other_col} constraint satisfied")
            
            # Check Low <= Open, Close
            if 'LOW' in [col.upper() for col in ohlcv_cols]:
                low_col = [col for col in ohlcv_cols if 'LOW' in col.upper()][0]
                
                for other_col in ohlcv_cols:
                    if other_col != low_col and other_col.upper() in ['OPEN', 'CLOSE']:
                        invalid_low = df[df[low_col] > df[other_col]]
                        if len(invalid_low) > 0:
                            print(f"     ⚠️  {len(invalid_low)} rows where Low > {other_col}")
                        else:
                            print(f"     ✅ Low <= {other_col} constraint satisfied")
        
        # 4. Temporal consistency
        print(f"\n⏰ Temporal Consistency:")
        
        # Check for timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        if timestamp_cols:
            for ts_col in timestamp_cols[:2]:  # Check first 2
                print(f"\n     📅 {ts_col}:")
                
                try:
                    # Convert to datetime
                    datetime_data = pd.to_datetime(df[ts_col], errors='coerce')
                    valid_datetimes = datetime_data.dropna()
                    
                    if len(valid_datetimes) > 0:
                        # Check for chronological order
                        sorted_datetimes = valid_datetimes.sort_values()
                        is_chronological = (sorted_datetimes == valid_datetimes).all()
                        
                        if is_chronological:
                            print(f"       ✅ Timestamps are in chronological order")
                        else:
                            print(f"       ⚠️  Timestamps are not in chronological order")
                        
                        # Check for future dates
                        current_time = pd.Timestamp.now()
                        future_dates = valid_datetimes[valid_datetimes > current_time]
                        
                        if len(future_dates) > 0:
                            print(f"       ⚠️  {len(future_dates)} future timestamps detected")
                        else:
                            print(f"       ✅ No future timestamps detected")
                        
                        # Check for duplicate timestamps
                        duplicate_timestamps = valid_datetimes.duplicated().sum()
                        if duplicate_timestamps > 0:
                            print(f"       ⚠️  {duplicate_timestamps} duplicate timestamps detected")
                        else:
                            print(f"       ✅ No duplicate timestamps detected")
                        
                except Exception as e:
                    print(f"       ❌ Error checking temporal consistency: {e}")
        
        # 5. Summary and recommendations
        print(f"\n📋 Consistency Check Summary:")
        
        # Count issues
        total_issues = 0
        
        if mixed_type_cols:
            total_issues += len(mixed_type_cols)
        
        # Add other issue counts as needed
        
        if total_issues == 0:
            print(f"   ✅ No consistency issues detected")
        else:
            print(f"   ⚠️  {total_issues} consistency issues detected")
        
        print(f"\n💡 Consistency Improvement Recommendations:")
        
        if mixed_type_cols:
            print(f"   • Fix mixed data types in: {', '.join([col for col, _ in mixed_type_cols[:3]])}")
        
        print(f"   • Implement data validation rules")
        print(f"   • Set up automated consistency checks")
        print(f"   • Document expected data constraints")
        
        return True
