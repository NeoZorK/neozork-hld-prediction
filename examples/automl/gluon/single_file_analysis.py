#!/usr/bin/env python3
"""
Single File Analysis Script for AutoGluon Models
Анализ одного файла для обучения и тестирования модели
"""

import pandas as pd
import numpy as np
import os
import sys
import shutil
import glob
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon import GluonAutoML
from automl.gluon.analysis.model_analysis import ModelAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_single_file(file_path: str, 
                       target_column: str = "target",
                       analysis_type: str = "full") -> Dict[str, Any]:
    """
    Analyze a single file with AutoGluon.
    
    Args:
        file_path: Path to the data file
        target_column: Target column name
        analysis_type: Type of analysis ("full", "quick", "backtest", "walk_forward", "monte_carlo")
        
    Returns:
        Analysis results
    """
    logger.info(f"Starting analysis of {file_path}")
    logger.info(f"Analysis type: {analysis_type}")
    
    # Initialize AutoGluon
    gluon = GluonAutoML()
    
    # Load data
    logger.info("Loading data...")
    data = gluon.load_data(file_path)
    
    # Prepare data for ML
    logger.info("Preparing data for ML...")
    # Create target variable (simplified for demo)
    data['target'] = np.where(data['Close'].diff() > 0, 1, 0)
    data = data.dropna(subset=['target'])
    
    # Create time series split
    logger.info("Creating time series split...")
    train_data, val_data, test_data = gluon.create_time_series_split(data)
    
    # Train model with error handling
    logger.info("Training model...")
    try:
        gluon.train_models(train_data, target_column, val_data)
    except Exception as e:
        error_msg = str(e)
        if "Learner is already fit" in error_msg or "already fit" in error_msg.lower():
            logger.warning("Model conflict detected. Cleaning existing models...")
            
            # Find and show model files
            model_paths = []
            
            # Check for main model directory
            if os.path.exists("models/autogluon"):
                model_paths.append("models/autogluon")
            
            # Check for sub-fit directories
            sub_fit_dirs = glob.glob("models/autogluon_ds_sub_fit*")
            model_paths.extend(sub_fit_dirs)
            
            # Check for single file analysis directories
            single_analysis_dirs = glob.glob("models/single_file_analysis_*")
            model_paths.extend(single_analysis_dirs)
            
            if model_paths:
                print(f"\n⚠️  Found {len(model_paths)} model directories that may be causing conflicts:")
                for path in model_paths:
                    if os.path.exists(path):
                        print(f"   📂 {path}")
                
                print(f"\n❓ Do you want to delete these model files and retry? (y/n): ", end="")
                try:
                    response = input().strip().lower()
                except KeyboardInterrupt:
                    logger.error("Analysis cancelled by user")
                    return {"status": "error", "message": "Analysis cancelled by user"}
                
                if response in ['y', 'yes', 'да', 'д']:
                    print("🧹 Cleaning model files...")
                    for path in model_paths:
                        try:
                            if os.path.exists(path):
                                shutil.rmtree(path)
                                print(f"   ✅ Cleaned: {path}")
                        except Exception as clean_error:
                            print(f"   ❌ Failed to clean {path}: {clean_error}")
                    
                    print("🔄 Retrying model training...")
                    gluon.train_models(train_data, target_column, val_data)
                else:
                    logger.error("Analysis cancelled - model files not cleaned")
                    return {"status": "error", "message": "Analysis cancelled - model files not cleaned"}
            else:
                logger.error("No model files found, but conflict detected")
                return {"status": "error", "message": "Model conflict detected but no files found to clean"}
        else:
            raise e
    
    # Evaluate model
    logger.info("Evaluating model...")
    evaluation = gluon.evaluate_models(test_data, target_column)
    
    # Make predictions
    logger.info("Making predictions...")
    predictions = gluon.predict(test_data)
    
    # Export model
    logger.info("Exporting model...")
    model_path = f"models/single_file_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    gluon.export_models(model_path)
    
    # Perform additional analysis based on type
    results = {
        "file_path": file_path,
        "analysis_type": analysis_type,
        "data_info": {
            "total_rows": len(data),
            "train_rows": len(train_data),
            "val_rows": len(val_data),
            "test_rows": len(test_data),
            "columns": list(data.columns)
        },
        "model_performance": evaluation,
        "predictions": predictions,
        "model_path": model_path
    }
    
    # Additional analysis
    if analysis_type in ["full", "backtest", "walk_forward", "monte_carlo"]:
        analyzer = ModelAnalyzer(model_path)
        if analyzer.load_model():
            
            if analysis_type in ["full", "backtest"]:
                logger.info("Performing backtesting analysis...")
                backtest_results = analyzer.backtest_analysis(test_data, target_column)
                results["backtest"] = backtest_results
            
            if analysis_type in ["full", "walk_forward"]:
                logger.info("Performing walk forward analysis...")
                walk_forward_results = analyzer.walk_forward_analysis(test_data, target_column)
                results["walk_forward"] = walk_forward_results
            
            if analysis_type in ["full", "monte_carlo"]:
                logger.info("Performing Monte Carlo analysis...")
                monte_carlo_results = analyzer.monte_carlo_analysis(test_data, target_column)
                results["monte_carlo"] = monte_carlo_results
    
    logger.info("Analysis completed successfully")
    return results


def main():
    """Main function for single file analysis."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Single File Analysis with AutoGluon")
    parser.add_argument("file_path", help="Path to the data file")
    parser.add_argument("--target", default="target", help="Target column name")
    parser.add_argument("--analysis", default="full", 
                       choices=["full", "quick", "backtest", "walk_forward", "monte_carlo"],
                       help="Type of analysis to perform")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file_path):
        logger.error(f"File not found: {args.file_path}")
        return
    
    # Perform analysis
    try:
        results = analyze_single_file(
            args.file_path, 
            args.target, 
            args.analysis
        )
        
        # Save results
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        
        # Print summary
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"File: {results['file_path']}")
        print(f"Analysis Type: {results['analysis_type']}")
        print(f"Data Rows: {results['data_info']['total_rows']}")
        print(f"Train/Val/Test: {results['data_info']['train_rows']}/{results['data_info']['val_rows']}/{results['data_info']['test_rows']}")
        
        if 'model_performance' in results:
            perf = results['model_performance']
            if 'accuracy' in perf:
                print(f"Accuracy: {perf['accuracy']:.4f}")
            if 'rmse' in perf:
                print(f"RMSE: {perf['rmse']:.4f}")
        
        print(f"Model saved to: {results['model_path']}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
