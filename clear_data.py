#!/usr/bin/env python3
"""
🧹 Data Cleaning Tool for Financial Data 🚀

This script provides automated data cleaning for financial time series data
from multiple sources and formats. It supports parquet, JSON, and CSV formats
from various data sources including Binance, Polygon, and yfinance.

Usage:
    # Single file processing:
    python clear_data.py -f <filename> [--auto]
    
    # Batch processing by directory:
    python clear_data.py --batch-raw-parquet [--auto]
    python clear_data.py --batch-csv-converted [--auto]
    python clear_data.py --batch-indicators-parquet [--auto]
    python clear_data.py --batch-indicators-json [--auto]
    python clear_data.py --batch-indicators-csv [--auto]
    python clear_data.py --batch-all [--auto]

The filename must be from one of the supported data directories:
- data/cache/csv_converted/
- data/raw_parquet/
- data/indicators/parquet/
- data/indicators/json/
- data/indicators/csv/

Options:
    --auto    Automatically answer 'y' to all questions (non-interactive mode)
    --version Show version information
"""

__version__ = "1.0.0"

import argparse
import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from data_cleaning.data_validator import DataValidator
from data_cleaning.file_operations import FileOperations
from data_cleaning.cleaning_procedures import CleaningProcedures
from data_cleaning.progress_tracker import ProgressTracker
from data_cleaning.reporting import CleaningReporter


