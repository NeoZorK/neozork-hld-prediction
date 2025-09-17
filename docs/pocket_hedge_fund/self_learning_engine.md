# Self-Learning Engine Documentation

## Overview

The Self-Learning Engine is a revolutionary AI-powered component of the NeoZork Pocket Hedge Fund that provides autonomous learning capabilities for trading strategies. It combines multiple advanced machine learning techniques to continuously improve trading performance.

## Key Features

### 🧠 Meta-Learning
- **Learning to Learn**: The engine learns how to learn from multiple trading tasks
- **Task Similarity**: Identifies similar market conditions and trading scenarios
- **Rapid Adaptation**: Quickly adapts to new market conditions using learned patterns
- **Performance Prediction**: Predicts strategy performance before deployment

### 🔄 Transfer Learning
- **Knowledge Transfer**: Transfers knowledge between different assets and timeframes
- **Domain Adaptation**: Adapts models trained on one market to another
- **Feature Importance Transfer**: Preserves important features across domains
- **Fine-tuning**: Continuously improves models with new data

### 🤖 AutoML (Automated Machine Learning)
- **Model Selection**: Automatically selects the best model for each task
- **Hyperparameter Optimization**: Optimizes model parameters for maximum performance
- **Feature Engineering**: Creates technical indicators and features automatically
- **Cross-validation**: Uses time-series cross-validation for robust evaluation

### 🧬 Neural Architecture Search (NAS)
- **Architecture Optimization**: Finds optimal neural network architectures
- **Evolutionary Design**: Evolves architectures based on performance feedback
- **Constraint-based Search**: Respects computational and memory constraints
- **Multi-objective Optimization**: Balances performance and complexity

## Architecture

```
SelfLearningEngine
├── MetaLearner
│   ├── Task Feature Extraction
│   ├── Similarity Calculation
│   ├── Performance Prediction
│   └── Adaptation Recommendations
├── TransferLearner
│   ├── Domain Similarity Analysis
│   ├── Feature Importance Transfer
│   ├── Model Weight Transfer
│   └── Fine-tuning Pipeline
├── AutoML
│   ├── Model Candidates
│   ├── Hyperparameter Search
│   ├── Feature Engineering
│   └── Performance Evaluation
└── NeuralArchitectureSearch
    ├── Architecture Generation
    ├── Performance Evaluation
    ├── Evolutionary Optimization
    └── Constraint Handling
```

## Usage Examples

### Basic Usage

```python
from src.pocket_hedge_fund.autonomous_bot.self_learning_engine import (
    SelfLearningEngine, LearningConfig
)

# Initialize engine
config = LearningConfig(
    meta_learning_enabled=True,
    transfer_learning_enabled=True,
    auto_ml_enabled=True,
    nas_enabled=True
)

engine = SelfLearningEngine(config)

# Learn from market data
market_data = {
    'market_data': your_dataframe,
    'target': 'close'
}

result = await engine.learn_from_market(market_data)
```

### Meta-Learning Example

```python
# Create tasks for meta-learning
tasks = [
    {
        'market_data': btc_data,
        'performance': {'sharpe_ratio': 1.5, 'max_drawdown': 0.05},
        'strategy_params': {'risk_level': 0.02, 'position_size': 0.1}
    },
    {
        'market_data': eth_data,
        'performance': {'sharpe_ratio': 2.0, 'max_drawdown': 0.03},
        'strategy_params': {'risk_level': 0.015, 'position_size': 0.12}
    }
]

# Learn from tasks
result = await engine.meta_learner.learn_from_tasks(tasks)

# Adapt to new task
new_task = {'market_data': new_data, 'performance': {...}}
adaptation = await engine.meta_learner.adapt_to_new_task(new_task)
```

### Transfer Learning Example

```python
# Transfer knowledge between domains
source_model = {
    'model': trained_model,
    'training_data': source_data
}

target_data = {'market_data': target_dataframe}

result = await engine.transfer_learner.transfer_knowledge(
    'source_domain', 'target_domain', source_model, target_data
)
```

### AutoML Example

```python
# Automatic model selection
data = {'market_data': your_dataframe, 'target': 'close'}
result = await engine.auto_ml.search_models(data, 'close')

# Hyperparameter optimization
optimized_model = await engine.auto_ml.optimize_hyperparameters(
    model, data
)
```

### Strategy Optimization

```python
# Optimize trading strategy
performance_metrics = {
    'sharpe_ratio': 1.2,
    'max_drawdown': 0.08,
    'win_rate': 0.45,
    'profit_factor': 1.1
}

optimization = await engine.optimize_strategy(performance_metrics)
```

