#!/usr/bin/env python3
"""
Isolated AutoGluon Trainer
Изолированный тренер AutoGluon

This script runs AutoGluon training in a completely isolated process
to avoid "Learner is already fit" errors.
"""

import sys
import os
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import pickle
import argparse
from tqdm import tqdm

# Add src to path
sys.path.insert(0, os.path.abspath('src'))

from automl.gluon.gluon import GluonAutoML
from automl.gluon.config import GluonConfig, ExperimentConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_model_isolated(train_data_path: str, val_data_path: str, 
                        target_column: str, model_path: str, 
                        config_path: str = None) -> bool:
    """
    Train AutoGluon model in isolated process.
    
    Args:
        train_data_path: Path to training data pickle file
        val_data_path: Path to validation data pickle file  
        target_column: Target column name
        model_path: Path to save model
        config_path: Path to config file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("🚀 Starting isolated AutoGluon training...")
        
        # Load data
        logger.info("📊 Loading training data...")
        with open(train_data_path, 'rb') as f:
            train_data = pickle.load(f)
        
        logger.info("📊 Loading validation data...")
        with open(val_data_path, 'rb') as f:
            val_data = pickle.load(f)
        
        logger.info(f"📊 Data loaded: Train={len(train_data)}, Val={len(val_data)}")
        
        # Create fresh GluonAutoML instance
        logger.info("🔄 Creating fresh GluonAutoML instance...")
        gluon = GluonAutoML()
        
        # Train model with simple progress indication
        logger.info("🤖 Training model...")
        
        # Simple progress indication without complex progress bar
        logger.info("🔄 Initializing AutoGluon...")
        gluon.train_models(train_data, target_column, val_data, model_path=model_path)
        logger.info("✅ AutoGluon training completed!")
        
        logger.info("✅ Model training completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        return False


def main():
    """Main function for isolated training."""
    parser = argparse.ArgumentParser(description='Isolated AutoGluon Training')
    parser.add_argument('--train-data', required=True, help='Path to training data pickle file')
    parser.add_argument('--val-data', required=True, help='Path to validation data pickle file')
    parser.add_argument('--target-column', required=True, help='Target column name')
    parser.add_argument('--model-path', required=True, help='Path to save model')
    parser.add_argument('--config-path', help='Path to config file')
    
    args = parser.parse_args()
    
    # Run training
    success = train_model_isolated(
        args.train_data,
        args.val_data, 
        args.target_column,
        args.model_path,
        args.config_path
    )
    
    if success:
        print("SUCCESS")
        sys.exit(0)
    else:
        print("FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
