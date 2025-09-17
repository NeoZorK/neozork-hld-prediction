"""
NeoZork Pocket Hedge Fund - Strategy Engine Test Suite

This module provides comprehensive testing for the strategy engine including:
- Strategy creation and management
- Strategy execution
- Signal generation
- Order management
- Performance monitoring
- Backtesting
- Risk management
- Error handling and edge cases
"""

import pytest
import asyncio
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, List, Any
import numpy as np

from .strategy_engine.strategy_executor import (
    StrategyExecutor, MomentumStrategy, MeanReversionStrategy,
    StrategyStatus, OrderType, OrderSide, OrderStatus, SignalType,
    TradingSignal, Order, StrategyExecution
)
from .config.database_manager import DatabaseManager
from .config.config_manager import ConfigManager
from .notifications.notification_manager import NotificationManager

class TestMomentumStrategy:
    """Test suite for MomentumStrategy"""
    
    @pytest.fixture
    def momentum_strategy(self):
        """Create momentum strategy instance for testing"""
        return MomentumStrategy("test_momentum_001")
    
    @pytest.mark.asyncio
    async def test_momentum_strategy_initialization(self, momentum_strategy):
        """Test momentum strategy initialization"""
        assert momentum_strategy.strategy_id == "test_momentum_001"
        assert momentum_strategy.name == "Momentum Strategy"
        assert momentum_strategy.description == "A momentum-based trading strategy that follows market trends"
        assert momentum_strategy.status == StrategyStatus.STOPPED
        assert "lookback_period" in momentum_strategy.parameters
        assert "threshold" in momentum_strategy.parameters
        assert "stop_loss" in momentum_strategy.parameters
        assert "take_profit" in momentum_strategy.parameters
    
    @pytest.mark.asyncio
    async def test_momentum_signal_generation_buy(self, momentum_strategy):
        """Test momentum strategy buy signal generation"""
        market_data = {
            "BTC": {
                "prices": [45000, 45100, 45200, 45300, 45400, 45500, 45600, 45700, 45800, 45900, 46000, 46100, 46200, 46300, 46400, 46500, 46600, 46700, 46800, 46900, 47000],
                "volume": 1000000,
                "timestamp": datetime.now(datetime.UTC)
            }
        }
        
        signals = await momentum_strategy.generate_signals(market_data)
        
        assert len(signals) > 0
        assert all(signal.signal_type == SignalType.BUY for signal in signals)
        assert all(signal.strength > 0 for signal in signals)
        assert all(signal.confidence > 0 for signal in signals)
        assert all(signal.price > 0 for signal in signals)
    
    @pytest.mark.asyncio
    async def test_momentum_signal_generation_sell(self, momentum_strategy):
        """Test momentum strategy sell signal generation"""
        market_data = {
            "BTC": {
                "prices": [47000, 46900, 46800, 46700, 46600, 46500, 46400, 46300, 46200, 46100, 46000, 45900, 45800, 45700, 45600, 45500, 45400, 45300, 45200, 45100, 45000],
                "volume": 1000000,
                "timestamp": datetime.now(datetime.UTC)
            }
        }
        
        signals = await momentum_strategy.generate_signals(market_data)
        
        assert len(signals) > 0
        assert all(signal.signal_type == SignalType.SELL for signal in signals)
        assert all(signal.strength > 0 for signal in signals)
        assert all(signal.confidence > 0 for signal in signals)
        assert all(signal.price > 0 for signal in signals)
    
    @pytest.mark.asyncio
    async def test_momentum_position_size_calculation(self, momentum_strategy):
        """Test momentum strategy position size calculation"""
        signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id="test_momentum_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=0,
            stop_loss=42750.0,  # 5% stop loss
            take_profit=49500.0,  # 10% take profit
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        portfolio_value = 100000.0
        position_size = await momentum_strategy.calculate_position_size(signal, portfolio_value)
        
        assert position_size > 0
        assert position_size <= portfolio_value * momentum_strategy.parameters["max_position_size"] / signal.price
    
    @pytest.mark.asyncio
    async def test_momentum_risk_metrics_calculation(self, momentum_strategy):
        """Test momentum strategy risk metrics calculation"""
        positions = {
            "BTC": {"value": 10000.0, "risk": 500.0},
            "ETH": {"value": 5000.0, "risk": 250.0}
        }
        
        risk_metrics = await momentum_strategy.calculate_risk_metrics(positions)
        
        assert "total_value" in risk_metrics
        assert "total_risk" in risk_metrics
        assert "risk_ratio" in risk_metrics
        assert "position_count" in risk_metrics
        assert "max_position_size" in risk_metrics
        assert risk_metrics["total_value"] == 15000.0
        assert risk_metrics["total_risk"] == 750.0
        assert risk_metrics["position_count"] == 2
    
    @pytest.mark.asyncio
    async def test_momentum_signal_validation(self, momentum_strategy):
        """Test momentum strategy signal validation"""
        # Valid signal
        valid_signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id="test_momentum_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await momentum_strategy.validate_signal(valid_signal) is True
        
        # Invalid signal - negative strength
        invalid_signal = TradingSignal(
            signal_id="test_signal_002",
            strategy_id="test_momentum_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=-0.1,  # Invalid
            price=45000.0,
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await momentum_strategy.validate_signal(invalid_signal) is False

class TestMeanReversionStrategy:
    """Test suite for MeanReversionStrategy"""
    
    @pytest.fixture
    def mean_reversion_strategy(self):
        """Create mean reversion strategy instance for testing"""
        return MeanReversionStrategy("test_mean_reversion_001")
    
    @pytest.mark.asyncio
    async def test_mean_reversion_strategy_initialization(self, mean_reversion_strategy):
        """Test mean reversion strategy initialization"""
        assert mean_reversion_strategy.strategy_id == "test_mean_reversion_001"
        assert mean_reversion_strategy.name == "Mean Reversion Strategy"
        assert mean_reversion_strategy.description == "A mean reversion strategy that profits from price corrections"
        assert mean_reversion_strategy.status == StrategyStatus.STOPPED
        assert "lookback_period" in mean_reversion_strategy.parameters
        assert "deviation_threshold" in mean_reversion_strategy.parameters
        assert "reversion_factor" in mean_reversion_strategy.parameters
    
    @pytest.mark.asyncio
    async def test_mean_reversion_signal_generation_buy(self, mean_reversion_strategy):
        """Test mean reversion strategy buy signal generation"""
        # Create data with price below mean (negative z-score)
        prices = [3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3000]  # Last price below mean
        
        market_data = {
            "ETH": {
                "prices": prices,
                "volume": 500000,
                "timestamp": datetime.now(datetime.UTC)
            }
        }
        
        signals = await mean_reversion_strategy.generate_signals(market_data)
        
        assert len(signals) > 0
        assert all(signal.signal_type == SignalType.BUY for signal in signals)
        assert all(signal.strength > 0 for signal in signals)
        assert all(signal.confidence > 0 for signal in signals)
    
    @pytest.mark.asyncio
    async def test_mean_reversion_signal_generation_sell(self, mean_reversion_strategy):
        """Test mean reversion strategy sell signal generation"""
        # Create data with price above mean (positive z-score)
        prices = [3000, 3010, 3020, 3030, 3040, 3050, 3060, 3070, 3080, 3090, 3100, 3110, 3120, 3130, 3140, 3150, 3160, 3170, 3180, 3190, 3300]  # Last price above mean
        
        market_data = {
            "ETH": {
                "prices": prices,
                "volume": 500000,
                "timestamp": datetime.now(datetime.UTC)
            }
        }
        
        signals = await mean_reversion_strategy.generate_signals(market_data)
        
        assert len(signals) > 0
        assert all(signal.signal_type == SignalType.SELL for signal in signals)
        assert all(signal.strength > 0 for signal in signals)
        assert all(signal.confidence > 0 for signal in signals)
    
    @pytest.mark.asyncio
    async def test_mean_reversion_position_size_calculation(self, mean_reversion_strategy):
        """Test mean reversion strategy position size calculation"""
        signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id="test_mean_reversion_001",
            symbol="ETH",
            signal_type=SignalType.BUY,
            strength=0.6,
            price=3000.0,
            quantity=0,
            stop_loss=2910.0,  # 3% stop loss
            take_profit=3180.0,  # 6% take profit
            confidence=0.8,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        portfolio_value = 100000.0
        position_size = await mean_reversion_strategy.calculate_position_size(signal, portfolio_value)
        
        assert position_size > 0
        assert position_size <= portfolio_value * mean_reversion_strategy.parameters["max_position_size"] / signal.price
    
    @pytest.mark.asyncio
    async def test_mean_reversion_risk_metrics_calculation(self, mean_reversion_strategy):
        """Test mean reversion strategy risk metrics calculation"""
        positions = {
            "ETH": {"value": 8000.0, "risk": 400.0},
            "BTC": {"value": 12000.0, "risk": 600.0}
        }
        
        risk_metrics = await mean_reversion_strategy.calculate_risk_metrics(positions)
        
        assert "total_value" in risk_metrics
        assert "total_risk" in risk_metrics
        assert "risk_ratio" in risk_metrics
        assert "position_count" in risk_metrics
        assert "avg_position_size" in risk_metrics
        assert risk_metrics["total_value"] == 20000.0
        assert risk_metrics["total_risk"] == 1000.0
        assert risk_metrics["position_count"] == 2

class TestStrategyExecutor:
    """Test suite for StrategyExecutor"""
    
    @pytest.fixture
    async def strategy_executor(self):
        """Create strategy executor instance for testing"""
        db_manager = Mock(spec=DatabaseManager)
        config_manager = Mock(spec=ConfigManager)
        notification_manager = Mock(spec=NotificationManager)
        
        # Mock configuration
        config_manager.get_config.side_effect = lambda key: {
            "redis": {"host": "localhost", "port": 6379, "db": 0},
            "risk_limits": {"max_total_risk": 0.1}
        }.get(key, {})
        
        executor = StrategyExecutor(db_manager, config_manager, notification_manager)
        
        # Mock Redis client
        executor.redis_client = AsyncMock()
        
        # Mock database session
        executor.db_manager.get_session.return_value.__aenter__ = AsyncMock()
        executor.db_manager.get_session.return_value.__aexit__ = AsyncMock()
        
        await executor.initialize()
        return executor
    
    @pytest.mark.asyncio
    async def test_create_momentum_strategy(self, strategy_executor):
        """Test creating momentum strategy"""
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_momentum_001",
            strategy_type="momentum",
            parameters={"lookback_period": 20, "threshold": 0.02},
            fund_id="test_fund_001"
        )
        
        assert strategy_id == "test_momentum_001"
        assert strategy_id in strategy_executor.strategies
        assert strategy_id in strategy_executor.executions
        assert isinstance(strategy_executor.strategies[strategy_id], MomentumStrategy)
    
    @pytest.mark.asyncio
    async def test_create_mean_reversion_strategy(self, strategy_executor):
        """Test creating mean reversion strategy"""
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_mean_reversion_001",
            strategy_type="mean_reversion",
            parameters={"lookback_period": 14, "deviation_threshold": 2.0},
            fund_id="test_fund_001"
        )
        
        assert strategy_id == "test_mean_reversion_001"
        assert strategy_id in strategy_executor.strategies
        assert strategy_id in strategy_executor.executions
        assert isinstance(strategy_executor.strategies[strategy_id], MeanReversionStrategy)
    
    @pytest.mark.asyncio
    async def test_start_strategy(self, strategy_executor):
        """Test starting strategy execution"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        # Start strategy
        success = await strategy_executor.start_strategy(strategy_id)
        
        assert success is True
        assert strategy_executor.strategies[strategy_id].status == StrategyStatus.ACTIVE
        assert strategy_executor.executions[strategy_id].status == StrategyStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_stop_strategy(self, strategy_executor):
        """Test stopping strategy execution"""
        # Create and start strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        await strategy_executor.start_strategy(strategy_id)
        
        # Stop strategy
        success = await strategy_executor.stop_strategy(strategy_id)
        
        assert success is True
        assert strategy_executor.strategies[strategy_id].status == StrategyStatus.STOPPED
        assert strategy_executor.executions[strategy_id].status == StrategyStatus.STOPPED
        assert strategy_executor.executions[strategy_id].end_time is not None
    
    @pytest.mark.asyncio
    async def test_execute_signal(self, strategy_executor):
        """Test executing a trading signal"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        # Create signal
        signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id=strategy_id,
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        # Execute signal
        order = await strategy_executor.execute_signal(signal, "test_fund_001")
        
        assert order is not None
        assert order.order_id in strategy_executor.orders
        assert order.strategy_id == strategy_id
        assert order.symbol == "BTC"
        assert order.side == OrderSide.BUY
        assert order.status == OrderStatus.FILLED
    
    @pytest.mark.asyncio
    async def test_get_strategy_performance(self, strategy_executor):
        """Test getting strategy performance"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        # Get performance
        performance = await strategy_executor.get_strategy_performance(strategy_id)
        
        assert performance is not None
        assert "strategy_id" in performance
        assert "name" in performance
        assert "status" in performance
        assert "total_signals" in performance
        assert "successful_signals" in performance
        assert "total_orders" in performance
        assert "total_pnl" in performance
    
    @pytest.mark.asyncio
    async def test_backtest_strategy(self, strategy_executor):
        """Test backtesting a strategy"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        # Run backtest
        start_date = datetime.now(datetime.UTC) - timedelta(days=30)
        end_date = datetime.now(datetime.UTC)
        initial_capital = 100000.0
        
        backtest_results = await strategy_executor.backtest_strategy(
            strategy_id=strategy_id,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital
        )
        
        assert backtest_results is not None
        assert "initial_capital" in backtest_results
        assert "final_capital" in backtest_results
        assert "total_return" in backtest_results
        assert "sharpe_ratio" in backtest_results
        assert "max_drawdown" in backtest_results
        assert "total_trades" in backtest_results
        assert "equity_curve" in backtest_results
        assert "trades" in backtest_results
    
    @pytest.mark.asyncio
    async def test_signal_validation(self, strategy_executor):
        """Test signal validation"""
        # Valid signal
        valid_signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id="test_strategy_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await strategy_executor._validate_signal(valid_signal) is True
        
        # Invalid signal - negative price
        invalid_signal = TradingSignal(
            signal_id="test_signal_002",
            strategy_id="test_strategy_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=-45000.0,  # Invalid
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await strategy_executor._validate_signal(invalid_signal) is False
    
    @pytest.mark.asyncio
    async def test_risk_limits_check(self, strategy_executor):
        """Test risk limits checking"""
        # Mock fund positions
        strategy_executor._get_fund_positions = AsyncMock(return_value={
            "BTC": {"value": 50000.0, "risk": 2500.0},
            "ETH": {"value": 30000.0, "risk": 1500.0}
        })
        
        strategy_executor._get_portfolio_value = AsyncMock(return_value=100000.0)
        
        # Create signal within risk limits
        signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id="test_strategy_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=0.1,  # Small position
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await strategy_executor._check_risk_limits(signal, "test_fund_001") is True
        
        # Create signal that exceeds risk limits
        large_signal = TradingSignal(
            signal_id="test_signal_002",
            strategy_id="test_strategy_001",
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=10.0,  # Large position
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        assert await strategy_executor._check_risk_limits(large_signal, "test_fund_001") is False
    
    @pytest.mark.asyncio
    async def test_order_creation(self, strategy_executor):
        """Test order creation from signal"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        # Mock portfolio value
        strategy_executor._get_portfolio_value = AsyncMock(return_value=100000.0)
        
        # Create signal
        signal = TradingSignal(
            signal_id="test_signal_001",
            strategy_id=strategy_id,
            symbol="BTC",
            signal_type=SignalType.BUY,
            strength=0.8,
            price=45000.0,
            quantity=1.0,
            stop_loss=42750.0,
            take_profit=49500.0,
            confidence=0.7,
            metadata={},
            created_at=datetime.now(datetime.UTC)
        )
        
        # Create order
        order = await strategy_executor._create_order(signal, "test_fund_001")
        
        assert order is not None
        assert order.strategy_id == strategy_id
        assert order.symbol == "BTC"
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.MARKET
        assert order.quantity > 0
        assert order.price == signal.price
        assert order.stop_price == signal.stop_loss
    
    @pytest.mark.asyncio
    async def test_order_submission(self, strategy_executor):
        """Test order submission"""
        # Create order
        order = Order(
            order_id="test_order_001",
            strategy_id="test_strategy_001",
            symbol="BTC",
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            quantity=1.0,
            price=45000.0,
            stop_price=None,
            status=OrderStatus.PENDING,
            filled_quantity=0.0,
            average_fill_price=None,
            commission=0.0,
            metadata={},
            created_at=datetime.now(datetime.UTC),
            updated_at=datetime.now(datetime.UTC)
        )
        
        # Submit order
        success = await strategy_executor._submit_order(order)
        
        assert success is True
        assert order.status == OrderStatus.FILLED
        assert order.filled_quantity == order.quantity
        assert order.average_fill_price == order.price
        assert order.commission > 0
    
    @pytest.mark.asyncio
    async def test_market_data_retrieval(self, strategy_executor):
        """Test market data retrieval"""
        market_data = await strategy_executor._get_market_data()
        
        assert market_data is not None
        assert "BTC" in market_data
        assert "ETH" in market_data
        assert "prices" in market_data["BTC"]
        assert "volume" in market_data["BTC"]
        assert "timestamp" in market_data["BTC"]
        assert len(market_data["BTC"]["prices"]) > 0
    
    @pytest.mark.asyncio
    async def test_historical_data_retrieval(self, strategy_executor):
        """Test historical data retrieval"""
        start_date = datetime.now(datetime.UTC) - timedelta(days=30)
        end_date = datetime.now(datetime.UTC)
        
        historical_data = await strategy_executor._get_historical_data(start_date, end_date)
        
        assert historical_data is not None
        assert "BTC" in historical_data
        assert "ETH" in historical_data
        assert "prices" in historical_data["BTC"]
        assert "dates" in historical_data["BTC"]
        assert len(historical_data["BTC"]["prices"]) > 0
        assert len(historical_data["BTC"]["dates"]) > 0
    
    @pytest.mark.asyncio
    async def test_max_drawdown_calculation(self, strategy_executor):
        """Test maximum drawdown calculation"""
        equity_curve = [100000, 105000, 110000, 108000, 112000, 109000, 115000, 113000, 118000, 116000, 120000]
        
        max_drawdown = strategy_executor._calculate_max_drawdown(equity_curve)
        
        assert max_drawdown >= 0
        assert max_drawdown <= 1.0  # Should be a percentage
    
    @pytest.mark.asyncio
    async def test_error_handling(self, strategy_executor):
        """Test error handling in strategy operations"""
        # Test creating strategy with invalid type
        with pytest.raises(ValueError):
            await strategy_executor.create_strategy(
                strategy_id="test_strategy_001",
                strategy_type="invalid_type",
                parameters={},
                fund_id="test_fund_001"
            )
        
        # Test starting non-existent strategy
        success = await strategy_executor.start_strategy("non_existent_strategy")
        assert success is False
        
        # Test stopping non-existent strategy
        success = await strategy_executor.stop_strategy("non_existent_strategy")
        assert success is False
        
        # Test getting performance of non-existent strategy
        performance = await strategy_executor.get_strategy_performance("non_existent_strategy")
        assert performance == {}
    
    @pytest.mark.asyncio
    async def test_strategy_parameter_updates(self, strategy_executor):
        """Test strategy parameter updates"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={"lookback_period": 20, "threshold": 0.02},
            fund_id="test_fund_001"
        )
        
        strategy = strategy_executor.strategies[strategy_id]
        
        # Update parameters
        new_parameters = {"lookback_period": 30, "threshold": 0.03}
        await strategy.update_parameters(new_parameters)
        
        assert strategy.parameters["lookback_period"] == 30
        assert strategy.parameters["threshold"] == 0.03
    
    @pytest.mark.asyncio
    async def test_strategy_performance_summary(self, strategy_executor):
        """Test strategy performance summary"""
        # Create strategy first
        strategy_id = await strategy_executor.create_strategy(
            strategy_id="test_strategy_001",
            strategy_type="momentum",
            parameters={},
            fund_id="test_fund_001"
        )
        
        strategy = strategy_executor.strategies[strategy_id]
        
        # Get performance summary
        summary = await strategy.get_performance_summary()
        
        assert "strategy_id" in summary
        assert "name" in summary
        assert "status" in summary
        assert "total_signals" in summary
        assert "positions" in summary
        assert "orders" in summary
        assert "performance_metrics" in summary

class TestStrategyEngineAPI:
    """Test suite for Strategy Engine API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from .api.strategy_engine_api import router
        
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    
    def test_create_strategy_endpoint(self, client):
        """Test strategy creation endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "TRADER"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_exec.create_strategy.return_value = "test_strategy_001"
                mock_executor.return_value = mock_exec
                
                response = client.post(
                    "/api/v1/strategy-engine/strategies",
                    json={
                        "strategy_type": "momentum",
                        "name": "Test Momentum Strategy",
                        "description": "A test momentum strategy",
                        "fund_id": "test_fund_001",
                        "parameters": {"lookback_period": 20, "threshold": 0.02}
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
                assert "strategy_id" in data
    
    def test_get_strategies_endpoint(self, client):
        """Test get strategies endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_strategy = Mock()
                mock_strategy.name = "Test Strategy"
                mock_strategy.description = "Test Description"
                mock_strategy.status = StrategyStatus.ACTIVE
                mock_strategy.parameters = {}
                mock_strategy.risk_parameters = {}
                mock_strategy.execution_parameters = {}
                
                mock_execution = Mock()
                mock_execution.fund_id = "test_fund_001"
                mock_execution.created_at = datetime.now(datetime.UTC)
                mock_execution.updated_at = datetime.now(datetime.UTC)
                
                mock_exec.strategies = {"test_strategy_001": mock_strategy}
                mock_exec.executions = {"test_strategy_001": mock_execution}
                mock_executor.return_value = mock_exec
                
                response = client.get(
                    "/api/v1/strategy-engine/strategies",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "strategies" in data
                assert "total_count" in data
    
    def test_start_strategy_endpoint(self, client):
        """Test start strategy endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "TRADER"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_strategy = Mock()
                mock_exec.strategies = {"test_strategy_001": mock_strategy}
                mock_exec.start_strategy.return_value = True
                mock_executor.return_value = mock_exec
                
                response = client.post(
                    "/api/v1/strategy-engine/strategies/test_strategy_001/start",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_stop_strategy_endpoint(self, client):
        """Test stop strategy endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "TRADER"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_strategy = Mock()
                mock_exec.strategies = {"test_strategy_001": mock_strategy}
                mock_exec.stop_strategy.return_value = True
                mock_executor.return_value = mock_exec
                
                response = client.post(
                    "/api/v1/strategy-engine/strategies/test_strategy_001/stop",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "success"
    
    def test_get_performance_endpoint(self, client):
        """Test get strategy performance endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_strategy = Mock()
                mock_exec.strategies = {"test_strategy_001": mock_strategy}
                mock_exec.get_strategy_performance.return_value = {
                    "strategy_id": "test_strategy_001",
                    "name": "Test Strategy",
                    "status": "active",
                    "total_signals": 10,
                    "successful_signals": 8,
                    "total_orders": 8,
                    "filled_orders": 7,
                    "total_pnl": 1000.0,
                    "total_commission": 50.0,
                    "net_pnl": 950.0,
                    "max_drawdown": 0.05,
                    "sharpe_ratio": 1.2,
                    "win_rate": 0.8,
                    "positions": 3,
                    "active_orders": 1
                }
                mock_executor.return_value = mock_exec
                
                response = client.get(
                    "/api/v1/strategy-engine/strategies/test_strategy_001/performance",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["strategy_id"] == "test_strategy_001"
                assert data["total_signals"] == 10
                assert data["total_pnl"] == 1000.0
    
    def test_backtest_endpoint(self, client):
        """Test backtest strategy endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ANALYST"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_strategy = Mock()
                mock_exec.strategies = {"test_strategy_001": mock_strategy}
                mock_exec.backtest_strategy.return_value = {
                    "initial_capital": 100000.0,
                    "final_capital": 110000.0,
                    "total_return": 0.1,
                    "sharpe_ratio": 1.2,
                    "max_drawdown": 0.05,
                    "total_trades": 20,
                    "winning_trades": 12,
                    "equity_curve": [100000, 101000, 102000, 110000],
                    "trades": []
                }
                mock_executor.return_value = mock_exec
                
                response = client.post(
                    "/api/v1/strategy-engine/strategies/test_strategy_001/backtest",
                    json={
                        "strategy_id": "test_strategy_001",
                        "start_date": "2025-01-01T00:00:00Z",
                        "end_date": "2025-01-31T23:59:59Z",
                        "initial_capital": 100000.0,
                        "symbols": ["BTC", "ETH"]
                    },
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert data["strategy_id"] == "test_strategy_001"
                assert data["initial_capital"] == 100000.0
                assert data["final_capital"] == 110000.0
                assert data["total_return"] == 0.1
    
    def test_get_statistics_endpoint(self, client):
        """Test get strategy statistics endpoint"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "ADMIN"}
            
            # Mock strategy executor
            with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_strategy_executor') as mock_executor:
                mock_exec = AsyncMock()
                mock_exec.strategies = {"strategy1": Mock(), "strategy2": Mock()}
                mock_exec.orders = {"order1": Mock(), "order2": Mock()}
                mock_exec.executions = {"exec1": Mock(), "exec2": Mock()}
                mock_executor.return_value = mock_exec
                
                response = client.get(
                    "/api/v1/strategy-engine/statistics",
                    headers={"Authorization": "Bearer test_token"}
                )
                
                assert response.status_code == 200
                data = response.json()
                assert "total_strategies" in data
                assert "active_strategies" in data
                assert "total_orders" in data
                assert "total_pnl" in data
    
    def test_unauthorized_access(self, client):
        """Test unauthorized access to endpoints"""
        # Test without authentication
        response = client.get("/api/v1/strategy-engine/strategies")
        assert response.status_code == 401
        
        # Test with invalid token
        response = client.get(
            "/api/v1/strategy-engine/strategies",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_insufficient_permissions(self, client):
        """Test insufficient permissions for admin-only endpoints"""
        # Mock authentication with non-admin user
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "USER"}
            
            response = client.post(
                "/api/v1/strategy-engine/strategies",
                json={
                    "strategy_type": "momentum",
                    "name": "Test Strategy",
                    "description": "Test Description",
                    "fund_id": "test_fund_001"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 403
    
    def test_invalid_input_validation(self, client):
        """Test input validation for API endpoints"""
        # Mock authentication
        with patch('src.pocket_hedge_fund.api.strategy_engine_api.get_current_user') as mock_auth:
            mock_auth.return_value = {"user_id": "test_user", "role": "TRADER"}
            
            # Test with invalid strategy type
            response = client.post(
                "/api/v1/strategy-engine/strategies",
                json={
                    "strategy_type": "invalid_type",
                    "name": "Test Strategy",
                    "description": "Test Description",
                    "fund_id": "test_fund_001"
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400
            
            # Test with invalid backtest dates
            response = client.post(
                "/api/v1/strategy-engine/strategies/test_strategy_001/backtest",
                json={
                    "strategy_id": "test_strategy_001",
                    "start_date": "2025-01-31T23:59:59Z",
                    "end_date": "2025-01-01T00:00:00Z",  # End before start
                    "initial_capital": 100000.0
                },
                headers={"Authorization": "Bearer test_token"}
            )
            
            assert response.status_code == 400

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
