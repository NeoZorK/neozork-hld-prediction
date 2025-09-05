# File: src/data/batch_csv_processor.py
# -*- coding: utf-8 -*-

"""
Batch CSV processing functionality for converting multiple CSV files in a folder.
All comments are in English.
"""
import os
import glob
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from src.common.logger import print_info, print_warning, print_error, print_success
from .fetchers.csv_fetcher import fetch_csv_data


def find_csv_files_in_folder(folder_path: str) -> List[str]:
    """
    Find all CSV files in the specified folder.
    
    Args:
        folder_path (str): Path to the folder containing CSV files
        
    Returns:
        List[str]: List of CSV file paths found in the folder
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print_error(f"Folder does not exist: {folder_path}")
        return []
    
    if not folder.is_dir():
        print_error(f"Path is not a directory: {folder_path}")
        return []
    
    # Find all CSV files in the folder (case insensitive)
    csv_patterns = ['*.csv', '*.CSV']
    csv_files = []
    
    for pattern in csv_patterns:
        csv_files.extend(glob.glob(str(folder / pattern)))
    
    # Sort files for consistent processing order
    csv_files.sort()
    
    print_info(f"Found {len(csv_files)} CSV files in folder: {folder_path}")
    for csv_file in csv_files:
        print_info(f"  - {Path(csv_file).name}")
    
    return csv_files


def process_csv_folder(args) -> Dict[str, Any]:
    """
    Process all CSV files in a folder and convert them to Parquet format.
    This function handles batch conversion of multiple CSV files.
    
    Args:
        args: Parsed command-line arguments containing csv_folder and point
        
    Returns:
        Dict[str, Any]: Results dictionary with processing metrics
    """
    results = {
        "success": True,
        "processed_files": 0,
        "successful_conversions": 0,
        "failed_conversions": 0,
        "total_files": 0,
        "error_messages": [],
        "converted_files": [],
        "failed_files": []
    }
    
    # Find all CSV files in the folder
    csv_files = find_csv_files_in_folder(args.csv_folder)
    
    if not csv_files:
        results["success"] = False
        results["error_messages"].append(f"No CSV files found in folder: {args.csv_folder}")
        return results
    
    results["total_files"] = len(csv_files)
    print_info(f"Starting batch conversion of {len(csv_files)} CSV files...")
    
    # Process each CSV file
    for csv_file in csv_files:
        results["processed_files"] += 1
        file_name = Path(csv_file).name
        
        try:
            print_info(f"Processing file {results['processed_files']}/{results['total_files']}: {file_name}")
            
            # Create a temporary args object for this file
            file_args = type('Args', (), {})()
            file_args.csv_file = csv_file
            file_args.point = args.point
            
            # Use the existing CSV fetcher to process the file
            # This will automatically handle Parquet caching
            csv_column_mapping = {
                'Open': 'Open,', 'High': 'High,', 'Low': 'Low,',
                'Close': 'Close,', 'Volume': 'TickVolume,'
            }
            csv_datetime_column = 'DateTime,'
            
            df = fetch_csv_data(
                file_path=csv_file,
                ohlc_columns=csv_column_mapping,
                datetime_column=csv_datetime_column,
                skiprows=1,
                separator=','
            )
            
            if df is not None and not df.empty:
                results["successful_conversions"] += 1
                results["converted_files"].append(file_name)
                print_success(f"Successfully converted: {file_name} ({len(df)} rows)")
            else:
                results["failed_conversions"] += 1
                results["failed_files"].append(file_name)
                error_msg = f"Failed to process CSV file: {file_name}"
                results["error_messages"].append(error_msg)
                print_error(error_msg)
                
        except Exception as e:
            results["failed_conversions"] += 1
            results["failed_files"].append(file_name)
            error_msg = f"Error processing {file_name}: {str(e)}"
            results["error_messages"].append(error_msg)
            print_error(error_msg)
    
    # Print summary
    print_info(f"\n--- Batch Conversion Summary ---")
    print_info(f"Total files processed: {results['processed_files']}")
    print_info(f"Successful conversions: {results['successful_conversions']}")
    print_info(f"Failed conversions: {results['failed_conversions']}")
    
    if results["converted_files"]:
        print_success(f"Successfully converted files:")
        for file_name in results["converted_files"]:
            print_success(f"  ✓ {file_name}")
    
    if results["failed_files"]:
        print_error(f"Failed to convert files:")
        for file_name in results["failed_files"]:
            print_error(f"  ✗ {file_name}")
    
    # Set overall success based on whether any files were successfully converted
    results["success"] = results["successful_conversions"] > 0
    
    return results
