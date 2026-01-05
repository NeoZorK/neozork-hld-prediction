#!/usr/bin/env python3
"""
Simple Pipeline Test - Quick validation without full training
A simple pypline test is a fast validation without full training.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.data.multi_indicator_loader import MultiIndicatorLoader
from automl.gluon.features.updated_feature_engineer import UpdatedCustomFeatureEngineer

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_data_Loading():
 """Test data Loading functionality."""
 print("🔍 testing data Loading...")

 loader = MultiIndicatorLoader()

 # Test Loading single symbol/Timeframe
 data_sources = loader.load_symbol_data('BTCUSD', 'D1')

 print(f"📊 data sources loaded: {List(data_sources.keys())}")

 for indicator, data in data_sources.items():
 if not data.empty:
 print(f" {indicator}: {len(data)} rows, {len(data.columns)} columns")
 print(f" columns: {List(data.columns)}")
 else:
 print(f" {indicator}: No data")

 return data_sources


def test_data_combination(data_sources):
 """Test data combination."""
 print("\n🔄 testing data combination...")

 loader = MultiIndicatorLoader()
 combined_data = loader.combine_indicators(data_sources)

 print(f"📊 Combined data: {len(combined_data)} rows, {len(combined_data.columns)} columns")
 print(f" columns: {List(combined_data.columns)}")

 return combined_data


def test_feature_engineering(combined_data):
 """Test feature engineering."""
 print("\n🔧 testing feature engineering...")

 # Create target variable
 loader = MultiIndicatorLoader()
 data_with_target = loader.create_target_variable(combined_data, method='price_direction')

 print(f"📊 data with target: {len(data_with_target)} rows")
 print(f" Target distribution: {data_with_target['target'].value_counts().to_dict()}")

 # Create custom features
 feature_engineer = UpdatedCustomFeatureEngineer()

 # Test SCHR features
 if any(col in data_with_target.columns for col in ['pressure', 'pressure_vector', 'predicted_low', 'predicted_high']):
 print(" Creating SCHR features...")
 data_with_schr = feature_engineer.create_schr_features(data_with_target)
 schr_features = [col for col in data_with_schr.columns if 'probability' in col]
 print(f" SCHR features created: {len(schr_features)}")
 print(f" SCHR feature names: {schr_features}")
 else:
 print(" ⚠️ No SCHR columns found")
 data_with_schr = data_with_target

 # Test WAVE2 features
 if any(col in data_with_schr.columns for col in ['wave', 'fast_line', 'ma_line', 'direction', 'signal']):
 print(" Creating WAVE2 features...")
 data_with_wave = feature_engineer.create_wave2_features(data_with_schr)
 wave_features = [col for col in data_with_wave.columns if 'wave' in col and 'probability' in col]
 print(f" WAVE2 features created: {len(wave_features)}")
 print(f" WAVE2 feature names: {wave_features}")
 else:
 print(" ⚠️ No WAVE2 columns found")
 data_with_wave = data_with_schr

 # Test SHORT3 features
 if any(col in data_with_wave.columns for col in ['short_trend', 'r_trend', 'global', 'direction', 'r_direction', 'signal', 'r_signal', 'g_direction', 'g_signal']):
 print(" Creating SHORT3 features...")
 data_with_short3 = feature_engineer.create_short3_features(data_with_wave)
 short3_features = [col for col in data_with_short3.columns if 'short3' in col and 'probability' in col]
 print(f" SHORT3 features created: {len(short3_features)}")
 print(f" SHORT3 feature names: {short3_features}")
 else:
 print(" ⚠️ No SHORT3 columns found")
 data_with_short3 = data_with_wave

 print(f"📊 Final data: {len(data_with_short3)} rows, {len(data_with_short3.columns)} columns")

 return data_with_short3


def test_Technical_indicators(data):
 """Test Technical indicators."""
 print("\n📈 testing Technical indicators...")

 loader = MultiIndicatorLoader()
 data_with_indicators = loader.add_Technical_indicators(data)

 new_indicators = [col for col in data_with_indicators.columns if col not in data.columns]
 print(f" Technical indicators added: {len(new_indicators)}")
 print(f" Indicator names: {new_indicators}")

 return data_with_indicators


def main():
 """Run simple pipeline test."""
 print("🚀 Simple Pipeline Test")
 print("=" * 50)

 try:
 # Test 1: data Loading
 data_sources = test_data_Loading()

 if not any(not df.empty for df in data_sources.values()):
 print("❌ No data loaded - test failed")
 return False

 # Test 2: data combination
 combined_data = test_data_combination(data_sources)

 if combined_data.empty:
 print("❌ data combination failed")
 return False

 # Test 3: Feature engineering
 data_with_features = test_feature_engineering(combined_data)

 if data_with_features.empty:
 print("❌ Feature engineering failed")
 return False

 # Test 4: Technical indicators
 final_data = test_Technical_indicators(data_with_features)

 if final_data.empty:
 print("❌ Technical indicators failed")
 return False

 # Summary
 print("\n" + "=" * 50)
 print("✅ SIMPLE PIPELINE TEST RESULTS")
 print("=" * 50)

 print(f"📊 Final dataset:")
 print(f" Rows: {len(final_data):,}")
 print(f" columns: {len(final_data.columns)}")
 print(f" Target distribution: {final_data['target'].value_counts().to_dict()}")

 # Count features by type
 schr_features = [col for col in final_data.columns if 'probability' in col and any(x in col for x in ['trend', 'yellow', 'blue', 'pv'])]
 wave_features = [col for col in final_data.columns if 'wave' in col and 'probability' in col]
 short3_features = [col for col in final_data.columns if 'short3' in col and 'probability' in col]
 Technical_features = [col for col in final_data.columns if any(x in col for x in ['sma', 'ema', 'rsi', 'macd', 'volatility'])]

 print(f"\n🔧 Features Created:")
 print(f" SCHR features: {len(schr_features)}")
 print(f" WAVE2 features: {len(wave_features)}")
 print(f" SHORT3 features: {len(short3_features)}")
 print(f" Technical indicators: {len(Technical_features)}")
 print(f" Total custom features: {len(schr_features) + len(wave_features) + len(short3_features)}")

 print(f"\n🎯 data Quality:")
 print(f" Missing values: {final_data.isnull().sum().sum()}")
 print(f" data types: {final_data.dtypes.value_counts().to_dict()}")

 print(f"\n✅ all tests passed! Pipeline is Working correctly.")
 print(f" Ready for model training with {len(final_data)} samples and {len(final_data.columns)} features.")

 return True

 except Exception as e:
 print(f"\n❌ Test failed: {e}")
 logger.error(f"Test failed: {e}")
 return False


if __name__ == "__main__":
 # Create Logs directory if it doesn't exist
 os.makedirs('Logs', exist_ok=True)

 # Run test
 success = main()

 if success:
 print("\n🎉 Simple pipeline test COMPLETED successfully!")
 else:
 print("\n💥 Simple pipeline test failed!")
 sys.exit(1)
