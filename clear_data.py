#!/usr/bin/env python3
"""
Data Cleaning Tool for Financial Data

This script provides automated data cleaning for financial time series data
from multiple sources and formats. It supports parquet, JSON, and CSV formats
from various data sources including Binance, Polygon, and yfinance.

Usage:
    python clear_data.py -f <filename>

The filename must be from one of the supported data directories:
- data/cache/csv_converted/
- data/raw_parquet/
- data/indicators/parquet/
- data/indicators/json/
- data/indicators/csv/
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from data_cleaning.data_validator import DataValidator
from data_cleaning.file_operations import FileOperations
from data_cleaning.cleaning_procedures import CleaningProcedures
from data_cleaning.progress_tracker import ProgressTracker
from data_cleaning.reporting import CleaningReporter


class DataCleaningTool:
    """Main class for data cleaning operations."""
    
    def __init__(self):
        """Initialize the data cleaning tool."""
        self.validator = DataValidator()
        self.file_ops = FileOperations()
        self.cleaner = CleaningProcedures()
        self.progress = ProgressTracker()
        self.reporter = CleaningReporter()
        
        # Supported data directories
        self.supported_dirs = [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/"
        ]
    
    def validate_file_path(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Validate if the file exists in supported directories.
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Dictionary with file metadata if valid, None otherwise
        """
        return self.validator.validate_file_path(filename, self.supported_dirs)
    
    def display_file_info(self, file_info: Dict[str, Any]) -> None:
        """
        Display comprehensive file information.
        
        Args:
            file_info: Dictionary containing file metadata
        """
        print("\n" + "="*80)
        print("FILE INFORMATION")
        print("="*80)
        
        for key, value in file_info.items():
            if key == "file_path":
                print(f"File Path: {value}")
            elif key == "file_size":
                print(f"File Size: {value:,} bytes")
            elif key == "format":
                print(f"Format: {value.upper()}")
            elif key == "symbol":
                print(f"Symbol: {value}")
            elif key == "timeframe":
                print(f"Time Frame: {value}")
            elif key == "source":
                print(f"Source: {value}")
            elif key == "folder_source":
                print(f"Folder Source: {value}")
            elif key == "indicator":
                print(f"Indicator: {value}")
            elif key == "rows_count":
                print(f"Rows Count: {value:,}")
            elif key == "columns_count":
                print(f"Columns Count: {value}")
            elif key == "start_date":
                print(f"Start Date: {value}")
            elif key == "end_date":
                print(f"End Date: {value}")
            elif key == "datetime_format":
                print(f"DateTime Format: {value}")
        
        print("="*80)
    
    def display_cleaning_procedures(self) -> None:
        """Display information about cleaning procedures."""
        print("\n" + "="*80)
        print("AUTOMATIC DATA CLEANING PROCEDURES")
        print("="*80)
        print("The following procedures will be performed:")
        print("1. Time Series Gaps Detection")
        print("2. Duplicates Detection")
        print("3. NaN Values Detection")
        print("4. Zero Values Detection")
        print("5. Negative Values Detection")
        print("6. Infinity Values Detection")
        print("7. Outliers Detection")
        print("\nNote: For Zero and Negative values, please review carefully")
        print("as some financial data may legitimately contain these values.")
        print("="*80)
    
    def run_cleaning_procedures(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all cleaning procedures on the data.
        
        Args:
            file_info: Dictionary containing file metadata
            
        Returns:
            Dictionary with cleaning results
        """
        # Load data
        data = self.file_ops.load_data(file_info["file_path"], file_info["format"])
        
        cleaning_results = {
            "original_data": data,
            "cleaned_data": data.copy(),
            "procedures": {},
            "total_issues_found": 0,
            "total_issues_fixed": 0
        }
        
        procedures = [
            ("gaps", "Time Series Gaps", self.cleaner.detect_gaps),
            ("duplicates", "Duplicates", self.cleaner.detect_duplicates),
            ("nan", "NaN Values", self.cleaner.detect_nan),
            ("zeros", "Zero Values", self.cleaner.detect_zeros),
            ("negative", "Negative Values", self.cleaner.detect_negative),
            ("infinity", "Infinity Values", self.cleaner.detect_infinity),
            ("outliers", "Outliers", self.cleaner.detect_outliers)
        ]
        
        for proc_id, proc_name, proc_func in procedures:
            print(f"\n--- {proc_name} Detection ---")
            
            # Run detection with progress bar
            def detect_wrapper(*args, **kwargs):
                return proc_func(data)
            
            issues = self.progress.run_with_progress(
                detect_wrapper, 
                f"Detecting {proc_name.lower()}"
            )
            
            if issues is not None and len(issues) > 0:
                print(f"\nFound {len(issues):,} {proc_name.lower()}")
                
                # Show detailed results
                self.reporter.show_detailed_results(proc_name, issues, data)
                
                # Ask user for action
                while True:
                    action = input(f"\nFix {proc_name.lower()} automatically? (y/n): ").lower().strip()
                    if action in ['y', 'n']:
                        break
                    print("Please enter 'y' or 'n'")
                
                if action == 'y':
                    # Fix issues
                    def fix_wrapper(*args, **kwargs):
                        return self.cleaner.fix_issues(data, proc_id, issues)
                    
                    fixed_data = self.progress.run_with_progress(
                        fix_wrapper,
                        f"Fixing {proc_name.lower()}"
                    )
                    
                    if fixed_data is not None:
                        data = fixed_data
                        cleaning_results["procedures"][proc_id] = {
                            "issues_found": len(issues),
                            "issues_fixed": len(issues),
                            "status": "fixed"
                        }
                        cleaning_results["total_issues_fixed"] += len(issues)
                    else:
                        cleaning_results["procedures"][proc_id] = {
                            "issues_found": len(issues),
                            "issues_fixed": 0,
                            "status": "failed"
                        }
                else:
                    cleaning_results["procedures"][proc_id] = {
                        "issues_found": len(issues),
                        "issues_fixed": 0,
                        "status": "skipped"
                    }
                
                cleaning_results["total_issues_found"] += len(issues)
            else:
                print(f"No {proc_name.lower()} found")
                cleaning_results["procedures"][proc_id] = {
                    "issues_found": 0,
                    "issues_fixed": 0,
                    "status": "clean"
                }
        
        cleaning_results["cleaned_data"] = data
        return cleaning_results
    
    def save_cleaned_data(self, file_info: Dict[str, Any], cleaning_results: Dict[str, Any]) -> str:
        """
        Save cleaned data to the specified path structure.
        
        Args:
            file_info: Original file metadata
            cleaning_results: Results from cleaning procedures
            
        Returns:
            Path where data was saved
        """
        # Create path structure: data/fixed/<source>/<format>/<symbol>/<indicator>/<timeframe>/
        source = file_info.get("source", "unknown")
        format_type = file_info["format"]
        symbol = file_info.get("symbol", "unknown")
        indicator = file_info.get("indicator", "unknown")
        timeframe = file_info.get("timeframe", "unknown")
        
        save_path = f"data/fixed/{source}/{format_type}/{symbol}/{indicator}/{timeframe}/"
        
        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Generate filename
        filename = f"{symbol}_{timeframe}_{indicator}_cleaned.{format_type}"
        full_path = os.path.join(save_path, filename)
        
        # Save data
        self.file_ops.save_data(cleaning_results["cleaned_data"], full_path, format_type)
        
        return full_path
    
    def run(self, filename: str) -> None:
        """
        Main execution method.
        
        Args:
            filename: Name of the file to process
        """
        try:
            # Validate file
            print(f"Validating file: {filename}")
            file_info = self.validate_file_path(filename)
            
            if file_info is None:
                print(f"\nError: Invalid file '{filename}'")
                print("Please choose a file from one of the supported directories:")
                for directory in self.supported_dirs:
                    print(f"  - {directory}")
                return
            
            # Display file information
            self.display_file_info(file_info)
            
            # Display cleaning procedures
            self.display_cleaning_procedures()
            
            # Ask for confirmation
            while True:
                proceed = input("\nProceed with cleaning? (y/n): ").lower().strip()
                if proceed in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if proceed != 'y':
                print("Cleaning cancelled.")
                return
            
            # Run cleaning procedures
            print("\nStarting data cleaning procedures...")
            cleaning_results = self.run_cleaning_procedures(file_info)
            
            # Display final report
            self.reporter.show_final_report(file_info, cleaning_results)
            
            # Ask to save
            while True:
                save = input("\nSave cleaned data? (y/n): ").lower().strip()
                if save in ['y', 'n']:
                    break
                print("Please enter 'y' or 'n'")
            
            if save == 'y':
                save_path = self.save_cleaned_data(file_info, cleaning_results)
                print(f"\nCleaned data saved to: {save_path}")
            else:
                print("Data not saved.")
            
            print("\nData cleaning completed successfully!")
            
        except Exception as e:
            print(f"\nError during data cleaning: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Data Cleaning Tool for Financial Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python clear_data.py -f GBPUSD_PERIOD_MN1.parquet
  python clear_data.py -f binance_BTCUSD_1h.parquet
  python clear_data.py -f polygon_ETHUSD_daily_rsi.json
        """
    )
    
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="Name of the file to clean (must be from supported directories)"
    )
    
    args = parser.parse_args()
    
    # Create and run the cleaning tool
    tool = DataCleaningTool()
    tool.run(args.file)


if __name__ == "__main__":
    main()
