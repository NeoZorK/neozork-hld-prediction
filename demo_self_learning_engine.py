#!/usr/bin/env python3
"""
Demo script for Self-Learning Engine

This script demonstrates the capabilities of the Self-Learning Engine
including meta-learning, transfer learning, AutoML, and neural architecture search.
"""

import sys
import os
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import tempfile
import shutil

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pocket_hedge_fund.autonomous_bot.self_learning_engine import (
    SelfLearningEngine,
    LearningConfig
)


def create_sample_market_data(symbol="BTCUSD", days=500, volatility=0.02):
    """Create realistic sample market data."""
    print(f"Creating sample market data for {symbol}...")
    
    # Generate realistic price data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=days, freq='D')
    
    # Create price series with trend and volatility
    returns = np.random.normal(0.0005, volatility, days)  # Daily returns
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Add volume data
    volume = np.random.lognormal(8, 0.5, days).astype(int)
    
    # Create DataFrame
    df = pd.DataFrame({
        'close': prices,
        'volume': volume,
        'open': prices * (1 + np.random.normal(0, 0.001, days)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.005, days))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.005, days)))
    }, index=dates)
    
    # Ensure high >= low and high >= close >= low
    df['high'] = np.maximum(df['high'], df['close'])
    df['low'] = np.minimum(df['low'], df['close'])
    
    print(f"✓ Created {len(df)} days of market data")
    return df


