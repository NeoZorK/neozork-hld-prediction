# -*- coding: utf-8 -*-
# src/calculation/trading_metrics.py

"""
Trading Metrics Calculation Module
Calculates comprehensive trading performance metrics for strategy evaluation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from src.common import logger
from src.common.constants import BUY, SELL, NOTRADE


class TradingMetricsCalculator:
    """
    Comprehensive trading metrics calculator for strategy evaluation.
    """
    
    def __init__(self, risk_free_rate: float = 0.02):
        """
        Initialize the trading metrics calculator.
        
        Args:
            risk_free_rate (float): Annual risk-free rate (default: 2%)
        """
        self.risk_free_rate = risk_free_rate
    
    def calculate_all_metrics(self, df: pd.DataFrame, 
                            price_col: str = 'Close',
                            signal_col: str = 'Direction',
                            volume_col: Optional[str] = 'Volume') -> Dict[str, float]:
        """
        Calculate all trading metrics for the given data.
        
        Args:
            df (pd.DataFrame): DataFrame with OHLCV data and trading signals
            price_col (str): Column name for price data
            signal_col (str): Column name for trading signals
            volume_col (str, optional): Column name for volume data
        
        Returns:
            Dict[str, float]: Dictionary containing all calculated metrics
        """
        try:
            # Validate input data
            if df.empty or price_col not in df.columns or signal_col not in df.columns:
                return self._get_empty_metrics()
            
            # Calculate trade counts
            buy_count, sell_count, total_trades = self._calculate_trade_counts(df, signal_col)
            
            # Calculate basic metrics
            win_ratio = self._calculate_win_ratio(df, price_col, signal_col)
            risk_reward_ratio = self._calculate_risk_reward_ratio(df, price_col, signal_col)
            profit_factor = self._calculate_profit_factor(df, price_col, signal_col)
            
            # Calculate risk-adjusted returns
            sharpe_ratio = self._calculate_sharpe_ratio(df, price_col, signal_col)
            sortino_ratio = self._calculate_sortino_ratio(df, price_col, signal_col)
            
            # Calculate probability metrics
            probability_risk_ratio = self._calculate_probability_risk_ratio(df, price_col, signal_col)
            
            # Calculate additional important metrics
            max_drawdown = self._calculate_max_drawdown(df, price_col, signal_col)
            total_return = self._calculate_total_return(df, price_col, signal_col)
            volatility = self._calculate_volatility(df, price_col, signal_col)
            calmar_ratio = self._calculate_calmar_ratio(total_return, max_drawdown)
            
            # Calculate volume-weighted metrics if volume data is available
            volume_metrics = {}
            if volume_col and volume_col in df.columns:
                volume_metrics = self._calculate_volume_metrics(df, price_col, signal_col, volume_col)
            
            # Compile all metrics
            metrics = {
                'buy_count': buy_count,
                'sell_count': sell_count,
                'total_trades': total_trades,
                'win_ratio': win_ratio,
                'risk_reward_ratio': risk_reward_ratio,
                'profit_factor': profit_factor,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'probability_risk_ratio': probability_risk_ratio,
                'max_drawdown': max_drawdown,
                'total_return': total_return,
                'volatility': volatility,
                'calmar_ratio': calmar_ratio,
                **volume_metrics
            }
            
            return metrics
            
        except Exception as e:
            logger.print_error(f"Error calculating trading metrics: {e}")
            return self._get_empty_metrics()
    
    def _calculate_win_ratio(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate win ratio (percentage of profitable trades)."""
        try:
            trades = self._extract_trades(df, price_col, signal_col)
            if not trades:
                return 0.0
            
            winning_trades = [trade for trade in trades if trade > 0]
            return len(winning_trades) / len(trades) * 100
            
        except Exception as e:
            logger.print_debug(f"Error calculating win ratio: {e}")
            return 0.0
    
    def _calculate_trade_counts(self, df: pd.DataFrame, signal_col: str) -> Tuple[int, int, int]:
        """Calculate buy, sell, and total trade counts."""
        try:
            if signal_col not in df.columns:
                return 0, 0, 0
            
            buy_count = int((df[signal_col] == BUY).sum())
            sell_count = int((df[signal_col] == SELL).sum())
            total_trades = buy_count + sell_count
            
            return buy_count, sell_count, total_trades
            
        except Exception as e:
            logger.print_debug(f"Error calculating trade counts: {e}")
            return 0, 0, 0
    
    def _calculate_risk_reward_ratio(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate risk-reward ratio (average win / average loss)."""
        try:
            trades = self._extract_trades(df, price_col, signal_col)
            if not trades:
                return 0.0
            
            winning_trades = [trade for trade in trades if trade > 0]
            losing_trades = [trade for trade in trades if trade < 0]
            
            if not winning_trades or not losing_trades:
                return 0.0
            
            avg_win = np.mean(winning_trades)
            avg_loss = abs(np.mean(losing_trades))
            
            return avg_win / avg_loss if avg_loss > 0 else 0.0
            
        except Exception as e:
            logger.print_debug(f"Error calculating risk-reward ratio: {e}")
            return 0.0
    
    def _calculate_profit_factor(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate profit factor (gross profit / gross loss)."""
        try:
            trades = self._extract_trades(df, price_col, signal_col)
            if not trades:
                return 0.0
            
            gross_profit = sum(trade for trade in trades if trade > 0)
            gross_loss = abs(sum(trade for trade in trades if trade < 0))
            
            return gross_profit / gross_loss if gross_loss > 0 else 0.0
            
        except Exception as e:
            logger.print_debug(f"Error calculating profit factor: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate Sharpe ratio (risk-adjusted return)."""
        try:
            returns = self._calculate_returns(df, price_col, signal_col)
            if len(returns) < 2:
                return 0.0
            
            mean_return = np.mean(returns)
            std_return = np.std(returns, ddof=1)
            
            if std_return == 0:
                return 0.0
            
            # Annualize the ratio (assuming daily data)
            sharpe = (mean_return - self.risk_free_rate / 252) / std_return * np.sqrt(252)
            return sharpe
            
        except Exception as e:
            logger.print_debug(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_sortino_ratio(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate Sortino ratio (downside risk-adjusted return)."""
        try:
            returns = self._calculate_returns(df, price_col, signal_col)
            if len(returns) < 2:
                return 0.0
            
            mean_return = np.mean(returns)
            downside_returns = returns[returns < 0]
            
            if len(downside_returns) == 0:
                return 0.0
            
            downside_std = np.std(downside_returns, ddof=1)
            
            if downside_std == 0:
                return 0.0
            
            # Annualize the ratio (assuming daily data)
            sortino = (mean_return - self.risk_free_rate / 252) / downside_std * np.sqrt(252)
            return sortino
            
        except Exception as e:
            logger.print_debug(f"Error calculating Sortino ratio: {e}")
            return 0.0
    
    def _calculate_probability_risk_ratio(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate probability risk ratio (probability of profit / probability of loss)."""
        try:
            trades = self._extract_trades(df, price_col, signal_col)
            if not trades:
                return 0.0
            
            winning_trades = [trade for trade in trades if trade > 0]
            losing_trades = [trade for trade in trades if trade < 0]
            
            prob_profit = len(winning_trades) / len(trades)
            prob_loss = len(losing_trades) / len(trades)
            
            return prob_profit / prob_loss if prob_loss > 0 else 0.0
            
        except Exception as e:
            logger.print_debug(f"Error calculating probability risk ratio: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate maximum drawdown percentage."""
        try:
            cumulative_returns = self._calculate_cumulative_returns(df, price_col, signal_col)
            if len(cumulative_returns) < 2:
                return 0.0
            
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - running_max) / running_max * 100
            max_drawdown = drawdown.min()
            
            return abs(max_drawdown)
            
        except Exception as e:
            logger.print_debug(f"Error calculating max drawdown: {e}")
            return 0.0
    
    def _calculate_total_return(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate total return percentage."""
        try:
            cumulative_returns = self._calculate_cumulative_returns(df, price_col, signal_col)
            if len(cumulative_returns) < 2:
                return 0.0
            
            total_return = (cumulative_returns.iloc[-1] - cumulative_returns.iloc[0]) / cumulative_returns.iloc[0] * 100
            return total_return
            
        except Exception as e:
            logger.print_debug(f"Error calculating total return: {e}")
            return 0.0
    
    def _calculate_volatility(self, df: pd.DataFrame, price_col: str, signal_col: str) -> float:
        """Calculate annualized volatility."""
        try:
            returns = self._calculate_returns(df, price_col, signal_col)
            if len(returns) < 2:
                return 0.0
            
            volatility = np.std(returns, ddof=1) * np.sqrt(252) * 100  # Annualized percentage
            return volatility
            
        except Exception as e:
            logger.print_debug(f"Error calculating volatility: {e}")
            return 0.0
    
    def _calculate_calmar_ratio(self, total_return: float, max_drawdown: float) -> float:
        """Calculate Calmar ratio (return / max drawdown)."""
        try:
            if max_drawdown == 0:
                return 0.0
            return total_return / max_drawdown
            
        except Exception as e:
            logger.print_debug(f"Error calculating Calmar ratio: {e}")
            return 0.0
    
    def _calculate_volume_metrics(self, df: pd.DataFrame, price_col: str, signal_col: str, volume_col: str) -> Dict[str, float]:
        """Calculate volume-weighted metrics."""
        try:
            trades = self._extract_trades_with_volume(df, price_col, signal_col, volume_col)
            if not trades:
                return {}
            
            # Volume-weighted average trade
            total_volume = sum(volume for _, volume in trades)
            volume_weighted_return = sum(return_val * volume for return_val, volume in trades) / total_volume
            
            # Volume-weighted win ratio
            winning_trades = [(ret, vol) for ret, vol in trades if ret > 0]
            losing_trades = [(ret, vol) for ret, vol in trades if ret < 0]
            
            winning_volume = sum(vol for _, vol in winning_trades)
            losing_volume = sum(vol for _, vol in losing_trades)
            
            volume_win_ratio = winning_volume / total_volume * 100 if total_volume > 0 else 0.0
            
            return {
                'volume_weighted_return': volume_weighted_return,
                'volume_win_ratio': volume_win_ratio
            }
            
        except Exception as e:
            logger.print_debug(f"Error calculating volume metrics: {e}")
            return {}
    
    def _extract_trades(self, df: pd.DataFrame, price_col: str, signal_col: str) -> list:
        """Extract individual trade returns from the data."""
        try:
            trades = []
            in_position = False
            entry_price = 0.0
            
            for i in range(1, len(df)):
                current_signal = df[signal_col].iloc[i]
                current_price = df[price_col].iloc[i]
                prev_price = df[price_col].iloc[i-1]
                
                # Check for entry signals
                if not in_position and current_signal == BUY:
                    in_position = True
                    entry_price = current_price
                
                # Check for exit signals or position reversal
                elif in_position and (current_signal == SELL or current_signal == BUY):
                    # Calculate trade return
                    trade_return = (current_price - entry_price) / entry_price * 100
                    trades.append(trade_return)
                    
                    # Update position
                    if current_signal == BUY:
                        entry_price = current_price  # New position
                    else:
                        in_position = False  # Exit position
            
            return trades
            
        except Exception as e:
            logger.print_debug(f"Error extracting trades: {e}")
            return []
    
    def _extract_trades_with_volume(self, df: pd.DataFrame, price_col: str, signal_col: str, volume_col: str) -> list:
        """Extract individual trade returns with volume data."""
        try:
            trades = []
            in_position = False
            entry_price = 0.0
            entry_volume = 0.0
            
            for i in range(1, len(df)):
                current_signal = df[signal_col].iloc[i]
                current_price = df[price_col].iloc[i]
                current_volume = df[volume_col].iloc[i]
                prev_price = df[price_col].iloc[i-1]
                
                # Check for entry signals
                if not in_position and current_signal == BUY:
                    in_position = True
                    entry_price = current_price
                    entry_volume = current_volume
                
                # Check for exit signals or position reversal
                elif in_position and (current_signal == SELL or current_signal == BUY):
                    # Calculate trade return
                    trade_return = (current_price - entry_price) / entry_price * 100
                    avg_volume = (entry_volume + current_volume) / 2
                    trades.append((trade_return, avg_volume))
                    
                    # Update position
                    if current_signal == BUY:
                        entry_price = current_price  # New position
                        entry_volume = current_volume
                    else:
                        in_position = False  # Exit position
            
            return trades
            
        except Exception as e:
            logger.print_debug(f"Error extracting trades with volume: {e}")
            return []
    
    def _calculate_returns(self, df: pd.DataFrame, price_col: str, signal_col: str) -> pd.Series:
        """Calculate daily returns based on trading signals."""
        try:
            returns = []
            in_position = False
            
            for i in range(1, len(df)):
                current_signal = df[signal_col].iloc[i]
                current_price = df[price_col].iloc[i]
                prev_price = df[price_col].iloc[i-1]
                
                # Check for entry signals
                if not in_position and current_signal == BUY:
                    in_position = True
                
                # Calculate return if in position
                if in_position:
                    daily_return = (current_price - prev_price) / prev_price
                    returns.append(daily_return)
                else:
                    returns.append(0.0)
                
                # Check for exit signals
                if in_position and current_signal == SELL:
                    in_position = False
            
            return pd.Series(returns)
            
        except Exception as e:
            logger.print_debug(f"Error calculating returns: {e}")
            return pd.Series()
    
    def _calculate_cumulative_returns(self, df: pd.DataFrame, price_col: str, signal_col: str) -> pd.Series:
        """Calculate cumulative returns based on trading signals."""
        try:
            returns = self._calculate_returns(df, price_col, signal_col)
            if returns.empty:
                return pd.Series()
            
            # Calculate cumulative returns starting from 1
            cumulative_returns = (1 + returns).cumprod()
            return cumulative_returns
            
        except Exception as e:
            logger.print_debug(f"Error calculating cumulative returns: {e}")
            return pd.Series()
    
    def _get_empty_metrics(self) -> Dict[str, float]:
        """Return empty metrics dictionary with zero values."""
        return {
            'buy_count': 0,
            'sell_count': 0,
            'total_trades': 0,
            'win_ratio': 0.0,
            'risk_reward_ratio': 0.0,
            'profit_factor': 0.0,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'probability_risk_ratio': 0.0,
            'max_drawdown': 0.0,
            'total_return': 0.0,
            'volatility': 0.0,
            'calmar_ratio': 0.0,
            'volume_weighted_return': 0.0,
            'volume_win_ratio': 0.0
        }


def calculate_trading_metrics(df: pd.DataFrame, 
                            price_col: str = 'Close',
                            signal_col: str = 'Direction',
                            volume_col: Optional[str] = 'Volume',
                            risk_free_rate: float = 0.02) -> Dict[str, float]:
    """
    Convenience function to calculate all trading metrics.
    
    Args:
        df (pd.DataFrame): DataFrame with OHLCV data and trading signals
        price_col (str): Column name for price data
        signal_col (str): Column name for trading signals
        volume_col (str, optional): Column name for volume data
        risk_free_rate (float): Annual risk-free rate
    
    Returns:
        Dict[str, float]: Dictionary containing all calculated metrics
    """
    calculator = TradingMetricsCalculator(risk_free_rate)
    return calculator.calculate_all_metrics(df, price_col, signal_col, volume_col) 