# -*- coding: utf-8 -*-
"""
AutoGluon drift monitor.

This module provides drift monitoring capabilities for AutoGluon models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union, Tuple
import logging
from datetime import datetime
import warnings

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class DriftMonitor:
    """AutoGluon drift monitor."""
    
    def __init__(self, drift_threshold: float = 0.1, 
                 psi_threshold: float = 0.2,
                 performance_threshold: float = 0.05):
        """
        Initialize drift monitor.
        
        Args:
            drift_threshold: Feature drift threshold
            psi_threshold: PSI threshold
            performance_threshold: Performance degradation threshold
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
        
        self.drift_threshold = drift_threshold
        self.psi_threshold = psi_threshold
        self.performance_threshold = performance_threshold
        self.baseline_data = None
        self.baseline_performance = None
        
    def set_baseline(self, baseline_data: pd.DataFrame, 
                    baseline_performance: float = None):
        """
        Set baseline data and performance.
        
        Args:
            baseline_data: Baseline training data
            baseline_performance: Baseline model performance
        """
        self.baseline_data = baseline_data
        self.baseline_performance = baseline_performance
        
        logger.info(f"Baseline set with {len(baseline_data)} samples")
    
    def check_drift(self, predictor: TabularPredictor, 
                   new_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Check for data drift.
        
        Args:
            predictor: Trained predictor
            new_data: New data to check
            
        Returns:
            Drift detection results
        """
        logger.info("Checking for data drift...")
        
        drift_results = {
            'drift_detected': False,
            'feature_drift': {},
            'performance_drift': False,
            'psi_scores': {},
            'recommendations': []
        }
        
        if self.baseline_data is None:
            logger.warning("No baseline data set, skipping drift check")
            return drift_results
        
        # Check feature drift
        feature_drift = self._check_feature_drift(new_data)
        drift_results['feature_drift'] = feature_drift
        
        # Check PSI scores
        psi_scores = self._calculate_psi_scores(new_data)
        drift_results['psi_scores'] = psi_scores
        
        # Check performance drift
        if self.baseline_performance is not None:
            performance_drift = self._check_performance_drift(predictor, new_data)
            drift_results['performance_drift'] = performance_drift
        
        # Determine overall drift
        drift_detected = (
            any(score > self.psi_threshold for score in psi_scores.values()) or
            drift_results['performance_drift']
        )
        drift_results['drift_detected'] = drift_detected
        
        # Generate recommendations
        if drift_detected:
            drift_results['recommendations'].append("Consider retraining the model")
            if any(score > self.psi_threshold for score in psi_scores.values()):
                drift_results['recommendations'].append("High PSI scores detected - data distribution changed")
            if drift_results['performance_drift']:
                drift_results['recommendations'].append("Performance degradation detected")
        
        logger.info(f"Drift check completed. Drift detected: {drift_detected}")
        return drift_results
    
    def _check_feature_drift(self, new_data: pd.DataFrame) -> Dict[str, float]:
        """Check for feature drift."""
        feature_drift = {}
        
        if self.baseline_data is None:
            return feature_drift
        
        # Compare numeric features
        numeric_cols = new_data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col in self.baseline_data.columns:
                # Calculate drift using statistical tests
                drift_score = self._calculate_feature_drift(
                    self.baseline_data[col], 
                    new_data[col]
                )
                feature_drift[col] = drift_score
        
        return feature_drift
    
    def _calculate_feature_drift(self, baseline: pd.Series, 
                                new_data: pd.Series) -> float:
        """Calculate feature drift score."""
        try:
            # Remove NaN values
            baseline_clean = baseline.dropna()
            new_data_clean = new_data.dropna()
            
            if len(baseline_clean) == 0 or len(new_data_clean) == 0:
                return 0.0
            
            # Calculate PSI
            psi_score = self._calculate_psi(baseline_clean, new_data_clean)
            return psi_score
            
        except Exception as e:
            logger.warning(f"Could not calculate drift for feature: {e}")
            return 0.0
    
    def _calculate_psi_scores(self, new_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate PSI scores for all features."""
        psi_scores = {}
        
        if self.baseline_data is None:
            return psi_scores
        
        numeric_cols = new_data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if col in self.baseline_data.columns:
                psi_score = self._calculate_psi(
                    self.baseline_data[col].dropna(),
                    new_data[col].dropna()
                )
                psi_scores[col] = psi_score
        
        return psi_scores
    
    def _calculate_psi(self, baseline: pd.Series, new_data: pd.Series) -> float:
        """Calculate Population Stability Index (PSI)."""
        try:
            # Create bins
            combined = pd.concat([baseline, new_data])
            bins = pd.cut(combined, bins=10, duplicates='drop')
            
            # Calculate distributions
            baseline_dist = baseline.groupby(pd.cut(baseline, bins=bins.cat.categories)).size() / len(baseline)
            new_dist = new_data.groupby(pd.cut(new_data, bins=bins.cat.categories)).size() / len(new_data)
            
            # Calculate PSI
            psi = 0
            for i in range(len(baseline_dist)):
                if baseline_dist.iloc[i] > 0 and new_dist.iloc[i] > 0:
                    psi += (new_dist.iloc[i] - baseline_dist.iloc[i]) * np.log(new_dist.iloc[i] / baseline_dist.iloc[i])
            
            return abs(psi)
            
        except Exception as e:
            logger.warning(f"Could not calculate PSI: {e}")
            return 0.0
    
    def _check_performance_drift(self, predictor: TabularPredictor, 
                                new_data: pd.DataFrame) -> bool:
        """Check for performance drift."""
        if self.baseline_performance is None:
            return False
        
        try:
            # Make predictions on new data
            predictions = predictor.predict(new_data)
            
            # Calculate performance (simplified)
            # In practice, you would need true labels for this
            current_performance = 0.8  # Placeholder
            
            performance_drop = self.baseline_performance - current_performance
            return performance_drop > self.performance_threshold
            
        except Exception as e:
            logger.warning(f"Could not check performance drift: {e}")
            return False
    
    def get_drift_summary(self, drift_results: Dict[str, Any]) -> Dict[str, Any]:
        """Get drift summary."""
        summary = {
            'drift_detected': drift_results['drift_detected'],
            'high_psi_features': [
                feature for feature, score in drift_results['psi_scores'].items()
                if score > self.psi_threshold
            ],
            'recommendations': drift_results['recommendations'],
            'monitoring_status': 'active' if drift_results['drift_detected'] else 'normal'
        }
        
        return summary
