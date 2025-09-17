"""
Minimal unit tests for Self-Learning Engine - Docker-safe version

This module contains only basic tests with comprehensive mocking
to ensure fast execution and prevent hangs in Docker environment.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch

from src.pocket_hedge_fund.autonomous_bot.self_learning_engine import (
    SelfLearningEngine,
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
    
    def test_export_learning_summary(self):
        """Test learning summary export."""
        config = LearningConfig()
        engine = SelfLearningEngine(config)
        
        summary = engine.export_learning_summary()
        
        assert isinstance(summary, dict)
        assert 'learning_history' in summary
        assert 'current_models' in summary
        assert 'export_timestamp' in summary
    
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
        assert 'error' in result or 'message' in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])