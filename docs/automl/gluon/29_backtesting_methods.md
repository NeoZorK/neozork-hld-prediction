# In-depth describe of betting techniques

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who backtting is critical for ML strategies

### ♪ The need to stab for ML strategies to succeed

```mermaid
graph TD
A[ML-Strategy] -- > B {Has the backting been done?}

B-~ ~ No ~ C[90 per cent of strategies fail]
C -> D[~ retraining on historical data]
C --> E[~ Unexpected loss in real trade]
C --> F[~ Instable performance]
C --> G[~ time and money]

B -->\\\\H[10% successful strategies]
H-> I[♪ Realistic evaluation of performance]
H -> J[~ risk understanding and prosedience]
H --> K[~ Stable Working on Different Conditions]
H -> L[~ Optimized parameters]

I -> M [Sustained trade]
 J --> M
 K --> M
 L --> M

 style A fill:#e3f2fd
 style C fill:#ffcdd2
 style H fill:#c8e6c9
 style M fill:#4caf50
```

Why is 90% of the ML strategy failing in real trade?

♪ ♪ ♪ What gives you the right backup?

- ** Reality**: Understanding real performance strategy
- **Platitude**: check stability on different market conditions
- **Risk Management**: Assessment of maximum loss and delay
** Optimization**: configurization of parameters for maximum efficiency

♪ ♪ What's going on without the right backup?

- **retraining**: Workinget strategy only on historical data
- ** Surprising loss**: Real results are worse than expected
- ** Instability**: The Workinget Strategy is unstable
- ** Disappointing**: Loss of time and money

## Theoretical foundations of betting

### Mathematical principles

**Bextering as a statistical task:**

```math
P(Strategy|Historical_data) = P(Returns|Parameters, Market_Conditions)
```

Where:

- `P(Strategy\historical_data)' is the probability of success of a strategy on historical data
- `P(Returns, Parameters, Market_Conditions)' - distribution of returns under specified parameters and market conditions

** Becketting quality criteria:**

1. **Statistical significance**: p-value < 0.05
2. ** Economic significance**: Sharpe > 1.0
3. ** Stability**: Maximum draught < 20 per cent
4. **Purity**: Results stable on different periods

### Bactering types

*# * * comparison of types of betting

```mermaid
graph TB
A[Tips of buffering] - • B [Simple buffering]
A-> C[Out-of-sample buffering]
A --> D [Walk-forward buffering]
A-> E[Cross-validation buffering]

B -> B1 [Learning on historical data]
B --> B2 [Text on the same period]
B --> B3[~ Speed]
B -> B4[~ Insecure]
B --> B5[❌ retraining]

C --> C1 [Learning on part of the data]
C --> C2 [Texting on the rest]
C --> C3[~ More realistic]
C --> C4[~ One break-up]
C --> C5[~ Better common]

D -> D1 [Slipping Learning Window]
D --> D2 [Continuing update model]
D -> D3[~ The most realistic]
D -> D4[~ Multiple tests]
D -> D5[~ Real Trade Simulation]

E --> E1 [multiple data breakdowns]
E --> E2 [Statistical validation]
E --> E3[~ Most reliable]
E -> E4[~ Statistical significance]
E -> E5[~ approach]

 style B fill:#ffcdd2
 style C fill:#fff3e0
 style D fill:#c8e6c9
 style E fill:#4caf50
```

### 1. Simple Backting

- Training on historical data
- Testing on the same period
Quick but unreliable.

###2. Out-of-sample buffering

- Training on part of the data
- Testing on the rest
- More realistic.

### 3. Walk-forward buffering

- Slipping Learning Window
- Permanent update model
- The most realistic.

###4. Cross-validation buffering

- Multiple breakdowns
- Statistical validation
- Most reliable.

♪ ♪ Advances in bactering techniques

♪##1 ♪ Becketting time series ♪

### ♪ process of the time series of bettings

```mermaid
graph TD
A [Reference temporary data] --> B [Section in time]

B --> C[Learning data<br/>70% from beginning]
B --> D[tests data<br/> 30% from end]

C -> E [model training]
E --> F [Treaties on test data]

D -> G [Real returns]
F --> H [strategic returns]
 G --> H

H -> I [Quality metric calculation]
I-> J [Sharp coefficient]
I -> K [Maximum draught]
I-> L [Total return]

J -> M [Strategy assessment]
 K --> M
 L --> M

M --> N{Strategy successful?}
N--♪ ♪ Yeah ♪ O[♪ Depla in sales]
N--~ ~ No~ P[~ Optimization of parameters]

P --> Q [configration model]
 Q --> E

 style A fill:#e3f2fd
 style C fill:#c8e6c9
 style D fill:#fff3e0
 style O fill:#4caf50
 style P fill:#ff9800
```

** Specialities of time series:**

```python
def time_series_backtest(data, model, train_size=0.7, test_size=0.3,
 config=None, validation=True, random_state=None):
 """
Becketting for time series with detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 train_size : float, default=0.7
Percentage of data for training (0.0 < tran_size < 1.0)
- 0.7 means 70 per cent of the data for training
- Recommended 0.6-0.8 for most cases
- Less than 0.6 can lead to retraining.
- More than 0.8 may lead to a lack of education

 test_size : float, default=0.3
Proportion of data for testing (0.0 < test_size < 1.0)
- 0.3 means 30 per cent of test data
- Must be 1.0 - train_size.
- A minimum of 0.2 for reliability is recommended

 config : dict, optional
Additional configuring for betting
- 'min_training_samples':int, default=100 - minimum number of teaching samples
- 'min_test_samples':int, default=50 = minimum number of testes
- 'shuffle': bell, default=False - whether to mix data (not recommended for time series)
- 'Strategy': bool, default=False - stratified separation
- 'return_predations': bool, default=True - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correctness of train_size and test_size

 random_state : int, optional
Seed for reproducible results
- Only used if shuffle=True
- It is recommended to ask for reproduction

 Returns:
 --------
 dict
Vocabulary withbacking results:
- 'sharpe': float - Sharp factor of strategy
- 'max_drawdown': float = maximum draught (negative)
- 'Total_return': float - total strategy return
- 'annual_return': float - annual return
- 'volatility': float - strategy volatility
- 'predications': np.array - model predictions (if return_predictations=True)
- 'training_metrics':dict - metrics on learning data
- 'test_metrics':dict - metrics on test data
- 'config_Used':dict - used configuration

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the no model supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = time_series_backtest(data, model)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'min_train_samples': 200,
 ... 'min_test_samples': 100,
 ... 'verbose': True
 ... }
 >>> results = time_series_backtest(data, model, train_size=0.8, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = time_series_backtest(data, model, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'min_train_samples': 100,
 'min_test_samples': 50,
 'shuffle': False,
 'stratify': False,
 'return_predictions': True,
 'return_metrics': True,
 'verbose': False
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_train_samples'] + config['min_test_samples']:
Minimum: {config['min_training_samples'] + config['min_test_samples']}}

 if not (0 < train_size < 1) or not (0 < test_size < 1):
Raise ValueError("training_size and test_size should be between 0 and 1)

 if abs(train_size + test_size - 1.0) > 1e-6:
Raise ValueError("training_size + test_size shall be 1.0")

# Data sharing in time
 split_point = int(len(data) * train_size)

 train_data = data[:split_point]
 test_data = data[split_point:]

# check minimum number of samples
 if len(train_data) < config['min_train_samples']:
raise ValueError(f "Insufficient learning data: {len(training_data)} < {config['min_training_samples]}})

 if len(test_data) < config['min_test_samples']:
raise ValueError(f "Insufficient test data: {len(test_data)} < {config['min_test_samples]}})

 if config['verbose']:
Print(f "Learning samples: {len(training_data)}})
(f"tests samples: {len(test_data}})

# Model learning
 try:
 model.fit(train_data)
 except Exception as e:
Raise TypeError(f) Model Training Error: {e})

# Premonition
 try:
 predictions = model.predict(test_data)
 except Exception as e:
Raise TypeError(f) "The model prediction error: {e}")

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()
 annual_return = strategy_returns.mean() * 252
 volatility = strategy_returns.std() * np.sqrt(252)

# Results
 results = {
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'annual_return': annual_return,
 'volatility': volatility,
 'config_Used': config.copy()
 }

# Additional results
 if config['return_predictions']:
 results['predictions'] = predictions

 if config['return_metrics']:
# metrics on learning data
 train_returns = train_data['returns']
 train_predictions = model.predict(train_data)
 train_strategy_returns = train_predictions * train_returns

 results['train_metrics'] = {
 'sharpe': train_strategy_returns.mean() / train_strategy_returns.std() * np.sqrt(252) if train_strategy_returns.std() > 0 else 0,
 'max_drawdown': calculate_max_drawdown(train_strategy_returns),
 'total_return': train_strategy_returns.sum(),
 'annual_return': train_strategy_returns.mean() * 252,
 'volatility': train_strategy_returns.std() * np.sqrt(252)
 }

# metrics on test data
 results['test_metrics'] = {
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'annual_return': annual_return,
 'volatility': volatility
 }

 return results

# Example of use
results = time_series_backtest(data, model, train_size=0.7, test_size=0.3)
```

**To account for time dependencies:**

```python
def temporal_dependency_backtest(data, model, lookback=30, step=1,
 config=None, validation=True, random_state=None):
 """
Becketting with timing and detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 lookback : int, default=30
Number of periods for learning (lookback Windows)
- 30 means training on the last 30 periods
- Recommended 20-50 for most cases
- Less than 20 could lead to retraining.
- More than 50 could lead to a lack of education.

 step : int, default=1
Step between the iterations of the bactering
- 1 means testing each period
- More than 1 means pass periods
- Recommended 1 for maximum accuracy
- More than 1 for accreditation (but less accurate)

 config : dict, optional
Additional configuring for betting
- 'min_lookback':int, default=20 - minimum size of the learning window
- 'max_lookback':int, default=100 is the maximum size of the learning window
- 'min_step':int, default=1 - minimum step
- 'max_step':int, default=10 - maximum step
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correct trackback and step.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of the model
- It is recommended to ask for reproduction

 Returns:
 --------
 pd.dataFrame
DataFrame with the backtting results:
- 'data': datame - test date
- 'sharpe': float - Sharp factor of strategy
- 'return': flat - strategy return
- 'volatility': float - strategy volatility
- 'max_drawdown': float = maximum draught
- 'predications': np.array - model predictions (if return_predictations=True)
- 'training_size':int is the size of the learning sample
- 'test_size':int is the tests sample size

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the no model supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = temporal_dependency_backtest(data, model)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'min_lookback': 50,
 ... 'max_lookback': 200,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = temporal_dependency_backtest(data, model, lookback=50, step=5, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = temporal_dependency_backtest(data, model, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'min_lookback': 20,
 'max_lookback': 100,
 'min_step': 1,
 'max_step': 10,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < lookback + step:
Raise ValueError(f "Insufficient data. Minimum: {lookback + step}")

 if not (config['min_lookback'] <= lookback <= config['max_lookback']):
Raise ValueError(f'lookback should be between {config['min_lookback']} and {config['max_lookback']})

 if not (config['min_step'] <= step <= config['max_step']):
raise ValueError(f'step should be between {config['min_step']} and {config['max_step']}})

# Data production
 results = []
 total_iterations = (len(data) - lookback) // step

 if config['verbose']:
(f) "Starting back-up with ith {total_iterations} iterations")
Print(f) Learning Window: {lookback}periods}
prent(f"Shag: {step}periods")

# Basic Baactering Cycle
 for i in range(lookback, len(data) - step + 1, step):
 try:
# Training data
 train_data = data[i-lookback:i]

# Testsy data
 test_data = data[i:i+step]

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 total_return = strategy_returns.sum()
 volatility = strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)

# The result of iteration
 result = {
 'date': test_data.index[0],
 'sharpe': sharpe,
 'return': total_return,
 'volatility': volatility,
 'max_drawdown': max_drawdown,
 'train_size': len(train_data),
 'test_size': len(test_data)
 }

# Additional results
 if config['return_predictions']:
 result['predictions'] = predictions

 results.append(result)

 if config['verbose'] and (i - lookback) % (step * 10) == 0:
spring(f"COMPLETED: {i - lookback + 1} from {total_iterations} iterations")

 except Exception as e:
 if config['verbose']:
Print(f) Mistake on iteration {i}: {e})
 continue

 if not results:
Raise ValueError("not has been able to perform no camouflage).

 # create dataFrame
 results_df = pd.dataFrame(results)

 if config['verbose']:
(pint(f"Backetting complete. Successful iterations: {len(effects_df)})
pint(f"Medial Sharp coefficient: {results_df['sharpe']mean(:4f}")
pint(f" Average return: {results_df['return']mean(:4f}")

 return results_df

# Example of use
results = temporal_dependency_backtest(data, model, lookback=30, step=1)
```

♪##2 ♪ Monte Carlo Baektsing ♪

### The Monte-Carlo Becketting process

