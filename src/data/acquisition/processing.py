# -*- coding: utf-8 -*-
# src/data/acquisition/processing.py

"""
Data acquisition processing functionality.
Handles data processing, cleaning, and transformation during acquisition.
All comments are in English.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta


class DataAcquisitionProcessing:
    """Handles data processing during acquisition."""
    
    def __init__(self):
        """Initialize the processing module."""
        self.required_columns = ['open', 'high', 'low', 'close', 'volume']
        self.timestamp_column = 'timestamp'
    
    def process_acquired_data(self, df: pd.DataFrame, instrument: str, 
                            processing_options: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Process acquired data with various cleaning and transformation steps.
        
        Args:
            df: Raw DataFrame to process
            instrument: Name of the instrument
            processing_options: Dictionary with processing options
            
        Returns:
            Processed DataFrame
        """
        if df is None or df.empty:
            print(f"❌ No data to process for {instrument}")
            return pd.DataFrame()
        
        print(f"🔧 Processing data for {instrument}: {len(df)} rows")
        
        # Apply processing steps
        processed_df = df.copy()
        
        # Standardize column names
        processed_df = self._standardize_columns(processed_df)
        
        # Clean data
        processed_df = self._clean_data(processed_df)
        
        # Validate data
        validation_result = self._validate_processed_data(processed_df)
        if not validation_result['is_valid']:
            print(f"⚠️  Data validation warnings: {validation_result['warnings']}")
        
        # Apply transformations
        if processing_options and processing_options.get('apply_transformations', True):
            processed_df = self._apply_transformations(processed_df, processing_options)
        
        print(f"✅ Processing completed for {instrument}: {len(processed_df)} rows")
        return processed_df
    
    def _standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names to lowercase."""
        df.columns = df.columns.str.lower()
        return df
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by removing invalid values and duplicates."""
        original_rows = len(df)
        
        # Remove rows with all NaN values
        df = df.dropna(how='all')
        
        # Remove duplicate rows
        df = df.drop_duplicates()
        
        # Handle missing values in numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in df.columns:
                # Forward fill for small gaps
                df[col] = df[col].fillna(method='ffill', limit=5)
                # Backward fill for remaining gaps
                df[col] = df[col].fillna(method='bfill', limit=5)
        
        # Remove rows with negative prices (for OHLC data)
        if 'open' in df.columns:
            df = df[df['open'] > 0]
        if 'high' in df.columns:
            df = df[df['high'] > 0]
        if 'low' in df.columns:
            df = df[df['low'] > 0]
        if 'close' in df.columns:
            df = df[df['close'] > 0]
        
        # Remove rows where high < low
        if 'high' in df.columns and 'low' in df.columns:
            df = df[df['high'] >= df['low']]
        
        # Remove rows where volume is negative
        if 'volume' in df.columns:
            df = df[df['volume'] >= 0]
        
        cleaned_rows = len(df)
        removed_rows = original_rows - cleaned_rows
        
        if removed_rows > 0:
            print(f"🧹 Cleaned data: removed {removed_rows} invalid rows")
        
        return df
    
    def _validate_processed_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate the processed data."""
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'statistics': {}
        }
        
        if df.empty:
            validation_result['is_valid'] = False
            validation_result['errors'].append("DataFrame is empty after processing")
            return validation_result
        
        # Check required columns
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            validation_result['warnings'].append(f"Missing required columns: {missing_columns}")
        
        # Check data types
        for col in ['open', 'high', 'low', 'close']:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    validation_result['warnings'].append(f"Column {col} is not numeric")
        
        # Check for anomalies
        if 'high' in df.columns and 'low' in df.columns:
            invalid_high_low = (df['high'] < df['low']).sum()
            if invalid_high_low > 0:
                validation_result['errors'].append(f"Found {invalid_high_low} rows where high < low")
                validation_result['is_valid'] = False
        
        # Calculate statistics
        validation_result['statistics'] = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum()
        }
        
        return validation_result
    
    def _apply_transformations(self, df: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        """Apply data transformations based on options."""
        transformed_df = df.copy()
        
        # Add technical indicators if requested
        if options.get('add_technical_indicators', False):
            transformed_df = self._add_technical_indicators(transformed_df)
        
        # Resample data if requested
        if options.get('resample', False):
            resample_freq = options.get('resample_freq', '1H')
            transformed_df = self._resample_data(transformed_df, resample_freq)
        
        # Add derived columns if requested
        if options.get('add_derived_columns', False):
            transformed_df = self._add_derived_columns(transformed_df)
        
        return transformed_df
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add basic technical indicators to the data."""
        result_df = df.copy()
        
        # Simple Moving Averages
        if 'close' in result_df.columns:
            result_df['sma_20'] = result_df['close'].rolling(window=20).mean()
            result_df['sma_50'] = result_df['close'].rolling(window=50).mean()
        
        # RSI (Relative Strength Index)
        if 'close' in result_df.columns:
            delta = result_df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            result_df['rsi'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        if 'close' in result_df.columns:
            sma_20 = result_df['close'].rolling(window=20).mean()
            std_20 = result_df['close'].rolling(window=20).std()
            result_df['bb_upper'] = sma_20 + (std_20 * 2)
            result_df['bb_lower'] = sma_20 - (std_20 * 2)
        
        return result_df
    
    def _resample_data(self, df: pd.DataFrame, freq: str) -> pd.DataFrame:
        """Resample data to a different frequency."""
        try:
            # Ensure timestamp column exists and is datetime
            timestamp_col = self._find_timestamp_column(df)
            if timestamp_col is None:
                print("⚠️  No timestamp column found for resampling")
                return df
            
            # Set timestamp as index for resampling
            df_for_resample = df.set_index(timestamp_col)
            
            # Resample OHLCV data
            resampled = df_for_resample.resample(freq).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
            
            # Reset index to make timestamp a column again
            resampled = resampled.reset_index()
            
            print(f"📊 Resampled data to {freq} frequency: {len(resampled)} rows")
            return resampled
            
        except Exception as e:
            print(f"⚠️  Error during resampling: {e}")
            return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived columns to the data."""
        result_df = df.copy()
        
        # Price changes
        if 'close' in result_df.columns:
            result_df['price_change'] = result_df['close'].diff()
            result_df['price_change_pct'] = result_df['close'].pct_change() * 100
        
        # Volatility
        if 'high' in result_df.columns and 'low' in result_df.columns:
            result_df['volatility'] = result_df['high'] - result_df['low']
            result_df['volatility_pct'] = (result_df['volatility'] / result_df['close']) * 100
        
        # Volume analysis
        if 'volume' in result_df.columns:
            result_df['volume_sma'] = result_df['volume'].rolling(window=20).mean()
            result_df['volume_ratio'] = result_df['volume'] / result_df['volume_sma']
        
        return result_df
    
    def _find_timestamp_column(self, df: pd.DataFrame) -> Optional[str]:
        """Find the timestamp column in the DataFrame."""
        timestamp_candidates = ['timestamp', 'time', 'date', 'datetime', 'ts']
        
        for col in df.columns:
            col_lower = col.lower()
            if any(candidate == col_lower for candidate in timestamp_candidates):
                return col
        
        # Check for datetime columns
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                return col
        
        return None
