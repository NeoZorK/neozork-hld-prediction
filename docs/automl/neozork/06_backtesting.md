# 06. ♪ Becketting

**Goal:** Learn how to keep trade policies under control and avoid typical mistakes.

♪ What's backup?

**Theory:** Becketting is a fundamental method of assessing trade strategies that allows them to be tested on historical data before actual use. This is a critical stage in the design of trading systems, as it helps to identify potential problems and assess performance.

**Bexting** is a test of a trade strategy on historical data for assessing its potential profitability.

**Why Baactism is critical for financial systems:**
- ** Risk reduction:** Identifys problems to real use
- ** Assessment performance:** Provides an indication of potential profitability
- ♪ Optimization: ♪ Helps find the best strategies ♪
- **validation:** Checks the performance of the strategy on different conditions

♪ ♪ ♪ Why do you need to be back up?

**Theory:** Becketting serves several critical purposes in the design of trading systems. Understanding these objectives helps to provide a proper back-up and interpretation of results.

- **check strategy** on historical data
- Why does it matter?
- ** Plus:** Objective assessment of performance, problem identification
- **Disadvantages:** Historical data may not reflect future conditions

- ** Risk assessment** and potential losses
- What's important is:** Helps understand maximum losses and volatility
- ** Plus:** Risk Planning, Management Capital
- **Disadvantages:** Past risks may not reflect future

- ** Optimization of parameters** of strategy
- What's important is:** Lets you find the best Settings for strategy?
- ** Plus:** improve performance, data adaptation
- **Disadvantages:** Risk retraining, need for validation

- **comparison** different approaches
- Why does it matter?
- ** Plus:** Objective comparison, choice of optimal solution
- **Disadvantages:** Need for correct comparison, statistical relevance

** Supplementary objectives of the buffering:**
- **validation Logski:** check correct implementation of the strategy
- ** Test on different conditions:** check stability on different market conditions
- ** Assessment of transaction costs:** Accounting for commissions, spreads and slips
- ** Capital Planning:** Determination of capital required

♪ Typical bactering errors

**Theory:** Becketting is subject to many errors that can lead to false results and incorrect conclusions.

###1. Look-ahead bias

**Theory:** Look-ahead bias is the use of information from the future in trade decisions in the past, which is one of the most common and dangerous mistakes in buffering.

♪ Why it's problematic ♪
- ** Irrealisticity:** in real trade future information is not available
- **Exceeded results:** Cause artificial overformance
- ♪ Fake confidence ♪ ♪ Creates the illusion of success ♪
- ** Financial losses:** Causes real-use losses

** Plus avoidance look-ahead bias:**
- Realistic results
- Honest assessment of performance
- Risk reduction
- Increased confidence in results

**Minuses of avoidance look-ahead bis:**
- More complex implementation
- Possible reduction in performance
- Need for careful inspection
```python
# ♪ It's not true - Use future data
def bad_backtest(df):
 for i in range(len(df)):
# Use data from the future!
If df.iloc['Close'] > df.iloc['Close']: # OSHIBKA!
 signal = 'BUY'
 else:
 signal = 'SELL'
 return signals

# ♪ It's normal - Use just past data
def good_backtest(df):
 signals = []
 for i in range(len(df)):
# Use only data to current moment
 if i > 0 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
 signal = 'BUY'
 else:
 signal = 'SELL'
 signals.append(signal)
 return signals
```

###2. Survivorship bias

**Theory:** Survivorship bias is an error in testing only on "survivor" assets, ignoring those that have ceased to exist.

♪ Why it's problematic ♪
- **Exceeded results:** Ignoring failed assets distorts results
- ** Irrealisticity: ** In real trade, Working with all the assets
- ♪ Fake confidence ♪ ♪ Creates the illusion of success ♪
- ** Financial losses:** Causes real-use losses

**Address of Survivorship Bias:**
- Realistic results
- Honest assessment of performance
- Risk reduction
- Increased confidence in results

** Accounting for survivorship bias:**
- More complex implementation
- Need for access to complete data
- Possible reduction in performance
```python
# ♪ Unexplained - test only on "survivor" assets
def bad_survivorship_test():
# Test only on assets that exist now
Symbols = ['AAPL', 'GOOGL', 'MSFT'] # All successful companies
 return backtest_symbols(symbols)

# ♪ It's normal to include all assets, including "dead"
def good_survivorship_test():
# Includes all assets that have been traded in the period
Symbols = ['AAPL', 'GOOGL', 'MSFT', 'ENRON', 'LEHMAN'] # integrating bankruptcy
 return backtest_symbols(symbols)
```

### 3. Overfitting (retraining)

**Theory:** Overfitting is an error that comes from over-optimizing the parameters of a strategy on historical data, which leads to a strategy that Working only on learning data but not on new data.

♪ Why it's problematic ♪
- ** Irrealisticity:** Strategy can not Working on new data
- **Exceeded results:** performance on historical data not reflects actual performance
- ♪ Fake confidence ♪ ♪ Creates the illusion of success ♪
- ** Financial losses:** Causes real-use losses

** Plus avoidance overfitting:**
- Realistic results
- Honest assessment of performance
- Risk reduction
- Increased confidence in results

**Mine of avoidance overfitting:**
- More complex implementation
- Need for validation
- Possible reduction in performance
- Need for data separation
```python
# ♪ NON-PREVIL - optimized on all data
def bad_optimization(df):
# Optimize paragraphs on all data
 best_params = optimize_parameters(df) # retraining!
 return backtest_with_params(df, best_params)

# ♪ It's the right thing to do - share on tran/test
def good_optimization(df):
# Split the data
 train_data = df[:int(len(df)*0.7)]
 test_data = df[int(len(df)*0.7):]

# Optimizing on train
 best_params = optimize_parameters(train_data)

# Testing on test
 return backtest_with_params(test_data, best_params)
```

## The right backup

**Theory:** The right buffering requires careful design and consideration of all aspects of trade.

1. **Logski Four Division** - Office of the Strategy from Implementation
2. ** Accounting for transaction costs** - commissions, spreads, slipping
3. ** Correct Management Positions** - Opening, closing, coup
4. ** Exact calculation of metric** - return, risk, fallout
5. **validation of results** - check of validity of calculations

###1.Structure buffering

**Theory:** The Backtester class is the basis for the bactering process. It encapsulates the entire Logs of Trade, Management Capital, and the calculation of metrics.

- ** Modularity:** Easy to test different strategies
- ** Extension:** Add new functions without changing the main Logski
- It's easy to find and correct mistakes.
- **validation:** Check the validity of the calculations

**key components:**
- **Management capital:** Traceability of available capital and position
- ** Execution of transactions:** Logs to open and close items
- **Metric calculation:** Evaluation of performance strategy
- ** History:** Recording all trades

```python
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Trade:
"Class for the storage of transaction information."
 timestamp: datetime
 price: float
 quantity: float
 direction: str # 'LONG' or 'SHORT'
 profit: float = 0.0
 commission: float = 0.0

class Backtester:
 """
Class for trade strategybacking

This class performs a full round of betting:
1. Initiating with seed capital
2. Receiving signals from the strategy
3. Trade performance
4. Calculation of the metric performance
5. Maintenance of history of transactions
 """

 def __init__(self, initial_capital: float = 10000, commission: float = 0.001):
 """
Initialization of the Baekrester

 Args:
institutional_capital: seed capital for trading
Commission: Commission for the transaction (in shares from the amount)
 """
 self.initial_capital = initial_capital
 self.commission = commission
Self.capital = initial_capital # Current available capital
Self.position = 0 # Current item (number of items of asset)
Self.position_value = 0 # Cost of current entry
Self.trades: List[Trade] = [] # History of transactions
Self.equity_curve: List[float] = [] # Capital curve
Self.daily_returns: List[float] = [] # Daily returns

 def run_backtest(self, data: pd.dataFrame, strategy) -> Dict[str, Any]:
 """
Launch full-cycle betting

 Args:
Data: Historical data (OHLCV)
strategy: Strategy subject with quet_signal()

 Returns:
Vocabulary with metrics
 """
prent(f"Launchbacking on {len(data)}periods...")

# Reset of fortune
 self.capital = self.initial_capital
 self.position = 0
 self.position_value = 0
 self.trades = []
 self.equity_curve = []
 self.daily_returns = []

 for i, (timestamp, row) in enumerate(data.iterrows()):
# We're getting a signal from strategy (only on historical data)
 signal = strategy.get_signal(data.iloc[:i+1])

# Doing a trade
 self.execute_trade(row, signal, timestamp)

# Calculate the present value of the portfolio
 current_equity = self.calculate_current_equity(row['Close'])
 self.equity_curve.append(current_equity)

# Calculate daily returns
 if i > 0:
 daily_return = (current_equity - self.equity_curve[i-1]) / self.equity_curve[i-1]
 self.daily_returns.append(daily_return)

Print(f"Bexting completed. {len(self.trades}}transactions completed)
 return self.calculate_metrics()

 def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
 """
Trade transaction on signal

 Args:
row: Current Data Line (OHLCV)
Signal: Trade signal ('BUY', 'SELL', 'HOLD')
Timetamp: Time mark of transaction
 """
 if signal == 'BUY' and self.position <= 0:
# Buying: close short position (if precent) and open long
 if self.position < 0:
 self.close_position(row['Close'], timestamp, 'SHORT')

 self.open_position(row['Close'], 'LONG', timestamp)

 elif signal == 'SELL' and self.position >= 0:
# Sale: close the long position (if precent) and open the short
 if self.position > 0:
 self.close_position(row['Close'], timestamp, 'LONG')

 self.open_position(row['Close'], 'SHORT', timestamp)

 elif signal == 'HOLD':
# Hold the current position
 pass

 def open_position(self, price: float, direction: str, timestamp: datetime) -> None:
 """
Opening of the new position

 Args:
Price: Price of opening position
direction: Position direction ('LONG' or 'SHORT')
Timetamp: Time mark
 """
 if direction == 'LONG':
# Buying: Use all available capital
 self.position = self.capital / price
 self.position_value = self.position * price
 self.capital = 0

# Recording the deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=self.position,
 direction='LONG',
 commission=self.position_value * self.commission
 )
 self.trades.append(trade)

 elif direction == 'SHORT':
# Sales: Open a short position
 self.position = -self.capital / price
 self.position_value = abs(self.position) * price
 self.capital = 0

# Recording the deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=abs(self.position),
 direction='SHORT',
 commission=self.position_value * self.commission
 )
 self.trades.append(trade)

 def close_position(self, price: float, timestamp: datetime, direction: str) -> None:
 """
Closure of current position

 Args:
Price: Cost of closing position
Timetamp: Time mark
direction: closed position direction
 """
 if direction == 'LONG' and self.position > 0:
# Close the long position
 self.capital = self.position * price * (1 - self.commission)
 profit = self.capital - self.position_value

# Recording the closing deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=self.position,
 direction='CLOSE_LONG',
 profit=profit,
 commission=self.position * price * self.commission
 )
 self.trades.append(trade)

 elif direction == 'SHORT' and self.position < 0:
# Close the short position
 self.capital = -self.position * price * (1 - self.commission)
 profit = self.capital - self.position_value

# Recording the closing deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=abs(self.position),
 direction='CLOSE_SHORT',
 profit=profit,
 commission=abs(self.position) * price * self.commission
 )
 self.trades.append(trade)

# Drop the position
 self.position = 0
 self.position_value = 0

 def calculate_current_equity(self, current_price: float) -> float:
 """
Calculation of current portfolio value

 Args:
Current_price: Current asset price

 Returns:
Current value of portfolio
 """
if Self.position > 0: # Long position
 return self.position * current_price
elif elf.position < 0: # Short Item
 return self.capital + (-self.position * current_price)
Else: # No position
 return self.capital
```

