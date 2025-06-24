# Advanced Trading Metrics

## Overview

The system provides comprehensive trading metrics for strategy analysis, including machine learning features and Monte Carlo simulations for robust strategy evaluation.

## Machine Learning Metrics

### Signal Quality Analysis

#### Signal Frequency
- **Description**: Measures how often trading signals occur
- **Formula**: `(Number of signal changes) / (Total periods)`
- **Interpretation**: Lower values indicate more stable strategies
- **Range**: 0.0 - 1.0

#### Signal Stability
- **Description**: Consistency of signal patterns over time
- **Formula**: `1 - Signal Frequency`
- **Interpretation**: Higher values indicate more consistent strategies
- **Range**: 0.0 - 1.0

#### Signal Accuracy
- **Description**: Percentage of signals that result in profitable trades
- **Formula**: `(Profitable signals) / (Total signals) * 100`
- **Interpretation**: Higher values indicate better signal quality
- **Range**: 0% - 100%

#### Signal Timing Score
- **Description**: Average return per signal
- **Formula**: `Mean(signal * price_change) * 100`
- **Interpretation**: Positive values indicate good timing
- **Range**: Unbounded

### Feature Correlation Analysis

#### Momentum Correlation
- **Description**: Correlation between price momentum and signals
- **Formula**: `Correlation(price_momentum, signals)`
- **Interpretation**: Values close to ±1 indicate strong relationships
- **Range**: -1.0 to 1.0

#### Volatility Correlation
- **Description**: Correlation between volatility and signals
- **Formula**: `Correlation(rolling_volatility, signals)`
- **Interpretation**: Helps identify volatility-based strategies
- **Range**: -1.0 to 1.0

#### Trend Correlation
- **Description**: Correlation between trend strength and signals
- **Formula**: `Correlation(trend_strength, signals)`
- **Interpretation**: Indicates trend-following behavior
- **Range**: -1.0 to 1.0

### Pattern Recognition

#### Pattern Consistency
- **Description**: Reliability of signal patterns using rolling windows
- **Formula**: `Mean(consistency_scores) * 100`
- **Interpretation**: Higher values indicate more reliable patterns
- **Range**: 0% - 100%

#### Signal Clustering
- **Description**: Concentration of signals in time
- **Formula**: `1 / (1 + average_distance_between_signals) * 100`
- **Interpretation**: Higher values indicate signal clustering
- **Range**: 0% - 100%

### Risk-Adjusted Features

#### Risk-Adjusted Momentum
- **Description**: Momentum normalized by volatility
- **Formula**: `Mean(price_momentum) / Mean(rolling_volatility)`
- **Interpretation**: Higher values indicate better risk-adjusted momentum
- **Range**: Unbounded

#### Risk-Adjusted Trend
- **Description**: Trend strength normalized by volatility
- **Formula**: `Mean(trend_strength) / Mean(rolling_volatility)`
- **Interpretation**: Higher values indicate better risk-adjusted trends
- **Range**: Unbounded

## Monte Carlo Metrics

### Return Analysis

#### Expected Return
- **Description**: Average return from Monte Carlo simulations
- **Formula**: `Mean(simulation_results) * 100`
- **Interpretation**: Expected performance across scenarios
- **Range**: Unbounded

#### Standard Deviation
- **Description**: Volatility of returns across simulations
- **Formula**: `Std(simulation_results) * 100`
- **Interpretation**: Lower values indicate more consistent returns
- **Range**: 0% - ∞

### Risk Metrics

#### Value at Risk (VaR) 95%
- **Description**: Maximum expected loss with 95% confidence
- **Formula**: `Percentile(simulation_results, 5) * 100`
- **Interpretation**: Worst-case scenario loss
- **Range**: Unbounded

#### Conditional Value at Risk (CVaR) 95%
- **Description**: Expected loss beyond VaR threshold
- **Formula**: `Mean(results <= VaR_95) * 100`
- **Interpretation**: Average loss in worst scenarios
- **Range**: Unbounded

#### Maximum Loss
- **Description**: Worst single simulation result
- **Formula**: `Min(simulation_results) * 100`
- **Interpretation**: Absolute worst-case scenario
- **Range**: Unbounded

#### Maximum Gain
- **Description**: Best single simulation result
- **Formula**: `Max(simulation_results) * 100`
- **Interpretation**: Absolute best-case scenario
- **Range**: Unbounded

### Probability Metrics

#### Profit Probability
- **Description**: Percentage of simulations with positive returns
- **Formula**: `(Positive_simulations / Total_simulations) * 100`
- **Interpretation**: Chance of profitable outcomes
- **Range**: 0% - 100%

