#!/usr/bin/env python3
"""
Exploratory Data Analysis (EDA) utilities.
Handles basic statistics, data quality checks, and correlation analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class EDAAnalyzer:
    """Handles exploratory data analysis operations."""
    
    def __init__(self):
        """Initialize EDAAnalyzer."""
        pass
    
    def run_basic_statistics(self, system) -> bool:
        """
        Run basic statistical analysis on the dataset.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 BASIC STATISTICAL ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        print(f"📁 Dataset Overview:")
        print(f"   • Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
        
        # Data types
        print(f"\n🔍 Data Types:")
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # Missing values
        print(f"\n⚠️  Missing Values:")
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df)) * 100
        
        missing_summary = pd.DataFrame({
            'Column': missing_data.index,
            'Missing_Count': missing_data.values,
            'Missing_Percent': missing_percent.values
        }).sort_values('Missing_Count', ascending=False)
        
        missing_summary = missing_summary[missing_summary['Missing_Count'] > 0]
        
        if len(missing_summary) > 0:
            for _, row in missing_summary.head(10).iterrows():
                print(f"   • {row['Column']}: {row['Missing_Count']:,} ({row['Missing_Percent']:.1f}%)")
            if len(missing_summary) > 10:
                print(f"   • ... and {len(missing_summary) - 10} more columns")
        else:
            print("   ✅ No missing values found")
        
        # Numeric columns statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"\n📈 Numeric Columns Statistics:")
            print(f"   • Total numeric columns: {len(numeric_cols)}")
            
            # Show statistics for first few numeric columns
            for col in numeric_cols[:5]:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    print(f"   • {col}:")
                    print(f"     - Mean: {col_data.mean():.4f}")
                    print(f"     - Median: {col_data.median():.4f}")
                    print(f"     - Std: {col_data.std():.4f}")
                    print(f"     - Min: {col_data.min():.4f}")
                    print(f"     - Max: {col_data.max():.4f}")
                    print(f"     - Range: {col_data.max() - col_data.min():.4f}")
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            print(f"\n🏷️  Categorical Columns:")
            print(f"   • Total categorical columns: {len(categorical_cols)}")
            
            # Show unique values for first few categorical columns
            for col in categorical_cols[:3]:
                unique_vals = df[col].nunique()
                print(f"   • {col}: {unique_vals} unique values")
                if unique_vals <= 10:
                    value_counts = df[col].value_counts().head(5)
                    for val, count in value_counts.items():
                        print(f"     - {val}: {count:,}")
        
        # Datetime columns
        datetime_cols = df.select_dtypes(include=['datetime64']).columns
        if len(datetime_cols) > 0:
            print(f"\n📅 Datetime Columns:")
            print(f"   • Total datetime columns: {len(datetime_cols)}")
            
            for col in datetime_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    print(f"   • {col}:")
                    print(f"     - Range: {col_data.min()} to {col_data.max()}")
                    print(f"     - Duration: {col_data.max() - col_data.min()}")
        
        print(f"\n✅ Basic statistical analysis completed!")
        return True
    
    def run_comprehensive_data_quality_check(self, system) -> Tuple[Dict, Dict, Dict]:
        """
        Run comprehensive data quality check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            Tuple of (nan_summary, dupe_summary, gap_summary)
        """
        print(f"\n🔍 COMPREHENSIVE DATA QUALITY CHECK")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return {}, {}, {}
        
        df = system.current_data
        
        print(f"📁 Analyzing dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        # 1. Missing Values Analysis
        print(f"\n1️⃣  MISSING VALUES ANALYSIS")
        print("-" * 30)
        
        nan_summary = self._analyze_missing_values(df)
        
        # 2. Duplicate Analysis
        print(f"\n2️⃣  DUPLICATE ANALYSIS")
        print("-" * 30)
        
        dupe_summary = self._analyze_duplicates(df)
        
        # 3. Time Series Gap Analysis
        print(f"\n3️⃣  TIME SERIES GAP ANALYSIS")
        print("-" * 30)
        
        gap_summary = self._analyze_time_series_gaps(df)
        
        # Summary
        print(f"\n📊 DATA QUALITY SUMMARY")
        print("-" * 30)
        print(f"   ⚠️  Missing values: {len(nan_summary)} columns affected")
        print(f"   🔄 Duplicates: {dupe_summary.get('total_duplicates', 0):,} rows")
        print(f"   ⏱️  Time series gaps: {len(gap_summary)} columns affected")
        
        return nan_summary, dupe_summary, gap_summary
    
    def _analyze_missing_values(self, df: pd.DataFrame) -> Dict:
        """Analyze missing values in DataFrame."""
        missing_data = df.isnull().sum()
        missing_percent = (missing_data / len(df)) * 100
        
        nan_summary = []
        for col in df.columns:
            missing_count = missing_data[col]
            if missing_count > 0:
                nan_summary.append({
                    'column': col,
                    'missing_count': missing_count,
                    'missing_percent': missing_percent[col],
                    'data_type': str(df[col].dtype),
                    'total_rows': len(df)
                })
        
        # Sort by missing count
        nan_summary.sort(key=lambda x: x['missing_count'], reverse=True)
        
        if nan_summary:
            print(f"   📊 Found {len(nan_summary)} columns with missing values:")
            for item in nan_summary[:10]:  # Show top 10
                print(f"      • {item['column']}: {item['missing_count']:,} ({item['missing_percent']:.1f}%)")
            if len(nan_summary) > 10:
                print(f"      • ... and {len(nan_summary) - 10} more columns")
        else:
            print("   ✅ No missing values found")
        
        return nan_summary
    
    def _analyze_duplicates(self, df: pd.DataFrame) -> Dict:
        """Analyze duplicate rows in DataFrame."""
        # Check for exact duplicates
        exact_dupes = df.duplicated()
        exact_dupe_count = exact_dupes.sum()
        
        # Check for duplicates based on key columns (if timestamp exists)
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        dupe_summary = {
            'total_duplicates': exact_dupe_count,
            'duplicate_percent': (exact_dupe_count / len(df)) * 100 if len(df) > 0 else 0,
            'exact_duplicates': exact_dupe_count,
            'timestamp_based_duplicates': 0,
            'key_columns': []
        }
        
        if exact_dupe_count > 0:
            print(f"   🔄 Found {exact_dupe_count:,} exact duplicate rows ({dupe_summary['duplicate_percent']:.1f}%)")
        else:
            print("   ✅ No exact duplicates found")
        
        # Check timestamp-based duplicates
        if timestamp_cols:
            for ts_col in timestamp_cols[:3]:  # Check first 3 timestamp columns
                try:
                    ts_dupes = df.duplicated(subset=[ts_col])
                    ts_dupe_count = ts_dupes.sum()
                    if ts_dupe_count > 0:
                        dupe_summary['timestamp_based_duplicates'] += ts_dupe_count
                        dupe_summary['key_columns'].append({
                            'column': ts_col,
                            'duplicate_count': ts_dupe_count
                        })
                        print(f"   ⏱️  {ts_col}: {ts_dupe_count:,} duplicates")
                except Exception:
                    continue
        
        return dupe_summary
    
    def _analyze_time_series_gaps(self, df: pd.DataFrame) -> List[Dict]:
        """Analyze time series gaps in DataFrame."""
        gap_summary = []
        
        # Find timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        if not timestamp_cols:
            print("   ⚠️  No timestamp columns found for gap analysis")
            return gap_summary
        
        print(f"   📅 Analyzing {len(timestamp_cols)} timestamp columns for gaps...")
        
        for ts_col in timestamp_cols:
            try:
                # Convert to datetime if needed
                if not pd.api.types.is_datetime64_any_dtype(df[ts_col]):
                    df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
                
                # Sort by timestamp
                sorted_df = df.dropna(subset=[ts_col]).sort_values(ts_col)
                
                if len(sorted_df) < 2:
                    continue
                
                # Calculate time differences
                time_diffs = sorted_df[ts_col].diff().dropna()
                
                if len(time_diffs) == 0:
                    continue
                
                # Determine expected frequency
                median_diff = time_diffs.median()
                expected_freq = self._determine_frequency_from_timedelta(median_diff)
                
                # Find gaps (1.5x expected frequency)
                threshold = median_diff * 1.5
                gaps = time_diffs[time_diffs > threshold]
                gap_count = len(gaps)
                
                if gap_count > 0:
                    gap_summary.append({
                        'column': ts_col,
                        'gap_count': gap_count,
                        'expected_frequency': expected_freq,
                        'median_interval': median_diff,
                        'threshold': threshold,
                        'total_intervals': len(time_diffs)
                    })
                    print(f"      • {ts_col}: {gap_count:,} gaps found")
                else:
                    print(f"      • {ts_col}: No gaps found")
                    
            except Exception as e:
                print(f"      • {ts_col}: Error analyzing gaps - {e}")
                continue
        
        return gap_summary
    
    def _determine_frequency_from_timedelta(self, td: pd.Timedelta) -> str:
        """Determine frequency string from timedelta."""
        if td <= pd.Timedelta(minutes=1):
            return '1T'
        elif td <= pd.Timedelta(minutes=5):
            return '5T'
        elif td <= pd.Timedelta(minutes=15):
            return '15T'
        elif td <= pd.Timedelta(minutes=30):
            return '30T'
        elif td <= pd.Timedelta(hours=1):
            return '1H'
        elif td <= pd.Timedelta(hours=4):
            return '4H'
        elif td <= pd.Timedelta(days=1):
            return '1D'
        elif td <= pd.Timedelta(weeks=1):
            return '1W'
        elif td <= pd.Timedelta(days=30):
            return '1M'
        else:
            return '1Y'
    
    def run_correlation_analysis(self, system) -> bool:
        """
        Run correlation analysis on numeric columns.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔗 CORRELATION ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numeric columns for correlation analysis")
            return False
        
        print(f"📊 Analyzing correlations for {len(numeric_cols)} numeric columns")
        
        # Calculate correlation matrix
        correlation_matrix = df[numeric_cols].corr()
        
        # Find high correlations
        high_corr_threshold = 0.8
        high_correlations = []
        
        for i in range(len(correlation_matrix.columns)):
            for j in range(i+1, len(correlation_matrix.columns)):
                corr_value = correlation_matrix.iloc[i, j]
                if abs(corr_value) >= high_corr_threshold:
                    high_correlations.append({
                        'col1': correlation_matrix.columns[i],
                        'col2': correlation_matrix.columns[j],
                        'correlation': corr_value
                    })
        
        # Display results
        print(f"\n📈 Correlation Analysis Results:")
        print(f"   • Total numeric columns: {len(numeric_cols)}")
        print(f"   • High correlations (≥{high_corr_threshold}): {len(high_correlations)}")
        
        if high_correlations:
            print(f"\n🔗 High Correlations:")
            for corr in high_correlations:
                direction = "positive" if corr['correlation'] > 0 else "negative"
                print(f"   • {corr['col1']} ↔ {corr['col2']}: {corr['correlation']:.3f} ({direction})")
        
        # Show correlation matrix for small datasets
        if len(numeric_cols) <= 10:
            print(f"\n📊 Correlation Matrix:")
            print(correlation_matrix.round(3))
        
        return True
    
    def run_time_series_analysis(self, system) -> bool:
        """
        Run time series analysis on the dataset.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n⏱️  TIME SERIES ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find timestamp columns
        timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
        
        if not timestamp_cols:
            print("❌ No timestamp columns found for time series analysis")
            return False
        
        print(f"📅 Found {len(timestamp_cols)} timestamp columns:")
        for ts_col in timestamp_cols:
            print(f"   • {ts_col}")
        
        # Analyze each timestamp column
        for ts_col in timestamp_cols[:3]:  # Analyze first 3
            print(f"\n📊 Analyzing {ts_col}:")
            
            try:
                # Convert to datetime if needed
                if not pd.api.types.is_datetime64_any_dtype(df[ts_col]):
                    df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
                
                # Get datetime info
                dt_data = df[ts_col].dropna()
                if len(dt_data) == 0:
                    print(f"   ⚠️  No valid datetime data in {ts_col}")
                    continue
                
                print(f"   📅 Range: {dt_data.min()} to {dt_data.max()}")
                print(f"   ⏱️  Duration: {dt_data.max() - dt_data.min()}")
                print(f"   📊 Total records: {len(dt_data):,}")
                
                # Check for gaps
                sorted_dt = dt_data.sort_values()
                time_diffs = sorted_dt.diff().dropna()
                
                if len(time_diffs) > 0:
                    median_diff = time_diffs.median()
                    expected_freq = self._determine_frequency_from_timedelta(median_diff)
                    print(f"   🔄 Expected frequency: {expected_freq}")
                    print(f"   📏 Median interval: {median_diff}")
                    
                    # Find gaps
                    threshold = median_diff * 1.5
                    gaps = time_diffs[time_diffs > threshold]
                    if len(gaps) > 0:
                        print(f"   ⚠️  Found {len(gaps):,} gaps")
                    else:
                        print(f"   ✅ No gaps detected")
                
            except Exception as e:
                print(f"   ❌ Error analyzing {ts_col}: {e}")
                continue
        
        return True

    def run_feature_importance_analysis(self, system) -> bool:
        """
        Run feature importance analysis on the dataset.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🎯 FEATURE IMPORTANCE ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find numeric columns for analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            print("❌ Need at least 2 numeric columns for feature importance analysis")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric features...")
        
        try:
            # Calculate feature importance using correlation with target
            # For now, we'll use the first numeric column as target (can be enhanced later)
            target_col = numeric_cols[0]
            feature_cols = numeric_cols[1:]
            
            print(f"🎯 Target column: {target_col}")
            print(f"🔍 Feature columns: {len(feature_cols)}")
            
            # Calculate correlations with target
            correlations = {}
            for col in feature_cols:
                corr = df[target_col].corr(df[col])
                if not pd.isna(corr):
                    correlations[col] = abs(corr)
            
            # Sort by importance (absolute correlation)
            sorted_features = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
            
            print(f"\n📈 Feature Importance (by correlation with {target_col}):")
            print(f"   • Total features analyzed: {len(sorted_features)}")
            
            if sorted_features:
                print(f"\n🏆 Top 10 Most Important Features:")
                for i, (feature, importance) in enumerate(sorted_features[:10], 1):
                    print(f"   {i:2d}. {feature:<25} | Importance: {importance:.4f}")
                
                # Show distribution
                importance_values = [imp for _, imp in sorted_features]
                print(f"\n📊 Importance Statistics:")
                print(f"   • Mean importance: {np.mean(importance_values):.4f}")
                print(f"   • Median importance: {np.median(importance_values):.4f}")
                print(f"   • Std importance: {np.std(importance_values):.4f}")
                print(f"   • Min importance: {np.min(importance_values):.4f}")
                print(f"   • Max importance: {np.max(importance_values):.4f}")
                
                # Categorize features
                high_importance = [f for f, imp in sorted_features if imp >= 0.7]
                medium_importance = [f for f, imp in sorted_features if 0.3 <= imp < 0.7]
                low_importance = [f for f, imp in sorted_features if imp < 0.3]
                
                print(f"\n🏷️  Feature Categories:")
                print(f"   • High importance (≥0.7): {len(high_importance)} features")
                print(f"   • Medium importance (0.3-0.7): {len(medium_importance)} features")
                print(f"   • Low importance (<0.3): {len(low_importance)} features")
                
                if high_importance:
                    print(f"\n⭐ High Importance Features:")
                    for feature in high_importance[:5]:
                        print(f"   • {feature}")
                
            else:
                print("❌ No valid correlations found")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error in feature importance analysis: {e}")
            return False

    def run_duplicates_analysis(self, system) -> bool:
        """
        Run detailed duplicates analysis on the dataset.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🔄 DUPLICATES ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        dupe_summary = self._analyze_duplicates(df)
        
        # Show detailed duplicates info
        if dupe_summary.get('total_duplicates', 0) > 0:
            print(f"\n📊 Duplicates Summary:")
            print(f"   • Total duplicates: {dupe_summary['total_duplicates']:,}")
            print(f"   • Duplicate percentage: {dupe_summary['duplicate_percent']:.2f}%")
            
            if dupe_summary.get('key_columns'):
                print(f"   • Key columns with duplicates:")
                for key_col in dupe_summary['key_columns']:
                    print(f"     - {key_col['column']}: {key_col['duplicate_count']:,} duplicates")
        else:
            print("✅ No duplicates found in the dataset")
        
        return True

    def run_nan_analysis(self, system) -> bool:
        """
        Run detailed NAN analysis on the dataset.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n❓ NAN ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        nan_summary = self._analyze_missing_values(df)
        
        if nan_summary:
            print(f"\n📊 NAN Summary:")
            print(f"   • Columns with NAN values: {len(nan_summary)}")
            
            # Show top columns by NAN count
            print(f"   • Top columns by NAN count:")
            for i, item in enumerate(nan_summary[:10], 1):
                print(f"     {i:2d}. {item['column']:<25} | {item['missing_count']:,} ({item['missing_percent']:.1f}%)")
            
            if len(nan_summary) > 10:
                print(f"     ... and {len(nan_summary) - 10} more columns")
        else:
            print("✅ No NAN values found in the dataset")
        
        return True

    def run_zero_analysis(self, system) -> bool:
        """
        Run zero values analysis on numeric columns.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n0️⃣ ZERO ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric columns found for zero analysis")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric columns for zero values...")
        
        zero_summary = []
        for col in numeric_cols:
            zero_count = (df[col] == 0).sum()
            zero_percent = (zero_count / len(df)) * 100 if len(df) > 0 else 0
            
            if zero_count > 0:
                zero_summary.append({
                    'column': col,
                    'zero_count': zero_count,
                    'zero_percent': zero_percent,
                    'total_rows': len(df)
                })
        
        if zero_summary:
            print(f"\n📊 Zero Values Summary:")
            print(f"   • Columns with zero values: {len(zero_summary)}")
            
            # Sort by zero count
            zero_summary.sort(key=lambda x: x['zero_count'], reverse=True)
            
            print(f"   • Top columns by zero count:")
            for i, item in enumerate(zero_summary[:10], 1):
                print(f"     {i:2d}. {item['column']:<25} | {item['zero_count']:,} ({item['zero_percent']:.1f}%)")
            
            if len(zero_summary) > 10:
                print(f"     ... and {len(zero_summary) - 10} more columns")
        else:
            print("✅ No zero values found in numeric columns")
        
        return True

    def run_negative_analysis(self, system) -> bool:
        """
        Run negative values analysis on numeric columns.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n➖ NEGATIVE ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric columns found for negative analysis")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric columns for negative values...")
        
        negative_summary = []
        for col in numeric_cols:
            negative_count = (df[col] < 0).sum()
            negative_percent = (negative_count / len(df)) * 100 if len(df) > 0 else 0
            
            if negative_count > 0:
                negative_summary.append({
                    'column': col,
                    'negative_count': negative_count,
                    'negative_percent': negative_percent,
                    'total_rows': len(df)
                })
        
        if negative_summary:
            print(f"\n📊 Negative Values Summary:")
            print(f"   • Columns with negative values: {len(negative_summary)}")
            
            # Sort by negative count
            negative_summary.sort(key=lambda x: x['negative_count'], reverse=True)
            
            print(f"   • Top columns by negative count:")
            for i, item in enumerate(negative_summary[:10], 1):
                print(f"     {i:2d}. {item['column']:<25} | {item['negative_count']:,} ({item['negative_percent']:.1f}%)")
            
            if len(negative_summary) > 10:
                print(f"     ... and {len(negative_summary) - 10} more columns")
        else:
            print("✅ No negative values found in numeric columns")
        
        return True

    def run_infinity_analysis(self, system) -> bool:
        """
        Run infinity values analysis on numeric columns.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n♾️ INFINITY ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric columns found for infinity analysis")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric columns for infinity values...")
        
        infinity_summary = []
        for col in numeric_cols:
            # Check for positive and negative infinity
            pos_inf_count = np.isinf(df[col]) & (df[col] > 0)
            neg_inf_count = np.isinf(df[col]) & (df[col] < 0)
            
            total_inf = pos_inf_count.sum() + neg_inf_count.sum()
            inf_percent = (total_inf / len(df)) * 100 if len(df) > 0 else 0
            
            if total_inf > 0:
                infinity_summary.append({
                    'column': col,
                    'positive_infinity': pos_inf_count.sum(),
                    'negative_infinity': neg_inf_count.sum(),
                    'total_infinity': total_inf,
                    'infinity_percent': inf_percent,
                    'total_rows': len(df)
                })
        
        if infinity_summary:
            print(f"\n📊 Infinity Values Summary:")
            print(f"   • Columns with infinity values: {len(infinity_summary)}")
            
            # Sort by total infinity count
            infinity_summary.sort(key=lambda x: x['total_infinity'], reverse=True)
            
            print(f"   • Top columns by infinity count:")
            for i, item in enumerate(infinity_summary[:10], 1):
                print(f"     {i:2d}. {item['column']:<25} | +∞: {item['positive_infinity']:,}, -∞: {item['negative_infinity']:,} ({item['infinity_percent']:.1f}%)")
            
            if len(infinity_summary) > 10:
                print(f"     ... and {len(infinity_summary) - 10} more columns")
        else:
            print("✅ No infinity values found in numeric columns")
        
        return True

    def run_outliers_analysis(self, system) -> bool:
        """
        Run outliers analysis using IQR method on numeric columns.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📊 OUTLIERS ANALYSIS")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric columns found for outliers analysis")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric columns for outliers using IQR method...")
        
        outliers_summary = []
        for col in numeric_cols[:20]:  # Limit to first 20 columns for performance
            try:
                data = df[col].dropna()
                if len(data) == 0:
                    continue
                
                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                iqr = q3 - q1
                
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                outliers_count = outliers_mask.sum()
                outliers_percent = (outliers_count / len(df)) * 100 if len(df) > 0 else 0
                
                if outliers_count > 0:
                    outliers_summary.append({
                        'column': col,
                        'outliers_count': outliers_count,
                        'outliers_percent': outliers_percent,
                        'q1': q1,
                        'q3': q3,
                        'iqr': iqr,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'total_rows': len(df)
                    })
            except Exception as e:
                print(f"   ⚠️  Error analyzing column {col}: {e}")
                continue
        
        if outliers_summary:
            print(f"\n📊 Outliers Summary:")
            print(f"   • Columns with outliers: {len(outliers_summary)}")
            
            # Sort by outliers count
            outliers_summary.sort(key=lambda x: x['outliers_count'], reverse=True)
            
            print(f"   • Top columns by outliers count:")
            for i, item in enumerate(outliers_summary[:10], 1):
                print(f"     {i:2d}. {item['column']:<25} | {item['outliers_count']:,} ({item['outliers_percent']:.1f}%)")
                print(f"         Q1: {item['q1']:.4f}, Q3: {item['q3']:.4f}, IQR: {item['iqr']:.4f}")
                print(f"         Bounds: [{item['lower_bound']:.4f}, {item['upper_bound']:.4f}]")
            
            if len(outliers_summary) > 10:
                print(f"     ... and {len(outliers_summary) - 10} more columns")
        else:
            print("✅ No outliers detected in numeric columns")
        
        return True

    def run_time_series_gaps_analysis(self, system) -> bool:
        """
        Run detailed time series gaps analysis on preloaded data files.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n⏱️ TIME SERIES GAPS ANALYSIS")
        print("-" * 50)
        
        # Check if data is loaded
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        print(f"📊 Analyzing preloaded data:")
        print(f"   • Main dataset: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
        
        # Check if timeframe info is available
        if hasattr(system, 'timeframe_info') and system.timeframe_info:
            if system.timeframe_info.get('cross_timeframes'):
                print(f"   • Additional timeframes available: {len(system.timeframe_info['cross_timeframes'])}")
        
        print("-" * 50)
        
        all_gap_summaries = []
        
        # Analyze main dataset
        print(f"\n📊 Analyzing main dataset...")
        main_gap_summary = self._analyze_time_series_gaps(system.current_data)
        
        if main_gap_summary:
            # Add dataset info to gap summary
            for gap_info in main_gap_summary:
                gap_info['dataset_name'] = 'Main Dataset'
                gap_info['dataset_type'] = 'current_data'
                gap_info['total_rows'] = len(system.current_data)
            
            all_gap_summaries.extend(main_gap_summary)
            print(f"   ✅ Found gaps in {len(main_gap_summary)} columns")
        else:
            print(f"   ✅ No gaps found in main dataset")
        
        # Analyze additional timeframes if available
        if hasattr(system, 'timeframe_info') and system.timeframe_info:
            cross_timeframes = system.timeframe_info.get('cross_timeframes', {})
            
            if cross_timeframes:
                print(f"\n📊 Analyzing additional timeframes...")
                
                for timeframe, files in cross_timeframes.items():
                    print(f"\n   ⏰ Timeframe: {timeframe}")
                    print(f"      📁 Files: {len(files)}")
                    
                    for i, file_path in enumerate(files, 1):
                        try:
                            print(f"      📊 File {i}/{len(files)}: {Path(file_path).name}")
                            
                            # Load file
                            df = self._load_file_for_gap_analysis(Path(file_path))
                            if df is None:
                                continue
                            
                            # Analyze gaps
                            gap_summary = self._analyze_time_series_gaps(df)
                            
                            if gap_summary:
                                # Add file info to gap summary
                                for gap_info in gap_summary:
                                    gap_info['dataset_name'] = f'{timeframe} Timeframe'
                                    gap_info['dataset_type'] = 'cross_timeframe'
                                    gap_info['file_name'] = Path(file_path).name
                                    gap_info['file_path'] = str(file_path)
                                    gap_info['timeframe'] = timeframe
                                    gap_info['total_rows'] = len(df)
                                
                                all_gap_summaries.extend(gap_summary)
                                print(f"         ✅ Found gaps in {len(gap_summary)} columns")
                            else:
                                print(f"         ✅ No gaps found")
                            
                            # Memory cleanup
                            del df
                            
                        except Exception as e:
                            print(f"         ❌ Error analyzing {Path(file_path).name}: {e}")
                            continue
        
        # Display comprehensive summary
        if all_gap_summaries:
            print(f"\n📊 COMPREHENSIVE TIME SERIES GAPS SUMMARY")
            print("=" * 60)
            
            # Count datasets
            main_dataset_count = len([g for g in all_gap_summaries if g['dataset_type'] == 'current_data'])
            cross_timeframe_count = len([g for g in all_gap_summaries if g['dataset_type'] == 'cross_timeframe'])
            
            print(f"📁 Main dataset gaps: {main_dataset_count}")
            print(f"⏰ Cross-timeframe gaps: {cross_timeframe_count}")
            print(f"🔍 Total gap issues found: {len(all_gap_summaries)}")
            
            # Group by dataset
            datasets_with_gaps = {}
            for gap_info in all_gap_summaries:
                dataset_key = gap_info['dataset_name']
                if dataset_key not in datasets_with_gaps:
                    datasets_with_gaps[dataset_key] = []
                datasets_with_gaps[dataset_key].append(gap_info)
            
            print(f"\n📋 Datasets with gaps: {len(datasets_with_gaps)}")
            
            for dataset_name, gaps in datasets_with_gaps.items():
                print(f"\n📁 {dataset_name}:")
                for gap_info in gaps:
                    print(f"   📅 {gap_info['column']}:")
                    print(f"      • Gaps: {gap_info['gap_count']:,}")
                    print(f"      • Frequency: {gap_info['expected_frequency']}")
                    print(f"      • Rows: {gap_info['total_rows']:,}")
                    
                    # Show additional info for cross-timeframe data
                    if gap_info.get('timeframe'):
                        print(f"      • Timeframe: {gap_info['timeframe']}")
                        print(f"      • File: {gap_info['file_name']}")
        else:
            print("\n✅ No time series gaps detected in any preloaded data")
        
        return True

    def _load_file_for_gap_analysis(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Load file for gap analysis.
        
        Args:
            file_path: Path to file
            
        Returns:
            DataFrame or None if loading failed
        """
        try:
            df = None
            if file_path.suffix.lower() == '.csv':
                # For CSV files, try to read with different encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(file_path, nrows=10000, encoding=encoding)  # Sample for analysis
                        break
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        print(f"      ⚠️  Error reading CSV: {e}")
                        continue
            elif file_path.suffix.lower() == '.parquet':
                try:
                    df = pd.read_parquet(file_path)
                except Exception as e:
                    print(f"      ⚠️  Error reading parquet: {e}")
                    return None
            
            if df is None or len(df) == 0:
                print(f"      ⚠️  Could not load file or file is empty")
                return None
            
            # Check if file has any timestamp columns
            timestamp_cols = [col for col in df.columns if 'time' in col.lower() or 'date' in col.lower()]
            if not timestamp_cols:
                print(f"      ⚠️  No timestamp columns found")
                return None
            
            print(f"      📊 Loaded {len(df):,} rows × {len(df.columns)} columns")
            return df
            
        except Exception as e:
            print(f"      ❌ Error loading file: {e}")
            return None