♪##2 ♪ Calculation of the metric

**Theory:** Calculation of the metric performance is a critical step in the buffering process.

- ** Assess profitability** strategies in absolute and relative terms
- ** Measure risk** through volatility and tarmacs
- ** Equalize strategies** objectively
- ** To decide** on the implementation of a strategy in real trade

** Key metrics:**
- ** Income:** Total, annual, average
- **Risk:** Volatility, maximum draught, VaR
- ** Effectiveness:** Sharpe ratio, Sortino ratio, Kalmar ratio
- **Stability:** Win rent, profit factor, recovery factor

```python
def calculate_metrics(self) -> Dict[str, Any]:
 """
Calculation of integrated metric performance strategy

This method calculates all major indicators for evaluation
Trade strategy:

1. Return rates
2. Risk metrics (risk metrics)
3. Efficiency metrics
4. Stability instruments

 Returns:
Vocabulary with calculated metrics
 """
 if not self.equity_curve:
 return self._empty_metrics()

# ==Metrics income==

#Total Return
# Shows total capital gains for the whole period
 total_return = (self.equity_curve[-1] - self.initial_capital) / self.initial_capital

# Annualized Return
# Brings returns to the annual equivalent for comparison
Years = Len(self.equity_curve) / 252 #252 trade days in year
 if years > 0:
 annual_return = (1 + total_return) ** (1/years) - 1
 else:
 annual_return = 0

# Average daily return
 if self.daily_returns:
 avg_daily_return = np.mean(self.daily_returns)
 else:
 avg_daily_return = 0

== sync, corrected by elderman ==

# Volatility
# Standard income deviation as per annual equivalent
 if self.daily_returns:
 volatility = np.std(self.daily_returns) * np.sqrt(252)
 else:
 volatility = 0

# Maximum Drawdown maximum
# Maximum loss from peak to minimum
 equity_series = pd.Series(self.equity_curve)
 running_max = equity_series.expanding().max()
 drawdown = (equity_series - running_max) / running_max
 max_drawdown = drawdown.min()

♪ Average tarmac
 avg_drawdown = drawdown[drawdown < 0].mean() if (drawdown < 0).any() else 0

# Maximum draught length (in days)
 max_dd_duration = self._calculate_max_drawdown_duration(drawdown)

# Value at Risk (VAR) - 95% confidence interval
 if self.daily_returns:
 var_95 = np.percentile(self.daily_returns, 5)
 else:
 var_95 = 0

# ==Metrics efficiency ==

 # Sharpe Ratio
# The ratio of excess returns to volatility
Risk_free_rate = 0.02 # 2% risk-free rate
 if volatility > 0:
 sharpe_ratio = (annual_return - risk_free_rate) / volatility
 else:
 sharpe_ratio = 0

 # Sortino Ratio
# AnaLogssically Sharpe, but only takes into account negative volatility
 if self.daily_returns:
 negative_returns = [r for r in self.daily_returns if r < 0]
 if negative_returns:
 downside_volatility = np.std(negative_returns) * np.sqrt(252)
 if downside_volatility > 0:
 sortino_ratio = (annual_return - risk_free_rate) / downside_volatility
 else:
 sortino_ratio = 0
 else:
 sortino_ratio = float('inf') if annual_return > risk_free_rate else 0
 else:
 sortino_ratio = 0

 # Calmar Ratio
# The ratio of annual return to maximum draught
 if abs(max_drawdown) > 0:
 calmar_ratio = annual_return / abs(max_drawdown)
 else:
 calmar_ratio = float('inf') if annual_return > 0 else 0

# ==Metrics STABILITY ==

# Win Rate - Percentage of profit-making transactions
 if self.trades:
 profitable_trades = [t for t in self.trades if t.profit > 0]
 win_rate = len(profitable_trades) / len(self.trades)

#Profit Factor - The profit-to-loss ratio
 total_profit = sum(t.profit for t in self.trades if t.profit > 0)
 total_loss = abs(sum(t.profit for t in self.trades if t.profit < 0))
 profit_factor = total_profit / total_loss if total_loss > 0 else float('inf')

# Average profit and loss
 avg_win = total_profit / len(profitable_trades) if profitable_trades else 0
 losing_trades = [t for t in self.trades if t.profit < 0]
 avg_loss = abs(sum(t.profit for t in losing_trades)) / len(losing_trades) if losing_trades else 0

# Recovery Factor - the ratio of total profits to maximum rainfall
 recovery_factor = total_profit / abs(max_drawdown) if abs(max_drawdown) > 0 else float('inf')
 else:
 win_rate = 0
 profit_factor = 0
 avg_win = 0
 avg_loss = 0
 recovery_factor = 0

* == sync, corrected by elderman == @elder_man

# The coefficient of variation
# The ratio of volatility to average return
 if avg_daily_return != 0:
 coefficient_of_variation = volatility / (avg_daily_return * 252)
 else:
 coefficient_of_variation = float('inf')

# Stability Index
# Shows stability of return
 if self.daily_returns:
 stability_index = 1 - (np.std(self.daily_returns) / abs(avg_daily_return)) if avg_daily_return != 0 else 0
 else:
 stability_index = 0

 return {
# Return metrics
 'total_return': total_return,
 'annual_return': annual_return,
 'avg_daily_return': avg_daily_return,

# risk metrics
 'volatility': volatility,
 'max_drawdown': max_drawdown,
 'avg_drawdown': avg_drawdown,
 'max_dd_duration': max_dd_duration,
 'var_95': var_95,

# metrics efficiency
 'sharpe_ratio': sharpe_ratio,
 'sortino_ratio': sortino_ratio,
 'calmar_ratio': calmar_ratio,

# metrics stability
 'win_rate': win_rate,
 'profit_factor': profit_factor,
 'avg_win': avg_win,
 'avg_loss': avg_loss,
 'recovery_factor': recovery_factor,

# Additional metrics
 'coefficient_of_variation': coefficient_of_variation,
 'stability_index': stability_index,
 'total_trades': len(self.trades),
 'final_capital': self.equity_curve[-1] if self.equity_curve else self.initial_capital
 }

def _calculate_max_drawdown_duration(self, drawdown: pd.Series) -> int:
 """
Calculation of the length of maximum draught in days

 Args:
drawdown: Slide Series

 Returns:
Maximum length of tarding in days
 """
 if drawdown.empty:
 return 0

# We find periods of tardiness
 in_drawdown = drawdown < 0
 drawdown_periods = []
 current_period = 0

 for is_dd in in_drawdown:
 if is_dd:
 current_period += 1
 else:
 if current_period > 0:
 drawdown_periods.append(current_period)
 current_period = 0

# Adding the last period if there is
 if current_period > 0:
 drawdown_periods.append(current_period)

 return max(drawdown_periods) if drawdown_periods else 0

def _empty_metrics(self) -> Dict[str, Any]:
"Returns empty metrics in the absence of data."
 return {
 'total_return': 0, 'annual_return': 0, 'avg_daily_return': 0,
 'volatility': 0, 'max_drawdown': 0, 'avg_drawdown': 0,
 'max_dd_duration': 0, 'var_95': 0, 'sharpe_ratio': 0,
 'sortino_ratio': 0, 'calmar_ratio': 0, 'win_rate': 0,
 'profit_factor': 0, 'avg_win': 0, 'avg_loss': 0,
 'recovery_factor': 0, 'coefficient_of_variation': 0,
 'stability_index': 0, 'total_trades': 0, 'final_capital': self.initial_capital
 }
```

## Advances in Baactering Technology

**Theory:** Advances in betting techniques provide more reliable and realistic estimates of performance strategies.

- ** Avoid retraining** through correct data separation
- ** Assess stability** strategies on different periods
- **Measure uncertainty** through statistical methods
- ** Checking the efficacy** strategies for market change

### 1. Walk-Forward Analysis

**Theory:** Walk-Forward Analysis (WFA) is a strategy test method that simulates real trade.

1. ** Training on historical data** - strategy learning on past data
2. ** Test on the following data** - trained strategy is tested on the following data:
3. **Slip window** - process repeated with moving data window

** Benefits of WFA:**
- ** Reality:** Simulates real trade
- ** Avoiding retraining:** Strategy nnot sees future data
- ** Stability assessment:** Shows how the Workinget strategy is on different periods.
- ** Adaptation: ** Strategy can adapt to market changes