#### Monte Carlo Sharpe Ratio
- **Description**: Risk-adjusted return from simulations
- **Formula**: `Expected_Return / Standard_Deviation`
- **Interpretation**: Higher values indicate better risk-adjusted returns
- **Range**: Unbounded

### Strategy Robustness

#### Strategy Robustness
- **Description**: Overall consistency and reliability score
- **Formula**: `Base_score + Consistency_bonus`
- **Interpretation**: Higher values indicate more robust strategies
- **Range**: 0% - 100%

#### Risk of Ruin
- **Description**: Probability of account depletion using Kelly Criterion
- **Formula**: `100 * (1 - Kelly_Fraction)`
- **Interpretation**: Lower values indicate safer strategies
- **Range**: 0% - 100%

## Strategy-Specific Metrics

### Position Sizing

#### Kelly Fraction
- **Description**: Optimal position size based on win rate and payoffs
- **Formula**: `(Win_Rate * Avg_Win - Loss_Rate * Avg_Loss) / Avg_Win`
- **Interpretation**: Fraction of capital to risk per trade
- **Range**: 0.0 - 1.0

#### Optimal Position Size
- **Description**: Recommended position size based on Kelly Criterion
- **Formula**: `Lot_Size * Kelly_Fraction`
- **Interpretation**: Risk-adjusted position sizing
- **Range**: 0.0 - Lot_Size

### Fee Analysis

#### Fee Impact
- **Description**: Percentage of gross returns consumed by fees
- **Formula**: `(Total_Fees / Abs(Gross_Return)) * 100`
- **Interpretation**: Lower values indicate better fee efficiency
- **Range**: 0% - 100%

#### Net Return
- **Description**: Returns after deducting all fees
- **Formula**: `Gross_Return - Total_Fees`
- **Interpretation**: Actual returns available to trader
- **Range**: Unbounded

### Break-Even Analysis

#### Break-Even Win Rate
- **Description**: Minimum win rate needed for profitability
- **Formula**: `Avg_Loss / (Avg_Win + Avg_Loss) * 100`
- **Interpretation**: Win rate threshold for profitability
- **Range**: 0% - 100%

#### Minimum Win Rate for Profit
- **Description**: Win rate needed considering fees
- **Formula**: `(Avg_Loss + Fee) / (Avg_Win + Avg_Loss + 2*Fee) * 100`
- **Interpretation**: Higher threshold due to fees
- **Range**: 0% - 100%

### Strategy Efficiency

#### Strategy Efficiency
- **Description**: Performance efficiency after fees
- **Formula**: `(Net_Return / Abs(Gross_Return)) * 100`
- **Interpretation**: Higher values indicate better efficiency
- **Range**: 0% - 100%

#### Risk-Adjusted Return with Fees
- **Description**: Risk-adjusted performance including fees
- **Formula**: `Expected_Reward / Expected_Risk`
- **Interpretation**: Higher values indicate better risk-adjusted returns
- **Range**: Unbounded

#### Strategy Sustainability
- **Description**: Overall strategy viability score
- **Formula**: `Profitability_score + Position_sizing_score + Efficiency_score`
- **Interpretation**: Higher values indicate more sustainable strategies
- **Range**: 0% - 100%

## Usage Examples

### Command Line Usage
```bash
# Basic strategy analysis
python run_analysis.py demo --rule RSI --strategy 1,2,0.07

# Conservative strategy
python run_analysis.py demo --rule RSI --strategy 0.5,1.5,0.05

# Aggressive strategy
python run_analysis.py demo --rule RSI --strategy 2,3,0.1
```

### Metric Interpretation

#### Good Metrics
- Win Ratio > 50%
- Profit Factor > 1.5
- Sharpe Ratio > 1.0
- Strategy Robustness > 70%
- Risk of Ruin < 20%

#### Warning Signs
- Win Ratio < 40%
- Profit Factor < 1.0
- Maximum Drawdown > 20%
- Strategy Robustness < 50%
- Risk of Ruin > 50%

## Color Coding

The system uses color coding to quickly identify metric quality:

- **🟢 Green**: Excellent performance
- **🟡 Yellow**: Average performance  
- **🔴 Red**: Poor performance

## Best Practices

1. **Start Conservative**: Use smaller position sizes initially
2. **Monitor Robustness**: Focus on strategy sustainability
3. **Consider Fees**: Account for transaction costs
4. **Validate Patterns**: Ensure signal consistency
5. **Risk Management**: Keep risk of ruin low
6. **Regular Review**: Monitor metrics over time 