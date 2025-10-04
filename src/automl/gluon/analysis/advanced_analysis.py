"""
Advanced Analysis for Trading Strategy Models
Продвинутый анализ для моделей торговых стратегий
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

logger = logging.getLogger(__name__)


class AdvancedTradingAnalyzer:
    """
    Advanced analysis for trading strategy models including backtesting, 
    walk forward analysis, and Monte Carlo simulation.
    """
    
    def __init__(self, initial_capital: float = 10000):
        """
        Initialize Advanced Trading Analyzer.
        
        Args:
            initial_capital: Initial capital for backtesting
        """
        self.initial_capital = initial_capital
        
    def comprehensive_backtesting(self, model, test_data: pd.DataFrame, 
                              signal_threshold: float = 0.6) -> Dict[str, Any]:
        """
        Comprehensive backtesting analysis.
        Комплексный анализ бэктестинга.
        
        Args:
            model: Trained model
            test_data: Test dataset
            signal_threshold: Threshold for trading signals
            
        Returns:
            Dictionary with backtesting results
        """
        logger.info("Starting comprehensive backtesting...")
        
        # Get predictions
        predictions = model.predict(test_data)
        probabilities = model.predict_proba(test_data)
        
        # Prepare backtesting data
        backtest_data = test_data.copy()
        backtest_data['prediction'] = predictions
        
        if len(probabilities.columns) > 1:
            backtest_data['probability'] = probabilities.iloc[:, 1]
        else:
            backtest_data['probability'] = probabilities.iloc[:, 0]
        
        # Create trading signals
        backtest_data['signal'] = np.where(
            backtest_data['probability'] > signal_threshold, 1,  # Buy
            np.where(backtest_data['probability'] < (1 - signal_threshold), -1, 0)  # Sell/Hold
        )
        
        # Calculate returns
        backtest_data['price_return'] = backtest_data['Close'].pct_change()
        backtest_data['strategy_return'] = backtest_data['signal'].shift(1) * backtest_data['price_return']
        backtest_data['cumulative_return'] = (1 + backtest_data['strategy_return']).cumprod()
        backtest_data['portfolio_value'] = self.initial_capital * backtest_data['cumulative_return']
        
        # Calculate performance metrics
        results = self._calculate_performance_metrics(backtest_data)
        
        # Add trade analysis
        trade_analysis = self._analyze_trades(backtest_data)
        results.update(trade_analysis)
        
        logger.info(f"Backtesting completed. Total return: {results['total_return']:.2%}")
        
        return results
    
    def _calculate_performance_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive performance metrics."""
        
        # Basic returns
        total_return = data['cumulative_return'].iloc[-1] - 1
        annual_return = (1 + total_return) ** (252 / len(data)) - 1
        
        # Risk metrics
        returns = data['strategy_return'].dropna()
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        
        # Maximum drawdown
        cumulative = data['cumulative_return']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Profit factor
        winning_trades = returns[returns > 0]
        losing_trades = returns[returns < 0]
        
        profit_factor = (winning_trades.sum() / abs(losing_trades.sum()) 
                       if len(losing_trades) > 0 and losing_trades.sum() != 0 else float('inf'))
        
        # Win rate
        win_rate = len(winning_trades) / len(returns) if len(returns) > 0 else 0
        
        # Additional metrics
        avg_win = winning_trades.mean() if len(winning_trades) > 0 else 0
        avg_loss = losing_trades.mean() if len(losing_trades) > 0 else 0
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'profit_factor': profit_factor,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'total_trades': (data['signal'] != 0).sum(),
            'final_portfolio_value': data['portfolio_value'].iloc[-1]
        }
    
    def _analyze_trades(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze individual trades."""
        
        # Find trade entry and exit points
        signals = data['signal']
        trade_starts = signals[signals != 0].index
        trade_ends = trade_starts[1:] if len(trade_starts) > 1 else []
        
        trades = []
        for i, start in enumerate(trade_starts):
            if i < len(trade_ends):
                end = trade_ends[i]
                trade_return = data.loc[end, 'cumulative_return'] / data.loc[start, 'cumulative_return'] - 1
                trades.append({
                    'start': start,
                    'end': end,
                    'return': trade_return,
                    'duration': (end - start).days if hasattr(end - start, 'days') else 1
                })
        
        if not trades:
            return {'trade_analysis': 'No trades found'}
        
        trade_df = pd.DataFrame(trades)
        
        return {
            'total_trades': len(trades),
            'avg_trade_return': trade_df['return'].mean(),
            'avg_trade_duration': trade_df['duration'].mean(),
            'best_trade': trade_df['return'].max(),
            'worst_trade': trade_df['return'].min(),
            'profitable_trades': len(trade_df[trade_df['return'] > 0]),
            'losing_trades': len(trade_df[trade_df['return'] <= 0])
        }
    
    def walk_forward_analysis(self, model, data: pd.DataFrame, 
                            window_size: int = 1000, step_size: int = 100,
                            retrain_frequency: int = 500) -> Dict[str, Any]:
        """
        Walk Forward Analysis for model stability.
        Анализ скользящего окна для стабильности модели.
        
        Args:
            model: Base model
            data: Full dataset
            window_size: Size of training window
            step_size: Step size for moving window
            retrain_frequency: How often to retrain model
            
        Returns:
            Dictionary with walk forward results
        """
        logger.info(f"Starting Walk Forward Analysis: window={window_size}, step={step_size}")
        
        results = []
        last_retrain = 0
        current_model = model
        
        for i in range(window_size, len(data), step_size):
            logger.info(f"Processing window {i-window_size}:{i}")
            
            # Define windows
            train_window = data.iloc[i-window_size:i-step_size]
            test_window = data.iloc[i-step_size:i]
            
            if len(test_window) == 0:
                break
            
            # Retrain model if needed
            if i - last_retrain >= retrain_frequency:
                logger.info("Retraining model...")
                try:
                    current_model.train_models(train_window, "target", train_window.iloc[-100:])
                    last_retrain = i
                except Exception as e:
                    logger.warning(f"Retraining failed: {e}")
            
            # Test on current window
            try:
                predictions = current_model.predict(test_window)
                actual = test_window['target']
                
                # Calculate metrics
                accuracy = accuracy_score(actual, predictions)
                
                # Quick backtest on window
                window_results = self.comprehensive_backtesting(current_model, test_window)
                
                window_result = {
                    'window_start': i - window_size,
                    'window_end': i,
                    'test_start': i - step_size,
                    'test_end': i,
                    'accuracy': accuracy,
                    'total_return': window_results['total_return'],
                    'sharpe_ratio': window_results['sharpe_ratio'],
                    'max_drawdown': window_results['max_drawdown'],
                    'profit_factor': window_results['profit_factor']
                }
                
                results.append(window_result)
                logger.info(f"Window {i}: Accuracy={accuracy:.3f}, Return={window_results['total_return']:.2%}")
                
            except Exception as e:
                logger.error(f"Error processing window {i}: {e}")
                continue
        
        # Analyze results
        if not results:
            return {'error': 'No valid windows processed'}
        
        results_df = pd.DataFrame(results)
        
        summary = {
            'total_windows': len(results),
            'mean_accuracy': results_df['accuracy'].mean(),
            'std_accuracy': results_df['accuracy'].std(),
            'mean_return': results_df['total_return'].mean(),
            'std_return': results_df['total_return'].std(),
            'mean_sharpe': results_df['sharpe_ratio'].mean(),
            'stability_score': 1 - results_df['accuracy'].std(),  # Lower std = more stable
            'consistency_score': (results_df['total_return'] > 0).mean(),  # % of profitable windows
            'results': results
        }
        
        logger.info(f"Walk Forward completed: {summary['total_windows']} windows, "
                   f"stability={summary['stability_score']:.3f}")
        
        return summary
    
    def monte_carlo_simulation(self, model, data: pd.DataFrame, 
                             n_simulations: int = 1000, sample_size: int = 500) -> Dict[str, Any]:
        """
        Monte Carlo simulation for robustness testing.
        Симуляция Монте-Карло для тестирования робастности.
        
        Args:
            model: Trained model
            data: Dataset for simulation
            n_simulations: Number of simulations
            sample_size: Size of each sample
            
        Returns:
            Dictionary with Monte Carlo results
        """
        logger.info(f"Starting Monte Carlo simulation: {n_simulations} simulations, sample size {sample_size}")
        
        simulation_results = []
        
        for i in range(n_simulations):
            if i % 100 == 0:
                logger.info(f"Simulation progress: {i}/{n_simulations}")
            
            try:
                # Random sample with replacement
                sample_data = data.sample(n=min(sample_size, len(data)), replace=True)
                
                # Get predictions
                predictions = model.predict(sample_data)
                actual = sample_data['target']
                
                # Calculate basic metrics
                accuracy = accuracy_score(actual, predictions)
                
                # Quick performance analysis
                sample_data_copy = sample_data.copy()
                sample_data_copy['prediction'] = predictions
                
                # Simple strategy simulation
                sample_data_copy['signal'] = np.where(predictions == 1, 1, -1)
                sample_data_copy['return'] = sample_data_copy['Close'].pct_change()
                sample_data_copy['strategy_return'] = sample_data_copy['signal'].shift(1) * sample_data_copy['return']
                
                total_return = sample_data_copy['strategy_return'].sum()
                sharpe = (sample_data_copy['strategy_return'].mean() / 
                         sample_data_copy['strategy_return'].std() * np.sqrt(252) 
                         if sample_data_copy['strategy_return'].std() > 0 else 0)
                
                simulation_results.append({
                    'accuracy': accuracy,
                    'total_return': total_return,
                    'sharpe_ratio': sharpe
                })
                
            except Exception as e:
                logger.warning(f"Simulation {i} failed: {e}")
                continue
        
        if not simulation_results:
            return {'error': 'No successful simulations'}
        
        # Analyze results
        results_df = pd.DataFrame(simulation_results)
        
        summary = {
            'total_simulations': len(simulation_results),
            'mean_accuracy': results_df['accuracy'].mean(),
            'std_accuracy': results_df['accuracy'].std(),
            'min_accuracy': results_df['accuracy'].min(),
            'max_accuracy': results_df['accuracy'].max(),
            'percentile_5': results_df['accuracy'].quantile(0.05),
            'percentile_95': results_df['accuracy'].quantile(0.95),
            'mean_return': results_df['total_return'].mean(),
            'mean_sharpe': results_df['sharpe_ratio'].mean(),
            'robustness_score': (results_df['accuracy'] > 0.5).mean(),  # % of simulations with accuracy > 50%
            'consistency_score': (results_df['total_return'] > 0).mean(),  # % of profitable simulations
            'results': simulation_results
        }
        
        logger.info(f"Monte Carlo completed: {summary['total_simulations']} simulations, "
                   f"robustness={summary['robustness_score']:.3f}")
        
        return summary
    
    def create_performance_report(self, backtest_results: Dict, wf_results: Dict, mc_results: Dict) -> str:
        """
        Create comprehensive performance report.
        Создать комплексный отчет о производительности.
        
        Args:
            backtest_results: Backtesting results
            wf_results: Walk Forward results
            mc_results: Monte Carlo results
            
        Returns:
            Formatted report string
        """
        
        report = f"""
# 📊 COMPREHENSIVE TRADING MODEL PERFORMANCE REPORT
# Отчет о производительности торговой модели

## 🎯 Executive Summary / Исполнительное резюме

**Model Performance Overview:**
- Backtest Total Return: {backtest_results.get('total_return', 0):.2%}
- Walk Forward Stability: {wf_results.get('stability_score', 0):.3f}
- Monte Carlo Robustness: {mc_results.get('robustness_score', 0):.3f}

## 📈 Backtesting Results / Результаты бэктестинга

**Performance Metrics:**
- Total Return: {backtest_results.get('total_return', 0):.2%}
- Annual Return: {backtest_results.get('annual_return', 0):.2%}
- Sharpe Ratio: {backtest_results.get('sharpe_ratio', 0):.3f}
- Maximum Drawdown: {backtest_results.get('max_drawdown', 0):.2%}
- Profit Factor: {backtest_results.get('profit_factor', 0):.2f}
- Win Rate: {backtest_results.get('win_rate', 0):.2%}

**Trade Analysis:**
- Total Trades: {backtest_results.get('total_trades', 0)}
- Average Trade Return: {backtest_results.get('avg_trade_return', 0):.2%}
- Best Trade: {backtest_results.get('best_trade', 0):.2%}
- Worst Trade: {backtest_results.get('worst_trade', 0):.2%}

## 🚶 Walk Forward Analysis / Анализ скользящего окна

**Stability Metrics:**
- Total Windows: {wf_results.get('total_windows', 0)}
- Mean Accuracy: {wf_results.get('mean_accuracy', 0):.3f} ± {wf_results.get('std_accuracy', 0):.3f}
- Mean Return: {wf_results.get('mean_return', 0):.2%} ± {wf_results.get('std_return', 0):.2%}
- Stability Score: {wf_results.get('stability_score', 0):.3f}
- Consistency Score: {wf_results.get('consistency_score', 0):.3f}

## 🎲 Monte Carlo Simulation / Симуляция Монте-Карло

**Robustness Metrics:**
- Total Simulations: {mc_results.get('total_simulations', 0)}
- Mean Accuracy: {mc_results.get('mean_accuracy', 0):.3f} ± {mc_results.get('std_accuracy', 0):.3f}
- Accuracy Range: {mc_results.get('min_accuracy', 0):.3f} - {mc_results.get('max_accuracy', 0):.3f}
- 95% Confidence Interval: {mc_results.get('percentile_5', 0):.3f} - {mc_results.get('percentile_95', 0):.3f}
- Robustness Score: {mc_results.get('robustness_score', 0):.3f}
- Consistency Score: {mc_results.get('consistency_score', 0):.3f}

## 🎯 Overall Assessment / Общая оценка

**Model Quality Indicators:**
- ✅ High Performance: Sharpe > 1.0 and Return > 10%
- ✅ Stable: Walk Forward stability > 0.7
- ✅ Robust: Monte Carlo robustness > 0.6
- ✅ Consistent: High consistency scores across all tests

**Recommendations:**
1. {'✅ Model ready for production' if all([
    backtest_results.get('sharpe_ratio', 0) > 1.0,
    backtest_results.get('total_return', 0) > 0.1,
    wf_results.get('stability_score', 0) > 0.7,
    mc_results.get('robustness_score', 0) > 0.6
]) else '⚠️ Model needs improvement'}
2. {'Monitor for drift and retrain regularly' if wf_results.get('stability_score', 0) > 0.7 else 'Consider additional feature engineering'}
3. {'Use conservative position sizing' if backtest_results.get('max_drawdown', 0) < -0.2 else 'Risk management is adequate'}

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
