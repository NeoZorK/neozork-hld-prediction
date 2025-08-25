# src/data/csv_folder_processor.py

"""
CSV folder processing module for batch processing multiple CSV files.
Includes progress bars with ETA and file information.
All comments are in English.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd
from tqdm import tqdm
import traceback

from src.common.logger import print_info, print_warning, print_error, print_debug
from src.data.fetchers.csv_fetcher import fetch_csv_data


def get_csv_files_from_folder(folder_path: str, mask: Optional[str] = None) -> List[Path]:
    """
    Get all CSV files from the specified folder, optionally filtered by mask.
    
    Args:
        folder_path (str): Path to the folder containing CSV files
        mask (Optional[str]): Optional mask to filter files by name (case-insensitive)
        
    Returns:
        List[Path]: List of CSV file paths
    """
    folder = Path(folder_path).resolve()
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not folder.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Find all CSV files in the folder
    csv_files = list(folder.glob("*.csv"))
    
    if not csv_files:
        raise ValueError(f"No CSV files found in folder: {folder_path}")
    
    # Apply mask filter if provided
    if mask:
        mask_lower = mask.lower()
        csv_files = [f for f in csv_files if mask_lower in f.name.lower()]
        
        if not csv_files:
            raise ValueError(f"No CSV files found in folder '{folder_path}' matching mask '{mask}'")
    
    # Sort files by name for consistent processing order
    csv_files.sort(key=lambda x: x.name)
    
    return csv_files


def get_file_info(file_path: Path) -> Dict[str, any]:
    """
    Get file information including size and estimated processing time.
    
    Args:
        file_path (Path): Path to the CSV file
        
    Returns:
        Dict[str, any]: File information dictionary
    """
    try:
        stat = file_path.stat()
        size_bytes = stat.st_size
        size_mb = size_bytes / (1024 * 1024)
        
        # Estimate processing time based on file size
        # Rough estimate: 1MB = ~1 second processing time
        estimated_time = max(1.0, size_mb * 0.5)
        
        return {
            'path': file_path,
            'name': file_path.name,
            'size_bytes': size_bytes,
            'size_mb': size_mb,
            'estimated_time': estimated_time
        }
    except Exception as e:
        print_warning(f"Could not get file info for {file_path}: {e}")
        return {
            'path': file_path,
            'name': file_path.name,
            'size_bytes': 0,
            'size_mb': 0,
            'estimated_time': 1.0
        }


def process_csv_folder(
    folder_path: str,
    point_size: float,
    rule: str = 'OHLCV',
    draw_mode: Optional[str] = None,
    export_formats: Optional[List[str]] = None,
    mask: Optional[str] = None
) -> Dict[str, any]:
    """
    Process all CSV files in a folder with progress bars and ETA.
    
    Args:
        folder_path (str): Path to folder containing CSV files
        point_size (float): Point size for calculations
        rule (str): Trading rule to apply
        draw_mode (Optional[str]): Drawing mode for plots
        export_formats (Optional[List[str]]): List of export formats
        mask (Optional[str]): Optional mask to filter files by name (case-insensitive)
        
    Returns:
        Dict[str, any]: Processing results and statistics
    """
    start_time = time.time()
    
    # Get all CSV files (with optional mask filtering)
    try:
        csv_files = get_csv_files_from_folder(folder_path, mask)
    except Exception as e:
        print_error(f"Error getting CSV files: {e}")
        return {
            'success': False,
            'error': str(e),
            'files_processed': 0,
            'files_failed': 0,
            'total_time': 0
        }
    
    # Display file count with mask information
    if mask:
        print_info(f"Found {len(csv_files)} CSV files in folder '{folder_path}' matching mask '{mask}'")
    else:
        print_info(f"Found {len(csv_files)} CSV files in folder: {folder_path}")
    
    # Get file information for all files
    file_infos = []
    for file_path in csv_files:
        file_info = get_file_info(file_path)
        file_infos.append(file_info)
    
    # Calculate total estimated time
    total_estimated_time = sum(info['estimated_time'] for info in file_infos)
    total_size_mb = sum(info['size_mb'] for info in file_infos)
    
    print_info(f"Total estimated processing time: {total_estimated_time:.1f} seconds")
    print_info(f"Total data size: {total_size_mb:.1f} MB")
    
    # Initialize results
    results = {
        'success': True,
        'files_processed': 0,
        'files_failed': 0,
        'failed_files': [],
        'total_time': 0,
        'total_size_mb': total_size_mb,
        'file_results': []
    }
    
    # Create overall progress bar
    with tqdm(
        total=len(csv_files),
        desc="Processing CSV files",
        unit="file",
        position=0,
        leave=True
    ) as overall_pbar:
        
        for i, file_info in enumerate(file_infos):
            file_path = file_info['path']
            file_name = file_info['name']
            file_size_mb = file_info['size_mb']
            
            # Update overall progress bar description
            overall_pbar.set_description(f"Processing: {file_name[:30]}...")
            
            # Create file-specific progress bar
            with tqdm(
                total=1,
                desc=f"File {i+1}/{len(csv_files)}: {file_name}",
                unit="file",
                position=1,
                leave=False,
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
            ) as file_pbar:
                
                try:
                    file_start_time = time.time()
                    
                    # Process single CSV file
                    file_result = process_single_csv_file(
                        file_path=str(file_path),
                        point_size=point_size,
                        rule=rule,
                        draw_mode=draw_mode,
                        export_formats=export_formats
                    )
                    
                    file_end_time = time.time()
                    file_duration = file_end_time - file_start_time
                    
                    # Update file progress
                    file_pbar.update(1)
                    file_pbar.set_postfix({
                        'size': f"{file_size_mb:.1f}MB",
                        'time': f"{file_duration:.1f}s"
                    })
                    
                    # Store file result
                    file_result['file_name'] = file_name
                    file_result['file_size_mb'] = file_size_mb
                    file_result['processing_time'] = file_duration
                    results['file_results'].append(file_result)
                    
                    if file_result.get('success', False):
                        results['files_processed'] += 1
                        print_info(f"✅ Successfully processed: {file_name}")
                    else:
                        results['files_failed'] += 1
                        results['failed_files'].append(file_name)
                        print_warning(f"❌ Failed to process: {file_name}")
                    
                except Exception as e:
                    file_duration = time.time() - file_start_time
                    file_pbar.update(1)
                    file_pbar.set_postfix({
                        'size': f"{file_size_mb:.1f}MB",
                        'time': f"{file_duration:.1f}s",
                        'error': 'Failed'
                    })
                    
                    results['files_failed'] += 1
                    results['failed_files'].append(file_name)
                    print_error(f"❌ Error processing {file_name}: {e}")
                    print_debug(f"Traceback: {traceback.format_exc()}")
                
                # Update overall progress
                overall_pbar.update(1)
                overall_pbar.set_postfix({
                    'processed': results['files_processed'],
                    'failed': results['files_failed'],
                    'size': f"{total_size_mb:.1f}MB"
                })
    
    # Calculate total processing time
    total_time = time.time() - start_time
    results['total_time'] = total_time
    
    # Print summary
    print_info(f"\n📊 Processing Summary:")
    print_info(f"   Files processed: {results['files_processed']}")
    print_info(f"   Files failed: {results['files_failed']}")
    print_info(f"   Total time: {total_time:.1f} seconds")
    print_info(f"   Average time per file: {total_time/len(csv_files):.1f} seconds")
    
    if results['failed_files']:
        print_warning(f"   Failed files: {', '.join(results['failed_files'])}")
    
    return results


def process_single_csv_file(
    file_path: str,
    point_size: float,
    rule: str = 'OHLCV',
    draw_mode: Optional[str] = None,
    export_formats: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Process a single CSV file using the existing workflow.
    
    Args:
        file_path (str): Path to the CSV file
        point_size (float): Point size for calculations
        rule (str): Trading rule to apply
        draw_mode (Optional[str]): Drawing mode for plots
        export_formats (Optional[List[str]]): List of export formats
        
    Returns:
        Dict[str, any]: Processing result
    """
    try:
        # Create mock args object for the existing workflow
        class MockArgs:
            def __init__(self):
                self.mode = 'csv'
                self.csv_file = file_path
                self.csv_folder = None
                self.point = point_size
                self.rule = rule
                self.draw = draw_mode
                self.export_parquet = export_formats and 'parquet' in export_formats
                self.export_csv = export_formats and 'csv' in export_formats
                self.export_json = export_formats and 'json' in export_formats
                # Add missing attributes that data_acquisition expects
                self.ticker = None
                self.interval = 'D1'
                self.period = None
                self.start = None
                self.end = None
        
        args = MockArgs()
        
        # Import and run the workflow
        from src.workflow.workflow import run_indicator_workflow
        
        result = run_indicator_workflow(args)
        
        return {
            'success': result.get('success', False),
            'error': result.get('error_message'),
            'rows_processed': result.get('rows_count', 0),
            'columns_count': result.get('columns_count', 0),
            'data_size_mb': result.get('data_size_mb', 0)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'rows_processed': 0,
            'columns_count': 0,
            'data_size_mb': 0
        }
