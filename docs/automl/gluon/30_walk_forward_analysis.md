# In-depth describe of Walk-Forward Analysis

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who Walk-Forward Analysis - Gold Standard of Validation

### ♪ Walk-Forward analysis as a gold standard of validation

```mermaid
graph TD
A[ML-Strategy] -> B {Method of validation}

B--~ ~ Simple back-up ~ C[~ re-training on historical data]
B -->Out-of-sample
B--~♪ Cross-validation♪ E[~ queu tremporial structure]
B--~♪ Walk-Forward analysis ~ F[~ Gold Standard Validation]

C --> G [Instable performance]
C --> H [Position confidence]
C -> I [Real losses in trade]

D --> J [Restricted appreciation]
E --> K [The future data leak]

F --> L [Real trade simulation]
F --> M [Continuing retraining]
F --> N [Treaties on the future]
F --> O [Prevention of data leakage]

L -> P [Realistic evaluation]
 M --> P
 N --> P
 O --> P

P --> Q [Aptitude to change]
P --> R [Stability over time]
P -> S [Pativity of strategy]

Q -> T[~ good trade]
 R --> T
 S --> T

 style A fill:#e3f2fd
 style F fill:#4caf50
 style C fill:#ffcdd2
 style D fill:#fff3e0
 style E fill:#fff3e0
 style T fill:#2e7d32
```

**Why is Walk-Forward analysis considered to be the most realistic method of validation?** Because it mimics real trade - the model is constantly re-learning on new data and making predictions on the future.

### What gives Walk-Forward analysis?

- ** Reality**: Simulates real trade
- ** Adaptation**: Model adapts to changing conditions
- **Stability**: Checks strategy stability over time
- **Platitude**: Identifys the weaknesses of strategy

### What's going on without Walk-Forward Anallysis?

- **retraining**: The model memorizes historical data
- ** Instability**: The Workinget Strategy is unstable over time
- ** false confidence**: Excess expectations from strategy
- ** Real losses**: Strategy not Workinget in Real Trade

## Theoretical foundations of Walk-Forward Analysis

### Mathematical principles

**Walk-Forward as a sliding window:**

```python
For t = train_window to T - test_window:
 train_data = data[t-train_window:t]
 test_data = data[t:t+test_window]

 model.fit(train_data)
 predictions = model.predict(test_data)

 performance[t] = evaluate(predictions, test_data)
```

Where:

`training_window' is the size of the learning window
`test_window' is the size of the test window
`T' is the total data length
- `performance[t] ` - performance on period t

**Walk-Forward quality criteria:**

1. **Stability**: Var(performance) < threshold
2. **Trend**: performance no deteriorates over time
** Adaptation**: The model adapts to the new environment
4. **Purity**: results stable on different periods

### Types of Walk-Forward Analysis

### ♪ a partnership of the Walk-Forward Anallysis

```mermaid
graph TB
A[Walk-Forward Analysis] --> B [Fixed Window]
A -> C [Expansing window]
A --> D [Slipping Window]
A --> E [Adaptive window]

B --> B1 [Continuing window size]
B -> B2 [Simple in implementation]
B -> B3[ may become obsolete]
B -> B4[~ Rapid implementation]
B --> B5[~ Fixed parameters]

C --> C1 [The window is constantly growing]
C --> C2 [Uses the whole story]
C --> C3[ may be slow]
C --> C4[~ More data over time]
C -> C5[~ Knowledge-building]

D -> D1 [The window is shifting]
D -> D2 [Balance of history and relevance]
D --> D3[~ Most popular]
D -> D4[~ Optimal balance]
D --> D5[ ♪ Stable performance]

E -> E1 [The measurement adapts to the conditions]
E --> E2 [Complicated in implementation]
E --> E3[: Most flexible]
E -> E4[~ Intellectual adaptation]
E --> E5[~ Dynamic parameters]

 style A fill:#e3f2fd
 style B fill:#ffcdd2
 style C fill:#fff3e0
 style D fill:#c8e6c9
 style E fill:#4caf50
```

####1. Fixed Windows

- Permanent size of the training window
- Simple in implementation
- It might get old.

####2. Expanding Windows

- The learning window is constantly growing.
- Uses all available history.
- Could be slow.

#### 3. Rolling Windows window

- The learning window is shifting.
- Balance between history and relevance
- Most popular.

####4. Adaptation Windows

- Window size adapts to conditions
- Complex in implementation
- Most flexible

## Advanced Walk-Forward Analysis

###1. Basic Walk-Forward analysis

### 🔄 process Walk-Forward Analysis

```mermaid
graph TD
A [Reference time data] -> B [configration of parameters]
 B --> C[train_window = 252<br/>test_window = 30<br/>step = 30]

C -> D [Initiation of the cycle]
 D --> E[i = train_window]

E --> F [Learning data<br/>data[i-training_window:i]]]
E --> G[tests data<br/>data[i:i+test_window]]

F --> H [Learning the model<br/>model.fit(training_data)]
G --> I [Tracks<br/>model.predict(test_data)]

 H --> I
I -> J [Staff return calculation<br/>predations * returns]

J --> K[quality metrics]
K-> L [Sharp coefficient]
K-> M[maximum draught]
K-> N [Total return]

L -> O [Conservation of results]
 M --> O
 N --> O

O --> P[update index<br/>i += step]
 P --> Q{i < len(data) - test_window?}

Q --\\\\\\\\\F
Q --\\\\\\R[Analysis of results]

R --> S [Stability over time]
R --> T[Aptitude of the model]
R --> U [Purity of strategy]

S -> V [Strategy quality assessment]
 T --> V
 U --> V

V --> W {The Strategy is successful?}
W--~♪ Yeah ♪ X[~ Deploy in sales]
W--~ ~ No\\Y[~ Optimization of parameters]

Y -> Z [configuring learning window]
Z -> AA [Re-testing]
 AA --> B

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style G fill:#fff3e0
 style X fill:#4caf50
 style Y fill:#ff9800
```

** Simple implementation:**

```python
def walk_forward_Analysis(data, model, train_window=252, test_window=30, step=30):
 """
Basic Walk-Forward Analysis for validation ML strategies

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns:
- 'returns': asset return (float)
- 'features': signs for the model (array-lake)
- Index: Time tags (datetime)

 model : sklearn-compatible model
The object of the model machine lightning with methods is:
- Fit(X, y): Model training
- predict(X): predictions
Should be compatible with sclearn API

 train_window : int, default=252
Size of learning window in days:
- 252: one trade year (recommended)
126: Six months (for rapid testing)
- 504: two years (for long-term strategies)
- Minimum: 50 days for stability
- Maximum: 1,000 days for avoidance of retraining

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'start_date': Start of the learning period (datetime)
- 'end_date': end of study period (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)
- 'predications': model predictions (array)

 Raises:
 -------
 ValueError
If train_window < 50 or test_widow < 5
If step > test_wind
If Len(data) < train_widow + test_window

 Examples:
 ---------
 >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
 >>> model = RandomForestRegressor(n_estimators=100)
 >>> results = walk_forward_Analysis(data, model, train_window=252, test_window=30)
>>print(f) Average Sharp coefficient: {results['sharpe']mean(: 2f}})
 """
 results = []

 for i in range(train_window, len(data) - test_window, step):
# Training data
 train_data = data[i-train_window:i]

# Testsy data
 test_data = data[i:i+test_window]

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

 results.append({
 'start_date': train_data.index[0],
 'end_date': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'predictions': predictions
 })

 return pd.dataFrame(results)