```mermaid
graph TD
A [Reference data] -> B [configration of parameters]
 B --> C[n_simulations = 1000]
 B --> D[confidence_level = 0.95]

C --> E [Simulation cycle]
 D --> E

E --> F[Incident data sampling<br/>80 per cent with replacement]
F --> G [Section on train/test<br/> 70 per cent / 30 per cent]

G -> H [model training]
H -> I [Treaties]
I -> J [Strategy return calculation]

J --> K[metrics simulations]
K-> L [Sharp coefficient]
K-> M[maximum draught]
K-> N [Total return]

L -> O [Compilation of results]
 M --> O
 N --> O

O --> P {All simulations<br/> are complete?}
P -->\\\\\E
P -->\\\Q[Statistical analysis]

Q -> R [Medical Sharpe coefficient]
Q -> S [standard deviation]
Q -> T [Confidence interval]

R -> U [Financial evaluation of the strategy]
 S --> U
 T --> U

U --> V {The Strategy is stable?}
V -->\\\\W[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\///\\\\\\\\\\////\///\/\/\/\/\/\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}}}}
V-~ ~ No~ X[~ Instable strategy]

 style A fill:#e3f2fd
 style E fill:#fff3e0
 style Q fill:#c8e6c9
 style W fill:#4caf50
 style X fill:#ffcdd2
```

** Simulation of multiple scenarios:**

```python
def monte_carlo_backtest(data, model, n_simulations=1000, confidence_level=0.95,
 config=None, validation=True, random_state=None):
 """
Monte Carlo Becketting with detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 n_simulations : int, default=1000
Number of simulations by Monte Carlo
- 1000 means 1,000 random samples
- Recommended 500-2000 for most cases
- Less than 500 can give inaccurate results.
- More than 2,000 may be too slow.

 confidence_level : float, default=0.95
Confidence level for confidence interval (0.0 < conference_level < 1.0)
- 0.95 means 95% confidence interval
Recommended 0.90-0.99 for most cases
- 0.90 gives a narrower interval
- 0.99 gives a wider interval

 config : dict, optional
Additional configuring for betting
- 'sample_frac': flat, default=0.8 is the percentage of data for the sample (0.0 < sample_frac < 1.0)
==Trin_frac==Float, default=0.7 is the share of data for learning (0.0 < tran_frac < 1.0)
- 'test_frac': flat, default=0.3 is the share of data for testing (0.0 < test_frac < 1.0)
- 'min_samples':int, default=100 = minimum number of samples in the sample
- 'max_samples':int, default=1000 = maximum number of samples in the sample
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'early_stopping': bell, default=False - stop when the criterion is reached
- 'Convergence_threshold': flat, default=0.01 - convergence threshold for life_stopping

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correct parameters.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 dict
The dictionary with the results of Monte Carlo betting:
- 'mean_sharpe': float = average Sharpe coefficient
- 'std_sharpe': float = standard deviation of Sharp coefficient
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- 'mean_total_return': flat = average total return
- 'std_total_return': flat = standard deviation of total return
- 'confidence_interval':List is the confidence interval for Sharp coefficient
- 'Percentiles': dict - percentiles for all metrics
- 'access_rate': flat = percentage of successful simulations (sharpe > 1.0)
- 'Results': pd.dataFrame - detailed results of all simulations
- 'config_Used':dict - used configuration

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the no model supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = monte_carlo_backtest(data, model)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'sample_frac': 0.9,
 ... 'train_frac': 0.8,
 ... 'test_frac': 0.2,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = monte_carlo_backtest(data, model, n_simulations=500, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = monte_carlo_backtest(data, model, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'sample_frac': 0.8,
 'train_frac': 0.7,
 'test_frac': 0.3,
 'min_samples': 100,
 'max_samples': 10000,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'early_stopping': False,
 'convergence_threshold': 0.01
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples']:
raise ValueError(f"Insufficient data. Minimum: {config['min_samples']})

 if not (0 < n_simulations <= 10000):
Raise ValueError("n_simulations should be between 1 and 10,000")

 if not (0 < confidence_level < 1):
Raise ValueError("confidence_level should be between 0 and 1)

 if not (0 < config['sample_frac'] < 1):
Raise ValueError("sample_frac should be between 0 and 1)

 if not (0 < config['train_frac'] < 1) or not (0 < config['test_frac'] < 1):
Raise ValueError("training_frac and test_frac should be between 0 and 1)

 if abs(config['train_frac'] + config['test_frac'] - 1.0) > 1e-6:
Raise ValueError("training_frac + test_frac shall be 1.0")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Data production
 results = []
 successful_simulations = 0

 if config['verbose']:
(f) Start Monte Carlo bactering with simulations)
(pint(f"Sample share: {config['ssample_frac']})
(pint(f "Learning rate: {config['training_frac']}})
(pint(f" Test rate: {config['test_frac']}})

# Basic simulation cycle
 for i in range(n_simulations):
 try:
# Random data sample
 sample_size = min(int(len(data) * config['sample_frac']), config['max_samples'])
 sample_data = data.sample(n=sample_size, replace=True)

# Separation on train/test
 split_point = int(len(sample_data) * config['train_frac'])
 train_data = sample_data[:split_point]
 test_data = sample_data[split_point:]

# check minimum number of samples
 if len(train_data) < config['min_samples'] or len(test_data) < config['min_samples']:
 continue

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()
 volatility = strategy_returns.std() * np.sqrt(252)
 annual_return = strategy_returns.mean() * 252

# The result of simulation
 result = {
 'simulation': i + 1,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'volatility': volatility,
 'annual_return': annual_return,
 'train_size': len(train_data),
 'test_size': len(test_data)
 }

# Additional results
 if config['return_predictions']:
 result['predictions'] = predictions

 results.append(result)
 successful_simulations += 1

 # Early stopping
 if config['early_stopping'] and i > 100:
 if i % 50 == 0:
 recent_sharpe = np.mean([r['sharpe'] for r in results[-50:]])
 if abs(recent_sharpe - np.mean([r['sharpe'] for r in results[-100:-50]])) < config['convergence_threshold']:
 if config['verbose']:
(f) Early stop on iteration {i+1} due to convergence)
 break

 if config['verbose'] and (i + 1) % 100 == 0:
(f"COMPLETED: {i + 1} from {n_simulations} simulations")

 except Exception as e:
 if config['verbose']:
Print(f) Error on simulation {i+1}: {e})
 continue

 if not results:
Raise ValueError("not has been able to perform no successful simulations")

 # create dataFrame
 results_df = pd.dataFrame(results)

# Statistical analysis
 mean_sharpe = results_df['sharpe'].mean()
 std_sharpe = results_df['sharpe'].std()
 mean_max_drawdown = results_df['max_drawdown'].mean()
 std_max_drawdown = results_df['max_drawdown'].std()
 mean_total_return = results_df['total_return'].mean()
 std_total_return = results_df['total_return'].std()

# Confidence interval
 confidence_interval = np.percentile(results_df['sharpe'],
 [100*(1-confidence_level)/2,
 100*(1+confidence_level)/2])

# Percentile
 percentiles = {
 'sharpe': np.percentile(results_df['sharpe'], [5, 25, 50, 75, 95]),
 'max_drawdown': np.percentile(results_df['max_drawdown'], [5, 25, 50, 75, 95]),
 'total_return': np.percentile(results_df['total_return'], [5, 25, 50, 75, 95])
 }

# Share of successful simulations
 success_rate = (results_df['sharpe'] > 1.0).mean()

# Final results
 final_results = {
 'mean_sharpe': mean_sharpe,
 'std_sharpe': std_sharpe,
 'mean_max_drawdown': mean_max_drawdown,
 'std_max_drawdown': std_max_drawdown,
 'mean_total_return': mean_total_return,
 'std_total_return': std_total_return,
 'confidence_interval': confidence_interval,
 'percentiles': percentiles,
 'success_rate': success_rate,
 'results': results_df,
 'config_Used': config.copy(),
 'successful_simulations': successful_simulations
 }

 if config['verbose']:
== sync, corrected by elderman == @elder_man
(f) Average Sharp coefficient: {mean_sharpe:.4f} ± {std_sharpe:.4f})
Print(f"Confidence interval (95 per cent): [{confidence_interval[0]:4f}, {conference_interval[1]:4f}]])
pprint(f) "Failure of successful simulations: {access_rate:2%}")

 return final_results

# Example of use
mc_results = monte_carlo_backtest(data, model, n_simulations=1000, confidence_level=0.95)
```

**Boutstrap Baektsing:**

```python
def bootstrap_backtest(data, model, n_bootstrap=1000, block_size=10,
 config=None, validation=True, random_state=None):
 """
Bottrap Backting with blocks and detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 n_bootstrap : int, default=1000
Number of iteration boots
- 1000 means 1,000 butstrap samples
- Recommended 500-2000 for most cases
- Less than 500 can give inaccurate results.
- More than 2,000 may be too slow.

 block_size : int, default=10
Size of block for butstrap
- 10 means blocks on 10 observations
- Recommended 5-20 for most cases
- Less than 5 could disrupt the time structure.
- More than 20 can produce less accurate results.

 config : dict, optional
Additional configuring for betting
==Trin_frac==Float, default=0.7 is the share of data for learning (0.0 < tran_frac < 1.0)
- 'test_frac': flat, default=0.3 is the share of data for testing (0.0 < test_frac < 1.0)
== sync, corrected by elderman == @elder_man
- 'max_locks':int, default=1000 - maximum number of blocks
- 'min_samples':int, default=100 = minimum number of samples in the sample
- 'max_samples':int, default=1000 = maximum number of samples in the sample
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'early_stopping': bell, default=False - stop when the criterion is reached
- 'Convergence_threshold': flat, default=0.01 - convergence threshold for life_stopping

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correct parameters.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 pd.dataFrame
DataFrame with the results of the battering boots:
- 'bootstrap':int is the number of the iteration booth.
- 'sharpe': float - Sharp factor of strategy
- 'max_drawdown': float = maximum draught
- 'Total_return': float - total strategy return
- 'volatility': float - strategy volatility
- 'annual_return': float - annual return
- 'training_size':int is the size of the learning sample
- 'test_size':int is the tests sample size
- 'n_locks':int is the number of blocks in the sample
- 'predications': np.array - model predictions (if return_predictations=True)

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the no model supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = bootstrap_backtest(data, model)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'train_frac': 0.8,
 ... 'test_frac': 0.2,
 ... 'block_size': 15,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = bootstrap_backtest(data, model, n_bootstrap=500, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = bootstrap_backtest(data, model, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'train_frac': 0.7,
 'test_frac': 0.3,
 'min_blocks': 10,
 'max_blocks': 1000,
 'min_samples': 100,
 'max_samples': 10000,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'early_stopping': False,
 'convergence_threshold': 0.01
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples']:
raise ValueError(f"Insufficient data. Minimum: {config['min_samples']})

 if not (0 < n_bootstrap <= 10000):
Raise ValueError("n_bootstrap should be between 1 and 10,000")

 if not (1 <= block_size <= 100):
Raise ValueError("block_size should be between 1 and 100")

 if not (0 < config['train_frac'] < 1) or not (0 < config['test_frac'] < 1):
Raise ValueError("training_frac and test_frac should be between 0 and 1)

 if abs(config['train_frac'] + config['test_frac'] - 1.0) > 1e-6:
Raise ValueError("training_frac + test_frac shall be 1.0")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Data production
 results = []
 successful_bootstraps = 0

 if config['verbose']:
(f) "Start battering with {n_bootstrap} iterations")
print(f) Unit measurement: {lock_size})
(pint(f "Learning rate: {config['training_frac']}})
(pint(f" Test rate: {config['test_frac']}})

# Basic Butstrap Cycle
 for i in range(n_bootstrap):
 try:
♪ the sample booth with blocks ♪
 bootstrap_data = []
 n_blocks = 0

# Random block selection
 while len(bootstrap_data) < config['min_samples'] and n_blocks < config['max_blocks']:
# Random selection of the initial index of the block
 start_idx = np.random.randint(0, len(data) - block_size + 1)
 block = data[start_idx:start_idx + block_size]

 if len(block) == block_size:
 bootstrap_data.append(block)
 n_blocks += 1

 if not bootstrap_data:
 continue

 bootstrap_data = pd.concat(bootstrap_data)

# check minimum number of samples
 if len(bootstrap_data) < config['min_samples']:
 continue

# Separation on train/test
 split_point = int(len(bootstrap_data) * config['train_frac'])
 train_data = bootstrap_data[:split_point]
 test_data = bootstrap_data[split_point:]

# check minimum number of samples
 if len(train_data) < config['min_samples'] or len(test_data) < config['min_samples']:
 continue

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()
 volatility = strategy_returns.std() * np.sqrt(252)
 annual_return = strategy_returns.mean() * 252

# The result of the boutstrap
 result = {
 'bootstrap': i + 1,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'volatility': volatility,
 'annual_return': annual_return,
 'train_size': len(train_data),
 'test_size': len(test_data),
 'n_blocks': n_blocks
 }

# Additional results
 if config['return_predictions']:
 result['predictions'] = predictions

 results.append(result)
 successful_bootstraps += 1

 # Early stopping
 if config['early_stopping'] and i > 100:
 if i % 50 == 0:
 recent_sharpe = np.mean([r['sharpe'] for r in results[-50:]])
 if abs(recent_sharpe - np.mean([r['sharpe'] for r in results[-100:-50]])) < config['convergence_threshold']:
 if config['verbose']:
(f) Early stop on iteration {i+1} due to convergence)
 break

 if config['verbose'] and (i + 1) % 100 == 0:
spring(f"COMPLETED: {i + 1} from {n_bootstrap} iterations)

 except Exception as e:
 if config['verbose']:
Print(f) Mistake on iteration boot {i+1}: {e})
 continue

 if not results:
Raise ValueError("not has been able to perform any successful iteration booths")

 # create dataFrame
 results_df = pd.dataFrame(results)

 if config['verbose']:
(f "Butstrap Baektezting Completed. Successful iterations: {accessfulful_botstraps}")
pint(f"Medial Sharp coefficient: {results_df['sharpe']mean(:4f}")
average return: {results_df['total_return'].mean(:4f})
pprint(f" Average number of blocks: {results_df['n_locks'].mean(:1f})

 return results_df

# Example of use
bootstrap_results = bootstrap_backtest(data, model, n_bootstrap=1000, block_size=10)
```

