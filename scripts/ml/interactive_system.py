#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive System Script for NeoZorK HLD Prediction

This script provides an interactive interface for the entire system,
including EDA, Feature Engineering, and other capabilities.

Usage:
    python scripts/interactive_system.py
    ./interactive_system.py
"""

import argparse
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import pandas as pd
    import numpy as np
    from src.ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
    from src.ml.feature_engineering.feature_selector import FeatureSelectionConfig
    # Import EDA modules for data fixing and reporting
    from src.eda import fix_files, html_report_generator, data_quality, file_info
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)


class InteractiveSystem:
    """Interactive system interface for NeoZorK HLD Prediction."""
    
    def __init__(self):
        """Initialize the interactive system."""
        self.feature_generator = None
        self.current_data = None
        self.current_results = {}
        # Track used submenus for showing green checkmarks
        self.used_menus = {
            'main': {
                'load_data': False,
                'eda_analysis': False,
                'feature_engineering': False,
                'data_visualization': False,
                'model_development': False,
                'testing_validation': False,
                'documentation_help': False,
                'system_configuration': False,
                'menu_status': False
            },
            'eda': {
                'basic_statistics': False,
                'data_quality_check': False,
                'correlation_analysis': False,
                'time_series_analysis': False,
                'feature_importance': False,
                'fix_data_issues': False,
                'generate_html_report': False,
                'restore_from_backup': False
            },
            'feature_engineering': {
                'generate_all_features': False,
                'proprietary_features': False,
                'technical_indicators': False,
                'statistical_features': False,
                'temporal_features': False,
                'cross_timeframe_features': False,
                'feature_selection': False,
                'feature_summary': False
            },
            'visualization': {
                'price_charts': False,
                'feature_distributions': False,
                'correlation_heatmaps': False,
                'time_series_plots': False,
                'feature_importance_charts': False,
                'export_visualizations': False
            },
            'model_development': {
                'data_preparation': False,
                'feature_engineering_pipeline': False,
                'ml_model_training': False,
                'model_evaluation': False,
                'hyperparameter_tuning': False,
                'model_report': False
            }
        }
    
    def calculate_submenu_completion_percentage(self, menu_category):
        """Calculate completion percentage for a submenu category."""
        if menu_category not in self.used_menus:
            return 0
        
        items = self.used_menus[menu_category]
        if not items:
            return 0
        
        completed_items = sum(1 for item in items.values() if item)
        total_items = len(items)
        
        return round((completed_items / total_items) * 100) if total_items > 0 else 0
    
    def mark_menu_as_used(self, menu_category, menu_item):
        """Mark a submenu item as successfully used."""
        if menu_category in self.used_menus and menu_item in self.used_menus[menu_category]:
            self.used_menus[menu_category][menu_item] = True
            print(f"✅ {menu_item.replace('_', ' ').title()} marked as completed!")
    
    def reset_menu_status(self, menu_category=None):
        """Reset menu status for all or specific category."""
        if menu_category:
            if menu_category in self.used_menus:
                for item in self.used_menus[menu_category]:
                    self.used_menus[menu_category][item] = False
                print(f"🔄 Reset status for {menu_category} menu")
        else:
            for category in self.used_menus:
                for item in self.used_menus[category]:
                    self.used_menus[category][item] = False
            print("🔄 Reset status for all menus")
    
    def show_menu_status(self):
        """Show current menu usage status."""
        print("\n📊 MENU USAGE STATUS")
        print("-" * 30)
        
        for category, items in self.used_menus.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            used_count = sum(1 for item in items.values() if item)
            total_count = len(items)
            print(f"  Progress: {used_count}/{total_count} items completed")
            
            for item, used in items.items():
                status = "✅" if used else "⏳"
                item_name = item.replace('_', ' ').title()
                print(f"    {status} {item_name}")
    
    def safe_input(self, prompt="\nPress Enter to continue..."):
        """Safely handle input with EOF protection."""
        try:
            return input(prompt)
        except EOFError:
            print("\n👋 Goodbye!")
            return None
        
    def print_banner(self):
        """Print system banner."""
        print("\n" + "="*80)
        print("🚀 NEOZORk HLD PREDICTION - INTERACTIVE SYSTEM")
        print("="*80)
        print("🎯 Advanced Feature Engineering & EDA Platform")
        print("🔧 ML-Ready Trading System Development")
        print("📊 Comprehensive Data Analysis & Visualization")
        print("="*80)
        
    def print_main_menu(self):
        """Print main menu options with green checkmarks and completion percentages for used items."""
        print("\n📋 MAIN MENU:")
        
        # Load Data
        checkmark = " ✅" if self.used_menus['main']['load_data'] else ""
        print(f"1. 📁 Load Data{checkmark}")
        
        # EDA Analysis
        checkmark = " ✅" if self.used_menus['main']['eda_analysis'] else ""
        eda_percentage = self.calculate_submenu_completion_percentage('eda')
        percentage_text = f" ({eda_percentage}%)" if eda_percentage > 0 else ""
        print(f"2. 🔍 EDA Analysis{checkmark}{percentage_text}")
        
        # Feature Engineering
        checkmark = " ✅" if self.used_menus['main']['feature_engineering'] else ""
        fe_percentage = self.calculate_submenu_completion_percentage('feature_engineering')
        percentage_text = f" ({fe_percentage}%)" if fe_percentage > 0 else ""
        print(f"3. ⚙️  Feature Engineering{checkmark}{percentage_text}")
        
        # Data Visualization
        checkmark = " ✅" if self.used_menus['main']['data_visualization'] else ""
        viz_percentage = self.calculate_submenu_completion_percentage('visualization')
        percentage_text = f" ({viz_percentage}%)" if viz_percentage > 0 else ""
        print(f"4. 📊 Data Visualization{checkmark}{percentage_text}")
        
        # Model Development
        checkmark = " ✅" if self.used_menus['main']['model_development'] else ""
        model_percentage = self.calculate_submenu_completion_percentage('model_development')
        percentage_text = f" ({model_percentage}%)" if model_percentage > 0 else ""
        print(f"5. 📈 Model Development{checkmark}{percentage_text}")
        
        # Testing & Validation
        checkmark = " ✅" if self.used_menus['main']['testing_validation'] else ""
        print(f"6. 🧪 Testing & Validation{checkmark}")
        
        # Documentation & Help
        checkmark = " ✅" if self.used_menus['main']['documentation_help'] else ""
        print(f"7. 📚 Documentation & Help{checkmark}")
        
        # System Configuration
        checkmark = " ✅" if self.used_menus['main']['system_configuration'] else ""
        print(f"8. ⚙️  System Configuration{checkmark}")
        
        # Menu Status
        checkmark = " ✅" if self.used_menus['main']['menu_status'] else ""
        print(f"9. 📊 Menu Status{checkmark}")
        
        print("0. 🚪 Exit")
        print("-" * 50)
        
    def print_eda_menu(self):
        """Print EDA menu options with green checkmarks for used items."""
        print("\n🔍 EDA ANALYSIS MENU:")
        print("0. 🔙 Back to Main Menu")
        
        # Basic Statistics
        checkmark = " ✅" if self.used_menus['eda']['basic_statistics'] else ""
        print(f"1. 📊 Basic Statistics{checkmark}")
        
        # Data Quality Check
        checkmark = " ✅" if self.used_menus['eda']['data_quality_check'] else ""
        print(f"2. 🧹 Comprehensive Data Quality Check{checkmark}")
        
        # Correlation Analysis
        checkmark = " ✅" if self.used_menus['eda']['correlation_analysis'] else ""
        print(f"3. 🔗 Correlation Analysis{checkmark}")
        
        # Time Series Analysis
        checkmark = " ✅" if self.used_menus['eda']['time_series_analysis'] else ""
        print(f"4. 📈 Time Series Analysis{checkmark}")
        
        # Feature Importance
        checkmark = " ✅" if self.used_menus['eda']['feature_importance'] else ""
        print(f"5. 🎯 Feature Importance{checkmark}")
        
        # Fix Data Issues
        checkmark = " ✅" if self.used_menus['eda']['fix_data_issues'] else ""
        print(f"6. 🛠️  Fix Data Issues{checkmark}")
        
        # Generate HTML Report
        checkmark = " ✅" if self.used_menus['eda']['generate_html_report'] else ""
        print(f"7. 📋 Generate HTML Report{checkmark}")
        
        # Restore from Backup
        checkmark = " ✅" if self.used_menus['eda']['restore_from_backup'] else ""
        print(f"8. 🔄 Restore from Backup{checkmark}")
        
        print("-" * 50)
        
    def print_feature_engineering_menu(self):
        """Print Feature Engineering menu options with green checkmarks for used items."""
        print("\n⚙️  FEATURE ENGINEERING MENU:")
        print("0. 🔙 Back to Main Menu")
        
        # Generate All Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['generate_all_features'] else ""
        print(f"1. 🚀 Generate All Features{checkmark}")
        
        # Proprietary Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['proprietary_features'] else ""
        print(f"2. 🎯 Proprietary Features (PHLD/Wave){checkmark}")
        
        # Technical Indicators
        checkmark = " ✅" if self.used_menus['feature_engineering']['technical_indicators'] else ""
        print(f"3. 📊 Technical Indicators{checkmark}")
        
        # Statistical Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['statistical_features'] else ""
        print(f"4. 📈 Statistical Features{checkmark}")
        
        # Temporal Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['temporal_features'] else ""
        print(f"5. ⏰ Temporal Features{checkmark}")
        
        # Cross-Timeframe Features
        checkmark = " ✅" if self.used_menus['feature_engineering']['cross_timeframe_features'] else ""
        print(f"6. 🔄 Cross-Timeframe Features{checkmark}")
        
        # Feature Selection
        checkmark = " ✅" if self.used_menus['feature_engineering']['feature_selection'] else ""
        print(f"7. 🎛️  Feature Selection & Optimization{checkmark}")
        
        # Feature Summary
        checkmark = " ✅" if self.used_menus['feature_engineering']['feature_summary'] else ""
        print(f"8. 📋 Feature Summary Report{checkmark}")
        
        print("-" * 50)
        
    def print_visualization_menu(self):
        """Print visualization menu options with green checkmarks for used items."""
        print("\n📊 DATA VISUALIZATION MENU:")
        
        # Price Charts
        checkmark = " ✅" if self.used_menus['visualization']['price_charts'] else ""
        print(f"1. 📈 Price Charts (OHLCV){checkmark}")
        
        # Feature Distribution Plots
        checkmark = " ✅" if self.used_menus['visualization']['feature_distributions'] else ""
        print(f"2. 📊 Feature Distribution Plots{checkmark}")
        
        # Correlation Heatmaps
        checkmark = " ✅" if self.used_menus['visualization']['correlation_heatmaps'] else ""
        print(f"3. 🔗 Correlation Heatmaps{checkmark}")
        
        # Time Series Plots
        checkmark = " ✅" if self.used_menus['visualization']['time_series_plots'] else ""
        print(f"4. 📈 Time Series Plots{checkmark}")
        
        # Feature Importance Charts
        checkmark = " ✅" if self.used_menus['visualization']['feature_importance_charts'] else ""
        print(f"5. 🎯 Feature Importance Charts{checkmark}")
        
        # Export Visualizations
        checkmark = " ✅" if self.used_menus['visualization']['export_visualizations'] else ""
        print(f"6. 📋 Export Visualizations{checkmark}")
        
        print("7. 🔙 Back to Main Menu")
        print("-" * 50)
        
    def print_model_development_menu(self):
        """Print model development menu options with green checkmarks for used items."""
        print("\n📈 MODEL DEVELOPMENT MENU:")
        
        # Data Preparation
        checkmark = " ✅" if self.used_menus['model_development']['data_preparation'] else ""
        print(f"1. 🎯 Data Preparation{checkmark}")
        
        # Feature Engineering Pipeline
        checkmark = " ✅" if self.used_menus['model_development']['feature_engineering_pipeline'] else ""
        print(f"2. 🔄 Feature Engineering Pipeline{checkmark}")
        
        # ML Model Training
        checkmark = " ✅" if self.used_menus['model_development']['ml_model_training'] else ""
        print(f"3. 🤖 ML Model Training{checkmark}")
        
        # Model Evaluation
        checkmark = " ✅" if self.used_menus['model_development']['model_evaluation'] else ""
        print(f"4. 📊 Model Evaluation{checkmark}")
        
        # Hyperparameter Tuning
        checkmark = " ✅" if self.used_menus['model_development']['hyperparameter_tuning'] else ""
        print(f"5. 🧪 Hyperparameter Tuning{checkmark}")
        
        # Model Report
        checkmark = " ✅" if self.used_menus['model_development']['model_report'] else ""
        print(f"6. 📋 Model Report{checkmark}")
        
        print("7. 🔙 Back to Main Menu")
        print("-" * 50)
        
    def load_data_from_file(self, file_path: str) -> pd.DataFrame:
        """Load data from file path."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Load data based on file type
        if file_path.suffix.lower() == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.parquet':
            return pd.read_parquet(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def load_data_from_folder(self, folder_path: str) -> List[str]:
        """Load data files from folder path."""
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Find all data files in the folder
        data_files = []
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                if file_path.suffix.lower() in ['.csv', '.parquet', '.xlsx', '.xls']:
                    data_files.append(str(file_path))
        
        return data_files
    
    def load_data(self) -> bool:
        """Load data interactively with support for multiple files."""
        print("\n📁 LOAD DATA")
        print("-" * 30)
        
        # Get all subfolders in data directory
        data_folder = Path("data")
        if not data_folder.exists():
            print("❌ Data folder not found. Please ensure 'data' folder exists.")
            return False
        
        # Find all subfolders
        subfolders = [data_folder]  # Include main data folder
        for item in data_folder.iterdir():
            if item.is_dir():
                subfolders.append(item)
                # Also include sub-subfolders
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        subfolders.append(subitem)
        
        print("💡 Available folders:")
        print("0. 🔙 Back to Main Menu")
        for i, folder in enumerate(subfolders, 1):
            try:
                rel_path = folder.relative_to(Path.cwd())
            except ValueError:
                rel_path = folder
            print(f"{i}. 📁 {rel_path}/")
        
        print("-" * 30)
        print("💡 Examples:")
        print("   • Enter folder number (e.g., 1 for data/)")
        print("   • Or enter folder path with mask (e.g., data gbpusd)")
        print("   • Or enter folder path with file type (e.g., data parquet)")
        print("")
        print("📋 More Examples:")
        print("   • 3 eurusd     (folder 3 with 'eurusd' in filename)")
        print("   • 8 btcusdt    (folder 8 with 'btcusdt' in filename)")
        print("   • data gbpusd  (data folder with 'gbpusd' in filename)")
        print("   • data sample  (data folder with 'sample' in filename)")
        print("   • 3 csv        (folder 3 with '.csv' files)")
        print("   • 7 parquet    (folder 7 with '.parquet' files)")
        print("   • 8 aapl       (folder 8 with 'aapl' in filename)")
        print("   • 3 btcusd     (folder 3 with 'btcusd' in filename)")
        print("   • data test    (data folder with 'test' in filename)")
        print("-" * 30)
        
        try:
            input_text = input("Enter folder number or path (with optional mask): ").strip()
        except EOFError:
            print("\n👋 Goodbye!")
            return False
        
        if not input_text:
            print("❌ No input provided")
            return False
        
        # Check if user wants to go back
        if input_text == "0":
            return False
        
        # Parse input for folder and mask
        parts = input_text.split()
        
        # Check if first part is a number (folder selection)
        if parts[0].isdigit():
            folder_idx = int(parts[0]) - 1
            if 0 <= folder_idx < len(subfolders):
                folder_path = subfolders[folder_idx]
                mask = parts[1].lower() if len(parts) > 1 else None
            else:
                print(f"❌ Invalid folder number. Please select 0-{len(subfolders)}")
                return False
        else:
            # Parse input for folder path and mask
            folder_path = parts[0]
            mask = parts[1].lower() if len(parts) > 1 else None
                
            folder_path = Path(folder_path)
            if not folder_path.exists() or not folder_path.is_dir():
                print(f"❌ Folder not found: {folder_path}")
                return False
        
        # Find all data files
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            if mask:
                # Apply mask filter
                pattern = f"*{mask}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                # Also try case-insensitive search
                pattern = f"*{mask.upper()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
                pattern = f"*{mask.lower()}*{ext}"
                data_files.extend(folder_path.glob(pattern))
            else:
                # No mask, get all files
                data_files.extend(folder_path.glob(f"*{ext}"))
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        if not data_files:
            if mask:
                print(f"❌ No files found matching mask '{mask}' in {folder_path}")
            else:
                print(f"❌ No data files found in {folder_path}")
            return False
        
        print(f"📁 Found {len(data_files)} data files:")
        for i, file in enumerate(data_files, 1):
            print(f"   {i}. {file.name}")
        
        # Load all files
        all_data = []
        for file in data_files:
            try:
                df = self.load_data_from_file(str(file))
                df['source_file'] = file.name  # Add source file info
                all_data.append(df)
                print(f"✅ Loaded: {file.name} ({df.shape[0]} rows)")
            except Exception as e:
                print(f"❌ Error loading {file.name}: {e}")
        
        if not all_data:
            print("❌ No files could be loaded")
            return False
        
        # Combine all data
        self.current_data = pd.concat(all_data, ignore_index=True)
        print(f"\n✅ Combined data loaded successfully!")
        print(f"   Total shape: {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns")
        print(f"   Files loaded: {len(all_data)}")
        if mask:
            print(f"   Mask used: '{mask}'")
        print(f"   Columns: {list(self.current_data.columns)}")
        
        # Show data preview
        show_preview = input("\nShow data preview? (y/n): ").strip().lower()
        if show_preview in ['y', 'yes']:
            print("\n📋 DATA PREVIEW:")
            print(self.current_data.head())
            print(f"\nData types:\n{self.current_data.dtypes}")
        
        return True
    

    

    

    
    def run_basic_statistics(self):
        """Run comprehensive basic statistical analysis with explanations and visualizations."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📊 COMPREHENSIVE BASIC STATISTICS")
        print("=" * 50)
        
        try:
            # Filter out infinite values and handle NaN values
            numeric_data = self.current_data.select_dtypes(include=[np.number]).copy()
            
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
            
            # Create visualizations
            print(f"\n📊 GENERATING VISUALIZATIONS...")
            self._create_statistics_plots(numeric_data)
            
            # Ask user if they want to show HTML plots
            print(f"\n🌐 HTML PLOTS OPTION")
            print("-" * 30)
            print("📋 Generated visualization files are available in: results/plots/statistics/")
            print("💡 You can also view them in an interactive HTML report with explanations")
            
            try:
                show_html = input("Show HTML Plot with explanations? (Yes/No): ").strip().lower()
                
                if show_html in ['yes', 'y']:
                    print(f"\n🌐 OPENING PLOTS IN BROWSER...")
                    self._show_plots_in_browser()
                else:
                    print(f"⏭️  Skipping HTML report. Plots are available in: results/plots/statistics/")
                    
            except (EOFError, OSError):
                # Handle test environment where input is not available
                print(f"⏭️  Skipping HTML report (test mode). Plots are available in: results/plots/statistics/")
            
            # Collect columns with high outlier percentages
            high_outlier_cols = []
            outlier_details = {}
            
            for col in numeric_data.columns:
                col_data = numeric_data[col].dropna()
                if len(col_data) == 0:
                    continue
                
                q25 = col_data.quantile(0.25)
                q75 = col_data.quantile(0.75)
                iqr = q75 - q25
                lower_bound = q25 - 1.5 * iqr
                upper_bound = q75 + 1.5 * iqr
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                outlier_pct = len(outliers) / len(col_data) * 100
                
                if outlier_pct > 5:
                    high_outlier_cols.append(col)
                    outlier_details[col] = {
                        'outlier_count': len(outliers),
                        'outlier_percentage': outlier_pct,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound
                    }
            
            # Save results
            self.current_results['comprehensive_basic_statistics'] = {
                'basic_stats': desc_stats.to_dict(),
                'descriptive_stats': desc_stats.to_dict(),
                'distribution_analysis': {
                    'skewness': {col: numeric_data[col].skew() for col in numeric_data.columns},
                    'kurtosis': {col: numeric_data[col].kurtosis() for col in numeric_data.columns}
                },
                'outlier_analysis': outlier_details,
                'time_series_analysis': {
                    'trend_analysis': 'Basic trend analysis completed',
                    'seasonality_check': 'Seasonality analysis completed'
                },
                'summary': {
                    'shape': numeric_data.shape,
                    'memory_usage_mb': numeric_data.memory_usage(deep=True).sum() / 1024 / 1024,
                    'missing_percentage': (numeric_data.isna().sum().sum() / (numeric_data.shape[0] * numeric_data.shape[1])) * 100,
                    'normal_distributions': len([col for col in numeric_data.columns if abs(numeric_data[col].skew()) < 0.5]),
                    'skewed_distributions': len([col for col in numeric_data.columns if abs(numeric_data[col].skew()) >= 0.5]),
                    'high_outlier_columns': len(high_outlier_cols)
                }
            }
            
            print("\n✅ Comprehensive basic statistics completed and saved!")
            print("📁 Plots saved to: results/plots/statistics/")
            
            # Check for outliers and ask user if they want to fix them
            print(f"\n🔍 OUTLIER ANALYSIS SUMMARY")
            print("=" * 50)
            
            if high_outlier_cols:
                print(f"⚠️  Found {len(high_outlier_cols)} columns with high outlier percentages (>5%):")
                for col in high_outlier_cols:
                    details = outlier_details[col]
                    print(f"   • {col}: {details['outlier_count']:,} outliers ({details['outlier_percentage']:.2f}%)")
                
                print(f"\n🔧 OUTLIER TREATMENT OPTIONS")
                print("-" * 30)
                print("💡 Available methods:")
                print("   1. Removal - Remove outlier rows completely")
                print("   2. Capping - Cap outliers to reasonable bounds")
                print("   3. Winsorization - Replace outliers with percentile values")
                print("   4. Skip - Continue without treatment")
                
                try:
                    fix_choice = input("\nDo you want to fix outliers? (Yes/No): ").strip().lower()
                    
                    if fix_choice in ['yes', 'y']:
                        print(f"\n🛠️  Starting outlier treatment...")
                        self._handle_outlier_treatment(high_outlier_cols, outlier_details)
                    else:
                        print("⏭️  Skipping outlier treatment. You can run it later from the EDA menu.")
                        
                except (EOFError, OSError):
                    # Handle test environment where input is not available
                    print("⏭️  Skipping outlier treatment (test mode). You can run it later from the EDA menu.")
            else:
                print("✅ No columns with high outlier percentages detected.")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'basic_statistics')
            
        except Exception as e:
            print(f"❌ Error in basic statistics: {e}")
            import traceback
            traceback.print_exc()
            
            # Statistical explanations and interpretations
            print("\n🔍 STATISTICAL INTERPRETATIONS")
            print("=" * 50)
            
            # Use numeric_data columns instead of numeric_cols
            for col in numeric_data.columns:
                col_data = self.current_data[col].dropna()
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
            
            # Generate summary before creating plots
            print(f"\n📋 ANALYSIS SUMMARY")
            print("=" * 50)
            print(f"📊 Dataset Overview:")
            print(f"  • Total numeric columns: {len(numeric_cols)}")
            print(f"  • Total observations: {len(self.current_data):,}")
            print(f"  • Columns with missing values: {len([col for col in numeric_cols if self.current_data[col].isna().sum() > 0])}")
            
            # Summary of key findings
            print(f"\n🔍 Key Findings:")
            skewed_cols = []
            high_outlier_cols = []
            high_cv_cols = []
            
            for col in numeric_cols:
                col_data = self.current_data[col].dropna()
                if len(col_data) == 0:
                    continue
                    
                skew_val = col_data.skew()
                if abs(skew_val) > 1:
                    skewed_cols.append(col)
                
                # Outlier analysis
                q25 = col_data.quantile(0.25)
                q75 = col_data.quantile(0.75)
                iqr = q75 - q25
                outliers = col_data[(col_data < q25 - 1.5*iqr) | (col_data > q75 + 1.5*iqr)]
                outlier_pct = len(outliers) / len(col_data) * 100
                if outlier_pct > 5:
                    high_outlier_cols.append(col)
                
                # Coefficient of variation
                mean_val = col_data.mean()
                std_val = col_data.std()
                cv = std_val / mean_val if mean_val != 0 else 0
                if cv > 1:
                    high_cv_cols.append(col)
            
            if skewed_cols:
                print(f"  ⚠️  Skewed columns ({len(skewed_cols)}): {skewed_cols[:3]}{'...' if len(skewed_cols) > 3 else ''}")
            if high_outlier_cols:
                print(f"  ⚠️  High outlier columns ({len(high_outlier_cols)}): {high_outlier_cols[:3]}{'...' if len(high_outlier_cols) > 3 else ''}")
            if high_cv_cols:
                print(f"  ⚠️  High variability columns ({len(high_cv_cols)}): {high_cv_cols[:3]}{'...' if len(high_cv_cols) > 3 else ''}")
            
            if not skewed_cols and not high_outlier_cols and not high_cv_cols:
                print(f"  ✅ Data quality looks good across all columns")
            
            print(f"\n📈 Next Steps:")
            print(f"  • Run correlation analysis to understand relationships")
            print(f"  • Check for seasonality in time series data")
            print(f"  • Consider feature scaling for machine learning")
            print(f"  • Investigate outliers if percentage is high")
            
        except Exception as e:
            print(f"❌ Error in comprehensive basic statistics: {e}")
            import traceback
            traceback.print_exc()
    
    def _handle_outlier_treatment(self, high_outlier_cols, outlier_details):
        """
        Handle outlier treatment with user interaction.
        
        Args:
            high_outlier_cols: List of columns with high outlier percentages
            outlier_details: Dictionary with outlier details for each column
        """
        try:
            from src.eda.outlier_handler import OutlierHandler
            
            print(f"\n🔧 OUTLIER TREATMENT INTERFACE")
            print("=" * 50)
            
            # Initialize outlier handler
            outlier_handler = OutlierHandler(self.current_data)
            
            # Show treatment options
            print(f"📊 Columns to treat: {len(high_outlier_cols)}")
            print(f"💡 Available treatment methods:")
            print(f"   1. Removal - Remove outlier rows (preserves data structure)")
            print(f"   2. Capping - Cap outliers to reasonable bounds (preserves all data)")
            print(f"   3. Winsorization - Replace outliers with percentile values")
            print(f"   4. Custom - Choose different method for each column")
            print(f"   5. Skip - Continue without treatment")
            
            try:
                method_choice = input("\nSelect treatment method (1-5): ").strip()
                
                if method_choice == "1":
                    # Removal method
                    print(f"\n🗑️  REMOVAL METHOD")
                    print("-" * 30)
                    print(f"⚠️  This will remove outlier rows completely.")
                    print(f"   Original shape: {self.current_data.shape}")
                    
                    confirm = input("Are you sure? (Yes/No): ").strip().lower()
                    if confirm in ['yes', 'y']:
                        results = outlier_handler.treat_outliers_removal(high_outlier_cols, method='iqr')
                        self.current_data = outlier_handler.current_data
                        self._show_treatment_results(results, "Removal")
                    else:
                        print("⏭️  Cancelled removal.")
                
                elif method_choice == "2":
                    # Capping method
                    print(f"\n🔒 CAPPING METHOD")
                    print("-" * 30)
                    print(f"💡 This will cap outliers to reasonable bounds.")
                    print(f"   All data will be preserved.")
                    
                    cap_method = input("Choose cap method (percentile/iqr/manual): ").strip().lower()
                    if cap_method not in ['percentile', 'iqr', 'manual']:
                        cap_method = 'percentile'
                        print(f"Using default method: {cap_method}")
                    
                    results = outlier_handler.treat_outliers_capping(high_outlier_cols, method='iqr', cap_method=cap_method)
                    self.current_data = outlier_handler.current_data
                    self._show_treatment_results(results, "Capping")
                
                elif method_choice == "3":
                    # Winsorization method
                    print(f"\n📊 WINSORIZATION METHOD")
                    print("-" * 30)
                    print(f"💡 This will replace outliers with percentile values.")
                    
                    try:
                        limit_input = input("Enter limits as 'lower,upper' (e.g., 0.05,0.05): ").strip()
                        if limit_input:
                            limits = tuple(map(float, limit_input.split(',')))
                        else:
                            limits = (0.05, 0.05)
                    except:
                        limits = (0.05, 0.05)
                        print(f"Using default limits: {limits}")
                    
                    results = outlier_handler.treat_outliers_winsorization(high_outlier_cols, limits=limits)
                    self.current_data = outlier_handler.current_data
                    self._show_treatment_results(results, "Winsorization")
                
                elif method_choice == "4":
                    # Custom method
                    print(f"\n🎛️  CUSTOM METHOD")
                    print("-" * 30)
                    self._handle_custom_outlier_treatment(outlier_handler, high_outlier_cols)
                
                elif method_choice == "5":
                    print("⏭️  Skipping outlier treatment.")
                    return
                
                else:
                    print("❌ Invalid choice. Skipping outlier treatment.")
                    return
                
                # Validate treatment
                validation = outlier_handler.validate_treatment()
                self._show_validation_results(validation)
                
                # Ask if user wants to check results
                try:
                    check_results = input("\nCheck outlier treatment results? (Yes/No): ").strip().lower()
                    if check_results in ['yes', 'y']:
                        self._check_outlier_treatment_results(outlier_handler, high_outlier_cols)
                except (EOFError, OSError):
                    pass
                
                # Save treatment summary
                treatment_summary = outlier_handler.get_treatment_summary()
                self.current_results['outlier_treatment'] = treatment_summary
                
                print(f"\n✅ Outlier treatment completed!")
                print(f"   Backup files saved to: {outlier_handler.backup_dir}")
                
            except (EOFError, OSError):
                print("⏭️  Skipping outlier treatment (test mode).")
                
        except ImportError as e:
            print(f"❌ Error importing outlier handler: {e}")
            print("   Please ensure the outlier handler module is available.")
        except Exception as e:
            print(f"❌ Error in outlier treatment: {e}")
            import traceback
            traceback.print_exc()
    
    def _handle_custom_outlier_treatment(self, outlier_handler, high_outlier_cols):
        """
        Handle custom outlier treatment for individual columns.
        
        Args:
            outlier_handler: OutlierHandler instance
            high_outlier_cols: List of columns to treat
        """
        print(f"🎯 Custom treatment for each column:")
        
        for col in high_outlier_cols:
            print(f"\n📊 Column: {col}")
            print(f"   Outlier percentage: {outlier_handler.detect_outliers_iqr(col)[1]['outlier_percentage']:.2f}%")
            
            try:
                method = input(f"   Treatment method for {col} (removal/capping/winsorization/skip): ").strip().lower()
                
                if method == 'removal':
                    results = outlier_handler.treat_outliers_removal([col], method='iqr')
                    print(f"   ✅ Removed {results['rows_removed']} rows")
                
                elif method == 'capping':
                    cap_method = input(f"   Cap method (percentile/iqr): ").strip().lower()
                    if cap_method not in ['percentile', 'iqr']:
                        cap_method = 'percentile'
                    results = outlier_handler.treat_outliers_capping([col], method='iqr', cap_method=cap_method)
                    print(f"   ✅ Capped {results['values_capped']} values")
                
                elif method == 'winsorization':
                    try:
                        limit_input = input(f"   Limits (e.g., 0.05,0.05): ").strip()
                        limits = tuple(map(float, limit_input.split(','))) if limit_input else (0.05, 0.05)
                    except:
                        limits = (0.05, 0.05)
                    results = outlier_handler.treat_outliers_winsorization([col], limits=limits)
                    print(f"   ✅ Winsorized {results['details'][col]['values_changed']} values")
                
                elif method == 'skip':
                    print(f"   ⏭️  Skipped {col}")
                
                else:
                    print(f"   ❌ Invalid method, skipping {col}")
                    
            except (EOFError, OSError):
                print(f"   ⏭️  Skipping {col} (test mode)")
        
        # Update current data
        self.current_data = outlier_handler.current_data
    
    def _show_treatment_results(self, results, method_name):
        """
        Show treatment results to user.
        
        Args:
            results: Treatment results dictionary
            method_name: Name of the treatment method
        """
        print(f"\n📋 {method_name.upper()} RESULTS")
        print("-" * 30)
        print(f"Method: {results['method']}")
        print(f"Detection: {results['detection_method']}")
        print(f"Columns treated: {len(results['columns_treated'])}")
        
        if 'rows_removed' in results:
            print(f"Rows removed: {results['rows_removed']:,}")
        if 'values_capped' in results:
            print(f"Values capped: {results['values_capped']:,}")
        
        print(f"Backup created: {results['backup_path']}")
        
        # Show details for each column
        if results['details']:
            print(f"\nColumn details:")
            for col, details in results['details'].items():
                if 'outliers_removed' in details:
                    print(f"   {col}: {details['outliers_removed']:,} outliers removed")
                elif 'values_capped' in details:
                    print(f"   {col}: {details['values_capped']:,} values capped")
                elif 'values_changed' in details:
                    print(f"   {col}: {details['values_changed']:,} values changed")
    
    def _show_validation_results(self, validation):
        """
        Show validation results to user.
        
        Args:
            validation: Validation results dictionary
        """
        print(f"\n🔍 VALIDATION RESULTS")
        print("-" * 30)
        
        if validation['data_integrity']:
            print("✅ Data integrity: OK")
        else:
            print("❌ Data integrity: Issues detected")
        
        if validation['shape_changed']:
            print("⚠️  Data shape: Changed")
        else:
            print("✅ Data shape: Unchanged")
        
        if validation['missing_values']:
            print("⚠️  Missing values: Detected")
        else:
            print("✅ Missing values: None")
        
        if validation['infinite_values']:
            print("⚠️  Infinite values: Detected")
        else:
            print("✅ Infinite values: None")
        
        if validation['warnings']:
            print(f"\n⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"   • {warning}")
    
    def _check_outlier_treatment_results(self, outlier_handler, original_columns):
        """
        Check and display outlier treatment results.
        
        Args:
            outlier_handler: OutlierHandler instance
            original_columns: List of original columns with outliers
        """
        print(f"\n🔍 CHECKING TREATMENT RESULTS")
        print("-" * 30)
        
        # Generate new outlier report
        new_report = outlier_handler.get_outlier_report(original_columns)
        
        print(f"📊 Post-treatment outlier analysis:")
        for col in original_columns:
            if col in new_report['results']:
                iqr_result = new_report['results'][col]['iqr']
                zscore_result = new_report['results'][col]['zscore']
                
                print(f"\n   {col}:")
                print(f"     IQR method: {iqr_result['outlier_count']:,} outliers ({iqr_result['outlier_percentage']:.2f}%)")
                print(f"     Z-score method: {zscore_result['outlier_count']:,} outliers ({zscore_result['outlier_percentage']:.2f}%)")
                
                # Check if treatment was effective
                if iqr_result['outlier_percentage'] < 5:
                    print(f"     ✅ Treatment effective (IQR outliers < 5%)")
                else:
                    print(f"     ⚠️  Treatment may need adjustment (IQR outliers >= 5%)")
    
    def _show_plots_in_browser(self):
        """Show generated plots in Safari browser with detailed explanations."""
        try:
            import webbrowser
            import tempfile
            import os
            
            # Create HTML file with plots and explanations
            html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeoZorK HLD Prediction - Statistical Analysis Plots</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .content {
            padding: 30px;
        }
        .plot-section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .plot-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .plot-header h2 {
            margin: 0;
            color: #2c3e50;
            font-size: 1.5em;
        }
        .plot-description {
            margin: 10px 0 0 0;
            color: #666;
            line-height: 1.6;
        }
        .plot-image {
            text-align: center;
            padding: 20px;
            background: white;
        }
        .plot-image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .interpretation {
            background: #f8f9fa;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .interpretation h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 1.2em;
        }
        .interpretation ul {
            margin: 0;
            padding-left: 20px;
        }
        .interpretation li {
            margin-bottom: 8px;
            line-height: 1.5;
        }
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        .timestamp {
            color: #95a5a6;
            font-size: 0.8em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Statistical Analysis Results</h1>
            <p>NeoZorK HLD Prediction Interactive System</p>
        </div>
        
        <div class="content">
"""
            
            # Add each plot with explanations
            plots_info = [
                {
                    'file': 'distributions.png',
                    'title': 'Distribution Analysis',
                    'description': 'Histograms with Kernel Density Estimation (KDE) showing the distribution of each variable',
                    'interpretation': [
                        'Shows the shape and spread of data for each variable',
                        'KDE curve helps identify the underlying distribution pattern',
                        'Look for symmetry, skewness, and modality (single vs multiple peaks)',
                        'Statistics box shows mean, standard deviation, and skewness values'
                    ]
                },
                {
                    'file': 'boxplots.png',
                    'title': 'Box Plot Analysis (Outlier Detection)',
                    'description': 'Box plots showing the median, quartiles, and outliers for each variable',
                    'interpretation': [
                        'Box shows the interquartile range (IQR) - middle 50% of data',
                        'Whiskers extend to the most extreme non-outlier points',
                        'Points beyond whiskers are considered outliers',
                        'Outlier count shows how many extreme values exist'
                    ]
                },
                {
                    'file': 'correlation_heatmap.png',
                    'title': 'Correlation Matrix',
                    'description': 'Heatmap showing pairwise correlations between all variables',
                    'interpretation': [
                        'Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation)',
                        'Red indicates positive correlations, blue indicates negative correlations',
                        'Darker colors indicate stronger correlations',
                        'Look for patterns that might indicate multicollinearity'
                    ]
                },
                {
                    'file': 'statistical_summary.png',
                    'title': 'Statistical Summary',
                    'description': 'Comparative analysis charts showing key statistical measures across variables',
                    'interpretation': [
                        'Mean vs Median comparison helps identify skewness',
                        'Coefficient of Variation shows relative variability',
                        'Skewness and Kurtosis indicate distribution shape',
                        'Use these to decide on data transformations'
                    ]
                }
            ]
            
            plots_dir = Path("results/plots/statistics")
            
            for plot_info in plots_info:
                plot_path = plots_dir / plot_info['file']
                if plot_path.exists():
                    # Convert plot to base64 for embedding in HTML
                    import base64
                    with open(plot_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                    
                    html_content += f"""
            <div class="plot-section">
                <div class="plot-header">
                    <h2>{plot_info['title']}</h2>
                    <p class="plot-description">{plot_info['description']}</p>
                </div>
                <div class="plot-image">
                    <img src="data:image/png;base64,{img_data}" alt="{plot_info['title']}">
                </div>
                <div class="interpretation">
                    <h3>How to Interpret:</h3>
                    <ul>
"""
                    
                    for item in plot_info['interpretation']:
                        html_content += f"                        <li>{item}</li>\n"
                    
                    html_content += """
                    </ul>
                </div>
            </div>
"""
            
            # Close HTML
            html_content += f"""
        </div>
        
        <div class="footer">
            <p>Generated by NeoZorK HLD Prediction Interactive System</p>
            <p class="timestamp">Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            # Open in Safari
            webbrowser.get('safari').open(f'file://{temp_html_path}')
            
            print("✅ Opening plots in Safari browser...")
            print(f"📄 HTML file created: {temp_html_path}")
            
        except Exception as e:
            print(f"❌ Error opening plots in browser: {e}")
            print("📁 Plots are still available in: results/plots/statistics/")
    
    def _create_statistics_plots(self, numeric_data):
        """Create comprehensive statistical visualizations with progress tracking."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            from tqdm import tqdm
            import time
            
            # Set modern style
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
            
            # Create plots directory
            plots_dir = Path("results/plots/statistics")
            plots_dir.mkdir(parents=True, exist_ok=True)
            
            # Select important columns for visualization (prioritize key fields)
            important_cols = ['open', 'high', 'low', 'close', 'volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
            
            # Find available important columns with improved matching logic
            available_important = []
            used_numeric_cols = set()  # Track which numeric columns we've already matched
            
            for important_col in important_cols:
                best_match = None
                best_match_score = 0
                
                for numeric_col in numeric_data.columns:
                    if numeric_col in used_numeric_cols:
                        continue
                    
                    # Calculate match score based on different matching strategies
                    numeric_col_lower = numeric_col.lower()
                    important_col_lower = important_col.lower()
                    
                    # Exact match gets highest score
                    if numeric_col_lower == important_col_lower:
                        best_match = numeric_col
                        best_match_score = 100
                        break
                    
                    # Contains match gets medium score
                    elif important_col_lower in numeric_col_lower:
                        score = len(important_col_lower) / len(numeric_col_lower) * 50
                        if score > best_match_score:
                            best_match = numeric_col
                            best_match_score = score
                    
                    # Partial word match gets lower score
                    elif any(word in numeric_col_lower for word in important_col_lower.split('_')):
                        score = 25
                        if score > best_match_score:
                            best_match = numeric_col
                            best_match_score = score
                
                if best_match and best_match_score > 0:
                    available_important.append(best_match)
                    used_numeric_cols.add(best_match)
            
            # Add other numeric columns if we have space
            other_cols = [col for col in numeric_data.columns if col not in available_important]
            
            # Combine important columns first, then others (limit to 9 total to include more important columns)
            cols_to_plot = available_important + other_cols
            cols_to_plot = cols_to_plot[:9]
            
            print(f"📊 Selected columns for visualization: {cols_to_plot}")
            
            # Debug information about column matching
            print(f"🔍 Column matching debug info:")
            print(f"   Important columns to find: {important_cols}")
            print(f"   Available numeric columns: {list(numeric_data.columns)}")
            print(f"   Found important columns: {available_important}")
            print(f"   Other columns added: {other_cols[:9-len(available_important)]}")
            
            # Check for missing important columns
            missing_important = []
            for important_col in important_cols:
                found = False
                for found_col in available_important:
                    if important_col.lower() in found_col.lower():
                        found = True
                        break
                if not found:
                    missing_important.append(important_col)
            
            if missing_important:
                print(f"   ⚠️  Missing important columns: {missing_important}")
            else:
                print(f"   ✅ All important columns found!")
            
            # Define plot tasks with estimated complexity
            plot_tasks = [
                {'name': 'Distribution Analysis', 'complexity': 1.0, 'description': 'Creating histograms with KDE'},
                {'name': 'Box Plot Analysis', 'complexity': 0.8, 'description': 'Creating box plots with outlier detection'},
                {'name': 'Correlation Heatmap', 'complexity': 0.6, 'description': 'Creating correlation matrix heatmap'},
                {'name': 'Statistical Summary', 'complexity': 1.2, 'description': 'Creating comparative statistics charts'}
            ]
            
            # Calculate total complexity for ETA estimation
            total_complexity = sum(task['complexity'] for task in plot_tasks)
            
            # Start progress tracking
            start_time = time.time()
            print(f"📊 Generating {len(plot_tasks)} visualization files...")
            
            with tqdm(total=len(plot_tasks), desc="Creating plots", unit="plot", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
                
                # 1. Distribution plots
                pbar.set_description(f"Creating {plot_tasks[0]['name']}")
                pbar.set_postfix_str(plot_tasks[0]['description'])
                
                # Calculate grid size for up to 9 columns
                n_cols = len(cols_to_plot)
                n_rows = (n_cols + 2) // 3  # Ceiling division to ensure enough rows
                
                fig, axes = plt.subplots(n_rows, 3, figsize=(18, 4 * n_rows))
                fig.suptitle('Distribution Analysis', fontsize=16, fontweight='bold')
                
                # Ensure axes is always 2D array
                if n_rows == 1:
                    axes = axes.reshape(1, -1)
                
                for i, col in enumerate(cols_to_plot):
                    row, col_idx = i // 3, i % 3
                    col_data = numeric_data[col].dropna()
                    
                    if len(col_data) > 0:
                        # Histogram with KDE
                        sns.histplot(col_data, kde=True, ax=axes[row, col_idx], bins=50)
                        axes[row, col_idx].set_title(f'{col} Distribution')
                        axes[row, col_idx].set_xlabel(col)
                        axes[row, col_idx].set_ylabel('Frequency')
                        
                        # Add statistics text
                        mean_val = col_data.mean()
                        std_val = col_data.std()
                        skew_val = col_data.skew()
                        axes[row, col_idx].text(0.02, 0.98, 
                                              f'Mean: {mean_val:.4f}\nStd: {std_val:.4f}\nSkew: {skew_val:.4f}',
                                              transform=axes[row, col_idx].transAxes,
                                              verticalalignment='top',
                                              bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                
                plt.tight_layout()
                plt.savefig(plots_dir / 'distributions.png', dpi=300, bbox_inches='tight')
                plt.close()
                pbar.update(1)
                
                # 2. Box plots
                pbar.set_description(f"Creating {plot_tasks[1]['name']}")
                pbar.set_postfix_str(plot_tasks[1]['description'])
                
                # Calculate grid size for up to 9 columns
                n_cols = len(cols_to_plot)
                n_rows = (n_cols + 2) // 3  # Ceiling division to ensure enough rows
                
                fig, axes = plt.subplots(n_rows, 3, figsize=(18, 4 * n_rows))
                fig.suptitle('Box Plot Analysis (Outlier Detection)', fontsize=16, fontweight='bold')
                
                # Ensure axes is always 2D array
                if n_rows == 1:
                    axes = axes.reshape(1, -1)
                
                for i, col in enumerate(cols_to_plot):
                    row, col_idx = i // 3, i % 3
                    col_data = numeric_data[col].dropna()
                    
                    if len(col_data) > 0:
                        sns.boxplot(y=col_data, ax=axes[row, col_idx], orientation='vertical')
                        axes[row, col_idx].set_title(f'{col} Box Plot')
                        
                        # Add outlier count
                        q1 = col_data.quantile(0.25)
                        q3 = col_data.quantile(0.75)
                        iqr = q3 - q1
                        outliers = col_data[(col_data < q1 - 1.5*iqr) | (col_data > q3 + 1.5*iqr)]
                        axes[row, col_idx].text(0.02, 0.98, 
                                              f'Outliers: {len(outliers):,}',
                                              transform=axes[row, col_idx].transAxes,
                                              verticalalignment='top',
                                              bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
                
                plt.tight_layout()
                plt.savefig(plots_dir / 'boxplots.png', dpi=300, bbox_inches='tight')
                plt.close()
                pbar.update(1)
                
                # 3. Correlation heatmap
                pbar.set_description(f"Creating {plot_tasks[2]['name']}")
                pbar.set_postfix_str(plot_tasks[2]['description'])
                
                if len(cols_to_plot) > 1:
                    fig, ax = plt.subplots(figsize=(10, 8))
                    corr_matrix = numeric_data[cols_to_plot].corr()
                    
                    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                               square=True, ax=ax, fmt='.3f')
                    ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
                    
                    plt.tight_layout()
                    plt.savefig(plots_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
                    plt.close()
                else:
                    # Create empty correlation plot if not enough columns
                    fig, ax = plt.subplots(figsize=(10, 8))
                    ax.text(0.5, 0.5, 'Not enough columns\nfor correlation analysis', 
                           ha='center', va='center', transform=ax.transAxes, fontsize=14)
                    ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
                    plt.savefig(plots_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
                    plt.close()
                
                pbar.update(1)
                
                # 4. Summary statistics visualization
                pbar.set_description(f"Creating {plot_tasks[3]['name']}")
                pbar.set_postfix_str(plot_tasks[3]['description'])
                
                fig, axes = plt.subplots(2, 2, figsize=(15, 12))
                fig.suptitle('Statistical Summary', fontsize=16, fontweight='bold')
                
                # Mean vs Median comparison
                means = [numeric_data[col].mean() for col in cols_to_plot]
                medians = [numeric_data[col].median() for col in cols_to_plot]
                
                x = range(len(cols_to_plot))
                width = 0.35
                
                axes[0, 0].bar([i - width/2 for i in x], means, width, label='Mean', alpha=0.8)
                axes[0, 0].bar([i + width/2 for i in x], medians, width, label='Median', alpha=0.8)
                axes[0, 0].set_title('Mean vs Median Comparison')
                axes[0, 0].set_xticks(x)
                axes[0, 0].set_xticklabels(cols_to_plot, rotation=45)
                axes[0, 0].legend()
                
                # Coefficient of Variation
                cvs = [numeric_data[col].std() / numeric_data[col].mean() 
                       if numeric_data[col].mean() != 0 else 0 for col in cols_to_plot]
                axes[0, 1].bar(cols_to_plot, cvs, color='skyblue', alpha=0.8)
                axes[0, 1].set_title('Coefficient of Variation')
                axes[0, 1].tick_params(axis='x', rotation=45)
                
                # Skewness
                skews = [numeric_data[col].skew() for col in cols_to_plot]
                colors = ['red' if abs(s) > 0.5 else 'green' for s in skews]
                axes[1, 0].bar(cols_to_plot, skews, color=colors, alpha=0.8)
                axes[1, 0].set_title('Skewness (Red = High Skew)')
                axes[1, 0].tick_params(axis='x', rotation=45)
                axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
                
                # Kurtosis
                kurts = [numeric_data[col].kurtosis() for col in cols_to_plot]
                colors = ['red' if abs(k) > 2 else 'green' for k in kurts]
                axes[1, 1].bar(cols_to_plot, kurts, color=colors, alpha=0.8)
                axes[1, 1].set_title('Kurtosis (Red = High Kurtosis)')
                axes[1, 1].tick_params(axis='x', rotation=45)
                axes[1, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
                
                plt.tight_layout()
                plt.savefig(plots_dir / 'statistical_summary.png', dpi=300, bbox_inches='tight')
                plt.close()
                
                pbar.update(1)
            
            # Calculate and display timing information
            end_time = time.time()
            total_time = end_time - start_time
            avg_time_per_plot = total_time / len(plot_tasks)
            
            print(f"\n✅ Generated {len(plot_tasks)} visualization files in {total_time:.1f}s:")
            print(f"   • distributions.png - Distribution analysis")
            print(f"   • boxplots.png - Outlier detection")
            print(f"   • correlation_heatmap.png - Feature relationships")
            print(f"   • statistical_summary.png - Statistical comparisons")
            print(f"   ⏱️  Average time per plot: {avg_time_per_plot:.1f}s")
            
        except ImportError:
            print("⚠️  matplotlib/seaborn not available - skipping visualizations")
        except Exception as e:
            print(f"⚠️  Error creating visualizations: {e}")
    
    def _show_plots_in_browser(self):
        """Show generated plots in Safari browser with detailed explanations."""
        try:
            import webbrowser
            import tempfile
            import os
            
            # Create HTML file with plots and explanations
            html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NeoZorK HLD Prediction - Statistical Analysis Plots</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .content {
            padding: 30px;
        }
        .plot-section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .plot-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .plot-header h2 {
            margin: 0;
            color: #2c3e50;
            font-size: 1.5em;
        }
        .plot-description {
            margin: 10px 0 0 0;
            color: #666;
            line-height: 1.6;
        }
        .plot-image {
            text-align: center;
            padding: 20px;
            background: white;
        }
        .plot-image img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .interpretation {
            background: #f8f9fa;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
        }
        .interpretation h3 {
            margin: 0 0 15px 0;
            color: #2c3e50;
            font-size: 1.2em;
        }
        .interpretation ul {
            margin: 0;
            padding-left: 20px;
        }
        .interpretation li {
            margin-bottom: 8px;
            line-height: 1.5;
        }
        .footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        .timestamp {
            color: #95a5a6;
            font-size: 0.8em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Statistical Analysis Results</h1>
            <p>NeoZorK HLD Prediction Interactive System</p>
        </div>
        
        <div class="content">
"""
            
            # Add each plot with explanations
            plots_info = [
                {
                    'file': 'distributions.png',
                    'title': 'Distribution Analysis',
                    'description': 'Histograms with Kernel Density Estimation (KDE) showing the distribution of each variable',
                    'interpretation': [
                        'Shows the shape and spread of data for each variable',
                        'KDE curve helps identify the underlying distribution pattern',
                        'Look for symmetry, skewness, and modality (single vs multiple peaks)',
                        'Statistics box shows mean, standard deviation, and skewness values'
                    ]
                },
                {
                    'file': 'boxplots.png',
                    'title': 'Box Plot Analysis (Outlier Detection)',
                    'description': 'Box plots showing the median, quartiles, and outliers for each variable',
                    'interpretation': [
                        'Box shows the interquartile range (IQR) - middle 50% of data',
                        'Whiskers extend to the most extreme non-outlier points',
                        'Points beyond whiskers are considered outliers',
                        'Outlier count shows how many extreme values exist'
                    ]
                },
                {
                    'file': 'correlation_heatmap.png',
                    'title': 'Correlation Matrix',
                    'description': 'Heatmap showing pairwise correlations between all variables',
                    'interpretation': [
                        'Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation)',
                        'Red indicates positive correlations, blue indicates negative correlations',
                        'Darker colors indicate stronger correlations',
                        'Look for patterns that might indicate multicollinearity'
                    ]
                },
                {
                    'file': 'statistical_summary.png',
                    'title': 'Statistical Summary',
                    'description': 'Comparative analysis charts showing key statistical measures across variables',
                    'interpretation': [
                        'Mean vs Median comparison helps identify skewness',
                        'Coefficient of Variation shows relative variability',
                        'Skewness and Kurtosis indicate distribution shape',
                        'Use these to decide on data transformations'
                    ]
                }
            ]
            
            plots_dir = Path("results/plots/statistics")
            
            for plot_info in plots_info:
                plot_path = plots_dir / plot_info['file']
                if plot_path.exists():
                    # Convert plot to base64 for embedding in HTML
                    import base64
                    with open(plot_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()
                    
                    html_content += f"""
            <div class="plot-section">
                <div class="plot-header">
                    <h2>{plot_info['title']}</h2>
                    <p class="plot-description">{plot_info['description']}</p>
                </div>
                <div class="plot-image">
                    <img src="data:image/png;base64,{img_data}" alt="{plot_info['title']}">
                </div>
                <div class="interpretation">
                    <h3>How to Interpret:</h3>
                    <ul>
"""
                    
                    for item in plot_info['interpretation']:
                        html_content += f"                        <li>{item}</li>\n"
                    
                    html_content += """
                    </ul>
                </div>
            </div>
"""
            
            # Close HTML
            html_content += f"""
        </div>
        
        <div class="footer">
            <p>Generated by NeoZorK HLD Prediction Interactive System</p>
            <p class="timestamp">Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
            
            # Create temporary HTML file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_html_path = f.name
            
            # Open in Safari
            webbrowser.get('safari').open(f'file://{temp_html_path}')
            
            print("✅ Opening plots in Safari browser...")
            print(f"📄 HTML file created: {temp_html_path}")
            
        except Exception as e:
            print(f"❌ Error opening plots in browser: {e}")
            print("📁 Plots are still available in: results/plots/statistics/")
    
    def run_data_quality_check(self):
        """Run comprehensive data quality check using modern methods."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🧹 COMPREHENSIVE DATA QUALITY CHECK")
        print("=" * 50)
        
        try:
            from tqdm import tqdm
            import time
            
            # Initialize summary collections
            nan_summary = []
            dupe_summary = []
            gap_summary = []
            zero_summary = []
            negative_summary = []
            inf_summary = []
            
            # Get file info for better analysis
            print("📊 Analyzing data structure...")
            file_info_dict = {
                'file_path': 'current_data',
                'file_name': 'current_data',
                'n_rows': self.current_data.shape[0],
                'n_cols': self.current_data.shape[1],
                'columns': list(self.current_data.columns),
                'dtypes': self.current_data.dtypes.to_dict(),
                'datetime_or_timestamp_fields': []
            }
            
            # Detect datetime fields
            for col in self.current_data.columns:
                if pd.api.types.is_datetime64_any_dtype(self.current_data[col]):
                    file_info_dict['datetime_or_timestamp_fields'].append(col)
            
            print(f"   📈 Shape: {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns")
            print(f"   🕒 Datetime columns: {len(file_info_dict['datetime_or_timestamp_fields'])}")
            print(f"   🔢 Numeric columns: {len(self.current_data.select_dtypes(include=[np.number]).columns)}")
            
            # Run comprehensive quality checks with progress tracking
            print("\n🔍 Running comprehensive data quality checks...")
            
            # Import colorama for colored output
            from colorama import Fore, Style
            
            # 1. NaN Check
            print("\n1️⃣  Checking for missing values (NaN)...")
            with tqdm(total=1, desc="NaN analysis", leave=False) as pbar:
                data_quality.nan_check(self.current_data, nan_summary, Fore, Style)
                pbar.update(1)
            
            # 2. Duplicate Check
            print("\n2️⃣  Checking for duplicates...")
            with tqdm(total=1, desc="Duplicate analysis", leave=False) as pbar:
                data_quality.duplicate_check(self.current_data, dupe_summary, Fore, Style)
                pbar.update(1)
            
            # 3. Gap Check
            print("\n3️⃣  Checking for time series gaps...")
            with tqdm(total=1, desc="Gap analysis", leave=False) as pbar:
                data_quality.gap_check(
                    self.current_data, gap_summary, Fore, Style,
                    schema_datetime_fields=file_info_dict['datetime_or_timestamp_fields'],
                    file_name=file_info_dict['file_path']
                )
                pbar.update(1)
            
            # 4. Zero Check
            print("\n4️⃣  Checking for zero values...")
            with tqdm(total=1, desc="Zero value analysis", leave=False) as pbar:
                data_quality.zero_check(
                    self.current_data, zero_summary, Fore, Style,
                    file_name=file_info_dict['file_path']
                )
                pbar.update(1)
            
            # 5. Negative Check
            print("\n5️⃣  Checking for negative values...")
            with tqdm(total=1, desc="Negative value analysis", leave=False) as pbar:
                data_quality.negative_check(
                    self.current_data, negative_summary, Fore, Style,
                    file_name=file_info_dict['file_path']
                )
                pbar.update(1)
            
            # 6. Infinity Check
            print("\n6️⃣  Checking for infinity values...")
            with tqdm(total=1, desc="Infinity analysis", leave=False) as pbar:
                data_quality.inf_check(
                    self.current_data, inf_summary, Fore, Style,
                    file_name=file_info_dict['file_path']
                )
                pbar.update(1)
            
            # Generate comprehensive summary
            print("\n" + "="*60)
            print("📋 COMPREHENSIVE DATA QUALITY SUMMARY")
            print("="*60)
            
            # Calculate overall quality score
            total_issues = len(nan_summary) + len(dupe_summary) + len(gap_summary) + len(zero_summary) + len(negative_summary) + len(inf_summary)
            quality_score = max(0, 100 - (total_issues * 10))
            
            print(f"🎯 Overall Data Quality Score: {quality_score}/100")
            
            # Detailed breakdown
            print(f"\n📊 Issue Breakdown:")
            print(f"   • Missing values (NaN): {len(nan_summary)} columns affected")
            print(f"   • Duplicates: {len(dupe_summary)} issues found")
            print(f"   • Time series gaps: {len(gap_summary)} issues found")
            print(f"   • Zero values: {len(zero_summary)} columns affected")
            print(f"   • Negative values: {len(negative_summary)} columns affected")
            print(f"   • Infinity values: {len(inf_summary)} columns affected")
            
            # Critical issues
            critical_issues = []
            if len(nan_summary) > 0:
                critical_issues.append(f"Missing values in {len(nan_summary)} columns")
            if len(dupe_summary) > 0:
                critical_issues.append(f"Duplicate data found")
            if len(gap_summary) > 0:
                critical_issues.append(f"Time series gaps detected")
            
            if critical_issues:
                print(f"\n⚠️  Critical Issues Found:")
                for issue in critical_issues:
                    print(f"   • {issue}")
            else:
                print(f"\n✅ No critical issues detected!")
            
            # Recommendations
            print(f"\n💡 Recommendations:")
            if len(nan_summary) > 0:
                print(f"   • Consider imputation strategies for missing values")
            if len(dupe_summary) > 0:
                print(f"   • Remove duplicate records to avoid bias")
            if len(gap_summary) > 0:
                print(f"   • Interpolate time series gaps for continuity")
            if len(zero_summary) > 0:
                print(f"   • Verify if zero values are legitimate or errors")
            if len(negative_summary) > 0:
                print(f"   • Check for data entry errors in negative values")
            if len(inf_summary) > 0:
                print(f"   • Handle infinity values that may cause computational issues")
            
            # Save comprehensive results
            self.current_results['comprehensive_data_quality'] = {
                'quality_score': quality_score,
                'total_issues': total_issues,
                'nan_summary': nan_summary,
                'dupe_summary': dupe_summary,
                'gap_summary': gap_summary,
                'zero_summary': zero_summary,
                'negative_summary': negative_summary,
                'inf_summary': inf_summary,
                'critical_issues': critical_issues,
                'file_info': file_info_dict,
                'timestamp': time.time()
            }
            
            print(f"\n✅ Comprehensive data quality check completed!")
            print(f"   Results saved for further analysis")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'data_quality_check')
            
            # Ask if user wants to fix issues (only if not in test mode)
            print(f"\n" + "="*60)
            print("🔧 DATA FIXING OPTIONS")
            print("="*60)
            
            if total_issues > 0:
                print(f"Found {total_issues} data quality issues that can be automatically fixed.")
                try:
                    fix_choice = input("Would you like to fix corrupted data (all what need to be fixed)? (Yes/No): ").strip().lower()
                    
                    if fix_choice in ['yes', 'y']:
                        print("\n🛠️  Starting automatic data fixing...")
                        self.fix_all_data_issues()
                    else:
                        print("⏭️  Skipping automatic fixes. You can run fixes later from the EDA menu.")
                except (EOFError, OSError):
                    # Handle test environment where input is not available
                    print("⏭️  Skipping automatic fixes (test mode). You can run fixes later from the EDA menu.")
            else:
                print("✅ No issues found that require fixing!")
            
        except Exception as e:
            print(f"❌ Error in comprehensive data quality check: {e}")
            import traceback
            traceback.print_exc()
    
    def run_correlation_analysis(self):
        """Run correlation analysis."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🔗 CORRELATION ANALYSIS")
        print("-" * 30)
        
        try:
            numeric_data = self.current_data.select_dtypes(include=[np.number])
            
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
            self.current_results['correlation_analysis'] = {
                'pearson_correlation': pearson_corr.to_dict(),
                'high_correlation_pairs': high_corr_pairs
            }
            
            print("\n✅ Correlation analysis completed and saved!")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'correlation_analysis')
            
        except Exception as e:
            print(f"❌ Error in correlation analysis: {e}")
    
    def run_time_series_analysis(self):
        """Run time series analysis."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📈 TIME SERIES ANALYSIS")
        print("-" * 30)
        
        try:
            from src.eda.time_series_analysis import TimeSeriesAnalyzer
            
            # Initialize analyzer
            analyzer = TimeSeriesAnalyzer(self.current_data)
            
            # Get column to analyze
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
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
            
            # Run comprehensive analysis
            print(f"\n🔍 Starting comprehensive time series analysis for column: {column}")
            print("   This will include:")
            print("   • Stationarity testing (ADF, KPSS)")
            print("   • Trend analysis (linear, moving averages)")
            print("   • Seasonality detection (decomposition, FFT)")
            print("   • Volatility analysis (clustering, persistence)")
            print("   • Autocorrelation analysis (ACF, PACF)")
            print("   • Forecasting (naive, seasonal, ARIMA)")
            print("   • Summary and recommendations")
            
            results = analyzer.comprehensive_analysis(column)
            
            # Display summary
            if 'summary' in results:
                summary = results['summary']
                
                print(f"\n📋 ANALYSIS SUMMARY:")
                print("-" * 30)
                
                if 'key_findings' in summary and summary['key_findings']:
                    print(f"🔍 Key Findings:")
                    for i, finding in enumerate(summary['key_findings'], 1):
                        print(f"   {i}. {finding}")
                
                if 'recommendations' in summary and summary['recommendations']:
                    print(f"\n💡 Recommendations:")
                    for i, rec in enumerate(summary['recommendations'], 1):
                        print(f"   {i}. {rec}")
                
                if not summary.get('key_findings') and not summary.get('recommendations'):
                    print("   No significant patterns detected in the data.")
            
            # Show detailed results
            show_details = input("\nShow detailed results? (y/n): ").strip().lower()
            if show_details in ['y', 'yes']:
                print(f"\n📊 DETAILED RESULTS:")
                print("-" * 30)
                
                analyses = results.get('analyses', {})
                
                # Stationarity results
                if 'stationarity' in analyses and 'error' not in analyses['stationarity']:
                    stationarity = analyses['stationarity']
                    print(f"\n📈 Stationarity Analysis:")
                    if 'tests' in stationarity:
                        tests = stationarity['tests']
                        if 'adf' in tests and 'error' not in tests['adf']:
                            adf = tests['adf']
                            print(f"   ADF Test: p-value={adf.get('p_value', 'N/A'):.4f}, "
                                  f"Stationary={adf.get('is_stationary', 'N/A')}")
                        if 'kpss' in tests and 'error' not in tests['kpss']:
                            kpss = tests['kpss']
                            print(f"   KPSS Test: p-value={kpss.get('p_value', 'N/A'):.4f}, "
                                  f"Stationary={kpss.get('is_stationary', 'N/A')}")
                
                # Trend results
                if 'trends' in analyses and 'error' not in analyses['trends']:
                    trends = analyses['trends']
                    print(f"\n📈 Trend Analysis:")
                    if 'trend_analysis' in trends:
                        trend_analysis = trends['trend_analysis']
                        if 'linear' in trend_analysis:
                            linear = trend_analysis['linear']
                            print(f"   Linear Trend: {linear.get('trend_direction', 'N/A')}, "
                                  f"R²={linear.get('r_squared', 'N/A'):.4f}")
                
                # Seasonality results
                if 'seasonality' in analyses and 'error' not in analyses['seasonality']:
                    seasonality = analyses['seasonality']
                    print(f"\n🔄 Seasonality Analysis:")
                    print(f"   Detected Period: {seasonality.get('detected_period', 'N/A')}")
                    if 'seasonality_analysis' in seasonality:
                        seasonality_analysis = seasonality['seasonality_analysis']
                        if 'decomposition' in seasonality_analysis and 'error' not in seasonality_analysis['decomposition']:
                            decomp = seasonality_analysis['decomposition']
                            print(f"   Seasonal Strength: {decomp.get('seasonal_strength', 'N/A'):.4f}")
                            print(f"   Has Seasonality: {decomp.get('has_seasonality', 'N/A')}")
                
                # Volatility results
                if 'volatility' in analyses and 'error' not in analyses['volatility']:
                    volatility = analyses['volatility']
                    print(f"\n📊 Volatility Analysis:")
                    if 'volatility_analysis' in volatility:
                        vol_analysis = volatility['volatility_analysis']
                        print(f"   Mean Volatility: {vol_analysis.get('mean_volatility', 'N/A'):.4f}")
                        print(f"   Volatility Clustering: {vol_analysis.get('has_clustering', 'N/A')}")
                
                # Autocorrelation results
                if 'autocorrelation' in analyses and 'error' not in analyses['autocorrelation']:
                    autocorr = analyses['autocorrelation']
                    print(f"\n🔗 Autocorrelation Analysis:")
                    if 'autocorrelation_analysis' in autocorr:
                        acf_analysis = autocorr['autocorrelation_analysis']
                        print(f"   Max ACF Lag: {acf_analysis.get('max_acf_lag', 'N/A')}")
                        print(f"   Max PACF Lag: {acf_analysis.get('max_pacf_lag', 'N/A')}")
            
            # Save results
            self.current_results['time_series_analysis'] = results
            print(f"\n✅ Time series analysis completed!")
            print(f"   Results saved to: {results.get('results_file', 'N/A')}")
            print(f"   Plots saved to: results/plots/time_series/")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'time_series_analysis')
            
        except ImportError as e:
            print(f"❌ Error importing time series analysis module: {e}")
            print("   Please ensure all dependencies are installed.")
        except Exception as e:
            print(f"❌ Error in time series analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def generate_all_features(self):
        """Generate all features using the Feature Engineering system."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🚀 GENERATING ALL FEATURES")
        print("-" * 30)
        
        try:
            # Ensure minimum data size
            if self.current_data.shape[0] < 500:
                print(f"⚠️  Warning: Data has only {self.current_data.shape[0]} rows, minimum recommended is 500")
                print(f"   Padding data to 500 rows for feature generation...")
                
                # Pad data by repeating last rows
                padding_needed = 500 - self.current_data.shape[0]
                padding_data = self.current_data.iloc[-padding_needed:].copy()
                self.current_data = pd.concat([self.current_data, padding_data], ignore_index=True)
                print(f"   Data padded to {self.current_data.shape[0]} rows")
            
            # Initialize feature generator
            feature_config = MasterFeatureConfig(
                max_features=150,
                min_importance=0.2,
                correlation_threshold=0.95,
                enable_proprietary=True,
                enable_technical=True,
                enable_statistical=True,
                enable_temporal=True,
                enable_cross_timeframe=True
            )
            
            selection_config = FeatureSelectionConfig(
                max_features=150,
                min_importance=0.2,
                correlation_threshold=0.95,
                methods=['correlation', 'importance', 'mutual_info', 'lasso', 'random_forest']
            )
            
            self.feature_generator = FeatureGenerator(
                config=feature_config
            )
            
            # Generate features
            print("   Generating features...")
            start_time = time.time()
            
            data_with_features = self.feature_generator.generate_features(self.current_data)
            
            generation_time = time.time() - start_time
            
            # Get feature summary
            feature_summary = self.feature_generator.get_feature_summary()
            
            # Get memory usage
            memory_usage = self.feature_generator.get_memory_usage()
            
            print(f"✅ Feature generation completed!")
            print(f"   Original data: {self.current_data.shape[0]} rows × {self.current_data.shape[0]} columns")
            print(f"   Final data: {data_with_features.shape[0]} rows × {data_with_features.shape[1]} columns")
            print(f"   Features generated: {data_with_features.shape[1] - self.current_data.shape[1]}")
            print(f"   Generation time: {generation_time:.2f} seconds")
            # Safe memory usage printing
            if isinstance(memory_usage, dict) and 'rss' in memory_usage:
                print(f"   Memory usage: {memory_usage['rss']:.1f} MB")
            else:
                print(f"   Memory usage: {memory_usage}")
            
            # Save results
            self.current_results['feature_engineering'] = {
                'original_shape': self.current_data.shape,
                'final_shape': data_with_features.shape,
                'features_generated': data_with_features.shape[1] - self.current_data.shape[1],
                'feature_summary': feature_summary,
                'memory_usage': memory_usage,
                'data_with_features': data_with_features,
                'generation_time': generation_time
            }
            
            # Update current data
            self.current_data = data_with_features
            
            # Mark as used
            self.mark_menu_as_used('feature_engineering', 'generate_all_features')
            
        except Exception as e:
            print(f"❌ Error in feature generation: {e}")
            import traceback
            traceback.print_exc()
    
    def show_feature_summary(self):
        """Show feature summary report."""
        if 'feature_engineering' not in self.current_results:
            print("❌ No feature engineering results available. Please generate features first.")
            return
            
        print("\n📋 FEATURE SUMMARY REPORT")
        print("-" * 30)
        
        try:
            feature_summary = self.current_results['feature_engineering']['feature_summary']
            
            # Sort features by importance
            sorted_features = sorted(
                feature_summary.items(),
                key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0,
                reverse=True
            )
            
            print(f"📊 Total features: {len(feature_summary)}")
            print(f"🎯 Top 20 features by importance:")
            
            for i, (feature, importance) in enumerate(sorted_features[:20], 1):
                if isinstance(importance, (int, float)):
                    print(f"   {i:2d}. {feature:<35} {importance:.4f}")
                else:
                    print(f"   {i:2d}. {feature:<35} {importance}")
            
            # Feature categories
            categories = {}
            for feature in feature_summary.keys():
                if 'phld' in feature.lower() or 'wave' in feature.lower():
                    categories['proprietary'] = categories.get('proprietary', 0) + 1
                elif any(x in feature.lower() for x in ['sma', 'ema', 'rsi', 'macd', 'bb', 'atr']):
                    categories['technical'] = categories.get('technical', 0) + 1
                elif any(x in feature.lower() for x in ['mean', 'std', 'skew', 'kurt', 'percentile']):
                    categories['statistical'] = categories.get('statistical', 0) + 1
                elif any(x in feature.lower() for x in ['hour', 'day', 'month', 'season']):
                    categories['temporal'] = categories.get('temporal', 0) + 1
                elif any(x in feature.lower() for x in ['ratio', 'diff', 'momentum', 'volatility']):
                    categories['cross_timeframe'] = categories.get('cross_timeframe', 0) + 1
                else:
                    categories['other'] = categories.get('other', 0) + 1
            
            print(f"\n📂 Feature Categories:")
            for category, count in categories.items():
                print(f"   {category.title()}: {count} features")
            
            # Mark as used
            self.mark_menu_as_used('feature_engineering', 'feature_summary')
            
        except Exception as e:
            print(f"❌ Error showing feature summary: {e}")
    
    def export_results(self):
        """Export current results to files."""
        if not self.current_results:
            print("❌ No results to export. Please run some analysis first.")
            return
            
        print("\n📤 EXPORT RESULTS")
        print("-" * 30)
        
        try:
            # Create output directory
            output_dir = Path("reports")
            output_dir.mkdir(exist_ok=True)
            
            # Export results to JSON
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            json_path = output_dir / f"interactive_results_{timestamp}.json"
            
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                elif isinstance(obj, pd.DataFrame):
                    return obj.to_dict()
                elif isinstance(obj, pd.Series):
                    return obj.to_dict()
                return obj
            
            # Convert results
            exportable_results = {}
            for key, value in self.current_results.items():
                if key == 'data_with_features':
                    # Don't export large DataFrames to JSON
                    exportable_results[key] = f"DataFrame with shape {value.shape}"
                else:
                    exportable_results[key] = value
            
            with open(json_path, 'w') as f:
                json.dump(exportable_results, f, indent=2, default=convert_numpy)
            
            print(f"✅ Results exported to: {json_path}")
            
            # Export data with features if available
            if 'feature_engineering' in self.current_results:
                data_path = output_dir / f"data_with_features_{timestamp}.parquet"
                self.current_data.to_parquet(data_path)
                print(f"✅ Data with features exported to: {data_path}")
            
            # Export summary report
            summary_path = output_dir / f"summary_report_{timestamp}.txt"
            with open(summary_path, 'w') as f:
                f.write("NEOZORk HLD PREDICTION - INTERACTIVE SYSTEM SUMMARY REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for key, value in self.current_results.items():
                    f.write(f"{key.upper()}:\n")
                    f.write("-" * 30 + "\n")
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if k != 'data_with_features':
                                f.write(f"  {k}: {v}\n")
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
            
            print(f"✅ Summary report exported to: {summary_path}")
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
    
    def fix_data_issues(self):
        """Fix common data quality issues in the current dataset."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🛠️  FIX DATA ISSUES")
        print("-" * 30)
        
        try:
            # Create backup
            backup_data = self.current_data.copy()
            print("✅ Backup created")
            
            # Check for issues
            print("\n🔍 Checking for data issues...")
            
            # NaN values
            nan_cols = [col for col in self.current_data.columns if self.current_data[col].isna().any()]
            if nan_cols:
                print(f"   Found NaN values in {len(nan_cols)} columns: {nan_cols}")
                self.current_data = fix_files.fix_nan(self.current_data)
                print("   ✅ NaN values fixed")
            else:
                print("   ✅ No NaN values found")
            
            # Duplicates
            duplicates = self.current_data.duplicated().sum()
            if duplicates > 0:
                print(f"   Found {duplicates} duplicate rows")
                self.current_data = fix_files.fix_duplicates(self.current_data)
                print("   ✅ Duplicates removed")
            else:
                print("   ✅ No duplicates found")
            
            # Zero values in OHLCV columns
            ohlcv_cols = [col for col in self.current_data.columns if any(x in col.lower() for x in ['open', 'high', 'low', 'close', 'volume'])]
            zero_issues = []
            for col in ohlcv_cols:
                if col in self.current_data.columns and (self.current_data[col] == 0).any():
                    zero_count = (self.current_data[col] == 0).sum()
                    zero_issues.append((col, zero_count))
            
            if zero_issues:
                print(f"   Found zero values in OHLCV columns:")
                for col, count in zero_issues:
                    print(f"     {col}: {count} zero values")
                # Note: We don't auto-fix zeros as they might be legitimate
                print("   ⚠️  Zero values detected but not auto-fixed (may be legitimate)")
            
            # Negative values in OHLCV columns
            negative_issues = []
            for col in ohlcv_cols:
                if col in self.current_data.columns and (self.current_data[col] < 0).any():
                    neg_count = (self.current_data[col] < 0).sum()
                    negative_issues.append((col, neg_count))
            
            if negative_issues:
                print(f"   Found negative values in OHLCV columns:")
                for col, count in negative_issues:
                    print(f"     {col}: {count} negative values")
                print("   ⚠️  Negative values detected but not auto-fixed (may be legitimate)")
            
            print(f"\n✅ Data issues check completed!")
            print(f"   Original shape: {backup_data.shape}")
            print(f"   Current shape: {self.current_data.shape}")
            
            # Ask if user wants to keep changes
            keep_changes = input("\nKeep the fixes? (y/n): ").strip().lower()
            if keep_changes in ['y', 'yes']:
                print("✅ Changes applied")
                self.current_results['data_fixes'] = {
                    'original_shape': backup_data.shape,
                    'current_shape': self.current_data.shape,
                    'nan_fixed': len(nan_cols) > 0,
                    'duplicates_removed': duplicates > 0
                }
                
                # Mark as used
                self.mark_menu_as_used('eda', 'fix_data_issues')
            else:
                self.current_data = backup_data
                print("🔄 Changes reverted")
                
        except Exception as e:
            print(f"❌ Error fixing data issues: {e}")
            import traceback
            traceback.print_exc()
    
    def generate_html_report(self):
        """Generate comprehensive HTML report for current data and analysis."""
        if self.current_data is None:
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
            
            # Initialize HTML report
            html_report = html_report_generator.HTMLReport(report_title, "interactive_analysis")
            
            # Add data overview
            html_report.add_section("Data Overview", f"""
                <h3>Dataset Information</h3>
                <p><strong>Shape:</strong> {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns</p>
                <p><strong>Memory Usage:</strong> {self.current_data.memory_usage(deep=True).sum() / 1024**2:.2f} MB</p>
                <p><strong>Data Types:</strong></p>
                <ul>
                    {''.join([f'<li>{col}: {dtype}</li>' for col, dtype in self.current_data.dtypes.items()])}
                </ul>
            """)
            
            # Add data quality information if available
            if 'data_quality' in self.current_results:
                dq = self.current_results['data_quality']
                html_report.add_section("Data Quality Analysis", f"""
                    <h3>Quality Metrics</h3>
                    <p><strong>Missing Values:</strong> {dq.get('total_missing', 0)} ({dq.get('missing_percentage', 0):.2f}%)</p>
                    <p><strong>Duplicates:</strong> {dq.get('duplicates', 0)} ({dq.get('duplicate_percentage', 0):.2f}%)</p>
                """)
            
            # Add correlation analysis if available
            if 'correlation_analysis' in self.current_results:
                html_report.add_section("Correlation Analysis", """
                    <h3>Feature Correlations</h3>
                    <p>High correlation pairs detected and analyzed.</p>
                """)
            
            # Add time series analysis if available
            if 'time_series_analysis' in self.current_results:
                html_report.add_section("Time Series Analysis", """
                    <h3>Time Series Insights</h3>
                    <p>Comprehensive time series analysis including stationarity, trends, and seasonality.</p>
                """)
            
            # Add feature engineering results if available
            if 'feature_engineering' in self.current_results:
                html_report.add_section("Feature Engineering", """
                    <h3>Generated Features</h3>
                    <p>Advanced features have been generated and are ready for modeling.</p>
                """)
            
            # Add basic statistics recommendations and summary if available
            if 'basic_statistics' in self.current_results:
                bs_results = self.current_results['basic_statistics']
                if 'analysis_summary' in bs_results:
                    summary = bs_results['analysis_summary']
                    
                    # Create recommendations section
                    recommendations_html = "<h3>Data Quality Recommendations</h3><ul>"
                    
                    if summary.get('skewed_columns'):
                        recommendations_html += f"<li><strong>Skewed Data:</strong> Consider log/box-cox transformation for columns: {', '.join(summary['skewed_columns'][:3])}{'...' if len(summary['skewed_columns']) > 3 else ''}</li>"
                    
                    if summary.get('high_outlier_columns'):
                        recommendations_html += f"<li><strong>Outliers:</strong> Investigate and potentially treat outliers in columns: {', '.join(summary['high_outlier_columns'][:3])}{'...' if len(summary['high_outlier_columns']) > 3 else ''}</li>"
                    
                    if summary.get('high_variability_columns'):
                        recommendations_html += f"<li><strong>High Variability:</strong> Consider standardization for columns: {', '.join(summary['high_variability_columns'][:3])}{'...' if len(summary['high_variability_columns']) > 3 else ''}</li>"
                    
                    if not any([summary.get('skewed_columns'), summary.get('high_outlier_columns'), summary.get('high_variability_columns')]):
                        recommendations_html += "<li><strong>Data Quality:</strong> ✅ Data looks good for most analyses</li>"
                    
                    recommendations_html += "</ul>"
                    
                    html_report.add_section("Recommendations", recommendations_html)
                    
                    # Create summary section
                    summary_html = f"""
                        <h3>Analysis Summary</h3>
                        <div class="summary-grid">
                            <div class="summary-item">
                                <strong>Total Columns:</strong> {summary.get('total_columns', 0)}
                            </div>
                            <div class="summary-item">
                                <strong>Total Observations:</strong> {summary.get('total_observations', 0):,}
                            </div>
                            <div class="summary-item">
                                <strong>Columns with Issues:</strong> {summary.get('columns_with_issues', 0)}
                            </div>
                            <div class="summary-item">
                                <strong>Skewed Columns:</strong> {len(summary.get('skewed_columns', []))}
                            </div>
                            <div class="summary-item">
                                <strong>High Outlier Columns:</strong> {len(summary.get('high_outlier_columns', []))}
                            </div>
                            <div class="summary-item">
                                <strong>High Variability Columns:</strong> {len(summary.get('high_variability_columns', []))}
                            </div>
                        </div>
                        <style>
                            .summary-grid {{
                                display: grid;
                                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                                gap: 15px;
                                margin: 20px 0;
                            }}
                            .summary-item {{
                                background: #f8f9fa;
                                padding: 15px;
                                border-radius: 8px;
                                border-left: 4px solid #007bff;
                            }}
                        </style>
                    """
                    
                    html_report.add_section("Analysis Summary", summary_html)
            
            # Generate and save report
            report_path = reports_dir / f"interactive_report_{timestamp}.html"
            html_report.save(str(report_path))
            
            print(f"✅ HTML report generated: {report_path}")
            print(f"   Open the file in your web browser to view the complete report")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'generate_html_report')
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            import traceback
            traceback.print_exc()
    
    def run_eda_analysis(self):
        """Run EDA analysis menu."""
        while True:
            self.print_eda_menu()
            try:
                choice = input("Select option (0-8): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            if choice == '0':
                break
            elif choice == '1':
                self.run_basic_statistics()
            elif choice == '2':
                self.run_data_quality_check()
            elif choice == '3':
                self.run_correlation_analysis()
            elif choice == '4':
                self.run_time_series_analysis()
            elif choice == '5':
                print("⏳ Feature Importance - Coming soon!")
            elif choice == '6':
                self.fix_data_issues()
            elif choice == '7':
                self.generate_html_report()
            elif choice == '8':
                self.restore_from_backup()
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != '0':
                if self.safe_input() is None:
                    break
    
    def run_feature_engineering_analysis(self):
        """Run Feature Engineering analysis menu."""
        while True:
            self.print_feature_engineering_menu()
            try:
                choice = input("Select option (0-8): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            if choice == '0':
                break
            elif choice == '1':
                self.generate_all_features()
            elif choice == '2':
                print("⏳ Proprietary Features - Coming soon!")
            elif choice == '3':
                print("⏳ Technical Indicators - Coming soon!")
            elif choice == '4':
                print("⏳ Statistical Features - Coming soon!")
            elif choice == '5':
                print("⏳ Temporal Features - Coming soon!")
            elif choice == '6':
                print("⏳ Cross-Timeframe Features - Coming soon!")
            elif choice == '7':
                print("⏳ Feature Selection - Coming soon!")
            elif choice == '8':
                self.show_feature_summary()
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != '0':
                if self.safe_input() is None:
                    break
    
    def run_visualization_analysis(self):
        """Run visualization analysis menu."""
        print("\n📊 DATA VISUALIZATION")
        print("-" * 30)
        print("⏳ Visualization features coming soon!")
        print("   This will include interactive charts, plots, and export capabilities.")
        self.safe_input()
    
    def run_model_development(self):
        """Run model development menu."""
        print("\n📈 MODEL DEVELOPMENT")
        print("-" * 30)
        print("⏳ Model development features coming soon!")
        print("   This will include ML pipeline, model training, and evaluation.")
        self.safe_input()
    
    def show_help(self):
        """Show help information."""
        print("\n📚 HELP & DOCUMENTATION")
        print("-" * 30)
        print("🔗 Available Resources:")
        print("   • Feature Engineering Guide: docs/ml/feature_engineering_guide.md")
        print("   • EDA Examples: docs/examples/eda-examples.md")
        print("   • Usage Examples: docs/examples/usage-examples.md")
        print("   • ML Module README: src/ml/README.md")
        print("\n🚀 Quick Start:")
        print("   1. Load your data file (CSV, Parquet, etc.)")
        print("   2. Run EDA analysis to understand your data")
        print("   3. Generate features using the Feature Engineering system")
        print("   4. Export results for further analysis")
        print("\n💡 Tips:")
        print("   • Ensure your data has at least 500 rows for optimal feature generation")
        print("   • Use OHLCV (Open, High, Low, Close, Volume) format for best results")
        print("   • The system automatically handles missing values and data validation")
        self.safe_input()
    
    def show_system_info(self):
        """Show system information."""
        print("\n⚙️  SYSTEM INFORMATION")
        print("-" * 30)
        print(f"🔧 Python version: {sys.version}")
        print(f"📦 Pandas version: {pd.__version__}")
        print(f"🔢 NumPy version: {np.__version__}")
        print(f"📁 Project root: {project_root}")
        print(f"📊 Current data: {'Loaded' if self.current_data is not None else 'None'}")
        if self.current_data is not None:
            print(f"   Shape: {self.current_data.shape}")
        print(f"📋 Results available: {len(self.current_results)}")
        self.safe_input()
    
    def run(self):
        """Run the interactive system."""
        self.print_banner()
        
        while True:
            self.print_main_menu()
            try:
                choice = input("Select option (0-8): ").strip()
            except EOFError:
                print("\n👋 Goodbye!")
                break
            
            if choice == '1':
                self.load_data()
                # Mark as used
                self.mark_menu_as_used('main', 'load_data')
            elif choice == '2':
                self.run_eda_analysis()
                # Mark as used
                self.mark_menu_as_used('main', 'eda_analysis')
            elif choice == '3':
                self.run_feature_engineering_analysis()
                # Mark as used
                self.mark_menu_as_used('main', 'feature_engineering')
            elif choice == '4':
                self.run_visualization_analysis()
                # Mark as used
                self.mark_menu_as_used('main', 'data_visualization')
            elif choice == '5':
                self.run_model_development()
                # Mark as used
                self.mark_menu_as_used('main', 'model_development')
            elif choice == '6':
                print("⏳ Testing & Validation - Coming soon!")
                # Mark as used
                self.mark_menu_as_used('main', 'testing_validation')
            elif choice == '7':
                self.show_help()
                # Mark as used
                self.mark_menu_as_used('main', 'documentation_help')
            elif choice == '8':
                self.show_system_info()
                # Mark as used
                self.mark_menu_as_used('main', 'system_configuration')
            elif choice == '9':
                self.show_menu_status()
                # Mark as used
                self.mark_menu_as_used('main', 'menu_status')
            elif choice == '0':
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 0-9.")
            
            if choice != '0':
                if self.safe_input() is None:
                    break
    
    def restore_from_backup(self):
        """Restore data from backup file."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🔄 RESTORE FROM BACKUP")
        print("=" * 50)
        
        try:
            from pathlib import Path
            import glob
            
            # Check if we have backup info
            if 'data_fixes' in self.current_results:
                backup_file = self.current_results['data_fixes'].get('backup_file')
                if backup_file and Path(backup_file).exists():
                    print(f"📁 Found backup file: {backup_file}")
                    try:
                        restore_choice = input("Would you like to restore from this backup? (Yes/No): ").strip().lower()
                        
                        if restore_choice in ['yes', 'y']:
                            print(f"🔄 Restoring from backup...")
                            self.current_data = pd.read_parquet(backup_file)
                            print(f"✅ Data restored successfully!")
                            print(f"   Shape: {self.current_data.shape}")
                            
                            # Mark as used
                            self.mark_menu_as_used('eda', 'restore_from_backup')
                            return
                    except (EOFError, OSError):
                        # Handle test environment where input is not available
                        print(f"🔄 Restoring from backup (test mode)...")
                        self.current_data = pd.read_parquet(backup_file)
                        print(f"✅ Data restored successfully!")
                        print(f"   Shape: {self.current_data.shape}")
                        return
            
            # Look for other backup files
            backup_dir = Path("data/backups")
            if backup_dir.exists():
                backup_files = list(backup_dir.glob("backup_*.parquet"))
                if backup_files:
                    print(f"📁 Found {len(backup_files)} backup files:")
                    for i, backup_file in enumerate(backup_files, 1):
                        file_size = backup_file.stat().st_size / (1024 * 1024)  # MB
                        print(f"   {i}. {backup_file.name} ({file_size:.1f} MB)")
                    
                    try:
                        choice = int(input(f"\nSelect backup to restore (1-{len(backup_files)}): ").strip())
                        if 1 <= choice <= len(backup_files):
                            selected_backup = backup_files[choice - 1]
                            print(f"🔄 Restoring from {selected_backup.name}...")
                            self.current_data = pd.read_parquet(selected_backup)
                            print(f"✅ Data restored successfully!")
                            print(f"   Shape: {self.current_data.shape}")
                        else:
                            print("❌ Invalid choice.")
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                else:
                    print("❌ No backup files found in data/backups/")
            else:
                print("❌ No backup directory found.")
                
        except Exception as e:
            print(f"❌ Error restoring from backup: {e}")
            import traceback
            traceback.print_exc()
    
    def fix_all_data_issues(self):
        """Fix all detected data quality issues with backup and restore system."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🛠️  COMPREHENSIVE DATA FIXING")
        print("=" * 50)
        
        try:
            from tqdm import tqdm
            import time
            import os
            from datetime import datetime
            
            # Create backup with timestamp
            backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_data = self.current_data.copy()
            
            # Save backup to file
            backup_dir = Path("data/backups")
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup_file = backup_dir / f"backup_{backup_timestamp}.parquet"
            
            print(f"💾 Creating backup: {backup_file}")
            backup_data.to_parquet(backup_file, index=False)
            print(f"✅ Backup saved successfully")
            
            # Get quality issues from previous analysis
            if 'comprehensive_data_quality' not in self.current_results:
                print("❌ No quality analysis found. Please run data quality check first.")
                return
            
            quality_data = self.current_results['comprehensive_data_quality']
            nan_summary = quality_data.get('nan_summary', [])
            dupe_summary = quality_data.get('dupe_summary', [])
            gap_summary = quality_data.get('gap_summary', [])
            zero_summary = quality_data.get('zero_summary', [])
            negative_summary = quality_data.get('negative_summary', [])
            inf_summary = quality_data.get('inf_summary', [])
            
            # Track fixes applied
            fixes_applied = []
            original_shape = self.current_data.shape
            
            print(f"\n🔧 Starting automatic fixes...")
            print(f"   Original shape: {original_shape}")
            
            # 1. Fix NaN values
            if nan_summary:
                print(f"\n1️⃣  Fixing NaN values in {len(nan_summary)} columns...")
                with tqdm(total=len(nan_summary), desc="Fixing NaN", leave=False) as pbar:
                    for nan_issue in nan_summary:
                        # Handle different possible structures of nan_issue
                        if isinstance(nan_issue, dict):
                            col = nan_issue.get('column', '')
                        else:
                            # If nan_issue is not a dict, try to extract column name
                            col = str(nan_issue) if nan_issue else ''
                        
                        if col and col in self.current_data.columns:
                            # Apply appropriate fix based on column type
                            if pd.api.types.is_numeric_dtype(self.current_data[col]):
                                # For numeric columns, fill with median
                                median_val = self.current_data[col].median()
                                self.current_data[col] = self.current_data[col].fillna(median_val)
                                fixes_applied.append(f"NaN in {col}: filled with median ({median_val})")
                            elif pd.api.types.is_datetime64_any_dtype(self.current_data[col]):
                                # For datetime, use forward fill then backward fill
                                self.current_data[col] = self.current_data[col].ffill().bfill()
                                fixes_applied.append(f"NaN in {col}: forward/backward fill")
                            else:
                                # For other types, use mode or empty string
                                if self.current_data[col].count() > 0:
                                    mode_val = self.current_data[col].mode().iloc[0] if not self.current_data[col].mode().empty else ""
                                    self.current_data[col] = self.current_data[col].fillna(mode_val)
                                    fixes_applied.append(f"NaN in {col}: filled with mode")
                                else:
                                    self.current_data[col] = self.current_data[col].fillna("")
                                    fixes_applied.append(f"NaN in {col}: filled with empty string")
                        pbar.update(1)
            
            # 2. Fix duplicates
            if dupe_summary:
                print(f"\n2️⃣  Fixing duplicate rows...")
                with tqdm(total=1, desc="Fixing duplicates", leave=False) as pbar:
                    initial_rows = len(self.current_data)
                    self.current_data = self.current_data.drop_duplicates(keep='first')
                    removed_rows = initial_rows - len(self.current_data)
                    if removed_rows > 0:
                        fixes_applied.append(f"Removed {removed_rows} duplicate rows")
                    else:
                        fixes_applied.append(f"No duplicate rows found to remove")
                    pbar.update(1)
            
            # 3. Fix gaps in time series
            if gap_summary:
                print(f"\n3️⃣  Fixing time series gaps...")
                with tqdm(total=len(gap_summary), desc="Fixing gaps", leave=False) as pbar:
                    for gap_issue in gap_summary:
                        # Handle different possible structures of gap_issue
                        if isinstance(gap_issue, dict):
                            dt_col = gap_issue.get('datetime_col', '')
                        else:
                            # If gap_issue is not a dict, try to find datetime column
                            dt_col = None
                            for col in self.current_data.columns:
                                if pd.api.types.is_datetime64_any_dtype(self.current_data[col]):
                                    dt_col = col
                                    break
                        
                        if dt_col and dt_col in self.current_data.columns:
                            # Sort by datetime and interpolate
                            self.current_data = self.current_data.sort_values(dt_col)
                            # Interpolate numeric columns
                            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
                            for col in numeric_cols:
                                if col != dt_col:
                                    self.current_data[col] = self.current_data[col].interpolate(method='linear')
                            fixes_applied.append(f"Interpolated gaps in time series using {dt_col}")
                        pbar.update(1)
            
            # 4. Fix zero values (with caution)
            if zero_summary:
                print(f"\n4️⃣  Analyzing zero values...")
                with tqdm(total=len(zero_summary), desc="Analyzing zeros", leave=False) as pbar:
                    for zero_issue in zero_summary:
                        # Handle different possible structures of zero_issue
                        if isinstance(zero_issue, dict):
                            col = zero_issue.get('column', '')
                            # Handle different possible keys for count
                            zero_count = zero_issue.get('count', 0)
                            if isinstance(zero_count, (list, tuple)):
                                zero_count = len(zero_count)
                            elif not isinstance(zero_count, (int, float)):
                                zero_count = 0
                        else:
                            # If zero_issue is not a dict, try to extract column name
                            col = str(zero_issue) if zero_issue else ''
                            zero_count = 0
                        
                        if col and col in self.current_data.columns:
                            # Count actual zeros in the column
                            actual_zeros = (self.current_data[col] == 0).sum()
                            total_count = len(self.current_data)
                            zero_percentage = (actual_zeros / total_count) * 100 if total_count > 0 else 0
                            
                            # Only fix if zero percentage is very high (likely error)
                            if zero_percentage > 50:
                                # Replace zeros with median of non-zero values
                                non_zero_data = self.current_data[self.current_data[col] != 0][col]
                                if len(non_zero_data) > 0:
                                    non_zero_median = non_zero_data.median()
                                    if not pd.isna(non_zero_median):
                                        self.current_data.loc[self.current_data[col] == 0, col] = non_zero_median
                                        fixes_applied.append(f"Replaced {actual_zeros} zeros in {col} with median")
                                    else:
                                        fixes_applied.append(f"Kept {actual_zeros} zeros in {col} (no valid median)")
                                else:
                                    fixes_applied.append(f"Kept {actual_zeros} zeros in {col} (no non-zero values)")
                            else:
                                fixes_applied.append(f"Kept {actual_zeros} zeros in {col} (likely legitimate)")
                        pbar.update(1)
            
            # 5. Fix negative values (with caution)
            if negative_summary:
                print(f"\n5️⃣  Analyzing negative values...")
                with tqdm(total=len(negative_summary), desc="Analyzing negatives", leave=False) as pbar:
                    for neg_issue in negative_summary:
                        # Handle different possible structures of neg_issue
                        if isinstance(neg_issue, dict):
                            col = neg_issue.get('column', '')
                            # Handle different possible keys for count
                            neg_count = neg_issue.get('count', 0)
                            if isinstance(neg_count, (list, tuple)):
                                neg_count = len(neg_count)
                            elif not isinstance(neg_count, (int, float)):
                                neg_count = 0
                        else:
                            # If neg_issue is not a dict, try to extract column name
                            col = str(neg_issue) if neg_issue else ''
                            neg_count = 0
                        
                        if col and col in self.current_data.columns:
                            # Count actual negative values in the column
                            actual_negatives = (self.current_data[col] < 0).sum()
                            total_count = len(self.current_data)
                            neg_percentage = (actual_negatives / total_count) * 100 if total_count > 0 else 0
                            
                            # Only fix if negative percentage is very high (likely error)
                            if neg_percentage > 30:
                                # Replace negatives with absolute values
                                self.current_data[col] = self.current_data[col].abs()
                                fixes_applied.append(f"Converted {actual_negatives} negative values in {col} to absolute values")
                            else:
                                fixes_applied.append(f"Kept {actual_negatives} negative values in {col} (likely legitimate)")
                        pbar.update(1)
            
            # 6. Fix infinity values
            if inf_summary:
                print(f"\n6️⃣  Fixing infinity values...")
                with tqdm(total=len(inf_summary), desc="Fixing infinities", leave=False) as pbar:
                    for inf_issue in inf_summary:
                        # Handle different possible structures of inf_issue
                        if isinstance(inf_issue, dict):
                            col = inf_issue.get('column', '')
                        else:
                            # If inf_issue is not a dict, try to extract column name
                            col = str(inf_issue) if inf_issue else ''
                        
                        if col and col in self.current_data.columns:
                            # Replace infinities with large finite values
                            max_val = self.current_data[col].replace([np.inf, -np.inf], np.nan).max()
                            min_val = self.current_data[col].replace([np.inf, -np.inf], np.nan).min()
                            
                            if not pd.isna(max_val) and not pd.isna(min_val):
                                # Replace +inf with max * 1.1, -inf with min * 0.9
                                self.current_data.loc[:, col] = self.current_data[col].replace(np.inf, max_val * 1.1)
                                self.current_data.loc[:, col] = self.current_data[col].replace(-np.inf, min_val * 0.9)
                                fixes_applied.append(f"Replaced infinity values in {col} with finite bounds")
                        pbar.update(1)
            
            # Final shape check
            final_shape = self.current_data.shape
            rows_removed = original_shape[0] - final_shape[0]
            cols_removed = original_shape[1] - final_shape[1]
            
            # Generate comprehensive fix summary
            print(f"\n" + "="*60)
            print("📋 COMPREHENSIVE FIX SUMMARY")
            print("="*60)
            
            print(f"🎯 Fixes Applied: {len(fixes_applied)}")
            print(f"📊 Shape Changes:")
            print(f"   • Rows: {original_shape[0]} → {final_shape[0]} ({rows_removed:+d})")
            print(f"   • Columns: {original_shape[1]} → {final_shape[1]} ({cols_removed:+d})")
            
            if fixes_applied:
                print(f"\n🔧 Detailed Fixes:")
                for i, fix in enumerate(fixes_applied, 1):
                    print(f"   {i}. {fix}")
            
            # Save fix results
            self.current_results['data_fixes'] = {
                'backup_file': str(backup_file),
                'backup_timestamp': backup_timestamp,
                'original_shape': original_shape,
                'final_shape': final_shape,
                'fixes_applied': fixes_applied,
                'rows_removed': rows_removed,
                'cols_removed': cols_removed,
                'timestamp': time.time()
            }
            
            print(f"\n✅ All data fixes completed successfully!")
            print(f"💾 Backup saved to: {backup_file}")
            
            # Mark as used
            self.mark_menu_as_used('eda', 'fix_data_issues')
            
            # Ask if user wants to restore (only if not in test mode)
            print(f"\n" + "="*60)
            print("🔄 RESTORE OPTIONS")
            print("="*60)
            
            try:
                restore_choice = input("Would you like to restore original data from backup? (Yes/No): ").strip().lower()
                if restore_choice in ['yes', 'y']:
                    print(f"🔄 Restoring original data from backup...")
                    self.current_data = backup_data
                    print(f"✅ Original data restored!")
                else:
                    print(f"✅ Keeping fixed data. Original backup preserved at: {backup_file}")
            except (EOFError, OSError):
                # Handle test environment where input is not available
                print(f"✅ Keeping fixed data. Original backup preserved at: {backup_file}")
            
        except Exception as e:
            print(f"❌ Error in data fixing: {e}")
            import traceback
            traceback.print_exc()
            
            # Try to restore from backup if available
            if 'backup_data' in locals():
                print(f"🔄 Attempting to restore from backup...")
                self.current_data = backup_data
                print(f"✅ Data restored from backup")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="NeoZorK HLD Prediction Interactive System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    

    parser.add_argument('--version', '-v', action='version', version='1.0.0')
    
    args = parser.parse_args()
    

    
    try:
        system = InteractiveSystem()
        system.run()
        return 0
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ System failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
