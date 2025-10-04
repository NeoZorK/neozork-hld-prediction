#!/usr/bin/env python3
"""
Financial Analysis Tool

This script provides comprehensive financial analysis capabilities for OHLCV data,
including price validation, volatility analysis, returns analysis, and drawdown analysis.

Usage:
    python finance_analysis.py -f filename.parquet --ohlcv --volatility --returns --drawdown
    python finance_analysis.py --batch-fixed --ohlcv --volatility --auto
    python finance_analysis.py --path data/custom/ --ohlcv --volatility --returns --drawdown --auto

Note: It is recommended to use already cleaned and transformed data by clear_data.py and
stat_analysis.py and time_analysis.py from data/fixed/ folder. You can run clear_data.py --help for more information.
"""

import sys
import os
import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.finance import (
    FinanceFileOperations,
    FinanceCLI,
    FinanceReporter,
    FinanceProgressTracker,
    OHLCVAnalysis,
    VolatilityAnalysis,
    ReturnsAnalysis,
    DrawdownAnalysis
)
from src.finance.color_utils import ColorUtils


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/finance_analysis.log', mode='a')
        ]
    )


def main():
    """Main function for financial analysis tool."""
    try:
        # Initialize components
        cli = FinanceCLI()
        file_ops = FinanceFileOperations()
        reporter = FinanceReporter()
        
        # Parse arguments
        args = cli.parse_arguments()
        config = cli.validate_arguments(args)
        
        # Setup logging
        setup_logging(config['processing_options']['verbose'])
        logger = logging.getLogger(__name__)
        
        # Display help examples if requested
        if hasattr(args, 'help_examples') and args.help_examples:
            cli.display_help_examples()
            return
        
        # Confirm analysis configuration
        if not cli.confirm_analysis(config, config['processing_options']['auto']):
            print(ColorUtils.warning("Analysis cancelled by user"))
            return
        
        # Process files based on configuration
        file_processing = config['file_processing']
        analysis_options = config['analysis_options']
        
        if file_processing['mode'] == 'single_file':
            # Process single file
            success = process_single_file(
                file_ops, file_processing['filename'], 
                analysis_options, config['processing_options']['auto']
            )
            
        elif file_processing['mode'] == 'batch':
            # Process batch directory
            success = process_batch_directory(
                file_ops, file_processing['directory'], 
                analysis_options, config['processing_options']['auto']
            )
            
        elif file_processing['mode'] == 'batch_all':
            # Process all supported directories
            success = process_all_directories(
                file_ops, analysis_options, config['processing_options']['auto']
            )
            
        elif file_processing['mode'] == 'custom_path':
            # Process custom path
            success = process_custom_path(
                file_ops, file_processing['directory'], 
                analysis_options, config['processing_options']['auto']
            )
        
        else:
            print(ColorUtils.error("Invalid file processing mode"))
            return
        
        if success:
            print(ColorUtils.success("Financial analysis completed successfully"))
        else:
            print(ColorUtils.error("Financial analysis completed with errors"))
    
    except KeyboardInterrupt:
        print(ColorUtils.warning("\nAnalysis interrupted by user"))
    except Exception as e:
        print(ColorUtils.error(f"Unexpected error: {str(e)}"))
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)


def process_single_file(file_ops: FinanceFileOperations, filename: str, 
                       analysis_options: Dict[str, bool], auto_mode: bool) -> bool:
    """Process a single file for financial analysis."""
    try:
        # Validate file
        file_metadata = file_ops.validate_file_path(filename)
        if not file_metadata:
            print(ColorUtils.error(f"File '{filename}' not found in supported directories"))
            return False
        
        print(ColorUtils.info(f"Processing file: {filename}"))
        print(ColorUtils.info(f"File metadata: {file_metadata}"))
        
        # Load data
        data = file_ops.load_data(file_metadata['file_path'], file_metadata['format'])
        if data is None:
            print(ColorUtils.error(f"Failed to load data from {filename}"))
            return False
        
        # Perform analysis
        return perform_financial_analysis(
            data, file_metadata, analysis_options, auto_mode
        )
    
    except Exception as e:
        print(ColorUtils.error(f"Error processing single file: {str(e)}"))
        return False