** Key variables:**
**Train Period:** Length of the learning period (usually 1-2 years)
- **Test Period:** Test period length (usually 1-3 months)
- **Step Size:** Step of the window shift (usually equals test_period)

```python
def walk_forward_Analysis(data: pd.dataFrame, strategy,
 train_period: int = 252,
 test_period: int = 63,
 step_size: int = None) -> List[Dict[str, Any]]:
 """
Implementation of the Walk-Forward Strategy

Walk-Forward analysis simulates real trade:
1. Training a strategy on historical data
2. Test on the following data
3. Move the window and repeat the process

 Args:
Data: Historical data (OHLCV)
strategy: subject to strategy with train() and get_signal()
Train_period: Length of learning period in days (on default 252)
test_period: Length of test period in days (on default 63)
step_size: Step of window shift in days (on default is test_period)

 Returns:
List of results for each test period
 """
 if step_size is None:
 step_size = test_period

 results = []
 total_periods = len(data) - train_period - test_period

 print(f"Launch Walk-Forward Analysis:")
Print(f" - Learning period: {training_period}days")
pprint(f" - test period: {test_period}days")
Print(f" - move: {step_size}days")
prent(f" - Total periods: {total_periods / / step_size + 1})

 for start_idx in range(0, total_periods + 1, step_size):
# Defining boundaries periods
 train_start = start_idx
 train_end = start_idx + train_period
 test_start = train_end
 test_end = test_start + test_period

# Checking that we have enough data
 if test_end > len(data):
 break

# Extracting data for learning and testing
 train_data = data.iloc[train_start:train_end].copy()
 test_data = data.iloc[test_start:test_end].copy()

prent(f"Period {len(results) + 1}:"
(f) Training {training_data.index[0].date()} - {training_data.index[-1].date()},"
f "Test {test_data.index[0].date()} - {test_data.index[-1].data(}}")

 try:
# Training strategy on historical data
 strategy.train(train_data)

# Testing on the following data
 backtester = Backtester()
 metrics = backtester.run_backtest(test_data, strategy)

# Save the results
 results.append({
 'period': len(results) + 1,
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'train_days': len(train_data),
 'test_days': len(test_data),
 'metrics': metrics,
 'trades': len(backtester.trades),
 'equity_curve': backtester.equity_curve.copy()
 })

 except Exception as e:
Print(f) Error in period {len(s) + 1}: {e}}
 continue

print(f"Walk-Forward analysis completed. ObWorkingno {len(results}periods)
 return results

def analyze_walk_forward_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
 """
Analysis of the results of the Walk-Forward Analysis

 Args:
Results: Results of Walk-Forward Analysis

 Returns:
The dictionary with aggregated metrics
 """
 if not results:
 return {}

# We extract metrics from all periods
 all_returns = [r['metrics']['total_return'] for r in results]
 all_sharpe = [r['metrics']['sharpe_ratio'] for r in results]
 all_max_dd = [r['metrics']['max_drawdown'] for r in results]
 all_win_rates = [r['metrics']['win_rate'] for r in results]

# Computing statistics
 Analysis = {
 'total_periods': len(results),
 'avg_return': np.mean(all_returns),
 'std_return': np.std(all_returns),
 'min_return': np.min(all_returns),
 'max_return': np.max(all_returns),
 'positive_periods': sum(1 for r in all_returns if r > 0),
 'positive_periods_pct': sum(1 for r in all_returns if r > 0) / len(all_returns),

 'avg_sharpe': np.mean(all_sharpe),
 'std_sharpe': np.std(all_sharpe),
 'min_sharpe': np.min(all_sharpe),
 'max_sharpe': np.max(all_sharpe),

 'avg_max_dd': np.mean(all_max_dd),
 'worst_dd': np.min(all_max_dd),
 'avg_win_rate': np.mean(all_win_rates),

 'consistency_score': 1 - np.std(all_returns) / (np.mean(all_returns) + 1e-8),
 'stability_score': sum(1 for r in all_returns if r > 0) / len(all_returns)
 }

 return Analysis
```

### 2. Monte Carlo Simulation

**Theory:** Monte Carlo simulation is a statistical method that uses a random sample for estimating uncertainty in the backtting results.

1. ** Accidental data conversion** - Creating multiple random trade days
2. ** Multiple bacters** - Test strategy on each conversion
3. ** Statistical analysis** - analysis of results distribution

** The benefits of Monte Carlo:**
- ** Uncertainty assessment:** Shows the range of possible results
- **check roboticity:** Testes strategy on different sequences
- **Statistical significance:** Allows an assessment of the reliability of the results
- **Manage Risks:** Helps understand the worst and best scenarios

** Application:**
- **validation strategy:** check that the results are not random
- ** Risk assessment:** Understanding potential losses
- ** Capital Planning:** Determination of capital required
- **comparison of strategies:** Statistical comparative of different approaches

```python
def monte_carlo_simulation(data: pd.dataFrame, strategy,
 n_simulations: int = 1000,
 block_size: int = 1) -> List[Dict[str, Any]]:
 """
Monte carlo simulation for uncertainty assessment

Monte Carlo simulation creates many random reboots.
And he's testing the strategy on each of them.
This makes it possible to assess the uncertainty and consistency of the results.

 Args:
Data: Historical data (OHLCV)
strategy: Strategy subject with quet_signal()
n_simulations: Number of simulations (on default 1000)
Block_size: Size of units for reset (on default 1)

 Returns:
List of results for each simulation
 """
Print(f"Launch Monte Carlo simulations:")
Print(f" - Number of simulations: {n_simulations})
Print(f" - Size of blocks: {lock_size}")
prent(f" - Data size: {len(data)}periods)

 results = []

 for i in range(n_simulations):
 if (i + 1) % 100 == 0:
(f) Implemented {i + 1}/{n_simulations} simulations}

 try:
 if block_size == 1:
# Simple shift (every day independently)
 shuffled_data = data.sample(frac=1).reset_index(drop=True)
 else:
# Blocking (save data structure)
 shuffled_data = _block_shuffle_data(data, block_size)

# Becketting on Transported Data
 backtester = Backtester()
 metrics = backtester.run_backtest(shuffled_data, strategy)

 results.append({
 'simulation': i + 1,
 'metrics': metrics,
 'trades': len(backtester.trades),
 'final_capital': backtester.equity_curve[-1] if backtester.equity_curve else backtester.initial_capital
 })

 except Exception as e:
Print(f) Error in simulation {i + 1}: {e})
 continue

Print(f"Monte Carlo simulation complete. Successfully implemented {len(results}) simulations)
 return results

def _block_shuffle_data(data: pd.dataFrame, block_size: int) -> pd.dataFrame:
 """
Blocking data for structure preservation

 Args:
Data: Reference data
Block_size: Size of blocks

 Returns:
Transferred data with structure retention
 """
 n_blocks = len(data) // block_size
 blocks = []

 for i in range(n_blocks):
 start_idx = i * block_size
 end_idx = start_idx + block_size
 block = data.iloc[start_idx:end_idx].copy()
 blocks.append(block)

# Randomly moving blocks
 np.random.shuffle(blocks)

# Uniting blocks
 shuffled_data = pd.concat(blocks, ignore_index=True)

# Add the rest of the data, if present
 remaining = len(data) % block_size
 if remaining > 0:
 remaining_data = data.iloc[-remaining:].copy()
 shuffled_data = pd.concat([shuffled_data, remaining_data], ignore_index=True)

 return shuffled_data

def analyze_monte_carlo_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
 """
Integrated analysis of the Monte Carlo simulation results

Analyses the distribution of results and provides statistics
To assess the uncertainties and risks of the strategy.

 Args:
Results: Monte Carlo simulation results

 Returns:
Vocabulary with Analysis of Results
 """
 if not results:
 return {}

# We're extracting the basic metrics
 returns = [r['metrics']['total_return'] for r in results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
 max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
 win_rates = [r['metrics']['win_rate'] for r in results]
 final_capitals = [r['final_capital'] for r in results]

# Basic statistics
 Analysis = {
 'n_simulations': len(results),

# Return rate statistics
 'return_stats': {
 'mean': np.mean(returns),
 'std': np.std(returns),
 'min': np.min(returns),
 'max': np.max(returns),
 'median': np.median(returns),
 'skewness': _calculate_skewness(returns),
 'kurtosis': _calculate_kurtosis(returns)
 },

# Percentages of return
 'return_percentiles': {
 'p1': np.percentile(returns, 1),
 'p5': np.percentile(returns, 5),
 'p10': np.percentile(returns, 10),
 'p25': np.percentile(returns, 25),
 'p50': np.percentile(returns, 50),
 'p75': np.percentile(returns, 75),
 'p90': np.percentile(returns, 90),
 'p95': np.percentile(returns, 95),
 'p99': np.percentile(returns, 99)
 },

# Probability
 'probabilities': {
 'positive_return': np.mean([r > 0 for r in returns]),
 'negative_return': np.mean([r < 0 for r in returns]),
 'return_above_10pct': np.mean([r > 0.1 for r in returns]),
 'return_above_20pct': np.mean([r > 0.2 for r in returns]),
 'return_below_minus10pct': np.mean([r < -0.1 for r in returns]),
 'return_below_minus20pct': np.mean([r < -0.2 for r in returns])
 },

# Risk statistics
 'risk_stats': {
 'avg_max_drawdown': np.mean(max_drawdowns),
 'worst_drawdown': np.min(max_drawdowns),
 'drawdown_std': np.std(max_drawdowns),
 'avg_sharpe': np.mean(sharpe_ratios),
 'sharpe_std': np.std(sharpe_ratios),
 'min_sharpe': np.min(sharpe_ratios),
 'max_sharpe': np.max(sharpe_ratios)
 },

 # VaR and CVaR
 'var_cvar': {
 'var_95': np.percentile(returns, 5),
 'var_99': np.percentile(returns, 1),
 'cvar_95': np.mean([r for r in returns if r <= np.percentile(returns, 5)]),
 'cvar_99': np.mean([r for r in returns if r <= np.percentile(returns, 1)])
 },

# Additional metrics
 'additional': {
 'avg_win_rate': np.mean(win_rates),
 'win_rate_std': np.std(win_rates),
 'avg_trades': np.mean([r['trades'] for r in results]),
 'consistency_score': 1 - np.std(returns) / (np.mean(returns) + 1e-8),
 'stability_score': np.mean([r > 0 for r in returns])
 }
 }

 return Analysis

def _calculate_skewness(data: List[float]) -> float:
"""""" "The calculation of distribution asymmetries"""
 if len(data) < 3:
 return 0
 mean = np.mean(data)
 std = np.std(data)
 if std == 0:
 return 0
 return np.mean([(x - mean) ** 3 for x in data]) / (std ** 3)

def _calculate_kurtosis(data: List[float]) -> float:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 if len(data) < 4:
 return 0
 mean = np.mean(data)
 std = np.std(data)
 if std == 0:
 return 0
 return np.mean([(x - mean) ** 4 for x in data]) / (std ** 4) - 3
```

