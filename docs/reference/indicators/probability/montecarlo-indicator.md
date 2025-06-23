# Monte Carlo Simulation Indicator

## Overview

The Monte Carlo Simulation indicator uses random sampling to estimate probability distributions of price movements. It generates multiple simulated price paths based on historical volatility and returns to provide probability estimates for future price levels.

## Formula

```
For each simulation:
  Returns = random_normal(mean_return, std_return, period)
  Simulated_Price = current_price × ∏(1 + returns)
Final_Price = median(all_simulated_prices)
```

Where:
- **mean_return**: Average historical return
- **std_return**: Standard deviation of historical returns
- **period**: Forecast period
- **random_normal**: Normal distribution random sampling

## Parameters

- **simulations** (default: 1000): Number of Monte Carlo simulations
- **period** (default: 20): Forecast period
- **price_type** (default: close): Price type to use (open/close)

## Usage

### Command Line

```bash
# Basic usage with default parameters
python run_analysis.py demo --rule MonteCarlo

# Custom parameters
python run_analysis.py demo --rule MonteCarlo --price-type open

# With specific data source
python run_analysis.py yfinance --ticker AAPL --period 1y --rule MonteCarlo
```

### Interactive Mode

```bash
python run_analysis.py interactive
# Select MonteCarlo from the indicator list
```

## Trading Signals

### Buy Signals
- Price is below forecast and forecast is rising
- Price crosses above forecast line
- Forecast shows upward probability

### Sell Signals
- Price is above forecast and forecast is falling
- Price crosses below forecast line
- Forecast shows downward probability

## Interpretation

### Probability Analysis
- **High Probability**: Forecast close to current price
- **Low Probability**: Forecast far from current price
- **Confidence Interval**: Range of likely outcomes

### Risk Assessment
- **High Volatility**: Wide range of simulated outcomes
- **Low Volatility**: Narrow range of simulated outcomes
- **Risk/Reward**: Balance of potential gains vs losses

### Market Conditions
- **Trending Market**: Clear directional bias in simulations
- **Sideways Market**: Mixed directional outcomes
- **Volatile Market**: Wide dispersion of outcomes

## Advantages

- ✅ Provides probability estimates
- ✅ Based on statistical methods
- ✅ Good for risk assessment
- ✅ Flexible parameters

## Disadvantages

- ❌ Computationally intensive
- ❌ Results may vary
- ❌ Requires sufficient historical data
- ❌ Assumes normal distribution

## Example Output

```
MonteCarlo: [150.25, 151.34, 152.67, 153.89, 155.12]
MonteCarlo_Signal: [NOTRADE, NOTRADE, BUY, BUY, BUY]
```

## Related Indicators

- **Kelly**: For position sizing
- **Bollinger Bands**: For volatility context
- **ATR**: For volatility measurement
- **Standard Deviation**: For risk assessment

## References

- Monte Carlo Method Wikipedia: https://en.wikipedia.org/wiki/Monte_Carlo_method
- Financial Risk Management by Philippe Jorion 