♪##3 ♪ Stressing ♪

♪# ♪ Stress-restraint scripts

```mermaid
graph TD
A[Reference data] -> B [Use of stress scenarios]

B --> C[market collapse<br/>volatility_multiplier: 3.0<br/>return_shift: -0.1]
B -> D[High volatility<br/>volatility_multiplier: 2.0<br/>return_shift: 0.0]
B --> E[Low volatility<br/>volatility_multiplier: 0.5<br/>return_shift: 0.0]
B --> F[market modes<br/>Regime Design]

C --> G [Learning on stress data]
 D --> G
 E --> G
 F --> G

G -> H [Treaties]
H -> I [Strategy return calculation]

I --> J[metrics stress test]
J --> K [Sharp coefficient]
J --> L [Maximum draught]
J-> M [Total return]

K --> N[comparison scenarios]
 L --> N
 M --> N

N -> O [Sustainability assessment]
O -> P[The Strategy is able to withstand the extreme conditions?]

P -->\\\\Q[\\\Robast Strategy]
P-~ ~ No~ R[~ Need to be improved]

Q -> S [Sixture in sales]
R -> T [Optimization of parameters]

T --> U [configuring risk-management]
U -> V [Re-testing]
 V --> B

 style A fill:#e3f2fd
 style C fill:#ffcdd2
 style D fill:#fff3e0
 style E fill:#e8f5e8
 style F fill:#f3e5f5
 style Q fill:#4caf50
 style R fill:#ff9800
```

** Test on extreme conditions:**

```python
def stress_test_backtest(data, model, stress_scenarios, config=None, validation=True, random_state=None):
 """
Stressing strategy with detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 stress_scenarios : dict
Vocabulary with stress-compressing scenarios
- Keys: scenario names (str)
- Values: script parameters (dict)
- examples of parameters:
- 'volatility_multiplier': float is a factor of volatility (1.0 = normal)
- 'return_shift': float = profit shift (0.0 = normal)
- 'correllation_multiplier': float is the correlation factor (1.0 = normal)
- 'liquidity_multiplier': flot = liquidity multiplier (1.0 = normal)
- 'regime_shift': str - market mode shift ('bull', 'bear', 'sideways')

 config : dict, optional
Additional configurization for Stress-Cancelling
==Trin_frac==Float, default=0.7 is the share of data for learning (0.0 < tran_frac < 1.0)
- 'test_frac': flat, default=0.3 is the share of data for testing (0.0 < test_frac < 1.0)
- 'min_samples':int, default=100 - minimum number of samples
- 'max_samples':int, default=1000 = maximum number of samples
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'Scenario_whites': dict, default= None - Weights for scenarios
- 'baseline_scenario':str, default='normaal' - Baseline scenario for comparison

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks scenarios.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 dict
Vocabulary with stress tweaking results:
- 'scenario_results':dict - results on each scenario
- 'Comparison_metrics':dict - Comparative metrics
- 'scenario_rankings': dict - ranking scenarios
- 'overall_assessment':dict - overall sustainability evaluation
- 'config_Used':dict - used configuration

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the no model supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> stress_scenarios = {
 ... 'market_crash': {'volatility_multiplier': 3.0, 'return_shift': -0.1},
 ... 'high_volatility': {'volatility_multiplier': 2.0, 'return_shift': 0.0},
 ... 'low_volatility': {'volatility_multiplier': 0.5, 'return_shift': 0.0}
 ... }
 >>> results = stress_test_backtest(data, model, stress_scenarios)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'train_frac': 0.8,
 ... 'test_frac': 0.2,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4,
 ... 'scenario_weights': {'market_crash': 0.5, 'high_volatility': 0.3, 'low_volatility': 0.2}
 ... }
 >>> results = stress_test_backtest(data, model, stress_scenarios, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = stress_test_backtest(data, model, stress_scenarios, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'train_frac': 0.7,
 'test_frac': 0.3,
 'min_samples': 100,
 'max_samples': 10000,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'scenario_weights': None,
 'baseline_scenario': 'normal'
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples']:
raise ValueError(f"Insufficient data. Minimum: {config['min_samples']})

 if not stress_scenarios:
Raise ValueError(" Stress-Cancelling scripts not specified")

 for scenario_name, scenario_params in stress_scenarios.items():
 if not isinstance(scenario_params, dict):
raise ValueError(f"parameters script '{scenario_name}' should be a dictionary")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Data production
 scenario_results = {}
 comparison_metrics = {}
 scenario_rankings = {}

 if config['verbose']:
prent(f) "Starting stress-disturbing with scenarios")
(pint(f "Learning rate: {config['training_frac']}})
(pint(f" Test rate: {config['test_frac']}})

# The main stress-compressing cycle
 for scenario_name, scenario_params in stress_scenarios.items():
 try:
 if config['verbose']:
print(f) "Try script: {scenario_name}")

# Stress scenario application
 stressed_data = apply_stress_scenario(data, scenario_params)

# check minimum number of samples
 if len(stressed_data) < config['min_samples']:
 if config['verbose']:
print(f"Slip the script '{scenario_name}': not enough data")
 continue

# Separation on train/test
 split_point = int(len(stressed_data) * config['train_frac'])
 train_data = stressed_data[:split_point]
 test_data = stressed_data[split_point:]

# check minimum number of samples
 if len(train_data) < config['min_samples'] or len(test_data) < config['min_samples']:
 if config['verbose']:
print(f"Skip the script '{scenario_name}': insufficient data for learning/testing")
 continue

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()
 volatility = strategy_returns.std() * np.sqrt(252)
 annual_return = strategy_returns.mean() * 252

# The result of the script
 scenario_result = {
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'volatility': volatility,
 'annual_return': annual_return,
 'train_size': len(train_data),
 'test_size': len(test_data),
 'scenario_params': scenario_params.copy()
 }

# Additional results
 if config['return_predictions']:
 scenario_result['predictions'] = predictions

 scenario_results[scenario_name] = scenario_result

 if config['verbose']:
"Sharpe: {sharpe:.4f}, Max DD: {max_drawdown:.4f})

 except Exception as e:
 if config['verbose']:
Print(f) Error in scenario '{scenario_name}': {e}}
 continue

 if not scenario_results:
Raise ValueError("not has been able to perform no successful stress-restraint scenario")

# Comparative analysis
 sharpe_values = [result['sharpe'] for result in scenario_results.values()]
 max_drawdown_values = [result['max_drawdown'] for result in scenario_results.values()]
 total_return_values = [result['total_return'] for result in scenario_results.values()]

 comparison_metrics = {
 'sharpe_range': [min(sharpe_values), max(sharpe_values)],
 'sharpe_std': np.std(sharpe_values),
 'max_drawdown_range': [min(max_drawdown_values), max(max_drawdown_values)],
 'max_drawdown_std': np.std(max_drawdown_values),
 'total_return_range': [min(total_return_values), max(total_return_values)],
 'total_return_std': np.std(total_return_values)
 }

# Earning scenarios
 scenario_rankings = {
 'by_sharpe': sorted(scenario_results.items(), key=lambda x: x[1]['sharpe'], reverse=True),
 'by_max_drawdown': sorted(scenario_results.items(), key=lambda x: x[1]['max_drawdown']),
 'by_total_return': sorted(scenario_results.items(), key=lambda x: x[1]['total_return'], reverse=True)
 }

# Overall sustainability assessment
 overall_assessment = {
 'is_robust': all(result['sharpe'] > 0.5 for result in scenario_results.values()),
 'is_stable': np.std(sharpe_values) < 1.0,
 'worst_scenario': min(scenario_results.items(), key=lambda x: x[1]['sharpe'])[0],
 'best_scenario': max(scenario_results.items(), key=lambda x: x[1]['sharpe'])[0],
 'average_sharpe': np.mean(sharpe_values),
 'average_max_drawdown': np.mean(max_drawdown_values),
 'scenarios_tested': len(scenario_results)
 }

# Final results
 final_results = {
 'scenario_results': scenario_results,
 'comparison_metrics': comparison_metrics,
 'scenario_rankings': scenario_rankings,
 'overall_assessment': overall_assessment,
 'config_Used': config.copy()
 }

 if config['verbose']:
Print(f"Stress-Certification complete. Scenarios challenged: {len(scenario_results)})
(f) Average Sharp coefficient: {overall_assessment['overage_sharpe']:4f})
(f "Strategy of Robast: {overall_assessment['is_robus']}")
(f "Strategy stable: {overall_assessment['is_stable']}})

 return final_results

# Example of use
stress_scenarios = {
 'market_crash': {'volatility_multiplier': 3.0, 'return_shift': -0.1},
 'high_volatility': {'volatility_multiplier': 2.0, 'return_shift': 0.0},
 'low_volatility': {'volatility_multiplier': 0.5, 'return_shift': 0.0}
}

stress_results = stress_test_backtest(data, model, stress_scenarios)
```

** Test on different market regimes:**

```python
def regime_based_backtest(data, model, regime_detector, config=None, validation=True, random_state=None):
 """
Becketting on different market regimes with detailed parameters

 Parameters:
 -----------
 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 model : object
ML model with Fit() and predict()
- Should support fit(X, y) for learning.
- Should support predict(X) for preferences
- It is recommended to use TabularPredictor from AutoGluon

 regime_detector : object
Market Modes Detector with Detect_Regimes()
- Should support protection_regimes(data) -> pd.Series
- Returns Series with regimes for each observation
- It is recommended to use Hidden Markov Model or an an Logsic methhods

 config : dict, optional
Additional configuring for betting
==Trin_frac==Float, default=0.7 is the share of data for learning (0.0 < tran_frac < 1.0)
- 'test_frac': flat, default=0.3 is the share of data for testing (0.0 < test_frac < 1.0)
== sync, corrected by elderman == @elder_man
- 'max_regimes':int, default=10 - maximum number of modes
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'regime_whites': dict, default= None - Weights for Modes
- 'baseline_regime': str, default= None - basic mode for comparison

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correct mode detector

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 dict
Vocabulary with back-up results on modes:
- 'regime_results':dict - results on each mode
- 'Comparison_metrics':dict - Comparative metrics
- 'regime_rankings': dict - mode ranking
- 'overall_assessment':dict - general estimate on modes
- 'regime_transitions':dict - inter-mode transition analysis
- 'config_Used':dict - used configuration

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If the mode detector model not supports the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = regime_based_backtest(data, model, regime_detector)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'train_frac': 0.8,
 ... 'test_frac': 0.2,
 ... 'min_samples_per_regime': 100,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = regime_based_backtest(data, model, regime_detector, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = regime_based_backtest(data, model, regime_detector, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'train_frac': 0.7,
 'test_frac': 0.3,
 'min_samples_per_regime': 50,
 'max_regimes': 10,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'regime_weights': None,
 'baseline_regime': None
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples_per_regime'] * 2:
Minimum: {config['min_samples_per_regime'] *2})

 if not hasattr(regime_detector, 'detect_regimes'):
raise TypeError("The mode detector shall have a protective_regimes() method")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Definition of regimes
 try:
 regimes = regime_detector.detect_regimes(data)
 except Exception as e:
Raise TypeError(f" Mode detector error: {e}")

 if len(regimes) != len(data):
Raise ValueError("The length of modes n corresponds to the length of data")

# Data production
 regime_results = {}
 comparison_metrics = {}
 regime_rankings = {}
 regime_transitions = {}

 if config['verbose']:
Print(f) "Backing on Modes")
Print(f"Provided modes: {len(regimes.unique()}})
(pint(f "Learning rate: {config['training_frac']}})
(pint(f" Test rate: {config['test_frac']}})

# The main round of back-up on modes
 for regime in regimes.unique():
 try:
 if config['verbose']:
print(f) "Try mode: {regime}")

# Data for Mode
 regime_data = data[regimes == regime]

# check minimum number of samples
 if len(regime_data) < config['min_samples_per_regime']:
 if config['verbose']:
print(f"Slip '{regime}': insufficient data ({len(regime_data)} < {config['min_samples_per_regime']}))
 continue

# Separation on train/test
 split_point = int(len(regime_data) * config['train_frac'])
 train_data = regime_data[:split_point]
 test_data = regime_data[split_point:]

# check minimum number of samples
 if len(train_data) < config['min_samples_per_regime'] // 2 or len(test_data) < config['min_samples_per_regime'] // 2:
 if config['verbose']:
print(f"Slip the mode `{regime}': insufficient data for learning/testing")
 continue

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# Basic metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()
 volatility = strategy_returns.std() * np.sqrt(252)
 annual_return = strategy_returns.mean() * 252

