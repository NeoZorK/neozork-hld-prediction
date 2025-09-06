"""
Phase 9 Completion Test
Test all Phase 9 components: Advanced Trading Strategies, Quantitative Research Tools, Advanced Risk Management, Performance Analytics
"""

import asyncio
import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_advanced_trading_strategies():
    """Test Advanced Trading Strategies"""
    try:
        from trading.advanced_strategies import MultiStrategyManager, StrategyType, MarketRegime
        
        strategies = MultiStrategyManager()
        
        # Test data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        n_assets = 5
        returns_data = {}
        for i in range(n_assets):
            asset_returns = np.random.normal(0.001, 0.02, len(dates))
            returns_data[f'Asset_{i+1}'] = asset_returns
        
        returns_df = pd.DataFrame(returns_data, index=dates)
        
        # Test market regime detection
        # Create proper data format for regime detection
        regime_data = pd.DataFrame({
            'close': 100 + np.cumsum(returns_df['Asset_1'] * 100)
        })
        market_regime = await strategies.regime_detector.detect_regime(regime_data)
        
        # Test portfolio performance
        portfolio_performance = await strategies.get_portfolio_performance()
        
        # Test system summary
        summary = strategies.get_summary()
        
        print("✅ Advanced Trading Strategies System test passed")
        return True
        
    except Exception as e:
        print(f"❌ Advanced Trading Strategies System test failed: {e}")
        return False

async def test_quantitative_research_tools():
    """Test Quantitative Research Tools"""
    try:
        from research.quantitative_research import QuantitativeResearchManager, ResearchType
        
        research_tools = QuantitativeResearchManager()
        
        # Test data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        n_assets = 5
        returns_data = {}
        for i in range(n_assets):
            asset_returns = np.random.normal(0.001, 0.02, len(dates))
            returns_data[f'Asset_{i+1}'] = asset_returns
        
        returns_df = pd.DataFrame(returns_data, index=dates)
        
        # Test statistical analysis
        stat_result = await research_tools.conduct_research(
            ResearchType.STATISTICAL_ANALYSIS,
            {"series": returns_df['Asset_1']}
        )
        
        # Test factor model
        factor_data = {
            "returns": returns_df['Asset_1'],
            "factors": {
                "market": returns_df['Asset_2'],
                "size": returns_df['Asset_3'],
                "value": returns_df['Asset_4']
            }
        }
        factor_result = await research_tools.conduct_research(
            ResearchType.FACTOR_MODEL,
            factor_data
        )
        
        # Test backtesting framework
        backtest_data = {
            "data": returns_df.rename(columns={'Asset_1': 'close'})
        }
        backtest_result = await research_tools.conduct_research(
            ResearchType.BACKTESTING,
            backtest_data
        )
        
        # Test correlation analysis
        corr_result = await research_tools.conduct_research(
            ResearchType.CORRELATION_ANALYSIS,
            {"dataframe": returns_df}
        )
        
        print("✅ Quantitative Research Tools System test passed")
        return True
        
    except Exception as e:
        print(f"❌ Quantitative Research Tools System test failed: {e}")
        return False

async def test_advanced_risk_management():
    """Test Advanced Risk Management"""
    try:
        from risk.advanced_risk_management import AdvancedRiskManager, HedgeType, OptimizationMethod, StressTestType
        
        risk_manager = AdvancedRiskManager()
        
        # Test data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        portfolio_returns = np.random.normal(0.001, 0.02, len(dates))
        portfolio_returns_series = pd.Series(portfolio_returns, index=dates)
        
        portfolio_data = {
            'portfolio_id': 'test_portfolio',
            'total_value': 1000000,
            'var_95': -0.03,
            'var_99': -0.05
        }
        
        # Test risk metrics calculation
        risk_metrics = await risk_manager.calculate_risk_metrics(portfolio_data, portfolio_returns_series)
        
        # Test hedge strategy creation
        hedge_id = await risk_manager.create_hedge_strategy(
            portfolio_data['portfolio_id'], risk_metrics, HedgeType.DYNAMIC
        )
        
        # Test portfolio optimization
        returns_df = pd.DataFrame({
            'Asset_1': np.random.normal(0.001, 0.02, len(dates)),
            'Asset_2': np.random.normal(0.001, 0.02, len(dates)),
            'Asset_3': np.random.normal(0.001, 0.02, len(dates))
        }, index=dates)
        
        optimization_result = await risk_manager.optimize_portfolio_risk(returns_df)
        
        # Test risk assessment
        risk_assessment = await risk_manager.run_risk_assessment(portfolio_data, portfolio_returns_series)
        
        # Test hedge effectiveness
        hedge_returns = np.random.normal(0.0005, 0.015, len(dates))
        hedge_effectiveness = await risk_manager.hedging_engine.calculate_hedge_effectiveness(
            hedge_id, portfolio_returns.tolist(), hedge_returns.tolist()
        )
        
        print("✅ Advanced Risk Management System test passed")
        return True
        
    except Exception as e:
        print(f"❌ Advanced Risk Management System test failed: {e}")
        return False

