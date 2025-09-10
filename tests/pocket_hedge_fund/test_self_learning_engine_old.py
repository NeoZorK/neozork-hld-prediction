"""
Comprehensive unit tests for Self-Learning Engine

This module tests all components of the self-learning engine including:
- Meta-learning functionality
- Transfer learning capabilities
- AutoML model selection
- Neural Architecture Search
- Integration and performance tests
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
        assert result.model_path is None


class TestMetaLearner:
    """Test MetaLearner component."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LearningConfig(meta_learning_tasks_threshold=3)
    
    @pytest.fixture
    def meta_learner(self, config):
        """Create MetaLearner instance."""
        return MetaLearner(config)
    
    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        # Create sample market data
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data1 = pd.DataFrame({
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
        
        data2 = pd.DataFrame({
            'close': np.random.randn(100).cumsum() + 200,
            'volume': np.random.randint(2000, 20000, 100)
        }, index=dates)
        
        return [
            {
                'market_data': data1,
                'performance': {'sharpe_ratio': 1.5, 'max_drawdown': 0.05, 'win_rate': 0.6, 'profit_factor': 1.3},
                'strategy_params': {'risk_level': 0.02, 'position_size': 0.1, 'stop_loss': 0.05, 'take_profit': 0.1}
            },
            {
                'market_data': data2,
                'performance': {'sharpe_ratio': 2.0, 'max_drawdown': 0.03, 'win_rate': 0.7, 'profit_factor': 1.5},
                'strategy_params': {'risk_level': 0.015, 'position_size': 0.12, 'stop_loss': 0.04, 'take_profit': 0.12}
            },
            {
                'market_data': data1,
                'performance': {'sharpe_ratio': 1.8, 'max_drawdown': 0.04, 'win_rate': 0.65, 'profit_factor': 1.4},
                'strategy_params': {'risk_level': 0.018, 'position_size': 0.11, 'stop_loss': 0.045, 'take_profit': 0.11}
            }
        ]
    
    def test_extract_task_features(self, meta_learner, sample_tasks):
        """Test task feature extraction."""
        task = sample_tasks[0]
        features = meta_learner._extract_task_features(task)
        
        assert isinstance(features, np.ndarray)
        assert len(features) > 0
        assert not np.isnan(features).any()
    
    def test_calculate_task_similarity(self, meta_learner):
        """Test task similarity calculation."""
        features1 = np.array([1.0, 2.0, 3.0, 4.0])
        features2 = np.array([1.1, 2.1, 3.1, 4.1])
        
        similarity = meta_learner._calculate_task_similarity(features1, features2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0.9  # Should be very similar
    
    def test_calculate_task_similarity_different_lengths(self, meta_learner):
        """Test task similarity with different feature lengths."""
        features1 = np.array([1.0, 2.0, 3.0])
        features2 = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        
        similarity = meta_learner._calculate_task_similarity(features1, features2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    @pytest.mark.asyncio
    async def test_learn_from_tasks_success(self, meta_learner, sample_tasks):
        """Test successful meta-learning from tasks."""
        result = await meta_learner.learn_from_tasks(sample_tasks)
        
        assert result['status'] == 'success'
        assert 'meta_model' in result
        assert 'tasks_processed' in result
        assert result['tasks_processed'] == len(sample_tasks)
        assert meta_learner.meta_knowledge is not None
    
    @pytest.mark.asyncio
    async def test_learn_from_tasks_insufficient_data(self, meta_learner):
        """Test meta-learning with insufficient tasks."""
        tasks = [{'market_data': pd.DataFrame({'close': [1, 2, 3]})}]
        
        result = await meta_learner.learn_from_tasks(tasks)
        
        assert result['status'] == 'insufficient_data'
        assert 'message' in result
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_task_success(self, meta_learner, sample_tasks):
        """Test successful task adaptation."""
        # First learn from tasks
        await meta_learner.learn_from_tasks(sample_tasks)
        
        # Then adapt to new task
        new_task = {
            'market_data': pd.DataFrame({
                'close': np.random.randn(50).cumsum() + 150,
                'volume': np.random.randint(1500, 15000, 50)
            }),
            'performance': {'sharpe_ratio': 1.2, 'max_drawdown': 0.06},
            'strategy_params': {'risk_level': 0.025, 'position_size': 0.08}
        }
        
        result = await meta_learner.adapt_to_new_task(new_task)
        
        assert result['status'] == 'success'
        assert 'adaptation_recommendations' in result
        assert 'confidence' in result['adaptation_recommendations']
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_task_no_meta_knowledge(self, meta_learner):
        """Test task adaptation without meta-knowledge."""
        new_task = {'market_data': pd.DataFrame({'close': [1, 2, 3]})}
        
        result = await meta_learner.adapt_to_new_task(new_task)
        
        assert result['status'] == 'no_meta_knowledge'
        assert 'message' in result


class TestTransferLearner:
    """Test TransferLearner component."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LearningConfig(transfer_learning_similarity_threshold=0.5)
    
    @pytest.fixture
    def transfer_learner(self, config):
        """Create TransferLearner instance."""
        return TransferLearner(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        dates = pd.date_range('2023-01-01', periods=200, freq='D')
        return pd.DataFrame({
            'close': np.random.randn(200).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 200)
        }, index=dates)
    
    def test_extract_domain_features(self, transfer_learner, sample_market_data):
        """Test domain feature extraction."""
        data = {'market_data': sample_market_data}
        features = transfer_learner._extract_domain_features(data)
        
        assert isinstance(features, np.ndarray)
        assert len(features) > 0
        assert not np.isnan(features).any()
    
    def test_calculate_domain_similarity(self, transfer_learner, sample_market_data):
        """Test domain similarity calculation."""
        data1 = {'market_data': sample_market_data}
        data2 = {'market_data': sample_market_data * 1.1}  # Slightly different
        
        similarity = transfer_learner._calculate_domain_similarity(data1, data2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
    
    def test_prepare_transfer_data(self, transfer_learner, sample_market_data):
        """Test data preparation for transfer learning."""
        source_model = {'training_data': sample_market_data}
        target_data = {'market_data': sample_market_data}
        
        X, y = transfer_learner._prepare_transfer_data(source_model, target_data)
        
        assert isinstance(X, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert X.shape[0] == y.shape[0]
        assert X.shape[0] > 0
    
    @pytest.mark.asyncio
    async def test_transfer_knowledge_success(self, transfer_learner, sample_market_data):
        """Test successful knowledge transfer."""
        # Create source model
        from sklearn.ensemble import RandomForestRegressor
        source_model = {
            'model': RandomForestRegressor(n_estimators=10, random_state=42),
            'training_data': sample_market_data
        }
        
        # Create target data
        target_data = {'market_data': sample_market_data}
        
        result = await transfer_learner.transfer_knowledge(
            'source_domain', 'target_domain', source_model, target_data
        )
        
        assert result['status'] == 'success'
        assert 'transferred_model' in result
        assert 'domain_similarity' in result
        assert 'performance' in result
    
    @pytest.mark.asyncio
    async def test_fine_tune_model_success(self, transfer_learner, sample_market_data):
        """Test successful model fine-tuning."""
        from sklearn.ensemble import RandomForestRegressor
        base_model = RandomForestRegressor(n_estimators=10, random_state=42)
        target_data = {'market_data': sample_market_data}
        
        result = await transfer_learner.fine_tune_model(base_model, target_data)
        
        assert result['status'] == 'success'
        assert 'fine_tuned_model' in result
        assert 'performance' in result
        assert 'data_size' in result


class TestAutoML:
    """Test AutoML component."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LearningConfig(cross_validation_folds=3)
    
    @pytest.fixture
    def auto_ml(self, config):
        """Create AutoML instance."""
        return AutoML(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        return pd.DataFrame({
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    def test_get_model_candidates(self, auto_ml):
        """Test model candidates generation."""
        candidates = auto_ml._get_model_candidates()
        
        assert isinstance(candidates, list)
        assert len(candidates) > 0
        
        for name, model, params in candidates:
            assert isinstance(name, str)
            assert hasattr(model, 'fit')
            assert isinstance(params, dict)
    
    def test_prepare_data(self, auto_ml, sample_market_data):
        """Test data preparation for AutoML."""
        data = {'market_data': sample_market_data}
        
        X, y, feature_names = auto_ml._prepare_data(data, 'close')
        
        assert isinstance(X, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert isinstance(feature_names, list)
        assert X.shape[0] == y.shape[0]
        assert X.shape[1] == len(feature_names)
        assert X.shape[0] > 0
    
    def test_calculate_rsi(self, auto_ml):
        """Test RSI calculation."""
        prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])
        rsi = auto_ml._calculate_rsi(prices, window=5)
        
        assert isinstance(rsi, pd.Series)
        assert len(rsi) == len(prices)
        assert not rsi.iloc[5:].isna().all()  # Should have some valid values after window
    
    @pytest.mark.asyncio
    async def test_search_models_success(self, auto_ml, sample_market_data):
        """Test successful model search."""
        data = {'market_data': sample_market_data}
        
        result = await auto_ml.search_models(data, 'close')
        
        assert result['status'] == 'success'
        assert 'best_model' in result
        assert 'performance' in result
        assert 'all_results' in result
        assert 'feature_names' in result
    
    @pytest.mark.asyncio
    async def test_search_models_insufficient_data(self, auto_ml):
        """Test model search with insufficient data."""
        data = {'market_data': pd.DataFrame({'close': [1, 2, 3]})}
        
        result = await auto_ml.search_models(data, 'close')
        
        assert result['status'] == 'error'
        assert 'message' in result
    
    @pytest.mark.asyncio
    async def test_optimize_hyperparameters_success(self, auto_ml, sample_market_data):
        """Test successful hyperparameter optimization."""
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(random_state=42)
        data = {'market_data': sample_market_data}
        
        result = await auto_ml.optimize_hyperparameters(model, data)
        
        assert result['status'] == 'success'
        assert 'optimized_model' in result
        assert 'best_params' in result
        assert 'best_score' in result
    
    def test_get_model_recommendations(self, auto_ml):
        """Test model recommendations."""
        data_characteristics = {
            'size': 500,
            'features': 10,
            'noise': 'medium'
        }
        
        recommendations = auto_ml.get_model_recommendations(data_characteristics)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert 'model' in rec
            assert 'reason' in rec
            assert 'confidence' in rec


class TestNeuralArchitectureSearch:
    """Test NeuralArchitectureSearch component."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return LearningConfig()
    
    @pytest.fixture
    def nas(self, config):
        """Create NeuralArchitectureSearch instance."""
        return NeuralArchitectureSearch(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data for testing."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        return pd.DataFrame({
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 100)
        }, index=dates)
    
    def test_generate_architecture_candidates(self, nas):
        """Test architecture candidate generation."""
        input_size = 10
        constraints = {'max_layers': 4, 'max_neurons': 100, 'min_neurons': 5}
        
        candidates = nas._generate_architecture_candidates(input_size, constraints)
        
        assert isinstance(candidates, list)
        assert len(candidates) > 0
        
        for candidate in candidates:
            assert 'layers' in candidate
            assert 'activation' in candidate
            assert 'alpha' in candidate
            assert candidate['layers'][0] == input_size
            assert candidate['layers'][-1] == 1  # Output layer
    
    def test_evaluate_architecture(self, nas, sample_market_data):
        """Test architecture evaluation."""
        # Prepare data
        df_features = sample_market_data.copy()
        df_features['returns'] = df_features['close'].pct_change()
        df_features['sma_5'] = df_features['close'].rolling(5).mean()
        df_features = df_features.dropna()
        
        X = df_features[['returns', 'sma_5']].values
        y = df_features['close'].values
        
        architecture = {
            'layers': [2, 10, 1],
            'activation': 'relu',
            'alpha': 0.001
        }
        
        score = nas._evaluate_architecture(architecture, X, y)
        
        assert isinstance(score, float)
        assert not np.isnan(score)
    
    @pytest.mark.asyncio
    async def test_search_architecture_success(self, nas, sample_market_data):
        """Test successful architecture search."""
        data = {'market_data': sample_market_data}
        constraints = {'max_layers': 4, 'max_neurons': 50}
        
        result = await nas.search_architecture(data, constraints)
        
        assert result['status'] == 'success'
        assert 'best_architecture' in result
        assert 'performance' in result
        assert 'all_results' in result
        assert 'input_size' in result
    
    @pytest.mark.asyncio
    async def test_evolve_architecture_success(self, nas):
        """Test successful architecture evolution."""
        current_architecture = {
            'layers': [10, 50, 1],
            'activation': 'relu',
            'alpha': 0.001
        }
        performance_feedback = 0.6
        
        result = await nas.evolve_architecture(current_architecture, performance_feedback)
        
        assert result['status'] == 'success'
        assert 'evolved_architecture' in result
        assert 'evolution_record' in result
    
    def test_get_architecture_recommendations(self, nas):
        """Test architecture recommendations."""
        data_characteristics = {
            'size': 1000,
            'features': 15
        }
        
        recommendations = nas.get_architecture_recommendations(data_characteristics)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        for rec in recommendations:
            assert 'architecture' in rec
            assert 'reason' in rec
            assert 'confidence' in rec


class TestSelfLearningEngine:
    """Test SelfLearningEngine integration."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def config(self, temp_dir):
        """Create test configuration with temp directory."""
        return LearningConfig(
            model_save_path=temp_dir,
            meta_learning_tasks_threshold=2,
            cross_validation_folds=3
        )
    
    @pytest.fixture
    def engine(self, config):
        """Create SelfLearningEngine instance."""
        return SelfLearningEngine(config)
    
    @pytest.fixture
    def sample_market_data(self):
        """Create sample market data."""
        dates = pd.date_range('2023-01-01', periods=200, freq='D')
        return pd.DataFrame({
            'close': np.random.randn(200).cumsum() + 100,
            'volume': np.random.randint(1000, 10000, 200)
        }, index=dates)
    
    def test_initialization(self, engine, config):
        """Test engine initialization."""
        assert engine.config == config
        assert isinstance(engine.meta_learner, MetaLearner)
        assert isinstance(engine.transfer_learner, TransferLearner)
        assert isinstance(engine.auto_ml, AutoML)
        assert isinstance(engine.nas, NeuralArchitectureSearch)
        assert engine.learning_history == []
        assert engine.current_models == {}
        assert engine.model_storage_path.exists()
    
    @pytest.mark.asyncio
    async def test_learn_from_market_automl_only(self, engine, sample_market_data):
        """Test learning from market data using AutoML only."""
        market_data = {
            'market_data': sample_market_data,
            'target': 'close'
        }
        
        result = await engine.learn_from_market(market_data)
        
        assert isinstance(result, LearningResult)
        assert result.success is True
        assert result.learning_time > 0
        assert result.model_performance is not None
        assert result.learning_method is not None
    
    @pytest.mark.asyncio
    async def test_learn_from_market_with_tasks(self, engine, sample_market_data):
        """Test learning from market data with tasks for meta-learning."""
        tasks = [
            {
                'market_data': sample_market_data.iloc[:100],
                'performance': {'sharpe_ratio': 1.5, 'max_drawdown': 0.05},
                'strategy_params': {'risk_level': 0.02, 'position_size': 0.1}
            },
            {
                'market_data': sample_market_data.iloc[100:],
                'performance': {'sharpe_ratio': 2.0, 'max_drawdown': 0.03},
                'strategy_params': {'risk_level': 0.015, 'position_size': 0.12}
            }
        ]
        
        market_data = {
            'market_data': sample_market_data,
            'target': 'close',
            'tasks': tasks
        }
        
        result = await engine.learn_from_market(market_data)
        
        assert isinstance(result, LearningResult)
        assert result.success is True
        assert len(engine.learning_history) == 1
        assert len(engine.current_models) > 0
    
    @pytest.mark.asyncio
    async def test_optimize_strategy(self, engine):
        """Test strategy optimization."""
        performance_metrics = {
            'sharpe_ratio': 1.2,
            'max_drawdown': 0.08,
            'win_rate': 0.45,
            'profit_factor': 1.1,
            'risk_level': 0.02,
            'position_size': 0.1,
            'stop_loss': 0.05,
            'take_profit': 0.1
        }
        
        result = await engine.optimize_strategy(performance_metrics)
        
        assert result['status'] == 'success'
        assert 'optimized_parameters' in result
        assert 'expected_improvement' in result
        assert 'optimization_reasons' in result
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_market_no_models(self, engine, sample_market_data):
        """Test market adaptation with no existing models."""
        market_conditions = {'market_data': sample_market_data}
        
        result = await engine.adapt_to_new_market(market_conditions)
        
        assert result['status'] == 'error'
        assert 'message' in result
    
    @pytest.mark.asyncio
    async def test_adapt_to_new_market_with_models(self, engine, sample_market_data):
        """Test market adaptation with existing models."""
        # First learn from market data to create models
        market_data = {'market_data': sample_market_data, 'target': 'close'}
        await engine.learn_from_market(market_data)
        
        # Then adapt to new market conditions
        new_market_data = sample_market_data * 1.1  # Slightly different market
        market_conditions = {'market_data': new_market_data}
        
        result = await engine.adapt_to_new_market(market_conditions)
        
        assert result['status'] == 'success'
        assert 'fine_tuned_model' in result
        assert 'performance' in result
    
    def test_get_learning_status(self, engine):
        """Test learning status retrieval."""
        status = engine.get_learning_status()
        
        assert isinstance(status, dict)
        assert 'total_learning_sessions' in status
        assert 'successful_sessions' in status
        assert 'success_rate' in status
        assert 'current_models_count' in status
        assert 'config' in status
    
    def test_get_best_model_no_models(self, engine):
        """Test getting best model when no models exist."""
        result = engine.get_best_model()
        
        assert result is None
    
    def test_get_best_model_with_models(self, engine):
        """Test getting best model when models exist."""
        # Add some mock models
        engine.current_models = {
            'model1': {'performance': 0.8, 'timestamp': datetime.now()},
            'model2': {'performance': 0.9, 'timestamp': datetime.now()},
            'model3': {'performance': 0.7, 'timestamp': datetime.now()}
        }
        
        result = engine.get_best_model()
        
        assert result is not None
        assert result['model_id'] == 'model2'  # Highest performance
        assert result['model_info']['performance'] == 0.9
    
    def test_cleanup_old_models(self, engine):
        """Test cleanup of old models."""
        # Add more models than the limit
        for i in range(15):
            engine.current_models[f'model_{i}'] = {
                'performance': 0.5 + i * 0.01,
                'timestamp': datetime.now() - timedelta(hours=i)
            }
        
        initial_count = len(engine.current_models)
        removed_count = engine.cleanup_old_models(keep_count=5)
        
        assert removed_count == initial_count - 5
        assert len(engine.current_models) == 5
    
    def test_export_learning_summary(self, engine):
        """Test learning summary export."""
        # Add some mock data
        engine.learning_history = [{'timestamp': datetime.now(), 'success': True}]
        engine.current_models = {'model1': {'performance': 0.8, 'learning_method': 'automl', 'timestamp': datetime.now()}}
        
        summary = engine.export_learning_summary()
        
        assert isinstance(summary, dict)
        assert 'learning_history' in summary
        assert 'current_models' in summary
        assert 'meta_learner_status' in summary
        assert 'transfer_learner_status' in summary
        assert 'automl_status' in summary
        assert 'nas_status' in summary
        assert 'export_timestamp' in summary


class TestIntegration:
    """Integration tests for the complete self-learning engine."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def engine(self, temp_dir):
        """Create SelfLearningEngine with temp directory."""
        config = LearningConfig(
            model_save_path=temp_dir,
            meta_learning_tasks_threshold=2,
            cross_validation_folds=3
        )
        return SelfLearningEngine(config)
    
    @pytest.fixture
    def realistic_market_data(self):
        """Create realistic market data for integration testing."""
        np.random.seed(42)  # For reproducible tests
        dates = pd.date_range('2023-01-01', periods=500, freq='D')
        
        # Create realistic price series with trend and volatility
        returns = np.random.normal(0.0005, 0.02, 500)  # Daily returns
        prices = 100 * np.exp(np.cumsum(returns))
        
        # Add some volume data
        volume = np.random.lognormal(8, 0.5, 500).astype(int)
        
        return pd.DataFrame({
            'close': prices,
            'volume': volume
        }, index=dates)
    
    @pytest.mark.asyncio
    async def test_complete_learning_workflow(self, engine, realistic_market_data):
        """Test complete learning workflow with mocked ML operations."""
        # Mock the ML operations to avoid long-running computations
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
        # Mock the meta-learning operations
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
        # Mock the transfer learning operations
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
        
        # Test predictions are similar
        predictions_original = model.predict(X[:10])
        predictions_loaded = loaded_model.predict(X[:10])
        
        np.testing.assert_array_almost_equal(predictions_original, predictions_loaded)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