# The result of the regime
 regime_result = {
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'volatility': volatility,
 'annual_return': annual_return,
 'train_size': len(train_data),
 'test_size': len(test_data),
 'regime_size': len(regime_data),
 'regime_frequency': len(regime_data) / len(data)
 }

# Additional results
 if config['return_predictions']:
 regime_result['predictions'] = predictions

 regime_results[regime] = regime_result

 if config['verbose']:
"Sharpe: {sharpe:.4f}, Max DD: {max_drawdown:.4f}")

 except Exception as e:
 if config['verbose']:
print(f) Error in mode '{regime}': {e}}
 continue

 if not regime_results:
Raise ValueError("not has been able to perform no successful betting mode")

# Comparative analysis
 sharpe_values = [result['sharpe'] for result in regime_results.values()]
 max_drawdown_values = [result['max_drawdown'] for result in regime_results.values()]
 total_return_values = [result['total_return'] for result in regime_results.values()]
 regime_frequencies = [result['regime_frequency'] for result in regime_results.values()]

 comparison_metrics = {
 'sharpe_range': [min(sharpe_values), max(sharpe_values)],
 'sharpe_std': np.std(sharpe_values),
 'max_drawdown_range': [min(max_drawdown_values), max(max_drawdown_values)],
 'max_drawdown_std': np.std(max_drawdown_values),
 'total_return_range': [min(total_return_values), max(total_return_values)],
 'total_return_std': np.std(total_return_values),
 'regime_frequency_range': [min(regime_frequencies), max(regime_frequencies)],
 'regime_frequency_std': np.std(regime_frequencies)
 }

# Absorbing regimes
 regime_rankings = {
 'by_sharpe': sorted(regime_results.items(), key=lambda x: x[1]['sharpe'], reverse=True),
 'by_max_drawdown': sorted(regime_results.items(), key=lambda x: x[1]['max_drawdown']),
 'by_total_return': sorted(regime_results.items(), key=lambda x: x[1]['total_return'], reverse=True),
 'by_frequency': sorted(regime_results.items(), key=lambda x: x[1]['regime_frequency'], reverse=True)
 }

# Analysis of inter-mode crossings
 regime_transitions = {
 'transition_matrix': calculate_transition_matrix(regimes),
 'transition_probabilities': calculate_transition_probabilities(regimes),
 'regime_durations': calculate_regime_durations(regimes),
 'regime_stability': calculate_regime_stability(regimes)
 }

# General assessment on regimes
 overall_assessment = {
 'is_robust': all(result['sharpe'] > 0.5 for result in regime_results.values()),
 'is_stable': np.std(sharpe_values) < 1.0,
 'worst_regime': min(regime_results.items(), key=lambda x: x[1]['sharpe'])[0],
 'best_regime': max(regime_results.items(), key=lambda x: x[1]['sharpe'])[0],
 'average_sharpe': np.mean(sharpe_values),
 'average_max_drawdown': np.mean(max_drawdown_values),
 'regimes_tested': len(regime_results),
 'regime_diversity': len(regime_results) / len(regimes.unique())
 }

# Final results
 final_results = {
 'regime_results': regime_results,
 'comparison_metrics': comparison_metrics,
 'regime_rankings': regime_rankings,
 'overall_assessment': overall_assessment,
 'regime_transitions': regime_transitions,
 'config_Used': config.copy()
 }

 if config['verbose']:
pint(f"Backetting on Modes completed. Objection to Modes: {len(regime_results)})
(f) Average Sharp coefficient: {overall_assessment['overage_sharpe']:4f})
(f "Strategy of Robast: {overall_assessment['is_robus']}")
(f "Strategy stable: {overall_assessment['is_stable']}})
(f "Diversity of modes: {overall_assessment['regime_diversity']:2%}")

 return final_results

# Example of use
regime_results = regime_based_backtest(data, model, regime_detector)
```

♪##4 ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪ ♪

### Architecture of portfolio buffering

```mermaid
graph TD
A[Postfel strategy] --> B [Strategy 1<br/>40% weight]
A -> C[Strategy 2<br/> 30 per cent weight]
A -> D[Strategy 3<br/> 30 per cent weight]

B -> E [Strategy 1 projection]
C -> F [Strategy 2 projection]
D -> G [Strategy 3 prognosis]

E --> H [Reweighting preferences]
 F --> H
 G --> H

H --> I [weighted predictions<br/>w1*p1 + w2*p2 + w3*p3]

I -> J [market returns]
J --> K[Portle returns<br/>weated_predations * returns]

K --> L[metrics portfolio]
L-> M[Sharp portfolio ratio]
L --> N [Maximum portfolio spread]
L -> O [Total return on portfolio]

M --> P [Portfolio evaluation]
 N --> P
 O --> P

P --> Q [Dynamic rebalancing]
Q -> R [Calculation of new weights<br/>on base performance]

R --> S[update balance]
S --> T [New iteration of the bactering]
 T --> H

P --> U[comparison with benchmarking]
U-> V[Alpha and Beta coefficients]
U -> W [Information ratio]

V -> X [Financial evaluation of the portfolio]
 W --> X

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
 style X fill:#4caf50
```

** Policy portfolio audit:**

```python
def Portfolio_backtest(strategies, data, weights=None, rebalance_freq='M',
 config=None, validation=True, random_state=None):
 """
Becketting the strategy portfolio with detailed parameters

 Parameters:
 -----------
 strategies : List
List of strategies for the portfolio
- Each strategy has to have methods fit() and predict()
- It is recommended to use TabularPredictor from AutoGluon
- Minimum 2 strategies for diversification

 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 weights : array-like, optional
Weights for strategies in the portfolio
- If None, even distribution is used
- To be added to 1.0
- Balance optimization recommended

 rebalance_freq : str, default='M'
Portfolio rebalancing frequency
- 'D' - daily.
- 'W' - weekly
- 'M' - monthly
- 'Q' - quarterly
- 'Y' - every year.
- Recommended 'M' for most cases

 config : dict, optional
Additional configuring for portfolio buffering
==Trin_frac==Float, default=0.7 is the share of data for learning (0.0 < tran_frac < 1.0)
- 'test_frac': flat, default=0.3 is the share of data for testing (0.0 < test_frac < 1.0)
- 'min_samples':int, default=100 - minimum number of samples
- 'max_samples':int, default=1000 = maximum number of samples
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'rebalance_method': str, default='fixed' - rebalancing method ('fixed', 'dynamic', 'adaptive')
- 'transaction_costs': flat, default=0.001 - transaction costs (0.0-0.01)
- 'slippage': flat, default=0.005 - slip (0.0-0.005)
- 'max_white': flat, default=0.5 - maximum weight of one strategy
- 'min_white': flat, default=0.05 - minimum weight of one strategy

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the correct policies and weights.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 dict
Vocabulary with portfoliobacking results:
- 'Porthfolio_metrics': dict - metrics portfolio
- 'Individual_metrics': dict - metrics of selected strategies
- 'rebalancing_info':dict - rebalancing information
- 'risk_metrics': dict - risk metrics portfolio
- 'diversification_metrics': dict - metrics diversification
- 'config_Used':dict - used configuration

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If no strategies support the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = Portfolio_backtest(strategies, data)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'train_frac': 0.8,
 ... 'test_frac': 0.2,
 ... 'rebalance_method': 'dynamic',
 ... 'transaction_costs': 0.002,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = Portfolio_backtest(strategies, data, weights=[0.4, 0.3, 0.3], config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = Portfolio_backtest(strategies, data, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'train_frac': 0.7,
 'test_frac': 0.3,
 'min_samples': 100,
 'max_samples': 10000,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'rebalance_method': 'fixed',
 'transaction_costs': 0.001,
 'slippage': 0.0005,
 'max_weight': 0.5,
 'min_weight': 0.05
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples']:
raise ValueError(f"Insufficient data. Minimum: {config['min_samples']})

 if len(strategies) < 2:
Raise ValueError

 for i, strategy in enumerate(strategies):
 if not hasattr(strategy, 'fit') or not hasattr(strategy, 'predict'):
Raise TypeError(f"The strategy {i} shall have methods fat() and predict()")

 if weights is not None:
 if len(weights) != len(strategies):
Raise ValueError("Number of weights should correspond to number of strategies")

 if abs(sum(weights) - 1.0) > 1e-6:
Raise ValueError("The weights shall be added to 1.0")

 if any(w < 0 for w in weights):
Raise ValueError ("No weights may be negative")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Weight preparation
 if weights is None:
 weights = np.ones(len(strategies)) / len(strategies)

 weights = np.array(weights)

# Normalization of weights
 weights = weights / weights.sum()

# Application of weight limits
 weights = np.clip(weights, config['min_weight'], config['max_weight'])
 weights = weights / weights.sum()

 if config['verbose']:
(f) Start portfolio buffering with strategies)
(f "Strategy Weights: {weights}")
Print(f "Rebalancing rate: {reballance_freq}")
(pint(f "Learning rate: {config['training_frac']}})
(pint(f" Test rate: {config['test_frac']}})

# Data sharing
 split_point = int(len(data) * config['train_frac'])
 train_data = data[:split_point]
 test_data = data[split_point:]

# Training strategies
 if config['verbose']:
Print("Strategy training...")

 for i, strategy in enumerate(strategies):
 try:
 strategy.fit(train_data)
 if config['verbose']:
(f "Strategy {i+1} trained")
 except Exception as e:
 if config['verbose']:
Print(f) "A mistake in learning strategy {i+1}: {e}")
 continue

# Getting Preventions from All Strategies
 predictions = {}
 individual_returns = {}

 for i, strategy in enumerate(strategies):
 try:
 pred = strategy.predict(test_data)
 predictions[f'strategy_{i}'] = pred
 individual_returns[f'strategy_{i}'] = pred * test_data['returns']
 except Exception as e:
 if config['verbose']:
Print(f) "The error in the prediction of strategy {i+1}: {e}")
 continue

 if not predictions:
Raise ValueError("not has been able to obtain predictions from no one strategy")

# Create dataFrame with predictions
 predictions_df = pd.dataFrame(predictions)

# Weighting preferences
 weighted_predictions = (predictions_df * weights).sum(axis=1)

# Calculation of portfolio returns
 returns = test_data['returns']
 Portfolio_returns = weighted_predictions * returns

# Applying transaction costs and slipping
 if config['transaction_costs'] > 0 or config['slippage'] > 0:
 total_costs = config['transaction_costs'] + config['slippage']
 Portfolio_returns = Portfolio_returns - total_costs

# Basic metrics portfolio
 sharpe = Portfolio_returns.mean() / Portfolio_returns.std() * np.sqrt(252) if Portfolio_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(Portfolio_returns)
 total_return = Portfolio_returns.sum()
 volatility = Portfolio_returns.std() * np.sqrt(252)
 annual_return = Portfolio_returns.mean() * 252

# metrics portfolio
 Portfolio_metrics = {
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'volatility': volatility,
 'annual_return': annual_return,
 'weights': weights.toList()
 }

# Metrics selected strategies
 individual_metrics = {}
 for strategy_name, strategy_returns in individual_returns.items():
 individual_metrics[strategy_name] = {
 'sharpe': strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0,
 'max_drawdown': calculate_max_drawdown(strategy_returns),
 'total_return': strategy_returns.sum(),
 'volatility': strategy_returns.std() * np.sqrt(252),
 'annual_return': strategy_returns.mean() * 252
 }

# Information on rebalancing
 rebalancing_info = {
 'frequency': rebalance_freq,
 'method': config['rebalance_method'],
 'transaction_costs': config['transaction_costs'],
 'slippage': config['slippage'],
 'total_costs': config['transaction_costs'] + config['slippage']
 }

♪ risk packages ♪
 risk_metrics = {
 'var_95': np.percentile(Portfolio_returns, 5),
 'var_99': np.percentile(Portfolio_returns, 1),
 'cvar_95': Portfolio_returns[Portfolio_returns <= np.percentile(Portfolio_returns, 5)].mean(),
 'cvar_99': Portfolio_returns[Portfolio_returns <= np.percentile(Portfolio_returns, 1)].mean(),
 'skewness': Portfolio_returns.skew(),
 'kurtosis': Portfolio_returns.kurtosis()
 }

# metrics diversification
 diversification_metrics = {
 'effective_n': 1 / (weights ** 2).sum(),
 'concentration_index': (weights ** 2).sum(),
 'herfindahl_index': (weights ** 2).sum(),
 'gini_coefficient': calculate_gini_coefficient(weights),
 'entropy': -np.sum(weights * np.log(weights + 1e-10))
 }

# Final results
 final_results = {
 'Portfolio_metrics': Portfolio_metrics,
 'individual_metrics': individual_metrics,
 'rebalancing_info': rebalancing_info,
 'risk_metrics': risk_metrics,
 'diversification_metrics': diversification_metrics,
 'config_Used': config.copy()
 }

# Additional results
 if config['return_predictions']:
 final_results['predictions'] = predictions_df
 final_results['weighted_predictions'] = weighted_predictions

 if config['return_metrics']:
 final_results['Portfolio_returns'] = Portfolio_returns
 final_results['individual_returns'] = individual_returns

 if config['verbose']:
prent(f "Portphel Baactering Completed")
(f "Sharp portfolio: {sharpe:.4f}")
print(f "Maximal prosperity: {max_drawdown:.4f}")
"Total_return:.4f}")
(f "Efficient number of strategies: {diveration_metrics['effective_n']:2f}")

 return final_results

# Example of use
Portfolio_results = Portfolio_backtest(strategies, data, weights=[0.4, 0.3, 0.3])
```

** Dynamic rebalancing:**

```python
def dynamic_rebalance_backtest(strategies, data, rebalance_freq='M',
 lookback_window=252, config=None, validation=True, random_state=None):
 """
Battering with dynamic rebalancing and detailed parameters

 Parameters:
 -----------
 strategies : List
List of strategies for the portfolio
- Each strategy has to have methods fit() and predict()
- It is recommended to use TabularPredictor from AutoGluon
- Minimum 2 strategies for diversification

 data : pd.dataFrame
temporary data series with columns 'returns' and other signature
- Should be sorted in time
- Shall contain a column "returns" with returns
- A minimum of 1,000 observations are recommended for reliability

 rebalance_freq : str, default='M'
Portfolio rebalancing frequency
- 'D' - daily.
- 'W' - weekly
- 'M' - monthly
- 'Q' - quarterly
- 'Y' - every year.
- Recommended 'M' for most cases

 lookback_window : int, default=252
Window for learning strategies (in days)
- 252 means learning on the last 252 days
- Recommended 100-500 for most cases
- Less than 100 could lead to retraining.
- More than 500 could lead to a lack of education.

 config : dict, optional
Additional configuring for dynamic buffering
- 'test_window':int, default=30 - test window (in days)
- 'min_samples':int, default=100 - minimum number of samples
- 'max_samples':int, default=1000 = maximum number of samples
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'parallel': bool, default=False - use parallel calculations
- 'n_jobs':int, default=1 - number of processes for parallel calculations
- 'rebalance_method': str, default='performance' - rebalancing method ('performance', 'volatility', 'momentum', 'adaptive')
- 'transaction_costs': flat, default=0.001 - transaction costs (0.0-0.01)
- 'slippage': flat, default=0.005 - slip (0.0-0.005)
- 'max_white': flat, default=0.5 - maximum weight of one strategy
- 'min_white': flat, default=0.05 - minimum weight of one strategy
- 'weight_smoothing': flat, default=0.1 - balance smoothing (0.0-1.0)
- 'Performance_lookback':int, default=30 - window for calculating performance (in days)
- 'volatility_lookback':int, default=30 - window for calculating volatility (in days)
- 'momentum_lookback':int, default=30 - window for calculating momentum (in days)

 validation : bool, default=True
Whether to validate input data
- Checks out the 'returns' column.
- Checks data adequacy
- Checks the strategies.

 random_state : int, optional
Seed for reproducible results
- Used for initialization of random number generator
- It is recommended to ask for reproduction

 Returns:
 --------
 pd.dataFrame
DataFrame with dynamic buffering results:
- 'data': datatime - rebalancing date
- 'sharpe': float - Sharp index of the portfolio
- 'return': float - portfolio return
- 'volatility': float - portfolio volatility
- 'max_drawdown': float = maximum draught
- 'weights': List - the weight of strategies
- 'rebalance_cost': float - rebalancing cost
- 'Strategy_returns': dict - returns of selected strategies
- 'predications':dict - strategy predictions (if return_predictations=True)

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If no strategies support the necessary methhods

 Examples:
 ---------
>># Basic use
 >>> results = dynamic_rebalance_backtest(strategies, data)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'test_window': 60,
 ... 'rebalance_method': 'adaptive',
 ... 'transaction_costs': 0.002,
 ... 'verbose': True,
 ... 'parallel': True,
 ... 'n_jobs': 4
 ... }
 >>> results = dynamic_rebalance_backtest(strategies, data, lookback_window=500, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> results = dynamic_rebalance_backtest(strategies, data, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'test_window': 30,
 'min_samples': 100,
 'max_samples': 10000,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'parallel': False,
 'n_jobs': 1,
 'rebalance_method': 'performance',
 'transaction_costs': 0.001,
 'slippage': 0.0005,
 'max_weight': 0.5,
 'min_weight': 0.05,
 'weight_smoothing': 0.1,
 'performance_lookback': 30,
 'volatility_lookback': 30,
 'momentum_lookback': 30
 }

# Validation of input data
 if validation:
 if 'returns' not in data.columns:
Raise ValueError

 if len(data) < config['min_samples']:
raise ValueError(f"Insufficient data. Minimum: {config['min_samples']})

 if len(strategies) < 2:
Raise ValueError

 for i, strategy in enumerate(strategies):
 if not hasattr(strategy, 'fit') or not hasattr(strategy, 'predict'):
Raise TypeError(f"The strategy {i} shall have methods fat() and predict()")

 # installation random_state
 if random_state is not None:
 np.random.seed(random_state)

# Data production
 results = []
 previous_weights = None

 if config['verbose']:
(f) Start dynamic buffering with strategies)
Print(f) Learning window: {lookback_wind}days}
pprint(f) Test window: {config['test_window']} days")
Print(f "Rebalancing rate: {reballance_freq}")
(f "Rebalancing method: {config['rebalance_method']}})

# Basic dynamic buffering cycle
 for i in range(lookback_window, len(data) - config['test_window'] + 1, config['test_window']):
 try:
# Training data
 train_data = data[i-lookback_window:i]

# Testsy data
 test_data = data[i:i+config['test_window']]

# Learning all strategies
 strategy_predictions = {}
 strategy_returns = {}

 for j, strategy in enumerate(strategies):
 try:
 strategy.fit(train_data)
 pred = strategy.predict(test_data)
 strategy_predictions[f'strategy_{j}'] = pred
 strategy_returns[f'strategy_{j}'] = pred * test_data['returns']
 except Exception as e:
 if config['verbose']:
(f) Strategy error {j+1} on iteration {i}: {e})
 continue

 if not strategy_predictions:
 if config['verbose']:
