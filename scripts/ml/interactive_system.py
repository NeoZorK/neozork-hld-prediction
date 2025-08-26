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
    from src.eda import fix_files, html_report_generator
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
        """Print main menu options."""
        print("\n📋 MAIN MENU:")
        print("1. 📁 Load Data")
        print("2. 🔍 EDA Analysis")
        print("3. ⚙️  Feature Engineering")
        print("4. 📊 Data Visualization")
        print("5. 📈 Model Development")
        print("6. 🧪 Testing & Validation")
        print("7. 📚 Documentation & Help")
        print("8. ⚙️  System Configuration")
        print("0. 🚪 Exit")
        print("-" * 50)
        
    def print_eda_menu(self):
        """Print EDA menu options."""
        print("\n🔍 EDA ANALYSIS MENU:")
        print("0. 🔙 Back to Main Menu")
        print("1. 📊 Basic Statistics")
        print("2. 🧹 Data Quality Check")
        print("3. 🔗 Correlation Analysis")
        print("4. 📈 Time Series Analysis")
        print("5. 🎯 Feature Importance")
        print("6. 🛠️  Fix Data Issues")
        print("7. 📋 Generate HTML Report")
        print("-" * 50)
        
    def print_feature_engineering_menu(self):
        """Print Feature Engineering menu options."""
        print("\n⚙️  FEATURE ENGINEERING MENU:")
        print("0. 🔙 Back to Main Menu")
        print("1. 🚀 Generate All Features")
        print("2. 🎯 Proprietary Features (PHLD/Wave)")
        print("3. 📊 Technical Indicators")
        print("4. 📈 Statistical Features")
        print("5. ⏰ Temporal Features")
        print("6. 🔄 Cross-Timeframe Features")
        print("7. 🎛️  Feature Selection & Optimization")
        print("8. 📋 Feature Summary Report")
        print("-" * 50)
        
    def print_visualization_menu(self):
        """Print visualization menu options."""
        print("\n📊 DATA VISUALIZATION MENU:")
        print("1. 📈 Price Charts (OHLCV)")
        print("2. 📊 Feature Distribution Plots")
        print("3. 🔗 Correlation Heatmaps")
        print("4. 📈 Time Series Plots")
        print("5. 🎯 Feature Importance Charts")
        print("6. 📋 Export Visualizations")
        print("7. 🔙 Back to Main Menu")
        print("-" * 50)
        
    def print_model_development_menu(self):
        """Print model development menu options."""
        print("\n📈 MODEL DEVELOPMENT MENU:")
        print("1. 🎯 Data Preparation")
        print("2. 🔄 Feature Engineering Pipeline")
        print("3. 🤖 ML Model Training")
        print("4. 📊 Model Evaluation")
        print("5. 🧪 Hyperparameter Tuning")
        print("6. 📋 Model Report")
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
            
            # Generate summary before creating plots
            print(f"\n📋 ANALYSIS SUMMARY")
            print("=" * 50)
            print(f"📊 Dataset Overview:")
            print(f"  • Total numeric columns: {len(numeric_data.columns)}")
            print(f"  • Total observations: {len(numeric_data):,}")
            print(f"  • Columns with missing values: {len([col for col in numeric_data.columns if numeric_data[col].isna().sum() > 0])}")
            
            # Summary of key findings
            print(f"\n🔍 Key Findings:")
            skewed_cols = []
            high_outlier_cols = []
            high_cv_cols = []
            
            for col in numeric_data.columns:
                col_data = numeric_data[col].dropna()
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
            
            # Create visualizations
            print(f"\n📊 GENERATING VISUALIZATIONS...")
            self._create_statistics_plots(numeric_data)
            
            # Ask user if they want to view plots in browser
            print(f"\n🌐 VIEW PLOTS IN BROWSER")
            print("-" * 30)
            print("📊 Generated 4 visualization files:")
            print("  • distributions.png - Histograms with KDE and statistics")
            print("  • boxplots.png - Outlier detection with counts")
            print("  • correlation_heatmap.png - Feature relationships")
            print("  • statistical_summary.png - Comparative analysis charts")
            
            show_plots = input("\nShow plots in Safari browser? (y/n): ").strip().lower()
            if show_plots in ['y', 'yes']:
                self._show_plots_in_browser()
            
            # Save results
            self.current_results['basic_statistics'] = {
                'descriptive_stats': desc_stats.to_dict(),
                'numeric_columns': list(numeric_data.columns),
                'analysis_summary': {
                    'total_columns': len(numeric_data.columns),
                    'total_observations': len(numeric_data),
                    'columns_with_issues': len([col for col in numeric_data.columns 
                                              if numeric_data[col].isna().sum() > 0]),
                    'skewed_columns': skewed_cols,
                    'high_outlier_columns': high_outlier_cols,
                    'high_variability_columns': high_cv_cols
                }
            }
            
            print("\n✅ Comprehensive basic statistics completed and saved!")
            print("📁 Plots saved to: results/plots/statistics/")
            
        except Exception as e:
            print(f"❌ Error in basic statistics: {e}")
            import traceback
            traceback.print_exc()
    
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
        """Create comprehensive statistical visualizations."""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            # Set modern style
            plt.style.use('seaborn-v0_8')
            sns.set_palette("husl")
            
            # Create plots directory
            plots_dir = Path("results/plots/statistics")
            plots_dir.mkdir(parents=True, exist_ok=True)
            
            # Limit to first 6 columns for visualization
            cols_to_plot = numeric_data.columns[:6]
            
            # 1. Distribution plots
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Distribution Analysis', fontsize=16, fontweight='bold')
            
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
            
            # 2. Box plots
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('Box Plot Analysis (Outlier Detection)', fontsize=16, fontweight='bold')
            
            for i, col in enumerate(cols_to_plot):
                row, col_idx = i // 3, i % 3
                col_data = numeric_data[col].dropna()
                
                if len(col_data) > 0:
                    sns.boxplot(y=col_data, ax=axes[row, col_idx])
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
            
            # 3. Correlation heatmap
            if len(cols_to_plot) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                corr_matrix = numeric_data[cols_to_plot].corr()
                
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                           square=True, ax=ax, fmt='.3f')
                ax.set_title('Correlation Matrix', fontsize=16, fontweight='bold')
                
                plt.tight_layout()
                plt.savefig(plots_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
                plt.close()
            
            # 4. Summary statistics visualization
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
            
            print(f"✅ Generated 4 visualization files:")
            print(f"   • distributions.png - Distribution analysis")
            print(f"   • boxplots.png - Outlier detection")
            print(f"   • correlation_heatmap.png - Feature relationships")
            print(f"   • statistical_summary.png - Statistical comparisons")
            
        except ImportError:
            print("⚠️  matplotlib/seaborn not available - skipping visualizations")
        except Exception as e:
            print(f"⚠️  Error creating visualizations: {e}")
    
    def run_data_quality_check(self):
        """Run data quality check."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n🧹 DATA QUALITY CHECK")
        print("-" * 30)
        
        try:
            # Missing values
            missing_data = self.current_data.isna().sum()
            total_missing = missing_data.sum()
            total_cells = self.current_data.shape[0] * self.current_data.shape[1]
            missing_percentage = (total_missing / total_cells) * 100
            
            print(f"📊 Missing Values Analysis:")
            print(f"  Total missing values: {total_missing}")
            print(f"  Missing percentage: {missing_percentage:.2f}%")
            
            if total_missing > 0:
                print(f"  Missing by column:")
                for col, missing in missing_data[missing_data > 0].items():
                    print(f"    {col}: {missing} ({missing/self.current_data.shape[0]*100:.2f}%)")
            
            # Duplicates
            duplicates = self.current_data.duplicated().sum()
            duplicate_percentage = (duplicates / self.current_data.shape[0]) * 100
            
            print(f"\n🔄 Duplicate Analysis:")
            print(f"  Total duplicates: {duplicates}")
            print(f"  Duplicate percentage: {duplicate_percentage:.2f}%")
            
            # Data types
            dtype_counts = self.current_data.dtypes.value_counts()
            print(f"\n🔧 Data Types:")
            for dtype, count in dtype_counts.items():
                print(f"  {dtype}: {count} columns")
            
            # Save results
            self.current_results['data_quality'] = {
                'missing_values': missing_data.to_dict(),
                'total_missing': total_missing,
                'missing_percentage': missing_percentage,
                'duplicates': duplicates,
                'duplicate_percentage': duplicate_percentage,
                'data_types': dtype_counts.to_dict()
            }
            
            print("\n✅ Data quality check completed and saved!")
            
        except Exception as e:
            print(f"❌ Error in data quality check: {e}")
    
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
            
            # Generate and save report
            report_path = reports_dir / f"interactive_report_{timestamp}.html"
            html_report.save(str(report_path))
            
            print(f"✅ HTML report generated: {report_path}")
            print(f"   Open the file in your web browser to view the complete report")
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {e}")
            import traceback
            traceback.print_exc()
    
    def run_eda_analysis(self):
        """Run EDA analysis menu."""
        while True:
            self.print_eda_menu()
            try:
                choice = input("Select option (0-7): ").strip()
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
            else:
                print("❌ Invalid choice. Please select 0-7.")
            
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
            elif choice == '2':
                self.run_eda_analysis()
            elif choice == '3':
                self.run_feature_engineering_analysis()
            elif choice == '4':
                self.run_visualization_analysis()
            elif choice == '5':
                self.run_model_development()
            elif choice == '6':
                print("⏳ Testing & Validation - Coming soon!")
            elif choice == '7':
                self.show_help()
            elif choice == '8':
                self.show_system_info()
            elif choice == '0':
                print("\n👋 Thank you for using NeoZorK HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 0-8.")
            
            if choice != '0':
                if self.safe_input() is None:
                    break


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
