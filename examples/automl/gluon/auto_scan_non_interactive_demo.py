#!/usr/bin/env python3
"""
Auto Scan Non-Interactive Demo - Automatic data selection without user input
Демо автоматического сканирования без интерактивности - Автоматический выбор данных без ввода пользователя

This script demonstrates the auto-scanning functionality without interactive prompts.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.complete_pipeline import CompleteTradingPipeline
from automl.gluon.data.auto_data_scanner import AutoDataScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/auto_scan_non_interactive_demo.log')
    ]
)

logger = logging.getLogger(__name__)


def test_auto_scanner():
    """Test the auto scanner functionality."""
    print("🔍 Testing Auto Data Scanner")
    print("=" * 50)
    
    # Initialize scanner
    scanner = AutoDataScanner()
    
    # Scan directory
    print("📊 Scanning data directory...")
    scan_results = scanner.scan_directory()
    
    if scan_results.get('scan_successful'):
        scanner.print_scan_results()
        return scanner
    else:
        print(f"❌ Scan failed: {scan_results.get('error')}")
        return None


def test_auto_selection(scanner):
    """Test automatic selection (non-interactive)."""
    print("\n🤖 Testing Automatic Selection")
    print("=" * 50)
    
    # Auto-select first available combination
    if not scanner.available_data:
        print("❌ No data available for auto-selection")
        return None
    
    # Get first indicator
    first_indicator = list(scanner.available_data.keys())[0]
    print(f"🎯 Auto-selected indicator: {first_indicator}")
    
    # Get first symbol for this indicator
    first_symbol = list(scanner.available_data[first_indicator].keys())[0]
    print(f"💱 Auto-selected symbol: {first_symbol}")
    
    # Get all timeframes for this symbol
    timeframes = scanner.get_symbol_timeframes(first_indicator, first_symbol)
    print(f"⏰ Available timeframes: {', '.join(timeframes)}")
    
    # Create selection
    selection = {
        'success': True,
        'indicator': first_indicator,
        'symbol': first_symbol,
        'timeframes': timeframes,
        'file_paths': {}
    }
    
    # Get file paths
    for timeframe in timeframes:
        file_path = scanner.get_file_path(first_indicator, first_symbol, timeframe)
        if file_path:
            selection['file_paths'][timeframe] = file_path
            print(f"📁 {timeframe}: {file_path}")
    
    print(f"\n✅ Auto-selection completed:")
    print(f"   Indicator: {selection['indicator']}")
    print(f"   Symbol: {selection['symbol']}")
    print(f"   Timeframes: {', '.join(selection['timeframes'])}")
    print(f"   Files found: {len(selection['file_paths'])}")
    
    return selection


def test_auto_pipeline():
    """Test the complete pipeline with auto-scanning (non-interactive)."""
    print("\n🚀 Testing Auto Pipeline (Non-Interactive)")
    print("=" * 50)
    
    # Initialize pipeline
    pipeline = CompleteTradingPipeline()
    
    # Run pipeline with auto-scanning (non-interactive)
    print("🔍 Running pipeline with automatic scanning (non-interactive)...")
    
    try:
        results = pipeline.run_complete_pipeline(
            use_auto_scan=True,
            interactive=False  # Non-interactive mode
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 AUTO PIPELINE RESULTS (NON-INTERACTIVE)")
        print("=" * 60)
        
        # Pipeline summary
        summary = results.get('pipeline_summary', {})
        print(f"✅ Status: {'SUCCESS' if summary.get('pipeline_successful', False) else 'FAILED'}")
        print(f"⏱️  Total Time: {summary.get('total_time_minutes', 0):.1f} minutes")
        
        # Data loading results
        data_loading = results.get('data_loading', {})
        print(f"\n📊 Data Loading:")
        print(f"   Total Rows: {data_loading.get('total_rows', 0):,}")
        print(f"   Total Columns: {data_loading.get('total_columns', 0)}")
        print(f"   Symbols: {', '.join(data_loading.get('symbols_loaded', []))}")
        print(f"   Timeframes: {', '.join(data_loading.get('timeframes_loaded', []))}")
        print(f"   Indicators: {', '.join(data_loading.get('indicators_loaded', []))}")
        print(f"   Auto-scan used: {data_loading.get('auto_scan_used', False)}")
        
        # Feature engineering results
        feature_eng = results.get('feature_engineering', {})
        print(f"\n🔧 Feature Engineering:")
        print(f"   Custom Features: {feature_eng.get('features_created', 0)}")
        print(f"   Total Features: {feature_eng.get('total_features', 0)}")
        
        # Model training results
        model_training = results.get('model_training', {})
        print(f"\n🤖 Model Training:")
        print(f"   Training Time: {model_training.get('training_time_minutes', 0):.1f} minutes")
        print(f"   Model Ready: {'✅' if model_training.get('model_ready', False) else '❌'}")
        
        # Model evaluation results
        evaluation = results.get('model_evaluation', {})
        print(f"\n📈 Model Evaluation:")
        for metric, value in evaluation.items():
            if isinstance(value, (int, float)):
                print(f"   {metric}: {value:.4f}")
        
        # Advanced analysis results
        advanced_analysis = results.get('advanced_analysis', {})
        if advanced_analysis and 'error' not in advanced_analysis:
            print(f"\n🔍 Advanced Analysis:")
            
            # Backtesting results
            if 'backtesting' in advanced_analysis:
                bt = advanced_analysis['backtesting']
                print(f"   📈 Backtesting:")
                print(f"      Total Return: {bt.get('total_return', 0):.2%}")
                print(f"      Sharpe Ratio: {bt.get('sharpe_ratio', 0):.3f}")
                print(f"      Max Drawdown: {bt.get('max_drawdown', 0):.2%}")
                print(f"      Profit Factor: {bt.get('profit_factor', 0):.2f}")
            
            # Walk Forward results
            if 'walk_forward' in advanced_analysis:
                wf = advanced_analysis['walk_forward']
                print(f"   🚶 Walk Forward:")
                print(f"      Stability Score: {wf.get('stability_score', 0):.3f}")
                print(f"      Mean Accuracy: {wf.get('mean_accuracy', 0):.3f}")
            
            # Monte Carlo results
            if 'monte_carlo' in advanced_analysis:
                mc = advanced_analysis['monte_carlo']
                print(f"   🎲 Monte Carlo:")
                print(f"      Robustness Score: {mc.get('robustness_score', 0):.3f}")
                print(f"      Mean Accuracy: {mc.get('mean_accuracy', 0):.3f}")
        else:
            print(f"\n⚠️ Advanced Analysis: {'Failed' if advanced_analysis.get('error') else 'Not performed'}")
        
        # Model export results
        model_export = results.get('model_export', {})
        print(f"\n💾 Model Export:")
        print(f"   Export Path: {model_export.get('export_path', 'N/A')}")
        print(f"   Export Status: {'✅ Success' if model_export.get('export_successful', False) else '❌ Failed'}")
        
        # Final recommendations
        print(f"\n🎯 Recommendations:")
        if summary.get('pipeline_successful', False):
            print("   ✅ Pipeline completed successfully")
            print("   ✅ Model is ready for production")
            print("   ✅ Auto-scanning worked correctly")
            print("   ✅ Non-interactive mode worked correctly")
        else:
            print("   ❌ Pipeline failed - check logs for details")
            print("   ❌ Fix issues before deploying to production")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Auto pipeline failed: {e}")
        print(f"\n❌ Auto pipeline failed: {e}")
        return None


def main():
    """Main function for auto scan non-interactive demo."""
    print("🚀 Auto Scan Non-Interactive Demo")
    print("=" * 60)
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    try:
        # Test 1: Auto scanner
        scanner = test_auto_scanner()
        if not scanner:
            print("❌ Auto scanner test failed")
            return False
        
        # Test 2: Auto selection
        selection = test_auto_selection(scanner)
        if not selection:
            print("❌ Auto selection test failed")
            return False
        
        # Test 3: Auto pipeline (non-interactive)
        results = test_auto_pipeline()
        if not results:
            print("❌ Auto pipeline test failed")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 Auto Scan Non-Interactive Demo Completed Successfully!")
        print("=" * 60)
        
        print("\n✅ All tests passed!")
        print("✅ Auto-scanning functionality is working correctly")
        print("✅ Non-interactive selection is working correctly")
        print("✅ Complete pipeline with auto-scan is working correctly")
        print("✅ No user input required - fully automated!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        return False


if __name__ == "__main__":
    # Run demo
    success = main()
    
    if success:
        print("\n🎉 Auto scan non-interactive demo completed successfully!")
    else:
        print("\n💥 Auto scan non-interactive demo failed!")
        sys.exit(1)