Print(f"Skip iteration {i}: no successful strategies")
 continue

# Calculation of weights on basis of the chosen method
 if config['rebalance_method'] == 'performance':
 weights = calculate_performance_weights(strategy_returns, train_data, config)
 elif config['rebalance_method'] == 'volatility':
 weights = calculate_volatility_weights(strategy_returns, train_data, config)
 elif config['rebalance_method'] == 'momentum':
 weights = calculate_momentum_weights(strategy_returns, train_data, config)
 elif config['rebalance_method'] == 'adaptive':
 weights = calculate_adaptive_weights(strategy_returns, train_data, config)
 else:
# Equitable distribution
 weights = np.ones(len(strategy_predictions)) / len(strategy_predictions)

# Application of weight limits
 weights = np.clip(weights, config['min_weight'], config['max_weight'])
 weights = weights / weights.sum()

# Balance smoothing
 if previous_weights is not None and config['weight_smoothing'] > 0:
 weights = (1 - config['weight_smoothing']) * weights + config['weight_smoothing'] * previous_weights

# Weighting preferences
 weighted_predictions = sum(w * p for w, p in zip(weights, strategy_predictions.values()))

# Calculation of portfolio returns
 returns = test_data['returns']
 Portfolio_returns = weighted_predictions * returns

# Applying transaction costs and slipping
 rebalance_cost = 0.0
 if previous_weights is not None:
 weight_change = np.abs(weights - previous_weights).sum()
 rebalance_cost = weight_change * (config['transaction_costs'] + config['slippage'])
 Portfolio_returns = Portfolio_returns - rebalance_cost

# Basic metrics
 sharpe = Portfolio_returns.mean() / Portfolio_returns.std() * np.sqrt(252) if Portfolio_returns.std() > 0 else 0
 max_drawdown = calculate_max_drawdown(Portfolio_returns)
 total_return = Portfolio_returns.sum()
 volatility = Portfolio_returns.std() * np.sqrt(252)

# The result of iteration
 result = {
 'date': test_data.index[0],
 'sharpe': sharpe,
 'return': total_return,
 'volatility': volatility,
 'max_drawdown': max_drawdown,
 'weights': weights.toList(),
 'rebalance_cost': rebalance_cost,
 'strategy_returns': {k: v.sum() for k, v in strategy_returns.items()}
 }

# Additional results
 if config['return_predictions']:
 result['predictions'] = strategy_predictions

 results.append(result)
 previous_weights = weights.copy()

 if config['verbose'] and len(results) % 10 == 0:
(f"COMPLETED Iterations: {len(results)})

 except Exception as e:
 if config['verbose']:
Print(f) Mistake on iteration {i}: {e})
 continue

 if not results:
raise ValueError("not has been able to perform no successful iteration of dynamic buffering")

 # create dataFrame
 results_df = pd.dataFrame(results)

 if config['verbose']:
(pint(f) "Dynamic backup complete. Successful iterations: {len(results_df)}")
pint(f"Medial Sharp coefficient: {results_df['sharpe']mean(:4f}")
pint(f" Average return: {results_df['return']mean(:4f}")
"Total cost of rebalancing: {results_df['rebalance_cost'].sum(:4f}")

 return results_df

# Example of use
dynamic_results = dynamic_rebalance_backtest(strategies, data, rebalance_freq='M')
```

## metrics quality bactering

### ♪ Becketting quality metric classification

```mermaid
graph TD
A[metrics of betting quality] -> B [Base-based metrics]
A-> C [Processed metrics]
A --> D[Metrics performance]

B -> B1 [income and risk]
B1-> B11 [Total return]
B1 -> B12 [annual return]
B1-> B13 [Volatility]
B1-> B14 [Sharp coefficient]
B1-> B15 [Maximum draught]
B1-> B16 [Sortino Coefficient]

C --> C1 [Metrics stability]
C1-> C11 [Slip factor Sharp]
C1-> C12 [Stable of Sharp coefficient]
C1-> C13 [Optional factor]
C1-> C14 [Stable factor]

C --> C2 [risk metrics]
 C2 --> C21[Value at Risk - VaR]
 C2 --> C22[Conditional VaR - CVaR]
 C2 --> C23[Expected Shortfall]
C2-> C24 [Calmar coefficient]
C2-> C25 [Sterling coefficient]

