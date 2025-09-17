"""
Backtesting Engine for Pocket Hedge Fund.

This module provides comprehensive backtesting functionality
for trading strategies and ML models.
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass
from enum import Enum

from ..ml.price_predictor import PricePredictor
from ..trading.automated_trader import AutomatedTrader, TradingStrategy
from ..data.data_manager import DataManager
from ..analysis.indicator_integration_simple import IndicatorIntegration
from ..portfolio.portfolio_manager import PortfolioManager

logger = logging.getLogger(__name__)

class BacktestMode(Enum):
    """Backtesting modes."""
    WALK_FORWARD = "walk_forward"
    FIXED_WINDOW = "fixed_window"
    EXPANDING_WINDOW = "expanding_window"

@dataclass
class BacktestConfig:
    """Backtesting configuration."""
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000.0
    commission: float = 0.001  # 0.1% commission
    slippage: float = 0.0005   # 0.05% slippage
    mode: BacktestMode = BacktestMode.WALK_FORWARD
    train_window_days: int = 252  # 1 year
    test_window_days: int = 63    # 3 months
    retrain_frequency_days: int = 21  # Retrain every 3 weeks

@dataclass
class BacktestResult:
    """Backtesting result."""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    profit_factor: float
    calmar_ratio: float
    sortino_ratio: float
    trades: List[Dict[str, Any]]
    equity_curve: pd.DataFrame
    performance_metrics: Dict[str, Any]

class BacktestEngine:
    """Comprehensive backtesting engine for trading strategies."""
    
    def __init__(self, config: BacktestConfig):
        """Initialize BacktestEngine."""
        self.config = config
        self.data_manager = DataManager()
        self.trades = []
        self.equity_curve = []
        self.current_capital = config.initial_capital
        self.peak_capital = config.initial_capital
        self.max_drawdown = 0.0
        
    async def run_backtest(self, symbols: List[str], strategy: TradingStrategy, 
                          model_type: str = "ensemble") -> BacktestResult:
        """Run comprehensive backtest."""
        try:
            logger.info(f"Starting backtest for symbols: {symbols}")
            logger.info(f"Strategy: {strategy.value}, Model: {model_type}")
            logger.info(f"Period: {self.config.start_date} to {self.config.end_date}")
            
            # Initialize results
            self.trades = []
            self.equity_curve = []
            self.current_capital = self.config.initial_capital
            self.peak_capital = self.config.initial_capital
            self.max_drawdown = 0.0
            
            # Get data for all symbols
            symbol_data = {}
            for symbol in symbols:
                try:
                    if symbol.startswith('data/'):
                        data = await self.data_manager.get_local_data(symbol)
                    else:
                        data = await self.data_manager.get_yahoo_data(
                            symbol, 
                            start=self.config.start_date,
                            end=self.config.end_date
                        )
                    
                    if not data.empty:
                        symbol_data[symbol] = data
                        logger.info(f"Loaded {len(data)} records for {symbol}")
                    else:
                        logger.warning(f"No data available for {symbol}")
                        
                except Exception as e:
                    logger.error(f"Error loading data for {symbol}: {e}")
            
            if not symbol_data:
                raise ValueError("No data available for any symbol")
            
            # Run backtest based on mode
            if self.config.mode == BacktestMode.WALK_FORWARD:
                await self._run_walk_forward_backtest(symbol_data, strategy, model_type)
            elif self.config.mode == BacktestMode.FIXED_WINDOW:
                await self._run_fixed_window_backtest(symbol_data, strategy, model_type)
            elif self.config.mode == BacktestMode.EXPANDING_WINDOW:
                await self._run_expanding_window_backtest(symbol_data, strategy, model_type)
            
            # Calculate performance metrics
            result = self._calculate_performance_metrics()
            
            logger.info(f"Backtest completed. Total return: {result.total_return:.2%}")
            return result
            
        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            raise
    
    async def _run_walk_forward_backtest(self, symbol_data: Dict[str, pd.DataFrame], 
                                       strategy: TradingStrategy, model_type: str):
        """Run walk-forward backtest."""
        logger.info("Running walk-forward backtest")
        
        current_date = self.config.start_date
        while current_date < self.config.end_date:
            # Define training and test periods
            train_start = current_date - timedelta(days=self.config.train_window_days)
            train_end = current_date
            test_start = current_date
            test_end = min(current_date + timedelta(days=self.config.test_window_days), 
                          self.config.end_date)
            
            logger.info(f"Training period: {train_start} to {train_end}")
            logger.info(f"Test period: {test_start} to {test_end}")
            
            # Train models on training data
            trained_models = await self._train_models_for_period(
                symbol_data, train_start, train_end, model_type
            )
            
            # Test on test period
            await self._test_models_for_period(
                symbol_data, test_start, test_end, strategy, trained_models
            )
            
            # Move to next period
            current_date += timedelta(days=self.config.retrain_frequency_days)
    
    async def _run_fixed_window_backtest(self, symbol_data: Dict[str, pd.DataFrame], 
                                       strategy: TradingStrategy, model_type: str):
        """Run fixed window backtest."""
        logger.info("Running fixed window backtest")
        
        # Train on first part of data
        train_end = self.config.start_date + timedelta(days=self.config.train_window_days)
        trained_models = await self._train_models_for_period(
            symbol_data, self.config.start_date, train_end, model_type
        )
        
        # Test on remaining data
        await self._test_models_for_period(
            symbol_data, train_end, self.config.end_date, strategy, trained_models
        )
    
    async def _run_expanding_window_backtest(self, symbol_data: Dict[str, pd.DataFrame], 
                                           strategy: TradingStrategy, model_type: str):
        """Run expanding window backtest."""
        logger.info("Running expanding window backtest")
        
        current_date = self.config.start_date + timedelta(days=self.config.train_window_days)
        while current_date < self.config.end_date:
            # Train on expanding window
            trained_models = await self._train_models_for_period(
                symbol_data, self.config.start_date, current_date, model_type
            )
            
            # Test on next period
            test_end = min(current_date + timedelta(days=self.config.retrain_frequency_days),
                          self.config.end_date)
            await self._test_models_for_period(
                symbol_data, current_date, test_end, strategy, trained_models
            )
            
            current_date += timedelta(days=self.config.retrain_frequency_days)
    
    async def _train_models_for_period(self, symbol_data: Dict[str, pd.DataFrame], 
                                     start_date: datetime, end_date: datetime, 
                                     model_type: str) -> Dict[str, PricePredictor]:
        """Train models for a specific period."""
        trained_models = {}
        
        for symbol, data in symbol_data.items():
            try:
                # Filter data for training period
                # Ensure index is datetime
                if not isinstance(data.index, pd.DatetimeIndex):
                    data.index = pd.to_datetime(data.index)
                train_data = data[(data.index >= start_date) & (data.index < end_date)]
                
                if len(train_data) < 50:  # Need minimum data for training
                    logger.warning(f"Insufficient data for {symbol} in training period")
                    continue
                
                # Create and train predictor
                predictor = PricePredictor(model_type=model_type)
                await predictor.train_models(train_data)
                trained_models[symbol] = predictor
                
                logger.info(f"Trained model for {symbol} on {len(train_data)} records")
                
            except Exception as e:
                logger.error(f"Error training model for {symbol}: {e}")
        
        return trained_models
    
    async def _test_models_for_period(self, symbol_data: Dict[str, pd.DataFrame], 
                                    start_date: datetime, end_date: datetime, 
                                    strategy: TradingStrategy, 
                                    trained_models: Dict[str, PricePredictor]):
        """Test models for a specific period."""
        for symbol, data in symbol_data.items():
            if symbol not in trained_models:
                continue
            
            try:
                # Filter data for test period
                # Ensure index is datetime
                if not isinstance(data.index, pd.DatetimeIndex):
                    data.index = pd.to_datetime(data.index)
                test_data = data[(data.index >= start_date) & (data.index < end_date)]
                
                if test_data.empty:
                    continue
                
                predictor = trained_models[symbol]
                
                # Generate signals for each day
                for i in range(len(test_data)):
                    current_data = test_data.iloc[:i+1]
                    if len(current_data) < 20:  # Need minimum data for prediction
                        continue
                    
                    # Make prediction
                    prediction_result = await predictor.predict(current_data)
                    
                    if prediction_result['status'] == 'success':
                        # Generate trading signal
                        signal = self._generate_trading_signal(
                            prediction_result, strategy, symbol, current_data.iloc[-1]
                        )
                        
                        if signal['action'] != 'HOLD':
                            # Execute trade
                            await self._execute_trade(signal, current_data.iloc[-1])
                    
                    # Update equity curve
                    self._update_equity_curve(current_data.index[i])
                
            except Exception as e:
                logger.error(f"Error testing model for {symbol}: {e}")
    
    def _generate_trading_signal(self, prediction_result: Dict[str, Any], 
                               strategy: TradingStrategy, symbol: str, 
                               current_bar: pd.Series) -> Dict[str, Any]:
        """Generate trading signal based on prediction and strategy."""
        try:
            predictions = prediction_result.get('predictions', {})
            
            # Get ensemble prediction
            ensemble_pred = predictions.get('ensemble', {})
            if not ensemble_pred or 'prediction' not in ensemble_pred:
                return {'action': 'HOLD', 'confidence': 0.0}
            
            prediction = ensemble_pred['prediction']
            confidence = ensemble_pred['confidence']
            
            # Generate signal based on strategy
            if strategy == TradingStrategy.CONSERVATIVE:
                threshold = 0.02  # 2% threshold
                min_confidence = 0.8
            elif strategy == TradingStrategy.AGGRESSIVE:
                threshold = 0.01  # 1% threshold
                min_confidence = 0.6
            else:  # Combined or others
                threshold = 0.015  # 1.5% threshold
                min_confidence = 0.7
            
            if confidence >= min_confidence:
                if prediction > threshold:
                    return {
                        'action': 'BUY',
                        'symbol': symbol,
                        'confidence': confidence,
                        'prediction': prediction,
                        'price': current_bar['close']
                    }
                elif prediction < -threshold:
                    return {
                        'action': 'SELL',
                        'symbol': symbol,
                        'confidence': confidence,
                        'prediction': prediction,
                        'price': current_bar['close']
                    }
            
            return {'action': 'HOLD', 'confidence': confidence}
            
        except Exception as e:
            logger.error(f"Error generating trading signal: {e}")
            return {'action': 'HOLD', 'confidence': 0.0}
    
    async def _execute_trade(self, signal: Dict[str, Any], current_bar: pd.Series):
        """Execute a trade based on signal."""
        try:
            symbol = signal['symbol']
            action = signal['action']
            price = signal['price']
            confidence = signal['confidence']
            
            # Calculate position size based on confidence
            position_size_pct = min(0.1, confidence * 0.15)  # Max 10%, scaled by confidence
            position_value = self.current_capital * position_size_pct
            
            if action == 'BUY':
                # Buy position
                quantity = position_value / price
                commission = position_value * self.config.commission
                slippage = position_value * self.config.slippage
                
                total_cost = position_value + commission + slippage
                
                if total_cost <= self.current_capital:
                    self.current_capital -= total_cost
                    
                    trade = {
                        'timestamp': current_bar.name,
                        'symbol': symbol,
                        'action': 'BUY',
                        'quantity': quantity,
                        'price': price,
                        'value': position_value,
                        'commission': commission,
                        'slippage': slippage,
                        'confidence': confidence,
                        'capital_after': self.current_capital
                    }
                    
                    self.trades.append(trade)
                    logger.info(f"Executed BUY: {symbol} {quantity:.2f} @ {price:.2f}")
            
            elif action == 'SELL':
                # Sell position (simplified - would need position tracking)
                quantity = position_value / price
                commission = position_value * self.config.commission
                slippage = position_value * self.config.slippage
                
                proceeds = position_value - commission - slippage
                self.current_capital += proceeds
                
                trade = {
                    'timestamp': current_bar.name,
                    'symbol': symbol,
                    'action': 'SELL',
                    'quantity': quantity,
                    'price': price,
                    'value': position_value,
                    'commission': commission,
                    'slippage': slippage,
                    'confidence': confidence,
                    'capital_after': self.current_capital
                }
                
                self.trades.append(trade)
                logger.info(f"Executed SELL: {symbol} {quantity:.2f} @ {price:.2f}")
            
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
    
    def _update_equity_curve(self, timestamp):
        """Update equity curve."""
        self.equity_curve.append({
            'timestamp': timestamp,
            'capital': self.current_capital,
            'return': (self.current_capital - self.config.initial_capital) / self.config.initial_capital
        })
        
        # Update peak and drawdown
        if self.current_capital > self.peak_capital:
            self.peak_capital = self.current_capital
        
        current_drawdown = (self.peak_capital - self.current_capital) / self.peak_capital
        if current_drawdown > self.max_drawdown:
            self.max_drawdown = current_drawdown
    
    def _calculate_performance_metrics(self) -> BacktestResult:
        """Calculate comprehensive performance metrics."""
        try:
            if not self.trades:
                return self._create_empty_result()
            
            # Convert trades to DataFrame
            trades_df = pd.DataFrame(self.trades)
            equity_df = pd.DataFrame(self.equity_curve)
            
            # Basic metrics
            total_return = (self.current_capital - self.config.initial_capital) / self.config.initial_capital
            
            # Calculate annualized return
            days = (self.config.end_date - self.config.start_date).days
            years = days / 365.25
            annualized_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0
            
            # Calculate volatility
            if len(equity_df) > 1:
                returns = equity_df['return'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252) if len(returns) > 1 else 0
            else:
                volatility = 0
            
            # Calculate Sharpe ratio
            risk_free_rate = 0.02  # 2% risk-free rate
            sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            # Calculate Sortino ratio
            downside_returns = returns[returns < 0]
            downside_volatility = downside_returns.std() * np.sqrt(252) if len(downside_returns) > 1 else 0
            sortino_ratio = (annualized_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else 0
            
            # Calculate Calmar ratio
            calmar_ratio = annualized_return / self.max_drawdown if self.max_drawdown > 0 else 0
            
            # Trade statistics
            total_trades = len(trades_df)
            winning_trades = len(trades_df[trades_df['action'] == 'SELL'])  # Simplified
            losing_trades = total_trades - winning_trades
            win_rate = winning_trades / total_trades if total_trades > 0 else 0
            
            # Average win/loss
            avg_win = trades_df[trades_df['action'] == 'SELL']['value'].mean() if winning_trades > 0 else 0
            avg_loss = trades_df[trades_df['action'] == 'BUY']['value'].mean() if losing_trades > 0 else 0
            
            # Profit factor
            gross_profit = trades_df[trades_df['action'] == 'SELL']['value'].sum() if winning_trades > 0 else 0
            gross_loss = trades_df[trades_df['action'] == 'BUY']['value'].sum() if losing_trades > 0 else 0
            profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
            
            return BacktestResult(
                total_return=total_return,
                annualized_return=annualized_return,
                volatility=volatility,
                sharpe_ratio=sharpe_ratio,
                max_drawdown=self.max_drawdown,
                win_rate=win_rate,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades,
                avg_win=avg_win,
                avg_loss=avg_loss,
                profit_factor=profit_factor,
                calmar_ratio=calmar_ratio,
                sortino_ratio=sortino_ratio,
                trades=self.trades,
                equity_curve=equity_df,
                performance_metrics={
                    'gross_profit': gross_profit,
                    'gross_loss': gross_loss,
                    'net_profit': gross_profit - gross_loss,
                    'total_commission': trades_df['commission'].sum(),
                    'total_slippage': trades_df['slippage'].sum(),
                    'avg_confidence': trades_df['confidence'].mean(),
                    'best_trade': trades_df['value'].max() if not trades_df.empty else 0,
                    'worst_trade': trades_df['value'].min() if not trades_df.empty else 0
                }
            )
            
        except Exception as e:
            logger.error(f"Error calculating performance metrics: {e}")
            return self._create_empty_result()
    
    def _create_empty_result(self) -> BacktestResult:
        """Create empty result when no trades."""
        return BacktestResult(
            total_return=0.0,
            annualized_return=0.0,
            volatility=0.0,
            sharpe_ratio=0.0,
            max_drawdown=0.0,
            win_rate=0.0,
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            avg_win=0.0,
            avg_loss=0.0,
            profit_factor=0.0,
            calmar_ratio=0.0,
            sortino_ratio=0.0,
            trades=[],
            equity_curve=pd.DataFrame(),
            performance_metrics={}
        )
