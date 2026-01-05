# 07. ♪ Walk-Forward analysis

**Goal:** Learn to conduct a Walk-Forward analysis for verifying the stability of trade policies.

♪ What's a Walk-Forward analysis?

**Theory:** Walk-Forward analysis is an advanced method of testing trade strategies that simulates real terms of trade. In contrast to a simple back-up, it takes into account the need to retrain the model on new data, making it more realistic and reliable.

**Walk-Forward Analysis** is a method of testing trade strategies that simulates real trade, where the model is re-trained on new data as they become available.

### The mathematical basis of Walk-Forward Anallysis

**Theory:** Walk-Forward analysis is based on the principle of temporal data separation, where each test period uses only previous data for learning. This prevents "look-ahead bis" and provides a realistic assessment of performance.

** Mathematic formula:**

```
for period t:
- Training data: D[training_start : train_end]
- testes data: D[test_start : test_end]
- Condition: test_start = train_end
```

**key principles:**
1. ** Time sequence:** data processed in chronoLogsch order
2. **retraining:** The model is re-trained for each new period
3. ** Reality:** Simulates real terms of trade
4. **Stability:** Checks the strategy &apos; s resilience to change

**Why Walk-Forward analysis is critical for financial systems:**
- ** Reality:** Simulates real terms of trade
- **Stability:** Checks out how the Workinget strategy is on new data.
- ** Adaptation:** Assesses the ability of the model to adapt to changes
- **Robity:** Identify problems not visible in simple buffering.

### Why do you need a Walk-Forward analysis?

**Theory:** Walk-Forward analysis addresses the fundamental problems of traditional bactering associated with re-education and unrealisticity. It provides a more honest assessment of performance strategy.

- ** Reality** - mimics real trade
- What's important is:** in real trade, the model should be retrained on new data
- ** Plus:** More honest assessment of performance, realistic results
- **Disadvantages:** More complex implementation requires more computing resources

- **check stability** - like the Workinget strategy on new data
- What's important is:** The strategy has to be stable on new data
- ** Plus:** Identification of stability issues, assessment of long-term performance
- **Disadvantages:** May show worse results than simple bactering

- ** Avoiding retraining** - prevents optimization on historical data
- # Why does it matter? # Retraining leads to unrealistic results?
- ** Plus:** Fairer assessment, risk reduction
- **Disadvantages:** May show worse results, requires more data

- ** Adaptation assessment** - how the model adapts to changes
- What's important is that markets are constantly changing, the model has to adapt.
- **plus: ** Assessment of adaptive capacity, identification of adaptation problems
- **Disadvantages:**Complicity of assessment of adaptiveness, need for an adaptive metric

** Additional benefits of Walk-Forward Analysis:**
** Time Structure: ** Reflects the time structure of the data
- ** Degradation:** Degradation performance over time
- ** Market conditions:** Allows analysis of performance in different market conditions
- ** Parametric stability:** Assesss the stability of the strategy parameters

## The Walk-Forward Anallysis Principles

**Theory:** Walk-Forward analysis is based on several key principles that make it effective and realistic.

♪##1 ♪ Data sharing

**Theory:** The correct data separation is the basis of Walk-Forward Analysis. data should be divided into learning and test periods in such a way as to simulate the real terms of trade.

**Why the correct division of data is critical:**
- ** TimeStructure:** Financial data have a temporary dependency, and breaking timeLogsy can lead to unrealistic results
- ** Reality: ** in real trade we can use future information for current decision-making
- ** Prevention of leaks:** Strict temporary separation prevents the use of information from the future
- **Stability:** Provides an honest assessment of the ability of the Working on New Data strategy

** Mathematical rationale for separation:**

```
Let T = {t1, t2, ..., tn} - time tags
for each test period i:
- Learning period: [t_start_i, t_training_end_i]
- test period: [t_test_start_i, t_test_end_i]
- Condition: t_test_start_i = t_training_end_i + 1 (strict separation)
```

** Plus the right split:**
- Realistic evaluation of performance strategy
- Prevention of data leaks (look-ahead bis)
- Accounting for the statistical structure of financial data
- Stable and reproducible results
- Meeting the realities of trade

**Minuses of correct separation:**
- The difficulty of implementing the algorithm
- Need for more historical data
Possible reduction performance compared to unrealistic methods
- Complexity of Settings (window dimensions, steps)
- Higher computing requirements
**Functions of section creation:**
This function provides an algorithm for creating temporary sections for Walk-Forward Analysis. It creates a sequence of learning and testes periods where each test period follows immediately after the respective learning period.

**parameters functions:**
- `training_size=252': The size of the training window (252 trade days ~ 1 year)
- `test_size=63': Size of test window (63 trade days ~ 3 months)
- `step_size=21': Step of the window shift (21 trade day ~ 1 month)

**Algorithm:**
1. Start with the first data index
2. Creating a fixed-length learning period
3. Creating test period immediately after the training period
4. Move on step_size and repeat process
5. Continue until we have exhausted the data

♪ Why exactly are these parameters: ♪
- **252 learning days:** sufficient for model learning, but not too much for obsolescence
**63 days of testing:** Enough for statistically significant results
- **21 days step:** Balance between retraining and stability

```python
# Necessary imports for Walk-Forward Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
import warnings
from scipy import stats
Import yfinance as yf # for downloading real data

# Configuring matplotlib for better display
plt.style.Use('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def create_walk_forward_splits(data: pd.dataFrame,
 train_size: int = 252,
 test_size: int = 63,
 step_size: int = 21) -> List[Dict[str, Any]]:
 """
"Create Walk-Forward" sections for Time Series Analysis.

This function creates a sequence of learning and testes perios
Each test period should be followed by:
immediately after the relevant learning period, which simulates
Real terms of trade.

 Args:
Data (pd.dataFrame): time series with index data
Train_size (int): The size of the learning window in days (on default 252)
test_size (int): Test window size in days (on default 63)
step_size (int): Step of window shift in days (on default 21)

 Returns:
List[Dict]: List dictionaries with information on each section

 Raises:
ValueError: If data are not sufficient to create at least one section

 Example:
 >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
 >>> splits = create_walk_forward_splits(data, train_size=100, test_size=20)
>> prent(f) Created {len(splits)} sections")
 """

# Checking data adequacy
 min_required = train_size + test_size
 if len(data) < min_required:
Raise ValueError(f"Insufficient data. Minimum {min_required} records required, received {len(data)})

 splits = []
 start_idx = 0

# Creating sections to exhaust
 while start_idx + train_size + test_size <= len(data):
# Learning period (strength to test)
 train_start = start_idx
 train_end = start_idx + train_size

# Testsy period (after the trainer)
test_start = train_end # Critical: no break!
 test_end = train_end + test_size

# Creating dictionary with section information
 split_info = {
 'train_start': train_start,
 'train_end': train_end,
 'test_start': test_start,
 'test_end': test_end,
 'train_data': data.iloc[train_start:train_end].copy(),
 'test_data': data.iloc[test_start:test_end].copy(),
 'train_dates': (data.index[train_start], data.index[train_end-1]),
 'test_dates': (data.index[test_start], data.index[test_end-1])
 }

 splits.append(split_info)

# Move on step_size for next section
 start_idx += step_size

(f) Created {len(splits}Walk-Forward sections")
"print(f" First section: education {splits[0]['training_data' [0]} - {splits[0]['training_data'][1]},"
f "test {splits[0]['test_data' [0]} - {splits[0]['test_data'[1]}}")
"Print(f)" Final section: education {splits[1]['training_data'[0]} - {splits[1]['training_data'][1]},"
f "test {splits[1]['test_data' [0]} - {splits[1]['test_data'[1]}}")

 return splits
```

### 2. Structure Analysis

**WalkForward Analizer:**
This class is the central component of the Walk-Forward Anallysis. It encapsulates the entire Logs of Analysis, including creation sections, model training, testing and results analysis.

**architecture class:**
1. **Initiation:** installation of Analysis parameters
2. **Launch Analysis:** Basic method for conducting Walk-Forward testing
3. ** Analysis of results:** Statistical analysis of results

** Key principles of implementation:**
- **Incapsulation:** All Logsca Analysis is encapsulated in one class
- ** Reuse:** Class can Work with any strategy
- ** Extension:** It's easy to add new metrics and meths Analisis
- ** Traceability:** Full tracking of all phases of Analysis

```python
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import warnings

class TradingStrategy(ABC):
"Abstruction Basic Class for Trade Strategies"

 @abstractmethod
 def train(self, data: pd.dataFrame) -> None:
"Learning Strategy on Historical Data"
 pass

 @abstractmethod
 def predict(self, data: pd.dataFrame) -> pd.Series:
"Generation of Trade Signs."
 pass

 @abstractmethod
 def get_name(self) -> str:
"Returns the name of the strategy."
 pass

class SimpleMovingAverageStrategy(TradingStrategy):
"Simple strategy on bases moving medium."

 def __init__(self, short_window: int = 20, long_window: int = 50):
 self.short_window = short_window
 self.long_window = long_window
 self.short_ma = None
 self.long_ma = None
 self.is_trained = False

 def train(self, data: pd.dataFrame) -> None:
"""""" (in this case, simply calculation of parameters)""
 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")

 self.short_ma = data['close'].rolling(window=self.short_window).mean()
 self.long_ma = data['close'].rolling(window=self.long_window).mean()
 self.is_trained = True

 def predict(self, data: pd.dataFrame) -> pd.Series:
"Generation of Trade Signs."
 if not self.is_trained:
Raise ValueError.

 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")

# We're counting moving averages for new data
 short_ma = data['close'].rolling(window=self.short_window).mean()
 long_ma = data['close'].rolling(window=self.long_window).mean()

# Generate signals: 1 = purchase, -1 = sale, 0 = retention
 signals = pd.Series(0, index=data.index)

# Buying signal: Short MA crosses long MA from the bottom up
 buy_signal = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))

# Sales signal: Short MA crosses long MA from top down
 sell_signal = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))

 signals[buy_signal] = 1
 signals[sell_signal] = -1

 return signals

 def get_name(self) -> str:
 return f"SMA_{self.short_window}_{self.long_window}"

class Backtester:
"Class for Trade Strategy Beckets."

 def __init__(self, initial_capital: float = 100000.0, commission: float = 0.001):
 self.initial_capital = initial_capital
 self.commission = commission

 def run_backtest(self, data: pd.dataFrame, strategy: TradingStrategy) -> Dict[str, float]:
 """
Launchbacking strategy

 Args:
Data: data for testing
strategy: Trade strategy trained

 Returns:
Vocabulary with metrics
 """
 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")

# Generate trade signals
 signals = strategy.predict(data)

# We're calculating returns
 returns = data['close'].pct_change()

# Calculate strategic returns
strategy_returns = signals.shift(1) * returns # Move signals on 1 period

# Take into account the commission
 position_changes = signals.diff().abs()
 strategy_returns -= position_changes * self.commission

# Remove NaN values
 strategy_returns = strategy_returns.dropna()

 if len(strategy_returns) == 0:
 return {
 'total_return': 0.0,
 'sharpe_ratio': 0.0,
 'max_drawdown': 0.0,
 'win_rate': 0.0,
 'total_trades': 0
 }

# Computing cumulative returns
 cumulative_returns = (1 + strategy_returns).cumprod()

# Basic metrics
 total_return = cumulative_returns.iloc[-1] - 1

# Sharpe Ratio
 sharpe_ratio = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0

# Maximum tarmac
 rolling_max = cumulative_returns.expanding().max()
 drawdowns = (cumulative_returns - rolling_max) / rolling_max
 max_drawdown = drawdowns.min()

# Percentage of winning transactions
 winning_trades = strategy_returns[strategy_returns > 0]
 total_trades = len(strategy_returns[strategy_returns != 0])
 win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0

 return {
 'total_return': total_return,
 'sharpe_ratio': sharpe_ratio,
 'max_drawdown': max_drawdown,
 'win_rate': win_rate,
 'total_trades': total_trades,
 'strategy_returns': strategy_returns,
 'cumulative_returns': cumulative_returns
 }

class WalkForwardAnalyzer:
 """
The class for Walk-Forward Analysis Trade Strategies.

Walk-Forward analysis is a test method that simulates real
in which the model is re-trained on new data on the extent to which they
This provides a more realistic assessment of performance.
Strategies.
 """

 def __init__(self, train_size: int = 252, test_size: int = 63, step_size: int = 21):
 """
Initiating the Analysistor Walk-Forward.

 Args:
Train_size: The size of the learning window in days (on default 252)
test_size: Test window size in days (on default 63)
step_size: Step of window shift in days (on default 21)
 """
 self.train_size = train_size
 self.test_size = test_size
 self.step_size = step_size
 self.results: List[Dict[str, Any]] = []
 self.backtester = Backtester()

 def run_Analysis(self, data: pd.dataFrame, strategy: TradingStrategy) -> Dict[str, Any]:
 """
Launch is full of Walk-Forward Analysis.

This method is the heart of Walk-Forward Analysis.
1. Creates temporary data sections
2. Trains the strategy on learning data for each section
3. Testing strategy on test data
4. Collects and analyses results

 Args:
Data: financial series
strategy: Trade strategy for testing

 Returns:
The dictionary with results Analysis

 Raises:
ValueError: If data are not sufficient for Analysis
 """
 print(f"Launch Walk-Forward Analysis...")