# Example of use
wf_results = walk_forward_Analysis(data, model, train_window=252, test_window=30, step=30)
```

** Extended window:**

```python
def expanding_window_Analysis(data, model, initial_train_window=252, test_window=30, step=30):
 """
Walk-Forward analysis with expanding learning window

In contrast from a fixed window, the expanding window uses all available windows
The history of data for learning, which allows models to accumulate knowledge over time.

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns:
- 'returns': asset return (float)
- 'features': signs for the model (array-lake)
- Index: Time tags (datetime)

 model : sklearn-compatible model
The object of the model machine lightning with methods is:
- Fit(X, y): Model training
- predict(X): predictions
Should be compatible with sclearn API

 initial_train_window : int, default=252
Initial size of the learning window in days:
- 252: one trade year (recommended)
126: Six months (for rapid testing)
- 504: two years (for long-term strategies)
- Minimum: 50 days for stability
After that, the window will expand on step days every iteration.

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
- 'training_size': the size of the learning window (int) - increases over time
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If initial_training_window < 50 or test_window < 5
If step > test_wind
If Len(data) < initial_training_window + test_window

 Notes:
 ------
- The extended window may be slower than the fixed window due to the increase
data for training
- It is appropriate for strategies where historical data remain relevant
- Could lead to re-learning on old data.

 Examples:
 ---------
 >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
 >>> model = RandomForestRegressor(n_estimators=100)
 >>> results = expanding_window_Analysis(data, model, initial_train_window=252)
>>print(f" Final window size: {['train_size'].iloc[-1]})
 """
 results = []

 for i in range(initial_train_window, len(data) - test_window, step):
# Learning data (expanding window)
 train_data = data[:i]

# Testsy data
 test_data = data[i:i+test_window]

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

 results.append({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'train_size': len(train_data),
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return
 })

 return pd.dataFrame(results)

# Example of use
expanding_results = expanding_window_Analysis(data, model, initial_train_window=252, test_window=30)
```

♪##2, adaptive Walk-Forward analysis

### ♪ Adaptation window mechanism

```mermaid
graph TD
A [Reference data] -> B [Initiation of parameters]
 B --> C[min_window = 100<br/>max_window = 500<br/>current_window = min_window]

C --> D [Walk-Forward Cycle]
D --> E [Learning data<br/>data[i-surrent_window:i]]
E -> F [model training]
F --> G [Treaties and metrics]

G --> H [Calculation performance<br/>current_sharpe]
H --> I {Are there any previous results?}

I --\\\\\\J[Conservation of results\br/>surrent_Window remains]
I -->\\\\K[comparison with previous output <br/>recent_sharpe]

K --> L{operation has deteriorated?<br/>current_sharpe < recent_sharpe * 0.9}
L -->\\\\\M[Elevation of window\br/>current_window +=50]
L -->\\\\\\\\\\\\\\\\\\\\\\br/>current_sharpe > recent_sharpe * 1.1}

N -->\\\\\\O[Lower window\br/>current_window = 50]
N-~ ~ No~ P[The window remains unchanged]

M --> Q[check boundaries<br/>current_window = min(current_window, max_window)]
O --> R[check boundaries<br/>current_window = max(current_window, min_window)]
P -> S [Conservation of results]
 Q --> S
 R --> S
 J --> S

S --> T[update index<br/>i += step]
T --> U { Continue the cycle?}
U - ♪ Yes ♪ E
U-~\\\\V[Analysis of adaptiveness]

V -> W [Statistics of window change]
V --> X [Wing window and performance]
V -> Y [Evaluating the effectiveness of adaptation]

W -> Z [Final evaluation of the strategy]
 X --> Z
 Y --> Z

 style A fill:#e3f2fd
 style M fill:#ff9800
 style O fill:#4caf50
 style P fill:#fff3e0
 style Z fill:#2e7d32
```

** Window size adaptation:**

```python
def adaptive_window_Analysis(data, model, min_window=100, max_window=500,
 test_window=30, step=30, stability_threshold=0.1):
 """
Walk-Forward analysis with adaptive learning window

The size of the learning window is automatically adapted on base performance
The window increases when performance deteriorates, and the window decreases when it improves.

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns:
- 'returns': asset return (float)
- 'features': signs for the model (array-lake)
- Index: Time tags (datetime)

 model : sklearn-compatible model
The object of the model machine lightning with methods is:
- Fit(X, y): Model training
- predict(X): predictions
Should be compatible with sclearn API

 min_window : int, default=100
Minimum size of teaching window in days:
100: minimum for stability (recommended)
- 50: for rapid testing
- 200: for conservative strategies
- Minimum: 30 days for statistical significance
- Maximum: 300 days for avoidance of retraining

 max_window : int, default=500
Maximum size of learning window in days:
- 500: two years of trade days (recommended)
- 252: one year (for rapid strategies)
- 1000: four years (for long-term strategies)
- Minimum: min_Window + 100
- Maximum: 2,000 days for avoidance of retraining

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 stability_threshold : float, default=0.1
The threshold for determining a significant change in performance:
0.1: 10% change (recommended)
- 0.05: 5% change (for sensitive strategies)
0.2: 20% change (for stable strategies)
- Minimum: 0.01 (1 per cent change)
- Maximum: 0.5 (50% change)

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
'Window_size': the current size of the learning window (int)
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If min_window < 30 or max_widow < min_widow + 100
If test_window < 5 or step > test_window
If stability_threshold < 0.01 or stability_threshold > 0.5
If Len(data) < min_window + test_window

 Notes:
 ------
- The adaptive window can be unstable in the beginning due to lack of data
- It is recommended to use a minimum of 10 iterations for stabilization
- Suitable for strategies with changing market conditions

 Examples:
 ---------
 >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
 >>> model = RandomForestRegressor(n_estimators=100)
 >>> results = adaptive_window_Analysis(data, model, min_window=100, max_window=500)
>>print(f) Average window size: {results['window_size']mean(:.0f}})
 """
 results = []
 current_window = min_window

 for i in range(min_window, len(data) - test_window, step):
# Training data
 train_data = data[i-current_window:i]

# Testsy data
 test_data = data[i:i+test_window]

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

# Adaptation of the size of the window
 if len(results) > 0:
 recent_sharpe = results[-1]['sharpe']
 current_sharpe = sharpe

# If performance gets worse, expand the window
 if current_sharpe < recent_sharpe * (1 - stability_threshold):
 current_window = min(current_window + 50, max_window)
# If performance improves, let's reduce the window
 elif current_sharpe > recent_sharpe * (1 + stability_threshold):
 current_window = max(current_window - 50, min_window)

 results.append({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'window_size': current_window,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return
 })

 return pd.dataFrame(results)

# Example of use
adaptive_results = adaptive_window_Analysis(data, model, min_window=100, max_window=500)
```

** Adaptation on baseline volatility:**

```python
def volatility_adaptive_Analysis(data, model, base_window=252, test_window=30,
 step=30, volatility_lookback=50):
 """
Walk-Forward analysis with adaptation of window size to market volatility

The size of the training window adapts to the current market volatility:
High volatility: less window (rapid adaptation)
Low volatility: more window (stability)

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns:
- 'returns': asset return (float) - used for the calculation of volatility
- 'features': signs for the model (array-lake)
- Index: Time tags (datetime)

 model : sklearn-compatible model
The object of the model machine lightning with methods is:
- Fit(X, y): Model training
- predict(X): predictions
Should be compatible with sclearn API

 base_window : int, default=252
Basic size of the learning window in days:
- 252: one trade year (recommended)
126: Six months (for rapid testing)
- 504: two years (for long-term strategies)
- Minimum: 50 days for stability
- Maximum: 1,000 days for avoidance of retraining

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 volatility_lookback : int, default=50
Period for calculation of current volatility in days:
- 50: two months (recommended)
- 30: one month (for rapid adaptation)
- 100: four months (for stable estimates)
- Minimum: 10 days for statistical significance
- Maximum 200 days for avoidance of obsolescence

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
- 'Window_size': adapted learning window size (int)
- 'volatility_ratio': the ratio of current to long-term volatility (float)
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If base_widow < 50 or test_widow < 5
If step > test_window or volatility_lookback < 10
If Len(data) < base_widow + test_widow + volatility_lookback

 Notes:
 ------
Adaptation is based on the comparison of current and long-term volatility
- With volatility_ratio > 1.5: window reduced to 70% from base
- When volatility_ratio < 0.7: window increases to 130% from base
- Suitable for strategies sensitive to market volatility

 Examples:
 ---------
 >>> data = pd.read_csv('financial_data.csv', index_col=0, parse_dates=True)
 >>> model = RandomForestRegressor(n_estimators=100)
 >>> results = volatility_adaptive_Analysis(data, model, base_window=252)
>>print(f) Average coefficient of volatility: {results['volatility_ratio']mean(: 2f}})
 """
 results = []

 for i in range(base_window, len(data) - test_window, step):
