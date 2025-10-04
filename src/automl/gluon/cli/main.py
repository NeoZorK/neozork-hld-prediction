"""
Main CLI interface for SCHR Levels AutoML

Provides flexible command-line control with comprehensive flags.
"""

import argparse
import sys
import os
from typing import List, Optional
from .commands import (
    TrainCommand,
    PredictCommand,
    BacktestCommand, 
    ValidateCommand,
    WebCommand
)


class SCHRCLI:
    """Main CLI controller for SCHR Levels AutoML"""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.commands = {
            'train': TrainCommand(),
            'predict': PredictCommand(),
            'backtest': BacktestCommand(),
            'validate': ValidateCommand(),
            'web': WebCommand()
        }
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create main argument parser with all CLI flags"""
        parser = argparse.ArgumentParser(
            prog='schr-gluon',
            description='SCHR Levels AutoML - Flexible Financial Analysis Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Train all models with custom settings
  schr-gluon train --symbol BTCUSD --timeframe MN1 --time-limit 3600 --tasks all
  
  # Quick prediction with web visualization
  schr-gluon predict --symbol BTCUSD --timeframe MN1 --web --browser
  
  # Comprehensive backtest with custom parameters
  schr-gluon backtest --symbol BTCUSD --timeframe MN1 --start-date 2020-01-01 --end-date 2024-01-01 --web
  
  # Walk-forward validation with visualization
  schr-gluon validate --type walk-forward --symbol BTCUSD --timeframe MN1 --splits 5 --web
  
  # Monte Carlo validation
  schr-gluon validate --type monte-carlo --symbol BTCUSD --timeframe MN1 --iterations 50 --web
  
  # Launch web dashboard
  schr-gluon web --port 8080 --host 0.0.0.0 --browser
            """
        )
        
        # Global options
        parser.add_argument('--verbose', '-v', action='store_true', 
                          help='Enable verbose logging')
        parser.add_argument('--quiet', '-q', action='store_true',
                          help='Suppress output except errors')
        parser.add_argument('--config', '-c', type=str,
                          help='Path to configuration file')
        parser.add_argument('--output-dir', '-o', type=str, default='results',
                          help='Output directory for results')
        parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                          default='INFO', help='Logging level')
        
        # Data options
        parser.add_argument('--data-path', type=str, default='data/cache/csv_converted/',
                          help='Path to data directory')
        parser.add_argument('--symbol', type=str, default='BTCUSD',
                          help='Trading symbol (BTCUSD, ETHUSD, EURUSD, etc.)')
        parser.add_argument('--timeframe', type=str, default='MN1',
                          choices=['MN1', 'W1', 'D1', 'H4', 'H1', 'M15', 'M5', 'M1'],
                          help='Timeframe for analysis')
        
        # Model options
        parser.add_argument('--tasks', type=str, nargs='+', 
                          choices=['pressure_vector_sign', 'price_direction_1period', 'level_breakout', 'all'],
                          default=['all'], help='ML tasks to run')
        parser.add_argument('--time-limit', type=int, default=1800,
                          help='Training time limit in seconds')
        parser.add_argument('--presets', type=str, default='best_quality',
                          choices=['best_quality', 'high_quality', 'good_quality', 'medium_quality'],
                          help='AutoGluon presets')
        parser.add_argument('--exclude-models', type=str, nargs='+',
                          help='Models to exclude (NN_TORCH, FASTAI, etc.)')
        
        # Validation options
        parser.add_argument('--test-size', type=float, default=0.2,
                          help='Test set size (0.0-1.0)')
        parser.add_argument('--cv-folds', type=int, default=5,
                          help='Cross-validation folds')
        parser.add_argument('--random-state', type=int, default=42,
                          help='Random state for reproducibility')
        
        # Web and visualization options
        parser.add_argument('--web', action='store_true',
                          help='Enable web visualization')
        parser.add_argument('--browser', action='store_true',
                          help='Open browser automatically')
        parser.add_argument('--port', type=int, default=8080,
                          help='Web server port')
        parser.add_argument('--host', type=str, default='127.0.0.1',
                          help='Web server host')
        parser.add_argument('--theme', type=str, default='dark',
                          choices=['dark', 'light'], help='Dashboard theme')
        
        # Backtest options
        parser.add_argument('--start-date', type=str,
                          help='Backtest start date (YYYY-MM-DD)')
        parser.add_argument('--end-date', type=str,
                          help='Backtest end date (YYYY-MM-DD)')
        parser.add_argument('--initial-capital', type=float, default=10000,
                          help='Initial capital for backtesting')
        parser.add_argument('--commission', type=float, default=0.001,
                          help='Trading commission rate')
        
        # Validation specific options
        parser.add_argument('--type', type=str, choices=['walk-forward', 'monte-carlo', 'cross-validation'],
                          help='Validation type')
        parser.add_argument('--splits', type=int, default=5,
                          help='Number of splits for walk-forward')
        parser.add_argument('--iterations', type=int, default=20,
                          help='Number of Monte Carlo iterations')
        
        # Performance options
        parser.add_argument('--n-jobs', type=int, default=-1,
                          help='Number of parallel jobs (-1 for all cores)')
        parser.add_argument('--memory-limit', type=str,
                          help='Memory limit for training')
        parser.add_argument('--gpu', action='store_true',
                          help='Enable GPU acceleration')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Train command
        train_parser = subparsers.add_parser('train', help='Train ML models')
        train_parser.add_argument('--force-retrain', action='store_true',
                                help='Force retraining even if models exist')
        
        # Predict command  
        predict_parser = subparsers.add_parser('predict', help='Make predictions')
        predict_parser.add_argument('--model-path', type=str,
                                  help='Path to trained model')
        predict_parser.add_argument('--save-predictions', action='store_true',
                                  help='Save predictions to file')
        
        # Backtest command
        backtest_parser = subparsers.add_parser('backtest', help='Run backtesting')
        backtest_parser.add_argument('--strategy', type=str, default='simple',
                                   choices=['simple', 'advanced', 'ensemble'],
                                   help='Backtesting strategy')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Run validation')
        validate_parser.add_argument('--save-results', action='store_true',
                                  help='Save validation results')
        
        # Web command
        web_parser = subparsers.add_parser('web', help='Launch web dashboard')
        web_parser.add_argument('--auto-refresh', type=int, default=30,
                              help='Auto-refresh interval in seconds')
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run CLI with given arguments"""
        try:
            parsed_args = self.parser.parse_args(args)
            
            if not parsed_args.command:
                self.parser.print_help()
                return 1
            
            # Set up logging
            self._setup_logging(parsed_args)
            
            # Execute command
            command = self.commands.get(parsed_args.command)
            if not command:
                print(f"Unknown command: {parsed_args.command}")
                return 1
            
            return command.execute(parsed_args)
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 130
        except Exception as e:
            print(f"Error: {e}")
            if parsed_args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    def _setup_logging(self, args):
        """Setup logging configuration"""
        import logging
        
        level = getattr(logging, args.log_level)
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        if args.quiet:
            logging.getLogger().setLevel(logging.ERROR)


def main():
    """Main entry point for CLI"""
    cli = SCHRCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
