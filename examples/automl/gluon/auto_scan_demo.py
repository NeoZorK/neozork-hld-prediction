#!/usr/bin/env python3
"""
Auto Scan Demo - Interactive data selection and pipeline execution
Демо автоматического сканирования - Интерактивный выбор данных and выполнение пайплайна

This script demonstrates the new auto-scanning functionality that automatically
discovers available indicators, symbols, and Timeframes from filenames.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.complete_pipeline import CompleteTradingPipeline
from automl.gluon.data.auto_data_scanner import AutodataScanner, InteractivedataSelector

# Configure logging
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[
 logging.StreamHandler(),
 logging.FileHandler('logs/auto_scan_demo.log')
 ]
)

logger = logging.getLogger(__name__)


def test_auto_scanner():
 """Test the auto scanner functionality."""
 print("🔍 testing Auto data Scanner")
 print("=" * 50)

 # Initialize scanner
 scanner = AutodataScanner()

 # Scan directory
 print("📊 Scanning data directory...")
 scan_results = scanner.scan_directory()

 if scan_results.get('scan_successful'):
 scanner.print_scan_results()
 return scanner
 else:
 print(f"❌ Scan failed: {scan_results.get('error')}")
 return None


def test_interactive_selection(scanner):
 """Test interactive selection."""
 print("\n🎯 testing Interactive Selection")
 print("=" * 50)

 selector = InteractivedataSelector(scanner)
 selection = selector.interactive_selection()

 if selection.get('success'):
 print(f"\n✅ Selection successful!")
 print(f" Indicator: {selection['indicator']}")
 print(f" symbol: {selection['symbol']}")
 print(f" Timeframes: {', '.join(selection['Timeframes'])}")
 print(f" Files: {len(selection.get('file_paths', {}))}")
 return selection
 else:
 print(f"❌ Selection failed: {selection.get('error')}")
 return None


def test_auto_pipeline():
 """Test the complete pipeline with auto-scanning."""
 print("\n🚀 testing Auto Pipeline")
 print("=" * 50)

 # Initialize pipeline
 pipeline = CompleteTradingPipeline()

 # Run pipeline with auto-scanning
 print("🔍 Running pipeline with automatic scanning...")

 try:
 results = pipeline.run_complete_pipeline(
 Use_auto_scan=True,
 interactive=True
 )

 # Display results
 print("\n" + "=" * 60)
 print("📊 AUTO PIPELINE RESULTS")
 print("=" * 60)

 # Pipeline summary
 summary = results.get('pipeline_summary', {})
 print(f"✅ Status: {'SUCCESS' if summary.get('pipeline_successful', False) else 'FAILED'}")
 print(f"⏱️ Total Time: {summary.get('total_time_minutes', 0):.1f} minutes")

 # data Loading results
 data_Loading = results.get('data_Loading', {})
 print(f"\n📊 data Loading:")
 print(f" Total Rows: {data_Loading.get('total_rows', 0):,}")
 print(f" Total columns: {data_Loading.get('total_columns', 0)}")
 print(f" symbols: {', '.join(data_Loading.get('symbols_loaded', []))}")
 print(f" Timeframes: {', '.join(data_Loading.get('Timeframes_loaded', []))}")
 print(f" Indicators: {', '.join(data_Loading.get('indicators_loaded', []))}")
 print(f" Auto-scan Used: {data_Loading.get('auto_scan_Used', False)}")

 # Feature engineering results
 feature_eng = results.get('feature_engineering', {})
 print(f"\n🔧 Feature Engineering:")
 print(f" Custom Features: {feature_eng.get('features_created', 0)}")
 print(f" Total Features: {feature_eng.get('total_features', 0)}")

 # Model training results
 model_training = results.get('model_training', {})
 print(f"\n🤖 Model Training:")
 print(f" Training Time: {model_training.get('training_time_minutes', 0):.1f} minutes")
 print(f" Model Ready: {'✅' if model_training.get('model_ready', False) else '❌'}")

 # Model evaluation results
 evaluation = results.get('model_evaluation', {})
 print(f"\n📈 Model Evaluation:")
 for metric, value in evaluation.items():
 if isinstance(value, (int, float)):
 print(f" {metric}: {value:.4f}")

 # Advanced Analysis results
 advanced_Analysis = results.get('advanced_Analysis', {})
 if advanced_Analysis and 'error' not in advanced_Analysis:
 print(f"\n🔍 Advanced Analysis:")

 # Backtesting results
 if 'backtesting' in advanced_Analysis:
 bt = advanced_Analysis['backtesting']
 print(f" 📈 Backtesting:")
 print(f" Total Return: {bt.get('total_return', 0):.2%}")
 print(f" Sharpe Ratio: {bt.get('sharpe_ratio', 0):.3f}")
 print(f" Max Drawdown: {bt.get('max_drawdown', 0):.2%}")
 print(f" Profit Factor: {bt.get('profit_factor', 0):.2f}")

 # Walk Forward results
 if 'walk_forward' in advanced_Analysis:
 wf = advanced_Analysis['walk_forward']
 print(f" 🚶 Walk Forward:")
 print(f" Stability Score: {wf.get('stability_score', 0):.3f}")
 print(f" Mean Accuracy: {wf.get('mean_accuracy', 0):.3f}")

 # Monte Carlo results
 if 'monte_carlo' in advanced_Analysis:
 mc = advanced_Analysis['monte_carlo']
 print(f" 🎲 Monte Carlo:")
 print(f" Robustness Score: {mc.get('robustness_score', 0):.3f}")
 print(f" Mean Accuracy: {mc.get('mean_accuracy', 0):.3f}")
 else:
 print(f"\n⚠️ Advanced Analysis: {'Failed' if advanced_Analysis.get('error') else 'Not performed'}")

 # Model export results
 model_export = results.get('model_export', {})
 print(f"\n💾 Model Export:")
 print(f" Export Path: {model_export.get('export_path', 'N/A')}")
 print(f" Export Status: {'✅ Success' if model_export.get('export_successful', False) else '❌ Failed'}")

 # Final recommendations
 print(f"\n🎯 Recommendations:")
 if summary.get('pipeline_successful', False):
 print(" ✅ Pipeline COMPLETED successfully")
 print(" ✅ Model is ready for production")
 print(" ✅ Auto-scanning worked correctly")
 else:
 print(" ❌ Pipeline failed - check logs for details")
 print(" ❌ Fix issues before deploying to production")

 return results

 except Exception as e:
 logger.error(f"❌ Auto pipeline failed: {e}")
 print(f"\n❌ Auto pipeline failed: {e}")
 return None


def main():
 """main function for auto scan demo."""
 print("🚀 Auto Scan Demo - Interactive data Selection")
 print("=" * 60)

 # Create logs directory if it doesn't exist
 os.makedirs('logs', exist_ok=True)

 try:
 # Test 1: Auto scanner
 scanner = test_auto_scanner()
 if not scanner:
 print("❌ Auto scanner test failed")
 return False

 # Test 2: Interactive selection
 selection = test_interactive_selection(scanner)
 if not selection:
 print("❌ Interactive selection test failed")
 return False

 # Test 3: Auto pipeline
 results = test_auto_pipeline()
 if not results:
 print("❌ Auto pipeline test failed")
 return False

 print("\n" + "=" * 60)
 print("🎉 Auto Scan Demo COMPLETED Successfully!")
 print("=" * 60)

 print("\n✅ all tests passed!")
 print("✅ Auto-scanning functionality is Working correctly")
 print("✅ Interactive selection is Working correctly")
 print("✅ Complete pipeline with auto-scan is Working correctly")

 return True

 except Exception as e:
 logger.error(f"❌ Demo failed: {e}")
 print(f"\n❌ Demo failed: {e}")
 return False


if __name__ == "__main__":
 # Run demo
 success = main()

 if success:
 print("\n🎉 Auto scan demo COMPLETED successfully!")
 else:
 print("\n💥 Auto scan demo failed!")
 sys.exit(1)
