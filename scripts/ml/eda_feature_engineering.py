#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EDA Feature Engineering Integration Script

This script integrates the existing EDA capabilities with the new Feature Engineering system.
It provides a unified interface for data analysis, feature generation, and comprehensive reporting.

Usage:
    python scripts/eda_feature_engineering.py [options]
    ./eda_feature_engineering.py [options]

Options:
    --help, -h              Show this help message
    --version, -v           Show version information
    --file FILE, -f FILE    Input data file (CSV, Parquet, etc.)
    --output-dir DIR, -o DIR Output directory for reports
    --config CONFIG, -c CONFIG Configuration file for feature engineering
    --eda-only              Run only EDA analysis (no feature engineering)
    --features-only         Run only feature engineering (no EDA)
    --full-pipeline         Run complete EDA + Feature Engineering pipeline
    --quality-check         Run data quality checks
    --basic-stats           Run basic statistical analysis
    --correlation           Run correlation analysis
    --feature-importance    Run feature importance analysis
    --visualize             Generate visualizations
    --export-results        Export results to files
    --verbose               Verbose output
    --debug                 Debug mode

Examples:
    # Run complete pipeline
    python scripts/eda_feature_engineering.py --file data.csv --full-pipeline

    # EDA only
    python scripts/eda_feature_engineering.py --file data.csv --eda-only

    # Feature engineering only
    python scripts/eda_feature_engineering.py --file data.csv --features-only

    # Custom configuration
    python scripts/eda_feature_engineering.py --file data.csv --config config.json --full-pipeline
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


