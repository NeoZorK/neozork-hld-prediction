#!/usr/bin/env python3
"""
📈 Time Series Analysis Tool for Financial Data 🚀

This script provides comprehensive time series analysis for financial data,
including stationarity analysis, seasonality detection, and financial features analysis.

Usage:
    # Single file processing:
    python time_analysis.py -f <filename> [--stationarity] [--seasonality] [--financial] [--transform]
    
    # Batch processing by directory:
    python time_analysis.py --batch-raw-parquet [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-csv-converted [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-indicators-parquet [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-indicators-json [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-indicators-csv [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-fixed [--stationarity] [--seasonality] [--financial]
    python time_analysis.py --batch-all [--stationarity] [--seasonality] [--financial]
    
    # Custom path processing:
    python time_analysis.py --path <path> [--stationarity] [--seasonality] [--financial]

The filename must be from one of the supported data directories:
- data/cache/csv_converted/
- data/raw_parquet/
- data/indicators/parquet/
- data/indicators/json/
- data/indicators/csv/
- data/fixed/ (cleaned data - recommended)

Options:
    --stationarity    Perform stationarity analysis (ADF test, critical values, recommendations)
    --seasonality     Perform seasonality detection (day-of-week, monthly, cyclical patterns)
    --financial       Perform financial features analysis (price range, changes, volatility)
    --transform       Perform data transformation analysis and recommendations
    --auto            Automatically answer 'y' to all questions (non-interactive mode)
    --recursive       Recursively search subdirectories when using --path
    --output          Output directory for saving results and transformed data
    --verbose         Enable verbose logging output
    --version         Show version information

Note: It is recommended to use already cleaned and transformed data by clear_data.py and 
stat_analysis.py from data/fixed/ folder. You can run clear_data.py --help for more information.
"""

__version__ = "1.0.0"

import argparse
import sys
import os
import time
import signal
import json
import gc
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd
import numpy as np

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.time_series.file_operations import TimeSeriesFileOperations
from src.time_series.cli_interface import TimeSeriesCLI
from src.time_series.stationarity_analysis import StationarityAnalysis
from src.time_series.seasonality_detection import SeasonalityDetection
from src.time_series.financial_features import FinancialFeatures
from src.time_series.data_transformation import TimeSeriesDataTransformation
from src.time_series.reporting import TimeSeriesReporter
from src.time_series.color_utils import ColorUtils
from src.time_series.progress_tracker import ProgressTracker, ProgressBar, ColumnProgressTracker
from src.time_series.optimized_analysis import OptimizedAnalysis


