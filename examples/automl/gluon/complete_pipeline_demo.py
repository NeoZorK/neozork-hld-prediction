#!/usr/bin/env python3
"""
Complete Trading Strategy Pipeline Demo
Демонстрация полного пайплайна торговой стратегии

This script demonstrates the complete workflow from data loading to model deployment.
Этот скрипт демонстрирует полный рабочий процесс от загрузки данных до развертывания модели.
"""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.complete_pipeline import CompleteTradingPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/complete_pipeline_demo.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Run complete trading strategy pipeline demo.
    Запустить демонстрацию полного пайплайна торговой стратегии.
    """
    
    print("🚀 Complete Trading Strategy Pipeline Demo")
    print("=" * 60)
    
    # Configuration
    symbols = ['BTCUSD']  # Start with one symbol for demo
    timeframes = ['D1']    # Start with daily timeframe
    target_symbol = 'BTCUSD'
    target_timeframe = 'D1'
    
    print(f"📊 Configuration:")
    print(f"   Symbols: {symbols}")
    print(f"   Timeframes: {timeframes}")
    print(f"   Target: {target_symbol} {target_timeframe}")
    print()
    
    try:
        # Initialize pipeline
        print("🔧 Initializing complete trading pipeline...")
        pipeline = CompleteTradingPipeline()
        
        # Run complete pipeline
        print("🚀 Starting complete pipeline...")
        results = pipeline.run_complete_pipeline(
            symbols=symbols,
            timeframes=timeframes,
            target_symbol=target_symbol,
            target_timeframe=target_timeframe
        )
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 PIPELINE RESULTS")
        print("=" * 60)
        
        # Pipeline summary
        summary = results.get('pipeline_summary', {})
        print(f"✅ Status: {'SUCCESS' if summary.get('pipeline_successful', False) else 'FAILED'}")
        print(f"⏱️  Total Time: {summary.get('total_time_minutes', 0):.1f} minutes")
        print(f"🎯 Target: {summary.get('target_symbol', 'N/A')} {summary.get('target_timeframe', 'N/A')}")
        
        # Data processing results
        data_loading = results.get('data_loading', {})
        print(f"\n📊 Data Processing:")
        print(f"   Total Rows: {data_loading.get('total_rows', 0):,}")
        print(f"   Total Columns: {data_loading.get('total_columns', 0)}")
        
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
        
        # Performance report
        if 'performance_report' in results.get('advanced_analysis', {}):
            print(f"\n📊 Performance Report:")
            print("   (See detailed report in advanced_analysis.performance_report)")
        
        # Final recommendations
        print(f"\n🎯 Recommendations:")
        if summary.get('pipeline_successful', False):
            print("   ✅ Pipeline completed successfully")
            print("   ✅ Model is ready for production")
            print("   ✅ Set up monitoring and retraining schedule")
        else:
            print("   ❌ Pipeline failed - check logs for details")
            print("   ❌ Fix issues before deploying to production")
        
        print("\n" + "=" * 60)
        print("🎉 Complete Pipeline Demo Finished!")
        print("=" * 60)
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        return None


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Run demo
    results = main()
    
    if results:
        print("\n✅ Demo completed successfully!")
    else:
        print("\n❌ Demo failed!")
        sys.exit(1)