### 3. Bootstrap Analysis

**Theory:** Bootstrap analysis is a statistical method that uses a resample with return for estimating uncertainty in results. In contrast from Monte Carlo, Bootstrap retains the temporal structure of the data.

** Basic principles:**
1. ** Block sample**-Creating sample from data blocks
2. **Continuing structure** - Support temporary dependencies
3. ** Resample** - Creating multiple data options
4. ** Statistical analysis** - assess uncertainty of results

** Benefits of Bootstrap:**
- ** Structure preservation:** Considers time dependencies in data
- ** Non-parametricity:**not requires distribution assumptions
- ** Flexibility: ** Can be adapted to different types of data
- ** Reliability:** Provides conservative estimates of uncertainty

** Application:**
- ** Evaluation of confidence intervals** for metric
- **Texting hypothese** about strategy performance
- **comparison of strategies** with uncertainty
- **Planation of sample size** for testing

```python
def bootstrap_Analysis(data: pd.dataFrame, strategy,
 n_bootstrap: int = 1000,
 block_size: int = 20) -> List[Dict[str, Any]]:
 """
Implementation of Bootstrap Analysis for the assessment of uncertainty of results

Bootstrap Analysis creates multiple samples from the raw data
This allows the evaluation of the structure.
Uncertainty in the back-up results.

 Args:
Data: Historical data (OHLCV)
strategy: Strategy subject with quet_signal()
n_bootstrap: Number of bootstrap samples (on default 1000)
Block_size: Sample block size (on default 20)

 Returns:
List of results for each Bootstrap sample
 """
 print(f"Launch Bootstrap Analysis:")
Print(f" - Number of samples: {n_bootstrap})
Print(f" - Size of blocks: {lock_size}")
prent(f" - Data size: {len(data)}periods)

 results = []
 n_blocks_needed = len(data) // block_size

 for i in range(n_bootstrap):
 if (i + 1) % 100 == 0:
Print(f) Implemented {i + 1}/{n_bootstrap} sample}

 try:
♪ Create bootstrap sample with blocks
 bootstrap_data = _create_bootstrap_sample(data, block_size, n_blocks_needed)

# Becketting on Bootstrap sample
 backtester = Backtester()
 metrics = backtester.run_backtest(bootstrap_data, strategy)

 results.append({
 'bootstrap': i + 1,
 'metrics': metrics,
 'trades': len(backtester.trades),
 'final_capital': backtester.equity_curve[-1] if backtester.equity_curve else backtester.initial_capital
 })

 except Exception as e:
print(f" Error in bootstrap sample {i + 1}: {e})
 continue

print(f"Bootstrap analysis completed. Successfully completed {len(results)} sample)
 return results

def _create_bootstrap_sample(data: pd.dataFrame, block_size: int, n_blocks: int) -> pd.dataFrame:
 """
core bootstrap sample with blocks

 Args:
Data: Reference data
Block_size: Size of blocks
n_locks: Number of blocks for sample

 Returns:
Bootstrap Data Sample
 """
 bootstrap_blocks = []
 max_start_idx = len(data) - block_size

 for _ in range(n_blocks):
# Randomly picks the initial index block
 start_idx = np.random.randint(0, max_start_idx + 1)
 end_idx = start_idx + block_size

# Extract the block
 block = data.iloc[start_idx:end_idx].copy()
 bootstrap_blocks.append(block)

# Uniting blocks
 bootstrap_data = pd.concat(bootstrap_blocks, ignore_index=True)

 return bootstrap_data

def analyze_bootstrap_results(results: List[Dict[str, Any]], confidence_level: float = 0.95) -> Dict[str, Any]:
 """
Analysis of Bootstrap Analysis results

Computes confidence intervals and statistics
To assess the uncertainty of results.

 Args:
Results: Results of Bootstrap Analysis
confidence_level: Confidence level (on default 0.95)

 Returns:
Vocabulary with Analysis of Results
 """
 if not results:
 return {}

# We're extracting the basic metrics
 returns = [r['metrics']['total_return'] for r in results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
 max_drawdowns = [r['metrics']['max_drawdown'] for r in results]
 win_rates = [r['metrics']['win_rate'] for r in results]

# Counting confidence intervals
 alpha = 1 - confidence_level
 lower_percentile = (alpha / 2) * 100
 upper_percentile = (1 - alpha / 2) * 100

 Analysis = {
 'n_bootstrap': len(results),
 'confidence_level': confidence_level,

# Confidence interval for return
 'return_ci': {
 'mean': np.mean(returns),
 'std': np.std(returns),
 'lower': np.percentile(returns, lower_percentile),
 'upper': np.percentile(returns, upper_percentile),
 'width': np.percentile(returns, upper_percentile) - np.percentile(returns, lower_percentile)
 },

# Trusting interval for Sharpe ratio
 'sharpe_ci': {
 'mean': np.mean(sharpe_ratios),
 'std': np.std(sharpe_ratios),
 'lower': np.percentile(sharpe_ratios, lower_percentile),
 'upper': np.percentile(sharpe_ratios, upper_percentile),
 'width': np.percentile(sharpe_ratios, upper_percentile) - np.percentile(sharpe_ratios, lower_percentile)
 },

# Confidence intervals for maximum tarmac
 'drawdown_ci': {
 'mean': np.mean(max_drawdowns),
 'std': np.std(max_drawdowns),
 'lower': np.percentile(max_drawdowns, lower_percentile),
 'upper': np.percentile(max_drawdowns, upper_percentile),
 'width': np.percentile(max_drawdowns, upper_percentile) - np.percentile(max_drawdowns, lower_percentile)
 },

# Trusting interval for Win rent
 'win_rate_ci': {
 'mean': np.mean(win_rates),
 'std': np.std(win_rates),
 'lower': np.percentile(win_rates, lower_percentile),
 'upper': np.percentile(win_rates, upper_percentile),
 'width': np.percentile(win_rates, upper_percentile) - np.percentile(win_rates, lower_percentile)
 },

# Statistical significance
 'significance': {
 'return_significant': np.percentile(returns, lower_percentile) > 0,
 'sharpe_significant': np.percentile(sharpe_ratios, lower_percentile) > 0,
 'positive_return_prob': np.mean([r > 0 for r in returns]),
 'sharpe_above_1_prob': np.mean([s > 1 for s in sharpe_ratios])
 }
 }

 return Analysis
```

## Taking into account reality

**Theory:** Realistic back-up should take into account all the factors that influence real trade has to take into account. Ignoring these factors leads to overperformance and incorrect conclusions about strategy performance.

** Key factors of realism:**
- **Target costs:** Commission, spreads, Logs
- ** Visibility:** Impact of volume of bid on price
- ** Slipping:** The difference between the expected and actual price
- ** Delays in execution:** Time between signal and execution
- ** Capital limits:** Minimum positions, marginal requirements

###1: Commissions and distributions

**Theory:** Commissions and spreads are the main transaction costs that are significantly inflatable to the profitability of the strategy; taking these costs into account is critical for achieving realistic results.

**Trips of transaction costs:**
- ** Commissions:** Fixed or interest payments to broker
- **Disbursements:** The difference between purchase price and sale price
- **Logs:** Income tax with profits
- **Bills:** Additional service charges

** Impact on results:**
- ** Decrease in yield:** Direct decrease in profits
- ** Change in trading frequency:** High costs make frequent trade unfavourable
- ** Impact on the size of items:** The need to take into account costs in calculating the size
- ** Change of strategy:** May require modification of the Logs of Trade