def create_sample_tasks(market_data, num_tasks=3):
    """Create sample tasks for meta-learning."""
    print(f"Creating {num_tasks} sample tasks for meta-learning...")
    
    tasks = []
    chunk_size = len(market_data) // num_tasks
    
    for i in range(num_tasks):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < num_tasks - 1 else len(market_data)
        
        task_data = market_data.iloc[start_idx:end_idx]
        
        # Simulate different performance characteristics
        task = {
            'market_data': task_data,
            'performance': {
                'sharpe_ratio': 1.0 + i * 0.3,
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
    
    print(f"✓ Created {len(tasks)} tasks")
    return tasks


async def demo_meta_learning(engine, tasks):
    """Demonstrate meta-learning capabilities."""
    print("\n🧠 Meta-Learning Demo")
    print("=" * 50)
    
    # Learn from tasks
    print("Learning from multiple tasks...")
    result = await engine.meta_learner.learn_from_tasks(tasks)
    
    if result['status'] == 'success':
        print(f"✓ Meta-learning completed successfully")
        print(f"  - Tasks processed: {result['tasks_processed']}")
        print(f"  - Meta-model: {result['meta_model']}")
        
        # Test adaptation to new task
        print("\nAdapting to new task...")
        new_task = {
            'market_data': tasks[0]['market_data'] * 1.05,  # 5% different market
            'performance': {'sharpe_ratio': 1.4, 'max_drawdown': 0.04},
            'strategy_params': {'risk_level': 0.018, 'position_size': 0.12}
        }
        
        adaptation_result = await engine.meta_learner.adapt_to_new_task(new_task)
        
        if adaptation_result['status'] == 'success':
            recommendations = adaptation_result['adaptation_recommendations']
            print(f"✓ Task adaptation completed")
            print(f"  - Confidence: {recommendations['confidence']:.3f}")
            print(f"  - Similar tasks found: {len(recommendations['similar_tasks'])}")
        else:
            print(f"❌ Task adaptation failed: {adaptation_result.get('message', 'Unknown error')}")
    else:
        print(f"❌ Meta-learning failed: {result.get('message', 'Unknown error')}")


async def demo_automl(engine, market_data):
    """Demonstrate AutoML capabilities."""
    print("\n🤖 AutoML Demo")
    print("=" * 50)
    
    # Prepare market data
    data = {'market_data': market_data, 'target': 'close'}
    
    print("Searching for optimal models...")
    result = await engine.auto_ml.search_models(data, 'close')
    
    if result['status'] == 'success':
        print(f"✓ AutoML completed successfully")
        print(f"  - Best model: {result['best_model']}")
        print(f"  - Performance (MSE): {result['performance']:.6f}")
        print(f"  - Models evaluated: {len(result['all_results'])}")
        
        # Show top 3 models
        print("\nTop 3 models:")
        sorted_results = sorted(result['all_results'], 
                              key=lambda x: x['mean_score'], reverse=True)
        for i, model_result in enumerate(sorted_results[:3]):
            print(f"  {i+1}. {model_result['model_name']}: "
                  f"Score = {model_result['mean_score']:.4f} "
                  f"(±{model_result['std_score']:.4f})")
    else:
        print(f"❌ AutoML failed: {result.get('message', 'Unknown error')}")


async def demo_transfer_learning(engine, market_data):
    """Demonstrate transfer learning capabilities."""
    print("\n🔄 Transfer Learning Demo")
    print("=" * 50)
    
    # Create source model
    from sklearn.ensemble import RandomForestRegressor
    source_model = {
        'model': RandomForestRegressor(n_estimators=20, random_state=42),
        'training_data': market_data.iloc[:200]
    }
    
    # Create target data (different market conditions)
    target_data = {'market_data': market_data.iloc[200:400] * 1.1}
    
    print("Transferring knowledge between domains...")
    result = await engine.transfer_learner.transfer_knowledge(
        'source_domain', 'target_domain', source_model, target_data
    )
    
    if result['status'] == 'success':
        print(f"✓ Transfer learning completed successfully")
        print(f"  - Domain similarity: {result['domain_similarity']:.3f}")
        print(f"  - Transfer method: {result['transfer_method']}")
        print(f"  - Performance (R²): {result['performance']['r2']:.3f}")
    else:
        print(f"❌ Transfer learning failed: {result.get('message', 'Unknown error')}")


async def demo_neural_architecture_search(engine, market_data):
    """Demonstrate Neural Architecture Search capabilities."""
    print("\n🧬 Neural Architecture Search Demo")
    print("=" * 50)
    
    data = {'market_data': market_data}
    constraints = {'max_layers': 4, 'max_neurons': 100}
    
    print("Searching for optimal neural network architecture...")
    result = await engine.nas.search_architecture(data, constraints)
    
    if result['status'] == 'success':
        print(f"✓ NAS completed successfully")
        print(f"  - Best architecture: {result['best_architecture']}")
        print(f"  - Performance (MSE): {result['performance']:.6f}")
        print(f"  - Architectures evaluated: {len(result['all_results'])}")
        
        # Show architecture details
        arch = result['best_architecture']
        print(f"\nBest architecture details:")
        print(f"  - Layers: {arch['layers']}")
        print(f"  - Activation: {arch['activation']}")
        print(f"  - Regularization (α): {arch['alpha']}")
    else:
        print(f"❌ NAS failed: {result.get('message', 'Unknown error')}")


async def demo_complete_learning_workflow(engine, market_data, tasks):
    """Demonstrate complete learning workflow."""
    print("\n🚀 Complete Learning Workflow Demo")
    print("=" * 50)
    
    # Prepare market data with tasks
    market_data_with_tasks = {
        'market_data': market_data,
        'target': 'close',
        'tasks': tasks
    }
    
    print("Running complete self-learning workflow...")
    result = await engine.learn_from_market(market_data_with_tasks)
    
    if result.success:
        print(f"✓ Complete learning workflow completed successfully")
        print(f"  - Learning time: {result.learning_time:.2f} seconds")
        print(f"  - Best method: {result.learning_method}")
        print(f"  - Model performance (R²): {result.model_performance.get('r2_score', 'N/A')}")
        print(f"  - Model type: {result.model_type}")
        
        # Show learning status
        status = engine.get_learning_status()
        print(f"\nLearning Status:")
        print(f"  - Total sessions: {status['total_learning_sessions']}")
        print(f"  - Success rate: {status['success_rate']:.1%}")
        print(f"  - Current models: {status['current_models_count']}")
        print(f"  - Average performance: {status['average_model_performance']:.3f}")
    else:
        print(f"❌ Complete learning workflow failed: {result.error_message}")


async def demo_strategy_optimization(engine):
    """Demonstrate strategy optimization."""
    print("\n⚡ Strategy Optimization Demo")
    print("=" * 50)
    
    # Simulate poor performance metrics
    performance_metrics = {
        'sharpe_ratio': 1.1,  # Low Sharpe ratio
        'max_drawdown': 0.08,  # High drawdown
        'win_rate': 0.45,  # Low win rate
        'profit_factor': 1.05,  # Low profit factor
        'risk_level': 0.02,
        'position_size': 0.1,
        'stop_loss': 0.05,
        'take_profit': 0.1
    }
    
    print("Optimizing strategy based on performance metrics...")
    result = await engine.optimize_strategy(performance_metrics)
    
    if result['status'] == 'success':
        print(f"✓ Strategy optimization completed successfully")
        print(f"  - Expected improvement: {result['expected_improvement']:.1%}")
        print(f"  - Optimization reasons: {len(result['optimization_reasons'])}")
        
        print(f"\nOptimized parameters:")
        for param, value in result['optimized_parameters'].items():
            print(f"  - {param}: {value:.4f}")
        
        print(f"\nOptimization reasons:")
        for reason in result['optimization_reasons']:
            print(f"  - {reason}")
    else:
        print(f"❌ Strategy optimization failed: {result.get('message', 'Unknown error')}")


async def main():
    """Main demo function."""
    print("🎯 NeoZork Self-Learning Engine Demo")
    print("=" * 60)
    print("This demo showcases the advanced AI capabilities of the")
    print("Self-Learning Engine for autonomous trading.")
    print("=" * 60)
    
    # Create temporary directory for models
    temp_dir = tempfile.mkdtemp()
    print(f"Using temporary directory: {temp_dir}")
    
    try:
        # Initialize engine
        config = LearningConfig(
            meta_learning_enabled=True,
            transfer_learning_enabled=True,
            auto_ml_enabled=True,
            nas_enabled=True,
            model_save_path=temp_dir,
            meta_learning_tasks_threshold=3,
            cross_validation_folds=3
        )
        
        engine = SelfLearningEngine(config)
        print("✓ Self-Learning Engine initialized")
        
        # Create sample data
        market_data = create_sample_market_data("BTCUSD", days=300)
        tasks = create_sample_tasks(market_data, num_tasks=3)
        
        # Run demos
        await demo_meta_learning(engine, tasks)
        await demo_automl(engine, market_data)
        await demo_transfer_learning(engine, market_data)
        await demo_neural_architecture_search(engine, market_data)
        await demo_strategy_optimization(engine)
        await demo_complete_learning_workflow(engine, market_data, tasks)
        
        # Export learning summary
        print("\n📊 Learning Summary Export")
        print("=" * 50)
        summary = engine.export_learning_summary()
        print(f"✓ Learning summary exported")
        print(f"  - Learning history entries: {len(summary['learning_history'])}")
        print(f"  - Current models: {len(summary['current_models'])}")
        print(f"  - Export timestamp: {summary['export_timestamp']}")
        
        print("\n🎉 Demo completed successfully!")
        print("The Self-Learning Engine is ready for autonomous trading!")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temporary directory: {temp_dir}")


if __name__ == "__main__":
    asyncio.run(main())