def process_batch_directory(file_ops: FinanceFileOperations, directory: str,
                          analysis_options: Dict[str, bool], auto_mode: bool) -> bool:
    """Process all files in a batch directory."""
    try:
        if not os.path.exists(directory):
            print(ColorUtils.error(f"Directory '{directory}' does not exist"))
            return False
        
        # Get files in directory
        files = file_ops.get_files_in_directory(directory)
        if not files:
            print(ColorUtils.warning(f"No supported files found in '{directory}'"))
            return True
        
        print(ColorUtils.info(f"Processing {len(files)} files in '{directory}'"))
        
        # Initialize progress tracker
        progress_tracker = FinanceProgressTracker(len(files), verbose=True)
        progress_tracker.start_analysis()
        
        successful_files = 0
        failed_files = 0
        
        for filename in files:
            progress_tracker.start_file(filename)
            
            try:
                # Load and analyze file
                file_path = os.path.join(directory, filename)
                format_type = filename.split('.')[-1].lower()
                
                data = file_ops.load_data(file_path, format_type)
                if data is None:
                    progress_tracker.complete_file(False, f"Failed to load data")
                    failed_files += 1
                    continue
                
                # Create file metadata with proper parsing
                file_ops_temp = FinanceFileOperations()
                symbol, timeframe, indicator = file_ops_temp._parse_filename(filename)
                source = file_ops_temp._determine_source(directory)
                folder_source = file_ops_temp._determine_folder_source(file_path)
                
                file_metadata = {
                    'file_path': file_path,
                    'format': format_type,
                    'symbol': symbol,
                    'timeframe': timeframe,
                    'source': source,
                    'indicator': indicator,
                    'folder_source': folder_source,
                    'folder_path': directory
                }
                
                # Perform analysis
                success = perform_financial_analysis(
                    data, file_metadata, analysis_options, auto_mode
                )
                
                if success:
                    progress_tracker.complete_file(True)
                    successful_files += 1
                else:
                    progress_tracker.complete_file(False, "Analysis failed")
                    failed_files += 1
                
            except Exception as e:
                progress_tracker.complete_file(False, str(e))
                failed_files += 1
        
        # Display final summary
        progress_tracker.display_final_summary()
        
        return successful_files > 0
    
    except Exception as e:
        print(ColorUtils.error(f"Error processing batch directory: {str(e)}"))
        return False


def process_all_directories(file_ops: FinanceFileOperations, 
                           analysis_options: Dict[str, bool], auto_mode: bool) -> bool:
    """Process all supported directories."""
    try:
        supported_dirs = file_ops.get_supported_directories()
        print(ColorUtils.info(f"Processing all supported directories: {supported_dirs}"))
        
        # Initialize batch progress tracker
        from src.finance.progress_tracker import BatchProgressTracker
        progress_tracker = BatchProgressTracker(len(supported_dirs), verbose=True)
        progress_tracker.start_batch()
        
        successful_dirs = 0
        failed_dirs = 0
        
        for directory in supported_dirs:
            if not os.path.exists(directory):
                print(ColorUtils.warning(f"Directory '{directory}' does not exist, skipping"))
                continue
            
            progress_tracker.start_directory(directory)
            
            try:
                # Process directory
                success = process_batch_directory(
                    file_ops, directory, analysis_options, auto_mode
                )
                
                if success:
                    progress_tracker.complete_directory(True)
                    successful_dirs += 1
                else:
                    progress_tracker.complete_directory(False)
                    failed_dirs += 1
                
            except Exception as e:
                progress_tracker.complete_directory(False)
                failed_dirs += 1
                print(ColorUtils.error(f"Error processing directory '{directory}': {str(e)}"))
        
        # Display final summary
        progress_tracker.display_final_summary()
        
        return successful_dirs > 0
    
    except Exception as e:
        print(ColorUtils.error(f"Error processing all directories: {str(e)}"))
        return False


def process_custom_path(file_ops: FinanceFileOperations, path: str,
                       analysis_options: Dict[str, bool], auto_mode: bool) -> bool:
    """Process custom file or directory path."""
    try:
        if os.path.isfile(path):
            # Single file
            filename = os.path.basename(path)
            format_type = filename.split('.')[-1].lower()
            
            if format_type not in ['parquet', 'json', 'csv']:
                print(ColorUtils.error(f"Unsupported file format: {format_type}"))
                return False
            
            # Load and analyze file
            data = file_ops.load_data(path, format_type)
            if data is None:
                print(ColorUtils.error(f"Failed to load data from {path}"))
                return False
            
            # Parse metadata from filename and path
            file_ops_temp = FinanceFileOperations()
            symbol, timeframe, indicator = file_ops_temp._parse_filename(filename)
            source = file_ops_temp._determine_source(os.path.dirname(path))
            folder_source = file_ops_temp._determine_folder_source(path)
            
            file_metadata = {
                'file_path': path,
                'format': format_type,
                'symbol': symbol,
                'timeframe': timeframe,
                'source': source,
                'indicator': indicator,
                'folder_source': folder_source,
                'folder_path': os.path.dirname(path)
            }
            
            return perform_financial_analysis(
                data, file_metadata, analysis_options, auto_mode
            )
        
        elif os.path.isdir(path):
            # Directory
            return process_batch_directory(
                file_ops, path, analysis_options, auto_mode
            )
        
        else:
            print(ColorUtils.error(f"Path '{path}' is neither a file nor a directory"))
            return False
    
    except Exception as e:
        print(ColorUtils.error(f"Error processing custom path: {str(e)}"))
        return False