```python
class ReaListicBacktester(Backtester):
 """
A realistic back-up with transaction costs

This class expands the base Backtester for accounting
of real trade:
- Transactions commissions
- Distribution between purchase and sale prices
- Minimum dimensions of entries
- Restrictions on the frequency of tendering
 """

 def __init__(self, initial_capital: float = 10000,
 commission: float = 0.001,
 spread: float = 0.0005,
 min_position_size: float = 100,
 min_trade_interval: int = 1):
 """
Initiating a realistic Baekrester

 Args:
initial_capital: seed capital
Commission: Commission for the transaction (in shares from the amount)
spread between purchase and sale prices (in shares)
min_position_size: Minimum size of entry in currency
min_trade_interval: Minimum interval between transactions (in periods)
 """
 super().__init__(initial_capital, commission)
 self.spread = spread
 self.min_position_size = min_position_size
 self.min_trade_interval = min_trade_interval
Self.last_trade_period = -min_trade_interval # Final trading period

 def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
 """
Realization of trade transactions

Considers:
- Distribution between purchase and sale prices
- Minimum dimensions of entries
- Intervals between transactions
- Commissions for each operation

 Args:
row: Current Data Line (OHLCV)
Signal: Trade signal ('BUY', 'SELL', 'HOLD')
Timetamp: Time mark of transaction
 """
 current_period = len(self.equity_curve)

# Checking minimum transaction interval
 if current_period - self.last_trade_period < self.min_trade_interval:
 return

# Calculate the price with the spread
 if signal == 'BUY':
# Buy on price above market
 price = row['Close'] * (1 + self.spread)
 elif signal == 'SELL':
# Sell on price below market
 price = row['Close'] * (1 - self.spread)
 else:
 return

# Checking minimum position size
 if signal == 'BUY' and self.capital < self.min_position_size:
 return
 elif signal == 'SELL' and self.position_value < self.min_position_size:
 return

# Making a deal
 if signal == 'BUY' and self.position <= 0:
 if self.position < 0:
# Close the short position
 self.close_position(price, timestamp, 'SHORT')

# Open a long position
 self.open_position(price, 'LONG', timestamp)
 self.last_trade_period = current_period

 elif signal == 'SELL' and self.position >= 0:
 if self.position > 0:
# Close the long position
 self.close_position(price, timestamp, 'LONG')

# Open a short position
 self.open_position(price, 'SHORT', timestamp)
 self.last_trade_period = current_period

 def open_position(self, price: float, direction: str, timestamp: datetime) -> None:
 """
Opening position with realistic conditions

 Args:
Price: Opening price (with spread-related)
direction: Position direction ('LONG' or 'SHORT')
Timetamp: Time mark
 """
 if direction == 'LONG':
# Buying: Use all available capital
 self.position = self.capital / price
 self.position_value = self.position * price
 self.capital = 0

# We're counting on a commission
 commission_cost = self.position_value * self.commission

# Recording the deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=self.position,
 direction='LONG',
 commission=commission_cost
 )
 self.trades.append(trade)

 elif direction == 'SHORT':
# Sales: Open a short position
 self.position = -self.capital / price
 self.position_value = abs(self.position) * price
 self.capital = 0

# We're counting on a commission
 commission_cost = self.position_value * self.commission

# Recording the deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=abs(self.position),
 direction='SHORT',
 commission=commission_cost
 )
 self.trades.append(trade)

 def close_position(self, price: float, timestamp: datetime, direction: str) -> None:
 """
Closing position with realistic conditions

 Args:
Price: Cost of closing position (with spread accounting)
Timetamp: Time mark
direction: closed position direction
 """
 if direction == 'LONG' and self.position > 0:
# Close the long position
 self.capital = self.position * price * (1 - self.commission)
 profit = self.capital - self.position_value

# Recording the closing deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=self.position,
 direction='CLOSE_LONG',
 profit=profit,
 commission=self.position * price * self.commission
 )
 self.trades.append(trade)

 elif direction == 'SHORT' and self.position < 0:
# Close the short position
 self.capital = -self.position * price * (1 - self.commission)
 profit = self.capital - self.position_value

# Recording the closing deal
 trade = Trade(
 timestamp=timestamp,
 price=price,
 quantity=abs(self.position),
 direction='CLOSE_SHORT',
 profit=profit,
 commission=abs(self.position) * price * self.commission
 )
 self.trades.append(trade)

# Drop the position
 self.position = 0
 self.position_value = 0
```

###2: Liquidity and slipping

**Theory:** Liquidity and slipping are factors that are much influence real trade but are often ignored in simple backstabbing; taking these factors into account is critical for achieving realistic results.

What's liquidity?
- ** Definition:** The ability to buy or sell an asset quickly without significant influence on the price
- **Factors:** Trading volume, number of participants, volatility
- **Measurement:** pre-bid-ask, market depth, time of execution

What's slipping?
- ** Definition: ** The difference between the expected price of performance and the actual price
- ** Causes:** Insufficient liquidity, large volumes, volatility
- **Tips:** Positive (benefit) and negative (unbenefit)

** Trade impact:**
- ** Decrease in profits:** Slips reduce returns
- ** Change of strategy:** May require modification of Logski
- **Manage risk: ** Need to account for liquidity in Planting
- ** Position size:** Limitations on maximum volumes

```python
def calculate_slippage(volume: float, market_volume: float, price: float,
 volatility: float = 0.02) -> float:
 """
Calculation of the slip on volume and liquidity

Slipping depends from:
- Relationship between volume of transaction and market volume
- Activability
- Time of execution
- Market depths

 Args:
Volume: The volume of our deal
Market_volume: Average market volume
Price: Current asset price
volatility: An asset &apos; s volatility (on default 2%)

 Returns:
Slip size in currency
 """
 if market_volume <= 0:
 return 0

# Volume to market volume
 volume_ratio = volume / market_volume

# Basic slipping in dependencies from volume
if volume_ratio < 0.001: # Very small volume (< 0.1%)
 base_slippage = 0.0001
elif volume_ratio < 0.01: # Small volume (0.1 % - 1%)
 base_slippage = 0.0005
elif volume_ratio < 0.05: # Average volume (1% - 5%)
 base_slippage = 0.001
elif volume_ratio < 0.1: # Large volume (5% - 10%)
 base_slippage = 0.002
else: #A very large volume (> 10%)
 base_slippage = 0.005

# Adjustment on volatility
volatility_multiplier = 1 + (volatility / 0.02) # Normalization to 2%

# Total slipping
 total_slippage = base_slippage * volatility_multiplier

 return price * total_slippage

def calculate_market_impact(volume: float, market_volume: float,
 price: float, volatility: float = 0.02) -> float:
 """
Calculation of influence to market (market impact)

Market impact is the effect of our deal on the value of an asset.
The larger the volume relative to the market, the greater the influence.

 Args:
Volume: The volume of our deal
Market_volume: Average market volume
Price: Current asset price
volatility: Volatility of an asset

 Returns:
Impact on price in currency
 """
 if market_volume <= 0:
 return 0

# Volume to market volume
 volume_ratio = volume / market_volume

# Impact coefficient (quadratic dependency)
 impact_coefficient = volume_ratio ** 1.5

# Adjustment on volatility
 volatility_multiplier = 1 + (volatility / 0.02)

# The final impact
 total_impact = impact_coefficient * volatility_multiplier * 0.001

 return price * total_impact

class LiquidityAwareBacktester(ReaListicBacktester):
 """
Becketster with liquidity and slip

This class expands ReaListicBacktester for accounting:
- Slipping in the execution of transactions
- Impact to Market (market impact)
- Liquidity restrictions
- Temporary delays
 """

 def __init__(self, initial_capital: float = 10000,
 commission: float = 0.001,
 spread: float = 0.0005,
 min_position_size: float = 100,
 min_trade_interval: int = 1,
 max_volume_ratio: float = 0.1,
 execution_delay: int = 0):
 """
Initiating a buffer with liquidity accounting

 Args:
initial_capital: seed capital
commission: Commission for the transaction
spread: spread between prices
min_position_size: Minimum entry size
min_trade_interval: Minimum transaction interval
max_volume_ratio: Maximum volume to market ratio
release_delay: Delayed performance in periods
 """
 super().__init__(initial_capital, commission, spread,
 min_position_size, min_trade_interval)
 self.max_volume_ratio = max_volume_ratio
 self.execution_delay = execution_delay
Self.pending_orders = [] # Pending execution of the warrant

 def execute_trade(self, row: pd.Series, signal: str, timestamp: datetime) -> None:
 """
Conducting bidding with liquidity

 Args:
row: Current Data Line (OHLCV)
Signal: Trade signal
Timetamp: Time mark
 """
# Processing pending warrants
 self._process_pending_orders(row, timestamp)

 if signal in ['BUY', 'SELL']:
# We're counting the deal
 if signal == 'BUY':
 volume = self.capital / row['Close']
 else: # SELL
 volume = abs(self.position) if self.position != 0 else 0

# Chucking liquidity restrictions
 if not self._check_liquidity_constraints(volume, row['Volume']):
 return

# We're counting on slipping and influencing to market
 slippage = calculate_slippage(volume, row['Volume'], row['Close'])
 market_impact = calculate_market_impact(volume, row['Volume'], row['Close'])

# Adjusting the price
 if signal == 'BUY':
 price = row['Close'] + slippage + market_impact
 else: # SELL
 price = row['Close'] - slippage - market_impact

# Creating warrant with delay
 if self.execution_delay > 0:
 self.pending_orders.append({
 'signal': signal,
 'price': price,
 'volume': volume,
 'timestamp': timestamp,
 'execution_time': len(self.equity_curve) + self.execution_delay
 })
 else:
# Immediate execution
 self._execute_immediate_trade(signal, price, timestamp)

 def _check_liquidity_constraints(self, volume: float, market_volume: float) -> bool:
 """
kheck liquidity restrictions

 Args:
Volume: The volume of our deal
Market_volume: Market volume

 Returns:
True, if restrictions are met
 """
 if market_volume <= 0:
 return False

 volume_ratio = volume / market_volume
 return volume_ratio <= self.max_volume_ratio

 def _process_pending_orders(self, row: pd.Series, timestamp: datetime) -> None:
 """
Processing of pending warrants

 Args:
row: Current data line
Timetamp: Current Time Mark
 """
 current_period = len(self.equity_curve)

# Filtering warrants ready for execution
 ready_orders = [order for order in self.pending_orders
 if order['execution_time'] <= current_period]

 for order in ready_orders:
 self._execute_immediate_trade(
 order['signal'],
 order['price'],
 order['timestamp']
 )

# Remove warrants executed
 self.pending_orders = [order for order in self.pending_orders
 if order['execution_time'] > current_period]

 def _execute_immediate_trade(self, signal: str, price: float, timestamp: datetime) -> None:
 """
Immediate execution of the transaction

 Args:
Signal: Trade signal
Price: Performance price
Timetamp: Time mark
 """
# Creating the time line with adjusted price
 temp_row = pd.Series({'Close': price})

# Making a deal through a parent's method
 super().execute_trade(temp_row, signal, timestamp)
```

♪ Visualization of results

**Theory:** Visualization of thebacksing results is critical for understanding the behaviour of the strategy.

- ** Identify pathologies** in strategy
- ** Identify problems** in Logsk of trade
- ** Equalize strategies** visually
- ** Understand the risks** through planting schedules
- ** Check stability**