class EDAFeatureEngineeringPipeline:
    """Integrated pipeline for EDA and Feature Engineering."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the pipeline with configuration."""
        self.config = config or {}
        self.results = {}
        self.start_time = time.time()
        
        # Initialize feature generator
        self.feature_generator = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from various file formats."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        print(f"Loading data from: {file_path}")
        
        if file_path.suffix.lower() == '.csv':
            data = pd.read_csv(file_path)
        elif file_path.suffix.lower() == '.parquet':
            data = pd.read_parquet(file_path)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            data = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        print(f"Data loaded: {data.shape[0]} rows × {data.shape[1]} columns")
        print(f"Columns: {list(data.columns)}")
        
        return data
    
    def run_data_quality_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run comprehensive data quality analysis."""
        print("\n" + "="*60)
        print("RUNNING DATA QUALITY ANALYSIS")
        print("="*60)
        
        try:
            # Missing values analysis
            missing_analysis = {
                'total_missing': data.isna().sum().sum(),
                'missing_by_column': data.isna().sum().to_dict(),
                'missing_percentage': (data.isna().sum().sum() / (data.shape[0] * data.shape[1])) * 100
            }
            
            # Duplicate analysis
            duplicate_analysis = {
                'total_duplicates': data.duplicated().sum(),
                'duplicate_percentage': (data.duplicated().sum() / data.shape[0]) * 100
            }
            
            # Data types analysis
            dtype_analysis = {
                'numeric_columns': list(data.select_dtypes(include=[np.number]).columns),
                'categorical_columns': list(data.select_dtypes(include=['object']).columns),
                'datetime_columns': list(data.select_dtypes(include=['datetime']).columns)
            }
            
            # Data range analysis for OHLCV
            range_analysis = {}
            if 'Open' in data.columns and 'High' in data.columns and 'Low' in data.columns and 'Close' in data.columns:
                range_analysis = {
                    'price_range': {
                        'min': min(data[['Open', 'High', 'Low', 'Close']].min().min(), data['Close'].min()),
                        'max': max(data[['Open', 'High', 'Low', 'Close']].max().max(), data['Close'].max())
                    },
                    'volume_range': {
                        'min': data['Volume'].min() if 'Volume' in data.columns else None,
                        'max': data['Volume'].max() if 'Volume' in data.columns else None
                    }
                }
            
            quality_results = {
                'missing_analysis': missing_analysis,
                'duplicate_analysis': duplicate_analysis,
                'dtype_analysis': dtype_analysis,
                'range_analysis': range_analysis
            }
            
            self.results['data_quality'] = quality_results
            
            # Print summary
            print(f"Data Quality Analysis Results:")
            print(f"  - Total missing values: {missing_analysis['total_missing']}")
            print(f"  - Missing percentage: {missing_analysis['missing_percentage']:.2f}%")
            print(f"  - Total duplicates: {duplicate_analysis['total_duplicates']}")
            print(f"  - Duplicate percentage: {duplicate_analysis['duplicate_percentage']:.2f}%")
            print(f"  - Numeric columns: {len(dtype_analysis['numeric_columns'])}")
            print(f"  - Categorical columns: {len(dtype_analysis['categorical_columns'])}")
            print(f"  - Datetime columns: {len(dtype_analysis['datetime_columns'])}")
            
            if range_analysis:
                print(f"  - Price range: {range_analysis['price_range']['min']:.4f} - {range_analysis['price_range']['max']:.4f}")
                if range_analysis['volume_range']['min'] is not None:
                    print(f"  - Volume range: {range_analysis['volume_range']['min']:,} - {range_analysis['volume_range']['max']:,}")
            
            return quality_results
            
        except Exception as e:
            print(f"Error in data quality analysis: {e}")
            return {}
    
    def run_basic_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run basic statistical analysis."""
        print("\n" + "="*60)
        print("RUNNING BASIC STATISTICAL ANALYSIS")
        print("="*60)
        
        try:
            # Descriptive statistics
            desc_stats = data.describe()
            
            # Additional statistics
            additional_stats = {}
            for col in data.select_dtypes(include=[np.number]).columns:
                col_data = data[col].dropna()
                if len(col_data) > 0:
                    additional_stats[col] = {
                        'skewness': col_data.skew(),
                        'kurtosis': col_data.kurtosis(),
                        'variance': col_data.var(),
                        'range': col_data.max() - col_data.min(),
                        'iqr': col_data.quantile(0.75) - col_data.quantile(0.25)
                    }
            
            # Time series analysis (if applicable)
            time_series_stats = {}
            if len(data.select_dtypes(include=['datetime']).columns) > 0:
                time_series_stats = {
                    'has_timestamps': True,
                    'time_range': {
                        'start': data.select_dtypes(include=['datetime']).iloc[:, 0].min(),
                        'end': data.select_dtypes(include=['datetime']).iloc[:, 0].max()
                    }
                }
            
            stats_results = {
                'descriptive_stats': desc_stats.to_dict(),
                'additional_stats': additional_stats,
                'time_series_stats': time_series_stats
            }
            
            self.results['basic_statistics'] = stats_results
            
            # Print summary
            print(f"Basic Statistics Results:")
            print(f"  - Descriptive statistics generated for {len(data.select_dtypes(include=[np.number]).columns)} numeric columns")
            print(f"  - Additional statistics (skewness, kurtosis, etc.) calculated")
            if time_series_stats.get('has_timestamps'):
                print(f"  - Time series detected: {time_series_stats['time_range']['start']} to {time_series_stats['time_range']['end']}")
            
            return stats_results
            
        except Exception as e:
            print(f"Error in basic statistics: {e}")
            return {}
    
    def run_correlation_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run correlation analysis."""
        print("\n" + "="*60)
        print("RUNNING CORRELATION ANALYSIS")
        print("="*60)
        
        try:
            # Filter out non-numeric columns and handle datetime conversion
            numeric_data = data.copy()
            
            # Convert datetime columns to numeric if possible
            for col in numeric_data.columns:
                if numeric_data[col].dtype == 'object':
                    try:
                        # Try to convert to datetime first
                        pd.to_datetime(numeric_data[col], errors='coerce')
                        # If successful, convert to numeric (timestamp)
                        numeric_data[col] = pd.to_datetime(numeric_data[col], errors='coerce').astype(np.int64) // 10**9
                    except:
                        # If not datetime, try to convert to numeric
                        try:
                            numeric_data[col] = pd.to_numeric(numeric_data[col], errors='coerce')
                        except:
                            # If all else fails, drop the column
                            numeric_data = numeric_data.drop(columns=[col])
            
            # Select only numeric columns
            numeric_data = numeric_data.select_dtypes(include=[np.number])
            
            if numeric_data.shape[1] < 2:
                print("  - Insufficient numeric columns for correlation analysis")
                return {}
            
            # Pearson correlation
            pearson_corr = numeric_data.corr(method='pearson')
            
            # Spearman correlation
            spearman_corr = numeric_data.corr(method='spearman')
            
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
            
            corr_results = {
                'pearson_correlation': pearson_corr.to_dict(),
                'spearman_correlation': spearman_corr.to_dict(),
                'high_correlation_pairs': high_corr_pairs
            }
            
            self.results['correlation_analysis'] = corr_results
            
            # Print summary
            print(f"Correlation Analysis Results:")
            print(f"  - Pearson correlation matrix: {pearson_corr.shape[0]} × {pearson_corr.shape[1]}")
            print(f"  - Spearman correlation matrix: {spearman_corr.shape[0]} × {spearman_corr.shape[1]}")
            print(f"  - High correlation pairs (|r| > 0.8): {len(high_corr_pairs)}")
            
            if high_corr_pairs:
                print("  - Top high correlation pairs:")
                for pair in high_corr_pairs[:5]:
                    print(f"    {pair['col1']} ↔ {pair['col2']}: {pair['correlation']:.3f}")
            
            return corr_results
            
        except Exception as e:
            print(f"Error in correlation analysis: {e}")
            return {}
    
    def run_feature_engineering(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run feature engineering pipeline."""
        print("\n" + "="*60)
        print("RUNNING FEATURE ENGINEERING PIPELINE")
        print("="*60)
        
        try:
            # Ensure minimum data size
            if data.shape[0] < 500:
                print(f"  - Warning: Data has only {data.shape[0]} rows, minimum recommended is 500")
                print(f"  - Padding data to 500 rows for feature generation...")
                
                # Pad data by repeating last rows
                padding_needed = 500 - data.shape[0]
                padding_data = data.iloc[-padding_needed:].copy()
                data = pd.concat([data, padding_data], ignore_index=True)
                print(f"  - Data padded to {data.shape[0]} rows")
            
            # Clean data: handle infinite values and NaN
            print("  - Cleaning data (handling infinite values and NaN)...")
            data_clean = data.copy()
            
            # Replace infinite values with NaN
            data_clean = data_clean.replace([np.inf, -np.inf], np.nan)
            
            # Fill NaN values with appropriate methods
            for col in data_clean.columns:
                if data_clean[col].dtype in ['float64', 'float32']:
                    # For numeric columns, fill with median
                    median_val = data_clean[col].median()
                    if pd.isna(median_val):
                        median_val = 0
                    data_clean[col] = data_clean[col].fillna(median_val)
                elif data_clean[col].dtype == 'object':
                    # For object columns, fill with mode
                    mode_val = data_clean[col].mode()
                    if len(mode_val) > 0:
                        data_clean[col] = data_clean[col].fillna(mode_val[0])
                    else:
                        data_clean[col] = data_clean[col].fillna('unknown')
            
            print(f"  - Data cleaned: {data_clean.shape[0]} rows × {data_clean.shape[1]} columns")
            
            # Initialize feature generator with configuration
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
            print("  - Generating features...")
            data_with_features = self.feature_generator.generate_features(data_clean)
            
            # Get feature summary
            feature_summary = self.feature_generator.get_feature_summary()
            
            # Get memory usage
            memory_usage = self.feature_generator.get_memory_usage()
            
            feature_results = {
                'original_shape': data.shape,
                'final_shape': data_with_features.shape,
                'features_generated': data_with_features.shape[1] - data.shape[1],
                'feature_summary': feature_summary,
                'memory_usage': memory_usage,
                'data_with_features': data_with_features
            }
            
            self.results['feature_engineering'] = feature_results
            
            # Print summary
            print(f"Feature Engineering Results:")
            print(f"  - Original data: {data.shape[0]} rows × {data.shape[1]} columns")
            print(f"  - Final data: {data_with_features.shape[0]} rows × {data_with_features.shape[1]} columns")
            print(f"  - Features generated: {feature_results['features_generated']}")
            
            # Safe memory usage printing
            if isinstance(memory_usage, dict) and 'rss' in memory_usage:
                print(f"  - Memory usage: {memory_usage['rss']:.1f} MB")
            elif isinstance(memory_usage, dict):
                print(f"  - Memory usage: {memory_usage}")
            else:
                print(f"  - Memory usage: {memory_usage}")
            
            return feature_results
            
        except Exception as e:
            print(f"Error in feature engineering: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def run_feature_importance_analysis(self, data_with_features: pd.DataFrame) -> Dict[str, Any]:
        """Run feature importance analysis on engineered features."""
        print("\n" + "="*60)
        print("RUNNING FEATURE IMPORTANCE ANALYSIS")
        print("="*60)
        
        try:
            if self.feature_generator is None:
                print("  - Feature engineering must be run first")
                return {}
            
            # Get feature importance from feature generator
            feature_importance = self.feature_generator.get_feature_summary()
            
            # Sort features by importance
            sorted_features = sorted(
                feature_importance.items(),
                key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0,
                reverse=True
            )
            
            # Top features
            top_features = sorted_features[:20]
            
            importance_results = {
                'feature_importance': feature_importance,
                'top_features': top_features,
                'total_features': len(feature_importance)
            }
            
            self.results['feature_importance'] = importance_results
            
            # Print summary
            print(f"Feature Importance Results:")
            print(f"  - Total features analyzed: {len(feature_importance)}")
            print(f"  - Top 10 features by importance:")
            for i, (feature, importance) in enumerate(top_features[:10], 1):
                try:
                    if isinstance(importance, (int, float)):
                        print(f"    {i:2d}. {feature:<35} {importance:.4f}")
                    else:
                        print(f"    {i:2d}. {feature:<35} {importance}")
                except Exception as e:
                    print(f"    {i:2d}. {feature:<35} [Error formatting: {importance}]")
            
            return importance_results
            
        except Exception as e:
            print(f"Error in feature importance analysis: {e}")
            return {}
    
    def generate_simple_report(self, output_dir: str) -> str:
        """Generate simple text report."""
        print("\n" + "="*60)
        print("GENERATING SIMPLE REPORT")
        print("="*60)
        
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate simple text report
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_path = output_path / f'eda_feature_engineering_report_{timestamp}.txt'
            
            with open(report_path, 'w') as f:
                f.write("NEOZORK HLD PREDICTION - EDA FEATURE ENGINEERING REPORT\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for key, value in self.results.items():
                    f.write(f"{key.upper()}:\n")
                    f.write("-" * 30 + "\n")
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if k != 'data_with_features':
                                f.write(f"  {k}: {v}\n")
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
            
            print(f"  - Report generated: {report_path}")
            
            # Export results to JSON
            json_path = output_path / f'eda_feature_engineering_results_{timestamp}.json'
            
            # Convert results for JSON serialization
            exportable_results = {}
            for key, value in self.results.items():
                if key == 'data_with_features':
                    exportable_results[key] = f"DataFrame with shape {value.shape}"
                else:
                    exportable_results[key] = value
            
            with open(json_path, 'w') as f:
                json.dump(exportable_results, f, indent=2, default=str)
            print(f"  - Results exported to JSON: {json_path}")
            
            return str(report_path)
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return ""
    
    def run_pipeline(self, file_path: str, output_dir: str, 
                    run_eda: bool = True, run_features: bool = True) -> Dict[str, Any]:
        """Run the complete pipeline."""
        print("="*80)
        print("EDA FEATURE ENGINEERING INTEGRATED PIPELINE")
        print("="*80)
        print(f"Input file: {file_path}")
        print(f"Output directory: {output_dir}")
        print(f"Run EDA: {run_eda}")
        print(f"Run Feature Engineering: {run_features}")
        print("="*80)
        
        try:
            # Load data
            data = self.load_data(file_path)
            
            # Run EDA components
            if run_eda:
                self.run_data_quality_analysis(data)
                self.run_basic_statistics(data)
                self.run_correlation_analysis(data)
            
            # Run feature engineering
            if run_features:
                self.run_feature_engineering(data)
                
                # Run feature importance analysis if features were generated
                if 'feature_engineering' in self.results:
                    data_with_features = self.results['feature_engineering']['data_with_features']
                    self.run_feature_importance_analysis(data_with_features)
            
            # Generate report
            report_path = self.generate_simple_report(output_dir)
            
            # Calculate execution time
            execution_time = time.time() - self.start_time
            
            # Final summary
            print("\n" + "="*80)
            print("PIPELINE EXECUTION COMPLETED")
            print("="*80)
            print(f"Total execution time: {execution_time:.2f} seconds")
            print(f"Results saved to: {output_dir}")
            if report_path:
                print(f"Report: {report_path}")
            print("="*80)
            
            return self.results
            
        except Exception as e:
            print(f"Pipeline execution failed: {e}")
            import traceback
            traceback.print_exc()
            return {}


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="EDA Feature Engineering Integration Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--file', '-f', required=True,
                       help='Input data file (CSV, Parquet, etc.)')
    parser.add_argument('--output-dir', '-o', default='./reports',
                       help='Output directory for reports (default: ./reports)')
    parser.add_argument('--config', '-c',
                       help='Configuration file for feature engineering')
    parser.add_argument('--eda-only', action='store_true',
                       help='Run only EDA analysis (no feature engineering)')
    parser.add_argument('--features-only', action='store_true',
                       help='Run only feature engineering (no EDA)')
    parser.add_argument('--full-pipeline', action='store_true',
                       help='Run complete EDA + Feature Engineering pipeline')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    parser.add_argument('--debug', action='store_true',
                       help='Debug mode')
    parser.add_argument('--version', '-v', action='version', version='1.0.0')
    
    args = parser.parse_args()
    
    # Load configuration if provided
    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file {args.config}: {e}")
    
    # Determine what to run
    run_eda = not args.features_only
    run_features = not args.eda_only
    
    if args.full_pipeline:
        run_eda = True
        run_features = True
    
    # Initialize and run pipeline
    pipeline = EDAFeatureEngineeringPipeline(config)
    
    try:
        results = pipeline.run_pipeline(
            file_path=args.file,
            output_dir=args.output_dir,
            run_eda=run_eda,
            run_features=run_features
        )
        
        if results:
            print("\n✅ Pipeline completed successfully!")
            return 0
        else:
            print("\n❌ Pipeline failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
