"""
Simple unit tests for Self-Learning Engine - Docker-safe version

This module contains only basic tests with comprehensive mocking
to ensure fast execution and prevent hangs in Docker environment.
"""

import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock

from src.pocket_hedge_fund.autonomous_bot.self_learning_engine import (
    SelfLearningEngine,
    MetaLearner,
    TransferLearner,
    AutoML,
    NeuralArchitectureSearch,
    LearningConfig,
    LearningResult
)


class TestLearningConfig:
    """Test LearningConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = LearningConfig()
        
        assert config.meta_learning_enabled is True
        assert config.transfer_learning_enabled is True
        assert config.auto_ml_enabled is True
        assert config.nas_enabled is True
        assert config.learning_rate == 0.001
        assert config.batch_size == 32
        assert config.max_epochs == 100
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = LearningConfig(
            meta_learning_enabled=False,
            learning_rate=0.01,
            batch_size=64
        )
        
        assert config.meta_learning_enabled is False
        assert config.learning_rate == 0.01
        assert config.batch_size == 64


class TestLearningResult:
    """Test LearningResult dataclass."""
    
    def test_successful_result(self):
        """Test successful learning result."""
        result = LearningResult(
            success=True,
            model_performance={'r2': 0.95, 'mse': 0.05},
            learning_time=120.5,
            model_path="/path/to/model",
            model_type="RandomForestRegressor",
            learning_method="automl"
        )
        
        assert result.success is True
        assert result.model_performance['r2'] == 0.95
        assert result.learning_time == 120.5
        assert result.model_type == "RandomForestRegressor"
    
    def test_failed_result(self):
        """Test failed learning result."""
        result = LearningResult(
            success=False,
            model_performance={},
            learning_time=0.0,
            error_message="Insufficient data"
        )
        
        assert result.success is False
        assert result.error_message == "Insufficient data"


class TestMetaLearner:
    """Test MetaLearner with mocked operations."""
    
    def test_initialization(self):
        """Test MetaLearner initialization."""
        meta_learner = MetaLearner()
        assert meta_learner is not None
    
    def test_extract_task_features(self):
        """Test task feature extraction."""
        meta_learner = MetaLearner()
        task = {
            'market_data': pd.DataFrame({'close': [100, 101, 102]}),
            'performance': {'sharpe_ratio': 1.2, 'max_drawdown': 0.05},
            'strategy_params': {'risk_level': 0.02, 'position_size': 0.1}
        }
        
        features = meta_learner.extract_task_features(task)
        
        assert isinstance(features, dict)
        assert 'market_features' in features
        assert 'performance_features' in features
        assert 'strategy_features' in features
    
    def test_calculate_task_similarity(self):
        """Test task similarity calculation."""
        meta_learner = MetaLearner()
        task1_features = {'market_features': [1, 2, 3], 'performance_features': [0.5, 0.6]}
        task2_features = {'market_features': [1.1, 2.1, 3.1], 'performance_features': [0.52, 0.62]}
        
        similarity = meta_learner.calculate_task_similarity(task1_features, task2_features)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0


class TestTransferLearner:
    """Test TransferLearner with mocked operations."""
    
    def test_initialization(self):
        """Test TransferLearner initialization."""
        transfer_learner = TransferLearner()
        assert transfer_learner is not None
    
    def test_extract_domain_features(self):
        """Test domain feature extraction."""
        transfer_learner = TransferLearner()
        market_data = pd.DataFrame({
            'close': [100, 101, 102, 103, 104],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        features = transfer_learner.extract_domain_features(market_data)
        
        assert isinstance(features, dict)
        assert 'statistical_features' in features
        assert 'technical_features' in features


class TestAutoML:
    """Test AutoML with mocked operations."""
    
    def test_initialization(self):
        """Test AutoML initialization."""
        auto_ml = AutoML()
        assert auto_ml is not None
    
    def test_get_model_candidates(self):
        """Test model candidate generation."""
        auto_ml = AutoML()
        candidates = auto_ml.get_model_candidates()
        
        assert isinstance(candidates, list)
        assert len(candidates) > 0
    
    def test_calculate_rsi(self):
        """Test RSI calculation."""
        auto_ml = AutoML()
        prices = [100, 101, 102, 101, 100, 99, 98, 99, 100, 101]
        rsi = auto_ml.calculate_rsi(prices, period=5)
        
        assert isinstance(rsi, float)
        assert 0.0 <= rsi <= 100.0


class TestNeuralArchitectureSearch:
    """Test NeuralArchitectureSearch with mocked operations."""
    
    def test_initialization(self):
        """Test NeuralArchitectureSearch initialization."""
        nas = NeuralArchitectureSearch()
        assert nas is not None
    
    def test_generate_architecture_candidates(self):
        """Test architecture candidate generation."""
        nas = NeuralArchitectureSearch()
        candidates = nas.generate_architecture_candidates(num_candidates=3)
        
        assert isinstance(candidates, list)
        assert len(candidates) == 3


class TestSelfLearningEngine:
    """Test SelfLearningEngine with comprehensive mocking."""
    
    def test_initialization(self):
        """Test engine initialization."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        assert engine.config == config
        assert engine.meta_learner is not None
        assert engine.transfer_learner is not None
        assert engine.auto_ml is not None
        assert engine.nas is not None
        assert len(engine.current_models) == 0
    
    def test_get_learning_status(self):
        """Test learning status retrieval."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        status = engine.get_learning_status()
        
        assert isinstance(status, dict)
        assert 'total_learning_sessions' in status
        assert 'current_models_count' in status
        assert 'success_rate' in status
    
    def test_get_best_model_no_models(self):
        """Test getting best model when no models exist."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        best_model = engine.get_best_model()
        
        assert best_model is None
    
    def test_get_best_model_with_models(self):
        """Test getting best model when models exist."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        # Add mock models
        engine.current_models['model1'] = {
            'model': Mock(),
            'performance': {'r2': 0.8},
            'created_at': '2023-01-01'
        }
        engine.current_models['model2'] = {
            'model': Mock(),
            'performance': {'r2': 0.9},
            'created_at': '2023-01-02'
        }
        
        best_model = engine.get_best_model()
        
        assert best_model is not None
        assert best_model['performance']['r2'] == 0.9
    
    def test_export_learning_summary(self):
        """Test learning summary export."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        summary = engine.export_learning_summary()
        
        assert isinstance(summary, dict)
        assert 'total_sessions' in summary
        assert 'success_rate' in summary
        assert 'model_count' in summary
    
    @pytest.mark.asyncio
    async def test_learn_from_market_mocked(self):
        """Test learning from market data with mocked operations."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        # Mock all ML operations
        with patch.object(engine.auto_ml, 'search_models') as mock_search:
            mock_search.return_value = {
                'status': 'success',
                'best_model': 'RandomForestRegressor',
                'performance': {'r2': 0.95, 'mse': 0.05}
            }
            
            market_data = {
                'market_data': pd.DataFrame({'close': [100, 101, 102], 'volume': [1000, 1100, 1200]}),
                'target': 'close'
            }
            
            result = await engine.learn_from_market(market_data)
            
            assert result.success is True
            assert result.learning_time > 0
            assert result.model_type == 'RandomForestRegressor'
    
    @pytest.mark.asyncio
    async def test_optimize_strategy(self):
        """Test strategy optimization."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        performance_metrics = {
            'sharpe_ratio': 1.3,
            'max_drawdown': 0.06,
            'win_rate': 0.55,
            'profit_factor': 1.2
        }
        
        result = await engine.optimize_strategy(performance_metrics)
        
        assert result['status'] == 'success'
        assert 'optimized_parameters' in result
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_market_no_models(self):
        """Test adaptation to new market with no existing models."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        new_market_data = {
            'market_data': pd.DataFrame({'close': [110, 111, 112], 'volume': [2000, 2100, 2200]})
        }
        
        result = await engine.adapt_to_new_market(new_market_data)
        
        assert result['status'] == 'error'
        assert 'no models' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_market_with_models(self):
        """Test adaptation to new market with existing models."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        # Add a mock model
        engine.current_models['test_model'] = {
            'model': Mock(),
            'performance': {'r2': 0.9},
            'created_at': '2023-01-01'
        }
        
        new_market_data = {
            'market_data': pd.DataFrame({'close': [110, 111, 112], 'volume': [2000, 2100, 2200]})
        }
        
        result = await engine.adapt_to_new_market(new_market_data)
        
        assert result['status'] == 'success'
        assert 'adaptation_score' in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