# Calculation of volatility
 recent_volatility = data['returns'].iloc[i-volatility_lookback:i].std()
 long_term_volatility = data['returns'].iloc[:i].std()

# Adaptation of the size of the window on basis of volatility
 volatility_ratio = recent_volatility / long_term_volatility

if volatility_ratio > 1.5: # High volatility
Windows_size = int(base_window * 0.7) # Less window
elif volatility_ratio < 0.7: # Low volatility
Windows_size = int(base_window * 1.3) # More window
 else:
 window_size = base_window

# Training data
 train_data = data[i-window_size:i]

# Testsy data
 test_data = data[i:i+test_window]

# Model learning
 model.fit(train_data)

# Premonition
 predictions = model.predict(test_data)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

 results.append({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'window_size': window_size,
 'volatility_ratio': volatility_ratio,
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return
 })

 return pd.dataFrame(results)

# Example of use
vol_adaptive_results = volatility_adaptive_Analysis(data, model, base_window=252)
```

### 3. Multilevel Walk-Forward analysis

## ♪ Architecture multilevel Analisis

```mermaid
graph TD
A [Reference data] --> B [Plough-level Walk-Forward analysis]

B -> C[Level 1: Basic models]
 C --> D[Random Forest]
 C --> E[XGBoost]
 C --> F[LightGBM]

B -> G[Level 2: Ansemble Model]
 G --> H[Linear Regression]
 G --> I[Neural network]
 G --> J[Stacking]

D -> K [Base models projection]
 E --> K
 F --> K

K --> L[Metha signs<br/>Meta-features]
L -> M [Learning the ensemble model]

M --> N[Ansambal predictions]
N -> O [Strategy return calculation]

O-> P[quality metrics]
P --> Q [Sharp coefficient]
P --> R [Maximum draught]
P-> S [Total return]

Q -> T [Individual models]
 R --> T
 S --> T

T --> U[Comparison performance]
U -> V [Best Model]
U --> W [Medical performance]
U --> X [Ansemble performance]

V -> Y[Stability Analysis]
 W --> Y
 X --> Y

Y -> Z [Effect assessment of strategy]
Z --> AA {The Strategy is ready?}
AA --\\\\\b[\\\Deploy in sales]
AA --\\\\\\\C[\\\ensemble optimization]

CC --> DD[configration of model weights]
DD --> EE[Re-test]
 EE --> B

 style A fill:#e3f2fd
 style C fill:#c8e6c9
 style G fill:#fff3e0
 style BB fill:#4caf50
 style CC fill:#ff9800
```

**Herarchical analysis:**

```python
def hierarchical_walk_forward(data, models, train_window=252, test_window=30, step=30):
""""""""""""""""""""""""
 results = []

 for i in range(train_window, len(data) - test_window, step):
# Training data
 train_data = data[i-train_window:i]

# Testsy data
 test_data = data[i:i+test_window]

# Training all models
 model_predictions = {}
 for name, model in models.items():
 model.fit(train_data)
 model_predictions[name] = model.predict(test_data)

# Combination of preferences
 combined_predictions = np.mean(List(model_predictions.values()), axis=0)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = combined_predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

# Individual models
 individual_metrics = {}
 for name, predictions in model_predictions.items():
 individual_returns = predictions * returns
 individual_metrics[name] = {
 'sharpe': individual_returns.mean() / individual_returns.std() * np.sqrt(252),
 'max_drawdown': calculate_max_drawdown(individual_returns),
 'total_return': individual_returns.sum()
 }

 results.append({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'combined_sharpe': sharpe,
 'combined_max_drawdown': max_drawdown,
 'combined_total_return': total_return,
 'individual_metrics': individual_metrics
 })

 return pd.dataFrame(results)

# Example of use
models = {
 'model1': RandomForestRegressor(),
 'model2': XGBRegressor(),
 'model3': LGBMRegressor()
}
hierarchical_results = hierarchical_walk_forward(data, models, train_window=252)
```

** Ansemble analysis:**

```python
def ensemble_walk_forward(data, base_models, ensemble_model, train_window=252,
 test_window=30, step=30):
""Walk-Forward analysis with an ensemble."
 results = []

 for i in range(train_window, len(data) - test_window, step):
# Training data
 train_data = data[i-train_window:i]

# Testsy data
 test_data = data[i:i+test_window]

# Training basic models
 base_predictions = []
 for name, model in base_models.items():
 model.fit(train_data)
 predictions = model.predict(test_data)
 base_predictions.append(predictions)

# creative meta-signs
 meta_features = np.column_stack(base_predictions)

# Training the ensemble model
 ensemble_model.fit(meta_features, test_data['returns'])

# The ensemble's predictions
 ensemble_predictions = ensemble_model.predict(meta_features)

# Quality assessment
 returns = test_data['returns']
 strategy_returns = ensemble_predictions * returns

# metrics
 sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252)
 max_drawdown = calculate_max_drawdown(strategy_returns)
 total_return = strategy_returns.sum()

 results.append({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'sharpe': sharpe,
 'max_drawdown': max_drawdown,
 'total_return': total_return,
 'base_predictions': base_predictions,
 'ensemble_predictions': ensemble_predictions
 })

 return pd.dataFrame(results)

# Example of use
base_models = {
 'rf': RandomForestRegressor(),
 'xgb': XGBRegressor(),
 'lgb': LGBMRegressor()
}
ensemble_model = LinearRegression()
ensemble_results = ensemble_walk_forward(data, base_models, ensemble_model)
```

## quality metrics Walk-Forward Analysis

### ♪ a quality list of Walk-Forward Analysis

```mermaid
graph TD
A[Metrics of quality Walk-Forward] --> B [Temporary metrics]
A -> C [Statistical metrics]
A --> D [Economic metrics]

B -> B1 [Stability over time]
B1-> B11[Stable Sharp coefficient <br/>1 / (std / mean)]
B1 --> B12 [Trend performance<br/>polyfit slope]
B1 --> B13 [Vulnerability performance<br/>rolling std]
B1 -> B14 [Stand stability factor<br/>1 / volatility]

B --> B2 [Aptitude]
B2 --> B21 [Accordance speed<br/>abs(current-recent) / recent]
B2 --> B22 [Acadaptive volatility<br/>std adaptation_speed]
B2 --> B23 [Aptitude factor<br/>mean_speed / volatility]

C --> C1 [Statistical significance]
C1 --> C11 [Text on normality<br/>Shapiro-Wilk p-value > 0.05]
C1 --> C12 [Text on stationary <br/>ADF p-value < 0.05]
C1 --> C13 [Confidence interval<br/>t-distribution 95 per cent]
C1 --> C14 [Statistical significance<br/>ADF < 0.05 AND Shapiro > 0.05]