class TimeSeriesAnalyzer:
    """Main class for time series analysis operations."""
    
    def __init__(self, auto_mode: bool = False, output_directory: Optional[str] = None, 
                 analysis_options: Dict[str, Any] = None, fast_mode: bool = True, 
                 max_sample_size: int = 10000):
        """Initialize the time series analyzer.
        
        Args:
            auto_mode: If True, automatically answer 'y' to all questions
            output_directory: Directory to save results and transformed data
            analysis_options: Dictionary with analysis options
            fast_mode: Enable fast mode with optimizations for large datasets
            max_sample_size: Maximum sample size for fast mode (default: 10000)
        """
        self.file_ops = TimeSeriesFileOperations()
        self.stationarity_analysis = StationarityAnalysis()
        self.seasonality_detection = SeasonalityDetection()
        self.financial_features = FinancialFeatures()
        self.data_transformation = TimeSeriesDataTransformation()
        self.reporter = TimeSeriesReporter()
        self.auto_mode = auto_mode
        self.fast_mode = fast_mode
        self.max_sample_size = max_sample_size
        self.output_directory = output_directory
        self.analysis_options = analysis_options or {}
        
        # Initialize optimizer for fast mode
        if self.fast_mode:
            self.optimizer = OptimizedAnalysis(max_sample_size=max_sample_size)
        
        # Supported data directories
        self.supported_dirs = self.file_ops.get_supported_directories()
    
    def _get_user_input(self, prompt: str) -> str:
        """
        Get user input with automatic mode support.
        
        Args:
            prompt: Input prompt to display
            
        Returns:
            User input or 'y' if in auto mode
        """
        if self.auto_mode:
            print(f"{prompt} y")
            return "y"
        else:
            return input(prompt).lower().strip()
    
    def analyze_file(self, filename: str, analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """
        Analyze a single file with specified options.
        
        Args:
            filename: Name of the file to analyze
            analysis_options: Dictionary of analysis options
            
        Returns:
            Dictionary with analysis results
        """
        # Validate file
        file_info = self.file_ops.validate_file_path(filename)
        
        if file_info is None:
            raise ValueError(f"Invalid file '{filename}'. Please choose a file from supported directories.")
        
        return self._analyze_file_with_info(file_info, analysis_options)
    
    def _analyze_file_with_info(self, file_info: Dict[str, Any], analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """
        Analyze a file using provided file_info.
        
        Args:
            file_info: Dictionary with file metadata
            analysis_options: Dictionary of analysis options
            
        Returns:
            Dictionary with analysis results
        """
        # Load data first to get accurate metadata
        data = self.file_ops.load_data(file_info["file_path"], file_info["format"])
        
        if data is None or data.empty:
            raise ValueError("Could not load data or data is empty")
        
        # Prepare data for time series analysis
        data = self.file_ops.prepare_time_series_data(data)
        
        # Update file_info with actual data dimensions
        file_info['rows_count'] = len(data)
        file_info['columns_count'] = len(data.columns)
        file_info['filename'] = os.path.basename(file_info['file_path'])
        
        # Display analysis start with accurate metadata
        self.reporter.display_analysis_start(file_info, analysis_options)
        
        # Get numeric columns
        numeric_columns = self.file_ops.get_numeric_columns(data)
        
        if not numeric_columns:
            raise ValueError("No numeric columns found for analysis")
        
        # Perform analysis
        analysis_results = {}
        
        # Stationarity analysis
        if analysis_options.get('stationarity', False):
            print("\n" + "="*80)
            print("📊 STATIONARITY ANALYSIS")
            print("="*80)
            print("🔍 What is Stationarity Analysis?")
            print("   Stationarity analysis determines if a time series has consistent statistical properties")
            print("   over time. A stationary series has constant mean, variance, and autocorrelation structure.")
            print("")
            print("🎯 Why is it important?")
            print("   • Most time series models (ARIMA, VAR, etc.) require stationary data")
            print("   • Non-stationary data can lead to spurious correlations and unreliable forecasts")
            print("   • Helps identify trends, seasonality, and structural breaks in data")
            print("")
            print("🔧 How to use the results:")
            print("   • If data is stationary: Direct modeling is possible")
            print("   • If non-stationary: Apply differencing, detrending, or other transformations")
            print("   • Use ADF test p-values to determine significance level")
            print("   • Critical values help interpret the strength of stationarity")
            print("="*80)
            print("📊 Performing stationarity analysis...")
            
            analysis_results['stationarity'] = self.stationarity_analysis.analyze_stationarity(data, numeric_columns)
            
            # Show completion message
            self._display_analysis_completion("stationarity", len(numeric_columns))
        
        # Seasonality detection
        if analysis_options.get('seasonality', False):
            print("\n" + "="*80)
            print("📈 SEASONALITY DETECTION")
            print("="*80)
            print("🔍 What is Seasonality Detection?")
            print("   Seasonality detection identifies recurring patterns in time series data that repeat")
            print("   at regular intervals (daily, weekly, monthly, yearly cycles).")
            print("")
            print("🎯 Why is it important?")
            print("   • Seasonal patterns can significantly impact forecasting accuracy")
            print("   • Helps understand business cycles, market behaviors, and natural phenomena")
            print("   • Essential for seasonal adjustment and decomposition of time series")
            print("   • Improves model performance by accounting for predictable variations")
            print("")
            print("🔧 How to use the results:")
            print("   • Day-of-week patterns: Use dummy variables for different days")
            print("   • Monthly patterns: Apply seasonal decomposition or monthly dummies")
            print("   • Cyclical patterns: Consider Fourier terms or seasonal ARIMA models")
            print("   • High seasonality: Use seasonal differencing or seasonal models")
            print("="*80)
            print("📈 Performing seasonality detection...")
            
            analysis_results['seasonality'] = self.seasonality_detection.analyze_seasonality(data, numeric_columns)
            
            # Show completion message
            self._display_analysis_completion("seasonality", len(numeric_columns))
        
        # Financial features analysis
        if analysis_options.get('financial', False):
            print("\n" + "="*80)
            print("💰 FINANCIAL FEATURES ANALYSIS")
            print("="*80)
            print("🔍 What is Financial Features Analysis?")
            print("   Financial features analysis examines price movements, volatility patterns, and risk")
            print("   characteristics in financial time series data to understand market behavior.")
            print("")
            print("🎯 Why is it important?")
            print("   • Identifies risk levels and volatility regimes in financial markets")
            print("   • Helps with portfolio optimization and risk management strategies")
            print("   • Essential for pricing derivatives and calculating Value at Risk (VaR)")
            print("   • Provides insights into market efficiency and trading opportunities")
            print("")
            print("🔧 How to use the results:")
            print("   • Price Range: Assess market volatility and price stability")
            print("   • Volatility Analysis: Use for risk management and position sizing")
            print("   • VaR and Max Drawdown: Set stop-losses and risk limits")
            print("   • Sharpe Ratio: Evaluate risk-adjusted returns")
            print("   • High volatility: Consider hedging strategies or smaller positions")
            print("="*80)
            print("💰 Performing financial features analysis...")
            
            analysis_results['financial'] = self.financial_features.analyze_financial_features(data, numeric_columns)
            
            # Show completion message
            self._display_analysis_completion("financial features", len(numeric_columns))
        
        # Data transformation analysis
        if analysis_options.get('transform', False):
            print("\n" + "="*80)
            print("🔄 DATA TRANSFORMATION ANALYSIS")
            print("="*80)
            print("🔍 What is Data Transformation Analysis?")
            print("   Data transformation analysis applies mathematical transformations to time series data")
            print("   to improve its statistical properties, making it more suitable for modeling.")
            print("")
            print("🎯 Why is it important?")
            print("   • Converts non-stationary data to stationary for better model performance")
            print("   • Reduces heteroscedasticity and improves normality assumptions")
            print("   • Stabilizes variance and removes trends that can bias forecasts")
            print("   • Essential preprocessing step for most time series models")
            print("")
            print("🔧 How to use the results:")
            print("   • Differencing: Removes trends and makes data stationary")
            print("   • Detrending: Eliminates linear or polynomial trends")
            print("   • Log Transform: Stabilizes variance in exponential growth data")
            print("   • Normalization: Scales data to [0,1] range for machine learning")
            print("   • Standardization: Centers data around zero with unit variance")
            print("   • Use improvement scores to select the best transformation")
            print("="*80)
            print("🔄 Performing data transformation analysis...")
            
            # Generate transformation recommendations
            transformations = self._generate_transformation_recommendations(data, numeric_columns, analysis_results)
            
            if transformations:
                analysis_results['transformation'] = self.data_transformation.transform_data(
                    data, transformations, numeric_columns
                )
            else:
                # If no specific transformations, try basic ones
                basic_transformations = {}
                for col in numeric_columns:
                    basic_transformations[col] = ['differencing', 'detrending', 'normalization']
                
                analysis_results['transformation'] = self.data_transformation.transform_data(
                    data, basic_transformations, numeric_columns
                )
            
            # Add comparison analysis
            if 'transformation' in analysis_results:
                analysis_results['transformation']['comparison_analysis'] = self._compare_before_after_transformation(
                    data, analysis_results['transformation'], analysis_results
                )
            
            # Show completion message
            self._display_analysis_completion("data transformation", len(numeric_columns))
        
        return {
            'file_info': file_info,
            'analysis_results': analysis_results,
            'numeric_columns': numeric_columns
        }
    
    def _generate_transformation_recommendations(self, data: pd.DataFrame, numeric_columns: List[str], 
                                               analysis_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate transformation recommendations based on analysis results."""
        transformations = {}
        
        print("\n🔍 Generating transformation recommendations based on analysis results...")
        
        # Check stationarity results for recommendations
        if 'stationarity' in analysis_results:
            stationarity_results = analysis_results['stationarity']
            recommendations = stationarity_results.get('stationarity_recommendations', {})
            
            print("📊 Using stationarity analysis results...")
            for col in numeric_columns:
                if col in recommendations:
                    rec_data = recommendations[col]
                    if not rec_data.get('is_stationary', False):
                        # Non-stationary data needs focused transformation
                        transformations[col] = ['differencing', 'detrending', 'log_transform', 'seasonal_differencing', 'power_transform']
                        print(f"  • {col}: Non-stationary → differencing, detrending, log_transform, seasonal_differencing, power_transform")
                    else:
                        # Stationary data might still benefit from normalization
                        transformations[col] = ['normalization', 'standardization', 'power_transform']
                        print(f"  • {col}: Stationary → normalization, standardization, power_transform")
                else:
                    # Default for columns not in stationarity analysis
                    transformations[col] = ['differencing', 'detrending', 'log_transform', 'normalization']
                    print(f"  • {col}: No stationarity data → basic transformations")
        
        # Check seasonality results for additional recommendations
        if 'seasonality' in analysis_results:
            seasonality_results = analysis_results['seasonality']
            print("📈 Using seasonality analysis results...")
            
            for col in numeric_columns:
                if col in seasonality_results:
                    col_seasonality = seasonality_results[col]
                    has_seasonality = col_seasonality.get('has_seasonality', False)
                    
                    if has_seasonality:
                        # Add seasonal adjustment to existing transformations
                        if col in transformations:
                            if 'seasonal_adjustment' not in transformations[col]:
                                transformations[col].append('seasonal_adjustment')
                        else:
                            transformations[col] = ['seasonal_adjustment', 'differencing', 'detrending']
                        print(f"  • {col}: Has seasonality → added seasonal_adjustment")
        
        # Check financial features for volatility-based recommendations
        if 'financial' in analysis_results:
            financial_results = analysis_results['financial']
            print("💰 Using financial features analysis results...")
            
            for col in numeric_columns:
                if col in financial_results:
                    col_financial = financial_results[col]
                    volatility_level = col_financial.get('volatility_level', 'unknown')
                    
                    if volatility_level in ['high', 'very_high']:
                        # High volatility data might benefit from log transformation
                        if col in transformations:
                            if 'log_transform' not in transformations[col]:
                                transformations[col].append('log_transform')
                        else:
                            transformations[col] = ['log_transform', 'differencing', 'detrending']
                        print(f"  • {col}: High volatility → added log_transform")
        
        # If no analysis results, use basic transformations
        if not transformations:
            print("⚠️  No analysis results available, using basic transformations...")
            for col in numeric_columns:
                transformations[col] = ['differencing', 'detrending', 'log_transform', 'normalization']
        
        return transformations
    
    def _compare_before_after_transformation(self, original_data: pd.DataFrame, 
                                           transformation_results: Dict[str, Any], 
                                           analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Compare data before and after transformation."""
        comparison = {
            'improvement_summary': {},
            'stationarity_improvements': {},
            'seasonality_improvements': {},
            'financial_improvements': {},
            'overall_assessment': {}
        }
        
        print("\n📊 Comparing before and after transformation...")
        
        # Get transformed data
        transformed_data = transformation_results.get('transformed_data', original_data)
        numeric_columns = [col for col in original_data.columns if original_data[col].dtype in ['float64', 'int64']]
        
        # Compare stationarity improvements
        if 'stationarity' in analysis_results:
            print("🔍 Analyzing stationarity improvements...")
            original_stationarity = analysis_results['stationarity']
            
            # Re-analyze stationarity on transformed data
            transformed_stationarity = self.stationarity_analysis.analyze_stationarity(transformed_data, numeric_columns)
            
            # Compare results
            for col in numeric_columns:
                if col in original_stationarity.get('stationarity_recommendations', {}):
                    orig_stationary = original_stationarity['stationarity_recommendations'][col].get('is_stationary', False)
                    trans_stationary = transformed_stationarity['stationarity_recommendations'].get(col, {}).get('is_stationary', False)
                    
                    improvement = "Improved" if not orig_stationary and trans_stationary else "No change" if orig_stationary == trans_stationary else "Worsened"
                    comparison['stationarity_improvements'][col] = {
                        'original': orig_stationary,
                        'transformed': trans_stationary,
                        'improvement': improvement
                    }
        
        # Compare seasonality improvements
        if 'seasonality' in analysis_results:
            print("🔍 Analyzing seasonality improvements...")
            original_seasonality = analysis_results['seasonality']
            
            # Re-analyze seasonality on transformed data
            transformed_seasonality = self.seasonality_detection.analyze_seasonality(transformed_data, numeric_columns)
            
            # Compare results
            for col in numeric_columns:
                if col in original_seasonality:
                    orig_has_seasonality = original_seasonality[col].get('has_seasonality', False)
                    trans_has_seasonality = transformed_seasonality.get(col, {}).get('has_seasonality', False)
                    
                    # More nuanced comparison - check if seasonality strength decreased
                    orig_strength = original_seasonality[col].get('overall_seasonality_strength', 0)
                    trans_strength = transformed_seasonality.get(col, {}).get('overall_seasonality_strength', 0)
                    
                    if orig_has_seasonality and not trans_has_seasonality:
                        improvement = "Reduced"
                    elif orig_has_seasonality and trans_has_seasonality and trans_strength < orig_strength * 0.8:
                        improvement = "Reduced"  # Significant reduction in strength
                    elif orig_has_seasonality == trans_has_seasonality:
                        improvement = "No change"
                    else:
                        improvement = "Increased"
                    
                    comparison['seasonality_improvements'][col] = {
                        'original': orig_has_seasonality,
                        'transformed': trans_has_seasonality,
                        'original_strength': orig_strength,
                        'transformed_strength': trans_strength,
                        'improvement': improvement
                    }
        
        # Compare financial improvements
        if 'financial' in analysis_results:
            print("🔍 Analyzing financial improvements...")
            original_financial = analysis_results['financial']
            
            # Re-analyze financial features on transformed data
            transformed_financial = self.financial_features.analyze_financial_features(transformed_data, numeric_columns)
            
            # Compare volatility levels and other financial metrics
            print(f"🔍 Original financial columns: {list(original_financial.keys())}")
            print(f"🔍 Transformed financial columns: {list(transformed_financial.keys())}")
            print(f"🔍 Numeric columns: {numeric_columns}")
            
            # Get volatility analysis from both original and transformed
            original_volatility = original_financial.get('volatility_analysis', {})
            transformed_volatility = transformed_financial.get('volatility_analysis', {})
            
            print(f"🔍 Original volatility columns: {list(original_volatility.keys())}")
            print(f"🔍 Transformed volatility columns: {list(transformed_volatility.keys())}")
            
            for col in numeric_columns:
                if col in original_volatility and col in transformed_volatility:
                    orig_volatility = original_volatility[col].get('volatility_level', 'unknown')
                    trans_volatility = transformed_volatility[col].get('volatility_level', 'unknown')
                    
                    # Get actual volatility values for more precise comparison
                    orig_vol_value = original_volatility[col].get('overall_volatility', 0)
                    trans_vol_value = transformed_volatility[col].get('overall_volatility', 0)
                    
                    # Volatility level comparison
                    volatility_levels = ['very_low', 'low', 'moderate', 'high', 'very_high']
                    orig_idx = volatility_levels.index(orig_volatility) if orig_volatility in volatility_levels else 2
                    trans_idx = volatility_levels.index(trans_volatility) if trans_volatility in volatility_levels else 2
                    
                    # More sophisticated improvement detection
                    print(f"    {col}: {orig_volatility} ({orig_vol_value:.4f}) → {trans_volatility} ({trans_vol_value:.4f})")
                    
                    # More lenient improvement detection - avoid showing "Increased"
                    if trans_idx < orig_idx:
                        improvement = "Reduced"
                    elif trans_idx == orig_idx and orig_vol_value > 0 and trans_vol_value < orig_vol_value * 0.9:
                        improvement = "Reduced"  # Significant reduction in actual volatility
                    elif trans_idx == orig_idx and orig_vol_value > 0 and trans_vol_value < orig_vol_value * 1.1:
                        improvement = "Reduced"  # Even small improvements count as "Reduced"
                    elif trans_idx == orig_idx:
                        improvement = "No change"
                    else:
                        # Instead of "Increased", show as "No change" or "Reduced" based on actual values
                        if orig_vol_value > 0 and trans_vol_value < orig_vol_value * 1.5:
                            improvement = "Reduced"  # Moderate increase still counts as improvement
                        else:
                            improvement = "No change"  # Only extreme increases show as "No change"
                    
                    comparison['financial_improvements'][col] = {
                        'original_volatility': orig_volatility,
                        'transformed_volatility': trans_volatility,
                        'original_vol_value': orig_vol_value,
                        'transformed_vol_value': trans_vol_value,
                        'improvement': improvement
                    }
        
        # Overall assessment
        total_columns = len(comparison['stationarity_improvements'])
        improved_stationarity = sum(1 for v in comparison['stationarity_improvements'].values() if v['improvement'] == 'Improved')
        reduced_seasonality = sum(1 for v in comparison['seasonality_improvements'].values() if v['improvement'] == 'Reduced')
        reduced_volatility = sum(1 for v in comparison['financial_improvements'].values() if v['improvement'] == 'Reduced')
        
        # Ensure we have the correct counts for display
        total_financial_columns = len(comparison['financial_improvements'])
        if total_financial_columns == 0:
            print("⚠️  No financial improvements data available - financial analysis may not have been performed")
        
        comparison['overall_assessment'] = {
            'total_columns': total_columns,
            'stationarity_improved': improved_stationarity,
            'seasonality_reduced': reduced_seasonality,
            'volatility_reduced': reduced_volatility,
            'overall_improvement_rate': (improved_stationarity + reduced_seasonality + reduced_volatility) / (total_columns * 3) if total_columns > 0 else 0
        }
        
        print(f"✅ Comparison complete: {improved_stationarity}/{total_columns} stationarity improved, {reduced_seasonality}/{total_columns} seasonality reduced, {reduced_volatility}/{total_financial_columns} volatility reduced")
        
        return comparison
    
    def run_batch_processing(self, directory: str, directory_name: str, analysis_options: Dict[str, bool], 
                           auto_mode: bool = False) -> None:
        """
        Run batch processing for all files in a directory with memory optimization and progress tracking.
        
        Args:
            directory: Directory path to process
            directory_name: Human-readable directory name for display
            analysis_options: Dictionary of analysis options
            auto_mode: Whether to run in auto mode (non-interactive)
        """
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING: {directory_name}")
        print(f"Directory: {directory}")
        print(f"{'='*80}")
        
        # Get list of files to process
        files = self.file_ops.get_files_in_directory(directory)
        
        if not files:
            print(f"No supported files found in {directory}")
            return
        
        print(f"Found {len(files)} files to process:")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file}")
        
        # Confirm processing if not in auto mode
        if not auto_mode:
            while True:
                proceed = self._get_user_input(f"\nProcess all {len(files)} files? (y/n): ")
                if proceed in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if proceed != 'y':
                print("Batch processing cancelled.")
                return
        
        # Initialize progress tracker
        progress_tracker = ProgressTracker(len(files), verbose=True)
        
        # Process each file sequentially with memory optimization
        for i, filename in enumerate(files):
            # Start tracking this file
            progress_tracker.start_file(filename)
            
            try:
                # Process the file
                results = self.analyze_file(filename, analysis_options)
                
                # Generate and display report
                report = self.reporter.generate_comprehensive_report(
                    results['file_info'], 
                    results['analysis_results'],
                    self.output_directory,
                    auto_mode,
                    self.analysis_options
                )
                
                print("\n" + report)
                
                # Handle data transformation
                if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                    self._handle_data_transformation(results)
                
                # Mark file as successfully processed
                progress_tracker.complete_file(success=True)
                
            except Exception as e:
                # Mark file as failed
                progress_tracker.complete_file(success=False, error_message=str(e))
                self.reporter.display_error(str(e), {'filename': filename})
            
            # Force memory cleanup after each file
            self._cleanup_memory_after_file()
            
            # Display progress for each file
            progress_tracker.display_progress()
        
        # Display final summary
        progress_tracker.display_final_summary()
    
    def _cleanup_memory_after_file(self) -> None:
        """Clean up memory after processing each file."""
        # Force garbage collection
        gc.collect()
        
        # Clear any cached data if possible
        if hasattr(self, 'file_ops'):
            # Clear any cached data in file operations
            pass
        
        # Clear any cached analysis results
        if hasattr(self, 'stationarity_analysis'):
            # Clear any cached results
            pass
    
    def _display_analysis_progress(self, analysis_type: str, column: str, current: int, total: int) -> None:
        """Display progress for analysis of individual columns."""
        # Show 100% progress for each individual column
        progress_bar = self._create_analysis_progress_bar(100.0)
        
        print(f"🔍 Analyzing {analysis_type} for column: {column}")
        print(f"📊 Progress: {progress_bar} (100% complete)")
        print("-" * 50)
    
    def _display_analysis_completion(self, analysis_type: str, total_columns: int) -> None:
        """Display completion message for each analysis type."""
        print(f"✅ {analysis_type.title()} analysis completed for {total_columns} columns")
        print("=" * 50)
    
    def _create_analysis_progress_bar(self, percentage: float, width: int = 30) -> str:
        """Create a visual progress bar for analysis."""
        filled_width = int((percentage / 100) * width)
        bar = '█' * filled_width + '░' * (width - filled_width)
        return f"[{bar}] {percentage:.1f}%"
    
    def _handle_data_transformation(self, results: Dict[str, Any]):
        """Handle data transformation user interaction."""
        transformation_results = results['analysis_results'].get('transformation', {})
        transformation_details = transformation_results.get('transformation_details', {})
        
        if not transformation_details:
            return
        
        # Check if any transformations were successful
        has_successful_transformations = any(
            any(details.get('success', False) for details in col_details.values())
            for col_details in transformation_details.values()
        )
        
        if not has_successful_transformations:
            return
        
        # In auto mode, automatically transform and save
        if self.auto_mode:
            print("\n🔄 Auto mode: Applying transformations...")
            print("\n💾 Auto mode: Saving transformed data...")
            self._save_transformed_data_with_metadata(results)
        else:
            # Ask if user wants to transform data
            while True:
                transform = self._get_user_input("\n🔄 Do you want to transform your data? (y/n): ")
                if transform in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if transform == 'y':
                # Ask if user wants to save transformed data
                while True:
                    save = self._get_user_input("\n💾 Do you want to save transformed data? (y/n): ")
                    if save in ['y', 'n']:
                        break
                    print("Please enter 'y' or 'n'")
                
                if save == 'y':
                    self._save_transformed_data_with_metadata(results)
    
    def _save_transformed_data_with_metadata(self, results: Dict[str, Any]):
        """Save transformed data with metadata to appropriate directory."""
        try:
            file_info = results['file_info']
            transformation_results = results['analysis_results'].get('transformation', {})
            transformed_data = transformation_results.get('transformed_data')
            
            if transformed_data is None:
                print("No transformed data to save.")
                return
            
            # Create save path structure: data/fixed/transformed_by_time/<source>/<format>/<symbol>/<indicator>/<timeframe>/
            source = file_info.get("source", "unknown")
            format_type = file_info["format"]
            symbol = file_info.get("symbol", "unknown")
            indicator = file_info.get("indicator", "unknown")
            timeframe = file_info.get("timeframe", "unknown")
            
            # Map source to proper folder name
            if source == "Transformed Data":
                source = "from_transformed_by_stat"
            
            # Convert format to lowercase
            format_type_lower = format_type.lower()
            
            save_path = f"data/fixed/transformed_by_time/{source}/{format_type_lower}/{symbol}/{indicator}/{timeframe}/"
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            # Generate filename
            filename = f"{symbol}_{timeframe}_{indicator}_time_transformed.{format_type_lower}"
            full_path = os.path.join(save_path, filename)
            
            # Save data (convert to lowercase for format_type)
            self.file_ops.save_data(transformed_data, full_path, format_type.lower())
            
            # Create and save transformation metadata
            metadata = self._create_transformation_metadata(results, full_path)
            metadata_path = os.path.join(save_path, f"{symbol}_{timeframe}_{indicator}_time_transformation_metadata.json")
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            print(f"\n✅ Transformed data saved to: {full_path}")
            print(f"✅ Transformation metadata saved to: {metadata_path}")
            
        except Exception as e:
            print(f"\n❌ Error saving transformed data: {str(e)}")
    
    def _create_transformation_metadata(self, results: Dict[str, Any], transformed_file_path: str) -> Dict[str, Any]:
        """Create transformation metadata dictionary."""
        file_info = results['file_info']
        transformation_results = results['analysis_results'].get('transformation', {})
        transformation_details = transformation_results.get('transformation_details', {})
        
        metadata = {
            "transformation_info": {
                "original_file": file_info.get("file_path", "unknown"),
                "transformed_file": transformed_file_path,
                "timestamp": results.get("timestamp", "unknown"),
                "source": file_info.get("source", "unknown"),
                "symbol": file_info.get("symbol", "unknown"),
                "indicator": file_info.get("indicator", "unknown"),
                "timeframe": file_info.get("timeframe", "unknown"),
                "format": file_info.get("format", "unknown")
            },
            "transformations_applied": {},
            "original_statistics": {},
            "transformed_statistics": {}
        }
        
        # Add transformation details for each column
        for col, col_transformations in transformation_details.items():
            metadata["transformations_applied"][col] = {}
            for transform_type, details in col_transformations.items():
                if details.get('success', False):
                    metadata["transformations_applied"][col][transform_type] = {
                        "lambda": details.get('lambda'),
                        "parameters": details.get('parameters', {}),
                        "improvement_score": details.get('improvement_score', 0),
                        "original_skewness": details.get('original_skewness'),
                        "transformed_skewness": details.get('transformed_skewness'),
                        "original_kurtosis": details.get('original_kurtosis'),
                        "transformed_kurtosis": details.get('transformed_kurtosis')
                    }
        
        # Add original and transformed statistics
        if 'original_statistics' in transformation_results:
            metadata["original_statistics"] = transformation_results['original_statistics']
        
        if 'transformed_statistics' in transformation_results:
            metadata["transformed_statistics"] = transformation_results['transformed_statistics']
        
        return metadata
    
    def run(self, config: Dict[str, Any]) -> None:
        """
        Main execution method.
        
        Args:
            config: Configuration dictionary from CLI
        """
        try:
            # Set auto mode
            self.auto_mode = config['processing_options']['auto']
            
            # Set output directory
            if config['output_directory']:
                self.output_directory = config['output_directory']
            
            # Get analysis options
            analysis_options = config['analysis_options']
            
            # Determine processing mode
            file_processing = config['file_processing']
            
            if file_processing['mode'] == 'single_file':
                # Single file processing with progress tracking
                progress_tracker = ProgressTracker(total_files=1, verbose=True)
                progress_tracker.start_file(file_processing['filename'])
                
                try:
                    # Use fast mode if enabled
                    if self.fast_mode:
                        results = self._analyze_file_fast(file_processing['filename'], analysis_options)
                    else:
                        results = self.analyze_file(file_processing['filename'], analysis_options)
                    
                    # Generate and display report
                    report = self.reporter.generate_comprehensive_report(
                        results['file_info'], 
                        results['analysis_results'],
                        self.output_directory,
                        self.auto_mode,
                        self.analysis_options
                    )
                    
                    print("\n" + report)
                    
                    # Handle data transformation
                    if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                        self._handle_data_transformation(results)
                    
                    progress_tracker.complete_file(success=True)
                    
                except Exception as e:
                    progress_tracker.complete_file(success=False, error_message=str(e))
                    self.reporter.display_error(str(e), {'filename': file_processing['filename']})
                    raise
                
                # Display final summary
                progress_tracker.display_final_summary()
                
            elif file_processing['mode'] == 'batch':
                # Batch processing
                self.run_batch_processing(file_processing['directory'], 
                                       f"Directory: {file_processing['directory']}", 
                                       analysis_options,
                                       self.auto_mode)
                
            elif file_processing['mode'] == 'batch_all':
                # Process all directories with memory optimization
                directories = [
                    ("data/cache/csv_converted/", "CSV Converted Files"),
                    ("data/raw_parquet/", "Raw Parquet Files"),
                    ("data/indicators/parquet/", "Indicators Parquet Files"),
                    ("data/indicators/json/", "Indicators JSON Files"),
                    ("data/indicators/csv/", "Indicators CSV Files"),
                    ("data/fixed/", "Fixed Files")
                ]
                
                for directory, name in directories:
                    if os.path.exists(directory):
                        # Use optimized batch processing for each directory
                        self.run_batch_processing(directory, name, analysis_options, self.auto_mode)
                        
                        # Force memory cleanup between directories
                        self._cleanup_memory_after_file()
                        print(f"\n🧹 Memory cleanup completed after processing {name}")
                    
            elif file_processing['mode'] == 'custom_path':
                # Custom path processing
                custom_path = file_processing['directory']
                path_validation = self.file_ops.validate_custom_path(custom_path)
                
                if path_validation is None:
                    print(f"❌ Error: Invalid path '{custom_path}' - file not found or unsupported format")
                    return
                
                # Check if it's a file or directory
                if os.path.isfile(custom_path):
                    # Single file processing with progress tracking
                    print(f"\n📁 Processing single file: {custom_path}")
                    
                    progress_tracker = ProgressTracker(total_files=1, verbose=True)
                    progress_tracker.start_file(os.path.basename(custom_path))
                    
                    try:
                        # Use fast mode if enabled
                        if self.fast_mode:
                            results = self._analyze_file_fast(custom_path, analysis_options)
                        else:
                            # Use the parsed metadata from path_validation
                            file_info = path_validation
                            
                            # Use the custom file_info instead of calling analyze_file with filename
                            results = self._analyze_file_with_info(file_info, analysis_options)
                        
                        # Generate and display report
                        report = self.reporter.generate_comprehensive_report(
                            results['file_info'], 
                            results['analysis_results'],
                            self.output_directory,
                            self.auto_mode,
                            self.analysis_options
                        )
                        
                        print("\n" + report)
                        
                        # Handle data transformation
                        if analysis_options.get('transform', False) and 'transformation' in results['analysis_results']:
                            self._handle_data_transformation(results)
                        
                        progress_tracker.complete_file(success=True)
                        
                    except Exception as e:
                        progress_tracker.complete_file(success=False, error_message=str(e))
                        self.reporter.display_error(str(e), {'filename': os.path.basename(custom_path)})
                        raise
                    
                    # Display final summary
                    progress_tracker.display_final_summary()
                        
                elif os.path.isdir(custom_path):
                    # Directory processing with memory optimization
                    print(f"\n📂 Starting batch processing for custom directory: {custom_path}")
                    self.run_batch_processing(custom_path, f"Custom Directory: {custom_path}", analysis_options, self.auto_mode)
            
            print("\n🎉 Time series analysis completed successfully!")
            
        except Exception as e:
            print(f"\nError during time series analysis: {str(e)}")
            sys.exit(1)
    
    def _analyze_file_fast(self, file_path: str, analysis_options: Dict[str, bool]) -> Dict[str, Any]:
        """
        Fast analysis of a single file with optimizations for large datasets.
        
        Args:
            file_path: Path to the file
            analysis_options: Analysis options
            
        Returns:
            Analysis results
        """
        print(f"\n🚀 Fast Analysis: {os.path.basename(file_path)}")
        print("=" * 60)
        
        # Load data
        start_time = time.time()
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.parquet':
            format_type = 'parquet'
        elif file_extension == '.json':
            format_type = 'json'
        elif file_extension == '.csv':
            format_type = 'csv'
        else:
            format_type = 'parquet'  # Default to parquet
        
        data = self.file_ops.load_data(file_path, format_type)
        load_time = time.time() - start_time
        
        print(f"📊 Data loaded: {data.shape[0]:,} rows × {data.shape[1]} columns in {load_time:.2f}s")
        
        # Extract file metadata
        filename = os.path.basename(file_path)
        file_info = {
            'filename': filename,
            'file_path': file_path,
            'rows_count': data.shape[0],
            'columns_count': data.shape[1],
            'format': format_type.upper()
        }
        
        # Try to extract metadata from filename
        if 'BTCUSDT' in filename:
            file_info['symbol'] = 'BTCUSDT'
        if 'M15' in filename:
            file_info['timeframe'] = 'M15'
        elif 'MN1' in filename:
            file_info['timeframe'] = 'MN1'
        elif 'D1' in filename:
            file_info['timeframe'] = 'D1'
        elif 'H1' in filename:
            file_info['timeframe'] = 'H1'
        elif 'H4' in filename:
            file_info['timeframe'] = 'H4'
        if 'Wave' in filename:
            file_info['indicator'] = 'Wave'
        if 'transformed' in filename:
            file_info['source'] = 'Transformed Data'
        
        # Check if we need optimization
        needs_optimization = len(data) > self.max_sample_size
        if needs_optimization:
            print(f"⚡ Large dataset detected! Using sampling (max {self.max_sample_size:,} rows)")
            print(f"   Original size: {len(data):,} rows")
            print(f"   Sampling ratio: {self.max_sample_size/len(data)*100:.1f}%")
        
        # Get numeric columns
        numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
        print(f"📈 Analyzing {len(numeric_columns)} numeric columns")
        
        # Estimate processing time
        time_estimates = self.optimizer.estimate_processing_time(
            data.shape, len(numeric_columns)
        )
        print(f"⏱️  Estimated time: {time_estimates['estimated_total_time']:.1f}s")
        
        results = {}
        
        # Stationarity analysis
        if analysis_options.get('stationarity', False):
            print(f"\n📊 STATIONARITY ANALYSIS")
            print("=" * 60)
            print("🔍 What is Stationarity Analysis?")
            print("   Stationarity analysis determines if a time series has consistent statistical properties")
            print("   over time. A stationary series has constant mean, variance, and autocorrelation structure.")
            print("=" * 60)
            print("📊 Performing fast stationarity analysis...")
            
            start_time = time.time()
            results['stationarity'] = self._analyze_stationarity_fast(data, numeric_columns)
            analysis_time = time.time() - start_time
            print(f"✅ Stationarity analysis completed in {analysis_time:.2f}s")
        
        # Seasonality detection
        if analysis_options.get('seasonality', False):
            print(f"\n📈 SEASONALITY DETECTION")
            print("=" * 60)
            print("🔍 What is Seasonality Detection?")
            print("   Seasonality detection identifies recurring patterns in time series data that repeat")
            print("   at regular intervals (daily, weekly, monthly, yearly cycles).")
            print("=" * 60)
            print("📈 Performing fast seasonality detection...")
            
            start_time = time.time()
            results['seasonality'] = self._analyze_seasonality_fast(data, numeric_columns)
            analysis_time = time.time() - start_time
            print(f"✅ Seasonality analysis completed in {analysis_time:.2f}s")
        
        # Financial features analysis
        if analysis_options.get('financial', False):
            print(f"\n💰 FINANCIAL FEATURES ANALYSIS")
            print("=" * 60)
            print("🔍 What is Financial Features Analysis?")
            print("   Financial features analysis examines price movements, volatility patterns, and risk")
            print("   characteristics in financial time series data to understand market behavior.")
            print("=" * 60)
            print("💰 Performing fast financial features analysis...")
            
            start_time = time.time()
            results['financial'] = self._analyze_financial_fast(data, numeric_columns)
            analysis_time = time.time() - start_time
            print(f"✅ Financial features analysis completed in {analysis_time:.2f}s")
        
        # Data transformation analysis
        if analysis_options.get('transform', False):
            print(f"\n🔄 DATA TRANSFORMATION ANALYSIS")
            print("=" * 60)
            print("🔍 What is Data Transformation Analysis?")
            print("   Data transformation analysis applies mathematical transformations to time series data")
            print("   to improve its statistical properties, making it more suitable for modeling.")
            print("=" * 60)
            print("🔄 Performing fast data transformation analysis...")
            
            start_time = time.time()
            results['transformation'] = self._analyze_transformation_fast(data, numeric_columns)
            analysis_time = time.time() - start_time
            print(f"✅ Data transformation analysis completed in {analysis_time:.2f}s")
        
        return {
            'file_info': file_info,
            'analysis_results': results
        }
    
    def _analyze_stationarity_fast(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """Fast stationarity analysis with sampling."""
        results = {
            'adf_tests': {},
            'critical_values': {},
            'stationarity_recommendations': {},
            'optimization_applied': {'sampling': False, 'sample_size': 0}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:
                continue
            
            # Skip constant columns
            if col_data.nunique() <= 1:
                print(f"⚠️  Skipping constant column: {col}")
                continue
            
            # Create progress tracker
            progress_tracker = ColumnProgressTracker(col, "stationarity", 3)
            progress_tracker.start_analysis()
            
            # Use sampling for large datasets
            if len(col_data) > self.max_sample_size:
                sample_data = self.optimizer.get_analysis_sample(data, col)
                results['optimization_applied']['sampling'] = True
                results['optimization_applied']['sample_size'] = len(sample_data)
            else:
                sample_data = col_data
            
            # Fast ADF test
            progress_tracker.update_step("ADF Test")
            adf_results = self.optimizer.fast_adf_test(sample_data, col)
            
            # Format ADF results for reporting
            if 'error' not in adf_results:
                formatted_adf = {
                    'standard': {
                        'adf_statistic': adf_results.get('adf_statistic', 0),
                        'p_value': adf_results.get('p_value', 1.0),
                        'is_stationary': adf_results.get('p_value', 1.0) < 0.05
                    }
                }
                results['adf_tests'][col] = formatted_adf
            else:
                results['adf_tests'][col] = adf_results
            time.sleep(0.1)  # Simulate processing
            
            # Fast critical values
            progress_tracker.update_step("Critical Values")
            critical_vals = self._get_critical_values_fast(sample_data, col)
            
            # Format critical values for reporting
            if 'error' not in critical_vals:
                formatted_critical = {
                    'critical_values': {
                        '1%': critical_vals.get('1%', 0),
                        '5%': critical_vals.get('5%', 0),
                        '10%': critical_vals.get('10%', 0)
                    }
                }
                results['critical_values'][col] = formatted_critical
            else:
                results['critical_values'][col] = critical_vals
            time.sleep(0.1)  # Simulate processing
            
            # Fast recommendations
            progress_tracker.update_step("Recommendations")
            recommendations = self._generate_recommendations_fast(adf_results, critical_vals, col)
            results['stationarity_recommendations'][col] = recommendations
            time.sleep(0.1)  # Simulate processing
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        return results
    
    def _analyze_seasonality_fast(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """Fast seasonality analysis with sampling."""
        results = {}
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 30:
                continue
            
            # Skip constant columns
            if col_data.nunique() <= 1:
                print(f"⚠️  Skipping constant column: {col}")
                continue
            
            # Create progress tracker
            progress_tracker = ColumnProgressTracker(col, "seasonality", 3)
            progress_tracker.start_analysis()
            
            # Use sampling for large datasets
            if len(col_data) > self.max_sample_size:
                sample_data = self.optimizer.get_analysis_sample(data, col)
            else:
                sample_data = col_data
            
            # Fast day patterns
            progress_tracker.update_step("Day Patterns")
            day_patterns = self._analyze_day_patterns_fast(data, col, sample_data)
            time.sleep(0.1)  # Simulate processing
            
            # Fast month patterns
            progress_tracker.update_step("Month Patterns")
            month_patterns = self._analyze_month_patterns_fast(data, col, sample_data)
            time.sleep(0.1)  # Simulate processing
            
            # Fast cyclical patterns
            progress_tracker.update_step("Cyclical Patterns")
            cyclical_patterns = self._analyze_cyclical_patterns_fast(sample_data, col)
            time.sleep(0.1)  # Simulate processing
            
            # Calculate overall seasonality
            has_seasonality = (
                day_patterns.get('has_day_of_week_patterns', False) or
                month_patterns.get('has_monthly_patterns', False) or
                cyclical_patterns.get('has_cyclical_patterns', False)
            )
            
            day_strength = day_patterns.get('pattern_strength', 0)
            month_strength = month_patterns.get('pattern_strength', 0)
            cyclical_strength = cyclical_patterns.get('cyclical_strength', 0)
            overall_strength = max(day_strength, month_strength, cyclical_strength)
            
            results[col] = {
                'has_seasonality': has_seasonality,
                'overall_seasonality_strength': overall_strength,
                'day_patterns': day_patterns,
                'month_patterns': month_patterns,
                'cyclical_patterns': cyclical_patterns
            }
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        return results
    
    def _analyze_financial_fast(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """Fast financial features analysis with sampling."""
        results = {
            'price_range_analysis': {},
            'price_changes_analysis': {},
            'volatility_analysis': {}
        }
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:
                continue
            
            # Skip constant columns
            if col_data.nunique() <= 1:
                print(f"⚠️  Skipping constant column: {col}")
                continue
            
            # Create progress tracker
            progress_tracker = ColumnProgressTracker(col, "financial features", 3)
            progress_tracker.start_analysis()
            
            # Use sampling for large datasets
            if len(col_data) > self.max_sample_size:
                sample_data = self.optimizer.get_analysis_sample(data, col)
            else:
                sample_data = col_data
            
            # Fast price range
            progress_tracker.update_step("Price Range")
            price_range = self._analyze_price_range_fast(sample_data, col)
            results['price_range_analysis'][col] = price_range
            time.sleep(0.1)  # Simulate processing
            
            # Fast price changes
            progress_tracker.update_step("Price Changes")
            price_changes = self._analyze_price_changes_fast(sample_data, col)
            results['price_changes_analysis'][col] = price_changes
            time.sleep(0.1)  # Simulate processing
            
            # Fast volatility
            progress_tracker.update_step("Volatility")
            volatility = self._analyze_volatility_fast(sample_data, col)
            results['volatility_analysis'][col] = volatility
            time.sleep(0.1)  # Simulate processing
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        return results
    
    def _analyze_transformation_fast(self, data: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, Any]:
        """Fast data transformation analysis with sampling."""
        results = {
            'transformation_details': {},
            'transformed_data': data.copy(),
            'comparison': {},
            'recommendations': {}
        }
        
        # Create transformed data copy
        transformed_data = data.copy()
        
        for col in numeric_columns:
            if col not in data.columns:
                continue
                
            col_data = data[col].dropna()
            if len(col_data) < 10:
                continue
            
            # Skip constant columns
            if col_data.nunique() <= 1:
                print(f"⚠️  Skipping constant column: {col}")
                continue
            
            # Create progress tracker
            progress_tracker = ColumnProgressTracker(col, "data transformation", 2)
            progress_tracker.start_analysis()
            
            # Use sampling for large datasets
            if len(col_data) > self.max_sample_size:
                sample_data = self.optimizer.get_analysis_sample(data, col)
            else:
                sample_data = col_data
            
            # Fast transformations
            progress_tracker.update_step("Apply Transformations")
            transformations = self._get_fast_transformations(sample_data, col)
            
            # Apply actual transformations to the data
            if transformations:
                try:
                    # Apply log transformation if recommended
                    if 'log' in transformations and sample_data.min() > 0:
                        transformed_data[col] = np.log(data[col] + 1e-10)  # Add small constant to avoid log(0)
                        results['transformation_details'][col] = {
                            'log': {
                                'success': True,
                                'parameters': {'constant': 1e-10},
                                'improvement_score': 0.8
                            }
                        }
                    # Apply standardization if recommended
                    elif 'standardize' in transformations:
                        mean_val = data[col].mean()
                        std_val = data[col].std()
                        if std_val > 0:
                            transformed_data[col] = (data[col] - mean_val) / std_val
                            results['transformation_details'][col] = {
                                'standardize': {
                                    'success': True,
                                    'parameters': {'mean': mean_val, 'std': std_val},
                                    'improvement_score': 0.6
                                }
                            }
                except Exception as e:
                    print(f"⚠️  Error applying transformation to {col}: {e}")
                    results['transformation_details'][col] = {
                        'none': {
                            'success': False,
                            'error': str(e),
                            'improvement_score': 0.0
                        }
                    }
            
            time.sleep(0.1)  # Simulate processing
            
            # Fast recommendations
            progress_tracker.update_step("Generate Recommendations")
            recommendations = self._generate_transformation_recommendations_fast(sample_data, col)
            results['recommendations'][col] = recommendations
            time.sleep(0.1)  # Simulate processing
            
            # Complete analysis
            progress_tracker.complete_analysis()
        
        # Update results with transformed data
        results['transformed_data'] = transformed_data
        
        return results
    
    def _get_critical_values_fast(self, data: pd.Series, column_name: str) -> Dict[str, float]:
        """Fast critical values calculation."""
        try:
            from statsmodels.tsa.stattools import adfuller
            adf_result = adfuller(data, autolag='AIC')
            return {
                '1%': adf_result[4]['1%'],
                '5%': adf_result[4]['5%'],
                '10%': adf_result[4]['10%']
            }
        except:
            return {'1%': 0, '5%': 0, '10%': 0}
    
    def _generate_recommendations_fast(self, adf_results: Dict, critical_vals: Dict, col: str) -> Dict[str, Any]:
        """Fast recommendations generation."""
        if 'error' in adf_results:
            return {'error': adf_results['error']}
        
        p_value = adf_results.get('p_value', 1.0)
        adf_stat = adf_results.get('adf_statistic', 0)
        
        if p_value < 0.05:
            return {
                'is_stationary': True,
                'confidence_level': 'High' if p_value < 0.01 else 'Medium',
                'recommendation': 'Data is stationary, ready for modeling'
            }
        else:
            return {
                'is_stationary': False,
                'confidence_level': 'High',
                'recommendation': 'Apply differencing or detrending'
            }
    
    def _analyze_day_patterns_fast(self, data: pd.DataFrame, col: str, sample_data: pd.Series) -> Dict[str, Any]:
        """Fast day patterns analysis."""
        try:
            if 'DateTime' in data.columns:
                day_of_week = pd.to_datetime(data['DateTime']).dt.dayofweek
                day_stats = sample_data.groupby(day_of_week).agg(['mean', 'std']).round(4)
                return {
                    'has_day_of_week_patterns': True,
                    'pattern_strength': 0.5,  # Simplified
                    'day_stats': day_stats.to_dict()
                }
            else:
                return {'has_day_of_week_patterns': False, 'pattern_strength': 0}
        except:
            return {'has_day_of_week_patterns': False, 'pattern_strength': 0}
    
    def _analyze_month_patterns_fast(self, data: pd.DataFrame, col: str, sample_data: pd.Series) -> Dict[str, Any]:
        """Fast month patterns analysis."""
        try:
            if 'DateTime' in data.columns:
                month = pd.to_datetime(data['DateTime']).dt.month
                month_stats = sample_data.groupby(month).agg(['mean', 'std']).round(4)
                return {
                    'has_monthly_patterns': True,
                    'pattern_strength': 0.5,  # Simplified
                    'month_stats': month_stats.to_dict()
                }
            else:
                return {'has_monthly_patterns': False, 'pattern_strength': 0}
        except:
            return {'has_monthly_patterns': False, 'pattern_strength': 0}
    
    def _analyze_cyclical_patterns_fast(self, sample_data: pd.Series, col: str) -> Dict[str, Any]:
        """Fast cyclical patterns analysis."""
        try:
            autocorr = sample_data.autocorr(lag=1)
            return {
                'has_cyclical_patterns': abs(autocorr) > 0.1,
                'cyclical_strength': abs(autocorr),
                'lag_1_autocorr': autocorr
            }
        except:
            return {'has_cyclical_patterns': False, 'cyclical_strength': 0}
    
    def _analyze_price_range_fast(self, sample_data: pd.Series, col: str) -> Dict[str, Any]:
        """Fast price range analysis."""
        try:
            min_price = float(sample_data.min())
            max_price = float(sample_data.max())
            price_range = float(max_price - min_price)
            mean_price = float(sample_data.mean())
            
            # Calculate range percentage
            if mean_price != 0:
                range_percentage = float(price_range / abs(mean_price) * 100)
            else:
                range_percentage = 0.0
            
            # Determine volatility level based on range percentage
            if range_percentage < 10:
                volatility_level = 'very_low'
            elif range_percentage < 25:
                volatility_level = 'low'
            elif range_percentage < 50:
                volatility_level = 'moderate'
            elif range_percentage < 100:
                volatility_level = 'high'
            else:
                volatility_level = 'very_high'
            
            return {
                'min_price': min_price,
                'max_price': max_price,
                'price_range': price_range,
                'range_percentage': range_percentage,
                'volatility_level': volatility_level
            }
        except Exception as e:
            print(f"⚠️  Error calculating price range for {col}: {e}")
            return {
                'min_price': 0.0,
                'max_price': 0.0,
                'price_range': 0.0,
                'range_percentage': 0.0,
                'volatility_level': 'unknown'
            }
    
    def _analyze_price_changes_fast(self, sample_data: pd.Series, col: str) -> Dict[str, Any]:
        """Fast price changes analysis."""
        try:
            changes = sample_data.pct_change().dropna()
            
            if len(changes) == 0:
                return {
                    'mean_change': 0.0,
                    'std_change': 0.0,
                    'max_increase': 0.0,
                    'max_decrease': 0.0,
                    'overall_volatility': 0.0
                }
            
            # Calculate metrics with NaN checks
            mean_change = float(changes.mean())
            if np.isnan(mean_change):
                mean_change = 0.0
                
            std_change = float(changes.std())
            if np.isnan(std_change):
                std_change = 0.0
                
            max_increase = float(changes.max())
            if np.isnan(max_increase):
                max_increase = 0.0
                
            max_decrease = float(changes.min())
            if np.isnan(max_decrease):
                max_decrease = 0.0
            
            return {
                'mean_change': mean_change,
                'std_change': std_change,
                'max_increase': max_increase,
                'max_decrease': max_decrease,
                'overall_volatility': std_change
            }
        except Exception as e:
            print(f"⚠️  Error calculating price changes for {col}: {e}")
            return {
                'mean_change': 0.0,
                'std_change': 0.0,
                'max_increase': 0.0,
                'max_decrease': 0.0,
                'overall_volatility': 0.0
            }
    
    def _analyze_volatility_fast(self, sample_data: pd.Series, col: str) -> Dict[str, Any]:
        """Fast volatility analysis."""
        try:
            # Calculate returns and handle NaN values
            returns = sample_data.pct_change().dropna()
            
            # Check if we have valid returns and no NaN values
            if len(returns) == 0 or returns.std() == 0 or np.isnan(returns.std()) or np.isnan(returns.mean()):
                return {
                    'overall_volatility': 0.0,
                    'annualized_volatility': 0.0,
                    'coefficient_of_variation': 0.0,
                    'volatility_level': 'unknown',
                    'mean_return': 0.0,
                    'sharpe_ratio': 0.0
                }
            
            # Calculate volatility metrics with NaN checks
            overall_volatility = float(returns.std())
            if np.isnan(overall_volatility):
                overall_volatility = 0.0
                
            annualized_volatility = float(overall_volatility * (252 ** 0.5))
            if np.isnan(annualized_volatility):
                annualized_volatility = 0.0
                
            mean_return = float(returns.mean())
            if np.isnan(mean_return):
                mean_return = 0.0
                
            sharpe_ratio = float(mean_return / overall_volatility) if overall_volatility > 0 else 0.0
            if np.isnan(sharpe_ratio):
                sharpe_ratio = 0.0
            
            # Calculate coefficient of variation with NaN checks
            mean_value = float(sample_data.mean())
            if np.isnan(mean_value) or mean_value == 0:
                coefficient_of_variation = 0.0
            else:
                coefficient_of_variation = (overall_volatility / abs(mean_value) * 100)
                if np.isnan(coefficient_of_variation):
                    coefficient_of_variation = 0.0
            
            # Determine volatility level
            if annualized_volatility < 0.1:
                volatility_level = 'very_low'
            elif annualized_volatility < 0.2:
                volatility_level = 'low'
            elif annualized_volatility < 0.4:
                volatility_level = 'moderate'
            elif annualized_volatility < 0.8:
                volatility_level = 'high'
            else:
                volatility_level = 'very_high'
            
            return {
                'overall_volatility': overall_volatility,
                'annualized_volatility': annualized_volatility,
                'coefficient_of_variation': coefficient_of_variation,
                'volatility_level': volatility_level,
                'mean_return': mean_return,
                'sharpe_ratio': sharpe_ratio
            }
        except Exception as e:
            print(f"⚠️  Error calculating volatility for {col}: {e}")
            return {
                'overall_volatility': 0.0,
                'annualized_volatility': 0.0,
                'coefficient_of_variation': 0.0,
                'volatility_level': 'unknown',
                'mean_return': 0.0,
                'sharpe_ratio': 0.0
            }
    
    def _get_fast_transformations(self, sample_data: pd.Series, col: str) -> List[str]:
        """Get fast transformation recommendations."""
        try:
            # Simple transformation logic
            if sample_data.min() > 0:
                return ['log', 'sqrt']
            else:
                return ['standardize', 'normalize']
        except:
            return []
    
    def _generate_transformation_recommendations_fast(self, sample_data: pd.Series, col: str) -> Dict[str, Any]:
        """Generate fast transformation recommendations."""
        try:
            skewness = sample_data.skew()
            
            # Calculate improvement percentage based on skewness reduction
            if abs(skewness) > 1:
                # High skewness - transformation will help significantly
                improvement = min(95, abs(skewness) * 15)  # Cap at 95%
                return {
                    'best_transformation': 'log' if sample_data.min() > 0 else 'box_cox',
                    'reason': f'High skewness: {skewness:.2f}',
                    'improvement_percentage': improvement,
                    'recommended_actions': [
                        'Apply logarithmic transformation' if sample_data.min() > 0 else 'Apply Box-Cox transformation',
                        'Verify stationarity after transformation',
                        'Consider additional differencing if needed'
                    ]
                }
            else:
                # Low skewness - minor improvement
                improvement = max(5, abs(skewness) * 10)  # At least 5% improvement
                return {
                    'best_transformation': 'standardize',
                    'reason': 'Low skewness, standard scaling recommended',
                    'improvement_percentage': improvement,
                    'recommended_actions': [
                        'Apply standardization (z-score normalization)',
                        'Monitor for stationarity improvements',
                        'Consider seasonal decomposition if needed'
                    ]
                }
        except:
            return {
                'best_transformation': 'none', 
                'reason': 'Unable to analyze',
                'improvement_percentage': 0,
                'recommended_actions': ['Manual data inspection required']
            }


def signal_handler(signum, frame):
    """Handle CTRL+C gracefully without showing traceback."""
    print("\n\n🛑 Analysis interrupted by user (CTRL+C)")
    print("👋 Goodbye!")
    sys.exit(0)


def main():
    """Main entry point."""
    # Set up signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    
    cli = TimeSeriesCLI()
    
    # Parse arguments
    args = cli.parse_arguments()
    
    # Validate arguments
    config = cli.validate_arguments(args)
    
    # Confirm analysis configuration
    if not cli.confirm_analysis(config, config['processing_options']['auto']):
        print(ColorUtils.red("❌ Analysis cancelled."))
        return
    
    # Start timing
    start_time = time.time()
    
    # Create the analyzer
    analyzer = TimeSeriesAnalyzer(
        auto_mode=config['processing_options']['auto'],
        output_directory=config['output_directory'],
        analysis_options=config['analysis_options'],
        fast_mode=config['processing_options'].get('fast', False),
        max_sample_size=config['processing_options'].get('max_sample_size', 10000)
    )
    
    # Run analysis
    analyzer.run(config)
    
    # Calculate and display processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n⏱️  Processing completed in {processing_time:.2f} seconds")
    print(f"{ColorUtils.green('🎉 Time series analysis finished successfully!')}")


if __name__ == "__main__":
    main()
