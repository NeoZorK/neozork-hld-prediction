"""
Fast unit tests for Self-Learning Engine with comprehensive mocking

This module tests all components of the self-learning engine using mocks
to avoid long-running computations and prevent test hangs.
"""

import pytest
import numpy as np
import pandas as pd
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil
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
        assert config.few_shot_enabled is True
        assert config.learning_rate == 0.001
        assert config.batch_size == 32
        assert config.max_epochs == 100
        assert config.early_stopping_patience == 10
        assert config.model_save_path == "models/self_learning"
        assert config.max_models_in_memory == 10
        assert config.cross_validation_folds == 5
        assert config.hyperparameter_search_iterations == 50
        assert config.meta_learning_tasks_threshold == 5
        assert config.transfer_learning_similarity_threshold == 0.7
        assert config.performance_improvement_threshold == 0.05
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = LearningConfig(
            meta_learning_enabled=False,
            learning_rate=0.01,
            batch_size=64,
            model_save_path="/custom/path"
        )
        
        assert config.meta_learning_enabled is False
        assert config.learning_rate == 0.01
        assert config.batch_size == 64
        assert config.model_save_path == "/custom/path"


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
        assert result.model_path == "/path/to/model"
        assert result.model_type == "RandomForestRegressor"
        assert result.learning_method == "automl"
        assert result.error_message is None
    
    def test_failed_result(self):
        """Test failed learning result."""
        result = LearningResult(
            success=False,
            model_performance={},
            learning_time=0.0,
            error_message="Insufficient data"
        )
        
        assert result.success is False
        assert result.model_performance == {}
        assert result.learning_time == 0.0
        assert result.error_message == "Insufficient data"


class TestMetaLearner:
    """Test MetaLearner with mocked operations."""
    
    @pytest.fixture
    def meta_learner(self):
        """Create MetaLearner instance."""
        return MetaLearner()
    
    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        return [
            {
                'market_data': pd.DataFrame({'close': [100, 101, 102]}),
                'performance': {'sharpe_ratio': 1.2, 'max_drawdown': 0.05},
                'strategy_params': {'risk_level': 0.02, 'position_size': 0.1}
            },
            {
                'market_data': pd.DataFrame({'close': [102, 103, 104]}),
                'performance': {'sharpe_ratio': 1.4, 'max_drawdown': 0.04},
                'strategy_params': {'risk_level': 0.018, 'position_size': 0.12}
            }
        ]
    
    def test_extract_task_features(self, meta_learner, sample_tasks):
        """Test task feature extraction."""
        features = meta_learner.extract_task_features(sample_tasks[0])
        
        assert isinstance(features, dict)
        assert 'market_features' in features
        assert 'performance_features' in features
        assert 'strategy_features' in features
    
    def test_calculate_task_similarity(self, meta_learner):
        """Test task similarity calculation."""
        task1_features = {'market_features': [1, 2, 3], 'performance_features': [0.5, 0.6]}
        task2_features = {'market_features': [1.1, 2.1, 3.1], 'performance_features': [0.52, 0.62]}
        
        similarity = meta_learner.calculate_task_similarity(task1_features, task2_features)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_calculate_task_similarity_different_lengths(self, meta_learner):
        """Test task similarity with different feature lengths."""
        task1_features = {'market_features': [1, 2, 3], 'performance_features': [0.5, 0.6]}
        task2_features = {'market_features': [1.1, 2.1], 'performance_features': [0.52]}
        
        similarity = meta_learner.calculate_task_similarity(task1_features, task2_features)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    @pytest.mark.asyncio
    async def test_learn_from_tasks_success(self, meta_learner, sample_tasks):
        """Test successful learning from tasks."""
        result = await meta_learner.learn_from_tasks(sample_tasks)
        
        assert result['status'] == 'success'
        assert 'meta_knowledge' in result
    
    @pytest.mark.asyncio
    async def test_learn_from_tasks_insufficient_data(self, meta_learner):
        """Test learning from tasks with insufficient data."""
        result = await meta_learner.learn_from_tasks([])
        
        assert result['status'] == 'error'
        assert 'insufficient' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_task_success(self, meta_learner, sample_tasks):
        """Test successful adaptation to new task."""
        # First learn from existing tasks
        await meta_learner.learn_from_tasks(sample_tasks)
        
        new_task = {
            'market_data': pd.DataFrame({'close': [105, 106, 107]}),
            'performance': {'sharpe_ratio': 1.6, 'max_drawdown': 0.03},
            'strategy_params': {'risk_level': 0.015, 'position_size': 0.15}
        }
        
        result = await meta_learner.adapt_to_new_task(new_task)
        
        assert result['status'] == 'success'
        assert 'adaptation_recommendations' in result
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_task_no_meta_knowledge(self, meta_learner):
        """Test adaptation without meta knowledge."""
        new_task = {
            'market_data': pd.DataFrame({'close': [105, 106, 107]}),
            'performance': {'sharpe_ratio': 1.6, 'max_drawdown': 0.03},
            'strategy_params': {'risk_level': 0.015, 'position_size': 0.15}
        }
        
        result = await meta_learner.adapt_to_new_task(new_task)
        
        assert result['status'] == 'error'
        assert 'no meta knowledge' in result['error'].lower()