**Species of visualization:**
- ** Capital curves:** Show capital growth/fall over time
- ** Graphics:** Visualize losses from peaks
- ** Interest distributions:** Show statistical properties
- ** Correlation matrices:** Analysis of asset-to-asset dependencies
- **Techal cards:** Show performance on periods

### 1. Equity Curve

**Theory:** Capital curve is the main schedule for Analysis strategy, showing the change in portfolio value over time and allowing:

- ** Assess the overall trend** - rising or falling capital
- ** Identify periods of stagnation** - when the strategy not Workinget
- ** To detect volatility** - how stable returns are
- ♪ Equalize with the bookmark ♪ - Better or worse than the market ♪

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

def plot_equity_curve(equity_curve: List[float],
 dates: List[datetime] = None,
 benchmark: List[float] = None,
 benchmark_dates: List[datetime] = None,
 title: str = "Equity Curve",
 figsize: tuple = (15, 8)) -> None:
 """
Building the capital curve with additional information

 Args:
Equity_curve: List of capital values
data: List of dates (if present)
benchmark: Curve for comparison
benchmark_dates:
Title: Graphic Heading
figsize: Graphic size
 """
 plt.figure(figsize=figsize)

# Data production
 if dates is not None:
 x_data = dates
 x_label = "Date"
 else:
 x_data = range(len(equity_curve))
 x_label = "Period"

# Main capital curve
 plt.plot(x_data, equity_curve, label='Strategy', linewidth=2, color='blue')

# Benchmark (if present)
 if benchmark is not None:
 if benchmark_dates is not None:
 plt.plot(benchmark_dates, benchmark, label='Benchmark',
 linewidth=2, alpha=0.7, color='orange')
 else:
 plt.plot(x_data[:len(benchmark)], benchmark, label='Benchmark',
 linewidth=2, alpha=0.7, color='orange')

# The initial capital line
 initial_capital = equity_curve[0]
 plt.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.5,
 label=f'Initial Capital: ${initial_capital:,.0f}')

# Formatting
 plt.title(title, fontsize=16, fontweight='bold')
 plt.xlabel(x_label, fontsize=12)
 plt.ylabel('Portfolio Value ($)', fontsize=12)
 plt.legend(fontsize=11)
 plt.grid(True, alpha=0.3)

# Formatting the axles
 if dates is not None:
 plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
 plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
 plt.xticks(rotation=45)

# Formatting the Y axis
 plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

 plt.tight_layout()
 plt.show()

def plot_equity_curve_with_metrics(equity_curve: List[float],
 metrics: Dict[str, Any],
 dates: List[datetime] = None,
 title: str = "Equity Curve with Metrics") -> None:
 """
Building the capital curve with representation of key metrics

 Args:
Equity_curve: List of capital values
metrics: dictionary with metrics
data: List of dates
Title: Graphic Heading
 """
 fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10),
 gridspec_kw={'height_ratios': [3, 1]})

# Main schedule - capital curve
 if dates is not None:
 ax1.plot(dates, equity_curve, linewidth=2, color='blue')
 else:
 ax1.plot(equity_curve, linewidth=2, color='blue')

 ax1.set_title(title, fontsize=16, fontweight='bold')
 ax1.set_ylabel('Portfolio Value ($)', fontsize=12)
 ax1.grid(True, alpha=0.3)
 ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Add metrics on graph
 metrics_text = f"""
 Total Return: {metrics.get('total_return', 0):.2%}
 Annual Return: {metrics.get('annual_return', 0):.2%}
 Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}
 Max Drawdown: {metrics.get('max_drawdown', 0):.2%}
 Win Rate: {metrics.get('win_rate', 0):.2%}
 """
 ax1.text(0.02, 0.98, metrics_text, transform=ax1.transAxes,
 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Lower schedule - drops
 equity_series = pd.Series(equity_curve)
 running_max = equity_series.expanding().max()
 drawdown = (equity_series - running_max) / running_max

 if dates is not None:
 ax2.fill_between(dates, drawdown, 0, alpha=0.3, color='red')
 ax2.plot(dates, drawdown, color='red', linewidth=1)
 else:
 ax2.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
 ax2.plot(drawdown, color='red', linewidth=1)

 ax2.set_title('Drawdown', fontsize=14)
 ax2.set_xlabel('Time', fontsize=12)
 ax2.set_ylabel('Drawdown %', fontsize=12)
 ax2.grid(True, alpha=0.3)
 ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

 plt.tight_layout()
 plt.show()
```

### 2. Drawdown Chart

**Theory:** The planting schedule shows maximum losses from peak values. This is a critical schedule for understanding the risks of the strategy:

- ** Maximum draught** - worst loss from peak
- ** The length of the landing** - how long the strategy recovers
- ** The frequency of loss** - how often the loss occurs
- ** Recovery** - speed of return to peak values

```python
def plot_drawdown_Analysis(equity_curve: List[float],
 dates: List[datetime] = None,
 title: str = "Drawdown Analysis") -> None:
 """
Integrated sediment analysis

 Args:
Equity_curve: List of capital values
data: List of dates
Title: Graphic Heading
 """
 fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))

 equity_series = pd.Series(equity_curve)
 running_max = equity_series.expanding().max()
 drawdown = (equity_series - running_max) / running_max

# Graph 1: Capital curve with peaks
 if dates is not None:
 ax1.plot(dates, equity_curve, label='Portfolio Value', linewidth=2, color='blue')
 ax1.plot(dates, running_max, label='Running Maximum', linewidth=1,
 color='green', linestyle='--', alpha=0.7)
 else:
 ax1.plot(equity_curve, label='Portfolio Value', linewidth=2, color='blue')
 ax1.plot(running_max, label='Running Maximum', linewidth=1,
 color='green', linestyle='--', alpha=0.7)

 ax1.set_title(f'{title} - Portfolio Value', fontsize=14)
 ax1.set_ylabel('Value ($)', fontsize=12)
 ax1.legend()
 ax1.grid(True, alpha=0.3)
 ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

# Graph 2: Slows
 if dates is not None:
 ax2.fill_between(dates, drawdown, 0, alpha=0.3, color='red')
 ax2.plot(dates, drawdown, color='red', linewidth=1)
 else:
 ax2.fill_between(range(len(drawdown)), drawdown, 0, alpha=0.3, color='red')
 ax2.plot(drawdown, color='red', linewidth=1)

 ax2.set_title('Drawdown', fontsize=14)
 ax2.set_ylabel('Drawdown %', fontsize=12)
 ax2.grid(True, alpha=0.3)
 ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

# Graph 3: Distribution
drawdown_clean = drawdown[drawdown < 0] # Only negative prostheses
 if len(drawdown_clean) > 0:
 ax3.hist(drawdown_clean, bins=30, alpha=0.7, color='red', density=True)
 ax3.axvline(drawdown_clean.mean(), color='black', linestyle='--',
 label=f'Mean: {drawdown_clean.mean():.2%}')
 ax3.axvline(drawdown_clean.min(), color='darkred', linestyle='--',
 label=f'Min: {drawdown_clean.min():.2%}')

 ax3.set_title('Drawdown Distribution', fontsize=14)
 ax3.set_xlabel('Drawdown %', fontsize=12)
 ax3.set_ylabel('Density', fontsize=12)
 ax3.legend()
 ax3.grid(True, alpha=0.3)
 ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

 plt.tight_layout()
 plt.show()

def plot_rolling_metrics(equity_curve: List[float],
 window: int = 252,
 dates: List[datetime] = None) -> None:
 """
Building sliding metrics

 Args:
Equity_curve: List of capital values
Windows: Window size for calculation of metric
data: List of dates
 """
 equity_series = pd.Series(equity_curve)
 returns = equity_series.pct_change().dropna()

# Sliding metrics
Rolling_returns = returns.rolling.mean() * 252 # Annual return
Rolling_vol = returns.rolling.std() * np.sqrt(252) # Annual volatility
Rolling_sharpe = Rolling_returns / Rolling_vol # Sharpe ratio

 fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 10))

# Graph 1: Rolling returns
 if dates is not None:
 ax1.plot(dates[1:], rolling_returns, label='Rolling Annual Return', linewidth=2)
 else:
 ax1.plot(rolling_returns, label='Rolling Annual Return', linewidth=2)

 ax1.set_title('Rolling Annual Return', fontsize=14)
 ax1.set_ylabel('Return', fontsize=12)
 ax1.legend()
 ax1.grid(True, alpha=0.3)
 ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

# Graph 2: Flipping volatility
 if dates is not None:
 ax2.plot(dates[1:], rolling_vol, label='Rolling Volatility', linewidth=2, color='orange')
 else:
 ax2.plot(rolling_vol, label='Rolling Volatility', linewidth=2, color='orange')

 ax2.set_title('Rolling Volatility', fontsize=14)
 ax2.set_ylabel('Volatility', fontsize=12)
 ax2.legend()
 ax2.grid(True, alpha=0.3)
 ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

# Graph 3: Sharpe Ratio Rolling
 if dates is not None:
 ax3.plot(dates[1:], rolling_sharpe, label='Rolling Sharpe Ratio', linewidth=2, color='green')
 else:
 ax3.plot(rolling_sharpe, label='Rolling Sharpe Ratio', linewidth=2, color='green')

 ax3.set_title('Rolling Sharpe Ratio', fontsize=14)
 ax3.set_xlabel('Time', fontsize=12)
 ax3.set_ylabel('Sharpe Ratio', fontsize=12)
 ax3.legend()
 ax3.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()
```

### 3. Returns Distribution

**Theory:** Analysis of the distribution of returns helps understand the statistical characteristics of the strategy:

- ** Nominal distribution** - does the return correspond to the normal distribution
- ** Asymmetry** - trend towards positive or negative results
- **Excess** - frequency of extreme events
- **Wheats of distribution** - Probability of high loss or profit

```python
from scipy import stats
import seaborn as sns

