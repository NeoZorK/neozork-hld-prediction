print('DEBUG: universal_trading_metrics.py imported')
# -*- coding: utf-8 -*-
# src/calculation/universal_trading_metrics.py

"""
Universal Trading Metrics Module
Calculates and displays comprehensive trading metrics for any rule type strictly in console output.
"""

import pandas as pd
print('DEBUG: pandas imported')
import numpy as np
print('DEBUG: numpy imported')
from typing import Dict, Union, Optional
print('DEBUG: typing imported')
from datetime import datetime
print('DEBUG: datetime imported')
from src.common import logger
print('DEBUG: logger imported')
from src.common.constants import BUY, SELL, NOTRADE
print('DEBUG: constants imported')
from src.calculation.trading_metrics import calculate_trading_metrics
print('DEBUG: trading_metrics imported')


class UniversalTradingMetrics:
    """
    Universal trading metrics calculator that works with any rule type.
    Displays metrics strictly in console output.
    """
    
    def __init__(self, lot_size: float = 1.0, risk_reward_ratio: float = 2.0, 
                 fee_per_trade: float = 0.07):
        """
        Initialize the universal trading metrics calculator.
        
        Args:
            lot_size (float): Position size (default: 1.0)
            risk_reward_ratio (float): Risk to reward ratio (default: 2.0)
            fee_per_trade (float): Fee per trade in percentage (default: 0.07)
        """
        self.lot_size = lot_size
        self.risk_reward_ratio = risk_reward_ratio
        self.fee_per_trade = fee_per_trade
    
    def calculate_and_display_metrics(self, df: pd.DataFrame, rule: Union[str, object], 
                                    price_col: str = 'Close', signal_col: str = 'Direction',
                                    volume_col: Optional[str] = 'Volume') -> Dict[str, float]:
        print('DEBUG: UniversalTradingMetrics.calculate_and_display_metrics called')
        try:
            # Validate input data
            if df is None or df.empty:
                self._display_error("DataFrame is None or empty")
                return {}
            
            if signal_col not in df.columns:
                self._display_error(f"Signal column '{signal_col}' not found in data")
                return {}
            
            # Get rule name
            rule_name = self._get_rule_name(rule)
            
            # Calculate metrics
            metrics = calculate_trading_metrics(
                df, 
                price_col=price_col, 
                signal_col=signal_col, 
                volume_col=volume_col,
                lot_size=self.lot_size,
                risk_reward_ratio=self.risk_reward_ratio,
                fee_per_trade=self.fee_per_trade
            )
            
            # Display metrics in console
            self._display_metrics(metrics, rule_name, df)
            
            return metrics
            
        except Exception as e:
            logger.print_error(f"Error calculating universal trading metrics: {e}")
            self._display_error(f"Metrics calculation failed: {e}")
            return {}
    
    def _get_rule_name(self, rule: Union[str, object]) -> str:
        """Extract rule name from rule object or string."""
        if isinstance(rule, str):
            return rule
        elif hasattr(rule, 'name'):
            return rule.name
        elif hasattr(rule, '__class__'):
            return rule.__class__.__name__
        else:
            return str(rule)
    
    def _display_metrics(self, metrics: Dict[str, float], rule_name: str, df: pd.DataFrame) -> None:
        """Display comprehensive trading metrics in console."""
        try:
            # Header
            print(f"\n{'='*80}")
            print(f"{'UNIVERSAL TRADING METRICS ANALYSIS':^80}")
            print(f"{'Rule: ' + rule_name.upper():^80}")
            print(f"{'Generated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^80}")
            print(f"{'='*80}")
            
            # Basic statistics
            self._display_basic_statistics(df)
            
            # Core metrics
            self._display_core_metrics(metrics)
            
            # Strategy metrics
            self._display_strategy_metrics(metrics)
            
            # Risk metrics
            self._display_risk_metrics(metrics)
            
            # Advanced metrics
            self._display_advanced_metrics(metrics)
            
            # Monte Carlo metrics
            self._display_monte_carlo_metrics(metrics)
            
            # Volume metrics (if available)
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                self._display_volume_metrics(metrics)
            
            # Performance summary
            self._display_performance_summary(metrics)
            
            # Footer
            print(f"\n{'='*80}")
            print(f"{'END OF TRADING METRICS ANALYSIS':^80}")
            print(f"{'='*80}")
            
        except Exception as e:
            logger.print_error(f"Error displaying metrics: {e}")
    
    def _display_basic_statistics(self, df: pd.DataFrame) -> None:
        """Display basic data statistics."""
        print(f"\n📊 BASIC DATA STATISTICS:")
        print(f"{'─' * 50}")
        
        # Data info
        print(f"   📈 Total Rows:        {len(df):,}")
        print(f"   📋 Total Columns:     {len(df.columns)}")
        print(f"   💾 Memory Usage:      {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # Date range
        if 'datetime' in df.columns:
            date_col = 'datetime'
        elif 'DateTime' in df.columns:
            date_col = 'DateTime'
        elif 'Date' in df.columns:
            date_col = 'Date'
        else:
            date_col = None
        
        if date_col and date_col in df.columns:
            try:
                start_date = pd.to_datetime(df[date_col].min()).strftime('%Y-%m-%d')
                end_date = pd.to_datetime(df[date_col].max()).strftime('%Y-%m-%d')
                print(f"   📅 Date Range:        {start_date} to {end_date}")
            except:
                pass
        
        # Price statistics
        if 'Close' in df.columns:
            close_prices = df['Close'].dropna()
            if len(close_prices) > 0:
                print(f"   💰 Price Range:       {close_prices.min():.5f} - {close_prices.max():.5f}")
                print(f"   📊 Average Price:     {close_prices.mean():.5f}")
                print(f"   📈 Price Volatility:  {close_prices.std():.5f}")
        
        # Signal statistics
        if 'Direction' in df.columns:
            signals = df['Direction'].value_counts()
            print(f"\n🎯 SIGNAL STATISTICS:")
            print(f"   Buy Signals:       {signals.get(BUY, 0)}")
            print(f"   Sell Signals:      {signals.get(SELL, 0)}")
            print(f"   No Trade Signals:  {signals.get(NOTRADE, 0)}")
            print(f"   Total Signals:     {len(df[df['Direction'] != NOTRADE])}")
    
    def _display_core_metrics(self, metrics: Dict[str, float]) -> None:
        """Display core trading performance metrics."""
        print(f"\n💎 CORE TRADING METRICS:")
        print(f"{'─' * 50}")
        
        # Win ratio with color coding
        win_ratio = metrics.get('win_ratio', 0)
        win_color = self._get_metric_color(win_ratio, 50, 70)
        print(f"   🎯 Win Ratio:        {win_ratio:.1f}% {win_color}")
        
        # Risk/Reward ratio
        rr_ratio = metrics.get('risk_reward_ratio', 0)
        rr_color = self._get_metric_color(rr_ratio, 1.5, 2.0)
        print(f"   ⚖️  Risk/Reward:      {rr_ratio:.2f} {rr_color}")
        
        # Profit factor
        profit_factor = metrics.get('profit_factor', 0)
        pf_color = self._get_metric_color(profit_factor, 1.5, 2.0)
        print(f"   💰 Profit Factor:    {profit_factor:.2f} {pf_color}")
        
        # Total return
        total_return = metrics.get('total_return', 0)
        tr_color = self._get_metric_color(total_return, 10, 20)
        print(f"   📈 Total Return:     {total_return:.1f}% {tr_color}")
        
        # Net return (with fees)
        net_return = metrics.get('net_return', 0)
        nr_color = self._get_metric_color(net_return, 10, 20)
        print(f"   💵 Net Return:       {net_return:.2f}% {nr_color}")
        
        # Trade counts
        buy_count = metrics.get('buy_count', 0)
        sell_count = metrics.get('sell_count', 0)
        total_trades = metrics.get('total_trades', 0)
        print(f"   🔄 Total Trades:     {total_trades} (Buy: {buy_count}, Sell: {sell_count})")
    
    def _display_strategy_metrics(self, metrics: Dict[str, float]) -> None:
        """Display strategy-specific metrics."""
        print(f"\n🎯 STRATEGY METRICS:")
        print(f"{'─' * 50}")
        
        # Position sizing
        position_size = metrics.get('position_size', 0)
        optimal_position = metrics.get('optimal_position_size', 0)
        print(f"   📏 Position Size:     {position_size:.2f}")
        print(f"   🎯 Optimal Position:  {optimal_position:.2f}")
        
        # Kelly Criterion
        kelly_fraction = metrics.get('kelly_fraction', 0)
        kelly_color = self._get_metric_color(kelly_fraction, 0.1, 0.3)
        print(f"   🧮 Kelly Fraction:    {kelly_fraction:.3f} {kelly_color}")
        
        # Strategy efficiency
        strategy_efficiency = metrics.get('strategy_efficiency', 0)
        eff_color = self._get_metric_color(strategy_efficiency, 80, 90)
        print(f"   ⚡ Efficiency:        {strategy_efficiency:.1f}% {eff_color}")
        
        # Strategy sustainability
        sustainability = metrics.get('strategy_sustainability', 0)
        sus_color = self._get_metric_color(sustainability, 60, 80)
        print(f"   🌱 Sustainability:    {sustainability:.1f}% {sus_color}")
        
        # Break-even analysis
        break_even = metrics.get('break_even_win_rate', 0)
        print(f"   ⚖️  Break-even Win:    {break_even:.1f}%")
        
        # Minimum win rate for profit
        min_win_rate = metrics.get('min_win_rate_for_profit', 0)
        print(f"   📊 Min Win Rate:      {min_win_rate:.1f}%")
    
    def _display_risk_metrics(self, metrics: Dict[str, float]) -> None:
        """Display risk management metrics."""
        print(f"\n⚠️  RISK MANAGEMENT METRICS:")
        print(f"{'─' * 50}")
        
        # Maximum drawdown
        max_drawdown = metrics.get('max_drawdown', 0)
        dd_color = self._get_metric_color(max_drawdown, 10, 20, reverse=True)
        print(f"   📉 Max Drawdown:      {max_drawdown:.1f}% {dd_color}")
        
        # Volatility
        volatility = metrics.get('volatility', 0)
        vol_color = self._get_metric_color(volatility, 10, 20, reverse=True)
        print(f"   📊 Volatility:        {volatility:.1f}% {vol_color}")
        
        # Sharpe ratio
        sharpe_ratio = metrics.get('sharpe_ratio', 0)
        sharpe_color = self._get_metric_color(sharpe_ratio, 1.0, 2.0)
        print(f"   📈 Sharpe Ratio:      {sharpe_ratio:.2f} {sharpe_color}")
        
        # Sortino ratio
        sortino_ratio = metrics.get('sortino_ratio', 0)
        sortino_color = self._get_metric_color(sortino_ratio, 1.0, 2.0)
        print(f"   📊 Sortino Ratio:     {sortino_ratio:.2f} {sortino_color}")
        
        # Calmar ratio
        calmar_ratio = metrics.get('calmar_ratio', 0)
        calmar_color = self._get_metric_color(calmar_ratio, 1.0, 2.0)
        print(f"   📊 Calmar Ratio:      {calmar_ratio:.2f} {calmar_color}")
        
        # Risk of ruin
        risk_of_ruin = metrics.get('risk_of_ruin', 0)
        ruin_color = self._get_metric_color(risk_of_ruin, 5, 10, reverse=True)
        print(f"   💀 Risk of Ruin:      {risk_of_ruin:.1f}% {ruin_color}")
    
    def _display_advanced_metrics(self, metrics: Dict[str, float]) -> None:
        """Display advanced ML and probability metrics."""
        print(f"\n🧠 ADVANCED METRICS:")
        print(f"{'─' * 50}")
        
        # Signal quality metrics
        signal_accuracy = metrics.get('signal_accuracy', 0)
        acc_color = self._get_metric_color(signal_accuracy, 60, 80)
        print(f"   🎯 Signal Accuracy:   {signal_accuracy:.1f}% {acc_color}")
        
        signal_timing = metrics.get('signal_timing_score', 0)
        timing_color = self._get_metric_color(signal_timing, 5, 10)
        print(f"   ⏰ Signal Timing:     {signal_timing:.2f}% {timing_color}")
        
        signal_stability = metrics.get('signal_stability', 0)
        stab_color = self._get_metric_color(signal_stability, 0.7, 0.9)
        print(f"   🔒 Signal Stability:  {signal_stability:.3f} {stab_color}")
        
        # Pattern recognition
        pattern_consistency = metrics.get('pattern_consistency', 0)
        pattern_color = self._get_metric_color(pattern_consistency, 60, 80)
        print(f"   🔄 Pattern Consistency: {pattern_consistency:.1f}% {pattern_color}")
        
        signal_clustering = metrics.get('signal_clustering', 0)
        cluster_color = self._get_metric_color(signal_clustering, 60, 80)
        print(f"   📊 Signal Clustering: {signal_clustering:.1f}% {cluster_color}")
        
        # Correlation metrics
        momentum_corr = metrics.get('momentum_correlation', 0)
        print(f"   📈 Momentum Correlation: {momentum_corr:.3f}")
        
        volatility_corr = metrics.get('volatility_correlation', 0)
        print(f"   📊 Volatility Correlation: {volatility_corr:.3f}")
        
        trend_corr = metrics.get('trend_correlation', 0)
        print(f"   📈 Trend Correlation: {trend_corr:.3f}")
    
    def _display_monte_carlo_metrics(self, metrics: Dict[str, float]) -> None:
        """Display Monte Carlo simulation metrics."""
        print(f"\n🎲 MONTE CARLO SIMULATION METRICS:")
        print(f"{'─' * 50}")
        
        # Expected return
        mc_expected = metrics.get('mc_expected_return', 0)
        exp_color = self._get_metric_color(mc_expected, 10, 20)
        print(f"   📈 Expected Return:   {mc_expected:.1f}% {exp_color}")
        
        # Standard deviation
        mc_std = metrics.get('mc_std_deviation', 0)
        std_color = self._get_metric_color(mc_std, 10, 20, reverse=True)
        print(f"   📊 Std Deviation:     {mc_std:.1f}% {std_color}")
        
        # Value at Risk
        mc_var = metrics.get('mc_var_95', 0)
        var_color = self._get_metric_color(mc_var, -10, -5, reverse=True)
        print(f"   ⚠️  VaR (95%):         {mc_var:.1f}% {var_color}")
        
        # Conditional VaR
        mc_cvar = metrics.get('mc_cvar_95', 0)
        cvar_color = self._get_metric_color(mc_cvar, -15, -10, reverse=True)
        print(f"   ⚠️  CVaR (95%):        {mc_cvar:.1f}% {cvar_color}")
        
        # Probability of profit
        mc_prob_profit = metrics.get('mc_probability_profit', 0)
        prob_color = self._get_metric_color(mc_prob_profit, 60, 80)
        print(f"   📊 Profit Probability: {mc_prob_profit:.1f}% {prob_color}")
        
        # Strategy robustness
        robustness = metrics.get('strategy_robustness', 0)
        rob_color = self._get_metric_color(robustness, 60, 80)
        print(f"   🛡️  Strategy Robustness: {robustness:.1f}% {rob_color}")
        
        # Max gain/loss
        mc_max_gain = metrics.get('mc_max_gain', 0)
        mc_max_loss = metrics.get('mc_max_loss', 0)
        print(f"   📈 Max Gain:          {mc_max_gain:.1f}%")
        print(f"   📉 Max Loss:          {mc_max_loss:.1f}%")
    
    def _display_volume_metrics(self, metrics: Dict[str, float]) -> None:
        """Display volume-weighted metrics."""
        print(f"\n📊 VOLUME-WEIGHTED METRICS:")
        print(f"{'─' * 50}")
        
        volume_return = metrics.get('volume_weighted_return', 0)
        vol_ret_color = self._get_metric_color(volume_return, 10, 20)
        print(f"   📈 Volume Return:     {volume_return:.2f}% {vol_ret_color}")
        
        volume_win_ratio = metrics.get('volume_win_ratio', 0)
        vol_win_color = self._get_metric_color(volume_win_ratio, 60, 80)
        print(f"   📊 Volume Win Ratio:  {volume_win_ratio:.1f}% {vol_win_color}")
    
    def _display_performance_summary(self, metrics: Dict[str, float]) -> None:
        """Display performance summary and recommendations."""
        print(f"\n📋 PERFORMANCE SUMMARY:")
        print(f"{'─' * 50}")
        
        # Overall performance score
        performance_score = self._calculate_performance_score(metrics)
        score_color = self._get_metric_color(performance_score, 60, 80)
        print(f"   🎯 Overall Score:     {performance_score:.1f}/100 {score_color}")
        
        # Key strengths
        strengths = self._identify_strengths(metrics)
        if strengths:
            print(f"   ✅ Key Strengths:")
            for strength in strengths[:3]:  # Top 3 strengths
                print(f"      • {strength}")
        
        # Key weaknesses
        weaknesses = self._identify_weaknesses(metrics)
        if weaknesses:
            print(f"   ❌ Key Weaknesses:")
            for weakness in weaknesses[:3]:  # Top 3 weaknesses
                print(f"      • {weakness}")
        
        # Recommendations
        recommendations = self._generate_recommendations(metrics)
        if recommendations:
            print(f"   💡 Recommendations:")
            for rec in recommendations[:3]:  # Top 3 recommendations
                print(f"      • {rec}")
    
    def _get_metric_color(self, value: float, low_threshold: float, high_threshold: float, 
                         reverse: bool = False) -> str:
        """Get color coding for metric values."""
        if reverse:
            if value <= low_threshold:
                return "🟢"  # Green for good (low values)
            elif value <= high_threshold:
                return "🟡"  # Yellow for moderate
            else:
                return "🔴"  # Red for bad (high values)
        else:
            if value >= high_threshold:
                return "🟢"  # Green for good (high values)
            elif value >= low_threshold:
                return "🟡"  # Yellow for moderate
            else:
                return "🔴"  # Red for bad (low values)
    
    def _calculate_performance_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall performance score (0-100)."""
        try:
            score = 0
            max_score = 0
            
            # Core metrics (40% weight)
            core_metrics = {
                'win_ratio': (50, 70, 20),
                'profit_factor': (1.5, 2.0, 10),
                'sharpe_ratio': (1.0, 2.0, 10)
            }
            
            for metric, (low, high, weight) in core_metrics.items():
                value = metrics.get(metric, 0)
                if value >= high:
                    score += weight
                elif value >= low:
                    score += weight * 0.5
                max_score += weight
            
            # Risk metrics (30% weight)
            risk_metrics = {
                'max_drawdown': (10, 20, 15, True),  # Reverse scoring
                'volatility': (10, 20, 15, True)     # Reverse scoring
            }
            
            for metric, (low, high, weight, reverse) in risk_metrics.items():
                value = metrics.get(metric, 0)
                if reverse:
                    if value <= low:
                        score += weight
                    elif value <= high:
                        score += weight * 0.5
                else:
                    if value >= high:
                        score += weight
                    elif value >= low:
                        score += weight * 0.5
                max_score += weight
            
            # Strategy metrics (30% weight)
            strategy_metrics = {
                'strategy_efficiency': (80, 90, 15),
                'strategy_sustainability': (60, 80, 15)
            }
            
            for metric, (low, high, weight) in strategy_metrics.items():
                value = metrics.get(metric, 0)
                if value >= high:
                    score += weight
                elif value >= low:
                    score += weight * 0.5
                max_score += weight
            
            return (score / max_score) * 100 if max_score > 0 else 0
            
        except Exception as e:
            logger.print_debug(f"Error calculating performance score: {e}")
            return 0
    
    def _identify_strengths(self, metrics: Dict[str, float]) -> list:
        """Identify key strengths of the strategy."""
        strengths = []
        
        win_ratio = metrics.get('win_ratio')
        if win_ratio is not None and win_ratio >= 70:
            strengths.append("High win ratio indicates consistent profitability")
        
        profit_factor = metrics.get('profit_factor')
        if profit_factor is not None and profit_factor >= 2.0:
            strengths.append("Strong profit factor shows good risk management")
        
        sharpe_ratio = metrics.get('sharpe_ratio')
        if sharpe_ratio is not None and sharpe_ratio >= 2.0:
            strengths.append("Excellent risk-adjusted returns")
        
        max_drawdown = metrics.get('max_drawdown')
        if max_drawdown is not None and max_drawdown <= 10:
            strengths.append("Low maximum drawdown indicates good risk control")
        
        strategy_efficiency = metrics.get('strategy_efficiency')
        if strategy_efficiency is not None and strategy_efficiency >= 90:
            strengths.append("High strategy efficiency with minimal costs")
        
        return strengths
    
    def _identify_weaknesses(self, metrics: Dict[str, float]) -> list:
        """Identify key weaknesses of the strategy."""
        weaknesses = []
        
        win_ratio = metrics.get('win_ratio')
        if win_ratio is not None and win_ratio < 50:
            weaknesses.append("Low win ratio suggests inconsistent performance")
        
        profit_factor = metrics.get('profit_factor')
        if profit_factor is not None and profit_factor < 1.5:
            weaknesses.append("Weak profit factor indicates poor risk management")
        
        max_drawdown = metrics.get('max_drawdown')
        if max_drawdown is not None and max_drawdown > 20:
            weaknesses.append("High maximum drawdown poses significant risk")
        
        volatility = metrics.get('volatility')
        if volatility is not None and volatility > 20:
            weaknesses.append("High volatility may indicate unstable performance")
        
        strategy_efficiency = metrics.get('strategy_efficiency')
        if strategy_efficiency is not None and strategy_efficiency < 70:
            weaknesses.append("Low efficiency suggests high trading costs")
        
        return weaknesses
    
    def _generate_recommendations(self, metrics: Dict[str, float]) -> list:
        """Generate actionable recommendations."""
        recommendations = []
        
        win_ratio = metrics.get('win_ratio')
        if win_ratio is not None and win_ratio < 50:
            recommendations.append("Consider improving entry/exit criteria to increase win rate")
        
        profit_factor = metrics.get('profit_factor')
        if profit_factor is not None and profit_factor < 1.5:
            recommendations.append("Review risk management to improve profit factor")
        
        max_drawdown = metrics.get('max_drawdown')
        if max_drawdown is not None and max_drawdown > 20:
            recommendations.append("Implement stricter stop-losses to reduce drawdown")
        
        strategy_efficiency = metrics.get('strategy_efficiency')
        if strategy_efficiency is not None and strategy_efficiency < 80:
            recommendations.append("Optimize position sizing and reduce trading frequency")
        
        kelly_fraction = metrics.get('kelly_fraction')
        if kelly_fraction is not None and kelly_fraction < 0.1:
            recommendations.append("Consider reducing position sizes based on Kelly criterion")
        
        return recommendations
    
    def _display_error(self, message: str) -> None:
        """Display error message."""
        print(f"\n❌ ERROR: {message}")
        print(f"{'─' * 50}")


def display_universal_trading_metrics(df: pd.DataFrame, rule: Union[str, object], 
                                    lot_size: float = 1.0, risk_reward_ratio: float = 2.0, 
                                    fee_per_trade: float = 0.07) -> Dict[str, float]:
    print('DEBUG: display_universal_trading_metrics called')
    """
    Universal function to calculate and display trading metrics for any rule type.
    """
    calculator = UniversalTradingMetrics(lot_size, risk_reward_ratio, fee_per_trade)
    return calculator.calculate_and_display_metrics(df, rule) 