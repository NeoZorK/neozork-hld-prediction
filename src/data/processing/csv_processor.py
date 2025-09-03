# -*- coding: utf-8 -*-
# src/../data/processing/csv_processor.py

"""
CSV file processing functionality.
Handles individual CSV file processing and data transformation.
All comments are in English.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class CSVProcessor:
    """Processes individual CSV files."""
    
    def __init__(self):
        """Initialize the CSV processor."""
        self.supported_formats = ['.csv', '.parquet', '.json']
        self.default_rule = 'OHLCV'
    
    def process_file(self, file_path: Path, point_size: Optional[float] = None,
                    rule: str = 'OHLCV', draw_mode: Optional[str] = None,
                    export_formats: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Process a single CSV file.
        
        Args:
            file_path: Path to the CSV file
            point_size: Point size for calculations
            rule: Processing rule
            draw_mode: Drawing mode
            export_formats: Export formats
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Load CSV file
            df = pd.read_csv(file_path)
            
            if df.empty:
                return {
                    'success': False,
                    'error': 'File is empty',
                    'file_size_mb': file_path.stat().st_size / (1024 * 1024)
                }
            
            # Process data according to rule
            processed_df = self._apply_processing_rule(df, rule, point_size)
            
            # Apply drawing mode if specified
            if draw_mode:
                processed_df = self._apply_drawing_mode(processed_df, draw_mode)
            
            # Export data if formats specified
            export_results = {}
            if export_formats:
                export_results = self._export_data(processed_df, file_path, export_formats)
            
            # Calculate file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            return {
                'success': True,
                'rows_processed': len(processed_df),
                'columns_processed': len(processed_df.columns),
                'file_size_mb': file_size_mb,
                'export_results': export_results,
                'processing_rule': rule
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'file_size_mb': file_path.stat().st_size / (1024 * 1024) if file_path.exists() else 0
            }
    
    def _apply_processing_rule(self, df: pd.DataFrame, rule: str, 
                              point_size: Optional[float]) -> pd.DataFrame:
        """Apply processing rule to the DataFrame."""
        processed_df = df.copy()
        
        if rule == 'OHLCV':
            processed_df = self._process_ohlcv_data(processed_df, point_size)
        elif rule == 'PRICE':
            processed_df = self._process_price_data(processed_df, point_size)
        elif rule == 'VOLUME':
            processed_df = self._process_volume_data(processed_df)
        else:
            # Default processing
            processed_df = self._process_default_data(processed_df)
        
        return processed_df
    
    def _process_ohlcv_data(self, df: pd.DataFrame, point_size: Optional[float]) -> pd.DataFrame:
        """Process OHLCV (Open, High, Low, Close, Volume) data."""
        processed_df = df.copy()
        
        # Standardize column names
        column_mapping = {
            'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume',
            'OPEN': 'open', 'HIGH': 'high', 'LOW': 'low', 'CLOSE': 'close', 'VOLUME': 'volume'
        }
        
        processed_df = processed_df.rename(columns=column_mapping)
        
        # Ensure required columns exist
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for col in required_columns:
            if col not in processed_df.columns:
                # Try to find similar columns
                similar_cols = [c for c in processed_df.columns if col in c.lower()]
                if similar_cols:
                    processed_df[col] = processed_df[similar_cols[0]]
                else:
                    # Create dummy column
                    processed_df[col] = 0
        
        # Apply point size if specified
        if point_size:
            for col in ['open', 'high', 'low', 'close']:
                if col in processed_df.columns:
                    processed_df[col] = processed_df[col] * point_size
        
        # Clean data
        processed_df = self._clean_ohlcv_data(processed_df)
        
        return processed_df
    
    def _process_price_data(self, df: pd.DataFrame, point_size: Optional[float]) -> pd.DataFrame:
        """Process price-only data."""
        processed_df = df.copy()
        
        # Find price column
        price_columns = [col for col in df.columns if 'price' in col.lower() or 'close' in col.lower()]
        
        if price_columns:
            price_col = price_columns[0]
            processed_df['price'] = processed_df[price_col]
            
            # Apply point size if specified
            if point_size:
                processed_df['price'] = processed_df['price'] * point_size
        else:
            # Assume first numeric column is price
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                processed_df['price'] = processed_df[numeric_cols[0]]
        
        return processed_df
    
    def _process_volume_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process volume data."""
        processed_df = df.copy()
        
        # Find volume column
        volume_columns = [col for col in df.columns if 'volume' in col.lower()]
        
        if volume_columns:
            volume_col = volume_columns[0]
            processed_df['volume'] = processed_df[volume_col]
        else:
            # Assume last numeric column is volume
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                processed_df['volume'] = processed_df[numeric_cols[-1]]
        
        return processed_df
    
    def _process_default_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply default processing to data."""
        processed_df = df.copy()
        
        # Remove completely empty rows and columns
        processed_df = processed_df.dropna(how='all').dropna(axis=1, how='all')
        
        # Convert numeric columns
        for col in processed_df.columns:
            if processed_df[col].dtype == 'object':
                try:
                    processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
                except:
                    pass
        
        return processed_df
    
    def _clean_ohlcv_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean OHLCV data by removing invalid values."""
        cleaned_df = df.copy()
        
        # Remove rows with negative prices
        for col in ['open', 'high', 'low', 'close']:
            if col in cleaned_df.columns:
                cleaned_df = cleaned_df[cleaned_df[col] > 0]
        
        # Remove rows where high < low
        if 'high' in cleaned_df.columns and 'low' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['high'] >= cleaned_df['low']]
        
        # Remove rows where volume is negative
        if 'volume' in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df['volume'] >= 0]
        
        return cleaned_df
    
    def _apply_drawing_mode(self, df: pd.DataFrame, draw_mode: str) -> pd.DataFrame:
        """Apply drawing mode to the data."""
        # This is a placeholder for drawing functionality
        # In practice, you would implement actual drawing/visualization logic
        
        if draw_mode == 'candlestick':
            # Prepare data for candlestick chart
            pass
        elif draw_mode == 'line':
            # Prepare data for line chart
            pass
        elif draw_mode == 'bar':
            # Prepare data for bar chart
            pass
        
        return df
    
    def _export_data(self, df: pd.DataFrame, original_file: Path, 
                    export_formats: List[str]) -> Dict[str, bool]:
        """Export data in specified formats."""
        export_results = {}
        
        for export_format in export_formats:
            try:
                if export_format == 'parquet':
                    export_path = original_file.with_suffix('.parquet')
                    df.to_parquet(export_path, index=False)
                    export_results['parquet'] = True
                
                elif export_format == 'csv':
                    export_path = original_file.with_suffix('.processed.csv')
                    df.to_csv(export_path, index=False)
                    export_results['csv'] = True
                
                elif export_format == 'json':
                    export_path = original_file.with_suffix('.json')
                    df.to_json(export_path, orient='records')
                    export_results['json'] = True
                
            except Exception as e:
                export_results[export_format] = False
                print(f"⚠️  Failed to export {export_format}: {e}")
        
        return export_results
