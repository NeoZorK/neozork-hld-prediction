"""
Analytics Engine

Main orchestrator for analytics operations.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from decimal import Decimal

from ..models.analytics_models import (
    MarketData, PredictionResult, AnalyticsInsight,
    ModelPerformance, DataFrequency, PredictionType
)
from .data_processor import DataProcessor
from .feature_engineer import FeatureEngineer
from .insight_generator import InsightGenerator
from ..ml.prediction_models import PricePredictor, VolatilityPredictor
from ..ml.model_evaluator import ModelEvaluator

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Main analytics engine that orchestrates all analytics operations.
    """
    
    def __init__(self, db_manager=None):
        """Initialize analytics engine."""
        self.db_manager = db_manager
        self.data_processor = DataProcessor(db_manager)
        self.feature_engineer = FeatureEngineer()
        self.insight_generator = InsightGenerator()
        self.model_evaluator = ModelEvaluator()
        
        # ML models
        self.price_predictor = PricePredictor()
        self.volatility_predictor = VolatilityPredictor()
        
        # Cache for processed data
        self._data_cache = {}
        self._feature_cache = {}
        
    async def initialize(self):
        """Initialize the analytics engine."""
        try:
            await self.data_processor.initialize()
            await self.feature_engineer.initialize()
            await self.insight_generator.initialize()
            
            # Load pre-trained models
            await self._load_models()
            
            logger.info("Analytics engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize analytics engine: {e}")
            raise
    
    async def _load_models(self):
        """Load pre-trained ML models."""
        try:
            await self.price_predictor.load_model()
            await self.volatility_predictor.load_model()
            logger.info("ML models loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load some models: {e}")
    
    async def process_market_data(
        self,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        frequency: DataFrequency = DataFrequency.DAILY
    ) -> List[MarketData]:
        """
        Process and clean market data for analysis.
        
        Args:
            symbol: Asset symbol
            start_date: Start date for data
            end_date: End date for data
            frequency: Data frequency
            
        Returns:
            List of processed market data
        """
        try:
            # Get raw data
            raw_data = await self.data_processor.get_market_data(
                symbol, start_date, end_date, frequency
            )
            
            # Clean and validate data
            cleaned_data = await self.data_processor.clean_data(raw_data)
            
            # Cache processed data
            cache_key = f"{symbol}_{start_date}_{end_date}_{frequency}"
            self._data_cache[cache_key] = cleaned_data
            
            return cleaned_data
            
        except Exception as e:
            logger.error(f"Failed to process market data for {symbol}: {e}")
            raise
    
    async def generate_features(
        self,
        market_data: List[MarketData],
        feature_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate features from market data.
        
        Args:
            market_data: List of market data
            feature_types: Types of features to generate
            
        Returns:
            Dictionary of generated features
        """
        try:
            if feature_types is None:
                feature_types = ['technical', 'statistical', 'momentum']
            
            features = await self.feature_engineer.generate_features(
                market_data, feature_types
            )
            
            # Cache features
            cache_key = f"features_{hash(str(market_data))}"
            self._feature_cache[cache_key] = features
            
            return features
            
        except Exception as e:
            logger.error(f"Failed to generate features: {e}")
            raise
    
    async def make_prediction(
        self,
        symbol: str,
        prediction_type: PredictionType,
        horizon: int = 1,
        features: Dict[str, Any] = None
    ) -> PredictionResult:
        """
        Make prediction using ML models.
        
        Args:
            symbol: Asset symbol
            prediction_type: Type of prediction
            horizon: Prediction horizon
            features: Features for prediction
            
        Returns:
            Prediction result
        """
        try:
            if prediction_type == PredictionType.PRICE:
                predictor = self.price_predictor
            elif prediction_type == PredictionType.VOLATILITY:
                predictor = self.volatility_predictor
            else:
                raise ValueError(f"Unsupported prediction type: {prediction_type}")
            
            # Get latest market data if features not provided
            if features is None:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=365)
                market_data = await self.process_market_data(
                    symbol, start_date, end_date
                )
                features = await self.generate_features(market_data)
            
            # Make prediction
            prediction = await predictor.predict(features, horizon)
            
            return prediction
            
        except Exception as e:
            logger.error(f"Failed to make prediction for {symbol}: {e}")
            raise
    
    async def generate_insights(
        self,
        symbol: str,
        market_data: List[MarketData] = None,
        predictions: List[PredictionResult] = None
    ) -> List[AnalyticsInsight]:
        """
        Generate actionable insights.
        
        Args:
            symbol: Asset symbol
            market_data: Market data for analysis
            predictions: Model predictions
            
        Returns:
            List of generated insights
        """
        try:
            # Get market data if not provided
            if market_data is None:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                market_data = await self.process_market_data(
                    symbol, start_date, end_date
                )
            
            # Generate insights
            insights = await self.insight_generator.generate_insights(
                symbol, market_data, predictions
            )
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate insights for {symbol}: {e}")
            raise
    
    async def evaluate_model_performance(
        self,
        model_id: str,
        test_data: List[MarketData]
    ) -> ModelPerformance:
        """
        Evaluate model performance.
        
        Args:
            model_id: Model identifier
            test_data: Test data for evaluation
            
        Returns:
            Model performance metrics
        """
        try:
            performance = await self.model_evaluator.evaluate_model(
                model_id, test_data
            )
            return performance
            
        except Exception as e:
            logger.error(f"Failed to evaluate model {model_id}: {e}")
            raise
    
    async def run_comprehensive_analysis(
        self,
        symbol: str,
        analysis_period: int = 30
    ) -> Dict[str, Any]:
        """
        Run comprehensive analysis for a symbol.
        
        Args:
            symbol: Asset symbol
            analysis_period: Analysis period in days
            
        Returns:
            Comprehensive analysis results
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=analysis_period)
            
            # Process market data
            market_data = await self.process_market_data(
                symbol, start_date, end_date
            )
            
            # Generate features
            features = await self.generate_features(market_data)
            
            # Make predictions
            price_prediction = await self.make_prediction(
                symbol, PredictionType.PRICE
            )
            volatility_prediction = await self.make_prediction(
                symbol, PredictionType.VOLATILITY
            )
            
            # Generate insights
            insights = await self.generate_insights(
                symbol, market_data, [price_prediction, volatility_prediction]
            )
            
            return {
                'symbol': symbol,
                'market_data': market_data,
                'features': features,
                'predictions': {
                    'price': price_prediction,
                    'volatility': volatility_prediction
                },
                'insights': insights,
                'analysis_timestamp': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Failed to run comprehensive analysis for {symbol}: {e}")
            raise
    
    async def cleanup(self):
        """Cleanup resources."""
        try:
            await self.data_processor.cleanup()
            await self.feature_engineer.cleanup()
            await self.insight_generator.cleanup()
            
            # Clear caches
            self._data_cache.clear()
            self._feature_cache.clear()
            
            logger.info("Analytics engine cleanup completed")
        except Exception as e:
            logger.error(f"Error during analytics engine cleanup: {e}")
