"""
Backtesting Module for SCHR Levels AutoML

Provides comprehensive backtesting capabilities for trading strategies.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import logging


class SCHRBacktester:
    """Backtesting engine for SCHR Levels strategies"""
    
    def __init__(self, data_path: str, initial_capital: float = 10000, 
                 commission: float = 0.001):
        self.data_path = data_path
        self.initial_capital = initial_capital
        self.commission = commission
        self.logger = logging.getLogger(__name__)
    
    def run_backtest(self, symbol: str, timeframe: str, 
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None,
                    strategy: str = 'simple') -> Dict[str, Any]:
        """Run backtesting analysis"""
        try:
            # Load data
            data = self._load_data(symbol, timeframe)
            
            # Filter by date range
            if start_date:
                data = data[data.index >= start_date]
            if end_date:
                data = data[data.index <= end_date]
            
            self.logger.info(f"Backtesting {len(data)} records from {data.index[0]} to {data.index[-1]}")
            
            # Run strategy
            if strategy == 'simple':
                results = self._run_simple_strategy(data)
            elif strategy == 'advanced':
                results = self._run_advanced_strategy(data)
            elif strategy == 'ensemble':
                results = self._run_ensemble_strategy(data)
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
            
            # Calculate performance metrics
            metrics = self._calculate_metrics(results)
            
            return {
                'strategy': strategy,
                'symbol': symbol,
                'timeframe': timeframe,
                'start_date': data.index[0].strftime('%Y-%m-%d'),
                'end_date': data.index[-1].strftime('%Y-%m-%d'),
                'initial_capital': self.initial_capital,
                'final_capital': results['equity_curve'][-1],
                'total_return': (results['equity_curve'][-1] - self.initial_capital) / self.initial_capital,
                'equity_curve': results['equity_curve'],
                'drawdown': results['drawdown'],
                'returns': results['returns'],
                'trades': results['trades'],
                'metrics': metrics
            }
            
        except Exception as e:
            self.logger.error(f"Backtesting failed: {e}")
            raise
    
    def _load_data(self, symbol: str, timeframe: str) -> pd.DataFrame:
        """Load and prepare data for backtesting"""
        import os
        
        filename = f"CSVExport_{symbol}_PERIOD_{timeframe}.parquet"
        file_path = os.path.join(self.data_path, filename)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pd.read_parquet(file_path)
        
        # Set datetime index
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
        
        return df
    
    def _run_simple_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run simple momentum strategy"""
        equity_curve = [self.initial_capital]
        drawdown = [0]
        returns = [0]
        trades = []
        position = 0
        entry_price = 0
        
        for i in range(1, len(data)):
            current_price = data['Close'].iloc[i]
            prev_price = data['Close'].iloc[i-1]
            
            # Simple momentum signal
            price_change = (current_price - prev_price) / prev_price
            
            # Trading logic
            if price_change > 0.02 and position <= 0:  # Buy signal
                if position < 0:  # Close short
                    pnl = (entry_price - current_price) * abs(position)
                    trades.append({
                        'date': data.index[i],
                        'type': 'close_short',
                        'price': current_price,
                        'pnl': pnl
                    })
                
                # Open long
                position = 1
                entry_price = current_price
                trades.append({
                    'date': data.index[i],
                    'type': 'open_long',
                    'price': current_price,
                    'pnl': 0
                })
                
            elif price_change < -0.02 and position >= 0:  # Sell signal
                if position > 0:  # Close long
                    pnl = (current_price - entry_price) * position
                    trades.append({
                        'date': data.index[i],
                        'type': 'close_long',
                        'price': current_price,
                        'pnl': pnl
                    })
                
                # Open short
                position = -1
                entry_price = current_price
                trades.append({
                    'date': data.index[i],
                    'type': 'open_short',
                    'price': current_price,
                    'pnl': 0
                })
            
            # Calculate current equity
            if position != 0:
                unrealized_pnl = (current_price - entry_price) * position
                current_equity = equity_curve[-1] + unrealized_pnl
            else:
                current_equity = equity_curve[-1]
            
            equity_curve.append(current_equity)
            
            # Calculate drawdown
            peak = max(equity_curve)
            current_dd = (peak - current_equity) / peak
            drawdown.append(current_dd)
            
            # Calculate returns
            period_return = (current_equity - equity_curve[-2]) / equity_curve[-2]
            returns.append(period_return)
        
        return {
            'equity_curve': equity_curve,
            'drawdown': drawdown,
            'returns': returns,
            'trades': trades
        }
    
    def _run_advanced_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run advanced strategy using SCHR Levels"""
        equity_curve = [self.initial_capital]
        drawdown = [0]
        returns = [0]
        trades = []
        position = 0
        entry_price = 0
        
        for i in range(1, len(data)):
            current_price = data['Close'].iloc[i]
            
            # SCHR Levels signals
            if 'predicted_high' in data.columns and 'predicted_low' in data.columns:
                pred_high = data['predicted_high'].iloc[i]
                pred_low = data['predicted_low'].iloc[i]
                pressure = data['pressure'].iloc[i] if 'pressure' in data.columns else 0
                
                # Advanced logic using SCHR Levels
                if current_price > pred_high and pressure > 0 and position <= 0:
                    # Breakout above predicted high with positive pressure
                    if position < 0:
                        pnl = (entry_price - current_price) * abs(position)
                        trades.append({
                            'date': data.index[i],
                            'type': 'close_short',
                            'price': current_price,
                            'pnl': pnl
                        })
                    
                    position = 1
                    entry_price = current_price
                    trades.append({
                        'date': data.index[i],
                        'type': 'open_long',
                        'price': current_price,
                        'pnl': 0
                    })
                    
                elif current_price < pred_low and pressure < 0 and position >= 0:
                    # Breakout below predicted low with negative pressure
                    if position > 0:
                        pnl = (current_price - entry_price) * position
                        trades.append({
                            'date': data.index[i],
                            'type': 'close_long',
                            'price': current_price,
                            'pnl': pnl
                        })
                    
                    position = -1
                    entry_price = current_price
                    trades.append({
                        'date': data.index[i],
                        'type': 'open_short',
                        'price': current_price,
                        'pnl': 0
                    })
            
            # Calculate equity (same as simple strategy)
            if position != 0:
                unrealized_pnl = (current_price - entry_price) * position
                current_equity = equity_curve[-1] + unrealized_pnl
            else:
                current_equity = equity_curve[-1]
            
            equity_curve.append(current_equity)
            
            peak = max(equity_curve)
            current_dd = (peak - current_equity) / peak
            drawdown.append(current_dd)
            
            period_return = (current_equity - equity_curve[-2]) / equity_curve[-2]
            returns.append(period_return)
        
        return {
            'equity_curve': equity_curve,
            'drawdown': drawdown,
            'returns': returns,
            'trades': trades
        }
    
    def _run_ensemble_strategy(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Run ensemble strategy combining multiple signals"""
        # This would combine multiple models and signals
        # For now, use advanced strategy as base
        return self._run_advanced_strategy(data)
    
    def _calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Calculate performance metrics"""
        equity_curve = results['equity_curve']
        returns = results['returns']
        trades = results['trades']
        
        # Basic metrics
        total_return = (equity_curve[-1] - self.initial_capital) / self.initial_capital
        max_drawdown = max(results['drawdown'])
        
        # Sharpe ratio
        if len(returns) > 1:
            sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)
        else:
            sharpe_ratio = 0
        
        # Win rate
        profitable_trades = [t for t in trades if t['pnl'] > 0]
        win_rate = len(profitable_trades) / len(trades) if trades else 0
        
        # Profit factor
        gross_profit = sum(t['pnl'] for t in trades if t['pnl'] > 0)
        gross_loss = abs(sum(t['pnl'] for t in trades if t['pnl'] < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        return {
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_trades': len(trades)
        }