## Configuration Options

### LearningConfig Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `meta_learning_enabled` | `True` | Enable meta-learning capabilities |
| `transfer_learning_enabled` | `True` | Enable transfer learning |
| `auto_ml_enabled` | `True` | Enable AutoML |
| `nas_enabled` | `True` | Enable Neural Architecture Search |
| `learning_rate` | `0.001` | Learning rate for neural networks |
| `batch_size` | `32` | Batch size for training |
| `max_epochs` | `100` | Maximum training epochs |
| `cross_validation_folds` | `5` | Number of CV folds |
| `meta_learning_tasks_threshold` | `5` | Minimum tasks for meta-learning |
| `transfer_learning_similarity_threshold` | `0.7` | Domain similarity threshold |
| `performance_improvement_threshold` | `0.05` | Minimum improvement threshold |

## Performance Metrics

The engine tracks various performance metrics:

- **R² Score**: Model accuracy
- **MSE/MAE**: Prediction error
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Risk measurement
- **Win Rate**: Success percentage
- **Profit Factor**: Profit/loss ratio

## Model Management

### Model Storage
- Models are automatically saved to disk
- Configurable storage path
- Automatic cleanup of old models
- Model versioning and metadata

### Model Selection
- Best model selection based on performance
- Multi-criteria optimization
- Performance tracking over time
- Automatic model replacement

## Integration with Trading System

The Self-Learning Engine integrates seamlessly with:

- **Adaptive Strategy Manager**: Provides optimized strategies
- **Self-Monitoring System**: Monitors model performance
- **Self-Retraining System**: Triggers model updates
- **Risk Management**: Incorporates risk constraints

## Best Practices

### Data Preparation
1. Ensure sufficient data volume (minimum 100 samples)
2. Include relevant technical indicators
3. Handle missing data appropriately
4. Use proper time-series validation

### Model Selection
1. Start with AutoML for baseline models
2. Use transfer learning for similar assets
3. Apply meta-learning for rapid adaptation
4. Consider NAS for complex patterns

### Performance Monitoring
1. Monitor model performance continuously
2. Set up alerts for performance degradation
3. Regular model retraining
4. A/B testing for new models

## Troubleshooting

### Common Issues

**Low Performance**
- Check data quality and quantity
- Verify feature engineering
- Adjust hyperparameters
- Consider ensemble methods

**Slow Learning**
- Reduce model complexity
- Use fewer CV folds
- Optimize data preprocessing
- Consider transfer learning

**Memory Issues**
- Reduce model storage count
- Use smaller batch sizes
- Optimize feature selection
- Enable model cleanup

## Future Enhancements

- **Reinforcement Learning**: Integration with RL algorithms
- **Federated Learning**: Distributed learning across multiple funds
- **Quantum ML**: Quantum machine learning algorithms
- **Explainable AI**: Model interpretability features
- **Real-time Learning**: Online learning capabilities

## API Reference

### SelfLearningEngine

#### Methods

- `learn_from_market(market_data)`: Learn from market data
- `optimize_strategy(performance_metrics)`: Optimize trading strategy
- `adapt_to_new_market(market_conditions)`: Adapt to new market
- `get_learning_status()`: Get learning status
- `get_best_model()`: Get best performing model
- `cleanup_old_models(keep_count)`: Clean up old models
- `export_learning_summary()`: Export learning summary

### MetaLearner

#### Methods

- `learn_from_tasks(tasks)`: Learn from multiple tasks
- `adapt_to_new_task(task_data)`: Adapt to new task

### TransferLearner

#### Methods

- `transfer_knowledge(source_domain, target_domain, source_model, target_data)`: Transfer knowledge
- `fine_tune_model(base_model, target_data)`: Fine-tune model

### AutoML

#### Methods

- `search_models(data, target)`: Search for optimal models
- `optimize_hyperparameters(model, data)`: Optimize hyperparameters

### NeuralArchitectureSearch

#### Methods

- `search_architecture(data, constraints)`: Search for optimal architecture
- `evolve_architecture(current_architecture, performance_feedback)`: Evolve architecture

## Conclusion

The Self-Learning Engine represents a significant advancement in autonomous trading technology. By combining multiple AI techniques, it provides robust, adaptive, and continuously improving trading capabilities that can adapt to changing market conditions and learn from experience.

For more information, see the demo script `interactive/advanced_ml/demo_self_learning_engine.py` and the comprehensive test suite in `tests/pocket_hedge_fund/test_self_learning_engine.py`.