D --> D1[metrics effectiveness]
D1-> D11 [Beta coefficient]
D1-> D12 [Alpha index]
D1-> D13 [Information ratio]
D1-> D14 [Trenor coefficient]
D1-> D15 [Gensen coefficient]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
```

*## 1. Basic metrics

** Income and risk:**

```python
def calculate_basic_metrics(returns, config=None, validation=True):
 """
Calculation of the basic metric with detailed parameters

 Parameters:
 -----------
 returns : pd.Series or np.array
temporary number of strategy returns
- Shall contain numerical values
- A minimum of 100 observations for reliability are recommended
- May contain NaN, which will be ignored

 config : dict, optional
Additional conference for the calculation of metrics
- 'trade_days':int, default=252 - number of trade days in year
- 'risk_free_rate': flat, default=0.0 - risk-free rate (0.0-0.1)
- 'min_periods':int, default=30 = minimum number periods for calculation
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'Include_skeewness': bool, default=True - include asymmetries
- 'Include_curtosis': bool, default=True - include excess
- 'Include_jarque_bera': bool, default=True - turn on the test of Hark-Bera
- 'Include_autocorr': bool, default=True - turn on autocorration
- 'Include_state': bool, default=True - turn on the stability test

 validation : bool, default=True
Whether to validate input data
- Checks the data availability.
- Checks data adequacy
- Checks the correct parameters.

 Returns:
 --------
 dict
The dictionary with basic metrics:
- 'Total_return': float - total return
- 'annual_return': float - annual return
- 'volatility': float - volatility (annual)
- 'sharpe': float - Sharpe coefficient
- 'max_drawdown': float = maximum draught
- 'sortino': float - Sortino coefficient
- 'calmar': float - Calmar coefficient
- 'Sterling': float - Sterling coefficient
- 'skewness': float is asymmetrical (if include_skewness=True)
- 'curtosis': float is an excession (if include_curtosis=True)
- 'jarque_bera': dict - Test of Hark-Bera (if include_jarque_bera=True)
- 'autocorr': dict - autocorration (if include_autocorr=True)
- 'Stationarity': dict - stability test (if include_state=True)

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If data not are numerical

 Examples:
 ---------
>># Basic use
 >>> metrics = calculate_basic_metrics(strategy_returns)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'trading_days': 365,
 ... 'risk_free_rate': 0.02,
 ... 'min_periods': 50,
 ... 'verbose': True
 ... }
 >>> metrics = calculate_basic_metrics(strategy_returns, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> metrics = calculate_basic_metrics(strategy_returns, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'trading_days': 252,
 'risk_free_rate': 0.0,
 'min_periods': 30,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'include_skewness': True,
 'include_kurtosis': True,
 'include_jarque_bera': True,
 'include_autocorr': True,
 'include_stationarity': True
 }

# Validation of input data
 if validation:
 if len(returns) < config['min_periods']:
raise ValueError(f"Insufficient data. Minimum: {config['min_periods']})

 if not np.isfinite(returns).any():
Raise ValueError("data nt contains final values")

 if not (0 < config['trading_days'] <= 365):
Raise ValueError("trading_days should be between 1 and 365)

 if not (0 <= config['risk_free_rate'] <= 1):
Raise ValueError("risk_free_rate should be between 0 and 1)

# Clear data
 returns_clean = returns.dropna() if hasattr(returns, 'dropna') else returns[~np.isnan(returns)]

 if len(returns_clean) < config['min_periods']:
raise ValueError(f"After cleaning insufficient data.

 if config['verbose']:
pprint(f) "Calculation of basic metrics for {len(returns_clean}}observations")
(f "Trade days in year: {`trade_days'}")
pprint(f"Risk rate: {config['risk_free_rate']:2%}})

# Basic metrics
 total_return = returns_clean.sum()
 annual_return = returns_clean.mean() * config['trading_days']
 volatility = returns_clean.std() * np.sqrt(config['trading_days'])

# Sharpe coefficient
 excess_return = annual_return - config['risk_free_rate']
 sharpe = excess_return / volatility if volatility > 0 else 0

# Maximum tarmac
 max_drawdown = calculate_max_drawdown(returns_clean)

# The Sortino coefficient
 downside_returns = returns_clean[returns_clean < 0]
 downside_volatility = downside_returns.std() * np.sqrt(config['trading_days']) if len(downside_returns) > 0 else 0
 sortino = excess_return / downside_volatility if downside_volatility > 0 else 0

# Calmar coefficient
 calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0

# Sterling coefficient
 sterling = annual_return / abs(returns_clean.min()) if returns_clean.min() != 0 else 0

# Results
 results = {
 'total_return': total_return,
 'annual_return': annual_return,
 'volatility': volatility,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'sortino': sortino,
 'calmar': calmar,
 'sterling': sterling
 }

# Additional metrics
 if config['include_skewness']:
 results['skewness'] = returns_clean.skew() if hasattr(returns_clean, 'skew') else scipy.stats.skew(returns_clean)

 if config['include_kurtosis']:
 results['kurtosis'] = returns_clean.kurtosis() if hasattr(returns_clean, 'kurtosis') else scipy.stats.kurtosis(returns_clean)

 if config['include_jarque_bera']:
 try:
 from scipy import stats
 jb_stat, jb_pvalue = stats.jarque_bera(returns_clean)
 results['jarque_bera'] = {
 'statistic': jb_stat,
 'pvalue': jb_pvalue,
 'is_normal': jb_pvalue > 0.05
 }
 except importError:
 if config['verbose']:
"scipy not installed, miss the Hot-Ber test"

 if config['include_autocorr']:
 try:
 from statsmodels.tsa.stattools import acf
 autocorr = acf(returns_clean, nlags=10, fft=False)
 results['autocorr'] = {
 'lags': List(range(len(autocorr))),
 'values': autocorr.toList(),
 'max_autocorr': np.max(np.abs(autocorr[1:])),
 'has_autocorr': np.max(np.abs(autocorr[1:])) > 0.1
 }
 except importError:
 if config['verbose']:
"statsmodels not installed, let's skip autocorporation"

 if config['include_stationarity']:
 try:
 from statsmodels.tsa.stattools import adfuller
 adf_stat, adf_pvalue, adf_critical, adf_Usedlag = adfuller(returns_clean)
 results['stationarity'] = {
 'adf_statistic': adf_stat,
 'adf_pvalue': adf_pvalue,
 'adf_critical': adf_critical,
 'is_stationary': adf_pvalue < 0.05
 }
 except importError:
 if config['verbose']:
"statsmodels not installed, missing the stationary test"

 if config['verbose']:
(f) The calculation is complete. Sharpe: {sharpe:.4f}, Max DD: {max_drawdown:.4f})

 return results

# Example of use
metrics = calculate_basic_metrics(strategy_returns)
```

** Calculation of maximum draught:**

```python
def calculate_max_drawdown(returns, config=None, validation=True):
 """
Calculation of maximum draught with detailed parameters

 Parameters:
 -----------
 returns : pd.Series or np.array
temporary number of strategy returns
- Shall contain numerical values
- A minimum of 100 observations for reliability are recommended
- May contain NaN, which will be ignored

 config : dict, optional
Additional configuration for sediment calculation
- 'method': str, default='cumulative' is the calculation method ('cumulative', 'rolling', 'peak')
- 'Window': in, default= None - window for rolling method (if None, all period used)
- 'min_periods':int, default=30 = minimum number periods for calculation
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'Include_drawdown_series': bool, default=False - include a series of prostheses
- 'Include_drawdown_dates': bell, default=False - include the date of the pronoun
- 'include_recovery_time': bool, default=False - include recovery time
- 'include_underwater_periods': bool, default=False - include periods underwater

 validation : bool, default=True
Whether to validate input data
- Checks the data availability.
- Checks data adequacy
- Checks the correct parameters.

 Returns:
 --------
 float or dict
Maximum length or dictionary with detailed results:
- 'max_drawdown': float = maximum draught
- 'drawdown_series': pd.Serys is a series of prostheses (if include_drawdown_series=True)
- 'drawdown_dates': dict - date of prolitude (if include_drawdown_dates=True)
- 'recovery_time':int is the time of recovery in days (if include_recovery_time=True)
- 'underwater_periods':List - Underwater periods (if include_underwater_periods=True)

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If data not are numerical

 Examples:
 ---------