class TestTransferLearner:
    """Test TransferLearner with mocked operations."""
    
    @pytest.fixture
    def transfer_learner(self):
        """Create TransferLearner instance."""
        return TransferLearner()
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        return pd.DataFrame({
            'close': [100, 101, 102, 103, 104],
            'volume': [1000, 1100, 1200, 1300, 1400]
        })
    
    def test_extract_domain_features(self, transfer_learner, sample_market_data):
        """Test domain feature extraction."""
        features = transfer_learner.extract_domain_features(sample_market_data)
        
        assert isinstance(features, dict)
        assert 'statistical_features' in features
        assert 'technical_features' in features
    
    def test_calculate_domain_similarity(self, transfer_learner, sample_market_data):
        """Test domain similarity calculation."""
        features1 = transfer_learner.extract_domain_features(sample_market_data)
        features2 = transfer_learner.extract_domain_features(sample_market_data * 1.1)
        
        similarity = transfer_learner.calculate_domain_similarity(features1, features2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_prepare_transfer_data(self, transfer_learner, sample_market_data):
        """Test transfer data preparation."""
        prepared_data = transfer_learner.prepare_transfer_data(sample_market_data)
        
        assert isinstance(prepared_data, dict)
        assert 'X' in prepared_data
        assert 'y' in prepared_data
    
    @pytest.mark.asyncio
    async def test_transfer_knowledge_success(self, transfer_learner, sample_market_data):
        """Test successful knowledge transfer."""
        source_model = {
            'model': Mock(),
            'training_data': sample_market_data.iloc[:3]
        }
        
        target_data = {
            'market_data': sample_market_data.iloc[2:]
        }
        
        result = await transfer_learner.transfer_knowledge(
            'source_domain', 'target_domain', source_model, target_data
        )
        
        assert result['status'] == 'success'
        assert 'transferred_model' in result
        assert 'domain_similarity' in result
    
    @pytest.mark.asyncio
    async def test_fine_tune_model_success(self, transfer_learner, sample_market_data):
        """Test successful model fine-tuning."""
        mock_model = Mock()
        target_data = {
            'market_data': sample_market_data
        }
        
        result = await transfer_learner.fine_tune_model(mock_model, target_data)
        
        assert result['status'] == 'success'
        assert 'fine_tuned_model' in result


class TestAutoML:
    """Test AutoML with mocked operations."""
    
    @pytest.fixture
    def auto_ml(self):
        """Create AutoML instance."""
        return AutoML()
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        return pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
    
    def test_get_model_candidates(self, auto_ml):
        """Test model candidate generation."""
        candidates = auto_ml.get_model_candidates()
        
        assert isinstance(candidates, list)
        assert len(candidates) > 0
    
    def test_prepare_data(self, auto_ml, sample_market_data):
        """Test data preparation."""
        prepared_data = auto_ml.prepare_data(sample_market_data, 'close')
        
        assert isinstance(prepared_data, dict)
        assert 'X' in prepared_data
        assert 'y' in prepared_data
    
    def test_calculate_rsi(self, auto_ml):
        """Test RSI calculation."""
        prices = [100, 101, 102, 101, 100, 99, 98, 99, 100, 101]
        rsi = auto_ml.calculate_rsi(prices, period=5)
        
        assert isinstance(rsi, float)
        assert 0.0 <= rsi <= 100.0
    
    @pytest.mark.asyncio
    async def test_search_models_success(self, auto_ml, sample_market_data):
        """Test successful model search."""
        result = await auto_ml.search_models(sample_market_data, 'close')
        
        assert result['status'] == 'success'
        assert 'best_model' in result
        assert 'performance' in result
    
    @pytest.mark.asyncio
    async def test_search_models_insufficient_data(self, auto_ml):
        """Test model search with insufficient data."""
        small_data = pd.DataFrame({'close': [100, 101], 'volume': [1000, 1100]})
        
        result = await auto_ml.search_models(small_data, 'close')
        
        assert result['status'] == 'error'
        assert 'insufficient' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_optimize_hyperparameters_success(self, auto_ml, sample_market_data):
        """Test successful hyperparameter optimization."""
        mock_model = Mock()
        
        result = await auto_ml.optimize_hyperparameters(mock_model, sample_market_data, 'close')
        
        assert result['status'] == 'success'
        assert 'optimized_parameters' in result
    
    def test_get_model_recommendations(self, auto_ml):
        """Test model recommendations."""
        recommendations = auto_ml.get_model_recommendations()
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0


class TestNeuralArchitectureSearch:
    """Test NeuralArchitectureSearch with mocked operations."""
    
    @pytest.fixture
    def nas(self):
        """Create NeuralArchitectureSearch instance."""
        return NeuralArchitectureSearch()
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        return pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
    
    def test_generate_architecture_candidates(self, nas):
        """Test architecture candidate generation."""
        candidates = nas.generate_architecture_candidates(num_candidates=3)
        
        assert isinstance(candidates, list)
        assert len(candidates) == 3
    
    def test_evaluate_architecture(self, nas, sample_market_data):
        """Test architecture evaluation."""
        architecture = {
            'layers': [64, 32, 16],
            'activation': 'relu',
            'dropout': 0.2
        }
        
        score = nas.evaluate_architecture(architecture, sample_market_data, 'close')
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0
    
    @pytest.mark.asyncio
    async def test_search_architecture_success(self, nas, sample_market_data):
        """Test successful architecture search."""
        result = await nas.search_architecture(sample_market_data, 'close')
        
        assert result['status'] == 'success'
        assert 'best_architecture' in result
        assert 'performance_score' in result
    
    @pytest.mark.asyncio
    async def test_evolve_architecture_success(self, nas):
        """Test successful architecture evolution."""
        parent_architectures = [
            {'layers': [64, 32], 'activation': 'relu'},
            {'layers': [32, 16], 'activation': 'tanh'}
        ]
        
        result = await nas.evolve_architecture(parent_architectures)
        
        assert result['status'] == 'success'
        assert 'evolved_architectures' in result
    
    def test_get_architecture_recommendations(self, nas):
        """Test architecture recommendations."""
        recommendations = nas.get_architecture_recommendations()
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0


class TestSelfLearningEngine:
    """Test SelfLearningEngine with comprehensive mocking."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LearningConfig(
            meta_learning_enabled=True,
            transfer_learning_enabled=True,
            auto_ml_enabled=True,
            nas_enabled=True,
            max_epochs=10,  # Reduced for faster testing
            hyperparameter_search_iterations=5  # Reduced for faster testing
        )
    
    @pytest.fixture
    def engine(self, config):
        """Create SelfLearningEngine instance."""
        return SelfLearningEngine(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        return pd.DataFrame({
            'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109],
            'volume': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        })
    
    @pytest.fixture
    def realistic_market_data(self):
        """Create realistic market data for testing."""
        dates = pd.date_range(start='2023-01-01', periods=500, freq='D')
        prices = 100 + np.cumsum(np.random.randn(500) * 0.5)
        volume = 1000 + np.random.randn(500) * 100
        
        return pd.DataFrame({
            'close': prices,
            'volume': volume
        }, index=dates)
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_initialization(self, engine, config):
        """Test engine initialization."""
        assert engine.config == config
        assert engine.meta_learner is not None
        assert engine.transfer_learner is not None
        assert engine.auto_ml is not None
        assert engine.nas is not None
        assert len(engine.current_models) == 0
    
    @pytest.mark.asyncio
    async def test_learn_from_market_automl_only(self, engine, sample_market_data):
        """Test learning from market data using AutoML only."""
        with patch.object(engine.auto_ml, 'search_models') as mock_search:
            mock_search.return_value = {
                'status': 'success',
                'best_model': 'RandomForestRegressor',
                'performance': {'r2': 0.95, 'mse': 0.05}
            }
            
            market_data = {
                'market_data': sample_market_data,
                'target': 'close'
            }
            
            result = await engine.learn_from_market(market_data)
            
            assert result.success is True
            assert result.learning_time > 0
            assert result.model_type == 'RandomForestRegressor'
    
    @pytest.mark.asyncio
    async def test_learn_from_market_with_tasks(self, engine, sample_market_data):
        """Test learning from market data with tasks."""
        with patch.object(engine.auto_ml, 'search_models') as mock_search, \
             patch.object(engine.meta_learner, 'learn_from_tasks') as mock_meta:
            
            mock_search.return_value = {
                'status': 'success',
                'best_model': 'RandomForestRegressor',
                'performance': {'r2': 0.95, 'mse': 0.05}
            }
            mock_meta.return_value = {
                'status': 'success',
                'meta_knowledge': {'task_similarity': 0.8}
            }
            
            tasks = [
                {
                    'market_data': sample_market_data.iloc[:5],
                    'performance': {'sharpe_ratio': 1.2},
                    'strategy_params': {'risk_level': 0.02}
                }
            ]
            
            market_data = {
                'market_data': sample_market_data,
                'target': 'close',
                'tasks': tasks
            }
            
            result = await engine.learn_from_market(market_data)
            
            assert result.success is True
            assert result.learning_time > 0
    
    @pytest.mark.asyncio
    async def test_optimize_strategy(self, engine):
        """Test strategy optimization."""
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
    async def test_adapt_to_new_market_no_models(self, engine, sample_market_data):
        """Test adaptation to new market with no existing models."""
        new_market_data = {
            'market_data': sample_market_data * 1.1
        }
        
        result = await engine.adapt_to_new_market(new_market_data)
        
        assert result['status'] == 'error'
        assert 'no models' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_market_with_models(self, engine, sample_market_data):
        """Test adaptation to new market with existing models."""
        # Add a mock model
        engine.current_models['test_model'] = {
            'model': Mock(),
            'performance': {'r2': 0.9},
            'created_at': datetime.now()
        }
        
        new_market_data = {
            'market_data': sample_market_data * 1.1
        }
        
        result = await engine.adapt_to_new_market(new_market_data)
        
        assert result['status'] == 'success'
        assert 'adaptation_score' in result
    
    def test_get_learning_status(self, engine):
        """Test learning status retrieval."""
        status = engine.get_learning_status()
        
        assert isinstance(status, dict)
        assert 'total_learning_sessions' in status
        assert 'current_models_count' in status
        assert 'success_rate' in status
    
    def test_get_best_model_no_models(self, engine):
        """Test getting best model when no models exist."""
        best_model = engine.get_best_model()
        
        assert best_model is None
    
    def test_get_best_model_with_models(self, engine):
        """Test getting best model when models exist."""
        # Add mock models
        engine.current_models['model1'] = {
            'model': Mock(),
            'performance': {'r2': 0.8},
            'created_at': datetime.now()
        }
        engine.current_models['model2'] = {
            'model': Mock(),
            'performance': {'r2': 0.9},
            'created_at': datetime.now()
        }
        
        best_model = engine.get_best_model()
        
        assert best_model is not None
        assert best_model['performance']['r2'] == 0.9
    
    def test_cleanup_old_models(self, engine):
        """Test cleanup of old models."""
        # Add old models
        old_time = datetime.now() - timedelta(days=2)
        engine.current_models['old_model'] = {
            'model': Mock(),
            'performance': {'r2': 0.8},
            'created_at': old_time
        }
        
        engine.cleanup_old_models()
        
        assert 'old_model' not in engine.current_models
    
    def test_export_learning_summary(self, engine):
        """Test learning summary export."""
        summary = engine.export_learning_summary()
        
        assert isinstance(summary, dict)
        assert 'total_sessions' in summary
        assert 'success_rate' in summary
        assert 'model_count' in summary
    
    @pytest.mark.asyncio
    async def test_complete_learning_workflow(self, engine, realistic_market_data):
        """Test complete learning workflow with mocked ML operations."""
        with patch.object(engine.auto_ml, 'search_models') as mock_search, \
             patch.object(engine.auto_ml, 'optimize_hyperparameters') as mock_optimize, \
             patch.object(engine, 'adapt_to_new_market') as mock_adapt:
            
            # Setup mocks
            mock_search.return_value = {
                'status': 'success',
                'best_model': 'RandomForestRegressor',
                'performance': {'r2': 0.95, 'mse': 0.05}
            }
            mock_optimize.return_value = {
                'status': 'success',
                'optimized_parameters': {'n_estimators': 100, 'max_depth': 10}
            }
            mock_adapt.return_value = {
                'status': 'success',
                'adaptation_score': 0.85
            }
            
            # Step 1: Learn from market data
            market_data = {
                'market_data': realistic_market_data,
                'target': 'close'
            }
            
            learning_result = await engine.learn_from_market(market_data)
            
            assert learning_result.success is True
            assert learning_result.learning_time > 0
            
            # Step 2: Optimize strategy based on performance
            performance_metrics = {
                'sharpe_ratio': 1.3,
                'max_drawdown': 0.06,
                'win_rate': 0.55,
                'profit_factor': 1.2
            }
            
            optimization_result = await engine.optimize_strategy(performance_metrics)
            
            assert optimization_result['status'] == 'success'
            assert 'optimized_parameters' in optimization_result
            
            # Step 3: Adapt to new market conditions
            new_market_data = realistic_market_data * 1.05  # 5% different market
            adaptation_result = await engine.adapt_to_new_market({'market_data': new_market_data})
            
            assert adaptation_result['status'] == 'success'
            
            # Step 4: Check learning status
            status = engine.get_learning_status()
            
            assert status['total_learning_sessions'] >= 1
            assert status['current_models_count'] >= 0
            assert status['success_rate'] >= 0
    
    @pytest.mark.asyncio
    async def test_meta_learning_workflow(self, engine, realistic_market_data):
        """Test meta-learning workflow with mocked operations."""
        with patch.object(engine.meta_learner, 'learn_from_tasks') as mock_learn, \
             patch.object(engine.meta_learner, 'adapt_to_new_task') as mock_adapt:
            
            # Setup mocks
            mock_learn.return_value = {
                'status': 'success',
                'meta_knowledge': {'task_similarity': 0.8, 'performance_patterns': {}}
            }
            mock_adapt.return_value = {
                'status': 'success',
                'adaptation_recommendations': {'risk_level': 0.018, 'position_size': 0.12}
            }
            
            # Create multiple tasks for meta-learning
            tasks = []
            for i in range(3):
                start_idx = i * 100
                end_idx = (i + 1) * 100
                task_data = realistic_market_data.iloc[start_idx:end_idx]
                
                task = {
                    'market_data': task_data,
                    'performance': {
                        'sharpe_ratio': 1.0 + i * 0.2,
                        'max_drawdown': 0.05 + i * 0.01,
                        'win_rate': 0.5 + i * 0.05,
                        'profit_factor': 1.1 + i * 0.1
                    },
                    'strategy_params': {
                        'risk_level': 0.02 - i * 0.001,
                        'position_size': 0.1 + i * 0.01,
                        'stop_loss': 0.05 - i * 0.005,
                        'take_profit': 0.1 + i * 0.01
                    }
                }
                tasks.append(task)
            
            # Learn from tasks
            market_data = {
                'market_data': realistic_market_data,
                'target': 'close',
                'tasks': tasks
            }
            
            result = await engine.learn_from_market(market_data)
            
            assert result.success is True
            
            # Test adaptation to new task
            new_task = {
                'market_data': realistic_market_data.iloc[400:500],
                'performance': {'sharpe_ratio': 1.4, 'max_drawdown': 0.04},
                'strategy_params': {'risk_level': 0.018, 'position_size': 0.12}
            }
            
            adaptation_result = await engine.meta_learner.adapt_to_new_task(new_task)
            
            assert adaptation_result['status'] == 'success'
            assert 'adaptation_recommendations' in adaptation_result
    
    @pytest.mark.asyncio
    async def test_transfer_learning_workflow(self, engine, realistic_market_data):
        """Test transfer learning workflow with mocked operations."""
        with patch.object(engine.transfer_learner, 'transfer_knowledge') as mock_transfer, \
             patch.object(engine.transfer_learner, 'fine_tune_model') as mock_finetune:
            
            # Setup mocks
            mock_transfer.return_value = {
                'status': 'success',
                'transferred_model': 'MockModel',
                'domain_similarity': 0.75
            }
            mock_finetune.return_value = {
                'status': 'success',
                'fine_tuned_model': 'FineTunedModel'
            }
            
            # Create source model
            from sklearn.ensemble import RandomForestRegressor
            source_model = {
                'model': RandomForestRegressor(n_estimators=20, random_state=42),
                'training_data': realistic_market_data.iloc[:200]
            }
            
            # Create target data (different market conditions)
            target_data = {
                'market_data': realistic_market_data.iloc[200:400] * 1.1
            }
            
            # Perform transfer learning
            transfer_result = await engine.transfer_learner.transfer_knowledge(
                'source_domain', 'target_domain', source_model, target_data
            )
            
            assert transfer_result['status'] == 'success'
            assert 'transferred_model' in transfer_result
            assert 'domain_similarity' in transfer_result
            
            # Test fine-tuning
            fine_tune_result = await engine.transfer_learner.fine_tune_model(
                source_model['model'], target_data
            )
            
            assert fine_tune_result['status'] == 'success'
            assert 'fine_tuned_model' in fine_tune_result
    
    def test_model_persistence(self, engine, realistic_market_data, temp_dir):
        """Test model saving and loading."""
        # Create a simple model
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        
        # Train the model
        X = realistic_market_data[['volume']].values
        y = realistic_market_data['close'].values
        model.fit(X, y)
        
        # Save model
        model_id = "test_model"
        model_path = engine._save_model(model, model_id, "test_method")
        
        assert model_path is not None
        assert Path(model_path).exists()
        
        # Load model
        loaded_model = engine._load_model(model_path)
        
        assert loaded_model is not None
        assert hasattr(loaded_model, 'predict')


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