async def test_performance_analytics():
    """Test Performance Analytics"""
    try:
        from analytics.performance_analytics import PerformanceAnalytics, AttributionType, BenchmarkType
        
        analytics = PerformanceAnalytics()
        
        # Test data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        portfolio_returns = np.random.normal(0.001, 0.02, len(dates))
        portfolio_returns_series = pd.Series(portfolio_returns, index=dates)
        
        benchmark_returns = np.random.normal(0.0008, 0.015, len(dates))
        benchmark_returns_series = pd.Series(benchmark_returns, index=dates)
        
        portfolio_weights = {
            'Asset_1': 0.3,
            'Asset_2': 0.25,
            'Asset_3': 0.2,
            'Asset_4': 0.15,
            'Asset_5': 0.1
        }
        
        benchmark_weights = {
            'Asset_1': 0.2,
            'Asset_2': 0.2,
            'Asset_3': 0.2,
            'Asset_4': 0.2,
            'Asset_5': 0.2
        }
        
        # Test performance metrics calculation
        performance_metrics = await analytics.performance_calculator.calculate_performance_metrics(
            portfolio_returns_series, benchmark_returns_series
        )
        
        # Test attribution analysis
        attribution_result = await analytics.attribution_analyzer.perform_attribution_analysis(
            portfolio_returns_series, portfolio_weights, benchmark_returns_series, benchmark_weights, AttributionType.SECTOR
        )
        
        # Test benchmark comparison
        benchmark_id = await analytics.benchmark_comparator.create_market_benchmark({})
        comparison = await analytics.benchmark_comparator.compare_with_benchmark(
            portfolio_returns_series, benchmark_id
        )
        
        # Test comprehensive analysis
        analysis = await analytics.analyze_portfolio_performance(
            portfolio_returns_series, portfolio_weights, benchmark_returns_series, benchmark_weights
        )
        
        print("✅ Performance Analytics System test passed")
        return True
        
    except Exception as e:
        print(f"❌ Performance Analytics System test failed: {e}")
        return False

async def test_phase9_integration():
    """Test Phase 9 integration"""
    try:
        from trading.advanced_strategies import MultiStrategyManager, StrategyType
        from research.quantitative_research import QuantitativeResearchManager, ResearchType
        from risk.advanced_risk_management import AdvancedRiskManager, HedgeType
        from analytics.performance_analytics import PerformanceAnalytics, AttributionType
        
        # Initialize all systems
        strategies = MultiStrategyManager()
        research_tools = QuantitativeResearchManager()
        risk_manager = AdvancedRiskManager()
        analytics = PerformanceAnalytics()
        
        # Test data
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        n_assets = 5
        returns_data = {}
        for i in range(n_assets):
            asset_returns = np.random.normal(0.001, 0.02, len(dates))
            returns_data[f'Asset_{i+1}'] = asset_returns
        
        returns_df = pd.DataFrame(returns_data, index=dates)
        
        # Test integrated workflow
        # 1. Research and analysis
        research_result = await research_tools.conduct_research(
            ResearchType.STATISTICAL_ANALYSIS,
            {"series": returns_df['Asset_1']}
        )
        
        # 2. Strategy development
        regime_data = pd.DataFrame({
            'close': 100 + np.cumsum(returns_df['Asset_1'] * 100)
        })
        market_regime = await strategies.regime_detector.detect_regime(regime_data)
        
        # 3. Risk management
        portfolio_data = {'portfolio_id': 'integrated_portfolio', 'total_value': 1000000}
        portfolio_returns = returns_df.mean(axis=1)
        risk_metrics = await risk_manager.calculate_risk_metrics(portfolio_data, portfolio_returns)
        
        # 4. Performance analytics
        portfolio_weights = {f'Asset_{i+1}': 0.2 for i in range(n_assets)}
        analysis = await analytics.analyze_portfolio_performance(portfolio_returns, portfolio_weights)
        
        print("✅ Phase 9 Integration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Phase 9 Integration test failed: {e}")
        return False

async def main():
    """Run all Phase 9 tests"""
    print("🚀 Starting Phase 9 Completion Tests...")
    print("=" * 60)
    
    tests = [
        ("Advanced Trading Strategies", test_advanced_trading_strategies),
        ("Quantitative Research Tools", test_quantitative_research_tools),
        ("Advanced Risk Management", test_advanced_risk_management),
        ("Performance Analytics", test_performance_analytics),
        ("Phase 9 Integration", test_phase9_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Phase 9 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 9 tests passed! Phase 9 is 100% complete.")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Phase 9 needs attention.")
        return False

if __name__ == "__main__":
    asyncio.run(main())
