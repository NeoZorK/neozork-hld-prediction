#!/usr/bin/env python3
"""
Data Type Analyzer module.

This module provides comprehensive data type analysis capabilities
for financial data including optimization recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class DataTypeAnalyzer:
    """
    Analyzer for data types in financial data.
    
    Features:
    - Data type summary
    - Object column analysis
    - Numerical column analysis
    - Datetime detection
    - Memory optimization
    - Recommendations
    """
    
    def __init__(self):
        """Initialize the DataTypeAnalyzer."""
        pass
    
    def run_data_type_analysis(self, system) -> bool:
        """
        Run data type analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🏷️  DATA TYPE ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📊 Analyzing data types for {len(df.columns)} columns...")
        
        # Data type summary
        dtype_counts = df.dtypes.value_counts()
        print(f"\n📋 Data Type Summary:")
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # Analyze each data type
        print(f"\n🔍 Detailed Data Type Analysis:")
        
        # 1. Object columns (potential text/categorical)
        object_cols = df.select_dtypes(include=['object']).columns
        if len(object_cols) > 0:
            print(f"\n📝 Object Columns Analysis:")
            print(f"   • Found {len(object_cols)} object columns")
            
            for col in object_cols[:5]:  # Analyze first 5
                print(f"\n     📊 {col}:")
                
                # Check if it's actually categorical
                unique_count = df[col].nunique()
                total_count = len(df[col])
                cardinality_ratio = unique_count / total_count
                
                print(f"       - Unique values: {unique_count:,}")
                print(f"       - Cardinality ratio: {cardinality_ratio:.4f}")
                
                if cardinality_ratio < 0.1:
                    print(f"       → Low cardinality - good candidate for category type")
                elif cardinality_ratio < 0.5:
                    print(f"       → Medium cardinality - consider category type")
                else:
                    print(f"       → High cardinality - keep as object")
                
                # Check for mixed types
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    print(f"       - Sample values: {sample_values.tolist()}")
        
        # 2. Numerical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n🔢 Numerical Columns Analysis:")
            print(f"   • Found {len(numeric_cols)} numerical columns")
            
            for col in numeric_cols[:5]:  # Analyze first 5
                print(f"\n     📊 {col}:")
                
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    # Check if it's actually categorical
                    unique_count = col_data.nunique()
                    total_count = len(col_data)
                    
                    print(f"       - Data type: {df[col].dtype}")
                    print(f"       - Unique values: {unique_count:,}")
                    print(f"       - Range: [{col_data.min():.6f}, {col_data.max():.6f}]")
                    
                    # Check if it should be categorical
                    if unique_count < 20 and unique_count < total_count * 0.1:
                        print(f"       → Low unique values - consider converting to category")
                    
                    # Check precision
                    if df[col].dtype == 'float64':
                        # Check if float64 precision is needed
                        if col_data.apply(lambda x: x.is_integer()).all():
                            print(f"       → All values are integers - consider int64 type")
        
        # 3. Datetime columns
        datetime_cols = []
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to detect datetime columns
                try:
                    pd.to_datetime(df[col], errors='raise')
                    datetime_cols.append(col)
                except:
                    pass
        
        if datetime_cols:
            print(f"\n⏰ Datetime Columns Analysis:")
            print(f"   • Found {len(datetime_cols)} potential datetime columns")
            
            for col in datetime_cols[:3]:  # Analyze first 3
                print(f"\n     📅 {col}:")
                
                try:
                    datetime_data = pd.to_datetime(df[col], errors='coerce')
                    valid_datetimes = datetime_data.dropna()
                    
                    if len(valid_datetimes) > 0:
                        print(f"       - Valid datetimes: {len(valid_datetimes):,}")
                        print(f"       - Range: {valid_datetimes.min()} to {valid_datetimes.max()}")
                        print(f"       - Recommendation: Convert to datetime type")
                except:
                    print(f"       - Error parsing datetime values")
        
        # 4. Memory optimization analysis
        print(f"\n💾 Memory Optimization Analysis:")
        
        current_memory = df.memory_usage(deep=True).sum() / 1024**2
        print(f"   • Current memory usage: {current_memory:.2f} MB")
        
        # Calculate potential savings
        potential_savings = 0
        
        for col in df.columns:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                current_dtype = df[col].dtype
                
                # Suggest optimizations
                if current_dtype == 'object':
                    unique_count = col_data.nunique()
                    if unique_count < len(col_data) * 0.5:
                        # Estimate category memory savings
                        current_mem = df[col].memory_usage(deep=True)
                        estimated_cat_mem = len(col_data) * 4  # 4 bytes per category code
                        potential_savings += current_mem - estimated_cat_mem
                        print(f"     - {col}: object → category (save ~{current_mem - estimated_cat_mem} bytes)")
                
                elif current_dtype == 'float64':
                    # Check if float32 is sufficient
                    if col_data.apply(lambda x: x.is_integer()).all():
                        potential_savings += len(col_data) * 4  # 8 bytes → 4 bytes
                        print(f"     - {col}: float64 → int64 (save ~{len(col_data) * 4} bytes)")
                    else:
                        # Check if float32 precision is sufficient
                        if col_data.max() < 3.4e38 and col_data.min() > -3.4e38:
                            potential_savings += len(col_data) * 4  # 8 bytes → 4 bytes
                            print(f"     - {col}: float64 → float32 (save ~{len(col_data) * 4} bytes)")
        
        if potential_savings > 0:
            potential_savings_mb = potential_savings / 1024**2
            print(f"\n   💡 Potential memory savings: {potential_savings_mb:.2f} MB")
        
        # Recommendations
        print(f"\n💡 Data Type Optimization Recommendations:")
        
        print(f"   • Immediate Actions:")
        if len(object_cols) > 0:
            print(f"     - Convert low-cardinality object columns to category")
        
        if len(datetime_cols) > 0:
            print(f"     - Convert detected datetime columns to datetime type")
        
        print(f"   • Performance Improvements:")
        print(f"     - Use appropriate integer types (int8, int16, int32, int64)")
        print(f"     - Use float32 when precision allows")
        print(f"     - Use category for low-cardinality categorical data")
        
        return True