>># Basic use
 >>> max_dd = calculate_max_drawdown(strategy_returns)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'method': 'rolling',
 ... 'window': 252,
 ... 'include_drawdown_series': True,
 ... 'include_drawdown_dates': True,
 ... 'verbose': True
 ... }
 >>> results = calculate_max_drawdown(strategy_returns, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> max_dd = calculate_max_drawdown(strategy_returns, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'method': 'cumulative',
 'window': None,
 'min_periods': 30,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'include_drawdown_series': False,
 'include_drawdown_dates': False,
 'include_recovery_time': False,
 'include_underwater_periods': False
 }

# Validation of input data
 if validation:
 if len(returns) < config['min_periods']:
raise ValueError(f"Insufficient data. Minimum: {config['min_periods']})

 if not np.isfinite(returns).any():
Raise ValueError("data nt contains final values")

 if config['method'] not in ['cumulative', 'rolling', 'peak']:
Raise ValueError ("method should be 'cumulative', 'rolling' or 'peak'")

 if config['window'] is not None and config['window'] < 2:
Raise ValueError("window must be more than 1")

# Clear data
 returns_clean = returns.dropna() if hasattr(returns, 'dropna') else returns[~np.isnan(returns)]

 if len(returns_clean) < config['min_periods']:
raise ValueError(f"After cleaning insufficient data.

 if config['verbose']:
pprint(f) "Calculation of maximum tare for {len(returns_clean)} observation")
(pint(f" Method: {config['method']}})
 if config['window']:
(pint(f" Window: {config['window']}})

# Calculation of the margin in dependencies from the method
 if config['method'] == 'cumulative':
# Cumulative method
 cumulative = (1 + returns_clean).cumprod()
 running_max = cumulative.expanding().max()
 drawdown = (cumulative - running_max) / running_max

 elif config['method'] == 'rolling':
# Rolling method
 if config['window'] is None:
 config['window'] = len(returns_clean)

 cumulative = (1 + returns_clean).cumprod()
 running_max = cumulative.rolling(window=config['window'], min_periods=1).max()
 drawdown = (cumulative - running_max) / running_max

 elif config['method'] == 'peak':
# Peak method
 cumulative = (1 + returns_clean).cumprod()
 running_max = cumulative.expanding().max()
 drawdown = (cumulative - running_max) / running_max

# Maximum tarmac
 max_drawdown = drawdown.min()

# Results
 results = {
 'max_drawdown': max_drawdown
 }

# Additional results
 if config['include_drawdown_series']:
 results['drawdown_series'] = drawdown

 if config['include_drawdown_dates']:
# Find the maximum planting dates
 max_dd_idx = drawdown.idxmin() if hasattr(drawdown, 'idxmin') else np.argmin(drawdown)
 peak_idx = drawdown[:max_dd_idx].idxmax() if hasattr(drawdown, 'idxmax') else np.argmax(drawdown[:max_dd_idx])

 results['drawdown_dates'] = {
 'max_drawdown_date': max_dd_idx,
 'peak_date': peak_idx,
 'trough_date': max_dd_idx
 }

 if config['include_recovery_time']:
# Time of recovery
 max_dd_idx = drawdown.idxmin() if hasattr(drawdown, 'idxmin') else np.argmin(drawdown)
 peak_idx = drawdown[:max_dd_idx].idxmax() if hasattr(drawdown, 'idxmax') else np.argmax(drawdown[:max_dd_idx])

# Find out when the tarmac went back to zero
 recovery_idx = None
 for i in range(max_dd_idx, len(drawdown)):
 if drawdown.iloc[i] >= 0 if hasattr(drawdown, 'iloc') else drawdown[i] >= 0:
 recovery_idx = i
 break

 recovery_time = recovery_idx - max_dd_idx if recovery_idx is not None else None
 results['recovery_time'] = recovery_time

 if config['include_underwater_periods']:
# Underwater periods (sprout > 0)
 underwater = drawdown > 0
 underwater_periods = []

 in_underwater = False
 start_idx = None

 for i, is_underwater in enumerate(underwater):
 if is_underwater and not in_underwater:
# The beginning of the underwater period
 in_underwater = True
 start_idx = i
 elif not is_underwater and in_underwater:
# End of period underwater
 in_underwater = False
 underwater_periods.append({
 'start': start_idx,
 'end': i - 1,
 'duration': i - start_idx,
 'max_drawdown': drawdown.iloc[start_idx:i].min() if hasattr(drawdown, 'iloc') else drawdown[start_idx:i].min()
 })

# If the period under water is over #
 if in_underwater:
 underwater_periods.append({
 'start': start_idx,
 'end': len(drawdown) - 1,
 'duration': len(drawdown) - start_idx,
 'max_drawdown': drawdown.iloc[start_idx:].min() if hasattr(drawdown, 'iloc') else drawdown[start_idx:].min()
 })

 results['underwater_periods'] = underwater_periods

 if config['verbose']:
print(f "Maximal prosperity: {max_drawdown:.4f}")
 if config['include_recovery_time'] and 'recovery_time' in results:
Print(f"Recovery time: {`recovery_time'} days")
 if config['include_underwater_periods'] and 'underwater_periods' in results:
prent(f"periods underwater: {len(s['underwater_periods']}})

# We only return the maximum delay if not requested additional results
 if not any([config['include_drawdown_series'], config['include_drawdown_dates'],
 config['include_recovery_time'], config['include_underwater_periods']]):
 return max_drawdown

 return results

# Example of use
max_dd = calculate_max_drawdown(strategy_returns)
```

♪##2 ♪ Advanced metrics

**Metrics stability:**

```python
def calculate_stability_metrics(returns, window=252, config=None, validation=True):
 """
Calculation of stability metric with detailed parameters

 Parameters:
 -----------
 returns : pd.Series or np.array
temporary number of strategy returns
- Shall contain numerical values
- A minimum of 100 observations for reliability are recommended
- May contain NaN, which will be ignored

 window : int, default=252
Window for calculation of sliding metrics
- 252 means window in 252 days (year)
- Recommended 50-500 for most cases
- Less than 50 can give inaccurate results.
- More than 500 can be too slow.

 config : dict, optional
Additional conference for the calculation of the stability metric
- 'trade_days':int, default=252 - number of trade days in year
- 'risk_free_rate': flat, default=0.0 - risk-free rate (0.0-0.1)
- 'min_periods':int, default=30 = minimum number periods for calculation
- 'return_predations': bool, default=False - return predictions
- 'return_metrics': bool, default=True - return metrics
- 'verbose': bool, default=False - output details
- 'Include_rolling_metrics': bool, default=True - include sliding metrics
- 'Include_volatility_metrics': bool, default=True - include metrics volatility
- 'include_control_metrics': bool, default=True - include metrics correlations
- 'include_regime_metrics': bool, default=True - include metrics modes
- 'Include_trend_metrics': bool, default=True - include metrics trend
- 'Include_cyclic_metrics': bool, default=True - include cycles

 validation : bool, default=True
Whether to validate input data
- Checks the data availability.
- Checks data adequacy
- Checks the correct parameters.

 Returns:
 --------
 dict
Vocabulary with meters of stability:
- 'sharpe_state': float - Sharpe coefficient stability
- 'co-officent_of_variation': float = coefficient of variation
- 'Stability': float - total stability coefficient
- 'rolling_sharpe': pd.Serys is the sliding coefficient of Sharpe (if include_rolling_metrics=True)
- 'volatility_metrics': dict - metrics volatility (if include_volatility_metrics=True)
- 'correllation_metrics': dict - metrics correlations (if include_control_metrics=True)
- 'regime_metrics':dict - metrics modes (if include_regime_metrics=True)
- 'trend_metrics': dict - metrics trend (if include_trind_metrics=True)
- 'cyclic_metrics': dict - metrics cycles (if include_cyclic_metrics=True)

 Raises:
 -------
 ValueError
If data are insufficient or parameters incorrect
 TypeError
If data not are numerical

 Examples:
 ---------
>># Basic use
 >>> metrics = calculate_stability_metrics(strategy_returns)
 >>>
>> # with caste configuration
 >>> config = {
 ... 'trading_days': 365,
 ... 'risk_free_rate': 0.02,
 ... 'window': 500,
 ... 'verbose': True
 ... }
 >>> metrics = calculate_stability_metrics(strategy_returns, window=500, config=config)
 >>>
>> # Without vilification (rapid but less secure)
 >>> metrics = calculate_stability_metrics(strategy_returns, validation=False)
 """
# configuring on default
 if config is None:
 config = {
 'trading_days': 252,
 'risk_free_rate': 0.0,
 'min_periods': 30,
 'return_predictions': False,
 'return_metrics': True,
 'verbose': False,
 'include_rolling_metrics': True,
 'include_volatility_metrics': True,
 'include_correlation_metrics': True,
 'include_regime_metrics': True,
 'include_trend_metrics': True,
 'include_cyclical_metrics': True
 }

# Validation of input data
 if validation:
 if len(returns) < config['min_periods']:
raise ValueError(f"Insufficient data. Minimum: {config['min_periods']})

 if not np.isfinite(returns).any():
Raise ValueError("data nt contains final values")

 if not (2 <= window <= len(returns)):
raise ValueError(f"window should be between 2 and {len(returns)}})

 if not (0 < config['trading_days'] <= 365):
Raise ValueError("trading_days should be between 1 and 365)

 if not (0 <= config['risk_free_rate'] <= 1):
Raise ValueError("risk_free_rate should be between 0 and 1)

# Clear data
 returns_clean = returns.dropna() if hasattr(returns, 'dropna') else returns[~np.isnan(returns)]

 if len(returns_clean) < config['min_periods']:
raise ValueError(f"After cleaning insufficient data.

 if config['verbose']:
prent(f) "Calculating the stability metric for {len(returns_clean}}observations")
print(f) Window: {Window})
(f "Trade days in year: {`trade_days'}")
pprint(f"Risk rate: {config['risk_free_rate']:2%}})

# Basic metrics stability
# Sharpe rolling coefficient
 rolling_mean = returns_clean.rolling(window=window, min_periods=1).mean()
 rolling_std = returns_clean.rolling(window=window, min_periods=1).std()
 rolling_sharpe = (rolling_mean - config['risk_free_rate']) / rolling_std * np.sqrt(config['trading_days'])

# Stable Sharpe coefficient
 sharpe_stability = 1 / rolling_sharpe.std() if rolling_sharpe.std() > 0 else 0

# The coefficient of variation
 cv = returns_clean.std() / abs(returns_clean.mean()) if returns_clean.mean() != 0 else 0

# Stability factor
 stability = 1 / cv if cv > 0 else 0

# Results
 results = {
 'sharpe_stability': sharpe_stability,
 'coefficient_of_variation': cv,
 'stability': stability
 }

# Additional metrics
 if config['include_rolling_metrics']:
 results['rolling_sharpe'] = rolling_sharpe
 results['rolling_mean'] = rolling_mean
 results['rolling_std'] = rolling_std
 results['rolling_volatility'] = rolling_std * np.sqrt(config['trading_days'])

 if config['include_volatility_metrics']:
# metrics volatility
 volatility = returns_clean.std() * np.sqrt(config['trading_days'])
 rolling_volatility = rolling_std * np.sqrt(config['trading_days'])

 results['volatility_metrics'] = {
 'volatility': volatility,
 'volatility_std': rolling_volatility.std(),
 'volatility_stability': 1 / rolling_volatility.std() if rolling_volatility.std() > 0 else 0,
 'volatility_trend': np.polyfit(range(len(rolling_volatility)), rolling_volatility, 1)[0],
 'volatility_regime_changes': (rolling_volatility.diff() > rolling_volatility.std()).sum()
 }

 if config['include_correlation_metrics']:
# metrics correlations
 autocorr = returns_clean.autocorr(lag=1) if hasattr(returns_clean, 'autocorr') else np.corrcoef(returns_clean[:-1], returns_clean[1:])[0, 1]

 results['correlation_metrics'] = {
 'autocorrelation': autocorr,
 'autocorrelation_abs': abs(autocorr),
 'has_autocorrelation': abs(autocorr) > 0.1,
 'correlation_stability': 1 / abs(autocorr) if autocorr != 0 else 0
 }

 if config['include_regime_metrics']:
# metrics modes
 rolling_mean = returns_clean.rolling(window=window, min_periods=1).mean()
 rolling_std = returns_clean.rolling(window=window, min_periods=1).std()

# Definition of regimes (high/low volatility)
 high_vol_threshold = rolling_std.quantile(0.75)
 low_vol_threshold = rolling_std.quantile(0.25)

 high_vol_periods = (rolling_std > high_vol_threshold).sum()
 low_vol_periods = (rolling_std < low_vol_threshold).sum()

 results['regime_metrics'] = {
 'high_volatility_periods': high_vol_periods,
 'low_volatility_periods': low_vol_periods,
 'regime_stability': 1 - (high_vol_periods + low_vol_periods) / len(rolling_std),
 'volatility_regime_changes': (rolling_std.diff() > rolling_std.std()).sum()
 }

 if config['include_trend_metrics']:
# metrics trend
 trend_slope = np.polyfit(range(len(returns_clean)), returns_clean, 1)[0]
 trend_r2 = np.corrcoef(range(len(returns_clean)), returns_clean)[0, 1] ** 2

 results['trend_metrics'] = {
 'trend_slope': trend_slope,
 'trend_r2': trend_r2,
 'trend_strength': abs(trend_r2),
 'trend_direction': 'up' if trend_slope > 0 else 'down' if trend_slope < 0 else 'flat'
 }

 if config['include_cyclical_metrics']:
# metrics cycles
 try:
 from scipy import signal
# Searching for in-data cycles
 freqs, psd = signal.periodogram(returns_clean, fs=1.0)
 dominant_freq = freqs[np.argmax(psd)]
 cycle_length = 1 / dominant_freq if dominant_freq > 0 else 0

 results['cyclical_metrics'] = {
 'dominant_frequency': dominant_freq,
 'cycle_length': cycle_length,
 'spectral_density': psd.max(),
 'has_cyclical_pattern': cycle_length > 0 and cycle_length < len(returns_clean) / 2
 }
 except importError:
 if config['verbose']:
"spipy not installed, skip cycles")

 if config['verbose']:
prent(f) "The calculation is complete. Sharp stability: {sharpe_state:.4f}")
(f "Variation factor: {cv:.4f}")
(f "General stability: {stable: 4f}")

 return results

# Example of use
stability_metrics = calculate_stability_metrics(strategy_returns, window=252)
```

**Metrics risk:**

```python
def calculate_risk_metrics(returns, confidence_level=0.95):
""""""" "The calculation of the risk metric."
 # Value at Risk (VaR)
 var = np.percentile(returns, 100 * (1 - confidence_level))

 # Conditional Value at Risk (CVaR)
 cvar = returns[returns <= var].mean()

 # Expected Shortfall
 es = returns[returns <= var].mean()

# Calmar coefficient
 calmar = returns.mean() * 252 / abs(calculate_max_drawdown(returns))

# Sterling coefficient
 sterling = returns.mean() * 252 / abs(returns.min())

 return {
 'var': var,
 'cvar': cvar,
 'expected_shortfall': es,
 'calmar': calmar,
 'sterling': sterling
 }

# Example of use
risk_metrics = calculate_risk_metrics(strategy_returns, confidence_level=0.95)
```

### 3. Metrics performance

**Metrics efficiency:**

```python
def calculate_efficiency_metrics(returns, benchmark_returns):
"The calculation of the performance metric."
# Beta coefficient
 beta = np.cov(returns, benchmark_returns)[0, 1] / np.var(benchmark_returns)

# Alpha coefficient
 alpha = returns.mean() - beta * benchmark_returns.mean()

# Information ratio
 excess_returns = returns - benchmark_returns
 information_ratio = excess_returns.mean() / excess_returns.std()

# Trainor coefficient
 treynor = returns.mean() / beta if beta != 0 else 0

# The Jensen coefficient
 jensen = alpha

 return {
 'beta': beta,
 'alpha': alpha,
 'information_ratio': information_ratio,
 'treynor': treynor,
 'jensen': jensen
 }

# Example of use
efficiency_metrics = calculate_efficiency_metrics(strategy_returns, benchmark_returns)
```

## Validation of thebacking results

### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\t\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\############## \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#################################################### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

```mermaid
graph TD
A [Becketting results] -> B [Statistical appreciation]
A-> C [Economic recovery]

B --> B1 [Text on stability]
B1 --> B11 [Text Dickie-Fuller<br/>p-value < 0.05]
B1 --> B12 [Test KPC<br/>p-value > 0.05]

B --> B2 [Text on autocorration]
B2 --> B21 [Text Leunga-Box<br/>p-value > 0.05]
B2 --> B22 [Test of Darbin-Watson<br/>1.5 < DW < 2.5]

C --> C1 [Text on economic significance]
C1 -> C11 [To account for transaction costs<br/>0.1 per cent per transaction]
C1-> C12 [Minimum Sharp coefficient<br/>≥ 1.0]
C1 -> C13 [Maximum draught <br/> < 20 per cent]

C --> C2 [Text on retraining]
C2 --> C21[comparison train/test performance]
C2 --> C22 [Statistical test<br/>t-test]
C2 --> C23[check degradation<br/>training_sharpe > test_sharpe * 1.5]

B11 -> D [Valitability assessment]
 B12 --> D
 B21 --> D
 B22 --> D
 C11 --> D
 C12 --> D
 C13 --> D
 C21 --> D
 C22 --> D
 C23 --> D

D --> E {Results of valid?}
E --\\\\\\\F[\\The Strategy is ready for action]
E --\\\\\\G[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/E/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\E\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/ } } } } } } } } } } } } }     } } }   }        }  }        } } }

F --> H [Business in sales]
G -> I [Optimization of parameters]
I -> J [Return testing]
 J --> A

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style F fill:#4caf50
 style G fill:#ff9800
```

###1. Statistical validation

**Stability test:**

```python
def test_stationarity(returns, significance_level=0.05):
"Text on fixed time-series"
 from statsmodels.tsa.stattools import adfuller

# Dickie Fuller test
 adf_result = adfuller(returns)

# KPSS test
 from statsmodels.tsa.stattools import kpss
 kpss_result = kpss(returns)

 return {
 'adf_statistic': adf_result[0],
 'adf_pvalue': adf_result[1],
 'adf_stationary': adf_result[1] < significance_level,
 'kpss_statistic': kpss_result[0],
 'kpss_pvalue': kpss_result[1],
 'kpss_stationary': kpss_result[1] > significance_level
 }

# Example of use
stationarity_test = test_stationarity(strategy_returns, significance_level=0.05)
```

**Authorization test:**

```python
def test_autocorrelation(returns, lags=20, significance_level=0.05):
"The Test on AutoCorroration."
 from statsmodels.stats.diagnostic import acorr_ljungbox

# Leunga-Box test
 ljung_box = acorr_ljungbox(returns, lags=lags, return_df=True)

# Darbin-Watson test
 from statsmodels.stats.diagnostic import durbin_watson
 dw_statistic = durbin_watson(returns)

 return {
 'ljung_box': ljung_box,
 'ljung_box_significant': ljung_box['lb_pvalue'].min() < significance_level,
 'durbin_watson': dw_statistic,
 'durbin_watson_autocorr': dw_statistic < 1.5 or dw_statistic > 2.5
 }

# Example of use
autocorr_test = test_autocorrelation(strategy_returns, lags=20)
```

♪##2 ♪ Economic appreciation

** Issue on economic significance:**

```python
def test_economic_significance(returns, transaction_costs=0.001,
 min_sharpe=1.0, max_drawdown=0.2):
"The Issue on Economic Importance"
# Accounting for transaction costs
 net_returns = returns - transaction_costs

# The calculation of the metric
 sharpe = net_returns.mean() / net_returns.std() * np.sqrt(252)
 max_dd = calculate_max_drawdown(net_returns)

# check criteria
 sharpe_significant = sharpe >= min_sharpe
 drawdown_acceptable = abs(max_dd) <= max_drawdown

 return {
 'sharpe': sharpe,
 'max_drawdown': max_dd,
 'sharpe_significant': sharpe_significant,
 'drawdown_acceptable': drawdown_acceptable,
 'economically_significant': sharpe_significant and drawdown_acceptable
 }

