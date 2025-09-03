# -*- coding: utf-8 -*-
# src/cli/encyclopedia/quant_encyclopedia.py

"""
Quantitative Trading Encyclopedia Module
Provides comprehensive explanations of trading metrics and valuable tips for building robust profitable strategies.
All comments are in English.
"""

import re
from typing import Dict, List, Optional, Tuple
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class QuantEncyclopedia:
    """
    Comprehensive encyclopedia for quantitative traders with metrics explanations and strategy tips.
    """
    
    def __init__(self):
        """Initialize the encyclopedia with all metrics and tips."""
        self.metrics = self._initialize_metrics()
        self.tips = self._initialize_tips()
    
    def _initialize_metrics(self) -> Dict[str, Dict]:
        """Initialize comprehensive trading metrics with detailed explanations."""
        return {
            # Core Performance Metrics
            'win_ratio': {
                'name': 'Win Ratio',
                'icon': '🎯',
                'category': 'Core Performance',
                'description': 'Percentage of profitable trades out of total trades',
                'formula': 'Winning Trades / Total Trades × 100',
                'interpretation': 'Higher win ratios indicate more consistent profitability',
                'good_range': '60-80%',
                'excellent_range': '>80%',
                'warning_range': '<50%',
                'calculation_note': 'Based on actual trade outcomes, not predictions',
                'strategy_impact': 'High win ratio reduces emotional stress and improves consistency'
            },
            
            'profit_factor': {
                'name': 'Profit Factor',
                'icon': '💰',
                'category': 'Core Performance',
                'description': 'Ratio of gross profit to gross loss',
                'formula': 'Gross Profit / Gross Loss',
                'interpretation': 'Shows how much profit is generated per unit of loss',
                'good_range': '1.5-2.0',
                'excellent_range': '>2.0',
                'warning_range': '<1.0',
                'calculation_note': 'Accounts for all winning and losing trades',
                'strategy_impact': 'Key metric for risk-adjusted performance evaluation'
            },
            
            'risk_reward_ratio': {
                'name': 'Risk/Reward Ratio',
                'icon': '⚖️',
                'category': 'Core Performance',
                'description': 'Average win size divided by average loss size',
                'formula': 'Average Win / Average Loss',
                'interpretation': 'Shows potential reward relative to risk taken',
                'good_range': '1.5-2.5',
                'excellent_range': '>2.5',
                'warning_range': '<1.0',
                'calculation_note': 'Based on actual trade outcomes, not planned ratios',
                'strategy_impact': 'Critical for position sizing and risk management'
            },
            
            'sharpe_ratio': {
                'name': 'Sharpe Ratio',
                'icon': '📈',
                'category': 'Risk-Adjusted Returns',
                'description': 'Risk-adjusted return measure relative to risk-free rate',
                'formula': '(Return - Risk-Free Rate) / Standard Deviation',
                'interpretation': 'Higher values indicate better risk-adjusted performance',
                'good_range': '1.0-2.0',
                'excellent_range': '>2.0',
                'warning_range': '<0.5',
                'calculation_note': 'Annualized measure assuming daily returns',
                'strategy_impact': 'Industry standard for comparing strategy performance'
            },
            
            'sortino_ratio': {
                'name': 'Sortino Ratio',
                'icon': '📊',
                'category': 'Risk-Adjusted Returns',
                'description': 'Risk-adjusted return using downside deviation',
                'formula': '(Return - Risk-Free Rate) / Downside Deviation',
                'interpretation': 'Focuses on harmful volatility (downside risk)',
                'good_range': '1.0-2.0',
                'excellent_range': '>2.0',
                'warning_range': '<0.5',
                'calculation_note': 'More conservative than Sharpe ratio',
                'strategy_impact': 'Better measure for strategies with asymmetric returns'
            },
            
            'max_drawdown': {
                'name': 'Maximum Drawdown',
                'icon': '📉',
                'category': 'Risk Management',
                'description': 'Largest peak-to-trough decline in portfolio value',
                'formula': 'Max((Peak - Current) / Peak) × 100',
                'interpretation': 'Worst historical loss from a peak',
                'good_range': '<10%',
                'excellent_range': '<5%',
                'warning_range': '>20%',
                'calculation_note': 'Based on cumulative returns over time',
                'strategy_impact': 'Critical for capital preservation and emotional control'
            },
            
            'calmar_ratio': {
                'name': 'Calmar Ratio',
                'icon': '⚡',
                'category': 'Risk-Adjusted Returns',
                'description': 'Annual return divided by maximum drawdown',
                'formula': 'Annual Return / Maximum Drawdown',
                'interpretation': 'Return per unit of maximum risk',
                'good_range': '1.0-2.0',
                'excellent_range': '>2.0',
                'warning_range': '<0.5',
                'calculation_note': 'Requires sufficient historical data',
                'strategy_impact': 'Excellent for comparing strategies with different risk profiles'
            },
            
            'volatility': {
                'name': 'Volatility',
                'icon': '📊',
                'category': 'Risk Management',
                'description': 'Standard deviation of returns',
                'formula': 'Standard Deviation of Returns',
                'interpretation': 'Measure of return variability and risk',
                'good_range': '<15%',
                'excellent_range': '<10%',
                'warning_range': '>25%',
                'calculation_note': 'Annualized measure assuming daily returns',
                'strategy_impact': 'Lower volatility often leads to better compound returns'
            },
            
            'kelly_fraction': {
                'name': 'Kelly Fraction',
                'icon': '🎲',
                'category': 'Position Sizing',
                'description': 'Optimal fraction of capital to risk per trade',
                'formula': '(Win Rate × Avg Win - Loss Rate × Avg Loss) / Avg Win',
                'interpretation': 'Mathematically optimal position size',
                'good_range': '0.1-0.25',
                'excellent_range': '0.15-0.2',
                'warning_range': '>0.5',
                'calculation_note': 'Often used at 1/4 to 1/2 of full Kelly for safety',
                'strategy_impact': 'Optimal position sizing for maximum growth rate'
            },
            
            'total_return': {
                'name': 'Total Return',
                'icon': '📈',
                'category': 'Performance',
                'description': 'Overall percentage return over the period',
                'formula': '(Final Value - Initial Value) / Initial Value × 100',
                'interpretation': 'Absolute performance measure',
                'good_range': '10-30%',
                'excellent_range': '>30%',
                'warning_range': '<0%',
                'calculation_note': 'Does not account for risk or time period',
                'strategy_impact': 'Raw performance measure, should be combined with risk metrics'
            },
            
            'net_return': {
                'name': 'Net Return',
                'icon': '💵',
                'category': 'Performance',
                'description': 'Total return after deducting trading costs',
                'formula': 'Gross Return - Total Trading Costs',
                'interpretation': 'Actual profit after all expenses',
                'good_range': '8-25%',
                'excellent_range': '>25%',
                'warning_range': '<0%',
                'calculation_note': 'Includes commissions, spreads, and slippage',
                'strategy_impact': 'Real-world performance measure'
            },
            
            'strategy_efficiency': {
                'name': 'Strategy Efficiency',
                'icon': '⚙️',
                'category': 'Strategy Quality',
                'description': 'Net return as percentage of gross return',
                'formula': '(Net Return / Gross Return) × 100',
                'interpretation': 'How much of gross profit is retained after costs',
                'good_range': '80-95%',
                'excellent_range': '>90%',
                'warning_range': '<70%',
                'calculation_note': 'Higher values indicate lower trading costs',
                'strategy_impact': 'Critical for high-frequency or high-cost strategies'
            },
            
            'risk_of_ruin': {
                'name': 'Risk of Ruin',
                'icon': '💀',
                'category': 'Risk Management',
                'description': 'Probability of losing entire capital',
                'formula': 'Complex probability calculation based on win rate and R/R',
                'interpretation': 'Risk of complete capital loss',
                'good_range': '<5%',
                'excellent_range': '<1%',
                'warning_range': '>10%',
                'calculation_note': 'Based on Monte Carlo simulations',
                'strategy_impact': 'Ultimate risk measure for capital preservation'
            },
            
            'break_even_win_rate': {
                'name': 'Break-Even Win Rate',
                'icon': '⚖️',
                'category': 'Strategy Analysis',
                'description': 'Minimum win rate needed for profitability',
                'formula': 'Average Loss / (Average Win + Average Loss)',
                'interpretation': 'Win rate threshold for profitable trading',
                'good_range': '<40%',
                'excellent_range': '<30%',
                'warning_range': '>50%',
                'calculation_note': 'Lower values indicate more robust strategy',
                'strategy_impact': 'Helps assess strategy robustness and margin of safety'
            },
            
            'probability_risk_ratio': {
                'name': 'Probability Risk Ratio',
                'icon': '🎲',
                'category': 'Probability Analysis',
                'description': 'Ratio of winning probability to losing probability',
                'formula': 'Probability of Win / Probability of Loss',
                'interpretation': 'Relative likelihood of winning vs losing',
                'good_range': '1.2-2.0',
                'excellent_range': '>2.0',
                'warning_range': '<1.0',
                'calculation_note': 'Based on historical trade outcomes',
                'strategy_impact': 'Useful for understanding strategy edge'
            },
            
            'signal_frequency': {
                'name': 'Signal Frequency',
                'icon': '📡',
                'category': 'Strategy Analysis',
                'description': 'Number of trading signals per time period',
                'formula': 'Total Signals / Time Period',
                'interpretation': 'How often the strategy generates opportunities',
                'good_range': '5-20 per month',
                'excellent_range': '10-15 per month',
                'warning_range': '<2 or >50 per month',
                'calculation_note': 'Should be balanced with signal quality',
                'strategy_impact': 'Affects transaction costs and strategy scalability'
            },
            
            'signal_accuracy': {
                'name': 'Signal Accuracy',
                'icon': '🎯',
                'category': 'Strategy Analysis',
                'description': 'Percentage of signals that result in profitable trades',
                'formula': 'Profitable Signals / Total Signals × 100',
                'interpretation': 'Quality measure of trading signals',
                'good_range': '60-80%',
                'excellent_range': '>75%',
                'warning_range': '<50%',
                'calculation_note': 'Based on actual trade outcomes',
                'strategy_impact': 'Direct measure of strategy edge and reliability'
            }
        }
    
    def _initialize_tips(self) -> Dict[str, Dict]:
        """Initialize comprehensive trading tips and strategy advice."""
        return {
            # Win Rate Tips
            'winrate': {
                'title': 'Win Rate Optimization',
                'icon': '🎯',
                'category': 'Performance',
                'tips': [
                    {
                        'tip': 'Higher win rate is NOT always better! Reality: 1:3 risk/reward with 50% win rate outperforms 80% win rate with 1:1 risk/reward',
                        'explanation': 'Focus on risk-adjusted returns, not just win percentage',
                        'action': 'Calculate expected value: (Win Rate × Avg Win) - (Loss Rate × Avg Loss)'
                    },
                    {
                        'tip': 'Optimal win rate range: 40-70% for most strategies',
                        'explanation': 'Too high win rates often indicate poor risk management',
                        'action': 'Aim for 50-60% win rate with 2:1 or better risk/reward'
                    },
                    {
                        'tip': 'Improve win rate through better entry timing and market condition filters',
                        'explanation': 'Quality over quantity in trade selection',
                        'action': 'Add trend filters, volatility conditions, and time-based filters'
                    },
                    {
                        'tip': 'Accept that 30-40% of trades will be losses - focus on managing them',
                        'explanation': 'Losses are inevitable, but their size is controllable',
                        'action': 'Use strict stop losses and position sizing'
                    }
                ]
            },
            
            # Risk Management Tips
            'risk_management': {
                'title': 'Risk Management Excellence',
                'icon': '🛡️',
                'category': 'Risk Management',
                'tips': [
                    {
                        'tip': 'Never risk more than 1-2% of capital per trade',
                        'explanation': 'Preserves capital for compound growth',
                        'action': 'Calculate position size: (Account Size × Risk %) / Stop Loss Distance'
                    },
                    {
                        'tip': 'Use Kelly Criterion for optimal position sizing',
                        'explanation': 'Mathematically optimal bet sizing for maximum growth',
                        'action': 'Kelly % = (Win Rate × Avg Win - Loss Rate × Avg Loss) / Avg Win'
                    },
                    {
                        'tip': 'Maximum drawdown should never exceed 20%',
                        'explanation': 'Large drawdowns destroy compound growth',
                        'action': 'Implement circuit breakers and reduce position sizes during drawdowns'
                    },
                    {
                        'tip': 'Correlation risk: Don\'t have all positions in same direction',
                        'explanation': 'Diversification reduces portfolio risk',
                        'action': 'Limit correlated positions to 30% of total exposure'
                    }
                ]
            },
            
            # Monte Carlo Tips
            'monte_carlo': {
                'title': 'Monte Carlo Analysis',
                'icon': '🎲',
                'category': 'Advanced Analysis',
                'tips': [
                    {
                        'tip': 'Run 10,000+ simulations to assess strategy robustness',
                        'explanation': 'Monte Carlo reveals worst-case scenarios',
                        'action': 'Use historical trade data to generate random trade sequences'
                    },
                    {
                        'tip': 'Focus on 95% confidence intervals, not just average returns',
                        'explanation': 'Worst-case scenarios are more important than best-case',
                        'action': 'Calculate Value at Risk (VaR) and Conditional VaR'
                    },
                    {
                        'tip': 'Test strategy across different market conditions',
                        'explanation': 'Strategies that work in bull markets may fail in bear markets',
                        'action': 'Separate analysis for trending vs ranging markets'
                    },
                    {
                        'tip': 'Include transaction costs and slippage in simulations',
                        'explanation': 'Real-world performance differs from theoretical',
                        'action': 'Add realistic costs: commissions + spread + slippage'
                    }
                ]
            },
            
            # Neural Network Tips
            'neural_networks': {
                'title': 'Neural Network Strategies',
                'icon': '🧠',
                'category': 'Machine Learning',
                'tips': [
                    {
                        'tip': 'Use ensemble methods: combine multiple models for better predictions',
                        'explanation': 'Reduces overfitting and improves generalization',
                        'action': 'Combine LSTM, GRU, and Transformer models with voting'
                    },
                    {
                        'tip': 'Feature engineering is more important than model complexity',
                        'explanation': 'Quality inputs produce quality outputs',
                        'action': 'Create technical indicators, market regime features, and sentiment data'
                    },
                    {
                        'tip': 'Regular retraining prevents model decay',
                        'explanation': 'Market conditions change, models must adapt',
                        'action': 'Retrain monthly with expanding window approach'
                    },
                    {
                        'tip': 'Use walk-forward analysis to prevent look-ahead bias',
                        'explanation': 'Simulates real-world trading conditions',
                        'action': 'Train on past data, test on future data, then move forward'
                    }
                ]
            },
            
            # Deep Learning Tips
            'deep_learning': {
                'title': 'Deep Learning for Trading',
                'icon': '🤖',
                'category': 'Machine Learning',
                'tips': [
                    {
                        'tip': 'LSTM networks excel at capturing temporal dependencies',
                        'explanation': 'Price movements have memory and patterns',
                        'action': 'Use 50-200 time steps for input sequences'
                    },
                    {
                        'tip': 'Attention mechanisms improve prediction accuracy',
                        'explanation': 'Models learn which time periods are most important',
                        'action': 'Implement Transformer or attention-based architectures'
                    },
                    {
                        'tip': 'Regularization prevents overfitting to historical data',
                        'explanation': 'Overfitting leads to poor out-of-sample performance',
                        'action': 'Use dropout (0.2-0.5), L1/L2 regularization, and early stopping'
                    },
                    {
                        'tip': 'Multi-task learning improves feature representation',
                        'explanation': 'Learning multiple related tasks improves generalization',
                        'action': 'Predict price direction, volatility, and volume simultaneously'
                    }
                ]
            },
            
            # Strategy Development Tips
            'strategy_development': {
                'title': 'Strategy Development',
                'icon': '📊',
                'category': 'Strategy',
                'tips': [
                    {
                        'tip': 'Start simple: complex strategies often underperform simple ones',
                        'explanation': 'More parameters = more overfitting opportunities',
                        'action': 'Begin with moving average crossovers or RSI divergences'
                    },
                    {
                        'tip': 'Focus on edge identification, not prediction accuracy',
                        'explanation': 'Small edges with proper risk management beat perfect predictions',
                        'action': 'Look for statistical anomalies and market inefficiencies'
                    },
                    {
                        'tip': 'Market regime detection improves strategy performance',
                        'explanation': 'Different strategies work in different market conditions',
                        'action': 'Classify markets as trending, ranging, volatile, or calm'
                    },
                    {
                        'tip': 'Transaction costs kill high-frequency strategies',
                        'explanation': 'Frequent trading increases costs and reduces profits',
                        'action': 'Calculate break-even frequency: Cost per Trade / Expected Profit per Trade'
                    }
                ]
            },
            
            # Profit Factor Tips
            'profit_factor': {
                'title': 'Profit Factor Optimization',
                'icon': '💰',
                'category': 'Performance',
                'tips': [
                    {
                        'tip': 'Aim for profit factor > 1.5 for sustainable profitability',
                        'explanation': 'Below 1.5, strategies struggle to overcome costs',
                        'action': 'Focus on improving average win size or reducing average loss'
                    },
                    {
                        'tip': 'Profit factor is more important than win rate',
                        'explanation': 'A 40% win rate with 2:1 profit factor beats 80% win rate with 1:1',
                        'action': 'Let winners run and cut losses quickly'
                    },
                    {
                        'tip': 'Improve profit factor through better exit strategies',
                        'explanation': 'Entry gets you in, exit gets you paid',
                        'action': 'Use trailing stops, partial profit taking, and time-based exits'
                    },
                    {
                        'tip': 'Avoid strategies with profit factor < 1.0',
                        'explanation': 'These strategies lose money even before costs',
                        'action': 'Reject strategies that don\'t show positive expected value'
                    }
                ]
            },
            
            # Position Sizing Tips
            'position_sizing': {
                'title': 'Position Sizing Mastery',
                'icon': '📏',
                'category': 'Risk Management',
                'tips': [
                    {
                        'tip': 'Kelly Criterion provides optimal position sizing',
                        'explanation': 'Mathematically maximizes long-term growth rate',
                        'action': 'Use 1/4 to 1/2 of full Kelly for safety margin'
                    },
                    {
                        'tip': 'Position size should scale with account size',
                        'explanation': 'Larger accounts can take larger positions',
                        'action': 'Risk 1-2% of account per trade, regardless of account size'
                    },
                    {
                        'tip': 'Reduce position size during drawdowns',
                        'explanation': 'Protects capital and reduces emotional pressure',
                        'action': 'Cut position size by 50% when drawdown exceeds 10%'
                    },
                    {
                        'tip': 'Correlated positions require smaller individual sizes',
                        'explanation': 'Multiple similar positions increase portfolio risk',
                        'action': 'Limit correlated positions to 30% of total exposure'
                    }
                ]
            },
            
            # Backtesting Tips
            'backtesting': {
                'title': 'Backtesting Best Practices',
                'icon': '🔬',
                'category': 'Strategy Validation',
                'tips': [
                    {
                        'tip': 'Use out-of-sample testing to prevent overfitting',
                        'explanation': 'In-sample results are overly optimistic',
                        'action': 'Reserve 20-30% of data for final validation'
                    },
                    {
                        'tip': 'Include realistic transaction costs and slippage',
                        'explanation': 'Real trading costs significantly impact performance',
                        'action': 'Add 0.1-0.5% per trade for realistic simulation'
                    },
                    {
                        'tip': 'Test across multiple market conditions',
                        'explanation': 'Strategies must work in different environments',
                        'action': 'Separate testing for bull, bear, and sideways markets'
                    },
                    {
                        'tip': 'Use walk-forward analysis for time series data',
                        'explanation': 'Simulates real-world trading with expanding data',
                        'action': 'Train on past data, test on future, then move forward'
                    }
                ]
            }
        }
    
    def show_all_metrics(self, filter_text: Optional[str] = None) -> None:
        """Display all metrics with detailed explanations."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📚 QUANTITATIVE TRADING METRICS ENCYCLOPEDIA{Style.RESET_ALL}")
        print(f"{'=' * 80}")
        
        # Group metrics by category
        categories = {}
        for metric_key, metric_data in self.metrics.items():
            if filter_text and filter_text.lower() not in metric_key.lower() and filter_text.lower() not in metric_data['name'].lower():
                continue
            
            category = metric_data['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((metric_key, metric_data))
        
        for category, metrics_list in categories.items():
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}📂 {category.upper()}{Style.RESET_ALL}")
            print(f"{'─' * 60}")
            
            for metric_key, metric_data in metrics_list:
                self._display_metric(metric_data)
    
    def show_all_tips(self, filter_text: Optional[str] = None) -> None:
        """Display all trading tips and strategy advice."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}💡 QUANTITATIVE TRADING STRATEGY TIPS{Style.RESET_ALL}")
        print(f"{'=' * 80}")
        
        for tip_key, tip_data in self.tips.items():
            if filter_text and filter_text.lower() not in tip_key.lower() and filter_text.lower() not in tip_data['title'].lower():
                continue
            
            self._display_tip_category(tip_data)
    
    def show_filtered_content(self, filter_text: str) -> None:
        """Show both metrics and tips filtered by text."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔍 SEARCH RESULTS FOR: '{filter_text.upper()}'{Style.RESET_ALL}")
        print(f"{'=' * 80}")
        
        # Show filtered metrics
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}📊 MATCHING METRICS:{Style.RESET_ALL}")
        self.show_all_metrics(filter_text)
        
        # Show filtered tips
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}💡 MATCHING TIPS:{Style.RESET_ALL}")
        self.show_all_tips(filter_text)
    
    def _display_metric(self, metric_data: Dict) -> None:
        """Display a single metric with detailed information."""
        print(f"\n{metric_data['icon']} {Fore.GREEN}{Style.BRIGHT}{metric_data['name']}{Style.RESET_ALL}")
        print(f"   📝 {metric_data['description']}")
        print(f"   🧮 Formula: {metric_data['formula']}")
        print(f"   📊 Interpretation: {metric_data['interpretation']}")
        print(f"   ✅ Good Range: {Fore.GREEN}{metric_data['good_range']}{Style.RESET_ALL}")
        print(f"   🏆 Excellent Range: {Fore.CYAN}{metric_data['excellent_range']}{Style.RESET_ALL}")
        print(f"   ⚠️  Warning Range: {Fore.RED}{metric_data['warning_range']}{Style.RESET_ALL}")
        print(f"   💡 Calculation Note: {metric_data['calculation_note']}")
        print(f"   🎯 Strategy Impact: {metric_data['strategy_impact']}")
    
    def _display_tip_category(self, tip_data: Dict) -> None:
        """Display a category of tips."""
        print(f"\n{tip_data['icon']} {Fore.GREEN}{Style.BRIGHT}{tip_data['title']}{Style.RESET_ALL}")
        print(f"{'─' * 60}")
        
        for i, tip in enumerate(tip_data['tips'], 1):
            print(f"\n   {Fore.YELLOW}{i}.{Style.RESET_ALL} {Fore.CYAN}{Style.BRIGHT}{tip['tip']}{Style.RESET_ALL}")
            print(f"      📖 {tip['explanation']}")
            print(f"      🎯 {tip['action']}")
    
    def get_metric_info(self, metric_name: str) -> Optional[Dict]:
        """Get information about a specific metric."""
        metric_name_lower = metric_name.lower().replace(' ', '_')
        for key, data in self.metrics.items():
            if metric_name_lower in key or metric_name.lower() in data['name'].lower():
                return data
        return None
    
    def get_tips_by_category(self, category: str) -> List[Dict]:
        """Get tips filtered by category."""
        category_lower = category.lower()
        matching_tips = []
        for tip_data in self.tips.values():
            if category_lower in tip_data['category'].lower() or category_lower in tip_data['title'].lower():
                matching_tips.append(tip_data)
        return matching_tips


def main():
    """Main function for testing the encyclopedia."""
    encyclopedia = QuantEncyclopedia()
    
    print("Quantitative Trading Encyclopedia")
    print("Available commands:")
    print("  --metrics                    # Show all metrics")
    print("  --tips                       # Show all tips")
    print("  --filter <text>              # Filter by text")
    print("  --metric <name>              # Show specific metric")
    print("  --tips-category <category>   # Show tips by category")


if __name__ == "__main__":
    main() 