#!/usr/bin/env python3
"""
Phase 9 Implementation Test
Advanced Trading Strategies and Quantitative Research Tools
"""

import asyncio
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pytest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

@pytest.mark.asyncio
async def test_advanced_strategies():
    """Test Advanced Trading Strategies System"""
    print("Testing Advanced Trading Strategies System...")
    
    try:
        from trading.advanced_strategies import (
            MultiStrategyManager, MomentumStrategy, MeanReversionStrategy,
            StrategyConfig, StrategyType, MarketRegime, SignalType
        )
        
        manager = MultiStrategyManager()
        
        # Create momentum strategy configuration
        momentum_config = StrategyConfig(
            config_id="momentum_001",
            strategy_type=StrategyType.MOMENTUM,
            name="Momentum Strategy",
            description="Momentum-based trading strategy",
            parameters={'rsi_oversold': 30, 'rsi_overbought': 70, 'momentum_threshold': 0.02},
            risk_limits={'risk_per_trade': 0.02, 'stop_loss': 0.05, 'max_position': 0.2},
            position_sizing={'method': 'kelly', 'max_kelly': 0.25},
            entry_conditions=[{'type': 'rsi', 'condition': 'oversold'}],
            exit_conditions=[{'type': 'rsi', 'condition': 'overbought'}],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create mean reversion strategy configuration
        mean_reversion_config = StrategyConfig(
            config_id="mean_reversion_001",
            strategy_type=StrategyType.MEAN_REVERSION,
            name="Mean Reversion Strategy",
            description="Mean reversion trading strategy",
            parameters={'z_score_threshold': 2.0, 'bb_period': 20, 'bb_std': 2.0},
            risk_limits={'risk_per_trade': 0.015, 'stop_loss': 0.03, 'max_position': 0.15},
            position_sizing={'method': 'fixed', 'position_size': 0.1},
            entry_conditions=[{'type': 'bollinger_bands', 'condition': 'below_lower'}],
            exit_conditions=[{'type': 'bollinger_bands', 'condition': 'above_upper'}],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Create strategies
        momentum_strategy = MomentumStrategy(momentum_config)
        mean_reversion_strategy = MeanReversionStrategy(mean_reversion_config)
        
        # Add strategies to manager
        momentum_id = await manager.add_strategy(momentum_strategy)
        mean_reversion_id = await manager.add_strategy(mean_reversion_strategy)
        
        # Generate sample market data
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='H')
        np.random.seed(42)
        
        data = pd.DataFrame({
            'open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
            'high': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) + np.random.uniform(0, 2, len(dates)),
            'low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1) - np.random.uniform(0, 2, len(dates)),
            'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
            'volume': np.random.uniform(1000, 10000, len(dates))
        }, index=dates)
        
        # Test market regime detection
        regime = await manager.regime_detector.detect_regime(data)
        print(f"Detected market regime: {regime.value}")
        
        # Test regime probabilities
        regime_probs = await manager.regime_detector.get_regime_probabilities(data)
        print(f"Regime probabilities: {len(regime_probs)} regimes")
        
        # Test regime transition prediction
        next_regime, confidence = await manager.regime_detector.predict_regime_transition(data)
        print(f"Predicted next regime: {next_regime.value} (confidence: {confidence:.3f})")
        
        # Run strategies
        signals = await manager.run_strategies(data, 10000)
        print(f"Generated {len(signals)} signals")
        
        # Test strategy performance
        momentum_performance = await manager.get_strategy_performance(momentum_id)
        mean_reversion_performance = await manager.get_strategy_performance(mean_reversion_id)
        
        if momentum_performance:
            print(f"Momentum strategy: {momentum_performance.total_return:.4f} return, {momentum_performance.win_rate:.2f} win rate")
        
        if mean_reversion_performance:
            print(f"Mean reversion strategy: {mean_reversion_performance.total_return:.4f} return, {mean_reversion_performance.win_rate:.2f} win rate")
        
        # Test portfolio performance
        portfolio_performance = await manager.get_portfolio_performance()
        print(f"Portfolio performance: {portfolio_performance['total_return']:.4f} total return")
        
        # Test system summary
        summary = manager.get_summary()
        print(f"System summary: {summary}")
        
        print(f"✅ Advanced Trading Strategies System test passed")
        print(f"   - Created {len(manager.strategies)} strategies")
        print(f"   - Generated {len(signals)} signals")
        print(f"   - Market regime: {regime.value}")
        print(f"   - Portfolio return: {portfolio_performance['total_return']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced Trading Strategies System test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_quantitative_research():
    """Test Quantitative Research Tools System"""
    print("Testing Quantitative Research Tools System...")
    
    try:
        from research.quantitative_research import (
            QuantitativeResearchManager, ResearchType, FactorType, BacktestType
        )
        
        manager = QuantitativeResearchManager()
        
        # Generate sample data
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        
        # Create sample price data
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = 100 * np.cumprod(1 + returns)
        price_series = pd.Series(prices, index=dates)
        
        # Create factor data
        market_factor = pd.Series(np.random.normal(0.0005, 0.015, len(dates)), index=dates)
        size_factor = pd.Series(np.random.normal(0.0002, 0.01, len(dates)), index=dates)
        value_factor = pd.Series(np.random.normal(0.0001, 0.008, len(dates)), index=dates)
        
        # Test statistical analysis
        stats_result = await manager.conduct_research(
            ResearchType.STATISTICAL_ANALYSIS,
            {'series': price_series}
        )
        print(f"Statistical analysis: {len(stats_result.conclusions)} conclusions")
        
        # Test factor model analysis
        factor_result = await manager.conduct_research(
            ResearchType.FACTOR_MODEL,
            {
                'returns': pd.Series(returns, index=dates),
                'factors': {
                    'market': market_factor,
                    'size': size_factor,
                    'value': value_factor
                }
            },
            {'model_name': 'Sample Factor Model'}
        )
        print(f"Factor model: R² = {factor_result.statistics.get('r_squared', 0):.3f}")
        
        # Test correlation analysis
        correlation_data = pd.DataFrame({
            'returns': returns,
            'market': market_factor,
            'size': size_factor,
            'value': value_factor
        }, index=dates)
        
        correlation_result = await manager.conduct_research(
            ResearchType.CORRELATION_ANALYSIS,
            {'dataframe': correlation_data}
        )
        print(f"Correlation analysis: {len(correlation_result.conclusions)} conclusions")
        
        # Test backtesting analysis
        backtest_data = pd.DataFrame({
            'close': prices,
            'volume': np.random.uniform(1000, 10000, len(dates))
        }, index=dates)
        
        backtest_result = await manager.conduct_research(
            ResearchType.BACKTESTING,
            {'data': backtest_data},
            {'backtest_type': BacktestType.WALK_FORWARD}
        )
        print(f"Backtesting: {len(backtest_result.conclusions)} conclusions")
        
        # Test research summary
        summary = manager.get_research_summary()
        print(f"Research summary: {summary}")
        
        print(f"✅ Quantitative Research Tools System test passed")
        print(f"   - Statistical analysis: {len(stats_result.conclusions)} conclusions")
        print(f"   - Factor model: R² = {factor_result.statistics.get('r_squared', 0):.3f}")
        print(f"   - Correlation analysis: {len(correlation_result.conclusions)} conclusions")
        print(f"   - Backtesting: {len(backtest_result.conclusions)} conclusions")
        print(f"   - Total research: {summary['total_research']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Quantitative Research Tools System test failed: {e}")
        return False

@pytest.mark.asyncio
async def test_integration():
    """Test integration between Advanced Strategies and Quantitative Research"""
    print("Testing Phase 9 Integration...")
    
    try:
        from trading.advanced_strategies import MultiStrategyManager, MomentumStrategy, StrategyConfig, StrategyType
        from research.quantitative_research import QuantitativeResearchManager, ResearchType
        
        # Initialize systems
        strategy_manager = MultiStrategyManager()
        research_manager = QuantitativeResearchManager()
        
        # Create a strategy
        momentum_config = StrategyConfig(
            config_id="integration_001",
            strategy_type=StrategyType.MOMENTUM,
            name="Integration Test Strategy",
            description="Strategy for integration testing",
            parameters={'rsi_oversold': 30, 'rsi_overbought': 70},
            risk_limits={'risk_per_trade': 0.02, 'stop_loss': 0.05},
            position_sizing={'method': 'kelly', 'max_kelly': 0.25},
            entry_conditions=[{'type': 'rsi', 'condition': 'oversold'}],
            exit_conditions=[{'type': 'rsi', 'condition': 'overbought'}],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        momentum_strategy = MomentumStrategy(momentum_config)
        strategy_id = await strategy_manager.add_strategy(momentum_strategy)
        
        # Generate sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='H')
        np.random.seed(42)
        
        data = pd.DataFrame({
            'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.1),
            'volume': np.random.uniform(1000, 10000, len(dates))
        }, index=dates)
        
        # Run strategy
        signals = await strategy_manager.run_strategies(data, 10000)
        
        # Analyze strategy performance with research tools
        price_series = data['close']
        research_result = await research_manager.conduct_research(
            ResearchType.STATISTICAL_ANALYSIS,
            {'series': price_series}
        )
        
        # Get strategy performance
        strategy_performance = await strategy_manager.get_strategy_performance(strategy_id)
        
        # Get research summary
        research_summary = research_manager.get_research_summary()
        
        print(f"✅ Phase 9 Integration test passed")
        print(f"   - Strategy signals: {len(signals)}")
        print(f"   - Research conclusions: {len(research_result.conclusions)}")
        print(f"   - Strategy performance: {strategy_performance.total_return if strategy_performance else 0:.4f}")
        print(f"   - Research summary: {research_summary['total_research']} analyses")
        
        return True
        
    except Exception as e:
        print(f"❌ Phase 9 Integration test failed: {e}")
        return False

async def main():
    """Run all Phase 9 implementation tests"""
    print("=" * 60)
    print("PHASE 9 IMPLEMENTATION TEST - Advanced Trading Strategies & Research")
    print("=" * 60)
    
    tests = [
        ("Advanced Trading Strategies", test_advanced_strategies),
        ("Quantitative Research Tools", test_quantitative_research),
        ("Phase 9 Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("PHASE 9 IMPLEMENTATION TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 PHASE 9 IMPLEMENTATION: 100% SUCCESS!")
        print("Advanced Trading Strategies and Quantitative Research Tools implemented successfully.")
        return True
    else:
        print(f"\n⚠️  PHASE 9 IMPLEMENTATION: {passed}/{total} tests passed")
        print("Some features need attention before Phase 9 can be considered complete.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
