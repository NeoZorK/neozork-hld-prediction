#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive System Script for NeoZork HLD Prediction

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
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import pandas as pd
    import numpy as np
    from src.ml.feature_engineering.feature_generator import FeatureGenerator, MasterFeatureConfig
    from src.ml.feature_engineering.feature_selector import FeatureSelectionConfig
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed and the project structure is correct.")
    sys.exit(1)


class InteractiveSystem:
    """Interactive system interface for NeoZork HLD Prediction."""
    
    def __init__(self):
        """Initialize the interactive system."""
        self.feature_generator = None
        self.current_data = None
        self.current_results = {}
        
    def print_banner(self):
        """Print system banner."""
        print("\n" + "="*80)
        print("🚀 NEOZORK HLD PREDICTION - INTERACTIVE SYSTEM")
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
        print("9. 🚪 Exit")
        print("-" * 50)
        
    def print_eda_menu(self):
        """Print EDA menu options."""
        print("\n🔍 EDA ANALYSIS MENU:")
        print("1. 📊 Basic Statistics")
        print("2. 🧹 Data Quality Check")
        print("3. 🔗 Correlation Analysis")
        print("4. 📈 Time Series Analysis")
        print("5. 🎯 Feature Importance")
        print("6. 📋 Generate EDA Report")
        print("7. 🔙 Back to Main Menu")
        print("-" * 50)
        
    def print_feature_engineering_menu(self):
        """Print Feature Engineering menu options."""
        print("\n⚙️  FEATURE ENGINEERING MENU:")
        print("1. 🚀 Generate All Features")
        print("2. 🎯 Proprietary Features (PHLD/Wave)")
        print("3. 📊 Technical Indicators")
        print("4. 📈 Statistical Features")
        print("5. ⏰ Temporal Features")
        print("6. 🔄 Cross-Timeframe Features")
        print("7. 🎛️  Feature Selection & Optimization")
        print("8. 📋 Feature Summary Report")
        print("9. 🔙 Back to Main Menu")
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
        print("Choose loading method:")
        print("1. 📄 Load single file")
        print("2. 📁 Load all files from folder")
        print("3. 🔍 Load files by mask (e.g., 'gbpusd' for all GBPUSD files)")
        print("-" * 30)
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            return self._load_single_file()
        elif choice == "2":
            return self._load_folder_files()
        elif choice == "3":
            return self._load_files_by_mask()
        else:
            print("❌ Invalid choice")
            return False
    
    def _load_single_file(self) -> bool:
        """Load a single data file."""
        file_path = input("Enter data file path (CSV, Parquet, etc.): ").strip()
        
        if not file_path:
            print("❌ No file path provided")
            return False
            
        try:
            self.current_data = self.load_data_from_file(file_path)
            print(f"✅ Data loaded successfully!")
            print(f"   Shape: {self.current_data.shape[0]} rows × {self.current_data.shape[1]} columns")
            print(f"   Columns: {list(self.current_data.columns)}")
            
            # Show data preview
            show_preview = input("\nShow data preview? (y/n): ").strip().lower()
            if show_preview in ['y', 'yes']:
                print("\n📋 DATA PREVIEW:")
                print(self.current_data.head())
                print(f"\nData types:\n{self.current_data.dtypes}")
                
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def _load_folder_files(self) -> bool:
        """Load all data files from a folder."""
        folder_path = input("Enter folder path: ").strip()
        
        if not folder_path:
            print("❌ No folder path provided")
            return False
            
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"❌ Folder not found: {folder_path}")
            return False
        
        # Find all data files
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            data_files.extend(folder_path.glob(f"*{ext}"))
        
        if not data_files:
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
        print(f"   Columns: {list(self.current_data.columns)}")
        
        # Show data preview
        show_preview = input("\nShow data preview? (y/n): ").strip().lower()
        if show_preview in ['y', 'yes']:
            print("\n📋 DATA PREVIEW:")
            print(self.current_data.head())
            print(f"\nData types:\n{self.current_data.dtypes}")
        
        return True
    
    def _load_files_by_mask(self) -> bool:
        """Load files by mask pattern."""
        folder_path = input("Enter folder path: ").strip()
        mask = input("Enter file mask (e.g., 'gbpusd', 'eurusd'): ").strip().lower()
        
        if not folder_path or not mask:
            print("❌ Both folder path and mask are required")
            return False
            
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"❌ Folder not found: {folder_path}")
            return False
        
        # Find files matching mask
        data_files = []
        for ext in ['.csv', '.parquet', '.xlsx', '.xls']:
            pattern = f"*{mask}*{ext}"
            data_files.extend(folder_path.glob(pattern))
            # Also try case-insensitive search
            pattern = f"*{mask.upper()}*{ext}"
            data_files.extend(folder_path.glob(pattern))
            pattern = f"*{mask.lower()}*{ext}"
            data_files.extend(folder_path.glob(pattern))
        
        # Remove duplicates
        data_files = list(set(data_files))
        
        if not data_files:
            print(f"❌ No files found matching mask '{mask}' in {folder_path}")
            return False
        
        print(f"📁 Found {len(data_files)} files matching '{mask}':")
        for i, file in enumerate(data_files, 1):
            print(f"   {i}. {file.name}")
        
        # Load all matching files
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
        """Run basic statistical analysis."""
        if self.current_data is None:
            print("❌ No data loaded. Please load data first.")
            return
            
        print("\n📊 BASIC STATISTICS")
        print("-" * 30)
        
        try:
            # Descriptive statistics
            desc_stats = self.current_data.describe()
            print("\n📈 Descriptive Statistics:")
            print(desc_stats)
            
            # Additional statistics for numeric columns
            numeric_cols = self.current_data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                print(f"\n📊 Additional Statistics for {len(numeric_cols)} numeric columns:")
                for col in numeric_cols[:5]:  # Show first 5 columns
                    col_data = self.current_data[col].dropna()
                    if len(col_data) > 0:
                        print(f"\n{col}:")
                        print(f"  Skewness: {col_data.skew():.4f}")
                        print(f"  Kurtosis: {col_data.kurtosis():.4f}")
                        print(f"  Range: {col_data.max() - col_data.min():.4f}")
                        print(f"  IQR: {col_data.quantile(0.75) - col_data.quantile(0.25):.4f}")
            
            # Save results
            self.current_results['basic_statistics'] = {
                'descriptive_stats': desc_stats.to_dict(),
                'numeric_columns': list(numeric_cols)
            }
            
            print("\n✅ Basic statistics completed and saved!")
            
        except Exception as e:
            print(f"❌ Error in basic statistics: {e}")
    
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
                print(f"   {i:2d}. {feature:<35} {importance:.4f}")
            
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
                f.write("NEOZORK HLD PREDICTION - INTERACTIVE SYSTEM SUMMARY REPORT\n")
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
    
    def run_eda_analysis(self):
        """Run EDA analysis menu."""
        while True:
            self.print_eda_menu()
            choice = input("Select option (1-7): ").strip()
            
            if choice == '1':
                self.run_basic_statistics()
            elif choice == '2':
                self.run_data_quality_check()
            elif choice == '3':
                self.run_correlation_analysis()
            elif choice == '4':
                print("⏳ Time Series Analysis - Coming soon!")
            elif choice == '5':
                print("⏳ Feature Importance - Coming soon!")
            elif choice == '6':
                print("⏳ EDA Report Generation - Coming soon!")
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
            
            input("\nPress Enter to continue...")
    
    def run_feature_engineering_analysis(self):
        """Run Feature Engineering analysis menu."""
        while True:
            self.print_feature_engineering_menu()
            choice = input("Select option (1-9): ").strip()
            
            if choice == '1':
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
            elif choice == '9':
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
            
            input("\nPress Enter to continue...")
    
    def run_visualization_analysis(self):
        """Run visualization analysis menu."""
        print("\n📊 DATA VISUALIZATION")
        print("-" * 30)
        print("⏳ Visualization features coming soon!")
        print("   This will include interactive charts, plots, and export capabilities.")
        input("\nPress Enter to continue...")
    
    def run_model_development(self):
        """Run model development menu."""
        print("\n📈 MODEL DEVELOPMENT")
        print("-" * 30)
        print("⏳ Model development features coming soon!")
        print("   This will include ML pipeline, model training, and evaluation.")
        input("\nPress Enter to continue...")
    
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
        input("\nPress Enter to continue...")
    
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
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the interactive system."""
        self.print_banner()
        
        while True:
            self.print_main_menu()
            choice = input("Select option (1-9): ").strip()
            
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
            elif choice == '9':
                print("\n👋 Thank you for using NeoZork HLD Prediction Interactive System!")
                print("   Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-9.")
            
            if choice != '9':
                input("\nPress Enter to continue...")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="NeoZork HLD Prediction Interactive System",
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
