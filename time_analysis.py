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
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd

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


class TimeSeriesAnalyzer:
    """Main class for time series analysis operations."""
    
    def __init__(self, auto_mode: bool = False, output_directory: Optional[str] = None, 
                 analysis_options: Dict[str, Any] = None):
        """Initialize the time series analyzer.
        
        Args:
            auto_mode: If True, automatically answer 'y' to all questions
            output_directory: Directory to save results and transformed data
            analysis_options: Dictionary with analysis options
        """
        self.file_ops = TimeSeriesFileOperations()
        self.stationarity_analysis = StationarityAnalysis()
        self.seasonality_detection = SeasonalityDetection()
        self.financial_features = FinancialFeatures()
        self.data_transformation = TimeSeriesDataTransformation()
        self.reporter = TimeSeriesReporter()
        self.auto_mode = auto_mode
        self.output_directory = output_directory
        self.analysis_options = analysis_options or {}
        
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
            print("\n📊 Performing stationarity analysis...")
            analysis_results['stationarity'] = self.stationarity_analysis.analyze_stationarity(data, numeric_columns)
        
        # Seasonality detection
        if analysis_options.get('seasonality', False):
            print("\n📈 Performing seasonality detection...")
            analysis_results['seasonality'] = self.seasonality_detection.analyze_seasonality(data, numeric_columns)
        
        # Financial features analysis
        if analysis_options.get('financial', False):
            print("\n💰 Performing financial features analysis...")
            analysis_results['financial'] = self.financial_features.analyze_financial_features(data, numeric_columns)
        
        # Data transformation analysis
        if analysis_options.get('transform', False):
            print("\n🔄 Performing data transformation analysis...")
            # Generate transformation recommendations
            transformations = self._generate_transformation_recommendations(data, numeric_columns, analysis_results)
            
            if transformations:
                analysis_results['transformation'] = self.data_transformation.transform_data(
                    data, transformations, numeric_columns
                )
            else:
                analysis_results['transformation'] = {
                    'transformed_data': data,
                    'transformation_details': {},
                    'comparison': {},
                    'recommendations': {}
                }
        
        return {
            'file_info': file_info,
            'analysis_results': analysis_results,
            'numeric_columns': numeric_columns
        }
    
    def _generate_transformation_recommendations(self, data: pd.DataFrame, numeric_columns: List[str], 
                                               analysis_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate transformation recommendations based on analysis results."""
        transformations = {}
        
        # Check stationarity results for recommendations
        if 'stationarity' in analysis_results:
            stationarity_results = analysis_results['stationarity']
            recommendations = stationarity_results.get('stationarity_recommendations', {})
            
            for col in numeric_columns:
                if col in recommendations:
                    rec_data = recommendations[col]
                    if not rec_data.get('is_stationary', False):
                        # Non-stationary data needs transformation
                        transformations[col] = ['differencing', 'detrending', 'log_transform']
                    else:
                        # Stationary data might still benefit from normalization
                        transformations[col] = ['normalization', 'standardization']
        
        # If no stationarity analysis, use basic transformations
        if not transformations:
            for col in numeric_columns:
                transformations[col] = ['differencing', 'detrending', 'log_transform', 'normalization']
        
        return transformations
    
    def run_batch_processing(self, directory: str, directory_name: str, analysis_options: Dict[str, bool], 
                           auto_mode: bool = False) -> None:
        """
        Run batch processing for all files in a directory.
        
        Args:
            directory: Directory path to process
            directory_name: Human-readable directory name for display
            analysis_options: Dictionary of analysis options
        """
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING: {directory_name}")
        print(f"Directory: {directory}")
        print(f"{'='*80}")
        
        files = self.file_ops.get_files_in_directory(directory)
        
        if not files:
            print(f"No supported files found in {directory}")
            return
        
        print(f"Found {len(files)} files to process:")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file}")
        
        if not self.auto_mode:
            while True:
                proceed = self._get_user_input(f"\nProcess all {len(files)} files? (y/n): ")
                if proceed in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if proceed != 'y':
                print("Batch processing cancelled.")
                return
        
        # Process each file
        successful = 0
        failed = 0
        
        for i, filename in enumerate(files, 1):
            print(f"\n{'='*60}")
            print(f"PROCESSING FILE {i}/{len(files)}: {filename}")
            print(f"{'='*60}")
            
            try:
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
                
                successful += 1
                print(f"{ColorUtils.green('✅ Successfully processed:')} {filename}")
                
            except Exception as e:
                failed += 1
                self.reporter.display_error(str(e), {'filename': filename})
        
        # Summary
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"Total files: {len(files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/len(files)*100):.1f}%")
    
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
            
            save_path = f"data/fixed/transformed_by_time/{source}/{format_type}/{symbol}/{indicator}/{timeframe}/"
            
            # Create directory if it doesn't exist
            os.makedirs(save_path, exist_ok=True)
            
            # Generate filename
            filename = f"{symbol}_{timeframe}_{indicator}_time_transformed.{format_type}"
            full_path = os.path.join(save_path, filename)
            
            # Save data
            self.file_ops.save_data(transformed_data, full_path, format_type)
            
            print(f"\n✅ Transformed data saved to: {full_path}")
            
        except Exception as e:
            print(f"\n❌ Error saving transformed data: {str(e)}")
    
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
                # Single file processing
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
                
            elif file_processing['mode'] == 'batch':
                # Batch processing
                self.run_batch_processing(file_processing['directory'], 
                                       f"Directory: {file_processing['directory']}", 
                                       analysis_options,
                                       self.auto_mode)
                
            elif file_processing['mode'] == 'batch_all':
                # Process all directories
                directories = [
                    ("data/cache/csv_converted/", "CSV Converted Files"),
                    ("data/raw_parquet/", "Raw Parquet Files"),
                    ("data/indicators/parquet/", "Indicators Parquet Files"),
                    ("data/indicators/json/", "Indicators JSON Files"),
                    ("data/indicators/csv/", "Indicators CSV Files"),
                    ("data/fixed/", "Fixed Files")
                ]
                
                total_successful = 0
                total_failed = 0
                total_files = 0
                
                for directory, name in directories:
                    if os.path.exists(directory):
                        files = self.file_ops.get_files_in_directory(directory)
                        if files:
                            print(f"\n{'='*100}")
                            print(f"PROCESSING DIRECTORY: {name}")
                            print(f"{'='*100}")
                            
                            for filename in files:
                                total_files += 1
                                print(f"\n{'='*60}")
                                print(f"PROCESSING FILE: {filename}")
                                print(f"{'='*60}")
                                
                                try:
                                    results = self.analyze_file(filename, analysis_options)
                                    
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
                                    
                                    total_successful += 1
                                    print(f"{ColorUtils.green('✅ Successfully processed:')} {filename}")
                                    
                                except Exception as e:
                                    total_failed += 1
                                    self.reporter.display_error(str(e), {'filename': filename})
                
                # Overall summary
                print(f"\n{'='*100}")
                print(f"🌟 BATCH PROCESSING ALL DIRECTORIES COMPLETE 🌟")
                print(f"{'='*100}")
                print(f"📊 Total files processed: {total_files}")
                print(f"✅ Successful: {total_successful}")
                print(f"❌ Failed: {total_failed}")
                if total_files > 0:
                    success_rate = (total_successful/total_files*100)
                    print(f"📈 Overall success rate: {success_rate:.1f}%")
                else:
                    print("⚠️  No files found to process.")
                    
            elif file_processing['mode'] == 'custom_path':
                # Custom path processing
                custom_path = file_processing['directory']
                path_validation = self.file_ops.validate_custom_path(custom_path)
                
                if not path_validation['valid']:
                    print(f"❌ Error: {path_validation['error']}")
                    return
                
                if path_validation['is_file']:
                    # Single file processing
                    print(f"\n📁 Processing single file: {custom_path}")
                    
                    # Create file_info for direct processing
                    file_info = {
                        "file_path": custom_path,
                        "format": custom_path.split('.')[-1].lower(),
                        "symbol": "Unknown",
                        "timeframe": "Unknown",
                        "source": "Custom",
                        "indicator": None,
                        "folder_source": os.path.dirname(custom_path)
                    }
                    
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
                        
                elif path_validation['is_directory']:
                    # Directory processing
                    print(f"\n📂 Starting batch processing for custom directory: {custom_path}")
                    self.run_batch_processing(custom_path, f"Custom Directory: {custom_path}", analysis_options, self.auto_mode)
            
            print("\n🎉 Time series analysis completed successfully!")
            
        except Exception as e:
            print(f"\nError during time series analysis: {str(e)}")
            sys.exit(1)


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
        analysis_options=config['analysis_options']
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
