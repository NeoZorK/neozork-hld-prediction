"""
Financial Analysis CLI Interface

This module handles command-line argument parsing and validation for the financial analysis tool.
It provides a comprehensive CLI interface following the same patterns as existing analysis tools.
"""

import argparse
import sys
import os
from typing import Dict, Any, Optional
from pathlib import Path


class FinanceCLI:
    """Handles CLI interface for financial analysis."""
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.version = "1.0.0"
    
    def parse_arguments(self) -> argparse.Namespace:
        """
        Parse command-line arguments.
        
        Returns:
            Parsed arguments namespace
        """
        parser = argparse.ArgumentParser(
            description="📊 Financial Analysis Tool for Financial Data 🚀",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Single file processing:
  python finance_analysis.py -f GBPUSD_PERIOD_MN1.parquet --ohlcv --volatility
  python finance_analysis.py -f binance_BTCUSD_1h.parquet --returns --drawdown
  python finance_analysis.py -f polygon_ETHUSD_daily_rsi.json --ohlcv --volatility --returns --drawdown --auto
  
  # Batch processing:
  python finance_analysis.py --batch-raw-parquet --ohlcv --volatility --auto
  python finance_analysis.py --batch-fixed --returns --drawdown --auto
  python finance_analysis.py --batch-all --ohlcv --volatility --returns --drawdown --auto
  
  # Custom directory processing:
  python finance_analysis.py --path data/custom_folder/ --ohlcv --volatility --auto
  python finance_analysis.py --path /path/to/data/ --returns --drawdown --auto
  
  # Single file with full path:
  python finance_analysis.py --path data/cache/csv_converted/CSVExport_AAPL.NAS_PERIOD_D1.parquet --ohlcv --auto
  python finance_analysis.py --path data/raw_parquet/binance_BTCUSDT_MN1.parquet --volatility --auto
  python finance_analysis.py --path /absolute/path/to/file.parquet --returns --drawdown --auto

Note: It is recommended to use already cleaned and transformed data by clear_data.py and 
stat_analysis.py and time_analysis.py from data/fixed/ folder. You can run clear_data.py --help for more information.
            """
        )
        
        # File processing group
        file_group = parser.add_mutually_exclusive_group(required=True)
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
            help="🧹 Process all files in data/fixed/ directory (recommended)"
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
            "--ohlcv",
            action="store_true",
            help="📊 Perform OHLCV data analysis (price validation, volume analysis, price-volume relationships)"
        )
        
        analysis_group.add_argument(
            "--volatility",
            action="store_true",
            help="📈 Perform volatility analysis (rolling volatility, GARCH models, volatility clustering)"
        )
        
        analysis_group.add_argument(
            "--returns",
            action="store_true",
            help="💰 Perform returns analysis (simple returns, log returns, cumulative returns)"
        )
        
        analysis_group.add_argument(
            "--drawdown",
            action="store_true",
            help="📉 Perform drawdown analysis (max drawdown, drawdown duration, recovery analysis)"
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
            help="🔄 Recursively search subdirectories when using --path"
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
        
        parser.add_argument(
            "--version",
            action="version",
            version=f"📊 Financial Analysis Tool v{self.version} 🚀"
        )
        
        return parser.parse_args()
    
    def validate_arguments(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        Validate parsed arguments and return configuration.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            Configuration dictionary
        """
        # Check if at least one analysis option is selected
        analysis_options = {
            'ohlcv': args.ohlcv,
            'volatility': args.volatility,
            'returns': args.returns,
            'drawdown': args.drawdown
        }
        
        if not any(analysis_options.values()):
            print("❌ Error: At least one analysis option must be selected.")
            print("Available options: --ohlcv, --volatility, --returns, --drawdown")
            sys.exit(1)
        
        # Determine file processing mode
        file_processing = self._determine_file_processing_mode(args)
        
        # Validate file processing configuration
        if not file_processing['valid']:
            print(f"❌ Error: {file_processing['error']}")
            sys.exit(1)
        
        return {
            'file_processing': file_processing,
            'analysis_options': analysis_options,
            'processing_options': {
                'auto': args.auto,
                'recursive': args.recursive,
                'verbose': args.verbose
            },
            'output_directory': args.output
        }
    
    def _determine_file_processing_mode(self, args: argparse.Namespace) -> Dict[str, Any]:
        """
        Determine file processing mode from arguments.
        
        Args:
            args: Parsed arguments namespace
            
        Returns:
            File processing configuration
        """
        if args.file:
            return {
                'mode': 'single_file',
                'filename': args.file,
                'valid': True
            }
        elif args.batch_csv_converted:
            return {
                'mode': 'batch',
                'directory': 'data/cache/csv_converted/',
                'valid': True
            }
        elif args.batch_raw_parquet:
            return {
                'mode': 'batch',
                'directory': 'data/raw_parquet/',
                'valid': True
            }
        elif args.batch_indicators_parquet:
            return {
                'mode': 'batch',
                'directory': 'data/indicators/parquet/',
                'valid': True
            }
        elif args.batch_indicators_json:
            return {
                'mode': 'batch',
                'directory': 'data/indicators/json/',
                'valid': True
            }
        elif args.batch_indicators_csv:
            return {
                'mode': 'batch',
                'directory': 'data/indicators/csv/',
                'valid': True
            }
        elif args.batch_fixed:
            return {
                'mode': 'batch',
                'directory': 'data/fixed/',
                'valid': True
            }
        elif args.batch_all:
            return {
                'mode': 'batch_all',
                'valid': True
            }
        elif args.path:
            if not os.path.exists(args.path):
                return {
                    'mode': 'custom_path',
                    'directory': args.path,
                    'valid': False,
                    'error': f"Path '{args.path}' does not exist"
                }
            return {
                'mode': 'custom_path',
                'directory': args.path,
                'valid': True
            }
        else:
            return {
                'mode': 'none',
                'valid': False,
                'error': 'No file processing mode specified'
            }
    
    def confirm_analysis(self, config: Dict[str, Any], auto_mode: bool = False) -> bool:
        """
        Confirm analysis configuration with user.
        
        Args:
            config: Analysis configuration
            auto_mode: Whether to skip confirmation
            
        Returns:
            True if confirmed, False otherwise
        """
        if auto_mode:
            return True
        
        print("\n" + "="*80)
        print("📊 FINANCIAL ANALYSIS CONFIGURATION")
        print("="*80)
        
        # Display file processing mode
        file_processing = config['file_processing']
        if file_processing['mode'] == 'single_file':
            print(f"📁 File: {file_processing['filename']}")
        elif file_processing['mode'] == 'batch':
            print(f"📂 Directory: {file_processing['directory']}")
        elif file_processing['mode'] == 'batch_all':
            print("🌟 All supported directories")
        elif file_processing['mode'] == 'custom_path':
            print(f"📂 Custom path: {file_processing['directory']}")
        
        # Display analysis options
        analysis_options = config['analysis_options']
        selected_analyses = [name for name, selected in analysis_options.items() if selected]
        
        print(f"\n📊 Selected Analyses:")
        for analysis in selected_analyses:
            if analysis == 'ohlcv':
                print("  • OHLCV Data Analysis (price validation, volume analysis, price-volume relationships)")
            elif analysis == 'volatility':
                print("  • Volatility Analysis (rolling volatility, GARCH models, volatility clustering)")
            elif analysis == 'returns':
                print("  • Returns Analysis (simple returns, log returns, cumulative returns)")
            elif analysis == 'drawdown':
                print("  • Drawdown Analysis (max drawdown, drawdown duration, recovery analysis)")
        
        # Display processing options
        processing_options = config['processing_options']
        if processing_options['auto']:
            print("\n🤖 Auto mode: Non-interactive processing")
        if processing_options['verbose']:
            print("📝 Verbose logging enabled")
        
        if config['output_directory']:
            print(f"📁 Output directory: {config['output_directory']}")
        
        print("\n" + "="*80)
        
        # Confirm with user
        while True:
            proceed = input("🚀 Proceed with financial analysis? (y/n): ").lower().strip()
            if proceed in ['y', 'n']:
                return proceed == 'y'
            print("⚠️  Please enter 'y' or 'n'")
    
    def display_help_examples(self):
        """Display detailed help examples."""
        print("\n" + "="*80)
        print("📊 FINANCIAL ANALYSIS TOOL - DETAILED EXAMPLES")
        print("="*80)
        
        print("\n🔍 ANALYSIS TYPES:")
        print("  --ohlcv     : OHLCV data analysis (price validation, volume analysis)")
        print("  --volatility: Volatility analysis (rolling volatility, GARCH models)")
        print("  --returns   : Returns analysis (simple returns, log returns, cumulative returns)")
        print("  --drawdown  : Drawdown analysis (max drawdown, drawdown duration, recovery)")
        
        print("\n📁 SUPPORTED DIRECTORIES:")
        print("  • data/cache/csv_converted/     - CSV converted files")
        print("  • data/raw_parquet/             - Raw parquet files")
        print("  • data/indicators/parquet/      - Indicators parquet files")
        print("  • data/indicators/json/         - Indicators JSON files")
        print("  • data/indicators/csv/          - Indicators CSV files")
        print("  • data/fixed/                   - Cleaned data (recommended)")
        
        print("\n🚀 EXAMPLE COMMANDS:")
        print("  # Basic financial analysis:")
        print("  python finance_analysis.py -f BTCUSDT_MN1.parquet --ohlcv --volatility --returns --drawdown")
        
        print("\n  # Batch processing with auto mode:")
        print("  python finance_analysis.py --batch-fixed --ohlcv --volatility --returns --drawdown --auto")
        
        print("\n  # Custom directory analysis:")
        print("  python finance_analysis.py --path data/custom/ --ohlcv --volatility --output results/")
        
        print("\n  # All analyses on all directories:")
        print("  python finance_analysis.py --batch-all --ohlcv --volatility --returns --drawdown --auto")
        
        print("\n💡 TIPS:")
        print("  • Use --auto for non-interactive processing")
        print("  • Use data/fixed/ directory for best results (cleaned data)")
        print("  • Combine multiple analysis types for comprehensive analysis")
        print("  • Use --output to save results to specific directory")
        
        print("="*80)