class DataCleaningTool:
    """Main class for data cleaning operations."""
    
    def __init__(self, auto_mode: bool = False, skip_zero_columns: List[str] = None, skip_negative_columns: List[str] = None):
        """Initialize the data cleaning tool.
        
        Args:
            auto_mode: If True, automatically answer 'y' to all questions
            skip_zero_columns: List of column names to skip for zero value cleaning
            skip_negative_columns: List of column names to skip for negative value cleaning
        """
        self.validator = DataValidator()
        self.file_ops = FileOperations()
        self.cleaner = CleaningProcedures()
        self.progress = ProgressTracker()
        self.reporter = CleaningReporter()
        self.auto_mode = auto_mode
        self.skip_zero_columns = skip_zero_columns or []
        self.skip_negative_columns = skip_negative_columns or []
        
        # Supported data directories
        self.supported_dirs = [
            "data/cache/csv_converted/",
            "data/raw_parquet/",
            "data/indicators/parquet/",
            "data/indicators/json/",
            "data/indicators/csv/"
        ]
    
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
    
    def _calculate_issue_count(self, issues: List[Dict[str, Any]], proc_id: str) -> int:
        """
        Calculate the actual count of issues based on the procedure type.
        
        Args:
            issues: List of issues found
            proc_id: Procedure identifier
            
        Returns:
            Actual count of issues
        """
        if not issues:
            return 0
        
        if proc_id == "outliers":
            # For outliers, sum up all outliers across all methods and columns
            total_count = 0
            for col_outliers in issues:
                if 'methods' in col_outliers:
                    for method, data in col_outliers['methods'].items():
                        total_count += data['count']
            return total_count
        elif proc_id in ["zeros", "negative", "infinity", "nan"]:
            # For these, sum up the count from each column
            return sum(issue['count'] for issue in issues)
        elif proc_id == "duplicates":
            # For duplicates, sum up the total duplicate rows
            return sum(dup['count'] for dup in issues)
        else:
            # For gaps and others, use the length
            return len(issues)
    
    def get_files_in_directory(self, directory: str) -> List[str]:
        """
        Get all supported files in a directory.
        
        Args:
            directory: Directory path to scan
            
        Returns:
            List of filenames in the directory
        """
        if not os.path.exists(directory):
            return []
        
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                # Check if file has supported format
                if any(file.lower().endswith(ext) for ext in ['.parquet', '.json', '.csv']):
                    files.append(file)
        
        return sorted(files)
    
    def run_batch_processing(self, directory: str, directory_name: str) -> None:
        """
        Run batch processing for all files in a directory.
        
        Args:
            directory: Directory path to process
            directory_name: Human-readable directory name for display
        """
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING: {directory_name}")
        print(f"Directory: {directory}")
        print(f"{'='*80}")
        
        files = self.get_files_in_directory(directory)
        
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
                self.run(filename)
                successful += 1
                print(f"✅ Successfully processed: {filename}")
            except Exception as e:
                failed += 1
                print(f"❌ Failed to process {filename}: {str(e)}")
        
        # Summary
        print(f"\n{'='*80}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"Total files: {len(files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/len(files)*100):.1f}%")
    
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
            
            # Run detection with detailed progress bar
            def detect_wrapper(*args, **kwargs):
                return proc_func(data)
            
            issues = self.progress.run_detailed_progress(
                detect_wrapper, 
                data,
                f"Detecting {proc_name.lower()}"
            )
            
            if issues is not None and len(issues) > 0:
                # Filter out skipped columns for zeros and negative values
                if proc_id == 'zeros' and self.skip_zero_columns:
                    issues = [issue for issue in issues if issue['column'] not in self.skip_zero_columns]
                    if self.skip_zero_columns:
                        print(f"\n🚫 Skipping zero value cleaning for columns: {', '.join(self.skip_zero_columns)}")
                
                if proc_id == 'negative' and self.skip_negative_columns:
                    issues = [issue for issue in issues if issue['column'] not in self.skip_negative_columns]
                    if self.skip_negative_columns:
                        print(f"\n🚫 Skipping negative value cleaning for columns: {', '.join(self.skip_negative_columns)}")
                
                # Show detailed results (this will also show the count)
                self.reporter.show_detailed_results(proc_name, issues, data)
                
                # Special handling for zero and negative values - column by column choice
                if proc_id in ['zeros', 'negative']:
                    if self.auto_mode:
                        # In auto mode, fix all issues (already filtered)
                        issues_to_fix = issues
                        print(f"\nAuto mode: Fixing all {proc_name.lower()} in all columns")
                    else:
                        # Interactive mode: ask for each column
                        issues_to_fix = self.reporter.show_column_choice_prompt(issues, proc_id)
                else:
                    # For other procedures, ask once for all
                    while True:
                        action = self._get_user_input(f"\nFix {proc_name.lower()} automatically? (y/n): ")
                        if action in ['y', 'n']:
                            break
                        print("Please enter 'y' or 'n'")
                    
                    issues_to_fix = issues if action == 'y' else []
                
                if issues_to_fix:
                    # Fix issues
                    def fix_wrapper(*args, **kwargs):
                        return self.cleaner.fix_issues(data, proc_id, issues_to_fix)
                    
                    fixed_data = self.progress.run_detailed_progress(
                        fix_wrapper,
                        data,
                        f"Fixing {proc_name.lower()}"
                    )
                    
                    if fixed_data is not None:
                        data = fixed_data
                        # Calculate actual count of issues
                        total_issues_found = self._calculate_issue_count(issues, proc_id)
                        issues_fixed = self._calculate_issue_count(issues_to_fix, proc_id)
                        cleaning_results["procedures"][proc_id] = {
                            "issues_found": total_issues_found,
                            "issues_fixed": issues_fixed,
                            "status": "fixed" if issues_fixed > 0 else "skipped"
                        }
                        cleaning_results["total_issues_fixed"] += issues_fixed
                    else:
                        total_issues_found = self._calculate_issue_count(issues, proc_id)
                        cleaning_results["procedures"][proc_id] = {
                            "issues_found": total_issues_found,
                            "issues_fixed": 0,
                            "status": "failed"
                        }
                else:
                    actual_count = self._calculate_issue_count(issues, proc_id)
                    cleaning_results["procedures"][proc_id] = {
                        "issues_found": actual_count,
                        "issues_fixed": 0,
                        "status": "skipped"
                    }
                
                # Calculate total issues found for this procedure
                total_issues_found = self._calculate_issue_count(issues, proc_id)
                cleaning_results["total_issues_found"] += total_issues_found
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
            print(f"🔍 Validating file: {filename}")
            file_info = self.validate_file_path(filename)
            
            if file_info is None:
                print(f"\n❌ Error: Invalid file '{filename}'")
                print("📁 Please choose a file from one of the supported directories:")
                for directory in self.supported_dirs:
                    print(f"  - {directory}")
                return
            
            # Display file information
            self.display_file_info(file_info)
            
            # Display cleaning procedures
            self.display_cleaning_procedures()
            
            # Ask for confirmation
            while True:
                proceed = self._get_user_input("\n🚀 Proceed with cleaning? (y/n): ")
                if proceed in ['y', 'n']:
                    break
                print("⚠️  Please enter 'y' or 'n'")
            
            if proceed != 'y':
                print("❌ Cleaning cancelled.")
                return
            
            # Run cleaning procedures
            print("\n🧹 Starting data cleaning procedures...")
            cleaning_results = self.run_cleaning_procedures(file_info)
            
            # Display final report
            self.reporter.show_final_report(file_info, cleaning_results)
            
            # Ask to save
            while True:
                save = self._get_user_input("\n💾 Save cleaned data? (y/n): ")
                if save in ['y', 'n']:
                    break
                print("⚠️  Please enter 'y' or 'n'")
            
            if save == 'y':
                save_path = self.save_cleaned_data(file_info, cleaning_results)
                print(f"\n✅ Cleaned data saved to: {save_path}")
            else:
                print("💾 Data not saved.")
            
            print("\n🎉 Data cleaning completed successfully!")
            
        except Exception as e:
            print(f"\nError during data cleaning: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="🧹 Data Cleaning Tool for Financial Data 🚀",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file processing:
  python clear_data.py -f GBPUSD_PERIOD_MN1.parquet
  python clear_data.py -f binance_BTCUSD_1h.parquet
  python clear_data.py -f polygon_ETHUSD_daily_rsi.json
  python clear_data.py -f binance_BTCUSDT_MN1.parquet --auto
  
  # Skip specific columns:
  python clear_data.py -f data.parquet --skip-zero "Volume,Price" --skip-negative "Returns,Changes"
  python clear_data.py -f data.parquet --auto --skip-zero "Volume" --skip-negative "Returns"
  
  # Batch processing:
  python clear_data.py --batch-raw-parquet --auto
  python clear_data.py --batch-csv-converted --auto --skip-zero "Volume"
  python clear_data.py --batch-indicators-json --auto --skip-negative "Returns,Changes"
  python clear_data.py --batch-all --auto --skip-zero "Volume,Price" --skip-negative "Returns"
        """
    )
    
    # File processing group
    file_group = parser.add_mutually_exclusive_group(required=True)
    file_group.add_argument(
        "-f", "--file",
        help="📁 Name of the file to clean (must be from supported directories)"
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
        "--batch-all",
        action="store_true",
        help="🌟 Process all files in all supported directories"
    )
    
    parser.add_argument(
        "--auto",
        action="store_true",
        help="🤖 Automatically answer 'y' to all questions (non-interactive mode)"
    )
    
    parser.add_argument(
        "--skip-zero",
        type=str,
        help="🚫 Skip zero value cleaning for specified columns (comma-separated list, e.g., 'Volume,Price')"
    )
    
    parser.add_argument(
        "--skip-negative",
        type=str,
        help="🚫 Skip negative value cleaning for specified columns (comma-separated list, e.g., 'Returns,Changes')"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"🧹 Data Cleaning Tool v{__version__} 🚀"
    )
    
    args = parser.parse_args()
    
    # Start timing
    start_time = time.time()
    
    # Parse skip columns
    skip_zero_columns = []
    skip_negative_columns = []
    
    if args.skip_zero:
        skip_zero_columns = [col.strip() for col in args.skip_zero.split(',') if col.strip()]
    
    if args.skip_negative:
        skip_negative_columns = [col.strip() for col in args.skip_negative.split(',') if col.strip()]
    
    # Create the cleaning tool
    tool = DataCleaningTool(
        auto_mode=args.auto,
        skip_zero_columns=skip_zero_columns,
        skip_negative_columns=skip_negative_columns
    )
    
    # Determine processing mode
    if args.file:
        # Single file processing
        tool.run(args.file)
    elif args.batch_csv_converted:
        # Batch process CSV converted files
        tool.run_batch_processing("data/cache/csv_converted/", "CSV Converted Files")
    elif args.batch_raw_parquet:
        # Batch process raw parquet files
        tool.run_batch_processing("data/raw_parquet/", "Raw Parquet Files")
    elif args.batch_indicators_parquet:
        # Batch process indicators parquet files
        tool.run_batch_processing("data/indicators/parquet/", "Indicators Parquet Files")
    elif args.batch_indicators_json:
        # Batch process indicators JSON files
        tool.run_batch_processing("data/indicators/json/", "Indicators JSON Files")
    elif args.batch_indicators_csv:
        # Batch process indicators CSV files
        tool.run_batch_processing("data/indicators/csv/", "Indicators CSV Files")
    elif args.batch_all:
        # Batch process all directories
        directories = [
            ("data/cache/csv_converted/", "CSV Converted Files"),
            ("data/raw_parquet/", "Raw Parquet Files"),
            ("data/indicators/parquet/", "Indicators Parquet Files"),
            ("data/indicators/json/", "Indicators JSON Files"),
            ("data/indicators/csv/", "Indicators CSV Files")
        ]
        
        total_successful = 0
        total_failed = 0
        total_files = 0
        
        for directory, name in directories:
            if os.path.exists(directory):
                files = tool.get_files_in_directory(directory)
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
                            tool.run(filename)
                            total_successful += 1
                            print(f"✅ Successfully processed: {filename}")
                        except Exception as e:
                            total_failed += 1
                            print(f"❌ Failed to process {filename}: {str(e)}")
        
        # Overall summary
        print(f"\n{'='*100}")
        print(f"🌟 BATCH PROCESSING ALL DIRECTORIES COMPLETE 🌟")
        print(f"{'='*100}")
        print(f"📊 Total files processed: {total_files}")
        print(f"✅ Successful: {total_successful}")
        print(f"❌ Failed: {total_failed}")
        if total_files > 0:
            print(f"📈 Overall success rate: {(total_successful/total_files*100):.1f}%")
        else:
            print("⚠️  No files found to process.")
    
    # Calculate and display processing time
    end_time = time.time()
    processing_time = end_time - start_time
    
    print(f"\n⏱️  Processing completed in {processing_time:.2f} seconds")
    print(f"🎉 Data cleaning finished successfully!")


if __name__ == "__main__":
    main()