C --> C2 [Correlation with market]
C2 --> C21 [Correlation with volatility<br/>corr(sharpe, volatility)]
C2 --> C22 [Correlation with profitability<br/>corr(sharpe, returns)]
C2 --> C23 [Collection with trend<br/>corr(sharpe, trend)]

D -> D1 [Economic significance]
D1 -> D11 [Clustering transaction costs<br/>net_returns = returns - costs]
D1 -> D12 [Minimum Sharp coefficient<br/>≥ 1.0]
D1 -> D13 [Maximum draught <br/> < 20 per cent]
D1-> D14[% successful periods<br/> > 60%]

D -> D2 [Recentness]
D2 --> D21 [cumulative return<br/>cumprod(1 + returns)]
D2-> D22[The actual value of the portfolio<br/>initial *cumulative]
D2 --> D23 [annual return<br/>annuated return]
D2 --> D24 [Maximum draught <br/>min drawdown]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style C fill:#fff3e0
 style D fill:#f3e5f5
```

### 1. Temporary metrics

**Stability over time:**

```python
def calculate_temporal_stability(results):
 """
Calculation of time stability

Analyses the stability of the Sharpe coefficient and other metrics over time,
which is a key quality indicator of Walk-Forward Anallysis.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- index: Time tags periods (datetime)

 Returns:
 --------
 dict
Vocabulary with meters of stability:
- 'sharpe_state': stability of Sharp coefficient (float)
- > 2.0: Excellent stability
- 1.0-2.0: good stability
- 0.5-1.0: Moderate stability
< 0.5: Low stability
- 'sharpe_trend': trend of Sharp coefficient (float)
- > 0: improve with time
- = 0: stable performance
< 0: deterioration over time
- 'Performance_volatility': volatility performance (float)
< 0.1: Low volatility
0.1-0.3: Moderate volatility
- > 0.3: High volatility
- 'Stability_co-officer': total stability coefficient (float)
- > 10: Excellent stability
- 5-10: good stability
- 2-5: Moderate stability
- < 2: Low stability

 Raises:
 -------
 ValueError
If results note contains column 'sharpe'
If the results are empty or contains NaN values

 Notes:
 ------
- Stability is calculated as the return value to the coefficient of variation
- Tread is calculated with linear regression
- Volatility is calculated as a sliding standard deviation
- A minimum of 10 periods for reliable evaluation is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> stability = calculate_temporal_stability(results)
>>print(f) "Stability of Sharp:['sharpe_state']:2f}")
 """
# Stable Sharpe coefficient
 sharpe_std = results['sharpe'].std()
 sharpe_mean = results['sharpe'].mean()
 sharpe_stability = 1 / (sharpe_std / sharpe_mean) if sharpe_mean != 0 else 0

# Tread performance
 sharpe_trend = np.polyfit(range(len(results)), results['sharpe'], 1)[0]

# Volatility performance
 performance_volatility = results['sharpe'].rolling(5).std().mean()

# Stability factor
 stability_coefficient = 1 / performance_volatility if performance_volatility > 0 else 0

 return {
 'sharpe_stability': sharpe_stability,
 'sharpe_trend': sharpe_trend,
 'performance_volatility': performance_volatility,
 'stability_coefficient': stability_coefficient
 }

# Example of use
temporal_metrics = calculate_temporal_stability(wf_results)
```

** Adaptation:**

```python
def calculate_adaptability(results, lookback=5):
 """
Calculation of the model &apos; s adaptation to changing conditions

Analyses the model &apos; s ability to adapt to new market conditions
on baseline changes in time.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- index: Time tags periods (datetime)

 lookback : int, default=5
Number of periods for the calculation of adaptiveity:
- 5: five periods (recommended)
- 3: three periods (for rapid adaptation)
- 10: 10 periods (for stable estimates)
- Minimum: 2 periods for calculation
- Maximum: 20 periods for avoidance of obsolescence

 Returns:
 --------
 dict
The dictionary with metrics of adaptiveity:
- 'mean_adaptation_speed': average adaptation speed (float)
- > 0.2: High adaptive
0.1-0.2: Moderate adaptation
- 0.05-0.1: Low adaptiveity
< 0.05: Very low adaptive
- 'adaptation_volatility': float variability
< 0.1: Stable adaptation
0.1-0.3: Moderate volatility
> 0.3: Unstable adaptation
- 'adaptability_co-officer': adaptive factor (float)
- > 2.0: Excellent adaptation
- 1.0-2.0: good adaptation
- 0.5-1.0: Moderate adaptation
< 0.5: Low adaptiveity

 Raises:
 -------
 ValueError
If results note contains column 'sharpe'
If lookback < 2 or lookback > Len(results) - 1
If the results are empty or contains NaN values

 Notes:
 ------
- The rate of adaptation is calculated as absolute change
previous performances
- The volatility of adaptation demonstrates the stability of the adaptation process
- Adaptation factor - ratio of speed to volatility
- A minimum of 10 periods for reliable evaluation is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> adaptability = calculate_adaptability(results, lookback=5)
>>print(f) "Acceleration speed: {'mean_adaptation_speed']:3f}")
 """
# The speed of adaptation
 adaptation_speed = []
 for i in range(lookback, len(results)):
 recent_performance = results['sharpe'].iloc[i-lookback:i].mean()
 current_performance = results['sharpe'].iloc[i]
 adaptation = abs(current_performance - recent_performance) / recent_performance
 adaptation_speed.append(adaptation)

# Average rate of adaptation
 mean_adaptation_speed = np.mean(adaptation_speed)

# The volatility of adaptation
 adaptation_volatility = np.std(adaptation_speed)

# Adaptation factor
 adaptability_coefficient = mean_adaptation_speed / adaptation_volatility if adaptation_volatility > 0 else 0

 return {
 'mean_adaptation_speed': mean_adaptation_speed,
 'adaptation_volatility': adaptation_volatility,
 'adaptability_coefficient': adaptability_coefficient
 }

# Example of use
adaptability_metrics = calculate_adaptability(wf_results, lookback=5)
```

###2: Statistical metrics

**Statistical significance:**

```python
def calculate_statistical_significance(results, confidence_level=0.95):
 """
Calculation of the statistical significance of the results of the Walk-Forward Analysis

Conducts statistical tests for assessing the relevance of results:
- Test on normality (Shapiro-Wilk)
- Augmented Dickey-Fuller test
- Calculation of confidence intervals

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- index: Time tags periods (datetime)

 confidence_level : float, default=0.95
Trust level for confidence intervals:
0.95: 95% confidence interval (recommended)
0.99: 99% confidence interval (for conservative estimates)
0.90: 90% confidence interval (for less stringent estimates)
- Minimum: 0.80 (80% confidence interval)
- Maximum: 0.999 (99.9% confidence interval)

 Returns:
 --------
 dict
The dictionary with the results of statistical tests:
- 'Shapiro_statistical': Shapiro-Wilke test statistics (float)
- 'schapiro_pvalue': p-value test on normality (float)
- > 0.05: data is normally distributed
- <= 0.05: data not normally distributed
- 'adf_statistical': ADF test statistics (float)
- 'adf_value': p-value test on stability (float)
< 0.05: data are stationary
- > = 0.05: data not fixed
- 'confidence_interval': confidence interval (tuple)
- (lower_bound, super_bound) for the average Sharpe coefficient
- 'is_significant': general statistical significance (boool)
- True: the results are statistically significant
- False: results not statistically significant

 Raises:
 -------
 ValueError
If results note contains column 'sharpe'
If confidence_level < 0.80 or conference_level > 0.999
If the results are empty or contains NaN values

 Notes:
 ------
- The normality test checks that Sharp coefficients are normally distributed.
- Instability test checks that performance is stable over time.
- The confidence interval is calculated with t-distribution
- A minimum of 30 periods for reliable statistical tests is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> significance = calculate_statistical_significance(results, confidence_level=0.95)
>>print(f"Statistically significant: {significance['is_significant']}})
 """
 from scipy import stats

