#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis Runner for Interactive System

This module handles all analysis operations including EDA,
statistical analysis, and data quality checks.
"""

import time
from pathlib import Path
from typing import Dict, Any, TYPE_CHECKING

import pandas as pd
import numpy as np
from tqdm import tqdm
import sys
import os

if TYPE_CHECKING:
    from .core import InteractiveSystem

class AnalysisRunner:
    """Handles analysis operations and data processing."""
    
    def __init__(self, system: 'InteractiveSystem'):
        self.system = system
    
    def run_eda_analysis(self, system):
        """Run EDA analysis menu."""
        while True:
            system.menu_manager.print_eda_menu()
            try:
                choice = input("Select option (0-8): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            # Handle exit commands
            if choice.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            
            if choice == '0' or choice == '00':
                break
            elif choice == '1':
                self.run_comprehensive_data_quality_check(system)
            elif choice == '2':
                self.run_basic_statistics(system)
            elif choice == '3':
                self.run_correlation_analysis(system)
            elif choice == '4':
                self.run_time_series_analysis(system)
            elif choice == '5':
                print("⏳ Feature Importance - Coming soon!")
            elif choice == '6':
                self.generate_html_report(system)
            elif choice == '7':
                system.data_manager.restore_from_backup(system)
            elif choice == '8':
                system.data_manager.clear_data_backup(system)
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice not in ['0', '00']:
                if system.safe_input() is None:
                    break
    
    def run_basic_statistics(self, system):
        """Run comprehensive basic statistical analysis."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📊 COMPREHENSIVE BASIC STATISTICS")
        print("=" * 50)
        
        try:
            # Filter out infinite values and handle NaN values
            numeric_data = system.current_data.select_dtypes(include=[np.number]).copy()
            
            # Replace infinite values with NaN to avoid warnings
            numeric_data = numeric_data.replace([np.inf, -np.inf], np.nan)
            
            # Descriptive statistics
            desc_stats = numeric_data.describe()
            
            print("\n📈 DESCRIPTIVE STATISTICS")
            print("-" * 30)
            print(desc_stats)
            
            # Statistical explanations and interpretations
            print("\n🔍 STATISTICAL INTERPRETATIONS")
            print("=" * 50)
            
            for col in numeric_data.columns:
                col_data = numeric_data[col].dropna()
                if len(col_data) == 0:
                    continue
                    
                print(f"\n📊 {col.upper()} ANALYSIS:")
                print("-" * 30)
                
                # Basic statistics
                mean_val = col_data.mean()
                median_val = col_data.median()
                std_val = col_data.std()
                skew_val = col_data.skew()
                kurt_val = col_data.kurtosis()
                q25 = col_data.quantile(0.25)
                q75 = col_data.quantile(0.75)
                iqr = q75 - q25
                range_val = col_data.max() - col_data.min()
                cv = std_val / mean_val if mean_val != 0 else 0
                
                print(f"📈 Basic Statistics:")
                print(f"  • Count: {len(col_data):,} observations")
                print(f"  • Mean: {mean_val:.6f} (average value)")
                print(f"  • Median: {median_val:.6f} (middle value)")
                print(f"  • Standard Deviation: {std_val:.6f} (spread around mean)")
                print(f"  • Range: {range_val:.6f} (max - min)")
                print(f"  • IQR: {iqr:.6f} (Q3 - Q1, middle 50% of data)")
                print(f"  • Coefficient of Variation: {cv:.4f} (std/mean)")
                
                # Interpretations
                print(f"\n🎯 Interpretations:")
                
                # Mean vs Median
                if abs(mean_val - median_val) / mean_val > 0.1:
                    print(f"  ⚠️  Mean ({mean_val:.6f}) differs from median ({median_val:.6f})")
                    print(f"     → Data may be skewed or have outliers")
                else:
                    print(f"  ✅ Mean and median are similar → Data is well-centered")
                
                # Skewness interpretation
                if abs(skew_val) < 0.5:
                    print(f"  ✅ Skewness ({skew_val:.4f}) is low → Data is approximately symmetric")
                elif skew_val > 0.5:
                    print(f"  ⚠️  Positive skewness ({skew_val:.4f}) → Right-tailed distribution")
                    print(f"     → Many small values, few large values")
                else:
                    print(f"  ⚠️  Negative skewness ({skew_val:.4f}) → Left-tailed distribution")
                    print(f"     → Many large values, few small values")
                
                # Kurtosis interpretation
                if abs(kurt_val) < 2:
                    print(f"  ✅ Kurtosis ({kurt_val:.4f}) is moderate → Normal-like tails")
                elif kurt_val > 2:
                    print(f"  ⚠️  High kurtosis ({kurt_val:.4f}) → Heavy tails, more outliers")
                else:
                    print(f"  ⚠️  Low kurtosis ({kurt_val:.4f}) → Light tails, fewer outliers")
                
                # Coefficient of Variation
                if cv > 1:
                    print(f"  ⚠️  High CV ({cv:.4f}) → High relative variability")
                elif cv < 0.1:
                    print(f"  ✅ Low CV ({cv:.4f}) → Low relative variability")
                else:
                    print(f"  ✅ Moderate CV ({cv:.4f}) → Reasonable variability")
                
                # Outlier detection using IQR method
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_pct = len(outliers) / len(col_data) * 100
                
                print(f"\n🔍 Outlier Analysis:")
                print(f"  • Outliers (IQR method): {len(outliers):,} ({outlier_pct:.2f}%)")
                if outlier_pct > 5:
                    print(f"  ⚠️  High outlier percentage → Consider outlier treatment")
                else:
                    print(f"  ✅ Reasonable outlier percentage")
                
                # Recommendations
                print(f"\n💡 Recommendations:")
                recommendations = []
                
                if abs(skew_val) > 1:
                    recommendations.append("Consider log/box-cox transformation for skewed data")
                if kurt_val > 3:
                    recommendations.append("Watch for outliers in heavy-tailed distribution")
                if cv > 1:
                    recommendations.append("Consider standardization for high-variance features")
                if outlier_pct > 5:
                    recommendations.append("Investigate and potentially treat outliers")
                if len(col_data) < 100:
                    recommendations.append("Small sample size - consider collecting more data")
                
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        print(f"  {i}. {rec}")
                else:
                    print(f"  ✅ Data looks good for most analyses")
                
                print(f"\n📈 Next Steps:")
                print(f"  • Run correlation analysis to understand relationships")
                print(f"  • Check for seasonality in time series data")
                print(f"  • Consider feature scaling for machine learning")
                print(f"  • Investigate outliers if percentage is high")
            
            # Import outlier analysis function
            from ..eda.basic_stats import outlier_analysis
            
            # Perform outlier analysis
            outlier_results = outlier_analysis(numeric_data)
            
            # Save results
            system.current_results['comprehensive_basic_statistics'] = {
                'basic_stats': desc_stats.to_dict(),
                'descriptive_stats': desc_stats.to_dict(),
                'distribution_analysis': {
                    'skewness': {col: numeric_data[col].skew() for col in numeric_data.columns},
                    'kurtosis': {col: numeric_data[col].kurtosis() for col in numeric_data.columns}
                },
                'outlier_analysis': outlier_results,
                'summary': {
                    'shape': numeric_data.shape,
                    'memory_usage_mb': numeric_data.memory_usage(deep=True).sum() / 1024 / 1024,
                    'missing_percentage': (numeric_data.isna().sum().sum() / (numeric_data.shape[0] * numeric_data.shape[1])) * 100,
                    'normal_distributions': len([col for col in numeric_data.columns if abs(numeric_data[col].skew()) < 0.5]),
                    'skewed_distributions': len([col for col in numeric_data.columns if abs(numeric_data[col].skew()) >= 0.5])
                }
            }
            
            print("\n✅ Comprehensive basic statistics completed and saved!")
            
            # Ask user if they want to see plots
            try:
                show_plots = input("\n📊 Show Plots Yes/No ? ").strip().lower()
            except (EOFError, OSError):
                # Handle test environment where input is not available
                show_plots = 'n'
            
            if show_plots in ['y', 'yes']:
                print("\n📊 GENERATING VISUALIZATIONS...")
                
                # Create statistics plots with specific fields
                target_fields = ['predicted_high', 'predicted_low', 'pressure', 'pressure_vector']
                available_fields = [field for field in target_fields if field in numeric_data.columns]
                
                if available_fields:
                    # Use only available fields
                    plot_data = numeric_data[available_fields]
                    print(f"   📈 Creating plots for fields: {', '.join(available_fields)}")
                else:
                    # Use all numeric data if target fields not found
                    plot_data = numeric_data
                    print(f"   📈 Creating plots for all numeric fields: {', '.join(numeric_data.columns[:4])}")
                
                # Create plots using visualization manager
                plots_created = system.visualization_manager.create_statistics_plots(system, plot_data)
                
                if plots_created:
                    print("✅ Generated 4 visualization files:")
                    print("   • distributions.png - Distribution analysis")
                    print("   • boxplots.png - Outlier detection")
                    print("   • correlation_heatmap.png - Feature relationships")
                    print("   • statistical_summary.png - Statistical comparisons")
                    
                    # Show plots in browser
                    print("\n🌐 Opening plots in Safari browser...")
                    browser_opened = system.visualization_manager.show_plots_in_browser(system)
                    
                    if browser_opened:
                        print("✅ Plots opened in Safari browser with detailed descriptions")
                    else:
                        print("⚠️  Could not open browser automatically. Check the plots directory manually.")
                else:
                    print("❌ Failed to create plots")
            
            # Check for outliers and ask if user wants to fix them
            has_outliers = False
            outlier_summary = []
            
            for col, result in outlier_results.items():
                if 'error' not in result:
                    iqr_outliers = result['iqr_method']['outlier_percentage']
                    zscore_outliers = result['z_score_method']['outlier_percentage']
                    max_outliers = max(iqr_outliers, zscore_outliers)
                    
                    if max_outliers > 1:  # More than 1% outliers
                        has_outliers = True
                        outlier_summary.append((col, max_outliers))
            
            if has_outliers:
                print(f"\n⚠️  OUTLIER DETECTION SUMMARY:")
                print(f"   Found significant outliers in {len(outlier_summary)} columns:")
                for col, pct in sorted(outlier_summary, key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   • {col}: {pct:.2f}% outliers")
                
                try:
                    fix_outliers = input("\n🛠️  Do you want to fix data outliners ? ").strip().lower()
                except (EOFError, OSError):
                    # Handle test environment where input is not available
                    fix_outliers = 'n'
                
                if fix_outliers in ['y', 'yes']:
                    print("\n🛠️  FIXING DATA OUTLIERS...")
                    
                    # Create backup before fixing
                    backup_data = system.current_data.copy()
                    print("✅ Backup created")
                    
                    # Fix outliers using outlier handler
                    from ..eda.outlier_handler import OutlierHandler
                    outlier_handler = OutlierHandler(system.current_data)
                    
                    fixed_columns = []
                    for col, pct in outlier_summary:
                        if col in system.current_data.columns:
                            try:
                                # Use IQR method for outlier treatment
                                result = outlier_handler.treat_outliers_capping([col], method='iqr')
                                if result['values_capped'] > 0:
                                    fixed_columns.append((col, result['values_capped']))
                                    print(f"   ✅ Fixed {result['values_capped']} outliers in {col}")
                            except Exception as e:
                                print(f"   ❌ Error fixing outliers in {col}: {e}")
                    
                    if fixed_columns:
                        print(f"\n✅ Successfully fixed outliers in {len(fixed_columns)} columns")
                        print("   Summary of fixes:")
                        for col, count in fixed_columns:
                            print(f"   • {col}: {count} outliers capped")
                        
                        # Ask if user wants to keep the fixes
                        try:
                            keep_fixes = input("\nKeep the outlier fixes? (y/n): ").strip().lower()
                        except (EOFError, OSError):
                            keep_fixes = 'y'
                        
                        if keep_fixes in ['y', 'yes']:
                            print("✅ Outlier fixes applied and saved")
                            
                            # Save backup file
                            import time
                            backup_file = f"backup_outliers_{int(time.time())}.csv"
                            backup_path = Path("data/backups") / backup_file
                            backup_path.parent.mkdir(parents=True, exist_ok=True)
                            backup_data.to_csv(backup_path, index=False)
                            
                            # Update results
                            system.current_results['outlier_fixes'] = {
                                'original_shape': backup_data.shape,
                                'current_shape': system.current_data.shape,
                                'fixed_columns': fixed_columns,
                                'backup_file': backup_file
                            }
                        else:
                            # Revert changes
                            system.current_data = backup_data
                            print("🔄 Outlier fixes reverted")
                    else:
                        print("⚠️  No outliers were fixed")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'basic_statistics')
            
        except Exception as e:
            print(f"❌ Error in basic statistics: {e}")
            import traceback
            traceback.print_exc()
    

    
    def run_comprehensive_data_quality_check(self, system):
        """Run comprehensive data quality check using eda_batch_check functionality."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🧹 COMPREHENSIVE DATA QUALITY CHECK")
        print("=" * 50)
        
        try:
            # Import required modules
            from src.eda import data_quality, fix_files, file_info
            
            # Check if DataFrame is too large for quality checks
            memory_mb = data_quality._estimate_memory_usage(system.current_data)
            max_memory_mb = int(os.environ.get('MAX_MEMORY_MB', '4096'))  # Updated to match new settings
            
            # For very large datasets, warn but continue with processing
            if memory_mb > max_memory_mb * 3:  # Updated to match new thresholds
                print(f"📊 Very large dataset detected ({memory_mb}MB)")
                print(f"⚠️  This may take a while and use significant memory...")
                print(f"💡 Processing will use chunked approach and sampling where needed")
                print(f"   • Consider using a smaller dataset for faster results")
                print(f"   • Increase container memory limit if needed")
                print(f"   • Processing will continue with optimizations...")
                print(f"-" * 50)
            
            # Initialize summary lists
            nan_summary = []
            dupe_summary = []
            gap_summary = []
            zero_summary = []
            negative_summary = []
            inf_summary = []
            
            # Get file info for datetime detection
            file_info_data = file_info.get_file_info_from_dataframe(system.current_data)
            
            print("🔍 Running comprehensive data quality checks...")
            print("-" * 50)
            
            # Create simple color classes for compatibility
            class SimpleFore:
                MAGENTA = ""
                YELLOW = ""
                RED = ""
                GREEN = ""
                CYAN = ""
                BLUE = ""
                RESET = ""
            
            class SimpleStyle:
                BRIGHT = ""
                RESET = ""
                RESET_ALL = ""
            
            # Run all data quality checks with memory optimization
            data_quality.nan_check(system.current_data, nan_summary, SimpleFore(), SimpleStyle())
            data_quality.duplicate_check(system.current_data, dupe_summary, SimpleFore(), SimpleStyle())
            data_quality.gap_check(system.current_data, gap_summary, SimpleFore(), SimpleStyle())
            data_quality.zero_check(system.current_data, zero_summary, SimpleFore(), SimpleStyle())
            data_quality.negative_check(system.current_data, negative_summary, SimpleFore(), SimpleStyle())
            data_quality.inf_check(system.current_data, inf_summary, SimpleFore(), SimpleStyle())
            
            # Check if DateTime columns exist and are being used
            datetime_cols = []
            for col in system.current_data.columns:
                if pd.api.types.is_datetime64_any_dtype(system.current_data[col]):
                    datetime_cols.append(col)
            
            if datetime_cols:
                print(f"\n📅 DateTime columns found: {datetime_cols}")
            else:
                print("\n⚠️  No DateTime columns found in the dataset!")
                print("   This may affect time series analysis and gap detection.")
                print("   Consider converting timestamp columns to datetime format.")
                
                # Try to detect potential timestamp columns
                potential_timestamp_cols = []
                for col in system.current_data.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['time', 'date', 'timestamp', 'dt']):
                        potential_timestamp_cols.append(col)
                
                if potential_timestamp_cols:
                    print(f"   Potential timestamp columns found: {potential_timestamp_cols}")
                    print("   Consider converting these to datetime format using pd.to_datetime()")
                    
                    # Ask user if they want to convert timestamp columns
                    try:
                        convert_choice = input("\nDo you want to convert potential timestamp columns to datetime? (y/n): ").strip().lower()
                        
                        if convert_choice in ['y', 'yes']:
                            print("\n🔄 Converting timestamp columns to datetime...")
                            converted_cols = []
                            
                            for col in potential_timestamp_cols:
                                try:
                                    # Try to convert to datetime
                                    original_dtype = system.current_data[col].dtype
                                    system.current_data[col] = pd.to_datetime(system.current_data[col], errors='coerce')
                                    
                                    # Check if conversion was successful
                                    if pd.api.types.is_datetime64_any_dtype(system.current_data[col]):
                                        converted_cols.append(col)
                                        print(f"   ✅ Converted '{col}' from {original_dtype} to datetime")
                                    else:
                                        print(f"   ❌ Failed to convert '{col}' to datetime")
                                except Exception as e:
                                    print(f"   ❌ Error converting '{col}': {e}")
                            
                            if converted_cols:
                                print(f"\n✅ Successfully converted {len(converted_cols)} columns to datetime format")
                                datetime_cols.extend(converted_cols)
                            else:
                                print("\n❌ No columns were successfully converted")
                        else:
                            print("\n⏭️  Skipping timestamp conversion")
                    except EOFError:
                        print("\n⏭️  Skipping timestamp conversion due to input error")
            
            # Summary of issues found
            total_issues = len(nan_summary) + len(dupe_summary) + len(gap_summary) + len(zero_summary) + len(negative_summary) + len(inf_summary)
            
            print(f"\n📊 QUALITY CHECK SUMMARY:")
            print(f"   • NaN issues: {len(nan_summary)}")
            print(f"   • Duplicate issues: {len(dupe_summary)}")
            print(f"   • Gap issues: {len(gap_summary)}")
            print(f"   • Zero value issues: {len(zero_summary)}")
            print(f"   • Negative value issues: {len(negative_summary)}")
            print(f"   • Infinity issues: {len(inf_summary)}")
            print(f"   • Total issues found: {total_issues}")
            
            # Ask user if they want to fix all issues
            if total_issues > 0:
                print(f"\n🔧 ISSUES DETECTED - FIX OPTIONS:")
                print("   • Option 1: Fix all issues automatically")
                print("   • Option 2: Review and fix issues individually")
                print("   • Option 3: Skip fixing for now")
                
                try:
                    fix_choice = input("\nDo you want to fix all issues? (y/n/skip): ").strip().lower()
                    
                    if fix_choice in ['y', 'yes']:
                        print("\n🔧 FIXING ALL DETECTED ISSUES...")
                        print("-" * 50)
                        
                        # Create backup before fixing
                        backup_data = system.current_data.copy()
                        
                        # Fix all issues with additional duplicate removal after each fix
                        if nan_summary:
                            print("   • Fixing NaN values...")
                            fixed_data = fix_files.fix_nan(system.current_data, nan_summary)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                # Remove any new duplicates created by NaN fixing
                                initial_dupes = system.current_data.duplicated().sum()
                                if initial_dupes > 0:
                                    system.current_data = system.current_data.drop_duplicates(keep='first')
                                    final_dupes = system.current_data.duplicated().sum()
                                    removed_dupes = initial_dupes - final_dupes
                                    if removed_dupes > 0:
                                        print(f"   🔄 Removed {removed_dupes} new duplicate rows created by NaN fixing")
                                print(f"   ✅ NaN values fixed. Data shape: {system.current_data.shape}")
                        
                        if dupe_summary:
                            print("   • Fixing duplicate rows...")
                            fixed_data = fix_files.fix_duplicates(system.current_data, dupe_summary)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                print(f"   ✅ Duplicate rows fixed. Data shape: {system.current_data.shape}")
                        
                        if gap_summary:
                            print("   • Fixing time series gaps...")
                            # Find datetime column
                            datetime_col = None
                            for col in system.current_data.columns:
                                if pd.api.types.is_datetime64_any_dtype(system.current_data[col]):
                                    datetime_col = col
                                    break
                            fixed_data = fix_files.fix_gaps(system.current_data, gap_summary, datetime_col)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                # Remove any new duplicates created by gap fixing
                                initial_dupes = system.current_data.duplicated().sum()
                                if initial_dupes > 0:
                                    system.current_data = system.current_data.drop_duplicates(keep='first')
                                    final_dupes = system.current_data.duplicated().sum()
                                    removed_dupes = initial_dupes - final_dupes
                                    if removed_dupes > 0:
                                        print(f"   🔄 Removed {removed_dupes} new duplicate rows created by gap fixing")
                                print(f"   ✅ Time series gaps fixed. Data shape: {system.current_data.shape}")
                        
                        if zero_summary:
                            print("   • Fixing zero values...")
                            fixed_data = fix_files.fix_zeros(system.current_data, zero_summary)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                # Remove any new duplicates created by zero fixing
                                initial_dupes = system.current_data.duplicated().sum()
                                if initial_dupes > 0:
                                    system.current_data = system.current_data.drop_duplicates(keep='first')
                                    final_dupes = system.current_data.duplicated().sum()
                                    removed_dupes = initial_dupes - final_dupes
                                    if removed_dupes > 0:
                                        print(f"   🔄 Removed {removed_dupes} new duplicate rows created by zero fixing")
                                print(f"   ✅ Zero values fixed. Data shape: {system.current_data.shape}")
                        
                        if negative_summary:
                            print("   • Fixing negative values...")
                            fixed_data = fix_files.fix_negatives(system.current_data, negative_summary)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                # Remove any new duplicates created by negative fixing
                                initial_dupes = system.current_data.duplicated().sum()
                                if initial_dupes > 0:
                                    system.current_data = system.current_data.drop_duplicates(keep='first')
                                    final_dupes = system.current_data.duplicated().sum()
                                    removed_dupes = initial_dupes - final_dupes
                                    if removed_dupes > 0:
                                        print(f"   🔄 Removed {removed_dupes} new duplicate rows created by negative fixing")
                                print(f"   ✅ Negative values fixed. Data shape: {system.current_data.shape}")
                        
                        if inf_summary:
                            print("   • Fixing infinity values...")
                            fixed_data = fix_files.fix_infs(system.current_data, inf_summary)
                            if fixed_data is not None:
                                system.current_data = fixed_data
                                # Remove any new duplicates created by infinity fixing
                                initial_dupes = system.current_data.duplicated().sum()
                                if initial_dupes > 0:
                                    system.current_data = system.current_data.drop_duplicates(keep='first')
                                    final_dupes = system.current_data.duplicated().sum()
                                    removed_dupes = initial_dupes - final_dupes
                                    if removed_dupes > 0:
                                        print(f"   🔄 Removed {removed_dupes} new duplicate rows created by infinity fixing")
                                print(f"   ✅ Infinity values fixed. Data shape: {system.current_data.shape}")
                        
                        # Final duplicate removal to ensure no duplicates remain
                        final_dupe_check = system.current_data.duplicated().sum()
                        if final_dupe_check > 0:
                            print(f"   • Final duplicate removal...")
                            system.current_data = system.current_data.drop_duplicates(keep='first')
                            print(f"   ✅ Removed {final_dupe_check} remaining duplicate rows")
                        
                        print("\n✅ All issues have been fixed!")
                        print(f"   • Original data shape: {backup_data.shape}")
                        print(f"   • Fixed data shape: {system.current_data.shape}")
                        
                        # Verify that fixes were applied and continue fixing if needed
                        print("\n🔍 Verifying fixes...")
                        remaining_issues = 0
                        max_iterations = 5  # Prevent infinite loops
                        iteration = 1
                        
                        while iteration <= max_iterations:
                            print(f"\n🔄 Verification iteration {iteration}/{max_iterations}")
                            
                            # Check for remaining issues
                            remaining_issues = 0
                            
                            # Check for remaining NaN values
                            nan_count = system.current_data.isna().sum().sum()
                            if nan_count > 0:
                                print(f"   ⚠️  {nan_count} NaN values still remain")
                                remaining_issues += 1
                            
                            # Check for remaining duplicates
                            dup_count = system.current_data.duplicated().sum()
                            if dup_count > 0:
                                print(f"   ⚠️  {dup_count} duplicate rows still remain")
                                remaining_issues += 1
                            else:
                                print(f"   ✅ No duplicate rows remain")
                            
                            # Note: We don't check for duplicated values in metadata columns as they are expected
                            
                            # Check for remaining negative values in OHLCV columns (exclude pressure_vector)
                            ohlcv_cols = [col for col in system.current_data.columns if any(keyword in col.lower() for keyword in ['open', 'high', 'low', 'close', 'volume'])]
                            for col in ohlcv_cols:
                                # Skip pressure_vector as it can legitimately be negative
                                if col.lower() == 'pressure_vector':
                                    continue
                                if pd.api.types.is_numeric_dtype(system.current_data[col]):
                                    neg_count = (system.current_data[col] < 0).sum()
                                    if neg_count > 0:
                                        print(f"   ⚠️  {neg_count} negative values still remain in {col}")
                                        remaining_issues += 1
                            
                            # Check for remaining infinity values
                            inf_count = np.isinf(system.current_data.select_dtypes(include=[np.number])).sum().sum()
                            if inf_count > 0:
                                print(f"   ⚠️  {inf_count} infinity values still remain")
                                remaining_issues += 1
                            
                            # Check for remaining zero values in problematic columns
                            zero_issues = 0
                            for col in system.current_data.select_dtypes(include=[np.number]).columns:
                                if any(keyword in col.lower() for keyword in ['predicted', 'pressure']):
                                    zero_count = (system.current_data[col] == 0).sum()
                                    if zero_count > 0:
                                        print(f"   ⚠️  {zero_count} zero values still remain in {col}")
                                        zero_issues += 1
                            remaining_issues += zero_issues
                            
                            if remaining_issues == 0:
                                print("   ✅ All issues have been successfully resolved!")
                                break
                            else:
                                print(f"   ⚠️  {remaining_issues} types of issues still remain")
                                
                                if iteration < max_iterations:
                                    print(f"\n🔄 Automatically fixing remaining issues (iteration {iteration + 1})...")
                                    
                                    # Re-run quality checks to get updated summaries
                                    nan_summary = []
                                    dupe_summary = []
                                    gap_summary = []
                                    zero_summary = []
                                    negative_summary = []
                                    inf_summary = []
                                    
                                    # Re-run all quality checks
                                    data_quality.nan_check(system.current_data, nan_summary, SimpleFore(), SimpleStyle())
                                    data_quality.duplicate_check(system.current_data, dupe_summary, SimpleFore(), SimpleStyle())
                                    data_quality.gap_check(system.current_data, gap_summary, SimpleFore(), SimpleStyle())
                                    data_quality.zero_check(system.current_data, zero_summary, SimpleFore(), SimpleStyle())
                                    data_quality.negative_check(system.current_data, negative_summary, SimpleFore(), SimpleStyle())
                                    data_quality.inf_check(system.current_data, inf_summary, SimpleFore(), SimpleStyle())
                                    
                                    # Apply fixes for remaining issues
                                    if nan_summary:
                                        print("   • Fixing remaining NaN values...")
                                        fixed_data = fix_files.fix_nan(system.current_data, nan_summary)
                                        if fixed_data is not None:
                                            system.current_data = fixed_data
                                            print(f"   ✅ NaN values fixed. Data shape: {system.current_data.shape}")
                                    
                                    if dupe_summary:
                                        print("   • Fixing remaining duplicate rows...")
                                        fixed_data = fix_files.fix_duplicates(system.current_data, dupe_summary)
                                        if fixed_data is not None:
                                            system.current_data = fixed_data
                                            print(f"   ✅ Duplicate rows fixed. Data shape: {system.current_data.shape}")
                                    
                                    if zero_summary:
                                        print("   • Fixing remaining zero values...")
                                        fixed_data = fix_files.fix_zeros(system.current_data, zero_summary)
                                        if fixed_data is not None:
                                            system.current_data = fixed_data
                                            # Remove any new duplicates created by zero fixing
                                            initial_dupes = system.current_data.duplicated().sum()
                                            if initial_dupes > 0:
                                                system.current_data = system.current_data.drop_duplicates(keep='first')
                                                print(f"   🔄 Removed {initial_dupes} new duplicate rows created by zero fixing")
                                            print(f"   ✅ Zero values fixed. Data shape: {system.current_data.shape}")
                                    
                                    if negative_summary:
                                        print("   • Fixing remaining negative values...")
                                        fixed_data = fix_files.fix_negatives(system.current_data, negative_summary)
                                        if fixed_data is not None:
                                            system.current_data = fixed_data
                                            # Remove any new duplicates created by negative fixing
                                            initial_dupes = system.current_data.duplicated().sum()
                                            if initial_dupes > 0:
                                                system.current_data = system.current_data.drop_duplicates(keep='first')
                                                print(f"   🔄 Removed {initial_dupes} new duplicate rows created by negative fixing")
                                            print(f"   ✅ Negative values fixed. Data shape: {system.current_data.shape}")
                                    
                                    if inf_summary:
                                        print("   • Fixing remaining infinity values...")
                                        fixed_data = fix_files.fix_infs(system.current_data, inf_summary)
                                        if fixed_data is not None:
                                            system.current_data = fixed_data
                                            # Remove any new duplicates created by infinity fixing
                                            initial_dupes = system.current_data.duplicated().sum()
                                            if initial_dupes > 0:
                                                system.current_data = system.current_data.drop_duplicates(keep='first')
                                                print(f"   🔄 Removed {initial_dupes} new duplicate rows created by infinity fixing")
                                            print(f"   ✅ Infinity values fixed. Data shape: {system.current_data.shape}")
                                    
                                    # Final duplicate removal
                                    final_dupe_check = system.current_data.duplicated().sum()
                                    if final_dupe_check > 0:
                                        print(f"   • Final duplicate removal...")
                                        system.current_data = system.current_data.drop_duplicates(keep='first')
                                        print(f"   ✅ Removed {final_dupe_check} remaining duplicate rows")
                                else:
                                    print(f"   ⚠️  Maximum iterations ({max_iterations}) reached. Some issues may remain.")
                                    break
                            
                            iteration += 1
                        
                        # Save backup
                        backup_path = os.path.join('data', 'backups', f'data_backup_{int(time.time())}.parquet')
                        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                        backup_data.to_parquet(backup_path)
                        print(f"   • Backup saved to: {backup_path}")
                        
                        # Save fixed data
                        fixed_data_path = os.path.join('data', 'backups', f'data_fixed_{int(time.time())}.parquet')
                        system.current_data.to_parquet(fixed_data_path)
                        print(f"   • Fixed data saved to: {fixed_data_path}")
                        
                    elif fix_choice in ['n', 'no']:
                        self.show_individual_fix_menu(system, nan_summary, dupe_summary, gap_summary, 
                                                    zero_summary, negative_summary, inf_summary)
                        
                    else:
                        print("\n⏭️  Skipping fixes for now. You can run fixes later.")
                        
                except EOFError:
                    print("\n⏭️  Skipping fixes due to input error.")
            
            # Save results
            system.current_results['comprehensive_data_quality'] = {
                'nan_issues': nan_summary,
                'duplicate_issues': dupe_summary,
                'gap_issues': gap_summary,
                'zero_issues': zero_summary,
                'negative_issues': negative_summary,
                'infinity_issues': inf_summary,
                'total_issues': total_issues,
                'datetime_columns': datetime_cols,
                'data_shape': system.current_data.shape
            }
            
            print(f"\n✅ Comprehensive data quality check completed!")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'comprehensive_data_quality_check')
            
        except Exception as e:
            print(f"❌ Error in comprehensive data quality check: {e}")
            import traceback
            traceback.print_exc()
    
    def run_correlation_analysis(self, system):
        """Run correlation analysis."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🔗 CORRELATION ANALYSIS")
        print("-" * 30)
        
        try:
            numeric_data = system.current_data.select_dtypes(include=[np.number])
            
            if numeric_data.shape[1] < 2:
                print("❌ Insufficient numeric columns for correlation analysis")
                return
            
            # Pearson correlation
            pearson_corr = numeric_data.corr(method='pearson')
            
            # High correlation pairs
            high_corr_pairs = []
            for i in range(len(pearson_corr.columns)):
                for j in range(i+1, len(pearson_corr.columns)):
                    corr_value = pearson_corr.iloc[i, j]
                    if abs(corr_value) > 0.8:
                        high_corr_pairs.append({
                            'col1': pearson_corr.columns[i],
                            'col2': pearson_corr.columns[j],
                            'correlation': corr_value
                        })
            
            print(f"📊 Correlation Analysis Results:")
            print(f"  Matrix size: {pearson_corr.shape[0]} × {pearson_corr.shape[1]}")
            print(f"  High correlation pairs (|r| > 0.8): {len(high_corr_pairs)}")
            
            if high_corr_pairs:
                print(f"  Top high correlation pairs:")
                for i, pair in enumerate(high_corr_pairs[:5], 1):
                    print(f"    {i}. {pair['col1']} ↔ {pair['col2']}: {pair['correlation']:.3f}")
            
            # Save results
            system.current_results['correlation_analysis'] = {
                'pearson_correlation': pearson_corr.to_dict(),
                'high_correlation_pairs': high_corr_pairs
            }
            
            print("\n✅ Correlation analysis completed and saved!")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'correlation_analysis')
            
        except Exception as e:
            print(f"❌ Error in correlation analysis: {e}")
    
    def run_time_series_analysis(self, system):
        """Run time series analysis."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📈 TIME SERIES ANALYSIS")
        print("-" * 30)
        
        try:
            # Get column to analyze
            numeric_cols = system.current_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                print("❌ No numeric columns found in data")
                return
                
            print(f"📊 Available numeric columns: {list(numeric_cols)}")
            
            if len(numeric_cols) == 1:
                column = numeric_cols[0]
                print(f"🎯 Using column: {column}")
            else:
                column = input(f"Enter column to analyze ({', '.join(numeric_cols)}): ").strip()
                if column not in numeric_cols:
                    print(f"❌ Invalid column. Using first column: {numeric_cols[0]}")
                    column = numeric_cols[0]
            
            # Basic time series analysis
            print(f"\n🔍 Starting time series analysis for column: {column}")
            print("   This will include:")
            print("   • Trend analysis (linear, moving averages)")
            print("   • Seasonality detection (decomposition, FFT)")
            print("   • Volatility analysis (clustering, persistence)")
            print("   • Autocorrelation analysis (ACF, PACF)")
            print("   • Forecasting (naive, seasonal, ARIMA)")
            print("   • Summary and recommendations")
            
            # Perform basic analysis
            col_data = system.current_data[column].dropna()
            
            if len(col_data) == 0:
                print("❌ No valid data for analysis")
                return
            
            # Basic statistics
            mean_val = col_data.mean()
            std_val = col_data.std()
            trend = np.polyfit(range(len(col_data)), col_data, 1)[0]
            
            print(f"\n📋 ANALYSIS SUMMARY:")
            print("-" * 30)
            print(f"   • Mean: {mean_val:.6f}")
            print(f"   • Standard Deviation: {std_val:.6f}")
            print(f"   • Linear Trend: {trend:.6f} per observation")
            
            if trend > 0:
                print(f"   • Trend Direction: Upward")
            elif trend < 0:
                print(f"   • Trend Direction: Downward")
            else:
                print(f"   • Trend Direction: No clear trend")
            
            # Save results
            system.current_results['time_series_analysis'] = {
                'column': column,
                'mean': mean_val,
                'std': std_val,
                'trend': trend,
                'trend_direction': 'upward' if trend > 0 else 'downward' if trend < 0 else 'no_trend',
                'data_points': len(col_data)
            }
            
            print(f"\n✅ Time series analysis completed!")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'time_series_analysis')
            
        except Exception as e:
            print(f"❌ Error in time series analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def fix_data_issues(self, system):
        """Fix common data quality issues in the current dataset."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🛠️  FIX DATA ISSUES")
        print("-" * 30)
        
        try:
            # Create backup
            backup_data = system.current_data.copy()
            print("✅ Backup created")
            
            # Check for issues
            print("\n🔍 Checking for data issues...")
            
            # NaN values
            nan_cols = [col for col in system.current_data.columns if system.current_data[col].isna().any()]
            if nan_cols:
                print(f"   Found NaN values in {len(nan_cols)} columns: {nan_cols}")
                # Simple fix: fill with median for numeric, mode for categorical
                for col in nan_cols:
                    if pd.api.types.is_numeric_dtype(system.current_data[col]):
                        median_val = system.current_data[col].median()
                        system.current_data[col] = system.current_data[col].fillna(median_val)
                    else:
                        mode_val = system.current_data[col].mode().iloc[0] if not system.current_data[col].mode().empty else ""
                        system.current_data[col] = system.current_data[col].fillna(mode_val)
                print("   ✅ NaN values fixed")
            else:
                print("   ✅ No NaN values found")
            
            # Duplicates
            duplicates = system.current_data.duplicated().sum()
            if duplicates > 0:
                print(f"   Found {duplicates} duplicate rows")
                system.current_data = system.current_data.drop_duplicates(keep='first')
                print("   ✅ Duplicates removed")
            else:
                print("   ✅ No duplicates found")
            
            print(f"\n✅ Data issues check completed!")
            print(f"   Original shape: {backup_data.shape}")
            print(f"   Current shape: {system.current_data.shape}")
            
            # Ask if user wants to keep changes
            try:
                keep_changes = input("\nKeep the fixes? (y/n): ").strip().lower()
            except (EOFError, OSError):
                # Handle test environment where input is not available
                keep_changes = 'y'
            
            if keep_changes in ['y', 'yes']:
                print("✅ Changes applied")
                
                # Create backup file
                backup_file = f"backup_{int(time.time())}.csv"
                backup_path = Path("data/backups") / backup_file
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                backup_data.to_csv(backup_path, index=False)
                
                system.current_results['data_fixes'] = {
                    'original_shape': backup_data.shape,
                    'current_shape': system.current_data.shape,
                    'nan_fixed': len(nan_cols) > 0,
                    'duplicates_removed': duplicates > 0,
                    'backup_file': backup_file
                }
                
                # Mark as used
                system.menu_manager.mark_menu_as_used('eda', 'fix_data_issues')
            else:
                system.current_data = backup_data
                print("🔄 Changes reverted")
                
        except Exception as e:
            print(f"❌ Error fixing data issues: {e}")
            import traceback
            traceback.print_exc()
    
    def generate_html_report(self, system):
        """Generate comprehensive HTML report for current data and analysis."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📋 GENERATE HTML REPORT")
        print("-" * 30)
        
        try:
            # Create reports directory
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_title = f"Interactive System Analysis Report - {timestamp}"
            
            # Create simple HTML report
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #e8f4f8; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{report_title}</h1>
        <p>Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>Data Overview</h2>
        <div class="metric">Shape: {system.current_data.shape[0]} rows × {system.current_data.shape[1]} columns</div>
        <div class="metric">Memory: {system.current_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB</div>
    </div>
"""
            
            # Add analysis results
            if system.current_results:
                html_content += """
    <div class="section">
        <h2>Analysis Results</h2>
"""
                
                # Add Data Quality Analysis section
                if 'comprehensive_data_quality' in system.current_results or 'data_quality' in system.current_results:
                    html_content += """
    <div class="section">
        <h2>Data Quality Analysis</h2>
"""
                    quality_data = system.current_results.get('comprehensive_data_quality', system.current_results.get('data_quality', {}))
                    html_content += f"        <p><strong>Total Rows:</strong> {quality_data.get('total_rows', 'N/A')}</p>\n"
                    html_content += f"        <p><strong>Total Columns:</strong> {quality_data.get('total_cols', 'N/A')}</p>\n"
                    html_content += f"        <p><strong>Missing Values:</strong> {quality_data.get('missing_values', quality_data.get('total_missing', 'N/A'))} ({quality_data.get('missing_percentage', 'N/A'):.2f}%)</p>\n"
                    html_content += f"        <p><strong>Duplicates:</strong> {quality_data.get('duplicates', 'N/A')} ({quality_data.get('duplicate_percentage', 'N/A'):.2f}%)</p>\n"
                    html_content += "    </div>\n"
                
                # Add other analysis results
                for key, value in system.current_results.items():
                    if key != 'comprehensive_data_quality':  # Skip as it's handled above
                        html_content += f"        <h3>{key.replace('_', ' ').title()}</h3>\n"
                        if isinstance(value, dict):
                            for k, v in value.items():
                                if k != 'data_with_features':
                                    html_content += f"        <p><strong>{k}:</strong> {v}</p>\n"
                        else:
                            html_content += f"        <p>{value}</p>\n"
                
                html_content += "    </div>\n"
            
            html_content += """
</body>
</html>
"""
            
            # Save report
            report_path = reports_dir / f"interactive_report_{timestamp}.html"
            with open(report_path, 'w') as f:
                f.write(html_content)
            
            print(f"✅ HTML report generated: {report_path}")
            print(f"   Open the file in your web browser to view the complete report")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'generate_html_report')
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            import traceback
            traceback.print_exc()
    
    def run_outlier_detection(self, system):
        """Run outlier detection analysis."""
        if system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🔍 OUTLIER DETECTION ANALYSIS")
        print("=" * 50)
        
        try:
            from src.eda.outlier_handler import OutlierHandler
            
            # Create outlier handler
            outlier_handler = OutlierHandler(system.current_data)
            
            # Get numeric columns
            numeric_cols = system.current_data.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_cols:
                print("❌ No numeric columns found for outlier detection.")
                return
            
            print(f"📊 Analyzing {len(numeric_cols)} numeric columns for outliers...")
            print("-" * 50)
            
            outlier_results = {}
            
            for col in numeric_cols:
                print(f"\n🔍 Analyzing column: {col}")
                
                # IQR method
                iqr_mask, iqr_stats = outlier_handler.detect_outliers_iqr(col)
                iqr_count = iqr_mask.sum()
                
                # Z-score method
                zscore_mask, zscore_stats = outlier_handler.detect_outliers_zscore(col)
                zscore_count = zscore_mask.sum()
                
                print(f"   IQR method: {iqr_count} outliers detected")
                print(f"   Z-score method: {zscore_count} outliers detected")
                
                outlier_results[col] = {
                    'iqr_outliers': iqr_count,
                    'zscore_outliers': zscore_count,
                    'iqr_stats': iqr_stats,
                    'zscore_stats': zscore_stats
                }
            
            # Store results
            system.current_results['outlier_detection'] = outlier_results
            
            print(f"\n✅ Outlier detection completed for {len(numeric_cols)} columns")
            print("   Results stored in system.current_results['outlier_detection']")
            
            # Mark as used
            system.menu_manager.mark_menu_as_used('eda', 'outlier_detection')
            
        except Exception as e:
            print(f"❌ Error in outlier detection: {e}")
            import traceback
            traceback.print_exc()
    
    def run_model_development(self, system):
        """Run model development menu."""
        while True:
            system.menu_manager.print_model_development_menu()
            try:
                choice = input("Select option (0-6): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            # Handle exit commands
            if choice.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            
            if choice == '0' or choice == '00':
                break
            elif choice == '1':
                print("⏳ Data Preparation - Coming soon!")
            elif choice == '2':
                print("⏳ Feature Engineering Pipeline - Coming soon!")
            elif choice == '3':
                print("⏳ ML Model Training - Coming soon!")
            elif choice == '4':
                print("⏳ Model Evaluation - Coming soon!")
            elif choice == '5':
                print("⏳ Hyperparameter Tuning - Coming soon!")
            elif choice == '6':
                print("⏳ Model Report - Coming soon!")
            else:
                print("❌ Invalid choice. Please select 0-6.")
            
            if choice not in ['0', '00']:
                if system.safe_input() is None:
                    break
    
    def show_individual_fix_menu(self, system, nan_summary, dupe_summary, gap_summary, 
                                zero_summary, negative_summary, inf_summary):
        """Show individual fix options menu with status indicators."""
        print("\n📋 INDIVIDUAL FIX OPTIONS:")
        print("=" * 50)
        
        # Create backup before any fixes
        backup_data = system.current_data.copy()
        backup_created = False
        
        # Track which fixes have been applied
        fixes_applied = {
            'nan': False,
            'duplicates': False,
            'gaps': False,
            'zeros': False,
            'negatives': False,
            'infinities': False
        }
        
        while True:
            print("\n🔧 Available Fixes:")
            print("0. 🔙 Back to main quality check")
            
            # Show available fixes with status
            option_num = 1
            available_fixes = []
            
            if nan_summary:
                status = " ✅" if fixes_applied['nan'] else ""
                print(f"{option_num}. 🧹 Fix NaN values{status}")
                available_fixes.append(('nan', nan_summary))
                option_num += 1
            
            if dupe_summary:
                status = " ✅" if fixes_applied['duplicates'] else ""
                print(f"{option_num}. 🔄 Fix Duplicates{status}")
                available_fixes.append(('duplicates', dupe_summary))
                option_num += 1
            
            if gap_summary:
                status = " ✅" if fixes_applied['gaps'] else ""
                print(f"{option_num}. 📅 Fix Gaps{status}")
                available_fixes.append(('gaps', gap_summary))
                option_num += 1
            
            if zero_summary:
                status = " ✅" if fixes_applied['zeros'] else ""
                print(f"{option_num}. 🔢 Fix Zeros{status}")
                available_fixes.append(('zeros', zero_summary))
                option_num += 1
            
            if negative_summary:
                status = " ✅" if fixes_applied['negatives'] else ""
                print(f"{option_num}. ➖ Fix Negatives{status}")
                available_fixes.append(('negatives', negative_summary))
                option_num += 1
            
            if inf_summary:
                status = " ✅" if fixes_applied['infinities'] else ""
                print(f"{option_num}. ♾️  Fix Infinities{status}")
                available_fixes.append(('infinities', inf_summary))
                option_num += 1
            
            print(f"{option_num}. 🚀 Fix All Remaining Issues")
            print(f"{option_num + 1}. 📊 Show Current Status")
            
            print("-" * 50)
            
            try:
                choice = input("Select option (0-{}): ".format(option_num + 1)).strip()
            except (EOFError, OSError):
                print("⏭️  Returning to main quality check due to input error.")
                break
            
            if choice == '0':
                # Show summary of applied fixes
                if any(fixes_applied.values()):
                    print(f"\n📊 Summary of applied fixes:")
                    for fix_type, applied in fixes_applied.items():
                        if applied:
                            print(f"   ✅ {fix_type.title()} fix applied")
                    print(f"💾 All backups and fixed data have been saved to data/backups/")
                break
            elif choice == str(option_num):  # Fix All
                print("\n🚀 FIXING ALL REMAINING ISSUES...")
                self.apply_all_remaining_fixes(system, available_fixes, fixes_applied, backup_data, backup_created)
                
                # Show summary of applied fixes
                if any(fixes_applied.values()):
                    print(f"\n📊 Summary of applied fixes:")
                    for fix_type, applied in fixes_applied.items():
                        if applied:
                            print(f"   ✅ {fix_type.title()} fix applied")
                    print(f"💾 All backups and fixed data have been saved to data/backups/")
                break
            elif choice == str(option_num + 1):  # Show Status
                self.show_fix_status(system, available_fixes, fixes_applied)
            elif choice.isdigit() and 1 <= int(choice) <= len(available_fixes):
                fix_index = int(choice) - 1
                fix_type, fix_summary = available_fixes[fix_index]
                backup_created = self.apply_single_fix(system, fix_type, fix_summary, fixes_applied, backup_data, backup_created)
            else:
                print("❌ Invalid choice. Please select a valid option.")
    
    def apply_single_fix(self, system, fix_type, fix_summary, fixes_applied, backup_data=None, backup_created=False):
        """Apply a single fix based on type."""
        try:
            from src.eda import fix_files
            
            print(f"\n🔧 Applying {fix_type} fix...")
            
            # Create and save backup on first fix if not already created
            if not backup_created and backup_data is not None:
                print("💾 Creating backup before applying fixes...")
                try:
                    import time
                    backup_file = f"backup_individual_fixes_{int(time.time())}.parquet"
                    backup_path = Path("data/backups") / backup_file
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    backup_data.to_parquet(backup_path)
                    print(f"💾 Backup saved to: {backup_path}")
                    backup_created = True
                except Exception as e:
                    print(f"⚠️  Could not save backup: {e}")
            
            if fix_type == 'nan':
                fixed_data = fix_files.fix_nan(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['nan'] = True
                    print(f"✅ NaN values fixed. Data shape: {system.current_data.shape}")
            
            elif fix_type == 'duplicates':
                fixed_data = fix_files.fix_duplicates(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['duplicates'] = True
                    print(f"✅ Duplicates fixed. Data shape: {system.current_data.shape}")
            
            elif fix_type == 'gaps':
                fixed_data = fix_files.fix_gaps(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['gaps'] = True
                    print(f"✅ Gaps fixed. Data shape: {system.current_data.shape}")
            
            elif fix_type == 'zeros':
                fixed_data = fix_files.fix_zeros(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['zeros'] = True
                    print(f"✅ Zero values fixed. Data shape: {system.current_data.shape}")
            
            elif fix_type == 'negatives':
                fixed_data = fix_files.fix_negatives(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['negatives'] = True
                    print(f"✅ Negative values fixed. Data shape: {system.current_data.shape}")
            
            elif fix_type == 'infinities':
                fixed_data = fix_files.fix_infs(system.current_data, fix_summary)
                if fixed_data is not None:
                    system.current_data = fixed_data
                    fixes_applied['infinities'] = True
                    print(f"✅ Infinity values fixed. Data shape: {system.current_data.shape}")
            
            # Remove any new duplicates created by the fix
            initial_dupes = system.current_data.duplicated().sum()
            if initial_dupes > 0:
                system.current_data = system.current_data.drop_duplicates(keep='first')
                print(f"🔄 Removed {initial_dupes} new duplicate rows created by {fix_type} fixing")
            
            # Save current fixed data after each fix
            if fixes_applied[fix_type]:
                try:
                    import time
                    fixed_data_path = Path("data/backups") / f"data_fixed_{fix_type}_{int(time.time())}.parquet"
                    system.current_data.to_parquet(fixed_data_path)
                    print(f"💾 Current fixed data saved to: {fixed_data_path}")
                except Exception as e:
                    print(f"⚠️  Could not save current fixed data: {e}")
            
            return backup_created
            
        except Exception as e:
            print(f"❌ Error applying {fix_type} fix: {e}")
            return backup_created
    
    def apply_all_remaining_fixes(self, system, available_fixes, fixes_applied, backup_data=None, backup_created=False):
        """Apply all remaining fixes that haven't been applied yet."""
        try:
            from src.eda import fix_files
            
            # Create and save backup on first fix if not already created
            if not backup_created and backup_data is not None:
                print("💾 Creating backup before applying fixes...")
                try:
                    import time
                    backup_file = f"backup_all_fixes_{int(time.time())}.parquet"
                    backup_path = Path("data/backups") / backup_file
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    backup_data.to_parquet(backup_path)
                    print(f"💾 Backup saved to: {backup_path}")
                    backup_created = True
                except Exception as e:
                    print(f"⚠️  Could not save backup: {e}")
            
            for fix_type, fix_summary in available_fixes:
                if not fixes_applied[fix_type]:
                    print(f"   • Applying {fix_type} fix...")
                    backup_created = self.apply_single_fix(system, fix_type, fix_summary, fixes_applied, backup_data, backup_created)
            
            print("\n✅ All remaining issues have been fixed!")
            
        except Exception as e:
            print(f"❌ Error applying all fixes: {e}")
    
    def show_fix_status(self, system, available_fixes, fixes_applied):
        """Show current status of fixes."""
        print("\n📊 CURRENT FIX STATUS:")
        print("-" * 30)
        
        total_fixes = len(available_fixes)
        applied_fixes = sum(1 for fix_type, _ in available_fixes if fixes_applied[fix_type])
        
        print(f"📈 Progress: {applied_fixes}/{total_fixes} fixes applied")
        print(f"📊 Data shape: {system.current_data.shape}")
        
        for fix_type, fix_summary in available_fixes:
            status = "✅ Applied" if fixes_applied[fix_type] else "⏳ Pending"
            print(f"   • {fix_type.title()}: {status}")
        
        print("-" * 30)