def perform_financial_analysis(data, file_metadata: Dict[str, Any], 
                              analysis_options: Dict[str, bool], 
                              auto_mode: bool) -> bool:
    """Perform comprehensive financial analysis."""
    try:
        print(ColorUtils.header("Starting Financial Analysis"))
        print("=" * 80)
        
        # Identify numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            print(ColorUtils.error("No numeric columns found in data"))
            return False
        
        print(ColorUtils.info(f"Found {len(numeric_columns)} numeric columns: {numeric_columns}"))
        
        # Initialize analysis results
        analysis_results = {}
        
        # OHLCV Analysis
        if analysis_options.get('ohlcv', False):
            print(ColorUtils.analysis("Performing OHLCV Analysis..."))
            ohlcv_analyzer = OHLCVAnalysis()
            ohlcv_results = ohlcv_analyzer.analyze_ohlcv_data(data, numeric_columns)
            analysis_results['ohlcv_analysis'] = ohlcv_results
            
            # Display OHLCV summary
            ohlcv_summary = ohlcv_analyzer.get_analysis_summary(ohlcv_results)
            print(ColorUtils.info("OHLCV Analysis Summary:"))
            for line in ohlcv_summary.split('\n'):
                if line.strip():
                    print(ColorUtils.info(f"  {line}"))
        
        # Volatility Analysis
        if analysis_options.get('volatility', False):
            print(ColorUtils.analysis("Performing Volatility Analysis..."))
            volatility_analyzer = VolatilityAnalysis()
            volatility_results = volatility_analyzer.analyze_volatility(data, numeric_columns)
            analysis_results['volatility_analysis'] = volatility_results
            
            # Display volatility summary
            volatility_summary = volatility_analyzer.get_analysis_summary(volatility_results)
            print(ColorUtils.info("Volatility Analysis Summary:"))
            for line in volatility_summary.split('\n'):
                if line.strip():
                    print(ColorUtils.info(f"  {line}"))
        
        # Returns Analysis
        if analysis_options.get('returns', False):
            print(ColorUtils.analysis("Performing Returns Analysis..."))
            returns_analyzer = ReturnsAnalysis()
            returns_results = returns_analyzer.analyze_returns(data, numeric_columns)
            analysis_results['returns_analysis'] = returns_results
            
            # Display returns summary
            returns_summary = returns_analyzer.get_analysis_summary(returns_results)
            print(ColorUtils.info("Returns Analysis Summary:"))
            for line in returns_summary.split('\n'):
                if line.strip():
                    print(ColorUtils.info(f"  {line}"))
        
        # Drawdown Analysis
        if analysis_options.get('drawdown', False):
            print(ColorUtils.analysis("Performing Drawdown Analysis..."))
            drawdown_analyzer = DrawdownAnalysis()
            drawdown_results = drawdown_analyzer.analyze_drawdowns(data, numeric_columns)
            analysis_results['drawdown_analysis'] = drawdown_results
            
            # Display drawdown summary
            drawdown_summary = drawdown_analyzer.get_analysis_summary(drawdown_results)
            print(ColorUtils.info("Drawdown Analysis Summary:"))
            for line in drawdown_summary.split('\n'):
                if line.strip():
                    print(ColorUtils.info(f"  {line}"))
        
        # Generate comprehensive report
        print(ColorUtils.analysis("Generating Comprehensive Report..."))
        analysis_types = [analysis_type for analysis_type, enabled in analysis_options.items() if enabled]
        
        reporter = FinanceReporter()
        comprehensive_report = reporter.generate_comprehensive_report(
            analysis_results, file_metadata, analysis_types
        )
        
        # Display report
        print("\n" + "=" * 80)
        print(comprehensive_report)
        print("=" * 80)
        
        # Ask about data transformation if not in auto mode
        if not auto_mode:
            ask_about_transformation(analysis_results)
        
        return True
    
    except Exception as e:
        print(ColorUtils.error(f"Error in financial analysis: {str(e)}"))
        return False


def ask_about_transformation(analysis_results: Dict[str, Any]):
    """Ask user about data transformation recommendations."""
    try:
        print(ColorUtils.info("\nData Transformation Recommendations:"))
        
        # Generate transformation recommendations
        reporter = FinanceReporter()
        recommendations = reporter.generate_transformation_recommendations(analysis_results)
        
        # Display recommendations
        for category, recs in recommendations.items():
            if recs and category != 'error':
                print(f"\n{ColorUtils.section(category.replace('_', ' ').title())}:")
                for rec in recs:
                    print(f"  • {rec}")
        
        # Ask if user wants to transform data
        while True:
            transform = input(ColorUtils.info("\nDo you want to transform your data? (y/n): ")).lower().strip()
            if transform in ['y', 'n']:
                break
            print(ColorUtils.warning("Please enter 'y' or 'n'"))
        
        if transform == 'y':
            print(ColorUtils.info("Data transformation would be implemented here"))
            print(ColorUtils.info("This feature will be available in future versions"))
            
            # Ask if user wants to save transformed data
            while True:
                save = input(ColorUtils.info("Do you want to save transformed data? (y/n): ")).lower().strip()
                if save in ['y', 'n']:
                    break
                print(ColorUtils.warning("Please enter 'y' or 'n'"))
            
            if save == 'y':
                print(ColorUtils.info("Transformed data would be saved here"))
                print(ColorUtils.info("This feature will be available in future versions"))
    
    except Exception as e:
        print(ColorUtils.error(f"Error in transformation recommendations: {str(e)}"))


if __name__ == "__main__":
    main()