pint(f"parameters: training={self.train_size} days, test={self.test_size} days, step={self.step_size} days})

# Cleaning the previous results
 self.results = []

# time sections
 try:
 splits = create_walk_forward_splits(
 data, self.train_size, self.test_size, self.step_size
 )
 except ValueError as e:
Raise ValueError(f "Different of sections: {e}")

 if len(splits) == 0:
Raise ValueError("not has been able to create a single section for Analysis")

prent(f) Created {len(splits)} sections for Analysis)

# Processing each section
 for i, split in enumerate(splits):
Print(f" Processing period {i+1}/{len(splits)}:"
f "training {'training_data'[0].strftime('%Y-%m-%d']} - "
 f"{split['train_dates'][1].strftime('%Y-%m-%d')}, "
f "test {'test_data'][0].strftime('%Y-%m-%d']} - "
 f"{split['test_dates'][1].strftime('%Y-%m-%d')}")

 try:
# Training strategy on learning data
 strategy.train(split['train_data'])

# Testing on test data
 metrics = self.backtester.run_backtest(split['test_data'], strategy)

# Retaining results
 result = {
 'period': i + 1,
 'train_start': split['train_start'],
 'train_end': split['train_end'],
 'test_start': split['test_start'],
 'test_end': split['test_end'],
 'train_dates': split['train_dates'],
 'test_dates': split['test_dates'],
 'metrics': metrics
 }

 self.results.append(result)

result: rate of return={metrics['total_return']:2%},"
 f"Sharpe={metrics['sharpe_ratio']:.2f}, "
f "delay={metrics['max_drawdown']:2%}}

 except Exception as e:
Print(f" Error in period {i+1}: {e})
# Continue with the next period
 continue

 if len(self.results) == 0:
Raise ValueError("not has been successful on Working for no period")

Print(f)"Analysis completed. Successfully on Workingno(len(self.results)} periods)

 return self.analyze_results()

 def analyze_results(self) -> Dict[str, Any]:
 """
Analysis of Walk-Forward test results.

This method provides statistical analysis of all results
testing by calculating key metrics performance
and the stability of the strategy.

 Returns:
The dictionary with results Analysis
 """
 if not self.results:
Raise ValueError("No results for Analysis. Start run_Anallysis()")

# Extracting metrics from all periods
 returns = [r['metrics']['total_return'] for r in self.results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in self.results]
 max_drawdowns = [r['metrics']['max_drawdown'] for r in self.results]
 win_rates = [r['metrics']['win_rate'] for r in self.results]
 total_trades = [r['metrics']['total_trades'] for r in self.results]

# Convergence in numpy arrays for convenience of computation
 returns = np.array(returns)
 sharpe_ratios = np.array(sharpe_ratios)
 max_drawdowns = np.array(max_drawdowns)
 win_rates = np.array(win_rates)
 total_trades = np.array(total_trades)

# Basic statistics
 Analysis = {
# General
 'total_periods': len(self.results),
 'successful_periods': len([r for r in returns if not np.isnan(r)]),

# Interest statistics
 'mean_return': np.nanmean(returns),
 'std_return': np.nanstd(returns),
 'min_return': np.nanmin(returns),
 'max_return': np.nanmax(returns),
 'median_return': np.nanmedian(returns),

# Sharpe Rato statistics
 'mean_sharpe': np.nanmean(sharpe_ratios),
 'std_sharpe': np.nanstd(sharpe_ratios),
 'min_sharpe': np.nanmin(sharpe_ratios),
 'max_sharpe': np.nanmax(sharpe_ratios),

# Slow down statistics
 'mean_drawdown': np.nanmean(max_drawdowns),
 'worst_drawdown': np.nanmin(max_drawdowns),
 'std_drawdown': np.nanstd(max_drawdowns),

# Trade statistics
 'mean_win_rate': np.nanmean(win_rates),
 'mean_trades_per_period': np.nanmean(total_trades),
 'total_trades': np.nansum(total_trades),

# Consistence
 'positive_periods': np.sum(returns > 0),
 'negative_periods': np.sum(returns < 0),
 'consistency': np.sum(returns > 0) / len(returns) if len(returns) > 0 else 0,

# Additional metrics
 'coefficient_of_variation': np.nanstd(returns) / np.abs(np.nanmean(returns)) if np.nanmean(returns) != 0 else np.inf,
 'skewness': self._calculate_skewness(returns),
 'kurtosis': self._calculate_kurtosis(returns),

# Detailed results
 'period_returns': returns.toList(),
 'period_sharpe_ratios': sharpe_ratios.toList(),
 'period_drawdowns': max_drawdowns.toList()
 }

 return Analysis

 def _calculate_skewness(self, data: np.ndarray) -> float:
"""""" "The calculation of distribution asymmetries"""
 data_clean = data[~np.isnan(data)]
 if len(data_clean) < 3:
 return 0.0

 mean = np.mean(data_clean)
 std = np.std(data_clean)
 if std == 0:
 return 0.0

 return np.mean(((data_clean - mean) / std) ** 3)

 def _calculate_kurtosis(self, data: np.ndarray) -> float:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 data_clean = data[~np.isnan(data)]
 if len(data_clean) < 4:
 return 0.0

 mean = np.mean(data_clean)
 std = np.std(data_clean)
 if std == 0:
 return 0.0

 return np.mean(((data_clean - mean) / std) ** 4) - 3
```

## Advanced Walk-Forward

** Advanced Engineering Theory:**
The standard Walk-Forward analysis uses fixed window sizes, but in real trade, it can be useful to adapt paragraphs Analysis on basic strategy. Advanced technologies make the analysis more flexible and realistic.

### 1. Adaptive window size

** Adaptation window theory:**
Adaptive window size is a technique where the size of the learning window is dynamically changing on base performance strategy. If the strategy shows good results, we increase the learning window for greater stability. If the results are poor, we reduce the window for faster adjustment to market change.

** The benefits of adaptive windows:**
- ** Adaptation: ** Window size adjusted to market conditions
- **Stability:** Increased window with good performance
- ** Sensitivity:** Reduction of window with poor performance
- ** Reality:** More accurately simulates real trade

** Deficiencies of adaptive windows:**
- **Complicity:** More complex implementation and configration
- **retraining:** Risk retraining on adaptive parameters
- ** Instability:** Frequent changes in window size can reduce stability

** Mathematical rationale:**

```
Let W(t) = window size in time t
W(t+1) = {
W(t) + ΔW, if R(t) >
W(t) - ΔW, if R(t) < α_low
W(t), otherwise
}
where R(t) is the return in period t, Δ_high and_________________low = threshold values
```

```python
def adaptive_walk_forward(data: pd.dataFrame,
 strategy: TradingStrategy,
 min_train: int = 126,
 max_train: int = 504,
 test_size: int = 63,
 performance_threshold_high: float = 0.05,
 performance_threshold_low: float = -0.05,
 window_adjustment: int = 21) -> List[Dict[str, Any]]:
 """
Walk-Forward analysis with adaptive window size.

This function performs adaptive Walk-Forward analysis where size
the learning window is dynamically changing on base performance
This allows strategies to better adapt to changes
Market conditions.

 Args:
Data: financial series
strategy: Trade strategy for testing
min_training: Minimum size of the training window
max_training: Maximum size of the training window
test_size: Size of test window
Performance_threshold_high: Window extension threshold
Performance_threshold_low: Window reduction threshold
Windows_adjustment: Window Adjustment Size

 Returns:
List of results with information on window sizes
 """

 results = []
 current_train_size = min_train
 backtester = Backtester()

 start_idx = 0
 period = 1

(f "Launch adaptive Walk-Forward Analysis...")
prent(f) "Initiative window size: {surrent_training_size} days")
Spring(f" Window range: {min_training} - {max_training}days)

 while start_idx + current_train_size + test_size <= len(data):
# Learning period with current window size
 train_data = data.iloc[start_idx:start_idx + current_train_size]

# Testsy period
 test_data = data.iloc[start_idx + current_train_size:start_idx + current_train_size + test_size]

prent(f)"Period {period}: the size of the window= {surrent_training_size} days,"
f "test {test_data.index[0].strftime('%Y-%m-%d')}"
 f"{test_data.index[-1].strftime('%Y-%m-%d')}")

 try:
# Training and testing
 strategy.train(train_data)
 metrics = backtester.run_backtest(test_data, strategy)

# Adapting the size of the window on base form
 total_return = metrics['total_return']
 old_train_size = current_train_size

 if total_return > performance_threshold_high:
# Good performance - increasing the window
 current_train_size = min(current_train_size + window_adjustment, max_train)
extension_reason = "increase (good performance)"
 elif total_return < performance_threshold_low:
# Bad performance - reduce window
 current_train_size = max(current_train_size - window_adjustment, min_train)
extension_reason = "Decrease (bad performance)"
 else:
extension_reason = "without change (average performance)"

# Save the result
 result = {
 'period': period,
 'train_size': old_train_size,
 'new_train_size': current_train_size,
 'adjustment_reason': adjustment_reason,
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'metrics': metrics
 }

 results.append(result)

result: return= {total_return: 2%},"
 f"Sharpe={metrics['sharpe_ratio']:.2f}, "
f Window: {old_training_size}

 except Exception as e:
Print(f) Error in period {period}: {e})
# Continue with the current window size
 pass

# Moving on to the next period
 start_idx += test_size
 period += 1

Print(f"Adjustative analysis completed.
(f) Final window size: {surrent_training_size} days)

 return results
```

♪##2 ♪ Multiple strategies ♪

** Multi-pronged strategy theory:**
This is particularly important for portfolio management, where better strategies can be combined.

** Benefits of comparing strategies:**
- ** Relative estimate:** Comparative performance in the same conditions
- ** Identification of leaders:** Identification of best strategies
- **Diversification:** The possibility of combining the best strategies
- **Pativity:** heck stability of different approaches

** Criteria for comparison:**
- ** Average return:** Overall return on strategy
- **Consistence:** Stability of positive results
- **Sharpe Rato:** Risk-adjusted return
- ** Maximum draught:** Maximum loss

```python
def multi_strategy_walk_forward(data: pd.dataFrame,
 strategies: Dict[str, TradingStrategy],
 train_size: int = 252,
 test_size: int = 63) -> Tuple[Dict[str, Dict[str, Any]], List[Tuple[str, Dict[str, float]]]]:
 """
Walk-Forward analysis with multiple strategies.

This function conducts a Walk-Forward analysis for several strategies
Simultaneously, which allows them to compare their performance
In the same market conditions.

 Args:
Data: financial series
strategies: Strategy dictionary
Train_size: The size of the learning window
test_size: Size of test window

 Returns:
Courtage (deliverable_Analisis, comparison_Strategy)
 """

 results = {}

(f "Launch Walk-Forward Analysis for {len(Strategies)} Strategies...")
(f "Strategy: {List(Strategies.keys()}}")

 for strategy_name, strategy in strategies.items():
 print(f"\n{'='*50}")
(f "Strategy Analysis: {strategic_name}")
 print(f"{'='*50}")

 try:
# Creating a new copy of the Analysistor for each strategy
 analyzer = WalkForwardAnalyzer(train_size, test_size)
 Analysis = analyzer.run_Analysis(data, strategy)

 results[strategy_name] = Analysis

"Strategy {Strategy_name} is completed:")
average return: {Analysis['mean_return']:2%}}
Print(f"Consistence: {Analysis['consistency']: 2%}})
Middle Sharpe:(Analysis['mean_sharpe']:2f})
(f" Worst draught: {Anallysis['worth_drawdown']: 2 per cent}})

 except Exception as e:
Print(f) Mistake in strategy analysis {strategic_name}: {e})
 results[strategy_name] = None

# Comparison strategies
 comparison = compare_strategies(results)

 print(f"\n{'='*50}")
("comparison STRATEGIES")
 print(f"{'='*50}")

 for i, (strategy_name, metrics) in enumerate(comparison, 1):
 print(f"{i}. {strategy_name}:")
