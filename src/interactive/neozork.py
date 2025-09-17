#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NeoZork Interactive ML Trading Strategy Development System

A comprehensive interactive system for developing robust profitable ML model strategies
for trading on blockchains, deploying on CEX and DEX, and monitoring with retraining.

Features:
- Interactive modern colorful menus
- Data loading from multiple sources (CSV, Parquet, APIs)
- EDA analysis with comprehensive data quality checks
- Feature engineering with premium indicators (PHLD, PV, SR, WAVE)
- ML model development with Apple MLX
- Monte Carlo simulations and Walk Forward optimization
- Real-time monitoring and retraining capabilities

Usage:
    python neozork.py
    ./neozork.py
    uv run neozork.py
"""

import sys
import os
import time
import signal
from pathlib import Path
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import project modules
from src.common.logger import print_info, print_warning, print_error, print_success, print_debug
from src.interactive.menu_system import InteractiveMenuSystem
from src.interactive.data_management import DataLoader
from src.interactive.eda_analysis import EDAAnalyzer
from src.interactive.feature_engineering import FeatureEngineer
from src.interactive.ml_development import MLDeveloper
from src.interactive.monitoring import MonitoringSystem
from src.interactive.probability_methods import BayesianInference, MonteCarloRisk
from src.interactive.apple_mlx import MLXTrainer
from src.interactive.advanced_ml import DeepReinforcementLearning, EnsembleLearning
from src.interactive.containerization import AppleContainerManager

class NeoZorkInteractiveSystem:
    """
    Main interactive system for ML trading strategy development.
    
    This class orchestrates the entire workflow from data loading to model deployment
    and monitoring, providing a comprehensive platform for developing profitable
    trading strategies using machine learning.
    """
    
    def __init__(self):
        """Initialize the NeoZork Interactive System."""
        self.project_root = PROJECT_ROOT
        self.data_loader = DataLoader()
        self.eda_analyzer = EDAAnalyzer()
        self.feature_engineer = FeatureEngineer()
        self.ml_developer = MLDeveloper()
        self.monitoring_system = MonitoringSystem()
        self.current_data = None
        self.current_features = None
        self.current_model = None
        
        # Setup signal handlers for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print_success("🚀 NeoZork Interactive ML Trading Strategy Development System")
        print_info("Initialized successfully!")
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals for graceful exit."""
        print_warning("\n🛑 Interrupt received. Exiting gracefully...")
        self._cleanup()
        sys.exit(0)
    
    def _cleanup(self):
        """Cleanup resources before exit."""
        print_info("🧹 Cleaning up resources...")
        # Add cleanup logic here if needed
        print_success("✅ Cleanup completed")
    
    def run(self):
        """Run the main interactive system."""
        try:
            menu_system = InteractiveMenuSystem()
            menu_system.run()
        except KeyboardInterrupt:
            print_warning("\n🛑 User interrupted. Exiting...")
            self._cleanup()
        except Exception as e:
            print_error(f"❌ Unexpected error: {e}")
            self._cleanup()
            raise

def main():
    """Main entry point for the NeoZork Interactive System."""
    try:
        system = NeoZorkInteractiveSystem()
        system.run()
    except Exception as e:
        print_error(f"❌ Failed to start NeoZork Interactive System: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
