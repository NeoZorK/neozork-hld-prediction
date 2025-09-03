# -*- coding: utf-8 -*-
# src/interactive/analysis_runner.py
#!/usr/bin/env python3
"""
Main analysis runner for interactive data analysis.
Coordinates EDA, data quality checks, and issue resolution.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from ..eda import EDAAnalyzer
from ..data.data_fixer import DataFixer


class AnalysisRunner:
    """Main analysis runner coordinating all analysis operations."""
    
    def __init__(self, system: 'InteractiveSystem'):
        """
        Initialize AnalysisRunner.
        
        Args:
            system: InteractiveSystem instance
        """
        self.system = system
        self.eda_analyzer = EDAAnalyzer()
        self.data_fixer = DataFixer()
    
    def run_eda_analysis(self, system):
        """
        Run comprehensive EDA analysis with interactive menu.
        
        Args:
            system: InteractiveSystem instance
        """
        print(f"\n🔍 EXPLORATORY DATA ANALYSIS (EDA)")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
        
        print(f"📊 Dataset: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
        
        while True:
            # Show EDA menu
            system.menu_manager.print_eda_menu()
            
            try:
                choice = input("Select EDA option (0-15): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            # Handle exit commands
            if choice.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using EDA Analysis!")
                break
            
            if choice == '00':
                print("\n🏠 Returning to Main Menu...")
                break
            elif choice == '0':
                print("\n🔙 Returning to Main Menu...")
                break
            elif choice == '1':
                print(f"\n⏱️ TIME SERIES GAPS ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_time_series_gaps_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'time_series_gaps_analysis')
            elif choice == '2':
                print(f"\n🔄 DUPLICATES ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_duplicates_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'duplicates_analysis')
            elif choice == '3':
                print(f"\n🧹 COMPREHENSIVE DATA QUALITY CHECK")
                print("-" * 50)
                nan_summary, dupe_summary, gap_summary = self.eda_analyzer.run_comprehensive_data_quality_check(system)
                system.menu_manager.mark_menu_as_used('eda', 'comprehensive_data_quality_check')
            elif choice == '4':
                print(f"\n📊 BASIC STATISTICS")
                print("-" * 50)
                success = self.eda_analyzer.run_basic_statistics(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'basic_statistics')
            elif choice == '5':
                print(f"\n🔗 CORRELATION ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_correlation_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'correlation_analysis')
            elif choice == '6':
                print(f"\n📈 TIME SERIES ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_time_series_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'time_series_analysis')
            elif choice == '7':
                print(f"\n🎯 FEATURE IMPORTANCE")
                print("-" * 50)
                success = self.eda_analyzer.run_feature_importance_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'feature_importance')
            elif choice == '8':
                print(f"\n❓ NAN ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_nan_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'nan_analysis')
            elif choice == '9':
                print(f"\n0️⃣ ZERO ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_zero_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'zero_analysis')
            elif choice == '10':
                print(f"\n➖ NEGATIVE ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_negative_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'negative_analysis')
            elif choice == '11':
                print(f"\n♾️ INFINITY ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_infinity_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'infinity_analysis')
            elif choice == '12':
                print(f"\n📊 OUTLIERS ANALYSIS")
                print("-" * 50)
                success = self.eda_analyzer.run_outliers_analysis(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'outliers_analysis')
            elif choice == '13':
                print(f"\n📋 GENERATE HTML REPORT")
                print("-" * 50)
                success = self.generate_html_report(system)
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'generate_html_report')
            elif choice == '14':
                print(f"\n🔄 RESTORE FROM BACKUP")
                print("-" * 50)
                success = system.restore_from_backup()
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'restore_from_backup')
            elif choice == '15':
                print(f"\n🗑️ CLEAR DATA BACKUP")
                print("-" * 50)
                success = system.clear_data_backup()
                if success:
                    system.menu_manager.mark_menu_as_used('eda', 'clear_data_backup')
            else:
                print("❌ Invalid choice. Please select 0-15.")
            
            if choice not in ['0', '00']:
                try:
                    if system.safe_input() is None:
                        break
                except EOFError:
                    print("\n👋 Goodbye!")
                    break
    
    def run_basic_statistics(self, system) -> bool:
        """
        Run basic statistical analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.eda_analyzer.run_basic_statistics(system)
    
    def run_comprehensive_data_quality_check(self, system) -> Tuple[Dict, Dict, Dict]:
        """
        Run comprehensive data quality check.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            Tuple of (nan_summary, dupe_summary, gap_summary)
        """
        return self.eda_analyzer.run_comprehensive_data_quality_check(system)
    
    def run_correlation_analysis(self, system) -> bool:
        """
        Run correlation analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.eda_analyzer.run_correlation_analysis(system)
    
    def run_time_series_analysis(self, system) -> bool:
        """
        Run time series analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        return self.eda_analyzer.run_time_series_analysis(system)
    
    def fix_data_issues(self, system, nan_summary: List[Dict], 
                        dupe_summary: Dict, gap_summary: List[Dict]) -> bool:
        """
        Fix data quality issues.
        
        Args:
            system: InteractiveSystem instance
            nan_summary: Missing values summary
            dupe_summary: Duplicates summary
            gap_summary: Time series gaps summary
            
        Returns:
            bool: True if successful
        """
        return self.data_fixer.fix_data_issues(system, nan_summary, dupe_summary, gap_summary)
    
    def run_outlier_detection(self, system) -> bool:
        """
        Run outlier detection analysis.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🎯 OUTLIER DETECTION")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        df = system.current_data
        
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            print("❌ No numeric columns found for outlier detection")
            return False
        
        print(f"📊 Analyzing {len(numeric_cols)} numeric columns for outliers...")
        
        # Use IQR method for outlier detection
        outliers_summary = []
        
        for col in numeric_cols[:10]:  # Limit to first 10 columns
            try:
                col_data = df[col].dropna()
                if len(col_data) == 0:
                    continue
                
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_count = len(outliers)
                outlier_percent = (outlier_count / len(col_data)) * 100
                
                if outlier_count > 0:
                    outliers_summary.append({
                        'column': col,
                        'outlier_count': outlier_count,
                        'outlier_percent': outlier_percent,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'min_value': col_data.min(),
                        'max_value': col_data.max()
                    })
                    
                    print(f"   ⚠️  {col}: {outlier_count:,} outliers ({outlier_percent:.1f}%)")
                    print(f"      Range: [{lower_bound:.4f}, {upper_bound:.4f}]")
                    print(f"      Actual: [{col_data.min():.4f}, {col_data.max():.4f}]")
                else:
                    print(f"   ✅ {col}: No outliers detected")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing {col}: {e}")
                continue
        
        # Summary
        if outliers_summary:
            print(f"\n📊 OUTLIER DETECTION SUMMARY")
            print("-" * 40)
            print(f"   ⚠️  Columns with outliers: {len(outliers_summary)}")
            total_outliers = sum(item['outlier_count'] for item in outliers_summary)
            print(f"   🎯 Total outliers found: {total_outliers:,}")
            
            # Ask if user wants to handle outliers
            try:
                handle_outliers = input("\nHandle outliers? (y/n, default: n): ").strip().lower()
                if handle_outliers in ['y', 'yes']:
                    self._handle_outliers(system, outliers_summary)
            except EOFError:
                print("⏭️  Skipping outlier handling...")
        else:
            print(f"\n✅ No outliers detected in any numeric columns!")
        
        return True
    
    def _handle_outliers(self, system, outliers_summary: List[Dict]):
        """
        Handle detected outliers.
        
        Args:
            system: InteractiveSystem instance
            outliers_summary: Summary of detected outliers
        """
        print(f"\n🔧 OUTLIER HANDLING")
        print("-" * 40)
        
        print(f"💡 Select outlier handling strategy:")
        print(f"   1. Cap outliers to bounds (recommended)")
        print(f"   2. Remove outlier rows")
        print(f"   3. Log transform (for positive values)")
        print(f"   4. Skip outlier handling")
        
        try:
            choice = input("\nSelect strategy (1-4, default: 1): ").strip()
            if not choice:
                choice = '1'
        except EOFError:
            choice = '1'
        
        if choice == '1':
            self._cap_outliers(system, outliers_summary)
        elif choice == '2':
            self._remove_outliers(system, outliers_summary)
        elif choice == '3':
            self._log_transform_outliers(system, outliers_summary)
        else:
            print("⏭️  Skipping outlier handling...")
    
    def _cap_outliers(self, system, outliers_summary: List[Dict]):
        """Cap outliers to their bounds."""
        print(f"\n🔧 Capping outliers to bounds...")
        
        df = system.current_data
        capped_count = 0
        
        for item in outliers_summary:
            col = item['column']
            lower_bound = item['lower_bound']
            upper_bound = item['upper_bound']
            
            # Count outliers before capping
            outliers_before = df[col][(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            # Cap outliers
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            
            # Count outliers after capping
            outliers_after = df[col][(df[col] < lower_bound) | (df[col] > upper_bound)]
            capped = len(outliers_before) - len(outliers_after)
            capped_count += capped
            
            if capped > 0:
                print(f"   ✅ {col}: Capped {capped:,} outliers")
        
        print(f"\n📊 Outlier capping completed!")
        print(f"   🎯 Total outliers capped: {capped_count:,}")
    
    def _remove_outliers(self, system, outliers_summary: List[Dict]):
        """Remove rows with outliers."""
        print(f"\n🗑️  Removing rows with outliers...")
        
        df = system.current_data
        original_count = len(df)
        
        # Create outlier mask
        outlier_mask = pd.Series([False] * len(df), index=df.index)
        
        for item in outliers_summary:
            col = item['column']
            lower_bound = item['lower_bound']
            upper_bound = item['upper_bound']
            
            col_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_mask |= col_outliers
        
        # Remove outlier rows
        df_clean = df[~outlier_mask]
        removed_count = original_count - len(df_clean)
        
        # Update system data
        system.current_data = df_clean
        
        print(f"\n📊 Outlier removal completed!")
        print(f"   🗑️  Removed {removed_count:,} rows with outliers")
        print(f"   📊 New dataset size: {len(df_clean):,} rows")
    
    def _log_transform_outliers(self, system, outliers_summary: List[Dict]):
        """Apply log transform to handle outliers."""
        print(f"\n📊 Applying log transform to handle outliers...")
        
        df = system.current_data
        transformed_count = 0
        
        for item in outliers_summary:
            col = item['column']
            
            # Check if column has only positive values
            if df[col].min() <= 0:
                print(f"   ⚠️  {col}: Skipping log transform (contains non-positive values)")
                continue
            
            # Apply log transform
            df[f"{col}_log"] = np.log(df[col])
            transformed_count += 1
            print(f"   ✅ {col}: Added log-transformed column {col}_log")
        
        print(f"\n📊 Log transform completed!")
        print(f"   🔄 Transformed columns: {transformed_count}")
    
    def run_model_development(self, system) -> bool:
        """
        Run basic model development.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n🤖 MODEL DEVELOPMENT")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        print(f"📊 Starting basic model development...")
        print(f"   Dataset: {system.current_data.shape[0]:,} rows × {system.current_data.shape[1]} columns")
        
        # This is a placeholder for basic model development
        # In a full implementation, you would add actual ML model training here
        print(f"\n💡 Basic model development framework initialized")
        print(f"   🔧 Ready for feature engineering and model training")
        print(f"   📚 Use Feature Engineering menu to prepare features")
        print(f"   🚀 Model training will be available in future updates")
        
        return True
    
    def generate_html_report(self, system) -> bool:
        """
        Generate HTML report of analysis results.
        
        Args:
            system: InteractiveSystem instance
            
        Returns:
            bool: True if successful
        """
        print(f"\n📄 HTML REPORT GENERATION")
        print("-" * 50)
        
        if not hasattr(system, 'current_data') or system.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return False
        
        print(f"📊 Generating HTML report...")
        
        # This is a placeholder for HTML report generation
        # In a full implementation, you would generate an actual HTML report
        print(f"\n💡 HTML report generation framework initialized")
        print(f"   🔧 Ready for comprehensive report generation")
        print(f"   📚 Report generation will be available in future updates")
        
        return True
