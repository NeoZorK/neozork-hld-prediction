# -*- coding: utf-8 -*-
"""
AutoGluon predictor wrapper.

This module provides prediction capabilities using trained AutoGluon models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List, Union
import logging
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


class GluonPredictor:
    """AutoGluon predictor wrapper."""
    
    def __init__(self, predictor: TabularPredictor):
        """
        Initialize Gluon predictor.
        
        Args:
            predictor: Trained TabularPredictor
        """
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
        
        self.predictor = predictor
        
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions on new data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Predictions DataFrame
        """
        logger.info(f"Making predictions on {len(data)} samples...")
        
        # Make predictions
        predictions = self.predictor.predict(data)
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'predictions': predictions
        }, index=data.index)
        
        logger.info("Predictions completed successfully")
        return results_df
    
    def predict_proba(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make probability predictions on new data.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Probability predictions DataFrame
        """
        logger.info(f"Making probability predictions on {len(data)} samples...")
        
        # Make probability predictions
        proba_predictions = self.predictor.predict_proba(data)
        
        # Create results DataFrame
        results_df = pd.DataFrame(proba_predictions, index=data.index)
        
        logger.info("Probability predictions completed successfully")
        return results_df
    
    def predict_with_confidence(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Make predictions with confidence intervals.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Predictions with confidence DataFrame
        """
        logger.info(f"Making predictions with confidence on {len(data)} samples...")
        
        # Make predictions
        predictions = self.predictor.predict(data)
        
        # Get probability predictions for confidence
        proba_predictions = self.predictor.predict_proba(data)
        
        # Calculate confidence (max probability)
        confidence = proba_predictions.max(axis=1)
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'predictions': predictions,
            'confidence': confidence
        }, index=data.index)
        
        logger.info("Predictions with confidence completed successfully")
        return results_df
    
    def get_feature_contributions(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Get feature contributions for predictions.
        
        Args:
            data: Input data for prediction
            
        Returns:
            Feature contributions DataFrame
        """
        logger.info(f"Getting feature contributions for {len(data)} samples...")
        
        try:
            # Get feature contributions
            contributions = self.predictor.explain_prediction(data)
            
            logger.info("Feature contributions retrieved successfully")
            return contributions
            
        except Exception as e:
            logger.warning(f"Could not get feature contributions: {e}")
            return pd.DataFrame()
    
    def batch_predict(self, data: pd.DataFrame, batch_size: int = 1000) -> pd.DataFrame:
        """
        Make predictions in batches for large datasets.
        
        Args:
            data: Input data for prediction
            batch_size: Batch size for processing
            
        Returns:
            Predictions DataFrame
        """
        logger.info(f"Making batch predictions on {len(data)} samples with batch size {batch_size}...")
        
        all_predictions = []
        
        # Process in batches
        for i in range(0, len(data), batch_size):
            batch_data = data.iloc[i:i + batch_size]
            batch_predictions = self.predict(batch_data)
            all_predictions.append(batch_predictions)
        
        # Combine results
        results_df = pd.concat(all_predictions, ignore_index=False)
        
        logger.info("Batch predictions completed successfully")
        return results_df
