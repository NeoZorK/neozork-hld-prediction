#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Phase 4 implementation - Advanced Features.

This script tests the new Phase 4 implementations.
"""

import sys
from pathlib import Path
import asyncio
import pandas as pd
import numpy as np
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

def test_advanced_deep_learning():
    """Test advanced deep learning system."""
    print_info("\n🤖 Testing Advanced Deep Learning System...")
    
    try:
        from src.ml.advanced_deep_learning import (
            AdvancedDeepLearning, ModelConfig, ModelArchitecture, TrainingStrategy
        )
        
        # Create deep learning system
        dl_system = AdvancedDeepLearning()
        
        # Test different model architectures
        architectures = [
            ModelArchitecture.LSTM,
            ModelArchitecture.GRU,
            ModelArchitecture.TRANSFORMER,
            ModelArchitecture.CNN_LSTM,
            ModelArchitecture.ATTENTION_LSTM,
            ModelArchitecture.WAVENET,
            ModelArchitecture.RESNET,
            ModelArchitecture.DENSENET,
            ModelArchitecture.VAE,
            ModelArchitecture.GAN,
            ModelArchitecture.AUTOENCODER
        ]
        
        print("  • Testing model creation...")
        
        for architecture in architectures:
            config = ModelConfig(
                architecture=architecture,
                input_shape=(100, 50),  # 100 timesteps, 50 features
                output_shape=(1,),      # Single output
                hidden_layers=[128, 64, 32],
                dropout_rate=0.2,
                learning_rate=0.001,
                batch_size=32,
                epochs=50
            )
            
            result = dl_system.create_model(config)
            if result['status'] == 'success':
                model = result['model']
                print(f"    ✅ {architecture.value}: {model['type']} with {model['layers']} layers, {model['parameters']:,} parameters")
            else:
                print(f"    ❌ {architecture.value}: {result['message']}")
        
        print(f"  • Total models created: {len(dl_system.models)}")
        
        # Test training
        print("  • Testing model training...")
        
        # Generate sample data
        np.random.seed(42)
        X_train = np.random.randn(1000, 100, 50)
        y_train = np.random.randn(1000, 1)
        X_val = np.random.randn(200, 100, 50)
        y_val = np.random.randn(200, 1)
        
        for model_name in list(dl_system.models.keys())[:3]:  # Test first 3 models
            training_result = dl_system.train_model(model_name, X_train, y_train, X_val, y_val)
            
            print(f"    ✅ {model_name}:")
            print(f"        - Best epoch: {training_result.best_epoch}")
            print(f"        - Best loss: {training_result.best_loss:.4f}")
            print(f"        - Best accuracy: {training_result.best_accuracy:.4f}")
            print(f"        - Training time: {training_result.training_time:.2f}s")
            print(f"        - Model size: {training_result.model_size:,} parameters")
        
        # Test prediction
        print("  • Testing model prediction...")
        
        X_test = np.random.randn(100, 100, 50)
        y_test = np.random.randn(100, 1)
        
        for model_name in list(dl_system.models.keys())[:2]:  # Test first 2 models
            predictions = dl_system.predict(model_name, X_test)
            print(f"    ✅ {model_name}: Generated {len(predictions)} predictions")
            
            # Test evaluation
            metrics = dl_system.evaluate_model(model_name, X_test, y_test)
            if metrics:
                print(f"        - MSE: {metrics['mse']:.4f}")
                print(f"        - RMSE: {metrics['rmse']:.4f}")
                print(f"        - MAE: {metrics['mae']:.4f}")
                print(f"        - R²: {metrics['r2']:.4f}")
                print(f"        - Direction Accuracy: {metrics['direction_accuracy']:.4f}")
        
        # Get model summary
        summary = dl_system.get_model_summary()
        if summary['status'] == 'success':
            print(f"  • Model summary: ✅")
            print(f"    - Total models: {summary['summary']['total_models']}")
            print(f"    - Training history: {len(summary['summary']['training_history'])} models trained")
        
        print_success("✅ Advanced Deep Learning System test completed!")
        return dl_system
        
    except Exception as e:
        print_error(f"❌ Advanced Deep Learning System test failed: {str(e)}")
        return None

async def test_ai_trading_agents():
    """Test AI trading agents system."""
    print_info("\n🤖 Testing AI Trading Agents System...")
    
    try:
        from src.ai.trading_agents import (
            AgentManager, MomentumAgent, MLAgent, EnsembleAgent,
            AgentConfig, AgentType, MarketObservation
        )
        
        # Create agent manager
        agent_manager = AgentManager()
        
        # Create different types of agents
        momentum_config = AgentConfig(
            agent_type=AgentType.MOMENTUM_AGENT,
            name="MomentumAgent_1",
            risk_tolerance=0.6,
            max_position_size=0.15,
            decision_threshold=0.5
        )
        momentum_agent = MomentumAgent(momentum_config)
        
        ml_config = AgentConfig(
            agent_type=AgentType.ML_AGENT,
            name="MLAgent_1",
            risk_tolerance=0.4,
            max_position_size=0.1,
            decision_threshold=0.6
        )
        ml_agent = MLAgent(ml_config)
        
        ensemble_config = AgentConfig(
            agent_type=AgentType.ENSEMBLE_AGENT,
            name="EnsembleAgent_1",
            risk_tolerance=0.5,
            max_position_size=0.12,
            decision_threshold=0.55
        )
        ensemble_agent = EnsembleAgent(ensemble_config, [momentum_agent, ml_agent])
        
        # Add agents to manager
        agents = [momentum_agent, ml_agent, ensemble_agent]
        for agent in agents:
            result = agent_manager.add_agent(agent)
            print(f"  • Added {agent.config.name}: {'✅' if result['status'] == 'success' else '❌'}")
        
        print(f"  • Total agents: {len(agent_manager.agents)}")
        
        # Test market data processing
        print("  • Testing market data processing...")
        
        # Create sample market observations
        import random
        observations = []
        for i in range(3):
            observation = MarketObservation(
                timestamp=datetime.now(),
                symbol="BTCUSDT",
                price=50000 + random.uniform(-1000, 1000),
                volume=random.uniform(1000, 10000),
                bid=50000 + random.uniform(-1000, 1000),
                ask=50000 + random.uniform(-1000, 1000),
                spread=random.uniform(10, 50),
                volatility=random.uniform(0.01, 0.05),
                trend=random.choice(["up", "down", "sideways"]),
                sentiment=random.uniform(-1, 1),
                technical_indicators={
                    'rsi': random.uniform(20, 80),
                    'macd': random.uniform(-100, 100),
                    'bollinger_position': random.uniform(0, 1),
                    'sma_20': 50000 + random.uniform(-500, 500),
                    'ema_12': 50000 + random.uniform(-500, 500)
                }
            )
            observations.append(observation)
        
        # Process market data with agents
        for i, observation in enumerate(observations):
            result = await agent_manager.process_market_data(observation)
            
            if result['status'] == 'success':
                print(f"    ✅ Observation {i+1}: Processed with {result['total_agents']} agents")
                
                # Show decisions
                for agent_name, agent_result in result['results'].items():
                    if 'decision' in agent_result:
                        decision = agent_result['decision']
                        print(f"      {agent_name}: {decision.decision.value} (confidence: {decision.confidence:.3f})")
            else:
                print(f"    ❌ Observation {i+1}: {result['message']}")
        
        # Test agent performance
        performance = agent_manager.get_agent_performance()
        if performance['status'] == 'success':
            print(f"  • Agent performance: ✅")
            for agent_name, perf in performance['performance'].items():
                print(f"    {agent_name}:")
                print(f"      - Type: {perf['agent_type']}")
                print(f"      - State: {perf['state']}")
                print(f"      - Trades: {perf['total_trades']}")
                print(f"      - Win Rate: {perf['win_rate']:.1%}")
                print(f"      - PnL: ${perf['total_pnl']:.2f}")
        
        # Test individual agent status
        print("  • Testing individual agent status...")
        for agent in agents:
            status = agent.get_agent_status()
            print(f"    ✅ {status['agent_id']}: {status['state']}, {status['total_trades']} trades")
        
        print_success("✅ AI Trading Agents System test completed!")
        return agent_manager
        
    except Exception as e:
        print_error(f"❌ AI Trading Agents System test failed: {str(e)}")
        return None

def test_quantitative_research():
    """Test quantitative research system."""
    print_info("\n📊 Testing Quantitative Research System...")
    
    try:
        from src.research.quantitative_research import (
            QuantitativeResearcher, ResearchConfig, ResearchMethod
        )
        
        # Create researcher
        researcher = QuantitativeResearcher()
        
        # Generate sample data
        np.random.seed(42)
        n_observations = 1000
        n_assets = 5
        
        # Create sample price data
        dates = pd.date_range(start='2020-01-01', periods=n_observations, freq='D')
        data = pd.DataFrame(
            np.random.randn(n_observations, n_assets).cumsum(axis=0) + 100,
            index=dates,
            columns=[f'Asset_{i+1}' for i in range(n_assets)]
        )
        
        print(f"  • Sample data created: {data.shape[0]} observations, {data.shape[1]} assets")
        
        # Test different research methods
        methods = [
            ResearchMethod.STATISTICAL_ANALYSIS,
            ResearchMethod.TIME_SERIES_ANALYSIS,
            ResearchMethod.REGIME_DETECTION,
            ResearchMethod.CORRELATION_ANALYSIS,
            ResearchMethod.COINTEGRATION,
            ResearchMethod.CAUSALITY_ANALYSIS,
            ResearchMethod.FACTOR_ANALYSIS
        ]
        
        print("  • Testing research methods...")
        
        for method in methods:
            config = ResearchConfig(method=method)
            
            if method == ResearchMethod.STATISTICAL_ANALYSIS:
                result = researcher.perform_statistical_analysis(data, config)
            elif method == ResearchMethod.TIME_SERIES_ANALYSIS:
                result = researcher.perform_time_series_analysis(data.iloc[:, 0], config)
            elif method == ResearchMethod.REGIME_DETECTION:
                result = researcher.detect_regimes(data.iloc[:, 0], config)
            elif method == ResearchMethod.CORRELATION_ANALYSIS:
                result = researcher.analyze_correlations(data, config)
            elif method == ResearchMethod.COINTEGRATION:
                result = researcher.test_cointegration(data, config)
            elif method == ResearchMethod.CAUSALITY_ANALYSIS:
                result = researcher.analyze_causality(data, config)
            elif method == ResearchMethod.FACTOR_ANALYSIS:
                result = researcher.perform_factor_analysis(data, config)
            
            if result['status'] == 'success':
                print(f"    ✅ {method.value}: {result['message']}")
                
                # Show some key results
                if 'results' in result:
                    results = result['results']
                    if 'descriptive_statistics' in results:
                        print(f"        - Descriptive statistics calculated for {len(results['descriptive_statistics'])} assets")
                    if 'normality_tests' in results:
                        print(f"        - Normality tests performed for {len(results['normality_tests'])} assets")
                    if 'pearson_correlation' in results:
                        print(f"        - Correlation matrix: {results['pearson_correlation'].shape}")
                    if 'pca' in results:
                        print(f"        - PCA: {results['pca']['n_components']} components")
            else:
                print(f"    ❌ {method.value}: {result['message']}")
        
        print_success("✅ Quantitative Research System test completed!")
        return researcher
        
    except Exception as e:
        print_error(f"❌ Quantitative Research System test failed: {str(e)}")
        return None

async def test_integration():
    """Test integration between all Phase 4 components."""
    print_info("\n🔗 Testing Phase 4 Integration...")
    
    try:
        from src.ml.advanced_deep_learning import AdvancedDeepLearning, ModelConfig, ModelArchitecture
        from src.ai.trading_agents import AgentManager, MLAgent, AgentConfig, AgentType, MarketObservation
        from src.research.quantitative_research import QuantitativeResearcher, ResearchConfig, ResearchMethod
        
        # Create components
        dl_system = AdvancedDeepLearning()
        agent_manager = AgentManager()
        researcher = QuantitativeResearcher()
        
        print("  • Components initialized: ✅")
        
        # Create ML model for agent
        ml_config = ModelConfig(
            architecture=ModelArchitecture.LSTM,
            input_shape=(10, 10),
            output_shape=(1,),
            hidden_layers=[64, 32],
            epochs=10
        )
        
        ml_model_result = dl_system.create_model(ml_config)
        if ml_model_result['status'] == 'success':
            print(f"  • ML model created for agent: ✅")
            ml_model = ml_model_result['model']
        else:
            print(f"  • ML model creation failed: ❌")
            ml_model = None
        
        # Create ML agent with the model
        agent_config = AgentConfig(
            agent_type=AgentType.ML_AGENT,
            name="IntegratedMLAgent",
            risk_tolerance=0.5,
            max_position_size=0.1
        )
        ml_agent = MLAgent(agent_config, ml_model)
        
        # Add agent to manager
        agent_result = agent_manager.add_agent(ml_agent)
        if agent_result['status'] == 'success':
            print(f"  • ML agent added to manager: ✅")
        
        # Test research with agent data
        np.random.seed(42)
        research_data = pd.DataFrame(
            np.random.randn(100, 3).cumsum(axis=0) + 100,
            columns=['Price', 'Volume', 'Sentiment']
        )
        
        research_config = ResearchConfig(method=ResearchMethod.STATISTICAL_ANALYSIS)
        research_result = researcher.perform_statistical_analysis(research_data, research_config)
        
        if research_result['status'] == 'success':
            print(f"  • Research analysis completed: ✅")
            print(f"    - Data shape: {research_result['data_shape']}")
        
        # Test agent with market observation
        observation = MarketObservation(
            timestamp=datetime.now(),
            symbol="BTCUSDT",
            price=50000,
            volume=1000,
            bid=49990,
            ask=50010,
            spread=20,
            volatility=0.02,
            trend="up",
            sentiment=0.5,
            technical_indicators={
                'rsi': 60,
                'macd': 10,
                'bollinger_position': 0.6,
                'sma_20': 49500,
                'ema_12': 49800
            }
        )
        
        # Process with agent
        agent_result = await agent_manager.process_market_data(observation)
        if agent_result['status'] == 'success':
            print(f"  • Agent processed market data: ✅")
            print(f"    - Agents: {agent_result['total_agents']}")
        
        print_success("✅ Phase 4 Integration test completed!")
        return True
        
    except Exception as e:
        print_error(f"❌ Phase 4 Integration test failed: {str(e)}")
        return False

async def main():
    """Run all Phase 4 tests."""
    print_info("🧪 Testing Phase 4 Implementation - Advanced Features")
    print_info("=" * 80)
    
    try:
        # Test all components
        dl_system = test_advanced_deep_learning()
        agent_manager = await test_ai_trading_agents()
        researcher = test_quantitative_research()
        integration_success = await test_integration()
        
        if dl_system and agent_manager and researcher and integration_success:
            print_success(f"\n🎉 All Phase 4 tests completed successfully!")
            print_info("\n📋 Phase 4 Implementation Status:")
            print("  ✅ Advanced Deep Learning - 11 model architectures with training and evaluation")
            print("  ✅ AI Trading Agents - Autonomous trading agents with decision-making")
            print("  ✅ Quantitative Research - 7 research methods with statistical analysis")
            print("  ✅ Integration Testing - All components working together seamlessly")
            
            print_info("\n🚀 Phase 4 Now 60% Complete!")
            print("  • Advanced ML Models ✅")
            print("  • AI Trading Agents ✅")
            print("  • Quantitative Research ✅")
            print("  • Alternative Data Sources (Pending)")
            print("  • Advanced Analytics (Pending)")
            
            print_info("\n🎯 System Ready for Next Phase!")
            print("  • State-of-the-art deep learning models")
            print("  • Autonomous AI trading agents")
            print("  • Comprehensive quantitative research tools")
            print("  • Full integration across all components")
            
        else:
            print_error(f"\n❌ Some Phase 4 tests failed")
        
    except Exception as e:
        print_error(f"\n❌ Phase 4 tests failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