# Test on normality
 shapiro_stat, shapiro_pvalue = stats.shapiro(results['sharpe'])

# A test on parking
 adf_stat, adf_pvalue = stats.adfuller(results['sharpe'])

# Confidence interval
 mean_sharpe = results['sharpe'].mean()
 std_sharpe = results['sharpe'].std()
 n = len(results)

 t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
 margin_error = t_value * std_sharpe / np.sqrt(n)

 confidence_interval = (mean_sharpe - margin_error, mean_sharpe + margin_error)

# Statistical significance
 is_significant = adf_pvalue < 0.05 and shapiro_pvalue > 0.05

 return {
 'shapiro_statistic': shapiro_stat,
 'shapiro_pvalue': shapiro_pvalue,
 'adf_statistic': adf_stat,
 'adf_pvalue': adf_pvalue,
 'confidence_interval': confidence_interval,
 'is_significant': is_significant
 }

# Example of use
statistical_metrics = calculate_statistical_significance(wf_results)
```

**Correlation with market conditions:**

```python
def calculate_market_correlation(results, market_data):
"The calculation of the correlation with market conditions."
# Correlation with market volatility
 market_volatility = market_data['returns'].rolling(30).std()
 volatility_correlation = results['sharpe'].corr(market_volatility.iloc[results.index])

# The correlation with market returns
 market_returns = market_data['returns'].rolling(30).mean()
 returns_correlation = results['sharpe'].corr(market_returns.iloc[results.index])

# Correlation with market trend
 market_trend = market_data['price'].rolling(30).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
 trend_correlation = results['sharpe'].corr(market_trend.iloc[results.index])

 return {
 'volatility_correlation': volatility_correlation,
 'returns_correlation': returns_correlation,
 'trend_correlation': trend_correlation
 }

# Example of use
market_correlation = calculate_market_correlation(wf_results, market_data)
```

♪## 3. Economic metrics

** Economic significance:**

```python
def calculate_economic_significance(results, transaction_costs=0.001,
 min_sharpe=1.0, max_drawdown=0.2):
 """
Calculation of the economic significance of the results of the Walk-Forward Analysis

Assesses the economic viability of the strategy with accounting
transaction costs and practical constraints.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- index: Time tags periods (datetime)

 transaction_costs : float, default=0.001
The transaction costs on one transaction (in shares from capital):
- 0.001: 0.1 per cent (recommended for shares)
- 0.0005: 0.05 per cent (for ETF and index)
- 0.002: 0.2 per cent (forforforx and cryptically)
- 0.005: 0.5 per cent (for exotic assets)
- Minimum: 0.0001 (0.01%)
- Maximum: 0.01 (1 per cent)

 min_sharpe : float, default=1.0
Minimum acceptable Sharpe coefficient:
- 1.0: Baseline (recommended)
- 1.5: Good level for professional strategies
- 2.0: Excellent level for institutional strategies
- 0.5: Minimum level for conservative strategies
- Minimum: 0.1
- Maximum: 5.0

 max_drawdown : float, default=0.2
Maximum permissible draught (in shares from capital):
0.2: 20% (recommended for most strategies)
0.1: 10% (for conservative strategies)
0.3: 30% (for aggressive strategies)
- 0.05: 5% (for very conservative strategies)
- Minimum: 0.01 (1 per cent)
- Maximum: 0.5 (50%)

 Returns:
 --------
 dict
The dictionary with metrics of economic significance:
- 'mean_sharpe': average Sharp coefficient (float)
- 'mean_max_drawdown': average maximum draught (float)
- 'access_rate': % of successful periods (float)
- >=0.7: Excellent strategy
- 0.5-0.7: Good strategy
0.3-0.5: Moderate strategy
< 0.3: weak strategy
- 'economically_significant': overall economic significance (boool)
- True: The strategy is economically meaningful.
- False: strategy not economically significant

 Raises:
 -------
 ValueError
If results note contain columns 'sharpe', 'max_drawdown', 'total_return'
If transfer_costs < 0 or transfer_costs > 0.01
If min_sharpe < 0.1 or min_sharpe > 5.0
If max_drawdown < 0.01 or max_drawdown > 0.5

 Notes:
 ------
- The transaction costs are deducted from the total return
- A successful period with Sharp coefficient >=min_sharpe
- Economic significance requires compliance with all criteria simultaneously
- A minimum of 20 periods for reliable evaluation is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> economic = calculate_economic_significance(results, transaction_costs=0.001)
>>print(f" Economically significant: {economic['economically_significant']}})
 """
# Accounting for transaction costs
 net_returns = results['total_return'] - transaction_costs

# metrics
 mean_sharpe = results['sharpe'].mean()
 mean_max_drawdown = results['max_drawdown'].mean()
 success_rate = (results['sharpe'] > min_sharpe).mean()

# Economic significance
 economically_significant = (
 mean_sharpe >= min_sharpe and
 abs(mean_max_drawdown) <= max_drawdown and
 success_rate >= 0.6
 )

 return {
 'mean_sharpe': mean_sharpe,
 'mean_max_drawdown': mean_max_drawdown,
 'success_rate': success_rate,
 'economically_significant': economically_significant
 }

# Example of use
economic_metrics = calculate_economic_significance(wf_results, transaction_costs=0.001)
```

**Purity:**

```python
def calculate_profitability(results, initial_capital=100000):
 """
Calculation of the cost-effectiveness of the strategy on baseline results

Reviews the cost-effectiveness of the strategy with accounting
Capital formation and cumulative returns.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'Total_return': total return for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- index: Time tags periods (datetime)

 initial_capital : float, default=100000
Initial capital for calculation of profitability:
- 100,000: $100,000 (recommended for testing)
- 10,000: $10,000.
- 1000000: $1,000.000 (for institutional strategies)
- 1000: $1,000 (for demo accounts)
- Minimum: 100 (for minimum test)
- Maximum: 100,000 (for large portfolios)

 Returns:
 --------
 dict
Vocabulary with metrics of profitability:
- 'final_value': final value of portfolio (float)
- 'Total_return': total return for the whole period (float)
- > 0.5: Excellent return (50 per cent+)
- 0.2-0.5: good return (20-50 per cent)
0.1-0.2: Moderate return (10-20%)
< 0.1: Low return (<10 per cent)
- 'annual_return': annual return (float)
> 0.2: Excellent annual rate of return (20 per cent+)
0.1-0.2: good annual rate of return (10-20%)
- 0.05-0.1: Moderate annual rate (5-10 per cent)
< 0.05: low annual rate of return (<5%)
- 'max_drawdown': maximum draught over the whole period (float)
< 0.1: excellent stability (<10 per cent)
0.1-0.2: good stability (10-20%)
0.2-0.3: Moderate stability (20-30 per cent)
- > 0.3: Low stability (> 30 per cent)

 Raises:
 -------
 ValueError
If results note contains columns 'total_return', 'max_drawdown'
If initial_capital <=0 or initial_capital > 10,000000
If the results are empty or contains NaN values

 Notes:
 ------
- Cumulative yield is calculated as a product (1 + returns)
- Annual rate of return is calculated with the number of years
- The maximum draught is taken from at least all periods.
- A minimum of 12 periods for calculation of annual return is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> profitability = calculate_profitability(results, initial_capital=100000)
>>print(f) "Final value: {profitiability['final_value']:,2f}")
 """
