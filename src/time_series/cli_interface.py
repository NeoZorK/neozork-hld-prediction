"""
CLI Interface Module for Time Series Analysis

This module provides command-line interface for time series analysis.
It includes argument parsing and validation for all supported operations.

Features:
- File processing: Single file, batch processing, custom path
- Analysis options: Stationarity, seasonality, financial features, transformations
- Auto mode: Non-interactive processing
- Comprehensive help and examples
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
from .color_utils import ColorUtils


class TimeSeriesCLI:
    """Handles command-line interface for time series analysis."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.logger = logging.getLogger(__name__)
    
    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure argument parser.
        
        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="📈 Time Series Analysis Tool for Financial Data 🚀",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Single file processing:
  python time_analysis.py -f GBPUSD_PERIOD_MN1.parquet --stationarity --seasonality
  python time_analysis.py -f binance_BTCUSD_1h.parquet --stationarity --financial --auto
  python time_analysis.py -f polygon_ETHUSD_daily_rsi.json --stationarity --seasonality --financial
  
  # Batch processing:
  python time_analysis.py --batch-csv-converted --stationarity --auto
  python time_analysis.py --batch-raw-parquet --stationarity --seasonality --auto
  python time_analysis.py --batch-indicators-parquet --stationarity --seasonality --financial --auto
  python time_analysis.py --batch-indicators-json --stationarity --auto
  python time_analysis.py --batch-indicators-csv --stationarity --seasonality --auto
  python time_analysis.py --batch-fixed --stationarity --seasonality --financial --auto
  python time_analysis.py --batch-all --stationarity --seasonality --financial --auto
  
  # Custom path processing:
  python time_analysis.py --path data/custom_folder/ --stationarity --auto
  python time_analysis.py --path data/fixed/binance/parquet/BTCUSDT/ --stationarity --seasonality --auto
  python time_analysis.py --path data/indicators/parquet/specific_file.parquet --stationarity --financial
  python time_analysis.py --path data/fixed/ --recursive --stationarity --seasonality --financial --auto
  
  # Analysis options:
  python time_analysis.py -f data.parquet --stationarity
  python time_analysis.py -f data.parquet --seasonality
  python time_analysis.py -f data.parquet --financial
  python time_analysis.py -f data.parquet --transform
  python time_analysis.py -f data.parquet --stationarity --seasonality --financial --auto
  
  # Detailed analysis options:
  python time_analysis.py -f data.parquet --adf-test --day-patterns --price-range
  python time_analysis.py -f data.parquet --critical-values --month-patterns --volatility
  python time_analysis.py -f data.parquet --stationarity-recommendations --cyclical-patterns --price-changes
  
  # Output options:
  python time_analysis.py -f data.parquet --stationarity --output results/
  python time_analysis.py --batch-all --stationarity --output analysis_results/ --auto