# Example of use
economic_test = test_economic_significance(strategy_returns, transaction_costs=0.001)
```

**Text on retraining:**

```python
def test_overfitting(train_returns, test_returns, significance_level=0.05):
"The Test on Retraining"
 from scipy import stats

# Comparison performance
 train_sharpe = train_returns.mean() / train_returns.std() * np.sqrt(252)
 test_sharpe = test_returns.mean() / test_returns.std() * np.sqrt(252)

# Statistical test
 t_stat, p_value = stats.ttest_ind(train_returns, test_returns)

# check on retraining
 overfitting = train_sharpe > test_sharpe * 1.5 and p_value < significance_level

 return {
 'train_sharpe': train_sharpe,
 'test_sharpe': test_sharpe,
 'performance_degradation': train_sharpe - test_sharpe,
 't_statistic': t_stat,
 'p_value': p_value,
 'overfitting': overfitting
 }

# Example of use
overfitting_test = test_overfitting(train_returns, test_returns)
```

## Becketting automation

### ♪ Pypline automating the backtting

```mermaid
graph TD
A [Reference data] --> B [BacktestingPipeline]
B -> C [configration of parameters]

C --> D [Simple buffering<br/>training_size: 70%<br/>test_size: 30%]
C --> E[Walk-forward buffering<br/>training_window: 252<br/>test_window: 30]
C --> F[Monte-Carlo batting<br/>n_simulations: 1000<br/>confidence: 95%]

D -> G [model training]
 E --> G
 F --> G

G -> H [Treaties]
H -> I [Metrics calculation]

I-> J [Sharp coefficient]
I -> K [Maximum draught]
I-> L [Total return]

J-> M[Collection of results]
 K --> M
 L --> M

M --> N[Generation Reporta]
N -> O[Report on methods]
N -> P [Detail results]

O -> Q [Medical Sharpe coefficient]
O -> R [standard deviation]
O-> S[All successful strategies]

P -> T [Visualization of results]
T --> U [cumulative return]
T -> V [Metric distribution]
T --> W[comparison of methods]

Q -> X [Final evaluation]
 R --> X
 S --> X
 U --> X
 V --> X
 W --> X

X --> Y {The Strategy is ready?}
Y-~ ♪ Yeah ♪ Z[~ Deploy in sales]
Y --\\\\\\\A[\\\\imtimation of parameters]

AA --> BB [configration model]
BB --> CC[Return testing]
 CC --> B

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style N fill:#fff3e0
 style Z fill:#4caf50
 style AA fill:#ff9800
```

♪##1 ♪ Pipline backtting ♪

```python
class BacktestingPipeline:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""Pipline""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, data, model, metrics_calculator):
 self.data = data
 self.model = model
 self.metrics_calculator = metrics_calculator
 self.results = {}

 def run_simple_backtest(self, train_size=0.7, test_size=0.3):
"Simple Baactering."
# Data sharing
 split_point = int(len(self.data) * train_size)
 train_data = self.data[:split_point]
 test_data = self.data[split_point:]

# Model learning
 self.model.fit(train_data)

# Premonition
 predictions = self.model.predict(test_data)

# The calculation of the metric
 returns = test_data['returns']
 strategy_returns = predictions * returns

 self.results['simple'] = self.metrics_calculator.calculate(strategy_returns)
 return self.results['simple']

 def run_walk_forward_backtest(self, train_window=252, test_window=30, step=30):
"Walk-forward buffering."
 results = []

 for i in range(train_window, len(self.data) - test_window, step):
# Training data
 train_data = self.data[i-train_window:i]

# Testsy data
 test_data = self.data[i:i+test_window]

# Model learning
 self.model.fit(train_data)

# Premonition
 predictions = self.model.predict(test_data)

# The calculation of the metric
 returns = test_data['returns']
 strategy_returns = predictions * returns

 metrics = self.metrics_calculator.calculate(strategy_returns)
 metrics['date'] = test_data.index[0]
 results.append(metrics)

 self.results['walk_forward'] = pd.dataFrame(results)
 return self.results['walk_forward']

 def run_monte_carlo_backtest(self, n_simulations=1000, confidence_level=0.95):
"Monte-Carlo Becketting."
 results = []

 for i in range(n_simulations):
# Random data sample
 sample_data = self.data.sample(frac=0.8, replace=True)

# Separation on train/test
 split_point = int(len(sample_data) * 0.7)
 train_data = sample_data[:split_point]
 test_data = sample_data[split_point:]

# Model learning
 self.model.fit(train_data)

# Premonition
 predictions = self.model.predict(test_data)

# The calculation of the metric
 returns = test_data['returns']
 strategy_returns = predictions * returns

 metrics = self.metrics_calculator.calculate(strategy_returns)
 results.append(metrics)

 self.results['monte_carlo'] = pd.dataFrame(results)
 return self.results['monte_carlo']

 def generate_Report(self):
""""""" "Generation Report"""
 Report = {
 'summary': {},
 'Detailed_results': self.results
 }

# A summary on all methods
 for method, results in self.results.items():
 if isinstance(results, pd.dataFrame):
 Report['summary'][method] = {
 'mean_sharpe': results['sharpe'].mean(),
 'std_sharpe': results['sharpe'].std(),
 'mean_max_drawdown': results['max_drawdown'].mean(),
 'success_rate': (results['sharpe'] > 1.0).mean()
 }
 else:
 Report['summary'][method] = results

 return Report

# Example of use
pipeline = BacktestingPipeline(data, model, metrics_calculator)
pipeline.run_simple_backtest()
pipeline.run_walk_forward_backtest()
pipeline.run_monte_carlo_backtest()
Report = pipeline.generate_Report()
```

###2: Visualization of results

```python
def visualize_backtest_results(results, save_path=None):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 import matplotlib.pyplot as plt
 import seaborn as sns

# configuring style
 plt.style.Use('seaborn-v0_8')
 sns.set_palette("husl")

# Create figures
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Cumulative returns
 if 'walk_forward' in results:
 cumulative_returns = (1 + results['walk_forward']['return']).cumprod()
 axes[0, 0].plot(cumulative_returns.index, cumulative_returns.values)
axes[0,0].set_tile('cumulative return')
axes[0,0].set_xlabel('Data')
axes[0,0].set_ylabel('cumulative return')

♪ 2. Sharpe coefficient distribution
 if 'monte_carlo' in results:
 axes[0, 1].hist(results['monte_carlo']['sharpe'], bins=50, alpha=0.7)
 axes[0, 1].axvline(results['monte_carlo']['sharpe'].mean(),
color='red', lineyle='--', label='average')
axes[0,1].set_title('Sharp coefficient distribution')
axes[0,1].set_xlabel('Sharp's coefficient')
axes[0,1].set_ylabel('Part')
 axes[0, 1].legend()

# 3. Maximum tarmac
 if 'walk_forward' in results:
 axes[1, 0].plot(results['walk_forward']['date'],
 results['walk_forward']['max_drawdown'])
axes[1, 0].set_title('Maximal prosperity')
axes[1, 0].set_xlabel('Data')
axes[1, 0].set_ylabel('Maximal prosin')

# 4. Comparson of methods
 if 'simple' in results and 'walk_forward' in results:
 methods = ['Simple', 'Walk Forward']
 sharpe_values = [
 results['simple']['sharpe'],
 results['walk_forward']['sharpe'].mean()
 ]
 axes[1, 1].bar(methods, sharpe_values)
axes[1, 1].set_title('comparison methods')
axes[1, 1].set_ylabel('Sharpa's co-factor')

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
visualize_backtest_results(results, save_path='backtest_results.png')
```

## Summary table of betting parameters

### ♪ Basic {meters of the backting function

♪ function ♪ Basic factor ♪ describe ♪ The range of values ♪ Recommendations ♪
|---------|-------------------|----------|-------------------|--------------|
♪ Time_series_backtest** ♪ tran_size', `test_size', `config', `vacation' ♪ simple time-series buffering ♪ tran_sise: 0.6-0.8, test_sise: 0.2-0.4 ♪ 70/30 for most cases ♪
== sync, corrected by elderman == @elder_man
*monte_carlo_backtest** ♪ n_simulations, `confidence_level', `config' ♪ Monte-Carlo batting ♪ n_simulations: 500-2000, conference: 0.90-0.99 ~ 1,000 simulations, 95% trust ♪
== sync, corrected by elderman == @elder_man
*Structure_test_backtest**** [Structure_scenarios', `config', `validation'] [Scenarios strategy: 3-10, volatility_multiplier: 0.5-3.0] scenarios, including extreme scenarios
== sync, corrected by elderman == @elder_man
*Porthfolio_backtest** \\`Strategies', `whites', `rebalance_freq', `config' \\ \ \ \ \ \ \ portfolio buffering \ strategies: 2-10, reballance_freq: 'M' \5 strategies, monthly rebalancing \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\, `/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\, `///////////////////////////////////////// \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/////////////// \/ \/ \/////////////////////// \/ \/ \/ \/ \/ \/ \/ \/ \////////////// \/// \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \/ \////// \////
♪ dynamic_rebalance_backtest** ♪ "rebalance_freq", `lookback_window', `config' ♪ Dynamic rebalancing ♪ lowback_window: 100-500, test_widow: 30-60 ♪ 252 days of learning, 30 days of testing ♪

### ♪ The configuration parameters

================================================================================================================= )====== )===== ) )=========== )======== ) )============================)============================================================ ========================================================================================================================================================================================================================================================================
|----------|----------|----------------------|----------|-------------------------------|
♪ ♪ ♪ Train_frac** ♪ the share of data for learning ♪ 0.7 ♪ 0.6-0.8 ♪ More = better learning, less testing ♪
♪ ♪ test_frac** ♪ data share for testing ♪ 0.3 ♪ 0.2-0.4 ♪ More = reliable testing ♪
*min_samples** * Minimum number of samples * 100 * 50-200 * More = reliable results *
*Validation** \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ ♪ ♪ ♪ n_jobs** ♪ Number of processes ♪ 1 ♪ 1 ♪ 8 ♪ More ♪ ♪ Faster, more CPU ♪
== sync, corrected by elderman == @elder_man

### ♪ quality metrics

♪ Meter ♪ descube ♪ Good values ♪ Bad values ♪ How to improve ♪
|---------|----------|------------------|-----------------|---------------|
*Sharpe Radio** * The ratio of return to risk * 1.0 * 0.5 * to improve the model, reduce volatility *
*Max Drawdown** * Maximum draught * 20 per cent * 50 per cent * Improve risk management *
*Sortino Ratio** * Relationship to duenside risk *
*Calmar Ratio** * The ratio of income to rainfall ~ 0.5 ~ 0.2 ~ Improve the model, reduce the prostheses
*Stability** * Stability of results * 0.8 * 0.5 * Improve model, stabilize parameters *
*Success Rate** * Percentage of successful simulations * 60% * 40% * Improve model, optimize parameters *

### ♪ Recommendations on setting up

##### For starters

- Use `time_series_backtest` with `train_size=0.7`, `test_size=0.3`
- install `validation=True', `verbose'=True' for understanding the process
- Start with `min_samples=100', `n_simulations=500'
- Use basic metrics: Sharpe, Max Drawdown, Total Return

##### for experienced users

- Use `monte_carlo_backtest` with `n_simulations=1000`
- Add 'stress_test_backtest' with 5-7 scripts
- Use `Porthfolio_backtest' with 3-5 strategies
- Turn on advanced metrics: Sortino, Kalmar, Stability

#### # For sale

- Use `dynamic_rebalance_backtest` with `rebalance_freq='M'`
- install `parallel=True`, `n_jobs=4-8`
- Add `transaction_costs=0.001', `slippage=0.005'
- Use all quality and validation

♪ ♪ Frequent mistakes and decisions

♪ The reason ♪ ♪ The solution ♪
|--------|---------|---------|
There are too few samples of "min_samples" or collect more data.
* "retraining" * tran_sharpe >> test_sharpe * reduce `train_size', add regularization
♪ Unstable results ♪ ♪ the relative volatility of the metric ♪ ♪ put 'n_simulations' in place, improve the model ♪
♪ Slow Working too many simulations ♪ Reduce 'n_simulations', use 'parallel'=True' ♪
♪ "Faulty results" ♪ Wrong parameters ♪ Check 'validation=True', set 'config' ♪

## Conclusion

The right backup is the basis of a successful ML strategy.

1. ** Checking whether the strategy is realistic**
2. ** Assess risks** and potential losses
3. **Optify parameters** for maximum efficiency
**To assess stability** on different market conditions

### Key principles

1. ** Reality** - Use realistic data and conditions
2. ** Statistical significance** - check the relevance of the results
3. ** Economic significance** - account for transaction costs
4. **Plativity** - Test on different market conditions
5. **validation** - check the results on outof-sample data

### Next steps

Once you have mastered the bactering, go to:

- [Walk-forward analysis](./28_walk_forward_Anallysis.md)
- [Monte Carlo simulation](./29_monte_carlo_simulations.md)
- [Porthfolio Administration](./30_Porthfolio_Management.md)