def plot_returns_Analysis(returns: List[float],
 title: str = "Returns Analysis") -> None:
 """
Integrated analysis of the distribution of returns

 Args:
Returns: Income list
Title: Graphic Heading
 """
 returns_series = pd.Series(returns)

 fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Graph 1: Histogram with normal distribution
 ax1.hist(returns_series, bins=50, alpha=0.7, density=True,
 label='Returns', color='skyblue', edgecolor='black')

# Normal distribution for comparison
 mu, sigma = returns_series.mean(), returns_series.std()
 x = np.linspace(returns_series.min(), returns_series.max(), 100)
 normal_dist = stats.norm.pdf(x, mu, sigma)
 ax1.plot(x, normal_dist, 'r-', linewidth=2, label='Normal Distribution')

 ax1.set_title('Returns Distribution', fontsize=14)
 ax1.set_xlabel('Returns', fontsize=12)
 ax1.set_ylabel('Density', fontsize=12)
 ax1.legend()
 ax1.grid(True, alpha=0.3)

# Graph 2: Q-Q table for normality check
 stats.probplot(returns_series, dist="norm", plot=ax2)
 ax2.set_title('Q-Q Plot (Normal Distribution)', fontsize=14)
 ax2.grid(True, alpha=0.3)

# Graph 3: Box Platform
 ax3.boxplot(returns_series, vert=True)
 ax3.set_title('Box Plot', fontsize=14)
 ax3.set_ylabel('Returns', fontsize=12)
 ax3.grid(True, alpha=0.3)

# Graph 4: Cumulative function distribution
 sorted_returns = np.sort(returns_series)
 cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
 ax4.plot(sorted_returns, cumulative, linewidth=2, label='Empirical CDF')

# Theoretical CDF for normal distribution
 normal_cdf = stats.norm.cdf(sorted_returns, mu, sigma)
 ax4.plot(sorted_returns, normal_cdf, 'r--', linewidth=2, label='Normal CDF')

 ax4.set_title('Cumulative Distribution Function', fontsize=14)
 ax4.set_xlabel('Returns', fontsize=12)
 ax4.set_ylabel('Cumulative Probability', fontsize=12)
 ax4.legend()
 ax4.grid(True, alpha=0.3)

 plt.suptitle(title, fontsize=16, fontweight='bold')
 plt.tight_layout()
 plt.show()

# Bringing statistics out
 print(f"\n=== Returns Statistics ===")
 print(f"Count: {len(returns_series)}")
 print(f"Mean: {returns_series.mean():.4f}")
 print(f"Std: {returns_series.std():.4f}")
 print(f"Skewness: {returns_series.skew():.4f}")
 print(f"Kurtosis: {returns_series.kurtosis():.4f}")
 print(f"Min: {returns_series.min():.4f}")
 print(f"Max: {returns_series.max():.4f}")

# Test on normality
 shapiro_stat, shapiro_p = stats.shapiro(returns_series)
 print(f"\nShapiro-Wilk Test:")
 print(f"Statistic: {shapiro_stat:.4f}")
 print(f"P-value: {shapiro_p:.4f}")
 print(f"Normal distribution: {'Yes' if shapiro_p > 0.05 else 'No'}")

def plot_risk_return_scatter(returns: List[float],
 window: int = 252,
 title: str = "Risk-Return Analysis") -> None:
 """
Risk-income analysis

 Args:
Returns: Income list
Windows: Window size for calculation
Title: Graphic Heading
 """
 returns_series = pd.Series(returns)

# Sliding metrics
 rolling_returns = returns_series.rolling(window).mean() * 252
 rolling_vol = returns_series.rolling(window).std() * np.sqrt(252)

# Remove NaN values
 valid_data = pd.dataFrame({
 'returns': rolling_returns,
 'volatility': rolling_vol
 }).dropna()

 plt.figure(figsize=(12, 8))

 # Scatter plot
 scatter = plt.scatter(valid_data['volatility'], valid_data['returns'],
 c=range(len(valid_data)), cmap='viridis', alpha=0.6)

# Add a color scale
 cbar = plt.colorbar(scatter)
 cbar.set_label('Time', fontsize=12)

# Permanent Sharpe line
 sharpe_ratios = [0.5, 1.0, 1.5, 2.0]
 x_vol = np.linspace(valid_data['volatility'].min(), valid_data['volatility'].max(), 100)

 for sr in sharpe_ratios:
 y_return = sr * x_vol
 plt.plot(x_vol, y_return, '--', alpha=0.7,
 label=f'Sharpe = {sr}')

 plt.xlabel('Volatility (Annualized)', fontsize=12)
 plt.ylabel('Return (Annualized)', fontsize=12)
 plt.title(title, fontsize=14, fontweight='bold')
 plt.legend()
 plt.grid(True, alpha=0.3)

# Formatting the axles
 plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
 plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))

 plt.tight_layout()
 plt.show()
```

## Practical example

**Theory:** The complete buffering includes all stages: from basic testing to advanced Analysis. This example shows how to combine all the techniques studied for an integrated assessment of the strategy.

**Footback tanks:**
1. ** Basic back-up** - main evaluation of performance
2. **Walk-Forward analysis** - heck stability in time
3. **Monte Carlo simulation** - uncertainty assessment
4. **Bootstrap Analysis** - Statistical validation
5. ** Visualization** - graphic presentation of results
6. **Report** - summary of all metrics and conclusions

```python
class CompleteBacktest:
 """
Class for the full strategy back-up

Brings together all the methhods Analisis:
- Basic buffering
- Walk-Forward analysis
- Monte Carlo simulation
- Bootstrap analysis
Visualization of results
 """

 def __init__(self, data: pd.dataFrame, strategy,
 initial_capital: float = 10000,
 commission: float = 0.001,
 spread: float = 0.0005):
 """
Initiating full buffering

 Args:
Data: Historical data (OHLCV)
strategy: Purpose
initial_capital: seed capital
commission: Commission for the transaction
spread: spread between prices
 """
 self.data = data
 self.strategy = strategy
 self.initial_capital = initial_capital
 self.commission = commission
 self.spread = spread

# Results of Analysis
 self.basic_results = None
 self.wf_results = None
 self.mc_results = None
 self.bootstrap_results = None

 def run_complete_Analysis(self,
 wf_train_period: int = 252,
 wf_test_period: int = 63,
 mc_simulations: int = 1000,
 bootstrap_samples: int = 1000,
 bootstrap_block_size: int = 20) -> Dict[str, Any]:
 """
Launch full Analysis strategy

 Args:
wf_training_period: Learning period for Walk-Forward
wf_test_period: Test period for Walk-Forward
mc_simulations: Number of Monte Carlo simulations
Bootstrap_samples: Number of Bootstrap samples
Bootstrap_lock_size: Size of blocks for Bootstrap

 Returns:
Vocabulary with all results
 """
 print("=" * 60)
("Launch of the Full BECTESTING STRATEGY")
 print("=" * 60)

♪ 1 ♪ Basic buffering ♪
"Prent("\n1. Basic backting...")
 self._run_basic_backtest()

# 2. Walk-Forward analysis
Print("\n2. Walk-Forward analysis...")
 self._run_walk_forward_Analysis(wf_train_period, wf_test_period)

# 3. Monte Carlo simulation
Print("\n3.Monte Carlo simulation...")
 self._run_monte_carlo_Analysis(mc_simulations)

# 4. Bootstrap analysis
"spint("\n4. Bootstrap analysis...")
 self._run_bootstrap_Analysis(bootstrap_samples, bootstrap_block_size)

# 5. Visualization
Print("\n5. creative graphs...")
 self._create_visualizations()

 # 6. Report
"Prent("\n6. "Report generation...")
 self._generate_Report()

 return self._compile_results()

 def _run_basic_backtest(self) -> None:
