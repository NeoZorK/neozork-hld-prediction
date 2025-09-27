# -*- coding: utf-8 -*-
"""
AutoGluon metrics utility.

This module provides metrics and value score analysis for AutoGluon models.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class ValueScoreAnalyzer:
    """Value score analyzer for trading strategies."""
    
    def __init__(self):
        """Initialize value score analyzer."""
        pass
    
    def analyze_predictions(self, y_true: pd.Series, y_pred: pd.Series) -> Dict[str, float]:
        """
        Analyze predictions for trading value scores.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Value scores dictionary
        """
        logger.info("Analyzing predictions for value scores...")
        
        # Remove NaN values
        mask = ~(y_true.isna() | y_pred.isna())
        y_true_clean = y_true[mask]
        y_pred_clean = y_pred[mask]
        
        if len(y_true_clean) == 0:
            logger.warning("No valid data for value score analysis")
            return {}
        
        # Calculate value scores
        value_scores = {
            'profit_factor': self._calculate_profit_factor(y_true_clean, y_pred_clean),
            'sharpe_ratio': self._calculate_sharpe_ratio(y_true_clean, y_pred_clean),
            'max_drawdown': self._calculate_max_drawdown(y_true_clean, y_pred_clean),
            'win_rate': self._calculate_win_rate(y_true_clean, y_pred_clean),
            'avg_trade_duration': self._calculate_avg_trade_duration(y_true_clean, y_pred_clean),
            'total_return': self._calculate_total_return(y_true_clean, y_pred_clean),
            'volatility': self._calculate_volatility(y_true_clean, y_pred_clean)
        }
        
        logger.info("Value score analysis completed")
        return value_scores
    
    def _calculate_profit_factor(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate profit factor."""
        try:
            # Calculate returns
            returns = y_true.diff()
            returns = returns.dropna()
            
            # Separate profits and losses
            profits = returns[returns > 0].sum()
            losses = abs(returns[returns < 0].sum())
            
            if losses == 0:
                return float('inf') if profits > 0 else 0.0
            
            return profits / losses
            
        except Exception as e:
            logger.warning(f"Could not calculate profit factor: {e}")
            return 0.0
    
    def _calculate_sharpe_ratio(self, y_true: pd.Series, y_pred: pd.Series, 
                               risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio."""
        try:
            # Calculate returns
            returns = y_true.pct_change().dropna()
            
            if len(returns) == 0 or returns.std() == 0:
                return 0.0
            
            # Annualize (assuming daily data)
            annualized_return = returns.mean() * 252
            annualized_volatility = returns.std() * np.sqrt(252)
            
            return (annualized_return - risk_free_rate) / annualized_volatility
            
        except Exception as e:
            logger.warning(f"Could not calculate Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate maximum drawdown."""
        try:
            # Calculate cumulative returns
            cumulative_returns = (1 + y_true.pct_change()).cumprod()
            
            # Calculate running maximum
            running_max = cumulative_returns.expanding().max()
            
            # Calculate drawdown
            drawdown = (cumulative_returns - running_max) / running_max
            
            return abs(drawdown.min())
            
        except Exception as e:
            logger.warning(f"Could not calculate max drawdown: {e}")
            return 0.0
    
    def _calculate_win_rate(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate win rate."""
        try:
            # Calculate returns
            returns = y_true.pct_change().dropna()
            
            if len(returns) == 0:
                return 0.0
            
            # Count winning trades
            winning_trades = (returns > 0).sum()
            total_trades = len(returns)
            
            return winning_trades / total_trades
            
        except Exception as e:
            logger.warning(f"Could not calculate win rate: {e}")
            return 0.0
    
    def _calculate_avg_trade_duration(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate average trade duration."""
        try:
            # This is a simplified calculation
            # In practice, you would need trade entry/exit information
            return 1.0  # Placeholder
            
        except Exception as e:
            logger.warning(f"Could not calculate avg trade duration: {e}")
            return 0.0
    
    def _calculate_total_return(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate total return."""
        try:
            # Calculate cumulative return
            cumulative_return = (1 + y_true.pct_change()).cumprod()
            
            if len(cumulative_return) == 0:
                return 0.0
            
            return (cumulative_return.iloc[-1] - 1) * 100  # As percentage
            
        except Exception as e:
            logger.warning(f"Could not calculate total return: {e}")
            return 0.0
    
    def _calculate_volatility(self, y_true: pd.Series, y_pred: pd.Series) -> float:
        """Calculate volatility."""
        try:
            # Calculate returns
            returns = y_true.pct_change().dropna()
            
            if len(returns) == 0:
                return 0.0
            
            # Annualized volatility
            return returns.std() * np.sqrt(252) * 100  # As percentage
            
        except Exception as e:
            logger.warning(f"Could not calculate volatility: {e}")
            return 0.0
    
    def get_robustness_score(self, value_scores: Dict[str, float]) -> float:
        """
        Calculate overall robustness score.
        
        Args:
            value_scores: Value scores dictionary
            
        Returns:
            Robustness score (0-1)
        """
        try:
            # Normalize scores to 0-1 range
            normalized_scores = {}
            
            # Profit factor (0-5 range)
            pf = min(value_scores.get('profit_factor', 0), 5)
            normalized_scores['profit_factor'] = pf / 5
            
            # Sharpe ratio (-2 to 3 range)
            sr = max(min(value_scores.get('sharpe_ratio', 0), 3), -2)
            normalized_scores['sharpe_ratio'] = (sr + 2) / 5
            
            # Max drawdown (0-1 range, inverted)
            md = min(value_scores.get('max_drawdown', 1), 1)
            normalized_scores['max_drawdown'] = 1 - md
            
            # Win rate (0-1 range)
            wr = min(value_scores.get('win_rate', 0), 1)
            normalized_scores['win_rate'] = wr
            
            # Calculate weighted average
            weights = {
                'profit_factor': 0.25,
                'sharpe_ratio': 0.25,
                'max_drawdown': 0.25,
                'win_rate': 0.25
            }
            
            robustness_score = sum(
                normalized_scores.get(metric, 0) * weight
                for metric, weight in weights.items()
            )
            
            return min(max(robustness_score, 0), 1)
            
        except Exception as e:
            logger.warning(f"Could not calculate robustness score: {e}")
            return 0.0
    
    def generate_report(self, value_scores: Dict[str, float]) -> str:
        """
        Generate value score report.
        
        Args:
            value_scores: Value scores dictionary
            
        Returns:
            Report string
        """
        report = "=== Value Score Analysis Report ===\n\n"
        
        # Individual scores
        report += "Individual Metrics:\n"
        report += f"  Profit Factor: {value_scores.get('profit_factor', 0):.3f}\n"
        report += f"  Sharpe Ratio: {value_scores.get('sharpe_ratio', 0):.3f}\n"
        report += f"  Max Drawdown: {value_scores.get('max_drawdown', 0):.3f}\n"
        report += f"  Win Rate: {value_scores.get('win_rate', 0):.3f}\n"
        report += f"  Total Return: {value_scores.get('total_return', 0):.2f}%\n"
        report += f"  Volatility: {value_scores.get('volatility', 0):.2f}%\n\n"
        
        # Robustness score
        robustness = self.get_robustness_score(value_scores)
        report += f"Overall Robustness Score: {robustness:.3f}\n\n"
        
        # Interpretation
        if robustness >= 0.8:
            report += "Interpretation: EXCELLENT - Model shows strong robustness\n"
        elif robustness >= 0.6:
            report += "Interpretation: GOOD - Model shows good robustness\n"
        elif robustness >= 0.4:
            report += "Interpretation: FAIR - Model shows moderate robustness\n"
        else:
            report += "Interpretation: POOR - Model needs improvement\n"
        
        return report
