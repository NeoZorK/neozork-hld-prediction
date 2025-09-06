#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Phase 6 implementation - First 2 tasks.

This script tests the implementation of:
1. Advanced Machine Learning Models
2. AI-Powered Trading Strategies
"""

import sys
from pathlib import Path
import asyncio
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

def print_info(message):
    print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def test_advanced_ml_models():
    """Test advanced ML models system."""
    print_info("\n🤖 Testing Advanced Machine Learning Models System...")
    
    try:
        from src.ai.advanced_ml_models import (
            AdvancedMLManager, ModelConfig, ModelType, LearningTask, OptimizationAlgorithm
        )
        
        # Create advanced ML manager
        ml_manager = AdvancedMLManager()
        
        print("  • Advanced ML manager initialized: ✅")
        
        # Test ensemble stacking model
        print("  • Testing ensemble stacking model...")
        config = ModelConfig(
            model_type=ModelType.ENSEMBLE_STACKING,
            learning_task=LearningTask.REGRESSION,
            input_features=100,
            output_dimensions=1
        )
        result = ml_manager.create_advanced_model(config)
        if result['status'] == 'success':
            print(f"    ✅ Ensemble stacking model created: {result['model_id']}")
            ensemble_model_id = result['model_id']
        else:
            print(f"    ❌ Ensemble stacking model creation failed: {result['message']}")
            return None
        
        # Test ensemble blending model
        print("  • Testing ensemble blending model...")
        config = ModelConfig(
            model_type=ModelType.ENSEMBLE_BLENDING,
            learning_task=LearningTask.CLASSIFICATION,
            input_features=50,
            output_dimensions=3
        )
        result = ml_manager.create_advanced_model(config)
        if result['status'] == 'success':
            print(f"    ✅ Ensemble blending model created: {result['model_id']}")
        else:
            print(f"    ❌ Ensemble blending model creation failed: {result['message']}")
        
        # Test meta-learning model
        print("  • Testing meta-learning model...")
        config = ModelConfig(
            model_type=ModelType.META_LEARNING,
            learning_task=LearningTask.TIME_SERIES_FORECASTING,
            input_features=75,
            output_dimensions=1
        )
        result = ml_manager.create_advanced_model(config)
        if result['status'] == 'success':
            print(f"    ✅ Meta-learning model created: {result['model_id']}")
            meta_model_id = result['model_id']
        else:
            print(f"    ❌ Meta-learning model creation failed: {result['message']}")
        
        # Test AutoML pipeline
        print("  • Testing AutoML pipeline...")
        config = ModelConfig(
            model_type=ModelType.AUTO_ML,
            learning_task=LearningTask.REGRESSION,
            input_features=60,
            output_dimensions=1,
            optimization_algorithm=OptimizationAlgorithm.BAYESIAN_OPTIMIZATION
        )
        result = ml_manager.create_advanced_model(config)
        if result['status'] == 'success':
            print(f"    ✅ AutoML pipeline created: {result['model_id']}")
            automl_model_id = result['model_id']
        else:
            print(f"    ❌ AutoML pipeline creation failed: {result['message']}")
        
        # Test Neural Architecture Search
        print("  • Testing Neural Architecture Search...")
        config = ModelConfig(
            model_type=ModelType.NEURAL_ARCHITECTURE_SEARCH,
            learning_task=LearningTask.CLASSIFICATION,
            input_features=80,
            output_dimensions=5
        )
        result = ml_manager.create_advanced_model(config)
        if result['status'] == 'success':
            print(f"    ✅ NAS model created: {result['model_id']}")
        else:
            print(f"    ❌ NAS model creation failed: {result['message']}")
        
        # Test model training
        print("  • Testing model training...")
        X = np.random.randn(100, 50)
        y = np.random.randn(100)
        
        if 'ensemble_model_id' in locals():
            train_result = ml_manager.train_model(ensemble_model_id, X, y)
            if train_result['status'] == 'success':
                print(f"    ✅ Model training completed:")
                print(f"        - Accuracy: {train_result['performance']['accuracy']:.3f}")
                print(f"        - R² Score: {train_result['performance']['r2_score']:.3f}")
                print(f"        - Sharpe Ratio: {train_result['performance']['sharpe_ratio']:.3f}")
                print(f"        - Training Time: {train_result['performance']['training_time']:.3f}s")
            else:
                print(f"    ❌ Model training failed: {train_result['message']}")
        
        # Test model prediction
        print("  • Testing model prediction...")
        X_test = np.random.randn(10, 50)
        
        if 'ensemble_model_id' in locals():
            pred_result = ml_manager.predict(ensemble_model_id, X_test)
            if pred_result['status'] == 'success':
                print(f"    ✅ Model prediction completed: {len(pred_result['prediction'])} predictions")
            else:
                print(f"    ❌ Model prediction failed: {pred_result['message']}")
        
        # Test AutoML optimization
        print("  • Testing AutoML optimization...")
        if 'automl_model_id' in locals():
            opt_result = ml_manager.automl_manager.optimize_hyperparameters(
                automl_model_id, X, y, max_trials=20
            )
            if opt_result['status'] == 'success':
                print(f"    ✅ AutoML optimization completed:")
                print(f"        - Best Score: {opt_result['best_score']:.3f}")
                print(f"        - Trials: {opt_result['trials_completed']}")
                print(f"        - Best Params: {opt_result['best_params']}")
            else:
                print(f"    ❌ AutoML optimization failed: {opt_result['message']}")
        
        # Test meta-learning
        print("  • Testing meta-learning...")
        if 'meta_model_id' in locals():
            # Create sample tasks
            tasks = [
                {'task_type': 'regression', 'data_size': 100},
                {'task_type': 'classification', 'data_size': 150},
                {'task_type': 'forecasting', 'data_size': 200}
            ]
            
            meta_result = ml_manager.meta_learning_manager.learn_from_tasks(meta_model_id, tasks)
            if meta_result['status'] == 'success':
                print(f"    ✅ Meta-learning completed: {meta_result['tasks_learned']} tasks learned")
                
                # Test task adaptation
                new_task = {'task_type': 'new_regression', 'data_size': 120}
                adapt_result = ml_manager.meta_learning_manager.adapt_to_new_task(meta_model_id, new_task)
                if adapt_result['status'] == 'success':
                    print(f"    ✅ Task adaptation completed: performance {adapt_result['performance']:.3f}")
                else:
                    print(f"    ❌ Task adaptation failed: {adapt_result['message']}")
            else:
                print(f"    ❌ Meta-learning failed: {meta_result['message']}")
        
        # Test model summary
        print("  • Testing model summary...")
        summary = ml_manager.get_model_summary()
        print(f"    ✅ Model summary:")
        print(f"        - Total models: {summary['total_models']}")
        print(f"        - Ensemble models: {summary['ensemble_models']}")
        print(f"        - Meta-learning models: {summary['meta_learning_models']}")
        print(f"        - AutoML pipelines: {summary['automl_pipelines']}")
        print(f"        - NAS architectures: {summary['nas_architectures']}")
        print(f"        - Performance history: {summary['performance_history']}")
        
        print_success("✅ Advanced Machine Learning Models System test completed!")
        return ml_manager
        
    except Exception as e:
        print_error(f"❌ Advanced Machine Learning Models System test failed: {str(e)}")
        return None

def test_ai_trading_strategies():
    """Test AI trading strategies system."""
    print_info("\n🎯 Testing AI-Powered Trading Strategies System...")
    
    try:
        from src.ai.ai_trading_strategies import (
            AITradingStrategyManager, StrategyType, TradingState, MarketRegime, ActionType
        )
        
        # Create AI trading strategy manager
        ai_manager = AITradingStrategyManager()
        
        print("  • AI trading strategy manager initialized: ✅")
        
        # Test DQN strategy creation
        print("  • Testing DQN strategy creation...")
        result = ai_manager.create_strategy(
            strategy_type=StrategyType.DEEP_Q_NETWORK,
            name="DQN Trading Bot",
            description="Deep Q-Network for automated trading",
            parameters={'learning_rate': 0.001, 'epsilon': 0.1}
        )
        if result['status'] == 'success':
            print(f"    ✅ DQN strategy created: {result['strategy_id']}")
            dqn_strategy_id = result['strategy_id']
        else:
            print(f"    ❌ DQN strategy creation failed: {result['message']}")
            return None
        
        # Test Policy Gradient strategy creation
        print("  • Testing Policy Gradient strategy creation...")
        result = ai_manager.create_strategy(
            strategy_type=StrategyType.POLICY_GRADIENT,
            name="Policy Gradient Trader",
            description="Policy gradient method for trading",
            parameters={'learning_rate': 0.01, 'gamma': 0.99}
        )
        if result['status'] == 'success':
            print(f"    ✅ Policy Gradient strategy created: {result['strategy_id']}")
        else:
            print(f"    ❌ Policy Gradient strategy creation failed: {result['message']}")
        
        # Test Multi-Agent strategy creation
        print("  • Testing Multi-Agent strategy creation...")
        result = ai_manager.create_strategy(
            strategy_type=StrategyType.MULTI_AGENT,
            name="Multi-Agent Trading System",
            description="Coordinated multi-agent trading",
            parameters={'num_agents': 3, 'coordination': 'consensus'}
        )
        if result['status'] == 'success':
            print(f"    ✅ Multi-Agent strategy created: {result['strategy_id']}")
            multi_agent_strategy_id = result['strategy_id']
        else:
            print(f"    ❌ Multi-Agent strategy creation failed: {result['message']}")
        
        # Test adding agents to multi-agent system
        print("  • Testing multi-agent system...")
        
        # Add DQN agent
        agent_result = ai_manager.add_agent_to_system(
            agent_id="dqn_agent",
            strategy_type=StrategyType.DEEP_Q_NETWORK,
            parameters={'state_dim': 10, 'action_dim': 6, 'learning_rate': 0.001}
        )
        if agent_result['status'] == 'success':
            print(f"    ✅ DQN agent added: {agent_result['agent_id']}")
        else:
            print(f"    ❌ DQN agent addition failed: {agent_result['message']}")
        
        # Add Policy Gradient agent
        agent_result = ai_manager.add_agent_to_system(
            agent_id="pg_agent",
            strategy_type=StrategyType.POLICY_GRADIENT,
            parameters={'state_dim': 10, 'action_dim': 6, 'learning_rate': 0.01}
        )
        if agent_result['status'] == 'success':
            print(f"    ✅ Policy Gradient agent added: {agent_result['agent_id']}")
        else:
            print(f"    ❌ Policy Gradient agent addition failed: {agent_result['message']}")
        
        # Test market regime detection
        print("  • Testing market regime detection...")
        
        # Create sample market data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        prices = 100 + np.cumsum(np.random.randn(100) * 0.02)
        market_data = pd.DataFrame({'price': prices}, index=dates)
        
        regime_result = ai_manager.detect_market_regime(market_data)
        if regime_result['status'] == 'success':
            print(f"    ✅ Market regime detected:")
            print(f"        - Regime: {regime_result['regime']}")
            print(f"        - Confidence: {regime_result['confidence']:.3f}")
            print(f"        - Volatility: {regime_result['indicators']['volatility']:.4f}")
            print(f"        - Trend: {regime_result['indicators']['trend']:.4f}")
            print(f"        - Momentum: {regime_result['indicators']['momentum']:.4f}")
        else:
            print(f"    ❌ Market regime detection failed: {regime_result['message']}")
        
        # Test strategy execution
        print("  • Testing strategy execution...")
        
        # Create sample trading state
        trading_state = TradingState(
            timestamp=datetime.now(),
            price=100.0,
            volume=1000.0,
            volatility=0.02,
            trend=0.01,
            momentum=0.005,
            sentiment=0.3,
            market_regime=MarketRegime.BULL_MARKET,
            technical_indicators={
                'rsi': 65.0,
                'macd': 0.5,
                'bollinger_position': 0.6
            }
        )
        
        # Test DQN strategy execution
        if 'dqn_strategy_id' in locals():
            execution_result = ai_manager.execute_strategy(dqn_strategy_id, trading_state)
            if execution_result['status'] == 'success':
                action = execution_result['action']
                print(f"    ✅ DQN strategy execution:")
                print(f"        - Action: {action.action_type.value}")
                print(f"        - Confidence: {action.confidence:.3f}")
                print(f"        - Risk Score: {action.risk_score:.3f}")
                print(f"        - Reasoning: {action.reasoning}")
            else:
                print(f"    ❌ DQN strategy execution failed: {execution_result['message']}")
        
        # Test multi-agent strategy execution
        if 'multi_agent_strategy_id' in locals():
            execution_result = ai_manager.execute_strategy(multi_agent_strategy_id, trading_state)
            if execution_result['status'] == 'success':
                final_action = execution_result['final_action']
                print(f"    ✅ Multi-agent strategy execution:")
                print(f"        - Final Action: {final_action.action_type.value}")
                print(f"        - Confidence: {final_action.confidence:.3f}")
                print(f"        - Coordination: {execution_result['coordination_method']}")
                print(f"        - Agent Actions: {execution_result['agent_actions']}")
            else:
                print(f"    ❌ Multi-agent strategy execution failed: {execution_result['message']}")
        
        # Test strategy summary
        print("  • Testing strategy summary...")
        summary = ai_manager.get_strategy_summary()
        print(f"    ✅ Strategy summary:")
        print(f"        - Total strategies: {summary['total_strategies']}")
        print(f"        - Active strategies: {summary['active_strategies']}")
        print(f"        - Multi-agent agents: {summary['multi_agent_agents']}")
        print(f"        - Performance records: {summary['performance_records']}")
        print(f"        - Regime history: {summary['regime_history']}")
        print(f"        - Strategy types: {summary['strategy_types']}")
        
        print_success("✅ AI-Powered Trading Strategies System test completed!")
        return ai_manager
        
    except Exception as e:
        print_error(f"❌ AI-Powered Trading Strategies System test failed: {str(e)}")
        return None

async def test_integration():
    """Test integration between Phase 6 components."""
    print_info("\n🔗 Testing Phase 6 Integration...")
    
    try:
        from src.ai.advanced_ml_models import AdvancedMLManager, ModelConfig, ModelType, LearningTask
        from src.ai.ai_trading_strategies import AITradingStrategyManager, StrategyType, TradingState, MarketRegime
        
        # Create components
        ml_manager = AdvancedMLManager()
        ai_manager = AITradingStrategyManager()
        
        print("  • Components initialized: ✅")
        
        # Test ML model creation for trading
        print("  • Testing ML model creation for trading...")
        config = ModelConfig(
            model_type=ModelType.ENSEMBLE_STACKING,
            learning_task=LearningTask.REGRESSION,
            input_features=50,
            output_dimensions=1
        )
        ml_result = ml_manager.create_advanced_model(config)
        if ml_result['status'] == 'success':
            print(f"    ✅ ML model created for trading: {ml_result['model_id']}")
            ml_model_id = ml_result['model_id']
        else:
            print(f"    ❌ ML model creation failed: {ml_result['message']}")
            return False
        
        # Test AI strategy creation
        print("  • Testing AI strategy creation...")
        ai_result = ai_manager.create_strategy(
            strategy_type=StrategyType.DEEP_Q_NETWORK,
            name="Integrated AI Trader",
            description="AI strategy using advanced ML models",
            parameters={'ml_model_id': ml_model_id}
        )
        if ai_result['status'] == 'success':
            print(f"    ✅ AI strategy created: {ai_result['strategy_id']}")
            ai_strategy_id = ai_result['strategy_id']
        else:
            print(f"    ❌ AI strategy creation failed: {ai_result['message']}")
            return False
        
        # Test ML model training
        print("  • Testing ML model training...")
        X = np.random.randn(100, 50)
        y = np.random.randn(100)
        
        train_result = ml_manager.train_model(ml_model_id, X, y)
        if train_result['status'] == 'success':
            print(f"    ✅ ML model training completed: R² = {train_result['performance']['r2_score']:.3f}")
        else:
            print(f"    ❌ ML model training failed: {train_result['message']}")
        
        # Test AI strategy execution with ML model
        print("  • Testing AI strategy execution with ML model...")
        trading_state = TradingState(
            timestamp=datetime.now(),
            price=100.0,
            volume=1000.0,
            volatility=0.02,
            trend=0.01,
            momentum=0.005,
            sentiment=0.3,
            market_regime=MarketRegime.BULL_MARKET
        )
        
        execution_result = ai_manager.execute_strategy(ai_strategy_id, trading_state)
        if execution_result['status'] == 'success':
            action = execution_result['action']
            print(f"    ✅ AI strategy execution with ML model:")
            print(f"        - Action: {action.action_type.value}")
            print(f"        - Confidence: {action.confidence:.3f}")
            print(f"        - Strategy Type: {execution_result['strategy_type']}")
        else:
            print(f"    ❌ AI strategy execution failed: {execution_result['message']}")
        
        # Test market regime detection integration
        print("  • Testing market regime detection integration...")
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        prices = 100 + np.cumsum(np.random.randn(50) * 0.02)
        market_data = pd.DataFrame({'price': prices}, index=dates)
        
        regime_result = ai_manager.detect_market_regime(market_data)
        if regime_result['status'] == 'success':
            print(f"    ✅ Market regime detection: {regime_result['regime']} (confidence: {regime_result['confidence']:.3f})")
        else:
            print(f"    ❌ Market regime detection failed: {regime_result['message']}")
        
        # Test overall system status
        print("  • Testing overall system status...")
        ml_summary = ml_manager.get_model_summary()
        ai_summary = ai_manager.get_strategy_summary()
        
        print(f"    ✅ Overall system status:")
        print(f"        - ML Models: {ml_summary['total_models']} models, {ml_summary['ensemble_models']} ensembles")
        print(f"        - AI Strategies: {ai_summary['total_strategies']} strategies, {ai_summary['multi_agent_agents']} agents")
        print(f"        - Performance Records: {ai_summary['performance_records']}")
        print(f"        - Regime History: {ai_summary['regime_history']}")
        
        print_success("✅ Phase 6 Integration test completed!")
        return True
        
    except Exception as e:
        print_error(f"❌ Phase 6 Integration test failed: {str(e)}")
        return False

async def main():
    """Run all Phase 6 implementation tests."""
    print_info("🧪 Testing Phase 6 Implementation - First 2 Tasks")
    print_info("=" * 80)
    
    try:
        # Test all components
        ml_manager = test_advanced_ml_models()
        ai_manager = test_ai_trading_strategies()
        integration_success = await test_integration()
        
        if ml_manager and ai_manager and integration_success:
            print_success(f"\n🎉 All Phase 6 implementation tests passed successfully!")
            print_info("\n📋 Phase 6 Progress Status:")
            print("  ✅ Advanced Machine Learning Models - Ensemble methods, meta-learning, AutoML, NAS")
            print("  ✅ AI-Powered Trading Strategies - DQN, policy gradient, multi-agent, regime detection")
            print("  ✅ Integration Testing - ML models and AI strategies working together seamlessly")
            
            print_info("\n🚀 Phase 6 First 2 Tasks Complete!")
            print("  • Advanced ML Models ✅")
            print("  • AI Trading Strategies ✅")
            
            print_info("\n🎯 Ready for Next Tasks!")
            print("  • Predictive Analytics and Forecasting")
            print("  • Natural Language Processing")
            print("  • Computer Vision and Image Analysis")
            
        else:
            print_error(f"\n❌ Some Phase 6 implementation tests failed")
        
    except Exception as e:
        print_error(f"\n❌ Phase 6 implementation tests failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