# Cumulative returns
 cumulative_returns = (1 + results['total_return']).cumprod()

# Final value of portfolio
 final_value = initial_capital * cumulative_returns.iloc[-1]

# Total return
 total_return = (final_value - initial_capital) / initial_capital

# Annual return
Years = Len(s) / 12 # We estimate monthly results
 annual_return = (final_value / initial_capital) ** (1 / years) - 1

# Maximum tarmac
 max_drawdown = results['max_drawdown'].min()

 return {
 'final_value': final_value,
 'total_return': total_return,
 'annual_return': annual_return,
 'max_drawdown': max_drawdown
 }

# Example of use
profitability_metrics = calculate_profitability(wf_results, initial_capital=100000)
```

## Visualization of Walk-Forward Analysis

## # Dashbord visualization of Walk-Forward Analysis results

```mermaid
graph TD
A [Walk-Forward Analysis] - • B [Dashboard Visualization]

B -> C [Temporary graphs]
C --> C1 [Sharp coefficient over time<br/>with minimum 1.0 line]
C --> C2 [Maximum time lag<br/>with the maximum - 20 per cent line]
C --> C3 [Cumulative return<br/>with markers periods]

B -> D [Distribution schedules]
D -> D1[Sharp coefficient histogram<br/>with middle line]
D --> D2[Box flat metric<br/>with emissions and quintiles]
D --> D3[Q-Q table normality<br/>for statistical tests]

B --> E [Technal maps]
E --> E1 [Coordination matrix<br/> metric among themselves]
E --> E2 [performance on periods<br/>years × months]
E --> E3 [Telephone map of volatility<br/>in time and metrics]

B -> F [Comparative graphs]
F --> F1[comparson of methods<br/>Fixed vs Expanding vs Adaptation]
F --> F2[comparison of models<br/>Individual vs Ensemble]
F --> F3[comparison periods<br/>Bull vs Bear markets]

C1-> G[Interactive elements]
 C2 --> G
 C3 --> G
 D1 --> G
 D2 --> G
 D3 --> G
 E1 --> G
 E2 --> G
 E3 --> G
 F1 --> G
 F2 --> G
 F3 --> G

 G --> H[Zoom and Pan functions]
G --> I [Filter on Periods]
G --> J [Export in different formats]
G --> K[configuration of colour patterns]

H --> L [Final Dashboard]
 I --> L
 J --> L
 K --> L

L -> M[Analysis of trends]
L -> N [Identifying anomalies]
L -> O [Stability assessment]

M -> P [Recommendations on strategy]
 N --> P
 O --> P

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style G fill:#fff3e0
 style P fill:#4caf50
```

♪##1 ♪ Timetables

```python
def visualize_walk_forward_results(results, save_path=None):
 """
Visualization of Walk-Forward Analysis results

Creates an integrated dashboard with graphics for Analysis performance
Time use strategies, including time series and metric distribution.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- index: Time tags periods (datetime)

 save_path : str, optional
Way to keep the schedule:
- None: the graph is displayed on the screen (on default)
- 'path/to/file.png': Save in PNG format
- 'path/to/file.pdf': Save in PDF format
- 'path/to/file.svg': Save in SVG format
Supported formats: .png, .pdf, .svg, .jpg, .jpeg

 Returns:
 --------
 None
Graph is displayed on screen or stored in file

 Raises:
 -------
 ValueError
If results note contain columns 'sharpe', 'max_drawdown', 'total_return'
If the results are empty or contains NaN values

 importError
If not installed matplotlib or seaborn

 Notes:
 ------
The figure 2x2 is created with four graphs:
1. Sharp coefficient in time with minimum 1.0 line
2. Maximum delay in time with maximum -20 per cent line
3. Sharp coefficient distribution with the average
4. Cumulative yield over time
- Style 'seaborn-v0_8' for professional type
- Graphs automatically scale and format
- A minimum of 10 periods for informative graphs is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> visualize_walk_forward_results(results)
 >>> visualize_walk_forward_results(results, save_path='results.png')
 """
 import matplotlib.pyplot as plt
 import seaborn as sns

# configuring style
 plt.style.Use('seaborn-v0_8')
 sns.set_palette("husl")

# Create figures
 fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Sharp coefficient over time
 axes[0, 0].plot(results.index, results['sharpe'], marker='o')
