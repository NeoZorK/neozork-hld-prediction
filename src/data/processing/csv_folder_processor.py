# -*- coding: utf-8 -*-
# src/data/processing/csv_folder_processor.py

"""
CSV folder processing functionality.
Handles processing of multiple CSV files in a folder.
All comments are in English.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import glob
import time
from tqdm import tqdm

from .csv_processor import CSVProcessor


def process_csv_folder(folder_path: str, point_size: Optional[float] = None,
                      rule: str = 'OHLCV', draw_mode: Optional[str] = None,
                      export_formats: Optional[List[str]] = None,
                      mask: Optional[str] = None) -> Dict[str, Any]:
    """
    Process all CSV files in a folder.
    
    Args:
        folder_path: Path to the folder containing CSV files
        point_size: Point size for price calculations
        rule: Rule for data processing
        draw_mode: Drawing mode for visualization
        export_formats: List of export formats
        mask: File mask pattern
        
    Returns:
        Dictionary with processing results
    """
    processor = CSVFolderProcessor()
    return processor.process_folder(
        folder_path, point_size, rule, draw_mode, export_formats, mask
    )


class CSVFolderProcessor:
    """Processes multiple CSV files in a folder."""
    
    def __init__(self):
        """Initialize the CSV folder processor."""
        self.csv_processor = CSVProcessor()
    
    def process_folder(self, folder_path: str, point_size: Optional[float] = None,
                      rule: str = 'OHLCV', draw_mode: Optional[str] = None,
                      export_formats: Optional[List[str]] = None,
                      mask: Optional[str] = None) -> Dict[str, Any]:
        """
        Process all files in a folder.
        
        Args:
            folder_path: Path to the folder
            point_size: Point size for calculations
            rule: Processing rule
            draw_mode: Drawing mode
            export_formats: Export formats
            mask: File mask pattern
            
        Returns:
            Dictionary with processing results
        """
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            return {
                'success': False,
                'error': f'Folder does not exist: {folder_path}',
                'files_processed': 0,
                'files_failed': 0,
                'total_time': 0
            }
        
        # Find CSV files
        csv_files = self._find_csv_files(folder_path, mask)
        
        if not csv_files:
            return {
                'success': False,
                'error': f'No CSV files found in {folder_path}',
                'files_processed': 0,
                'files_failed': 0,
                'total_time': 0
            }
        
        print(f"📁 Processing {len(csv_files)} CSV files in {folder_path}")
        
        # Process files
        start_time = time.time()
        results = self._process_files(csv_files, point_size, rule, draw_mode, export_formats)
        total_time = time.time() - start_time
        
        # Calculate summary statistics
        total_size_mb = sum(result.get('file_size_mb', 0) for result in results.values())
        
        summary = {
            'success': True,
            'folder_path': str(folder_path),
            'files_processed': len([r for r in results.values() if r['success']]),
            'files_failed': len([r for r in results.values() if not r['success']]),
            'total_time': total_time,
            'total_size_mb': total_size_mb,
            'processing_results': results
        }
        
        print(f"✅ Folder processing completed: {summary['files_processed']} successful, {summary['files_failed']} failed")
        print(f"⏱️  Total time: {total_time:.2f} seconds")
        
        return summary
    
    def _find_csv_files(self, folder_path: Path, mask: Optional[str] = None) -> List[Path]:
        """Find CSV files in the folder."""
        csv_files = []
        
        if mask:
            # Use custom mask pattern
            pattern = folder_path / mask
            csv_files.extend(glob.glob(str(pattern)))
        else:
            # Find all CSV files
            for file_path in folder_path.iterdir():
                if file_path.is_file() and file_path.suffix.lower() == '.csv':
                    csv_files.append(file_path)
        
        # Convert to Path objects and sort
        csv_files = [Path(f) for f in csv_files]
        csv_files.sort()
        
        return csv_files
    
    def _process_files(self, csv_files: List[Path], point_size: Optional[float],
                      rule: str, draw_mode: Optional[str], 
                      export_formats: Optional[List[str]]) -> Dict[str, Dict[str, Any]]:
        """Process individual CSV files."""
        results = {}
        
        for csv_file in tqdm(csv_files, desc="Processing CSV files"):
            try:
                # Use CSVProcessor to process individual files
                result = self.csv_processor.process_file(
                    csv_file, point_size, rule, draw_mode, export_formats
                )
                results[str(csv_file)] = result
            except Exception as e:
                results[str(csv_file)] = {
                    'success': False,
                    'error': str(e),
                    'file_size_mb': 0
                }
        
        return results
