#!/usr/bin/env python3
"""
Improved AutoGluon Demo with CLI flags
Улучшенное демо AutoGluon с CLI флагами

This demo allows you to specify symbols and indicators via command line flags
to work with fewer files and avoid the CSVExport scanning issues.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.complete_pipeline import CompleteTradingPipeline
from automl.gluon.data.auto_data_scanner import AutoDataScanner

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function for improved demo."""
    parser = argparse.ArgumentParser(description='Improved AutoGluon Demo')
    parser.add_argument('--symbol', default='BTCUSD', help='Symbol to analyze (default: BTCUSD)')
    parser.add_argument('--indicator', default='WAVE2', choices=['WAVE2', 'SHORT3', 'CSVExport'], 
                       help='Indicator to use (default: WAVE2)')
    parser.add_argument('--timeframes', nargs='+', default=['D1'], 
                       help='Timeframes to use (default: D1). Use "ALL" for all available timeframes')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick analysis with limited data')
    parser.add_argument('--interactive', action='store_true', 
                       help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Handle ALL timeframes flag
    if 'ALL' in args.timeframes:
        # Get all available timeframes from the data directory
        import os
        from pathlib import Path
        
        data_path = Path("data/cache/csv_converted/")
        available_timeframes = set()
        
        if data_path.exists():
            for file_path in data_path.glob("*.parquet"):
                filename = file_path.name
                # Extract timeframe from filename patterns
                if f"_{args.symbol}_PERIOD_" in filename:
                    parts = filename.split("_PERIOD_")
                    if len(parts) > 1:
                        timeframe = parts[1].replace(".parquet", "")
                        available_timeframes.add(timeframe)
        
        # Sort timeframes in logical order
        timeframe_order = ['M1', 'M5', 'M15', 'H1', 'H4', 'D1', 'W1', 'MN1']
        sorted_timeframes = []
        for tf in timeframe_order:
            if tf in available_timeframes:
                sorted_timeframes.append(tf)
        
        # Add any remaining timeframes not in the standard order
        for tf in sorted(available_timeframes):
            if tf not in sorted_timeframes:
                sorted_timeframes.append(tf)
        
        args.timeframes = sorted_timeframes
        print(f"🔍 Found {len(args.timeframes)} available timeframes for {args.symbol}")
    
    print("🚀 Improved AutoGluon Demo")
    print("=" * 60)
    print(f"📊 Symbol: {args.symbol}")
    print(f"🎯 Indicator: {args.indicator}")
    print(f"⏰ Timeframes: {', '.join(args.timeframes)}")
    print(f"⚡ Quick mode: {'Yes' if args.quick else 'No'}")
    print("=" * 60)
    
    try:
        # Initialize pipeline
        pipeline = CompleteTradingPipeline()
        
        # Run pipeline with specific parameters
        results = pipeline.run_complete_pipeline(
            symbols=[args.symbol],
            timeframes=args.timeframes,
            target_symbol=args.symbol,
            target_timeframe=args.timeframes[0],
            use_auto_scan=False,  # Disable auto-scan to use specific parameters
            interactive=args.interactive
        )
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 PIPELINE RESULTS")
        print("=" * 60)
        print(f"✅ Status: {'SUCCESS' if results.get('pipeline_summary', {}).get('pipeline_successful', False) else 'FAILED'}")
        print(f"⏱️  Total Time: {results.get('pipeline_summary', {}).get('total_time_minutes', 0):.1f} minutes")
        
        if 'model_training' in results:
            print(f"🤖 Model Training: {results['model_training'].get('training_time_minutes', 0):.1f} minutes")
            print(f"📈 Model Ready: {'Yes' if results['model_training'].get('model_ready', False) else 'No'}")
        
        if 'model_evaluation' in results:
            print(f"📊 Model Evaluation: Completed")
        
        print("=" * 60)
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