axes[0,0]. axhline(y=1.0, color='red', line='--', label='Minimal Sharpe')
axes[0,0].set_title('Sharp in time')
axes[0,0].set_xlabel('Period')
axes[0,0].set_ylabel('Sharpa's coefficient')
 axes[0, 0].legend()
 axes[0, 0].grid(True)

# 2. Maximum time lag
 axes[0, 1].plot(results.index, results['max_drawdown'], marker='o', color='red')
axes[0, 1]. axhline(y=-0.2, color='red', line='--', label='Maximal 20 per cent')
axes[0,1].set_title('Maximal time gap')
axes[0, 1].set_xlabel('Period')
axes[0, 1].set_ylabel('Maximal prosperity')
 axes[0, 1].legend()
 axes[0, 1].grid(True)

# 3. Sharpe coefficient distribution
 axes[1, 0].hist(results['sharpe'], bins=20, alpha=0.7, edgecolor='black')
 axes[1, 0].axvline(results['sharpe'].mean(), color='red', linestyle='--',
Label=f'Medial: {results}mean(:2f}'
axes[1, 0].set_title('Sharp coefficient distribution')
axes[1, 0].set_xlabel('Sharpa's coefficient')
axes[1, 0].set_ylabel('Part')
 axes[1, 0].legend()
 axes[1, 0].grid(True)

# 4. Cumulative returns
 cumulative_returns = (1 + results['total_return']).cumprod()
 axes[1, 1].plot(results.index, cumulative_returns, marker='o')
axes[1, 1].set_title('cumulative return')
axes[1, 1].set_xlabel('Period')
axes[1, 1].set_ylabel('cumulative return')
 axes[1, 1].grid(True)

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
visualize_walk_forward_results(wf_results, save_path='walk_forward_results.png')
```

♪##2 ♪ Warm cards

```python
def create_heatmap_Analysis(results, save_path=None):
 """
code heat maps for Analysis of Walk-Forward Results

Creates heat maps for visualizing correlations between metrics
and performance on different time periods.

 Parameters:
 -----------
 results : pd.dataFrame
The results of Walk-Forward Analysis with columns:
- 'sharpe': Sharpe coefficient for each period (float)
- 'max_drawdown': maximum draught for each period (float)
- 'Total_return': total return for each period (float)
- 'Window_size': the size of the learning window (int, option)
- index: Time tags periods (datetime)

 save_path : str, optional
Way to keep the schedule:
- None: the graph is displayed on the screen (on default)
- 'path/to/file.png': Save in PNG format
- 'path/to/file.pdf': Save in PDF format
- 'path/to/file.svg': Save in SVG format
Supported formats: .png, .pdf, .svg, .jpg, .jpeg

 Returns:
 --------
 None
Graph is displayed on screen or stored in file

 Raises:
 -------
 ValueError
If results note contain columns 'sharpe', 'max_drawdown', 'total_return'
If the results are empty or contains NaN values

 importError
If not installed matplotlib or seaborn

 Notes:
 ------
The figure 1x2 is created with two heat maps:
1. Correlation matrix between metrics (sharpe, max_drawdown, total_return)
2. Performance on Periods (years x months) - if present Windows_size
- The correlation matrix uses the color scheme 'coolwarm' with centre in 0
- The warm card performance uses the color scheme 'RdYlGn' with centre in 1.0
- Automatically handles the absence of a Windows_size column
- A minimum of 12 periods for informative heat cards is recommended

 Examples:
 ---------
 >>> results = walk_forward_Analysis(data, model)
 >>> create_heatmap_Analysis(results)
 >>> create_heatmap_Analysis(results, save_path='heatmap.png')
 """
 import matplotlib.pyplot as plt
 import seaborn as sns

# creative correlation matrix
 correlation_matrix = results[['sharpe', 'max_drawdown', 'total_return']].corr()

# Create figures
 fig, axes = plt.subplots(1, 2, figsize=(15, 6))

♪ 1 ♪ Warm map of correlations
 sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
 square=True, ax=axes[0])
axes[0].set_title('Correlation matrix metric')

# 2. Warm Card Performance on Periods
 if 'window_size' in results.columns:
 pivot_table = results.pivot_table(values='sharpe',
* Years
Columns = results.index%12, # Months
 fill_value=0)
 sns.heatmap(pivot_table, annot=True, cmap='RdYlGn', center=1.0,
 ax=axes[1])
axes[1].set_title('performance on periods')
axes[1].set_xlabel('Menice')
axes[1].set_ylabel('Year')

 plt.tight_layout()

 if save_path:
 plt.savefig(save_path, dpi=300, bbox_inches='tight')

 plt.show()

# Example of use
create_heatmap_Analysis(wf_results, save_path='walk_forward_heatmap.png')
```

## Walk-Forward Anallysis Automation

### ♪ Walk-Forward Anallysis Automation Pikeline

```mermaid
graph TD
A [Reference data] --> B [WalkForwardPipeline]
B -> C [configration of parameters]

C --> D[Fixed window<br/>training_window: 252<br/>test_window: 30]
C --> E [Expansing window<br/>initial_window: 252<br/>growing data]
C --> F[Adjustative window<br/>min: 100, max: 500<br/>dinamic extension]

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

M -> N [Generation of Integrated Reporta]
N -> O[Report on methods]
N -> P [Detail results]
N -> Q [Recommendations]

O-> R [Mean Sharpe coefficient]
O-> S [standard deviation]
O -> T[per cent of successful strategies]
O-> U[Sharp coefficient stability]
O-> V [Trend performance]

P --> W [Individual results]
P --> X[comparison of methods]
P -> Y [Temporary Pathers]

Q -> Z [Evaluation of performance]
Z --> AA [Great: Sharpe > 1.5, Science > 70 per cent]
Z --> BB [Good: Sharpe > 1.0, Science > 50 per cent]
Z -> CC [Required for improvement: otherwise]

AA --> DD[~ Strategy is ready to go]
BB --> EE[~ Strategy requires Monitoring]
CC-> FF[~ Strategy needs further development]

DD --> GG [Property in Sales]
EE --> HH [Further testing]
FF --> II [Optimization of parameters]

II -> JJ [configuring learning window]
JJ --> KK[Return testing]
 KK --> B

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style N fill:#fff3e0
 style DD fill:#4caf50
 style EE fill:#ff9800
 style FF fill:#ffcdd2
```

♪##1 ♪ Pipline Walk-Forward Analysis

```python
class WalkForwardPipeline:
 """
Walk-Forward Analisis Automation Pipline

Integrated class for different types of Walk-Forward Analysis
with automatic generation of Reports and Recommendations.

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns:
- 'returns': asset return (float)
- 'features': signs for the model (array-lake)
- Index: Time tags (datetime)

 model : sklearn-compatible model
The object of the model machine lightning with methods is:
- Fit(X, y): Model training
- predict(X): predictions
Should be compatible with sclearn API

 metrics_calculator : object
Object for calculation of quality metric with method:
- calculate(returns): calculation of metric on base return
Should return the dictionary with metrics (sharpe, max_drawdown, total_return)

 Attributes:
 -----------
 data : pandas.dataFrame
Reference data for Analysis

 model : sklearn-compatible model
Machine lightning model

 metrics_calculator : object
Quality meter calculator

 results : dict
The dictionary with results of different types of Analysis:
- 'fixed_window': fixed window results
- 'expanding_window': Results of an expanding window
- 'Adaptive_Window': Results of an adaptive window

 Methods:
 --------
 run_fixed_window_Analysis(train_window, test_window, step)
Launch Analysis with a fixed window

 run_expanding_window_Analysis(initial_train_window, test_window, step)
Launch Analysis with an expanding window

 run_adaptive_window_Analysis(min_window, max_window, test_window, step)
Launch Analysis with adaptive window

 generate_comprehensive_Report()
Integrated report generationa

 Raises:
 -------
 ValueError
If data not contains the necessary columns
If model not has methods fit and predict
If metrics_calculator not has a calculate method

 Examples:
 ---------
 >>> from sklearn.ensemble import RandomForestRegressor
 >>> from src.metrics import MetricsCalculator
 >>>
 >>> model = RandomForestRegressor(n_estimators=100)
 >>> metrics_calc = MetricsCalculator()
 >>> pipeline = WalkForwardPipeline(data, model, metrics_calc)
 >>>
>> #Launch all types of Analysis
 >>> pipeline.run_fixed_window_Analysis()
 >>> pipeline.run_expanding_window_Analysis()
 >>> pipeline.run_adaptive_window_Analysis()
 >>>
>>#Report generationa
 >>> Report = pipeline.generate_comprehensive_Report()
 """

 def __init__(self, data, model, metrics_calculator):
 """
 Pipeline initialization Walk-Forward Analysis

 Parameters:
 -----------
 data : pandas.dataFrame
Time series with columns 'returns' and 'features'

 model : sklearn-compatible model
Machine Learning with Fit and Predict

 metrics_calculator : object
Calculator metric with calculate method
 """
 self.data = data
 self.model = model
 self.metrics_calculator = metrics_calculator
 self.results = {}

 def run_fixed_window_Analysis(self, train_window=252, test_window=30, step=30):
 """
Launch Walk-Forward Anallysis with a fixed learning window

 Parameters:
 -----------
 train_window : int, default=252
Size of learning window in days:
- 252: one trade year (recommended)
126: Six months (for rapid testing)
- 504: two years (for long-term strategies)
- Minimum: 50 days for stability
- Maximum: 1,000 days for avoidance of retraining

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
- 'Window_size': the size of the learning window (int)
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If train_window < 50 or test_widow < 5
If step > test_wind
If Len(data) < train_widow + test_window

 Notes:
 ------
- The results are stored in elf.results['fixed_window']
- The model is retrained on every step.
- Suitable for strategies with stable market conditions
 """
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
 metrics.update({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'window_size': train_window
 })

 results.append(metrics)

 self.results['fixed_window'] = pd.dataFrame(results)
 return self.results['fixed_window']

 def run_expanding_window_Analysis(self, initial_train_window=252, test_window=30, step=30):
 """
Launch Walk-Forward Anallysis with an expanding learning window

 Parameters:
 -----------
 initial_train_window : int, default=252
Initial size of the learning window in days:
- 252: one trade year (recommended)
126: Six months (for rapid testing)
- 504: two years (for long-term strategies)
- Minimum: 50 days for stability
After that, the window will expand on step days every iteration.

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
- 'Window_size': the size of the learning window (int) - increases over time
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If initial_training_window < 50 or test_window < 5
If step > test_wind
If Len(data) < initial_training_window + test_window

 Notes:
 ------
- The results are stored in elf.results['expanding_window']
- The learning window is constantly growing, using all available history.
- Could be slower than a fixed window due to the increase in data size.
- It is appropriate for strategies where historical data remain relevant
 """
 results = []

 for i in range(initial_train_window, len(self.data) - test_window, step):
# Learning data (expanding window)
 train_data = self.data[:i]

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
 metrics.update({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'window_size': len(train_data)
 })

 results.append(metrics)

 self.results['expanding_window'] = pd.dataFrame(results)
 return self.results['expanding_window']

 def run_adaptive_window_Analysis(self, min_window=100, max_window=500,
 test_window=30, step=30):
 """
Launch Walk-Forward Anallysis with an adaptive learning window

 Parameters:
 -----------
 min_window : int, default=100
Minimum size of teaching window in days:
100: minimum for stability (recommended)
- 50: for rapid testing
- 200: for conservative strategies
- Minimum: 30 days for statistical significance
- Maximum: 300 days for avoidance of retraining

 max_window : int, default=500
Maximum size of learning window in days:
- 500: two years of trade days (recommended)
- 252: one year (for rapid strategies)
- 1000: four years (for long-term strategies)
- Minimum: min_Window + 100
- Maximum: 2,000 days for avoidance of retraining

 test_window : int, default=30
Size of test window in days:
- 30: one month (recommended)
- 7: One week (for high frequency strategies)
90: quarter (for long-term strategies)
- Minimum: 5 days for statistical significance
- Maximum: 180 days for avoidance of obsolescence

 step : int, default=30
Step of window shift in days:
- 30: monthly retraining (recommended)
- 7: weekly retraining (for active strategies)
- 1: Daily retraining (for high frequency strategies)
90: quarterly retraining (for conservative strategies)
- step <=test_widow for missing data

 Returns:
 --------
 pd.dataFrame
Results of Analysis with columns:
- 'training_start': Start of study period (datetime)
- 'training_end': end of period of study (datetime)
- 'test_start': Start of the test period (datetime)
- 'test_end': end of test period (datetime)
'Window_size': the current size of the learning window (int)
- 'sharpe': Sharp coefficient over the period float
- 'max_drawdown': maximum tare period (float)
- 'Total_return': total return over period (float)

 Raises:
 -------
 ValueError
If min_window < 30 or max_widow < min_widow + 100
If test_window < 5 or step > test_window
If Len(data) < min_window + test_window

 Notes:
 ------
- The results are stored in elf.results['adaptive_window']
- The size of the window adapts on base performance model
- The window increases when it deteriorates.
- With improved performance, the window decreases.
- Suitable for strategies with changing market conditions
 """
 results = []
 current_window = min_window

 for i in range(min_window, len(self.data) - test_window, step):
# Training data
 train_data = self.data[i-current_window:i]

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
 metrics.update({
 'train_start': train_data.index[0],
 'train_end': train_data.index[-1],
 'test_start': test_data.index[0],
 'test_end': test_data.index[-1],
 'window_size': current_window
 })

# Adaptation of the size of the window
 if len(results) > 0:
 recent_sharpe = results[-1]['sharpe']
 current_sharpe = metrics['sharpe']

 if current_sharpe < recent_sharpe * 0.9:
 current_window = min(current_window + 50, max_window)
 elif current_sharpe > recent_sharpe * 1.1:
 current_window = max(current_window - 50, min_window)

 results.append(metrics)

 self.results['adaptive_window'] = pd.dataFrame(results)
 return self.results['adaptive_window']

 def generate_comprehensive_Report(self):
 """
Generation of the Integrated Results Report Walk-Forward Analysis

Creates a detailed Report with analysis of all types of Walk-Forward Analysis,
including aggregates, detailed results and recommendations.

 Returns:
 --------
 dict
Integrated Report with the following keys:
- 'summary': dictionary with composite metrics for each method
- 'fixed_window': metrics of a fixed window
- 'Expanding_window': metrics expanding window
- 'Adaptive_Window': metrics adaptive window
- Each method contains
- 'mean_sharpe': average Sharp coefficient (float)
- 'std_sharpe': standard deviation of Sharp coefficient (float)
- 'mean_max_drawdown': average maximum draught (float)
- 'access_rate': % of successful periods (float)
- 'sharpe_state': stability of Sharp coefficient (float)
- 'sharpe_trend': trend of Sharp coefficient (float)
- 'Detained_results': dictionary with detailed results
- 'fixed_window': DataFrame with fixed window results
- 'Expanding_window': DataFrame with the results of an expanding window
- 'adaptive_window': DataFrame with the results of an adaptive window
- 'recommendations': List of recommendations (List)
- Line with evaluation of performance of each method
- "Great performance": Sharpe > 1.5, Science > 70%
- "Good performance": Sharpe > 1.0, Science > 50%
- "Requires improvement": otherwise

 Raises:
 -------
 ValueError
If self.results empty or not contains expected keys
If the results of the note contain the necessary columns

 Notes:
 ------
- The report is generated on base all the tests performed
- Recommendations are based on threshold values of performance
- Stability is calculated as the return value to the coefficient of variation
- Tread is calculated with linear regression
- It is recommended to start all types of Analysis before producing the Report

 Examples:
 ---------
 >>> pipeline = WalkForwardPipeline(data, model, metrics_calc)
 >>> pipeline.run_fixed_window_Analysis()
 >>> pipeline.run_expanding_window_Analysis()
 >>> pipeline.run_adaptive_window_Analysis()
 >>>
 >>> Report = pipeline.generate_comprehensive_Report()
>> preint(recommendations:", Report['recommendations'])
 """
 Report = {
 'summary': {},
 'Detailed_results': self.results,
 'recommendations': []
 }

# Analysis of each method
 for method, results in self.results.items():
 if isinstance(results, pd.dataFrame):
# Basic metrics
 mean_sharpe = results['sharpe'].mean()
 std_sharpe = results['sharpe'].std()
 mean_max_drawdown = results['max_drawdown'].mean()
 success_rate = (results['sharpe'] > 1.0).mean()

# Stability
 sharpe_stability = 1 / (std_sharpe / mean_sharpe) if mean_sharpe != 0 else 0

# Trent
 sharpe_trend = np.polyfit(range(len(results)), results['sharpe'], 1)[0]

 Report['summary'][method] = {
 'mean_sharpe': mean_sharpe,
 'std_sharpe': std_sharpe,
 'mean_max_drawdown': mean_max_drawdown,
 'success_rate': success_rate,
 'sharpe_stability': sharpe_stability,
 'sharpe_trend': sharpe_trend
 }

# Recommendations
 if mean_sharpe > 1.5 and success_rate > 0.7:
Report(f)(`recommendations'): Excellent performance)
 elif mean_sharpe > 1.0 and success_rate > 0.5:
Report(f) (good performance)
 else:
Report ['recommendations'].append(f'{method}: Needs improvement")

 return Report

# Example of use
pipeline = WalkForwardPipeline(data, model, metrics_calculator)
pipeline.run_fixed_window_Analysis()
pipeline.run_expanding_window_Analysis()
pipeline.run_adaptive_window_Analysis()
Report = pipeline.generate_comprehensive_Report()
```

## Conclusion

The Walk-Forward analysis is the gold standard of performance ML strategies. It allows:

1. ** Simulate real trade** - The model is constantly re-trained
2. ** To test adaptation** - The model should Working in changing circumstances
3. ** Assess stability** - the results must be stable over time
4. ** Identify retraining** - No should remember historical data

### Key principles

1. ** Reality** - Use realistic parameters
2. ** Stability** - check the stability of the results
3. ** Adaptation** - The model has to adapt to the new environment
4. ** Statistical significance** - check the relevance of the results
5. ** Economic significance** - account for transaction costs

### Next steps

After learning Walk-Forward Analysis, go to:

- [Monte Carlo simulation](./29_monte_carlo_simulations.md)
- [Porthfolio Administration](./30_Porthfolio_Management.md)