Print(f) Income: {métrics['mean_return']:2%}})
Print(f"Consistence: {metrics['consistency']: 2%}})
 print(f" Sharpe: {metrics['mean_sharpe']:.2f}")
Print(f" Slide: {metrics['worth_drawdown']:2%}})

 return results, comparison

def compare_strategies(results: Dict[str, Dict[str, Any]]) -> List[Tuple[str, Dict[str, float]]]:
 """
a comparison of the results of multiple strategies.

This function compares the results of Walk-Forward Analysis
for different strategies and ranking them on key metrics.

 Args:
Results: Results dictionary of Analysis strategies

 Returns:
Sorted strategy list with metrics
 """

 comparison = {}

 for strategy_name, Analysis in results.items():
 if Analysis is None:
 continue

 comparison[strategy_name] = {
 'mean_return': Analysis['mean_return'],
 'consistency': Analysis['consistency'],
 'mean_sharpe': Analysis['mean_sharpe'],
 'worst_drawdown': Analysis['worst_drawdown'],
 'coefficient_of_variation': Analysis['coefficient_of_variation'],
 'total_periods': Analysis['total_periods']
 }

# Sorting on average return (on loss)
 sorted_strategies = sorted(
 comparison.items(),
 key=lambda x: x[1]['mean_return'],
 reverse=True
 )

 return sorted_strategies

class RSIStrategy(TradingStrategy):
"The Strategy on Basic RSI Indicator"

 def __init__(self, rsi_period: int = 14, oversold: float = 30, overbought: float = 70):
 self.rsi_period = rsi_period
 self.oversold = oversold
 self.overbought = overbought
 self.is_trained = False

 def train(self, data: pd.dataFrame) -> None:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")
 self.is_trained = True

 def predict(self, data: pd.dataFrame) -> pd.Series:
""""""""" "Generation of signals on base RSI"""
 if not self.is_trained:
Raise ValueError

 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")

# Counting RSI
 delta = data['close'].diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
 rs = gain / loss
 rsi = 100 - (100 / (1 + rs))

# Generate signals
 signals = pd.Series(0, index=data.index)

# Buying signal: RSI leaves the resell area
 buy_signal = (rsi > self.oversold) & (rsi.shift(1) <= self.oversold)

# The sale signal: RSI is leaving the shopping area
 sell_signal = (rsi < self.overbought) & (rsi.shift(1) >= self.overbought)

 signals[buy_signal] = 1
 signals[sell_signal] = -1

 return signals

 def get_name(self) -> str:
 return f"RSI_{self.rsi_period}_{self.oversold}_{self.overbought}"

class BollingerBandsStrategy(TradingStrategy):
"Strategy on Ballinger stripes."

 def __init__(self, period: int = 20, std_dev: float = 2.0):
 self.period = period
 self.std_dev = std_dev
 self.is_trained = False

 def train(self, data: pd.dataFrame) -> None:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")
 self.is_trained = True

 def predict(self, data: pd.dataFrame) -> pd.Series:
"""""" "Generation of the signals on the base of the Bollinger strips."
 if not self.is_trained:
Raise ValueError

 if 'close' not in data.columns:
Raise ValueError("data shall contain a column 'close'")

# Counting Bollinger strips
 sma = data['close'].rolling(window=self.period).mean()
 std = data['close'].rolling(window=self.period).std()
 upper_band = sma + (std * self.std_dev)
 lower_band = sma - (std * self.std_dev)

# Generate signals
 signals = pd.Series(0, index=data.index)

# Buying signal: price refers to bottom line
 buy_signal = (data['close'] <= lower_band) & (data['close'].shift(1) > lower_band.shift(1))

# The sale signal: price refers to the top page
 sell_signal = (data['close'] >= upper_band) & (data['close'].shift(1) < upper_band.shift(1))

 signals[buy_signal] = 1
 signals[sell_signal] = -1

 return signals

 def get_name(self) -> str:
 return f"BB_{self.period}_{self.std_dev}"
```

### 3. Rolling Window vs Expanding Window

```python
def rolling_walk_forward(data, strategy, window_size=252, test_size=63):
 """Rolling Window Walk-Forward"""

 results = []
 start_idx = 0

 while start_idx + window_size + test_size <= len(data):
# Learning period (fixed window)
 train_data = data.iloc[start_idx:start_idx + window_size]

# Testsy period
 test_data = data.iloc[start_idx + window_size:start_idx + window_size + test_size]

# Training and testing
 strategy.train(train_data)
 backtester = Backtester()
 metrics = backtester.run_backtest(test_data, strategy)

 results.append(metrics)
 start_idx += test_size

 return results

def expanding_walk_forward(data, strategy, min_train=126, test_size=63):
 """Expanding Window Walk-Forward"""

 results = []
 start_idx = 0
 train_size = min_train

 while start_idx + train_size + test_size <= len(data):
# Learning period (expanding window)
 train_data = data.iloc[:start_idx + train_size]

# Testsy period
 test_data = data.iloc[start_idx + train_size:start_idx + train_size + test_size]

# Training and testing
 strategy.train(train_data)
 backtester = Backtester()
 metrics = backtester.run_backtest(test_data, strategy)

 results.append(metrics)
 start_idx += test_size
train_size +=test_size # Extend window

 return results
```

## Analysis of stability

###1. Stability performance

```python
def analyze_stability(results):
"Analysis of Stability of Results."

 returns = [r['metrics']['total_return'] for r in results]

# The coefficient of variation
 cv = np.std(returns) / np.abs(np.mean(returns))

# Tread performance
 x = np.arange(len(returns))
 slope, intercept, r_value, p_value, std_err = stats.linregress(x, returns)

# Sharpe Ratio stability
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
 sharpe_stability = 1 - np.std(sharpe_ratios) / np.abs(np.mean(sharpe_ratios))

 return {
 'coefficient_of_variation': cv,
 'performance_trend': slope,
 'trend_significance': p_value,
 'sharpe_stability': sharpe_stability,
 'return_consistency': 1 - cv
 }
```

♪##2 ♪ Degradation analysis

```python
def analyze_degradation(results):
"Analysis of degradation performance."

 returns = [r['metrics']['total_return'] for r in results]

# Separation on Periods
 n_periods = len(returns)
 first_half = returns[:n_periods//2]
 second_half = returns[n_periods//2:]

 # Comparison performance
 first_half_mean = np.mean(first_half)
 second_half_mean = np.mean(second_half)

 degradation = (second_half_mean - first_half_mean) / abs(first_half_mean)

# Statistical test
 t_stat, p_value = stats.ttest_ind(first_half, second_half)

 return {
 'first_half_mean': first_half_mean,
 'second_half_mean': second_half_mean,
 'degradation': degradation,
 't_statistic': t_stat,
 'p_value': p_value,
 'significant_degradation': p_value < 0.05 and degradation < -0.1
 }
```

###3: Adaptation analysis

```python
def analyze_adaptability(results, market_conditions):
"Analysis of market adaptation"

 adaptability_scores = []

 for i, result in enumerate(results):
# Getting market conditions for the period
 period_conditions = market_conditions[i]

# Analysis of performance in different settings
if period_conditions['volatility'] > 0.3: # High volatility
 volatility_performance = result['metrics']['total_return']
 else:
 volatility_performance = result['metrics']['total_return']

if period_conditions['trend'] == 'bull': #Living market
 trend_performance = result['metrics']['total_return']
Else: # Bear market
 trend_performance = result['metrics']['total_return']

# Adaptation evaluation
 adaptability = (volatility_performance + trend_performance) / 2
 adaptability_scores.append(adaptability)

 return {
 'mean_adaptability': np.mean(adaptability_scores),
 'adaptability_std': np.std(adaptability_scores),
 'adaptability_trend': np.polyfit(range(len(adaptability_scores)), adaptability_scores, 1)[0]
 }
```

♪ Visualization of results

###1: Timetable on Periods

```python
def plot_performance_by_period(results):
"Graphic performance on periods."

 periods = [r['period'] for r in results]
 returns = [r['metrics']['total_return'] for r in results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]

 fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Income
 ax1.plot(periods, returns, marker='o', linewidth=2)
 ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
ax1.set_title('income on periods')
ax1.set_ylabel('income')
 ax1.grid(True, alpha=0.3)

 # Sharpe Ratio
 ax2.plot(periods, sharpe_ratios, marker='s', color='green', linewidth=2)
 ax2.axhline(y=1, color='r', linestyle='--', alpha=0.5)
ax2.set_title('Sharp Radio on Periods')
ax2.set_xlabel('Period')
 ax2.set_ylabel('Sharpe Ratio')
 ax2.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()
```

♪##2, distribution of results

** Analysis distribution:**
The analysis of the distribution of results helps to understand the statistical characteristics of the strategy &apos; s performance.

** Key aspects of distribution:**
- **Normality:** heck conformity to normal distribution
- **Asymmetry: ** Assessment of the distortion of results
- **Excess: ** Assessment of tail load
- ** Emissions:** Identification of abnormal results

```python
def plot_results_distribution(results: List[Dict[str, Any]]) -> None:
 """
Visualize the distribution of the results of the Walk-Forward Analysis.

This function creates a detailed visualization of distribution
Key metric performance strategy.

 Args:
results: List of results Walk-Forward Analysis
 """

 if not results:
"No data for visualization"
 return

# Retrieving metrics
 returns = [r['metrics']['total_return'] for r in results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
 max_drawdowns = [r['metrics']['max_drawdown'] for r in results]

# Creating the figure with sub-graphs
 fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Walk-Forward Analysis results distribution', fontsize=16, fonweight='bold')

* 1. Income distribution
 ax1 = axes[0, 0]
 ax1.hist(returns, bins=20, alpha=0.7, edgecolor='black', color='skyblue')
 ax1.axvline(np.mean(returns), color='red', linestyle='--', linewidth=2,
Label=f'average: {np.mean(returns):3f}'
 ax1.axvline(np.median(returns), color='green', linestyle='--', linewidth=2,
Label=f'Media: {np.median(returns):3f}'
ax1.set_title.
ax1.set_xlabel('income')
ax1.set_ylabel('Part')
 ax1.legend()
 ax1.grid(True, alpha=0.3)

# 2. Share Rato
 ax2 = axes[0, 1]
 ax2.hist(sharpe_ratios, bins=20, alpha=0.7, edgecolor='black', color='lightgreen')
 ax2.axvline(np.mean(sharpe_ratios), color='red', linestyle='--', linewidth=2,
Label=f'Medium: {np.mean(sharpe_ratios):3f}'
 ax2.axvline(1.0, color='orange', linestyle='-', linewidth=2, alpha=0.7,
 label='Sharpe = 1.0')
ax2.set_title.
 ax2.set_xlabel('Sharpe Ratio')
ax2.set_ylabel('Part')
 ax2.legend()
 ax2.grid(True, alpha=0.3)

# 3. Distribution of the proscessaries
 ax3 = axes[0, 2]
 ax3.hist(max_drawdowns, bins=20, alpha=0.7, edgecolor='black', color='lightcoral')
 ax3.axvline(np.mean(max_drawdowns), color='red', linestyle='--', linewidth=2,
Label=f'Medium: {np.mean(max_drawdowns):3f}'
 ax3.axvline(-0.1, color='orange', linestyle='-', linewidth=2, alpha=0.7,
Label='-10% prosedition')
ax3.set_title
ax3.set_xlabel.
ax3.set_ylabel('Part')
 ax3.legend()
 ax3.grid(True, alpha=0.3)

# 4. Q-Q table for return
 ax4 = axes[1, 0]
 from scipy import stats
 stats.probplot(returns, dist="norm", plot=ax4)
ax4.set_title('Q-Q Plot Interest', fontweight='bold')
 ax4.grid(True, alpha=0.3)

# 5. Box table for all metrics
 ax5 = axes[1, 1]
Data_for_box = [returns, sharpe_ratios, [abs(x) for x in max_drawdowns]] # Absolute values of sediment
Box_plot = ax5.boxplot(data_for_box, labels=['income', 'Sharp Ratio', '\\\\\\\\']
 patch_artist=True)

# Painting box bits
 colors = ['lightblue', 'lightgreen', 'lightcoral']
 for patch, color in zip(box_plot['boxes'], colors):
 patch.set_facecolor(color)

ax5.set_title('Box Plot metric',fonweight='bold')
ax5.set_ylabel('value')
 ax5.grid(True, alpha=0.3)

# 6. Cumulative returns on periods
 ax6 = axes[1, 2]
 cumulative_returns = np.cumprod([1 + r for r in returns])
 periods = range(1, len(cumulative_returns) + 1)
 ax6.plot(periods, cumulative_returns, marker='o', linewidth=2, markersize=4)
ax6.axhline(y=1.0, color='red', lineyle='--', alpha=0.7, label='Initiative capital')
ax6.set_title('cumulative return',fonweight='bold')
ax6.set_xlabel('Period')
ax6.set_ylabel('cumulative return')
 ax6.legend()
 ax6.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()

# Bringing statistics out
PRIint("\n\\\\\\cH00FFFF}SYMBOLS:")
pprint(f "Property:")
Middle: {np.mean(returns): 4f})
(pint(f" Median: {np.median(returns): 4f})
standard deviation: {np.std(returns): 4f})
asymmetry: {stats.skew(returns): 4f})
Print(f"Excess: {stats.curtosis(returns):4f}})

 print(f"\nSharpe Ratio:")
Middle: {np.mean(sharpe_ratios): 4f})
(pint(f" Median: {np.median(sharpe_ratios): 4f})
standard deviation: {np.std(sharpe_ratios): 4f})
Asymmetry: {stats.skew(sharpe_ratios): 4f})
Print(f"Excess: {stats.curtosis(sharpe_ratios):4f}})

def plot_cumulative_performance(results: List[Dict[str, Any]]) -> None:
 """
Visualization of cumulative strategy.

This function creates a schedule of cumulative returns and others
Key metrics on Walk-Forward Anallysis periods.

 Args:
results: List of results Walk-Forward Analysis
 """

 if not results:
"No data for visualization"
 return

# Extracting data
 periods = [r['period'] for r in results]
 returns = [r['metrics']['total_return'] for r in results]
 sharpe_ratios = [r['metrics']['sharpe_ratio'] for r in results]
 max_drawdowns = [r['metrics']['max_drawdown'] for r in results]

# Computing cumulative returns
 cumulative_returns = np.cumprod([1 + r for r in returns])

# Creating the figure
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))
"fig.sumptile" ('Collective strategy', fontsize=16, fontweight='bold')

# 1. Cumulative returns
 ax1 = axes[0, 0]
 ax1.plot(periods, cumulative_returns, marker='o', linewidth=2, markersize=4, color='blue')
ax1.axhline(y=1.0, color='red', lineyle='--', alpha=0.7, label='Initiative capital')
 ax1.fill_between(periods, cumulative_returns, 1.0, alpha=0.3, color='blue')
ax1.set_title('cumulative return',fonweight='bold')
ax1.set_xlabel('Period')
ax1.set_ylabel('cumulative return')
 ax1.legend()
 ax1.grid(True, alpha=0.3)

#2 Income on Periods
 ax2 = axes[0, 1]
 colors = ['green' if r > 0 else 'red' for r in returns]
 bars = ax2.bar(periods, returns, color=colors, alpha=0.7)
 ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5)
 ax2.axhline(y=np.mean(returns), color='blue', linestyle='--', alpha=0.7,
Label=f'average: {np.mean(returns):3f}'
ax2.set_title.
ax2.set_xlabel('Period')
ax2.set_ylabel('income')
 ax2.legend()
 ax2.grid(True, alpha=0.3)

# 3. Sharpe Ratio on Periods
 ax3 = axes[1, 0]
 ax3.plot(periods, sharpe_ratios, marker='s', linewidth=2, markersize=4, color='green')
 ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Sharpe = 1.0')
 ax3.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Sharpe = 0.5')
 ax3.fill_between(periods, sharpe_ratios, 0, alpha=0.3, color='green')
ax3.set_title('Sharp Ratio on Periods',fonweight='bold')
ax3.set_xlabel('Period')
 ax3.set_ylabel('Sharpe Ratio')
 ax3.legend()
 ax3.grid(True, alpha=0.3)

# 4. Delays on periods
 ax4 = axes[1, 1]
 ax4.bar(periods, max_drawdowns, color='red', alpha=0.7)
ax4.axhline(y=-0.1 color='range', linely='--', alpha=0.7, label='-10% prosa')
ax4.axhline(y=-0.2, color='red', lineyle='--', alpha=0.7, label='-20% landing')
ax4.set_title
ax4.set_xlabel('Period')
ax4.set_ylabel.
 ax4.legend()
 ax4.grid(True, alpha=0.3)

 plt.tight_layout()
 plt.show()
```

# Full workflow example

** Case study: **
This section shows the full Walk-Forward Analysis from downloading data to interpretation of results. Example includes all necessary components for an independent Launch Analysis.

### square testy data

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yfinance as yf
from scipy import stats

def create_sample_data(symbol: str = "AAPL", period: str = "2y") -> pd.dataFrame:
 """
Create test data for Walk-Forward Analysis.

This function downloads real financial data and prepares them
For Walk-Forward Analysis, data Yahoo Finance is used.

 Args:
symbol: Share symbol (on AAPL default)
period: Data period (on default 2 years)

 Returns:
DataFrame with prepared data
 """

spring(f"Loding data for {symbol} for the period {period}...)

 try:
# Loading data through yfinance
 ticker = yf.Ticker(symbol)
 data = ticker.history(period=period)

 if data.empty:
raise ValueError(f"not has been able to download data for {symbol})

# Rename columns for compatibility
 data.columns = [col.lower() for col in data.columns]

# Remove columns that are not needed
 if 'adj close' in data.columns:
 data = data.drop('adj close', axis=1)

 # checking presence of required columns
 required_columns = ['open', 'high', 'low', 'close', 'volume']
 Missing_columns = [col for col in required_columns if col not in data.columns]

 if Missing_columns:
Raise ValueError(f"Missing the necessary columns: {Missing_columns})

# Remove lines with NaN values
 data = data.dropna()

Print(f" Upload {len(data)} records")
prent(f"Period: {data.index[0].strftime('%Y-%m-%d')} - {data.index[-1].strftime('%Y-%m-%d'}}
(pint(f"Calls: {List(data.columns)})

 return data

 except Exception as e:
print(f" Data upload error: {e}")
"Creating synthetic data..."

# Creating synthetic data in case of error
 dates = pd.date_range(start='2022-01-01', end='2024-01-01', freq='D')
 np.random.seed(42)

# Generate random wandering with trend
returns = np.random.normal(0.005, 0.02, Len(data)) # Average return 0.05% in day
 prices = 100 * np.exp(np.cumsum(returns))

 # Creating OHLC data
 data = pd.dataFrame(index=dates)
 data['close'] = prices
 data['open'] = data['close'].shift(1).fillna(data['close'])
 data['high'] = data[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.normal(0, 0.01, len(dates))))
 data['low'] = data[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.normal(0, 0.01, len(dates))))
 data['volume'] = np.random.randint(1000000, 10000000, len(dates))

Print(f) Created {len(data)} synthetic records")
 return data

def complete_walk_forward_Analysis(data: pd.dataFrame,
 strategy: TradingStrategy,
 train_size: int = 252,
 test_size: int = 63,
 step_size: int = 21) -> Dict[str, Any]:
 """
Full Walk-Forward analysis with detailed Reporting.

This function runs the full Walk-Forward Analysis, including:
1. Create Analysistor
 2. Launch Analysis
3. Stability analysis
4. Analysis of degradation
5. Visualization of results
6. Report generationa

 Args:
Data: financial series
strategy: Trade strategy for testing
Train_size: The size of the learning window
test_size: Size of test window
step_size: Step of the window shift

 Returns:
The dictionary with full results of Analysis
 """

 print("="*60)
Prent("full WALK-FORWARD ANALYSIS")
 print("="*60)
"Strategy: {strategic.get_name()}")
prent(f"parameters: training={training_size} days, test=(test_size} days, step={step_size} days)
prent(f"data: {len(data)} notes with {data.index[0].strftime('%Y-%m-%d')} on {data.index[-1].strftime('%Y-%m-%d'}})

♪ 1 ♪ Create Analysistor
Print('n1.'create Analysistor Walk-Forward...')
 analyzer = WalkForwardAnalyzer(train_size=train_size, test_size=test_size, step_size=step_size)

 # 2. Launch Analysis
 print("\n2. Launch Walk-Forward Analysis...")
 Analysis = analyzer.run_Analysis(data, strategy)

# 3. Analysis of stability
Print("\n3. Analysis of stability...")
 stability = analyze_stability(analyzer.results)

#4 Analysis of degradation
Print("\n4. Degradation analysis...")
 degradation = analyze_degradation(analyzer.results)

# 5. Visualization
Print("\n5.
 try:
 plot_performance_by_period(analyzer.results)
 plot_results_distribution(analyzer.results)
 plot_cumulative_performance(analyzer.results)
 except Exception as e:
Print(f) Error in scheduling: {e})

♪ 6. Detailed Report
 print("\n" + "="*60)
"WALK-FORWARD Anallysis"
 print("="*60)

prent(f"\n
(f) Total periods: {Analysis['total_periods']}}
(f" Successful periods: {Analysis['accessfulful_periods']})
average return: {Analysis['mean_return']:2%}}
standard deviation: {Analysis['std_return':2%}})
(f" Median return:(Analysis['median_return']: 2 per cent})
minimum return: {Analysis['min_return':2%}})
peak(f" Maximum return: {Analysis['max_return']:2%}})

(f'n'\\\\ \RIS-SCORRECTED METHicS:")
Middle Sharpe Rato:(Analysis['mean_sharpe']:2f})
standard deviation Sharpe: {Analysis['std_sharpe']:2f}})
(f" Minimum Sharpe: {Analysis['min_sharpe':.2f}})
peak(f" Maximum Sharpe:(Analysis['max_sharpe':2f}})

(f)
average draught: {Analysis['mean_drawdown']:2%}}
(f" Worst draught: {Anallysis['worth_drawdown']: 2 per cent}})
pprint(f" Standard seed deviation: {Analysis['std_drawdown']:2%}})

Print(f'n'int'S CONSISTENCE:")
(f" Positive periods: {Analysis['positive_periods']}})
(f" Negative periods: {Analysis['negative_periods']})
Print(f"Consistence: {Analysis['consistency']: 2%}})
print(f "Variance coefficient: {Analysis['co-officent_of_variation']:3f}})

PRIint(f"\n\\\\n\ STATISTICAL CHARACTERISTICS:")
Asymmetry: {Analysis['skewness':.3f}})
Print(f"Excess: {Analysis['curtosis']:.3f}})
(f) Average percentage of winning transactions: {Analysis['mean_win_rate']:2%}}
(f" Average number of transactions over the period: {Analesis['mean_trades_per_per_period']:.1f})
(f" Total number of transactions: {Analysis['total_trades'}})

Print(f"\n\\\\\n\ANALYSIS OF STABILITY:")
Print(f" Rate of profit variation: {`co-officent_of_variation']:3f})
(f) Tread performance:(`security_trend':.4f})
pprint(f" Significance of trend (p-value): {`trend_significance']:4f})
(f"Stable Sharpe Ratio: {sharpe_state']:.3f})
Print(f" Return-rate consistency: {'return_consistency']:.3f})

Print(f)(n\n\\\} ANALYSIS OF DEGRADATION:)
first half income: {degration['first_half_mean']:2%})
prent(f" Income of the second half: {degradation['second_half_mean']:2%})
(f "Degradation: {degration['degration']: 2%}")
pprint(f" t-statistics: {degration['t_statistic']:.3f}})
 print(f" p-value: {degradation['p_value']:.4f}")
significant degradation: {'Yes' if demobilization['significant_degration'] else 'No'}})

# Assessment of the quality of strategy
PRINT(f)\n\\\\\\\\\\EVALUATION OF THE QUALITY OF THE STRATEGY:}

 quality_score = 0
 quality_factors = []

# Checking returns
 if Analysis['mean_return'] > 0.05:
 quality_score += 2
Quality_factors.append("\\\$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
 elif Analysis['mean_return'] > 0:
 quality_score += 1
Quality_factors.append("
 else:
Qualitity_factors.append("

 # checking Sharpe Ratio
 if Analysis['mean_sharpe'] > 1.0:
 quality_score += 2
Quality_factors.append("
 elif Analysis['mean_sharpe'] > 0.5:
 quality_score += 1
Qualitity_factors.append("
 else:
Quality_factors.append("

# Checking conspiracies
 if Analysis['consistency'] > 0.6:
 quality_score += 2
Quality_factors.append("
 elif Analysis['consistency'] > 0.4:
 quality_score += 1
Qualitity_factors.append("
 else:
Quality_factors.append("

# Checking proslands
 if Analysis['worst_drawdown'] > -0.1:
 quality_score += 1
Quality_factors.append("
 else:
Quality_factors.append("

# Checking degradation
 if not degradation['significant_degradation']:
 quality_score += 1
Quality_factors.append("
 else:
Quality_factors.append("

(f" Total score: {Quality_score}/8)
 for factor in quality_factors:
 print(f" {factor}")

 if quality_score >= 6:
Print(" * relevant strategy!")
 elif quality_score >= 4:
"Prent(" * Good Strategy")
 elif quality_score >= 2:
Prent(("HOCK FOR IMPROVEMENT")
 else:
Prent(("not RECOMMENDED")

 print("\n" + "="*60)

 return {
 'Analysis': Analysis,
 'stability': stability,
 'degradation': degradation,
 'results': analyzer.results,
 'quality_score': quality_score,
 'quality_factors': quality_factors
 }

# Example of use
if __name__ == "__main__":
 # Loading data
 data = create_sample_data("AAPL", "2y")

# Creating strategy
 strategies = {
 'SMA_20_50': SimpleMovingAverageStrategy(20, 50),
 'SMA_10_30': SimpleMovingAverageStrategy(10, 30),
 'RSI_14': RSIStrategy(14, 30, 70),
 'BB_20': BollingerBandsStrategy(20, 2.0)
 }

# We analyze every strategy
 for strategy_name, strategy in strategies.items():
 print(f"\n{'='*80}")
(f) STRATEGIC ANALYSIS: {strategic_name})
 print(f"{'='*80}")

 try:
 results = complete_walk_forward_Analysis(data, strategy)
 except Exception as e:
Print(f) Mistake in strategy analysis {strategic_name}: {e})

# Compare all strategies
 print(f"\n{'='*80}")
PRINT( "ANALYSIS ALL STRATEGY")
 print(f"{'='*80}")

 try:
 multi_results, comparison = multi_strategy_walk_forward(data, strategies)
 except Exception as e:
Print(f) Error in comparative analysis: {e})
```

## Next steps

After Walk-Forward Analysis go to:
- **[08_monte_carlo_simulation.md](08_monte_carlo_simulation.md)** - Monte Carlo simulation
- **[09_risk_Management.md](09_risk_Management.md)** - Risk Management

## Key findings

1. **Walk-Forward** is the most realistic test method
2. ** Stability** is more important than maximum return
3. ** Adaptation** - key to long-term success
4. ** Degradation** - normal, to be taken into account
5. ** Visualization** helps understand the behaviour of the strategy

---

♪ It's important ♪ ♪ A good strategy has to be stable on new data and not just on historical data ♪
