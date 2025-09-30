#!/usr/bin/env python3
"""
Data Enhancement Script
Скрипт для улучшения данных
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
from datetime import datetime, timedelta
import yfinance as yf
import requests
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

class DataEnhancer:
    """Enhanced data collection for better ML training."""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)
        
    def download_yfinance_data(self, symbol: str = "BTC-USD", period: str = "max") -> pd.DataFrame:
        """Download additional data from Yahoo Finance."""
        print(f"📥 Downloading {symbol} data from Yahoo Finance...")
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print(f"❌ No data found for {symbol}")
                return pd.DataFrame()
            
            # Rename columns to match our format
            data.columns = [col.title() for col in data.columns]
            data = data.reset_index()
            
            # Add symbol and timeframe
            data['Symbol'] = symbol
            data['Timeframe'] = '1d'  # Daily data
            
            print(f"✅ Downloaded {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            print(f"❌ Error downloading {symbol}: {e}")
            return pd.DataFrame()
    
    def download_multiple_symbols(self, symbols: list = None) -> pd.DataFrame:
        """Download data for multiple symbols."""
        if symbols is None:
            symbols = [
                "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD",
                "XRP-USD", "DOT-USD", "DOGE-USD", "AVAX-USD", "MATIC-USD"
            ]
        
        all_data = []
        
        for symbol in symbols:
            data = self.download_yfinance_data(symbol)
            if not data.empty:
                all_data.append(data)
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            print(f"✅ Combined data: {len(combined_data)} records from {len(all_data)} symbols")
            return combined_data
        else:
            print("❌ No data downloaded")
            return pd.DataFrame()
    
    def generate_synthetic_data(self, base_data: pd.DataFrame, multiplier: int = 3) -> pd.DataFrame:
        """Generate synthetic data for training augmentation."""
        print(f"🔄 Generating {multiplier}x synthetic data...")
        
        synthetic_data = []
        
        for _ in range(multiplier):
            # Add noise to existing data
            noise_factor = 0.01  # 1% noise
            synthetic = base_data.copy()
            
            # Add random noise to price columns
            price_cols = ['Open', 'High', 'Low', 'Close']
            for col in price_cols:
                if col in synthetic.columns:
                    noise = np.random.normal(0, noise_factor, len(synthetic))
                    synthetic[col] = synthetic[col] * (1 + noise)
            
            # Add noise to volume if available
            if 'Volume' in synthetic.columns:
                volume_noise = np.random.normal(0, 0.05, len(synthetic))
                synthetic['Volume'] = synthetic['Volume'] * (1 + volume_noise)
            
            # Add timestamp variation
            if 'Date' in synthetic.columns:
                time_delta = np.random.timedelta64(np.random.randint(-3600, 3600), 's')
                synthetic['Date'] = pd.to_datetime(synthetic['Date']) + time_delta
            
            synthetic_data.append(synthetic)
        
        combined_synthetic = pd.concat(synthetic_data, ignore_index=True)
        print(f"✅ Generated {len(combined_synthetic)} synthetic records")
        return combined_synthetic
    
    def enhance_existing_data(self, file_path: str) -> pd.DataFrame:
        """Enhance existing data with additional features."""
        print(f"🔧 Enhancing data from {file_path}...")
        
        # Load existing data
        if file_path.endswith('.parquet'):
            data = pd.read_parquet(file_path)
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            print(f"❌ Unsupported file format: {file_path}")
            return pd.DataFrame()
        
        # Add technical indicators
        data = self._add_technical_indicators(data)
        
        # Add time-based features
        data = self._add_time_features(data)
        
        # Add market regime features
        data = self._add_market_regime_features(data)
        
        print(f"✅ Enhanced data: {len(data)} records with {len(data.columns)} features")
        return data
    
    def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add comprehensive technical indicators."""
        if 'Close' not in data.columns:
            return data
        
        # Moving averages
        for window in [5, 10, 20, 50, 100, 200]:
            data[f'sma_{window}'] = data['Close'].rolling(window).mean()
            data[f'ema_{window}'] = data['Close'].ewm(span=window).mean()
        
        # Volatility
        for window in [5, 10, 20, 50]:
            data[f'volatility_{window}'] = data['Close'].pct_change().rolling(window).std()
        
        # RSI
        for period in [7, 14, 21]:
            data[f'rsi_{period}'] = self._calculate_rsi(data['Close'], period)
        
        # MACD
        macd_data = self._calculate_macd(data['Close'])
        data['macd'] = macd_data['macd']
        data['macd_signal'] = macd_data['signal']
        data['macd_histogram'] = macd_data['histogram']
        
        return data
    
    def _add_time_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add time-based features."""
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            data['year'] = data['Date'].dt.year
            data['month'] = data['Date'].dt.month
            data['day'] = data['Date'].dt.day
            data['day_of_week'] = data['Date'].dt.dayofweek
            data['quarter'] = data['Date'].dt.quarter
            data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)
        
        return data
    
    def _add_market_regime_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add market regime features."""
        if 'Close' not in data.columns:
            return data
        
        # Trend strength
        data['trend_20'] = (data['Close'] > data['Close'].rolling(20).mean()).astype(int)
        data['trend_50'] = (data['Close'] > data['Close'].rolling(50).mean()).astype(int)
        
        # Volatility regime
        data['volatility_regime'] = pd.cut(
            data['Close'].pct_change().rolling(20).std(),
            bins=3, labels=['Low', 'Medium', 'High']
        )
        
        return data
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI."""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, close: pd.Series) -> dict:
        """Calculate MACD."""
        ema_fast = close.ewm(span=12).mean()
        ema_slow = close.ewm(span=26).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': histogram
        }
    
    def save_enhanced_data(self, data: pd.DataFrame, filename: str = "enhanced_data.parquet"):
        """Save enhanced data."""
        file_path = self.data_path / filename
        data.to_parquet(file_path, index=False)
        print(f"💾 Saved enhanced data to {file_path}")
        return file_path

def main():
    """Main function to enhance data."""
    print("🚀 Starting data enhancement...")
    
    enhancer = DataEnhancer()
    
    # Download additional data
    print("\n📥 Downloading additional data...")
    additional_data = enhancer.download_multiple_symbols()
    
    if not additional_data.empty:
        # Save additional data
        enhancer.save_enhanced_data(additional_data, "additional_crypto_data.parquet")
    
    # Enhance existing BTC data
    print("\n🔧 Enhancing existing BTC data...")
    btc_file = "data/CSVExport_BTCUSD_PERIOD_MN1.parquet"
    
    if Path(btc_file).exists():
        enhanced_btc = enhancer.enhance_existing_data(btc_file)
        enhancer.save_enhanced_data(enhanced_btc, "enhanced_btc_data.parquet")
    
    # Generate synthetic data
    if not additional_data.empty:
        print("\n🔄 Generating synthetic data...")
        synthetic_data = enhancer.generate_synthetic_data(additional_data, multiplier=2)
        enhancer.save_enhanced_data(synthetic_data, "synthetic_crypto_data.parquet")
    
    print("\n✅ Data enhancement completed!")

if __name__ == "__main__":
    main()
