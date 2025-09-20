"""
CLI Interface Module

This module provides command-line interface for statistical analysis.
It includes argument parsing and validation for all supported operations.

Features:
- File processing: Single file, batch processing, custom path
- Analysis options: Descriptive stats, distribution analysis, transformations
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


class StatisticsCLI:
    """Handles command-line interface for statistical analysis."""
    
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
            description="📊 Statistical Analysis Tool for Financial Data 🚀",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Single file processing:
  python stat_analysis.py -f GBPUSD_PERIOD_MN1.parquet --descriptive --distribution
  python stat_analysis.py -f binance_BTCUSD_1h.parquet --descriptive --transform --auto
  python stat_analysis.py -f polygon_ETHUSD_daily_rsi.json --descriptive --distribution --transform
  
  # Batch processing:
  python stat_analysis.py --batch-csv-converted --descriptive --auto
  python stat_analysis.py --batch-raw-parquet --descriptive --distribution --auto
  python stat_analysis.py --batch-indicators-parquet --descriptive --distribution --transform --auto
  python stat_analysis.py --batch-indicators-json --descriptive --auto
  python stat_analysis.py --batch-indicators-csv --descriptive --distribution --auto
  python stat_analysis.py --batch-fixed --descriptive --distribution --transform --auto
  python stat_analysis.py --batch-all --descriptive --distribution --transform --auto
  
  # Custom path processing:
  python stat_analysis.py --path data/custom_folder/ --descriptive --auto
  python stat_analysis.py --path data/fixed/binance/parquet/BTCUSDT/ --descriptive --distribution --auto
  python stat_analysis.py --path data/indicators/parquet/specific_file.parquet --descriptive --transform
  python stat_analysis.py --path data/fixed/ --recursive --descriptive --distribution --transform --auto
  
  # Analysis options:
  python stat_analysis.py -f data.parquet --descriptive
  python stat_analysis.py -f data.parquet --distribution
  python stat_analysis.py -f data.parquet --transform
  python stat_analysis.py -f data.parquet --descriptive --distribution --transform --auto
  
  # Output options:
  python stat_analysis.py -f data.parquet --descriptive --output results/
  python stat_analysis.py --batch-all --descriptive --output analysis_results/ --auto
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
            help="🧹 Process all files in data/fixed/ directory (cleaned data)"
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
        
        # Analysis options
        analysis_group = parser.add_argument_group('Analysis Options')
        analysis_group.add_argument(
            "--descriptive",
            action="store_true",
            help="📊 Perform descriptive statistics analysis (mean, median, std, percentiles, etc.)"
        )
        
        analysis_group.add_argument(
            "--distribution",
            action="store_true",
            help="📈 Perform distribution analysis (normality tests, skewness, kurtosis)"
        )
        
        analysis_group.add_argument(
            "--transform",
            action="store_true",
            help="🔄 Perform data transformation analysis and recommendations"
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
            version="📊 Statistical Analysis Tool v1.0.0 🚀"
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
        if not any(config['analysis_options'].values()):
            print("❌ Error: At least one analysis option must be selected (--descriptive, --distribution, --transform)")
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
            'descriptive': getattr(args, 'descriptive', False),
            'distribution': getattr(args, 'distribution', False),
            'transform': getattr(args, 'transform', False)
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
        print("   It is recommended to use already cleaned data from data/fixed/ folder.")
        print("   You can run clear_data.py --help for more information about data cleaning.")
        print()
        print("📊 ANALYSIS COMBINATIONS:")
        print("   --descriptive                    : Basic statistics only")
        print("   --distribution                   : Distribution analysis only")
        print("   --transform                      : Transformation analysis only")
        print("   --descriptive --distribution     : Basic + distribution analysis")
        print("   --descriptive --transform        : Basic + transformation analysis")
        print("   --distribution --transform       : Distribution + transformation analysis")
        print("   --descriptive --distribution --transform : Complete analysis")
        print()
        print("📁 BATCH PROCESSING:")
        print("   --batch-fixed --auto             : Process all cleaned data automatically")
        print("   --batch-all --descriptive --auto : Process all data with basic stats")
        print("   --path data/fixed/ --recursive   : Process all files recursively")
        print()
        print("💾 OUTPUT OPTIONS:")
        print("   --output results/                : Save results to results/ directory")
        print("   --output analysis_2024/          : Save results to analysis_2024/ directory")
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
        print(ColorUtils.blue("ANALYSIS CONFIGURATION"))
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
        if analysis_options['descriptive']:
            print(f"  {ColorUtils.green('✅ Descriptive Statistics')}")
        if analysis_options['distribution']:
            print(f"  {ColorUtils.green('✅ Distribution Analysis')}")
        if analysis_options['transform']:
            print(f"  {ColorUtils.green('✅ Data Transformation')}")
        
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
            proceed = self.get_user_input("\n🚀 Proceed with analysis? (y/n): ", auto_mode)
            if proceed in ['y', 'n']:
                break
            print("⚠️  Please enter 'y' or 'n'")
        
        return proceed == 'y'
