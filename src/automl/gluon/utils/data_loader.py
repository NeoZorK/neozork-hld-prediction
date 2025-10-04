"""
Data Loader for SCHR Levels AutoML

Provides data loading and preprocessing utilities.
"""

import os
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional, List


class DataLoader:
    """Handles data loading and preprocessing"""
    
    def __init__(self, data_path: str = "data/cache/csv_converted/"):
        self.data_path = data_path
        self.logger = logging.getLogger(__name__)
    
    def load_schr_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """Load SCHR Levels data from parquet files"""
        try:
            filename = f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet"
            file_path = os.path.join(self.data_path, filename)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Data file not found: {file_path}")
            
            df = pd.read_parquet(file_path)
            self.logger.info(f"Loaded {len(df)} records for {symbol} {timeframe}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load data for {symbol} {timeframe}: {e}")
            raise
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess data for ML"""
        try:
            # Handle missing values
            df = df.fillna(method='ffill').fillna(method='bfill')
            
            # Handle infinite values
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.fillna(0)
            
            # Ensure numeric columns are numeric
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            self.logger.info(f"Preprocessed {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"Data preprocessing failed: {e}")
            raise
    
    def get_available_symbols(self) -> List[str]:
        """Get list of available symbols"""
        try:
            symbols = set()
            for filename in os.listdir(self.data_path):
                if filename.startswith('CSVExport_') and filename.endswith('.parquet'):
                    symbol = filename.split('_')[1]
                    symbols.add(symbol)
            return sorted(list(symbols))
            
        except Exception as e:
            self.logger.error(f"Failed to get available symbols: {e}")
            return []
    
    def get_available_timeframes(self) -> List[str]:
        """Get list of available timeframes"""
        return ['MN1', 'W1', 'D1', 'H4', 'H1', 'M15', 'M5', 'M1']