Note: It is recommended to use already cleaned and transformed data by clear_data.py and stat_analysis.py 
from data/fixed/ folder. You can run clear_data.py --help for more information.
            """
        )
        
        # File processing group (mutually exclusive)
        file_group = parser.add_mutually_exclusive_group(required=True)
        
        # Single file processing
        file_group.add_argument(
            "-f", "--file",
            help="📁 Name of the file to analyze (must be from supported directories)"
        )
        
        # Batch processing flags
        file_group.add_argument(
            "--batch-csv-converted",
            action="store_true",
            help="📊 Process all files in data/cache/csv_converted/ directory"
        )
        
        file_group.add_argument(
            "--batch-raw-parquet",
            action="store_true",
            help="📦 Process all files in data/raw_parquet/ directory"
        )
        
        file_group.add_argument(
            "--batch-indicators-parquet",
            action="store_true",
            help="📈 Process all files in data/indicators/parquet/ directory"
        )
        
        file_group.add_argument(
            "--batch-indicators-json",
            action="store_true",
            help="📋 Process all files in data/indicators/json/ directory"
        )
        
        file_group.add_argument(
            "--batch-indicators-csv",
            action="store_true",
            help="📄 Process all files in data/indicators/csv/ directory"
        )
        
        file_group.add_argument(
            "--batch-fixed",
            action="store_true",
            help="🧹 Process all files in data/fixed/ directory (cleaned data - recommended)"
        )
        
        file_group.add_argument(
            "--batch-all",
            action="store_true",
            help="🌟 Process all files in all supported directories"
        )
        
        file_group.add_argument(
            "--path",
            type=str,
            help="📂 Process all files in specified directory path or single file (e.g., --path data/custom_folder/ or --path data/file.parquet)"
        )
        
        # Main analysis options
        analysis_group = parser.add_argument_group('Main Analysis Options')
        analysis_group.add_argument(
            "--stationarity",
            action="store_true",
            help="📊 Perform stationarity analysis (ADF test, critical values, recommendations)"
        )
        
        analysis_group.add_argument(
            "--seasonality",
            action="store_true",
            help="📈 Perform seasonality detection (day-of-week, monthly, cyclical patterns)"
        )
        
        analysis_group.add_argument(
            "--financial",
            action="store_true",
            help="💰 Perform financial features analysis (price range, changes, volatility)"
        )
        
        analysis_group.add_argument(
            "--transform",
            action="store_true",
            help="🔄 Perform data transformation analysis and recommendations"
        )
        
        # Detailed stationarity options
        stationarity_group = parser.add_argument_group('Stationarity Analysis Options')
        stationarity_group.add_argument(
            "--adf-test",
            action="store_true",
            help="📊 Augmented Dickey-Fuller test for stationarity"
        )
        
        stationarity_group.add_argument(
            "--critical-values",
            action="store_true",
            help="📈 Critical values at different significance levels (1%%, 5%%, 10%%)"
        )
        
        stationarity_group.add_argument(
            "--stationarity-recommendations",
            action="store_true",
            help="💡 Recommendations for achieving stationarity through differencing"
        )
        
        # Detailed seasonality options
        seasonality_group = parser.add_argument_group('Seasonality Detection Options')
        seasonality_group.add_argument(
            "--day-patterns",
            action="store_true",
            help="📅 Day-of-week patterns analysis"
        )
        
        seasonality_group.add_argument(
            "--month-patterns",
            action="store_true",
            help="📆 Monthly patterns analysis"
        )
        
        seasonality_group.add_argument(
            "--cyclical-patterns",
            action="store_true",
            help="🔄 Cyclical patterns analysis"
        )
        
        # Detailed financial options
        financial_group = parser.add_argument_group('Financial Features Options')
        financial_group.add_argument(
            "--price-range",
            action="store_true",
            help="📊 Price range analysis (High - Low)"
        )
        
        financial_group.add_argument(
            "--price-changes",
            action="store_true",
            help="📈 Price changes analysis (absolute and percentage)"
        )
        
        financial_group.add_argument(
            "--volatility",
            action="store_true",
            help="📊 Volatility analysis (standard deviation, coefficient of variation)"
        )
        
        # Processing options
        processing_group = parser.add_argument_group('Processing Options')
        processing_group.add_argument(
            "--auto",
            action="store_true",
            help="🤖 Automatically answer 'y' to all questions (non-interactive mode)"
        )
        
        processing_group.add_argument(
            "--recursive",
            action="store_true",
            help="🔍 Recursively search subdirectories when using --path"
        )
        
        processing_group.add_argument(
            "--output",
            type=str,
            help="📁 Output directory for saving results and transformed data"
        )
        
        processing_group.add_argument(
            "--verbose",
            action="store_true",
            help="📝 Enable verbose logging output"
        )
        
        # Version and help
        parser.add_argument(
            "--version",
            action="version",
            version="📈 Time Series Analysis Tool v1.0.0 🚀"
        )
        
        return parser
    
    def parse_arguments(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command line arguments.
        
        Args:
            args: List of arguments to parse. If None, uses sys.argv.
            
        Returns:
            Parsed arguments namespace
        """
        parser = self.create_parser()
        return parser.parse_args(args)
    
    def validate_arguments(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        Validate parsed arguments and return configuration.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Dictionary with validated configuration
        """
        config = {
            'file_processing': self._determine_file_processing_mode(args),
            'analysis_options': self._get_analysis_options(args),
            'processing_options': self._get_processing_options(args),
            'output_directory': self._get_output_directory(args),
            'recursive': getattr(args, 'recursive', False),
            'verbose': getattr(args, 'verbose', False)
        }
        
        # Validate that at least one analysis option is selected
        analysis_options = config['analysis_options']
        main_options = ['stationarity', 'seasonality', 'financial', 'transform']
        detailed_options = [
            'adf_test', 'critical_values', 'stationarity_recommendations',
            'day_patterns', 'month_patterns', 'cyclical_patterns',
            'price_range', 'price_changes', 'volatility'
        ]
        
        has_main_option = any(analysis_options[option] for option in main_options)
        has_detailed_option = any(analysis_options[option] for option in detailed_options)
        
        if not has_main_option and not has_detailed_option:
            print("❌ Error: At least one analysis option must be selected")
            print("   Main options: --stationarity, --seasonality, --financial, --transform")
            print("   Detailed options: --adf-test, --critical-values, --stationarity-recommendations,")
            print("                     --day-patterns, --month-patterns, --cyclical-patterns,")
            print("                     --price-range, --price-changes, --volatility")
            sys.exit(1)
        
        # Validate file processing mode
        if not config['file_processing']['mode']:
            print("❌ Error: Invalid file processing mode")
            sys.exit(1)
        
        return config
    
    def _determine_file_processing_mode(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        Determine file processing mode from arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Dictionary with file processing configuration
        """
        if args.file:
            return {
                'mode': 'single_file',
                'filename': args.file,
                'directory': None
            }
        elif args.batch_csv_converted:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/cache/csv_converted/'
            }
        elif args.batch_raw_parquet:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/raw_parquet/'
            }
        elif args.batch_indicators_parquet:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/indicators/parquet/'
            }
        elif args.batch_indicators_json:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/indicators/json/'
            }
        elif args.batch_indicators_csv:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/indicators/csv/'
            }
        elif args.batch_fixed:
            return {
                'mode': 'batch',
                'filename': None,
                'directory': 'data/fixed/'
            }
        elif args.batch_all:
            return {
                'mode': 'batch_all',
                'filename': None,
                'directory': None
            }
        elif args.path:
            return {
                'mode': 'custom_path',
                'filename': None,
                'directory': args.path
            }
        else:
            return {
                'mode': None,
                'filename': None,
                'directory': None
            }
    
    def _get_analysis_options(self, args: argparse.Namespace) -> Dict[str, bool]:
        """
        Get analysis options from arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Dictionary with analysis options
        """
        return {
            # Main analysis options
            'stationarity': getattr(args, 'stationarity', False),
            'seasonality': getattr(args, 'seasonality', False),
            'financial': getattr(args, 'financial', False),
            'transform': getattr(args, 'transform', False),
            
            # Detailed stationarity options
            'adf_test': getattr(args, 'adf_test', False),
            'critical_values': getattr(args, 'critical_values', False),
            'stationarity_recommendations': getattr(args, 'stationarity_recommendations', False),
            
            # Detailed seasonality options
            'day_patterns': getattr(args, 'day_patterns', False),
            'month_patterns': getattr(args, 'month_patterns', False),
            'cyclical_patterns': getattr(args, 'cyclical_patterns', False),
            
            # Detailed financial options
            'price_range': getattr(args, 'price_range', False),
            'price_changes': getattr(args, 'price_changes', False),
            'volatility': getattr(args, 'volatility', False)
        }
    
    def _get_processing_options(self, args: argparse.Namespace) -> Dict[str, bool]:
        """
        Get processing options from arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Dictionary with processing options
        """
        return {
            'auto': getattr(args, 'auto', False),
            'recursive': getattr(args, 'recursive', False),
            'verbose': getattr(args, 'verbose', False)
        }
    
    def _get_output_directory(self, args: argparse.Namespace) -> Optional[str]:
        """
        Get output directory from arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Output directory path or None
        """
        output_dir = getattr(args, 'output', None)
        
        if output_dir:
            # Create directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            return output_dir
        
        return None
    
    def validate_custom_path(self, path: str) -> Dict[str, Any]:
        """
        Validate custom path argument.
        
        Args:
            path: Path to validate
            
        Returns:
            Dictionary with path validation results
        """
        result = {
            'valid': False,
            'is_file': False,
            'is_directory': False,
            'exists': False,
            'error': None
        }
        
        # Check if path exists
        if not os.path.exists(path):
            result['error'] = f"Path '{path}' does not exist"
            return result
        
        result['exists'] = True
        
        # Check if it's a file or directory
        if os.path.isfile(path):
            result['is_file'] = True
            result['valid'] = True
        elif os.path.isdir(path):
            result['is_directory'] = True
            result['valid'] = True
        else:
            result['error'] = f"Path '{path}' is neither a file nor a directory"
        
        return result
    
    def get_supported_directories(self) -> List[str]:
        """
        Get list of supported data directories.
        
        Returns:
            List of supported directory paths
        """
        return [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/",
            "data/fixed/"
        ]
    
    def display_help_examples(self):
        """Display additional help examples."""
        print("\n" + "=" * 80)
        print("ADDITIONAL EXAMPLES")
        print("=" * 80)
        print()
        print("🔍 RECOMMENDED USAGE:")
        print("   It is recommended to use already cleaned and transformed data by clear_data.py")
        print("   and stat_analysis.py from data/fixed/ folder.")
        print("   You can run clear_data.py --help for more information about data cleaning.")
        print()
        print("📊 ANALYSIS COMBINATIONS:")
        print("   --stationarity                    : Stationarity analysis only")
        print("   --seasonality                     : Seasonality detection only")
        print("   --financial                       : Financial features only")
        print("   --transform                       : Data transformation only")
        print("   --stationarity --seasonality      : Stationarity + seasonality")
        print("   --stationarity --financial        : Stationarity + financial features")
        print("   --seasonality --financial         : Seasonality + financial features")
        print("   --stationarity --seasonality --financial : Complete time series analysis")
        print()
        print("📁 BATCH PROCESSING:")
        print("   --batch-fixed --auto              : Process all cleaned data automatically")
        print("   --batch-all --stationarity --auto : Process all data with stationarity analysis")
        print("   --path data/fixed/ --recursive    : Process all files recursively")
        print()
        print("💾 OUTPUT OPTIONS:")
        print("   --output results/                 : Save results to results/ directory")
        print("   --output analysis_2024/           : Save results to analysis_2024/ directory")
        print()
    
    def get_user_input(self, prompt: str, auto_mode: bool = False) -> str:
        """
        Get user input with automatic mode support.
        
        Args:
            prompt: Input prompt to display
            auto_mode: If True, automatically answer 'y' to all questions
            
        Returns:
            User input or 'y' if in auto mode
        """
        if auto_mode:
            print(f"{prompt} y")
            return "y"
        else:
            return input(prompt).lower().strip()
    
    def confirm_analysis(self, config: Dict[str, Any], auto_mode: bool = False) -> bool:
        """
        Confirm analysis configuration with user.
        
        Args:
            config: Analysis configuration
            auto_mode: If True, automatically confirm
            
        Returns:
            True if user confirms, False otherwise
        """
        print("\n" + "=" * 80)
        print(ColorUtils.blue("TIME SERIES ANALYSIS CONFIGURATION"))
        print("=" * 80)
        
        # File processing mode
        file_mode = config['file_processing']['mode']
        if file_mode == 'single_file':
            print(f"📁 File: {config['file_processing']['filename']}")
        elif file_mode == 'batch':
            print(f"📂 Directory: {config['file_processing']['directory']}")
        elif file_mode == 'batch_all':
            print("🌟 All supported directories")
        elif file_mode == 'custom_path':
            print(f"📂 Custom path: {config['file_processing']['directory']}")
        
        # Analysis options
        analysis_options = config['analysis_options']
        print("\n📊 Analysis Options:")
        if analysis_options['stationarity']:
            print(f"  {ColorUtils.green('✅ Stationarity Analysis')}")
        if analysis_options['seasonality']:
            print(f"  {ColorUtils.green('✅ Seasonality Detection')}")
        if analysis_options['financial']:
            print(f"  {ColorUtils.green('✅ Financial Features')}")
        if analysis_options['transform']:
            print(f"  {ColorUtils.green('✅ Data Transformation')}")
        
        # Detailed analysis options
        detailed_options = []
        if analysis_options['adf_test']:
            detailed_options.append("ADF Test")
        if analysis_options['critical_values']:
            detailed_options.append("Critical Values")
        if analysis_options['stationarity_recommendations']:
            detailed_options.append("Stationarity Recommendations")
        if analysis_options['day_patterns']:
            detailed_options.append("Day-of-Week Patterns")
        if analysis_options['month_patterns']:
            detailed_options.append("Monthly Patterns")
        if analysis_options['cyclical_patterns']:
            detailed_options.append("Cyclical Patterns")
        if analysis_options['price_range']:
            detailed_options.append("Price Range Analysis")
        if analysis_options['price_changes']:
            detailed_options.append("Price Changes Analysis")
        if analysis_options['volatility']:
            detailed_options.append("Volatility Analysis")
        
        if detailed_options:
            print("\n🔍 Detailed Analysis Options:")
            for option in detailed_options:
                print(f"  {ColorUtils.green('✅ ' + option)}")
        
        # Processing options
        processing_options = config['processing_options']
        print("\n⚙️  Processing Options:")
        if processing_options['auto']:
            print(f"  {ColorUtils.green('✅ Auto mode (non-interactive)')}")
        if processing_options['recursive']:
            print(f"  {ColorUtils.green('✅ Recursive directory search')}")
        if processing_options['verbose']:
            print(f"  {ColorUtils.green('✅ Verbose logging')}")
        
        # Output directory
        if config['output_directory']:
            print(f"\n💾 Output Directory: {config['output_directory']}")
        
        print("=" * 80)
        
        # Get confirmation
        while True:
            proceed = self.get_user_input("\n🚀 Proceed with time series analysis? (y/n): ", auto_mode)
            if proceed in ['y', 'n']:
                break
            print("⚠️  Please enter 'y' or 'n'")
        
        return proceed == 'y'
