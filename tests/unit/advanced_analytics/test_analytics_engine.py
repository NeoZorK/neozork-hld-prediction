"""
Unit tests for Analytics Engine
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from decimal import Decimal

from src.pocket_hedge_fund.advanced_analytics.core.analytics_engine import AnalyticsEngine
from src.pocket_hedge_fund.advanced_analytics.models.analytics_models import (
    MarketData, DataFrequency, PredictionType
)


class TestAnalyticsEngine:
    """Test cases for Analytics Engine."""
    
    @pytest.fixture
    def mock_db_manager(self):
        """Mock database manager."""
        return AsyncMock()
    
    @pytest.fixture
    def analytics_engine(self, mock_db_manager):
        """Analytics engine instance."""
        return AnalyticsEngine(mock_db_manager)
    
    @pytest.fixture
    def sample_market_data(self):
        """Sample market data for testing."""
        return [
            MarketData(
                symbol='BTC',
                timestamp=datetime.now() - timedelta(days=2),
                open_price=Decimal('50000.00'),
                high_price=Decimal('51000.00'),
                low_price=Decimal('49000.00'),
                close_price=Decimal('50500.00'),
                volume=Decimal('1000.0'),
                frequency=DataFrequency.DAILY
            ),
            MarketData(
                symbol='BTC',
                timestamp=datetime.now() - timedelta(days=1),
                open_price=Decimal('50500.00'),
                high_price=Decimal('52000.00'),
                low_price=Decimal('50000.00'),
                close_price=Decimal('51500.00'),
                volume=Decimal('1200.0'),
                frequency=DataFrequency.DAILY
            ),
            MarketData(
                symbol='BTC',
                timestamp=datetime.now(),
                open_price=Decimal('51500.00'),
                high_price=Decimal('53000.00'),
                low_price=Decimal('51000.00'),
                close_price=Decimal('52500.00'),
                volume=Decimal('1100.0'),
                frequency=DataFrequency.DAILY
            )
        ]
    
    @pytest.mark.asyncio
    async def test_initialize_success(self, analytics_engine):
        """Test successful analytics engine initialization."""
        # Mock the initialization methods
        with patch.object(analytics_engine.data_processor, 'initialize') as mock_dp_init, \
             patch.object(analytics_engine.feature_engineer, 'initialize') as mock_fe_init, \
             patch.object(analytics_engine.insight_generator, 'initialize') as mock_ig_init, \
             patch.object(analytics_engine, '_load_models') as mock_load_models:
            
            # Act
            await analytics_engine.initialize()
            
            # Assert
            mock_dp_init.assert_called_once()
            mock_fe_init.assert_called_once()
            mock_ig_init.assert_called_once()
            mock_load_models.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_initialize_failure(self, analytics_engine):
        """Test analytics engine initialization failure."""
        # Mock initialization failure
        with patch.object(analytics_engine.data_processor, 'initialize', side_effect=Exception("Init failed")):
            
            # Act & Assert
            with pytest.raises(Exception, match="Init failed"):
                await analytics_engine.initialize()
    
    @pytest.mark.asyncio
    async def test_process_market_data_success(self, analytics_engine, sample_market_data):
        """Test successful market data processing."""
        # Mock data processor
        with patch.object(analytics_engine.data_processor, 'get_market_data', return_value=sample_market_data) as mock_get_data, \
             patch.object(analytics_engine.data_processor, 'clean_data', return_value=sample_market_data) as mock_clean_data:
            
            # Act
            result = await analytics_engine.process_market_data(
                symbol='BTC',
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now(),
                frequency=DataFrequency.DAILY
            )
            
            # Assert
            assert result == sample_market_data
            mock_get_data.assert_called_once()
            mock_clean_data.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_market_data_failure(self, analytics_engine):
        """Test market data processing failure."""
        # Mock data processor failure
        with patch.object(analytics_engine.data_processor, 'get_market_data', side_effect=Exception("Data error")):
            
            # Act & Assert
            with pytest.raises(Exception, match="Data error"):
                await analytics_engine.process_market_data(
                    symbol='BTC',
                    start_date=datetime.now() - timedelta(days=30),
                    end_date=datetime.now()
                )
    
    @pytest.mark.asyncio
    async def test_generate_features_success(self, analytics_engine, sample_market_data):
        """Test successful feature generation."""
        # Mock feature engineer
        mock_features = {
            'sma_20': [50000.0, 50500.0, 51500.0],
            'rsi': [45.0, 55.0, 65.0],
            'macd': [100.0, 150.0, 200.0]
        }
        
        with patch.object(analytics_engine.feature_engineer, 'generate_features', return_value=mock_features) as mock_generate:
            
            # Act
            result = await analytics_engine.generate_features(sample_market_data)
            
            # Assert
            assert result == mock_features
            mock_generate.assert_called_once_with(sample_market_data, ['technical', 'statistical', 'momentum'])
    
    @pytest.mark.asyncio
    async def test_generate_features_with_types(self, analytics_engine, sample_market_data):
        """Test feature generation with specific types."""
        # Mock feature engineer
        mock_features = {'technical': {}, 'statistical': {}}
        
        with patch.object(analytics_engine.feature_engineer, 'generate_features', return_value=mock_features) as mock_generate:
            
            # Act
            result = await analytics_engine.generate_features(
                sample_market_data, 
                feature_types=['technical', 'statistical']
            )
            
            # Assert
            assert result == mock_features
            mock_generate.assert_called_once_with(sample_market_data, ['technical', 'statistical'])
    
    @pytest.mark.asyncio
    async def test_make_prediction_success(self, analytics_engine):
        """Test successful prediction generation."""
        # Mock prediction result
        mock_prediction = MagicMock()
        mock_prediction.symbol = 'BTC'
        mock_prediction.prediction_type = PredictionType.PRICE
        mock_prediction.predicted_value = Decimal('53000.00')
        mock_prediction.confidence = Decimal('0.85')
        
        # Mock price predictor
        with patch.object(analytics_engine.price_predictor, 'predict', return_value=mock_prediction) as mock_predict:
            
            # Act
            result = await analytics_engine.make_prediction(
                symbol='BTC',
                prediction_type=PredictionType.PRICE,
                horizon=1
            )
            
            # Assert
            assert result == mock_prediction
            mock_predict.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_make_prediction_with_features(self, analytics_engine):
        """Test prediction with custom features."""
        # Mock prediction result
        mock_prediction = MagicMock()
        mock_prediction.symbol = 'BTC'
        mock_prediction.prediction_type = PredictionType.VOLATILITY
        mock_prediction.predicted_value = Decimal('0.25')
        mock_prediction.confidence = Decimal('0.75')
        
        # Mock volatility predictor
        with patch.object(analytics_engine.volatility_predictor, 'predict', return_value=mock_prediction) as mock_predict:
            
            # Act
            result = await analytics_engine.make_prediction(
                symbol='BTC',
                prediction_type=PredictionType.VOLATILITY,
                horizon=1,
                features={'volatility_lag1': 0.2, 'volume_ratio': 1.5}
            )
            
            # Assert
            assert result == mock_prediction
            mock_predict.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_make_prediction_unsupported_type(self, analytics_engine):
        """Test prediction with unsupported type."""
        # Act & Assert
        with pytest.raises(ValueError, match="Unsupported prediction type"):
            await analytics_engine.make_prediction(
                symbol='BTC',
                prediction_type='unsupported_type',  # This should be a valid PredictionType
                horizon=1
            )
    
    @pytest.mark.asyncio
    async def test_generate_insights_success(self, analytics_engine, sample_market_data):
        """Test successful insight generation."""
        # Mock insights
        mock_insights = [
            MagicMock(),
            MagicMock()
        ]
        
        # Mock insight generator
        with patch.object(analytics_engine.insight_generator, 'generate_insights', return_value=mock_insights) as mock_generate:
            
            # Act
            result = await analytics_engine.generate_insights('BTC', sample_market_data)
            
            # Assert
            assert result == mock_insights
            mock_generate.assert_called_once_with('BTC', sample_market_data, None)
    
    @pytest.mark.asyncio
    async def test_generate_insights_with_predictions(self, analytics_engine, sample_market_data):
        """Test insight generation with predictions."""
        # Mock insights and predictions
        mock_insights = [MagicMock()]
        mock_predictions = [MagicMock()]
        
        # Mock insight generator
        with patch.object(analytics_engine.insight_generator, 'generate_insights', return_value=mock_insights) as mock_generate:
            
            # Act
            result = await analytics_engine.generate_insights('BTC', sample_market_data, mock_predictions)
            
            # Assert
            assert result == mock_insights
            mock_generate.assert_called_once_with('BTC', sample_market_data, mock_predictions)
    
    @pytest.mark.asyncio
    async def test_evaluate_model_performance_success(self, analytics_engine, sample_market_data):
        """Test successful model performance evaluation."""
        # Mock model performance
        mock_performance = MagicMock()
        mock_performance.model_id = 'test_model'
        mock_performance.metrics = {'accuracy': 0.85, 'mse': 0.01}
        
        # Mock model evaluator
        with patch.object(analytics_engine.model_evaluator, 'evaluate_model', return_value=mock_performance) as mock_evaluate:
            
            # Act
            result = await analytics_engine.evaluate_model_performance('test_model', sample_market_data)
            
            # Assert
            assert result == mock_performance
            mock_evaluate.assert_called_once_with('test_model', sample_market_data)
    
    @pytest.mark.asyncio
    async def test_run_comprehensive_analysis_success(self, analytics_engine, sample_market_data):
        """Test successful comprehensive analysis."""
        # Mock all components
        mock_features = {'sma_20': [50000.0, 50500.0, 51500.0]}
        mock_price_prediction = MagicMock()
        mock_volatility_prediction = MagicMock()
        mock_insights = [MagicMock()]
        
        with patch.object(analytics_engine, 'process_market_data', return_value=sample_market_data) as mock_process, \
             patch.object(analytics_engine, 'generate_features', return_value=mock_features) as mock_features_gen, \
             patch.object(analytics_engine, 'make_prediction', side_effect=[mock_price_prediction, mock_volatility_prediction]) as mock_predict, \
             patch.object(analytics_engine, 'generate_insights', return_value=mock_insights) as mock_insights_gen:
            
            # Act
            result = await analytics_engine.run_comprehensive_analysis('BTC', 30)
            
            # Assert
            assert result['symbol'] == 'BTC'
            assert result['market_data'] == sample_market_data
            assert result['features'] == mock_features
            assert result['predictions']['price'] == mock_price_prediction
            assert result['predictions']['volatility'] == mock_volatility_prediction
            assert result['insights'] == mock_insights
            assert 'analysis_timestamp' in result
    
    @pytest.mark.asyncio
    async def test_run_comprehensive_analysis_failure(self, analytics_engine):
        """Test comprehensive analysis failure."""
        # Mock failure in process_market_data
        with patch.object(analytics_engine, 'process_market_data', side_effect=Exception("Processing error")):
            
            # Act & Assert
            with pytest.raises(Exception, match="Processing error"):
                await analytics_engine.run_comprehensive_analysis('BTC', 30)
    
    @pytest.mark.asyncio
    async def test_cleanup_success(self, analytics_engine):
        """Test successful cleanup."""
        # Mock cleanup methods
        with patch.object(analytics_engine.data_processor, 'cleanup') as mock_dp_cleanup, \
             patch.object(analytics_engine.feature_engineer, 'cleanup') as mock_fe_cleanup, \
             patch.object(analytics_engine.insight_generator, 'cleanup') as mock_ig_cleanup:
            
            # Act
            await analytics_engine.cleanup()
            
            # Assert
            mock_dp_cleanup.assert_called_once()
            mock_fe_cleanup.assert_called_once()
            mock_ig_cleanup.assert_called_once()
            assert len(analytics_engine._data_cache) == 0
            assert len(analytics_engine._feature_cache) == 0
    
    @pytest.mark.asyncio
    async def test_load_models_success(self, analytics_engine):
        """Test successful model loading."""
        # Mock model loading
        with patch.object(analytics_engine.price_predictor, 'load_model') as mock_price_load, \
             patch.object(analytics_engine.volatility_predictor, 'load_model') as mock_vol_load:
            
            # Act
            await analytics_engine._load_models()
            
            # Assert
            mock_price_load.assert_called_once()
            mock_vol_load.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_load_models_partial_failure(self, analytics_engine):
        """Test partial model loading failure."""
        # Mock partial failure
        with patch.object(analytics_engine.price_predictor, 'load_model') as mock_price_load, \
             patch.object(analytics_engine.volatility_predictor, 'load_model', side_effect=Exception("Load failed")):
            
            # Act - should not raise exception
            await analytics_engine._load_models()
            
            # Assert
            mock_price_load.assert_called_once()