""""""""""""""""""""""
 backtester = LiquidityAwareBacktester(
 initial_capital=self.initial_capital,
 commission=self.commission,
 spread=self.spread
 )

 self.basic_results = backtester.run_backtest(self.data, self.strategy)
(pint(f" * baseback completed")
Print(f) \\\\\\en(backtester.trades}}transactions}
total return: {self.basic_effects['total_return']:2%})

 def _run_walk_forward_Analysis(self, train_period: int, test_period: int) -> None:
"The Walk-Forward Anallysis"
 self.wf_results = walk_forward_Analysis(
 self.data, self.strategy, train_period, test_period
 )
 wf_Analysis = analyze_walk_forward_results(self.wf_results)
print(f" ♪ Walk-Forward analysis completed")
prent(f" ♪ ObWorkingno {len(self.wf_results)} periods")
pint(f" ♪ average return: {wf_Analisis['avg_return']:2%}}

 def _run_monte_carlo_Analysis(self, n_simulations: int) -> None:
♪ "The Monte Carlo Analysis performance" ♪
 self.mc_results = monte_carlo_simulation(
 self.data, self.strategy, n_simulations
 )
 mc_Analysis = analyze_monte_carlo_results(self.mc_results)
"spint(f" ♪ Monte Carlo simulation complete")
Print(f" ) Implemented {len(self.mc_results)} simulations}
print(f" ) Probability of profits: {mc_Analisis['probilities']['positive_return']:2%}})

 def _run_bootstrap_Analysis(self, n_bootstrap: int, block_size: int) -> None:
""The Bootstrap Analysis""
 self.bootstrap_results = bootstrap_Analysis(
 self.data, self.strategy, n_bootstrap, block_size
 )
 bootstrap_Analysis = analyze_bootstrap_results(self.bootstrap_results)
Print(f" ♪ Bootstrap analysis completed")
Print(f" \\\\len(self.bootstrap_results}} Sample completed}
"pint(f)" ♪ Trust rate of return:"
 f"{bootstrap_Analysis['return_ci']['lower']:.2%} - "
 f"{bootstrap_Analysis['return_ci']['upper']:.2%}")

 def _create_visualizations(self) -> None:
""create all graphs""
# Basic graphs
 plot_equity_curve_with_metrics(
 self.basic_results.get('equity_curve', []),
 self.basic_results
 )

 plot_drawdown_Analysis(
 self.basic_results.get('equity_curve', [])
 )

 if self.basic_results.get('daily_returns'):
 plot_returns_Analysis(self.basic_results['daily_returns'])
 plot_risk_return_scatter(self.basic_results['daily_returns'])

# Walk-Forward graphs
 if self.wf_results:
 self._plot_walk_forward_results()

# Monte carlo graphs
 if self.mc_results:
 self._plot_monte_carlo_results()

 def _plot_walk_forward_results(self) -> None:
"The Walk-Forward Anallysis Graphics."
 wf_returns = [r['metrics']['total_return'] for r in self.wf_results]
 wf_periods = [r['period'] for r in self.wf_results]

 plt.figure(figsize=(15, 6))
 plt.plot(wf_periods, wf_returns, 'o-', linewidth=2, markersize=6)
 plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
 plt.title('Walk-Forward Analysis - Returns by Period', fontsize=14)
 plt.xlabel('Period', fontsize=12)
 plt.ylabel('Return', fontsize=12)
 plt.grid(True, alpha=0.3)
 plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.1%}'))
 plt.tight_layout()
 plt.show()

 def _plot_monte_carlo_results(self) -> None:
"Monte Carlo Analysis Graphics."
 mc_returns = [r['metrics']['total_return'] for r in self.mc_results]

 plt.figure(figsize=(12, 8))

# The income hytogram
 plt.subplot(2, 2, 1)
 plt.hist(mc_returns, bins=50, alpha=0.7, density=True)
 plt.axvline(np.mean(mc_returns), color='red', linestyle='--',
 label=f'Mean: {np.mean(mc_returns):.2%}')
 plt.title('Monte Carlo Returns Distribution')
 plt.xlabel('Return')
 plt.ylabel('Density')
 plt.legend()
 plt.grid(True, alpha=0.3)

# Cumulative finance distribution
 plt.subplot(2, 2, 2)
 sorted_returns = np.sort(mc_returns)
 cumulative = np.arange(1, len(sorted_returns) + 1) / len(sorted_returns)
 plt.plot(sorted_returns, cumulative, linewidth=2)
 plt.title('Cumulative Distribution Function')
 plt.xlabel('Return')
 plt.ylabel('Cumulative Probability')
 plt.grid(True, alpha=0.3)

# temporary series of returns
 plt.subplot(2, 2, 3)
plt.plot(mc_returns[:100], alpha=0.7) # Showing the first 100
 plt.title('Monte Carlo Returns (First 100)')
 plt.xlabel('Simulation')
 plt.ylabel('Return')
 plt.grid(True, alpha=0.3)

 # Box plot
 plt.subplot(2, 2, 4)
 plt.boxplot(mc_returns)
 plt.title('Monte Carlo Returns Box Plot')
 plt.ylabel('Return')
 plt.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

 def _generate_Report(self) -> None:
"""""""""""""""""""""""
 print("\n" + "=" * 60)
"Report on the results of the BECTESTING"
 print("=" * 60)

# Basic metrics
("\n\\\\\\\\\\}BASIC METHICS:")
total return: {self.basic_results['total_return']:2%})
pprint(f" Annual rate of return: {self.basic_results['annual_return']:2%}})
(f" Volatility: {self.basic_results['volatility': 2 per cent}")
 print(f" Sharpe Ratio: {self.basic_results['sharpe_ratio']:.2f}")
peak(f" Maximum draught: {self.basic_results['max_drawdown']:2%}})
 print(f" Win Rate: {self.basic_results['win_rate']:.2%}")
 print(f" Profit Factor: {self.basic_results['profit_factor']:.2f}")

# Walk-Forward analysis
 if self.wf_results:
 wf_Analysis = analyze_walk_forward_results(self.wf_results)
Print(f)(\n\\\\\\}WALK-FORWARD ANALYSIS:)
 print(f" periods: {wf_Analysis['total_periods']}")
average return: {wf_Analisis['avg_return']:2%})
standard deviation: {wf_Analisis['std_return']:2%}})
pint(f" Positive periods: {wf_Analisis['positive_periods_pct']:2%})
Spring(f" Stability coefficient: {wf_Analisis['consistency_score']:2f}})

# Monte Carlo analysis
 if self.mc_results:
 mc_Analysis = analyze_monte_carlo_results(self.mc_results)
Print(f)(\n\\\\\\Montecarlo ANALYS:")
(pint(f" Simulations: {mc_Analisis['n_simulations'}})
average return: {mc_Anallysis['return_stats']['mean':2%}})
prent(f" Probability of profits: {mc_Analisis['probilities']['positive_return']: 2 per cent})
 print(f" VaR (95%): {mc_Analysis['var_cvar']['var_95']:.2%}")
 print(f" CVaR (95%): {mc_Analysis['var_cvar']['cvar_95']:.2%}")

# Bootstrap analysis
 if self.bootstrap_results:
 bootstrap_Analysis = analyze_bootstrap_results(self.bootstrap_results)
(f'n'\\\\ boOTSTRAP ANALYSIS:")
print(f" Sample: {bootstrap_analysis['n_bootstrap'}})
"print(f) "Confidence rate of return:"
 f"{bootstrap_Analysis['return_ci']['lower']:.2%} - "
 f"{bootstrap_Analysis['return_ci']['upper']:.2%}")
"print(f) "Statistical value of returns:"
(f) {'Yes' if bootstrap_Analisis['significance'] ['return_significant'] else 'No'})

 def _compile_results(self) -> Dict[str, Any]:
"Compilation of all results."
 return {
 'basic_results': self.basic_results,
 'walk_forward_results': self.wf_results,
 'monte_carlo_results': self.mc_results,
 'bootstrap_results': self.bootstrap_results,
 'summary': {
 'total_return': self.basic_results['total_return'],
 'sharpe_ratio': self.basic_results['sharpe_ratio'],
 'max_drawdown': self.basic_results['max_drawdown'],
 'win_rate': self.basic_results['win_rate']
 }
 }

# Example of use
def run_complete_backtest_example():
 """
example of full strategy buffering

This example shows how to use ComputerBacktest
To implement an integrated Trade Strategy Analysis.
 """
# Creating a simple strategy for example
 class SimpleMovingAverageStrategy:
 def __init__(self, short_window=20, long_window=50):
 self.short_window = short_window
 self.long_window = long_window
 self.short_ma = None
 self.long_ma = None

 def get_signal(self, data):
 if len(data) < self.long_window:
 return 'HOLD'

# We're counting moving average
 short_ma = data['Close'].rolling(self.short_window).mean().iloc[-1]
 long_ma = data['Close'].rolling(self.long_window).mean().iloc[-1]

# A simple crossing strategy
 if short_ma > long_ma:
 return 'BUY'
 elif short_ma < long_ma:
 return 'SELL'
 else:
 return 'HOLD'

# Generate testy data
 np.random.seed(42)
 dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
 prices = 100 * np.cumprod(1 + np.random.normal(0.0005, 0.02, len(dates)))

 data = pd.dataFrame({
 'Open': prices * (1 + np.random.normal(0, 0.001, len(dates))),
 'High': prices * (1 + np.abs(np.random.normal(0, 0.01, len(dates)))),
 'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, len(dates)))),
 'Close': prices,
 'Volume': np.random.randint(1000, 10000, len(dates))
 }, index=dates)

# Creating strategy
 strategy = SimpleMovingAverageStrategy()

# Launcha full analysis
 backtest = CompleteBacktest(data, strategy)
 results = backtest.run_complete_Analysis()

 return results

# Launch example
if __name__ == "__main__":
 results = run_complete_backtest_example()
```

## Next steps

After studying the bactering, go to:

- **[07_walk_forward_Analisis.md](07_walk_forward_Anallysis.md)** - Detailed study of Walk-Forward Analysis
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - In-depth study of Monte Carlo simulation
- **[09_risk_Management.md](09_risk_Management.md)** - Risk Management in Trade Strategies
- **[10_Porthfolio_optimization.md](10_Porthfolio_optimization.md)** - Optimizing the portfolio of strategies

## Key findings

♪ ♪ Basic principles ♪

1. ** Avoid look-ahead bias** - Use only historical data
2. ** Consider realistic** - commissions, spreads, liquidity, slipping
3. ** Check stability** - Use Walk-Forward analysis
4. ** Assess uncertainty** - apply Monte Carlo simulation
5. **Valide statistically** - Use Bootstrap analysis

### ♪ quality metrics

- ** Income:** Total, annual, average
- **Risk:** Volatility, maximum draught, VaR
- ** Effectiveness:** Sharpe ratio, Sortino ratio, Kalmar ratio
- **Stability:** Win rent, profit factor, recovery factor

### ♪ Typical errors

- **Look-ahead bis** - use of future information
- **Survivorship bias** - neglect of "dead" assets
- **Overfitting** - Retraining on historical data
- ** Ignoring transaction costs** - unrealistic results
- ** Risk underestimation** - focus on return only

♪# ♪ Tools

- ** Basic Baxter** - for simple testing
- **Realistic backtister** - with transaction costs
- **Bactester with liquidity** - with slips
- **Walk-Forward analysis** - for stability testing
- **Monte carlo simulation** - for uncertainty assessment
- **Bootstrap Analysis** - for statistical validation

### ♪ Visualization

- ** Capital curves** - for estimation of the overall trend
- ** Graphics** - for risk understanding
- ** Interest distribution** - for statistical Analysis
- ** Sliding metrics** - for Analysis stability

---

♪ ♪ Practical recommendations

### For starters

1. Start with a simple backuper
2. Study the main metrics
3. Learn to interpret graphs
4. Progressively add realism

### for advanced

1. Use all methhods Analysis
2. Create your own metrics
3. Adapt the code to your needs
4. Conduct A/B testing of strategies

### For professionals

1. Integration with real data
2. Automatically process the Analysis
3. Create dashboards for Monitoring
4. Develop allernet systems

---

♪ ♪ A good buffering is just a high return, and ♪ a stable, realistic, and reproducible ♪ ♪ a return that is confirmed by multiple Analysis methods!
