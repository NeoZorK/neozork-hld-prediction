# Deeper describe Feature Generation and Apply

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who Feature Generation is the key to success in ML

**Why 80 percent of the success of machine lyning depends on the quality of the signs?** Because even the best no algorithm can find patharies in bad data. Future Generation is the art of turning raw data into gold for machinin lyning.

### What gives you the right sign creation?

- **Total**: The Working on 20-50% models are better
- ** Interpretation**: Understanding what affects the outcome
- **Robity**: The Working Models are stable on new data
- ** Performance**: Less data, better results

### What happens without the correct generation of the signs?

- ** Bad results**: No models find pathers
- **retraining**: Models remember data instead of learning
- ** Instability**: Working models on-- different on similar data
- ** Disappointing**:not understand why the results are improving.

## Theoretical framework of Feature Generation

### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#####\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\cccccccccccc \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\#############\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\###############################\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

```mermaid
graph TD
A[Old data] --> B [Feature genetics]
B -> C [OWorking Signs]
C --> D[ML Model]
D -> E [Treaties]

B -> F [Temporary signs]
B -> G[Statistical indicators]
B --> H[Technical indicators]
B -> I [Categoral characteristics]
B -> J [Text indicators]

F --> F1 [Lags]
F --> F2 [Slip windows]
F --> F3 [seasonal indicators]

G --> G1 [distribution periods]
G --> G2 [Identifiers of change]
G --> G3 [Volatility]

H -> H1 [Trend indicators]
H -> H2 [Mementum of indicators]
H -> H3 [Indicators &apos; volatility]

 I --> I1[One-hot encoding]
 I --> I2[Target encoding]
I-> I3 [Hierarchical characteristics]

 J --> J1[TF-IDF]
 J --> J2[Word2Vec]
J --> J3 [Base text indicators]

C -> K [Quality assessment]
K-> L [Colletion]
K -> M [Elevity of the topics]
K-> N[Stability]

L -> O [Selection of topics]
 M --> O
 N --> O

O-> P [Final set of topics]
 P --> D

 style A fill:#ffcdd2
 style C fill:#c8e6c9
 style E fill:#a5d6a7
 style B fill:#e3f2fd
 style K fill:#fff3e0
```

### Mathematical principles

**Feature Engineering as an optimum objective:**

```math
F* = argmax P(Y|X, F(X))
```

Where:

`F*' is the optimal function of the topics
`Y' is the target variable
`X' is the reference data
`F(X)' is the derived characteristics

** Criteria for the quality of the indicators:**

1. **Information**: I(X;Y) = H(Y) - H(Y)X
2. **Stability**: Var(f(X)) < threshold
3. ** Independence**: Cov(f_i(X), f_j(X))
4. ** Capacity**: f(X) . [0.1] or standardized

### Types of characteristics on origin

### ♪ A list of types of topics

```mermaid
graph TD
A[Tips of indicators] -> B [Backgrounds]
A -> C [Productive indicators]
A -> D[Interactive signs]
A -> E [Temporary signs]
A -> F [Categorial characteristics]

B --> B1 [BothWorking Data]
B -> B2 [Required for pre-treatment]
B --> B3 [Can contain noise]

C --> C1 [Mathematical transformation]
C -> C2 [Statistical characteristics]
C -> C3 [Constructed from source]

D -> D1 [Purpose combination]
D -> D2 [Polinominal characteristics]
D --> D3[Logs]

E --> E1 [Continuing from time]
E --> E2 [Lags]
E --> E3 [Slip windows]

F --> F1[Details]
F --> F2 [Required for coding]
F --> F3 [may be hierarchical]

B1 -> G [Quality criteria]
 B2 --> G
 B3 --> G
 C1 --> G
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

G --> H [Informationality]
G -> I [Stability]
G --> J [Independence]
G --> K[Station capacity]

 H --> L[I(X;Y) = H(Y) - H(Y|X)]
 I --> M[Var(f(X)) < threshold]
 J --> N[Cov(f_i(X), f_j(X)) ≈ 0]
K --> O[f(X) ♪ [0.1] or standardized]

 style A fill:#e3f2fd
 style G fill:#c8e6c9
 style L fill:#fff3e0
 style M fill:#fff3e0
 style N fill:#fff3e0
 style O fill:#fff3e0
```

♪##1 ♪ Raw Features ♪

- Non-Working data from the source
- They often require pre-treatment.
- May contain noise and emissions

♪##2. ♪ Derived Features ♪

- Created from the originals
- Mathematical transformation
Statistical characteristics

### 3. Interactive Features

- Combinations of multiple features
- Polynomial signs
- Logs operations

♪##4 ♪ Time signs (Temporal Features)

- Signs depending on time
- Lug signs
- Sliding windows

###5.Categorical Features

- Discrete values
- Coded
- Could be hierarchical.

## Advanced evidence generation techniques

###1. Time signs (Time Series Features)

### ♪ The process of creating time signs

```mermaid
graph TD
A [Temporary series] -> B {Temporary sign type}

B--~\\\\\\C[Legage signs]
B-~ ~ Sliding windows ~ D [slip windows]
B -->\\\Exponential smoothing\E[Exponential smoothing]
B-~ ~ Seasonal ~ F[seasonal signs]

 C --> C1[lag_1, lag_2, lag_3]
 C --> C2[lag_7, lag_14, lag_30]
C --> C3 [Switch on N periods]

D -> D1 [Slipping average]
D --> D2[Slipping std]
D -> D3 [Slipping min/max]
D -> D4 [Slipping median]

 E --> E1[EWM with α=0.1]
 E --> E2[EWM with α=0.3]
 E --> E3[EWM with α=0.5]
 E --> E4[EWM with α=0.7]

F --> F1 [Year, month, day]
F --> F2 [Day of the Week, quarter]
F --> F3 [Cyclical signs]
F --> F4[sin/cos transformation]

C1 -> G [Temporary signs]
 C2 --> G
 C3 --> G
 D1 --> G
 D2 --> G
 D3 --> G
 D4 --> G
 E1 --> G
 E2 --> G
 E3 --> G
 E4 --> G
 F1 --> G
 F2 --> G
 F3 --> G
 F4 --> G

G -> H [Quality assessment]
H -> I [Colletion with target]
H -> J [Stability over time]
H -> K [Informationality]

I-> L [Selection of the best signs]
 J --> L
 K --> L

L -> M [Final time indications]

 style A fill:#e3f2fd
 style G fill:#c8e6c9
 style M fill:#a5d6a7
 style H fill:#fff3e0
```

**Lag Features:**

```python
def create_lag_features(df, target_col, lags=[1, 2, 3, 7, 14, 30], fill_method='forward',
 include_original=False, lag_prefix='lag', config=None):
 """
short lug signs for time series

 Args:
df (pd.dataFrame): Reference dataFrame with time data
Target_col (str): Name of target column for the creation of lags
Lags (List): List Lags for Creation (on default [1, 2, 3, 7, 14, 30])
- 1: Previous period
- 2-3: Short-term lags
- 7: A week's lag
- 14: Two-week lag
- 30: Monthly lag
Fill_method (str): Method of filling in passes ('forward', 'backward', 'interpolate', 'Zero')
- 'forward': Filling in the previous value (ffill)
- 'backward': Fill in the following value (bfill)
- 'interpolate': Linear interpolation
- 'Zero': Filling with zeros
including_original (bool): Do you include the reference column in result
lag_prefix (str): Prefix for Lague Names
config (dict): Additional configration
- max_lag: Maximum lag (on default max(lags))
- min_lag: Minimum lag (on default min(lags))
- lag_step: Step between lags (on default 1)
- Validation: validation of data (True/False)
- memory_officer: Effective use of memory (True/False)

 Returns:
pd.dataFrame: dataFrame with added lagoons

 Raises:
ValueError: If Target_col not exists in dataFrame
ValueError: If lags contain unacceptable values
TypeError: If fill_method not supported
 """
 if config is None:
 config = {
 'max_lag': max(lags) if lags else 1,
 'min_lag': min(lags) if lags else 1,
 'lag_step': 1,
 'validation': True,
 'memory_efficient': False
 }

# Validation of input data
 if config['validation']:
 if target_col not in df.columns:
 raise ValueError(f"Column '{target_col}' not found in dataFrame")

 if not lags or not all(isinstance(lag, int) and lag > 0 for lag in lags):
 raise ValueError("lags must be a List of positive integers")

 if fill_method not in ['forward', 'backward', 'interpolate', 'zero']:
 raise ValueError("fill_method must be one of: 'forward', 'backward', 'interpolate', 'zero'")

# Create copies of dataFrame for security
 result_df = df.copy() if not config['memory_efficient'] else df

# Create lague signs
 for lag in lags:
# Create lago a sign
 lag_col_name = f'{target_col}_{lag_prefix}_{lag}'
 result_df[lag_col_name] = result_df[target_col].shift(lag)

# Filling in dependencies from the method
 if fill_method == 'forward':
 result_df[lag_col_name] = result_df[lag_col_name].fillna(method='ffill')
 elif fill_method == 'backward':
 result_df[lag_col_name] = result_df[lag_col_name].fillna(method='bfill')
 elif fill_method == 'interpolate':
 result_df[lag_col_name] = result_df[lag_col_name].interpolate(method='linear')
 elif fill_method == 'zero':
 result_df[lag_col_name] = result_df[lag_col_name].fillna(0)

# remove reference column if not required
 if not include_original and target_col in result_df.columns:
 result_df = result_df.drop(columns=[target_col])

 return result_df

# example use with detailed parameters
df = create_lag_features(
 df,
 target_col='price',
Lags=[1, 2, 3, 7, 14, 30], #Lags from 1 to 30 days
Fill_method='forward', # Filling in previous value
include_original=True, #Retain the original column
lag_prefix='lag', #Prefix for names
 config={
'max_lag': 30, # Maximum lag
'min_lag': 1, #minimum lag
'Validation': True, #Enact validation
'Memory_officer': False # not save memory
 }
)
```

** Rolling Windows:**

```python
def create_rolling_features(df, target_col, windows=[3, 7, 14, 30],
 statistics=['mean', 'std', 'min', 'max', 'median'],
 min_periods=None, center=False, win_type=None,
 on=None, axis=0, closed=None, config=None):
 """
of sliding windows for time series

 Args:
df (pd.dataFrame): Reference dataFrame with time data
Target_col (str): Name of target column for sliding windows
Windows (List): Window size list (on default [3, 7, 14, 30])
- 3: Short window (3 periods)
- 7: A weekly window (7 periods)
14: Two-week window (14 periods)
- 30: Monthly window (30 periods)
Statistics (List): List Statistician for Calculation
- 'mean': Average
- 'std': Standard deviation
- 'var': Dispersion
- 'min': Minimum value
- 'max': Maximum value
- 'median':
- 'sum': Amount
- 'account': Number of values
- 'Skew': Asymmetry
- 'kurt': Excess
- 'Quantile': Quantile (requires additional parameter q)
min_periods (int): Minimum number of observations in the window
- None: Use window size
- 1: Minimum 1 observation
- Windows//2: Half window size
Center (bool): Centralize window (False for normal, True for centralized)
Win_type (str): Weight window type
- None: Normal window
- 'boxcar': A corner window
- 'triang': Triangle window
Blackman's Window
- 'Hamming':
- 'bartlett': Bartlett's window
on (str): Column for grouping in time
axis (int): Axis for use (0 for lines, 1 for columns)
clossed (str): Which side of the window is turned on ('right', 'left', 'both', 'neither')
config (dict): Additional configration
- Quantiles: List Quantiles for Calculation (on default [0.25, 0.5, 0.75])
- system_functions: User function dictionary
- Fill_method: Method of filling in passes ('forward', 'backward', 'interpolate', 'Zero')
- Validation: validation of data (True/False)
- memory_officer: Effective use of memory (True/False)
- prefix: Prefix for sign names (on default 'rolling')

 Returns:
pd.dataFrame: DataFrame with added sliding windows

 Raises:
ValueError: If Target_col not exists in dataFrame
ValueError: If Windows contain unacceptable values
ValueError: If statistics contain unsupported financials
TypeError: If the parameters have the wrong type
 """
 if config is None:
 config = {
 'quantiles': [0.25, 0.5, 0.75],
 'custom_functions': {},
 'fill_method': 'forward',
 'validation': True,
 'memory_efficient': False,
 'prefix': 'rolling'
 }

# Validation of input data
 if config['validation']:
 if target_col not in df.columns:
 raise ValueError(f"Column '{target_col}' not found in dataFrame")

 if not windows or not all(isinstance(w, int) and w > 0 for w in windows):
 raise ValueError("windows must be a List of positive integers")

 valid_stats = ['mean', 'std', 'var', 'min', 'max', 'median', 'sum', 'count',
 'skew', 'kurt', 'quantile']
 invalid_stats = [s for s in statistics if s not in valid_stats and s not in config['custom_functions']]
 if invalid_stats:
 raise ValueError(f"Invalid statistics: {invalid_stats}. Valid options: {valid_stats}")

# Create copies of dataFrame for security
 result_df = df.copy() if not config['memory_efficient'] else df

♪ the signs of sliding windows ♪
 for window in windows:
# creative object rolling
 rolling_obj = result_df[target_col].rolling(
 window=window,
 min_periods=min_periods or window,
 center=center,
 win_type=win_type,
 on=on,
 axis=axis,
 closed=closed
 )

# Calculation of the Statistician
 for stat in statistics:
 if stat == 'mean':
 col_name = f'{target_col}_{config["prefix"]}_mean_{window}'
 result_df[col_name] = rolling_obj.mean()
 elif stat == 'std':
 col_name = f'{target_col}_{config["prefix"]}_std_{window}'
 result_df[col_name] = rolling_obj.std()
 elif stat == 'var':
 col_name = f'{target_col}_{config["prefix"]}_var_{window}'
 result_df[col_name] = rolling_obj.var()
 elif stat == 'min':
 col_name = f'{target_col}_{config["prefix"]}_min_{window}'
 result_df[col_name] = rolling_obj.min()
 elif stat == 'max':
 col_name = f'{target_col}_{config["prefix"]}_max_{window}'
 result_df[col_name] = rolling_obj.max()
 elif stat == 'median':
 col_name = f'{target_col}_{config["prefix"]}_median_{window}'
 result_df[col_name] = rolling_obj.median()
 elif stat == 'sum':
 col_name = f'{target_col}_{config["prefix"]}_sum_{window}'
 result_df[col_name] = rolling_obj.sum()
 elif stat == 'count':
 col_name = f'{target_col}_{config["prefix"]}_count_{window}'
 result_df[col_name] = rolling_obj.count()
 elif stat == 'skew':
 col_name = f'{target_col}_{config["prefix"]}_skew_{window}'
 result_df[col_name] = rolling_obj.skew()
 elif stat == 'kurt':
 col_name = f'{target_col}_{config["prefix"]}_kurt_{window}'
 result_df[col_name] = rolling_obj.kurt()
 elif stat == 'quantile':
 for q in config['quantiles']:
 col_name = f'{target_col}_{config["prefix"]}_q{int(q*100)}_{window}'
 result_df[col_name] = rolling_obj.quantile(q)

# Use of user functions
 for func_name, func in config['custom_functions'].items():
 col_name = f'{target_col}_{config["prefix"]}_{func_name}_{window}'
 result_df[col_name] = rolling_obj.apply(func)

# Filling out passes
 if config['fill_method'] == 'forward':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='ffill')
 elif config['fill_method'] == 'backward':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='bfill')
 elif config['fill_method'] == 'interpolate':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].interpolate(method='linear')
 elif config['fill_method'] == 'zero':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(0)

 return result_df

# example use with detailed parameters
df = create_rolling_features(
 df,
 target_col='price',
Windows=[3, 7, 14, 30], # Window Dimensions
statistics=['mean', 'std', 'min', 'max', 'median', 'Quantile'], #Statistics
min_periods=1, #minimum 1 observation
Center=False, # Normal Window
Win_type= None, # No weights
 config={
'Quantiles': [0.25, 0.5, 0.75, 0.9, 0.95], #Quantiles
'Constom_functions': { # User functions
 'range': lambda x: x.max() - x.min(),
 'iqr': lambda x: x.quantile(0.75) - x.quantile(0.25)
 },
'fill_method': 'forward', # Filling in the previous value
'Validation': True, #Enact validation
'Memory_officer': False, #not save memory
'Prefix': 'rolling' #Prefix for names
 }
)
```

**Exponential Smoothing:**

```python
def create_ewm_features(df, target_col, alphas=[0.1, 0.3, 0.5, 0.7],
 statistics=['mean'], adjust=True, ignore_na=False,
 bias=False, config=None):
 """
:: Set of indicators of exponential smoothing for time series

 Args:
df (pd.dataFrame): Reference dataFrame with time data
Target_col (str): Name of target column for creating EWM features
aliphas (List): List of smoothing factors (on default [0.1, 0.3, 0.5, 0.7])
- 0.1: Slow smoothing (more weight of history)
- 0.3: Moderate smoothing
- 0.5: Balanced smoothing
-0.7: Rapid smoothing (more weight of current values)
- 0.9: Very quick smoothing
Statistics (List): List Statistician for Calculation
- 'mean': exponentially weighted average
- 'std': Explicitly weighted standard deviation
- 'var': Explicitly weighted dispersion
- 'min': exponentially weighted minimum
- 'max': exponentially weighted maximum
- 'sum': Explicitly weighted amount
- 'account': Exponsively weighted counter
adjust (bool): Use an adjustment for accounting for initial values
- True: Adjustment included (recommended)
- False: Adjustment disabled
ignore_na (bool): Ignore NaN values when calculating
- True: Ignore NaN
- False: Count NaN
bias (bool): Use displaced variance estimate
- True: The displaced estimate
- False: Unchanged estimate (recommended)
config (dict): Additional configration
- span: Alternative alpha (span = 2/alpha - 1)
- halflife: Alpha Alternative (halflife = ln(2)/alpha)
- com: Alpha Alternative (com = 1/alpha - 1)
- Fill_method: Method of filling in passes ('forward', 'backward', 'interpolate', 'Zero')
- Validation: validation of data (True/False)
- memory_officer: Effective use of memory (True/False)
- prefix: Prefix for topics (on default 'ewm')
- system_functions: User function dictionary

 Returns:
pd.dataFrame: DataFrame with added exponential smoothings

 Raises:
ValueError: If Target_col not exists in dataFrame
ValueError: If Alphas contains unacceptable values
ValueError: If statistics contain unsupported financials
TypeError: If the parameters have the wrong type
 """
 if config is None:
 config = {
 'span': None,
 'halflife': None,
 'com': None,
 'fill_method': 'forward',
 'validation': True,
 'memory_efficient': False,
 'prefix': 'ewm',
 'custom_functions': {}
 }

# Validation of input data
 if config['validation']:
 if target_col not in df.columns:
 raise ValueError(f"Column '{target_col}' not found in dataFrame")

 if not alphas or not all(isinstance(a, (int, float)) and 0 < a <= 1 for a in alphas):
 raise ValueError("alphas must be a List of numbers between 0 and 1")

 valid_stats = ['mean', 'std', 'var', 'min', 'max', 'sum', 'count']
 invalid_stats = [s for s in statistics if s not in valid_stats and s not in config['custom_functions']]
 if invalid_stats:
 raise ValueError(f"Invalid statistics: {invalid_stats}. Valid options: {valid_stats}")

# Create copies of dataFrame for security
 result_df = df.copy() if not config['memory_efficient'] else df

# the evidence of exponential smoothing
 for alpha in alphas:
# of the EWM object
 ewm_obj = result_df[target_col].ewm(
 alpha=alpha,
 adjust=adjust,
 ignore_na=ignore_na,
 bias=bias,
 span=config['span'],
 halflife=config['halflife'],
 com=config['com']
 )

# Calculation of the Statistician
 for stat in statistics:
 if stat == 'mean':
 col_name = f'{target_col}_{config["prefix"]}_mean_{alpha}'
 result_df[col_name] = ewm_obj.mean()
 elif stat == 'std':
 col_name = f'{target_col}_{config["prefix"]}_std_{alpha}'
 result_df[col_name] = ewm_obj.std()
 elif stat == 'var':
 col_name = f'{target_col}_{config["prefix"]}_var_{alpha}'
 result_df[col_name] = ewm_obj.var()
 elif stat == 'min':
 col_name = f'{target_col}_{config["prefix"]}_min_{alpha}'
 result_df[col_name] = ewm_obj.min()
 elif stat == 'max':
 col_name = f'{target_col}_{config["prefix"]}_max_{alpha}'
 result_df[col_name] = ewm_obj.max()
 elif stat == 'sum':
 col_name = f'{target_col}_{config["prefix"]}_sum_{alpha}'
 result_df[col_name] = ewm_obj.sum()
 elif stat == 'count':
 col_name = f'{target_col}_{config["prefix"]}_count_{alpha}'
 result_df[col_name] = ewm_obj.count()

# Use of user functions
 for func_name, func in config['custom_functions'].items():
 col_name = f'{target_col}_{config["prefix"]}_{func_name}_{alpha}'
 result_df[col_name] = ewm_obj.apply(func)

# Filling out passes
 if config['fill_method'] == 'forward':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='ffill')
 elif config['fill_method'] == 'backward':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='bfill')
 elif config['fill_method'] == 'interpolate':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].interpolate(method='linear')
 elif config['fill_method'] == 'zero':
 for col in result_df.columns:
 if col.startswith(f'{target_col}_{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(0)

 return result_df

# example use with detailed parameters
df = create_ewm_features(
 df,
 target_col='price',
Alphas=[0.1, 0.3, 0.5, 0.7], # Coefficients of smoothing
Statistics=['mean', 'std', 'var'], #Statistics
adjust=True, # Adjustment enabled
ignore_na=False, #To account for NaN
Bias=False, #The Unchanged Evaluation
 config={
'span': None, #not use span
'halflife': None, #not use halflife
'com': None, #not use com
'fill_method': 'forward', # Filling in the previous value
'Validation': True, #Enact validation
'Memory_officer': False, #not save memory
'prefix': 'ewm', #Prefix for names
'Constom_functions': { # User functions
 'trend': lambda x: x.iloc[-1] - x.iloc[0] if len(x) > 1 else 0,
 'volatility': lambda x: x.std() if len(x) > 1 else 0
 }
 }
)
```

** Seasonal Features: **

```python
def create_seasonal_features(df, date_col, features=['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter'],
 cyclic_features=True, timezone=None, business_hours=False,
 holidays=None, config=None):
 """
seasonality from time data

 Args:
df (pd.dataFrame): Reference dataFrame with time data
Data_col (str): Name of column with date/time
Features (List): List of seasonal features for creation
- 'year': Year (2020, 2021, 2022, ...)
- 'month': Month (1-12)
- 'day': Day of the month (1-31)
- 'dayofweek': Day of the Week (0=Monday, 6=Sunday)
- 'dayofyear': Day of the Year (1-366)
- 'week': Week of the Year (1-53)
- 'Quarter': Quarter (1-4)
- 'hour': Hour of day (0-23)
- 'minute': minutesa (0-59)
- 'second': seconds (0-59)
- 'is_weekend': Day off (True/False)
- 'is_month_start': The beginning of the month (True/False)
- 'is_month_end': End of month (True/False)
- 'is_Quarter_start': Start of the quarter (True/False)
- 'is_Quarter_end': End of block (True/False)
- 'is_year_start': Start of the year (True/False)
- 'is_year_end': End of the year (True/False)
cyclic_features (boool): Do you create cyclic signs (sin/cos)
- True: Create cyclical signs for periodic data
- False: Create only normal features
Timezone (str): Time belt for conversion (e.g. 'UTC', 'Europe/Moscow')
business_hours (bool): Do you create work-hour signs?
- True: Create signs of working hours (9-17 Monday-Friday)
- False: nnot create signs of working hours
holidays (List): List of holiday days for the creation of signs
- None:not to take into account holidays
== sync, corrected by elderman == @elder_man
config (dict): Additional configration
- cyclic_periods: Periods for cyclical signs
- 'month': 12 months
- 'dayofweek': 7 days
- 'hour': 24 hours
- 'dayofyear': 365 (days of year)
- business_hours_start: Start hours (on default 9)
- business_hours_end: End of working hours (on default 17)
- business_days: working days (on default [0.1,2,3.4] - Mon-Fri)
- Fill_method: Method of filling in passes ('forward', 'backward', 'interpolate', 'Zero')
- Validation: validation of data (True/False)
- memory_officer: Effective use of memory (True/False)
- prefix: Prefix for topics (on default 'seasonal')

 Returns:
pd.dataFrame: DataFrame with added seasonal signature

 Raises:
ValueError: If data_col not exists in dataFrame
ValueError: If Data_col not is datame
ValueError: If the features contain unsupported features
TypeError: If the parameters have the wrong type
 """
 if config is None:
 config = {
 'cyclic_periods': {
 'month': 12,
 'dayofweek': 7,
 'hour': 24,
 'dayofyear': 365
 },
 'business_hours_start': 9,
 'business_hours_end': 17,
'business_days': [0, 1, 2, 3, 4], # Mon–Fri
 'fill_method': 'forward',
 'validation': True,
 'memory_efficient': False,
 'prefix': 'seasonal'
 }

# Validation of input data
 if config['validation']:
 if date_col not in df.columns:
 raise ValueError(f"Column '{date_col}' not found in dataFrame")

 if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
 raise ValueError(f"Column '{date_col}' must be datetime type")

 valid_features = ['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter',
 'hour', 'minute', 'second', 'is_weekend', 'is_month_start', 'is_month_end',
 'is_quarter_start', 'is_quarter_end', 'is_year_start', 'is_year_end']
 invalid_features = [f for f in features if f not in valid_features]
 if invalid_features:
 raise ValueError(f"Invalid features: {invalid_features}. Valid options: {valid_features}")

# Create copies of dataFrame for security
 result_df = df.copy() if not config['memory_efficient'] else df

# Convergence in datam if necessary
 if not pd.api.types.is_datetime64_any_dtype(result_df[date_col]):
 result_df[date_col] = pd.to_datetime(result_df[date_col])

# Convergence of the time zone
 if timezone:
 result_df[date_col] = result_df[date_col].dt.tz_convert(timezone)

# Create of seasonal signs
 for feature in features:
 if feature == 'year':
 col_name = f'{config["prefix"]}_year'
 result_df[col_name] = result_df[date_col].dt.year
 elif feature == 'month':
 col_name = f'{config["prefix"]}_month'
 result_df[col_name] = result_df[date_col].dt.month
 elif feature == 'day':
 col_name = f'{config["prefix"]}_day'
 result_df[col_name] = result_df[date_col].dt.day
 elif feature == 'dayofweek':
 col_name = f'{config["prefix"]}_dayofweek'
 result_df[col_name] = result_df[date_col].dt.dayofweek
 elif feature == 'dayofyear':
 col_name = f'{config["prefix"]}_dayofyear'
 result_df[col_name] = result_df[date_col].dt.dayofyear
 elif feature == 'week':
 col_name = f'{config["prefix"]}_week'
 result_df[col_name] = result_df[date_col].dt.isocalendar().week
 elif feature == 'quarter':
 col_name = f'{config["prefix"]}_quarter'
 result_df[col_name] = result_df[date_col].dt.quarter
 elif feature == 'hour':
 col_name = f'{config["prefix"]}_hour'
 result_df[col_name] = result_df[date_col].dt.hour
 elif feature == 'minute':
 col_name = f'{config["prefix"]}_minute'
 result_df[col_name] = result_df[date_col].dt.minute
 elif feature == 'second':
 col_name = f'{config["prefix"]}_second'
 result_df[col_name] = result_df[date_col].dt.second
 elif feature == 'is_weekend':
 col_name = f'{config["prefix"]}_is_weekend'
 result_df[col_name] = result_df[date_col].dt.dayofweek.isin([5, 6])
 elif feature == 'is_month_start':
 col_name = f'{config["prefix"]}_is_month_start'
 result_df[col_name] = result_df[date_col].dt.is_month_start
 elif feature == 'is_month_end':
 col_name = f'{config["prefix"]}_is_month_end'
 result_df[col_name] = result_df[date_col].dt.is_month_end
 elif feature == 'is_quarter_start':
 col_name = f'{config["prefix"]}_is_quarter_start'
 result_df[col_name] = result_df[date_col].dt.is_quarter_start
 elif feature == 'is_quarter_end':
 col_name = f'{config["prefix"]}_is_quarter_end'
 result_df[col_name] = result_df[date_col].dt.is_quarter_end
 elif feature == 'is_year_start':
 col_name = f'{config["prefix"]}_is_year_start'
 result_df[col_name] = result_df[date_col].dt.is_year_start
 elif feature == 'is_year_end':
 col_name = f'{config["prefix"]}_is_year_end'
 result_df[col_name] = result_df[date_col].dt.is_year_end

# of the cycle signs
 if cyclic_features:
 for feature in features:
 if feature == 'month' and feature in features:
 period = config['cyclic_periods']['month']
 result_df[f'{config["prefix"]}_month_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_month'] / period)
 result_df[f'{config["prefix"]}_month_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_month'] / period)
 elif feature == 'dayofweek' and feature in features:
 period = config['cyclic_periods']['dayofweek']
 result_df[f'{config["prefix"]}_dayofweek_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_dayofweek'] / period)
 result_df[f'{config["prefix"]}_dayofweek_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_dayofweek'] / period)
 elif feature == 'hour' and feature in features:
 period = config['cyclic_periods']['hour']
 result_df[f'{config["prefix"]}_hour_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_hour'] / period)
 result_df[f'{config["prefix"]}_hour_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_hour'] / period)
 elif feature == 'dayofyear' and feature in features:
 period = config['cyclic_periods']['dayofyear']
 result_df[f'{config["prefix"]}_dayofyear_sin'] = np.sin(2 * np.pi * result_df[f'{config["prefix"]}_dayofyear'] / period)
 result_df[f'{config["prefix"]}_dayofyear_cos'] = np.cos(2 * np.pi * result_df[f'{config["prefix"]}_dayofyear'] / period)

# the watches are high
 if business_hours:
 result_df[f'{config["prefix"]}_is_business_hour'] = (
 (result_df[date_col].dt.hour >= config['business_hours_start']) &
 (result_df[date_col].dt.hour < config['business_hours_end']) &
 (result_df[date_col].dt.dayofweek.isin(config['business_days']))
 )
 result_df[f'{config["prefix"]}_is_business_day'] = result_df[date_col].dt.dayofweek.isin(config['business_days'])

# the sign of the holidays
 if holidays:
 result_df[f'{config["prefix"]}_is_holiday'] = result_df[date_col].dt.date.isin([pd.to_datetime(h).date() for h in holidays])

# Filling out passes
 if config['fill_method'] == 'forward':
 for col in result_df.columns:
 if col.startswith(f'{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='ffill')
 elif config['fill_method'] == 'backward':
 for col in result_df.columns:
 if col.startswith(f'{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(method='bfill')
 elif config['fill_method'] == 'interpolate':
 for col in result_df.columns:
 if col.startswith(f'{config["prefix"]}_'):
 result_df[col] = result_df[col].interpolate(method='linear')
 elif config['fill_method'] == 'zero':
 for col in result_df.columns:
 if col.startswith(f'{config["prefix"]}_'):
 result_df[col] = result_df[col].fillna(0)

 return result_df

# example use with detailed parameters
df = create_seasonal_features(
 df,
 date_col='date',
 features=['year', 'month', 'day', 'dayofweek', 'dayofyear', 'week', 'quarter', 'hour', 'is_weekend'],
Cyclic_features=True, # Create Cyclic Signs
Timezone='UTC', # UTC Hour Belt
business_hours=True, # Create signs of working hours
holidays=['2023-01-01', '2023-12-25'], #Festivities
 config={
'cyclic_periods': { # Periods for cyclical signs
 'month': 12,
 'dayofweek': 7,
 'hour': 24,
 'dayofyear': 365
 },
'business_hours_start': 9, # Office hours start
'business_hours_end': 17, # End of working hours
'business_days': [0, 1, 2, 3, 4], #Workdays (Mon-Fri)
'fill_method': 'forward', # Filling in the previous value
'Validation': True, #Enact validation
'Memory_officer': False, #not save memory
'Prefix': 'seasonal' #Prefix for names
 }
)
```

♪##2: Statistical Features

### \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ #####\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\###########\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

```mermaid
graph TD
A[Reference data] -> B {Statistical topics type}

B-------------------------------------------------------------------------------------------
B -->: Signs of change ~ D [Identifies of change]
B-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

C --> C1 [Med, std, var]
 C --> C2[Skewness, Kurtosis]
C --> C3 [Quantiles: q25, q50, q75, q90, q95, q99]

D -> D1 [Absolute modification]
D -> D2 [Logarithmic change]
D -> D3 [Difference of values]
D -> D4 [per cent change]

E --> E1 [Realized volatility]
E --> E2 [GARCH volatility]
E --> E3 [Maximum volatility]
E --> E4 [Vulnerability on windows]

C1 -> F [Statistical indicators]
 C2 --> F
 C3 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 D4 --> F
 E1 --> F
 E2 --> F
 E3 --> F
 E4 --> F

F --> G [Tank window]
G --> G1[7 days]
G --> G2[14 days]
G --> G3[30 days]
G --> G4[90 days]

G1-> H[Slipping Statistics]
 G2 --> H
 G3 --> H
 G4 --> H

H -> I [Quality assessment]
I -> J [Colletion with target]
I -> K [Stable distribution]
I -> L [Informationality]

J -> M [Selection of topics]
 K --> M
 L --> M

M -> N [Final statistical indicators]

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style N fill:#a5d6a7
 style I fill:#fff3e0
```

** Allocation points:**

```python
def create_moment_features(df, target_col, windows=[7, 14, 30]):
""create of distribution points""
 for window in windows:
 rolling = df[target_col].rolling(window)

# First moments
 df[f'{target_col}_mean_{window}'] = rolling.mean()
 df[f'{target_col}_std_{window}'] = rolling.std()
 df[f'{target_col}_var_{window}'] = rolling.var()

# The highest points
 df[f'{target_col}_skew_{window}'] = rolling.skew()
 df[f'{target_col}_kurt_{window}'] = rolling.kurt()

# Quantile
 df[f'{target_col}_q25_{window}'] = rolling.quantile(0.25)
 df[f'{target_col}_q50_{window}'] = rolling.quantile(0.50)
 df[f'{target_col}_q75_{window}'] = rolling.quantile(0.75)
 df[f'{target_col}_q90_{window}'] = rolling.quantile(0.90)
 df[f'{target_col}_q95_{window}'] = rolling.quantile(0.95)
 df[f'{target_col}_q99_{window}'] = rolling.quantile(0.99)

 return df

# Example of use
df = create_moment_features(df, 'price', windows=[7, 14, 30])
```

**Change Features signs:**

```python
def create_change_features(df, target_col, periods=[1, 2, 3, 7, 14, 30]):
""create signs of change."
 for period in periods:
# Absolute change
 df[f'{target_col}_change_{period}'] = df[target_col].pct_change(period)
# Logarithmic change
 df[f'{target_col}_log_change_{period}'] = np.log(df[target_col] / df[target_col].shift(period))
# The difference
 df[f'{target_col}_diff_{period}'] = df[target_col].diff(period)

 return df

# Example of use
df = create_change_features(df, 'price', periods=[1, 2, 3, 7, 14, 30])
```

** Signs of Volatility Features:**

```python
def create_volatility_features(df, target_col, windows=[7, 14, 30]):
""create signs of volatility."
 for window in windows:
# Realized volatility
 returns = df[target_col].pct_change()
 df[f'{target_col}_vol_{window}'] = returns.rolling(window).std() * np.sqrt(252)

# GarCH volatility (simplified)
 df[f'{target_col}_garch_vol_{window}'] = returns.rolling(window).std() * np.sqrt(252) * 1.2

# Maximum volatility
 df[f'{target_col}_max_vol_{window}'] = returns.rolling(window).std().rolling(window).max()

 return df

# Example of use
df = create_volatility_features(df, 'price', windows=[7, 14, 30])
```

♪## 3. Technical Indicators

### ♪ Technical indicators and their classification

```mermaid
graph TD
A[Tank data] --> B{Technical indicators type}

B -->\\\\\C[Trend indicators]
B-----~------------------------------------------------
B-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

 C --> C1[SMA - Simple Moving Average]
 C --> C2[EMA - Exponential Moving Average]
 C --> C3[WMA - Weighted Moving Average]
C --> C4[Trend = price difference and SMA]

 D --> D1[RSI - Relative Strength index]
 D --> D2[Stochastic Oscillator]
 D --> D3[Williams %R]
 D --> D4[ROC - Rate of Change]

 E --> E1[Bollinger Bands]
 E --> E2[ATR - Average True Range]
E --> E3 [Volatility on windows]
 E --> E4[Position in Bollinger Bands]

C1 --> F[Technical indicators]
 C2 --> F
 C3 --> F
 C4 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 D4 --> F
 E1 --> F
 E2 --> F
 E3 --> F
 E4 --> F

F --> G [Tank window]
 G --> G1[7 periods]
 G --> G2[14 periods]
 G --> G3[30 periods]
 G --> G4[50 periods]
 G --> G5[200 periods]

G1-> H[Slip indicators]
 G2 --> H
 G3 --> H
 G4 --> H
 G5 --> H

H -> I [Normalization]
I -> J [Massing 0-1]
I -> K[Z-score normalization]
I-> L[Min-Max normalization]

J -> M [Final indicators]
 K --> M
 L --> M

M --> N [Quality assessment]
N --> O [Collection with yield]
N --> P[Sensibility of signals]
N --> Q [Informationality]

O-> R [Selection of best indicators]
 P --> R
 Q --> R

R --> S [Final set of indicators]

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style S fill:#a5d6a7
 style N fill:#fff3e0
```

**Trend indicators:**

```python
def create_trend_features(df, target_col, windows=[7, 14, 30, 50, 200]):
""create trend indicators""
 for window in windows:
# A simple sliding average
 df[f'{target_col}_sma_{window}'] = df[target_col].rolling(window).mean()

# An exponential moving average
 df[f'{target_col}_ema_{window}'] = df[target_col].ewm(span=window).mean()

# Weighted moving average
 weights = np.arange(1, window + 1)
 df[f'{target_col}_wma_{window}'] = df[target_col].rolling(window).apply(
 lambda x: np.average(x, weights=weights), raw=True
 )

# Tread (the difference between price and SMA)
 df[f'{target_col}_trend_{window}'] = df[target_col] - df[f'{target_col}_sma_{window}']

 return df

# Example of use
df = create_trend_features(df, 'price', windows=[7, 14, 30, 50, 200])
```

** Timeline for indicators:**

```python
def create_momentum_features(df, target_col, windows=[7, 14, 30]):
""create moment indicators""
 for window in windows:
 # RSI (Relative Strength index)
 delta = df[target_col].diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
 rs = gain / loss
 df[f'{target_col}_rsi_{window}'] = 100 - (100 / (1 + rs))

 # Stochastic Oscillator
 low_min = df[target_col].rolling(window).min()
 high_max = df[target_col].rolling(window).max()
 df[f'{target_col}_stoch_{window}'] = 100 * (df[target_col] - low_min) / (high_max - low_min)

 # Williams %R
 df[f'{target_col}_williams_r_{window}'] = -100 * (high_max - df[target_col]) / (high_max - low_min)

 # Rate of Change
 df[f'{target_col}_roc_{window}'] = df[target_col].pct_change(window) * 100

 return df

# Example of use
df = create_momentum_features(df, 'price', windows=[7, 14, 30])
```

** Indicator volatility:**

```python
def create_volatility_indicators(df, target_col, windows=[7, 14, 30]):
""create volatility indicators""
 for window in windows:
 # Bollinger Bands
 sma = df[target_col].rolling(window).mean()
 std = df[target_col].rolling(window).std()
 df[f'{target_col}_bb_upper_{window}'] = sma + (std * 2)
 df[f'{target_col}_bb_lower_{window}'] = sma - (std * 2)
 df[f'{target_col}_bb_width_{window}'] = df[f'{target_col}_bb_upper_{window}'] - df[f'{target_col}_bb_lower_{window}']
 df[f'{target_col}_bb_position_{window}'] = (df[target_col] - df[f'{target_col}_bb_lower_{window}']) / df[f'{target_col}_bb_width_{window}']

 # Average True Range (ATR)
 high_low = df['high'] - df['low']
 high_close = np.abs(df['high'] - df[target_col].shift())
 low_close = np.abs(df['low'] - df[target_col].shift())
 true_range = np.maximum(high_low, np.maximum(high_close, low_close))
 df[f'{target_col}_atr_{window}'] = true_range.rolling(window).mean()

 return df

# Example of use
df = create_volatility_indicators(df, 'price', windows=[7, 14, 30])
```

♪##4 ♪ Categorical Features ♪

** Coding of the categorical signs:**

```python
def create_categorical_features(df, categorical_cols):
""create categorical signs."
 for col in categorical_cols:
 # One-hot encoding
 dummies = pd.get_dummies(df[col], prefix=col)
 df = pd.concat([df, dummies], axis=1)

 # Label encoding
 df[f'{col}_label'] = df[col].astype('category').cat.codes

# Target encoding
 target_mean = df.groupby(col)['target'].mean()
 df[f'{col}_target_encoded'] = df[col].map(target_mean)

 # Frequency encoding
 freq = df[col].value_counts()
 df[f'{col}_freq'] = df[col].map(freq)

 return df

# Example of use
df = create_categorical_features(df, ['category', 'region', 'type'])
```

**Herarchical characteristics:**

```python
def create_hierarchical_features(df, hierarchical_cols):
""create hierarchical features."
 for col in hierarchical_cols:
# Level of hierarchy
 df[f'{col}_level_1'] = df[col].str.split('.').str[0]
 df[f'{col}_level_2'] = df[col].str.split('.').str[1]
 df[f'{col}_level_3'] = df[col].str.split('.').str[2]

# The depth of the hierarchy
 df[f'{col}_depth'] = df[col].str.count('.') + 1

# Parental characteristics
 df[f'{col}_parent'] = df[col].str.rsplit('.', 1).str[0]

 return df

# Example of use
df = create_hierarchical_features(df, ['category_path', 'region_path'])
```

♪##5 ♪ Text Features ♪

** Basic textual features:**

```python
def create_text_features(df, text_col):
""create of basic textual features."
# Length of the text
 df[f'{text_col}_length'] = df[text_col].str.len()

# Number of words
 df[f'{text_col}_word_count'] = df[text_col].str.split().str.len()

# Number of proposals
 df[f'{text_col}_sentence_count'] = df[text_col].str.count(r'[.!?]+')

# Number of capital letters
 df[f'{text_col}_upper_count'] = df[text_col].str.count(r'[A-Z]')

# Number of figures
 df[f'{text_col}_digit_count'] = df[text_col].str.count(r'\d')

# Number of puncture signs
 df[f'{text_col}_punct_count'] = df[text_col].str.count(r'[^\w\s]')

# Number of unique words
 df[f'{text_col}_unique_words'] = df[text_col].str.split().apply(lambda x: len(set(x)))

# Average length of word
 df[f'{text_col}_avg_word_length'] = df[text_col].str.split().str.len().mean()

 return df

# Example of use
df = create_text_features(df, 'describe')
```

**TF-IDF indicators:**

```python
def create_tfidf_features(df, text_col, max_features=1000):
""create TF-IDF features""
 from sklearn.feature_extraction.text import TfidfVectorizer

# TF-IDF vector model
 tfidf = TfidfVectorizer(
 max_features=max_features,
 stop_words='english',
 ngram_range=(1, 2),
 min_df=2,
 max_df=0.95
 )

# Learning and transformation
 tfidf_matrix = tfidf.fit_transform(df[text_col].fillna(''))

# Create dataFrame with TF-IDF signature
 tfidf_df = pd.dataFrame(
 tfidf_matrix.toarray(),
 columns=[f'tfidf_{i}' for i in range(tfidf_matrix.shape[1])]
 )

# Association with original dataFrame
 df = pd.concat([df, tfidf_df], axis=1)

 return df

# Example of use
df = create_tfidf_features(df, 'describe', max_features=1000)
```

**Word2Vec signs:**

```python
def create_word2vec_features(df, text_col, vector_size=100):
""create Word2Vec signs""
 from gensim.models import Word2Vec

# Preparation of text
 sentences = df[text_col].fillna('').str.split().toList()

# Word2Vec model learning
 model = Word2Vec(
 sentences,
 vector_size=vector_size,
 window=5,
 min_count=2,
 workers=4
 )

# a list of features for each document
 def get_document_vector(words):
 vectors = []
 for word in words:
 if word in model.wv:
 vectors.append(model.wv[word])
 if vectors:
 return np.mean(vectors, axis=0)
 else:
 return np.zeros(vector_size)

# Application to each document
 doc_vectors = df[text_col].fillna('').str.split().apply(get_document_vector)

# Create dataFrame with Word2Vec
 w2v_df = pd.dataFrame(
 doc_vectors.toList(),
 columns=[f'w2v_{i}' for i in range(vector_size)]
 )

# Association with original dataFrame
 df = pd.concat([df, w2v_df], axis=1)

 return df

# Example of use
df = create_word2vec_features(df, 'describe', vector_size=100)
```

## Automatic signs generation

### ♪ Automatic signs generation

```mermaid
graph TD
A[Reference data] -> B {automatic generation method}

B-------------------------------------------------------------------------------
B--~ ~ Polynomial signs ~ D [Polynomial signs]
B -->\\\ Interactive signs\E[Interactive signs]

C --> C1 [create population]
C --> C2 [Moutations and crossovers]
C --> C3 [Phytnes assessment]
C --> C4 [Best Selection]

D -> D1 [Polinoma steppe]
D -> D2 [Experiences of topics]
D --> D3 [create combinations]
D -> D4 [Selection of significant]

E --> E1[Binary interactions]
E --> E2 [Try interactions]
E --> E3 [Mathematic operations]
E --> E4[Logs]

C1-> F[Automatically generated characteristics]
 C2 --> F
 C3 --> F
 C4 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 D4 --> F
 E1 --> F
 E2 --> F
 E3 --> F
 E4 --> F

F --> G [Quality assessment]
G --> H [Colletion with target]
G -> I [The importance of the topics]
G --> J [Stability]
G --> K [Multicollinaryity]

H -> L [Selection of topics]
 I --> L
 J --> L
 K --> L

L -> M [Final set of indicators]

M --> N [Applicable in AutoML Gluon]
N -> O [model training]
O -> P [Evaluation of performance]
P -> Q [Optimization of topics]

Q --> R{improve result?}
R -->\\\\S[Use the signs]
R--~ ~ No~ T[Reversing strategy]
 T --> B

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style M fill:#a5d6a7
 style S fill:#4caf50
 style T fill:#ff9800
```

*## 1. Genetic programming

```python
def genetic_feature_generation(df, target_col, generations=50, population_size=100):
"Genetic programming for the generation of signs."
 import random
 from deap import base, creator, tools, algorithms

# Definition of functions
 def add(x, y): return x + y
 def sub(x, y): return x - y
 def mul(x, y): return x * y
 def div(x, y): return x / (y + 1e-8)
 def sqrt(x): return np.sqrt(np.abs(x))
 def log(x): return np.log(np.abs(x) + 1e-8)
 def exp(x): return np.exp(np.clip(x, -10, 10))

# the core set of functions
 pset = base.PrimitiveSet("main", 2)
 pset.addPrimitive(add, 2)
 pset.addPrimitive(sub, 2)
 pset.addPrimitive(mul, 2)
 pset.addPrimitive(div, 2)
 pset.addPrimitive(sqrt, 1)
 pset.addPrimitive(log, 1)
 pset.addPrimitive(exp, 1)

# Classrooms
 creator.create("FitnessMax", base.Fitness, weights=(1.0,))
 creator.create("Individual", List, fitness=creator.FitnessMax)

# creative tools
 toolbox = base.Toolbox()
 toolbox.register("expr", tools.genHalfAndHalf, pset=pset, min_=1, max_=3)
 toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
 toolbox.register("population", tools.initRepeat, List, toolbox.individual)

# function evaluation
 def evaluate(individual):
 try:
# Compilation of wood
 tree = pset.compile(expr=individual)

# Application to data
 feature = tree(df.iloc[:, 0], df.iloc[:, 1])

# Check on valitude
 if np.isnan(feature).any() or np.isinf(feature).any():
 return (0,)

# Correlation with target variable
 correlation = np.corrcoef(feature, df[target_col])[0, 1]

 return (abs(correlation),)
 except:
 return (0,)

 toolbox.register("evaluate", evaluate)
 toolbox.register("mate", tools.cxOnePoint)
 toolbox.register("mutate", tools.mutUniform, expr=toolbox.expr, pset=pset)
 toolbox.register("select", tools.selTournament, tournsize=3)

# population
 population = toolbox.population(n=population_size)

# Evolution
 for gen in range(generations):
# Evaluation
 fitnesses = List(map(toolbox.evaluate, population))
 for ind, fit in zip(population, fitnesses):
 ind.fitness.values = fit

# Selection
 offspring = toolbox.select(population, len(population))
 offspring = List(map(toolbox.clone, offspring))

# Crossover
 for child1, child2 in zip(offspring[::2], offspring[1::2]):
 if random.random() < 0.5:
 toolbox.mate(child1, child2)
 del child1.fitness.values
 del child2.fitness.values

# Mutation
 for mutant in offspring:
 if random.random() < 0.2:
 toolbox.mutate(mutant)
 del mutant.fitness.values

# Population replacement
 population[:] = offspring

 return population

# Example of use
population = genetic_feature_generation(df, 'target', generations=50, population_size=100)
```

###2: Automatic creation of polynomial features

```python
def create_polynomial_features(df, feature_cols, degree=2, interaction_only=False):
""create polynomial signs."
 from sklearn.preprocessing import PolynomialFeatures

# Selection of signs
 X = df[feature_cols].fillna(0)

# of the polynomial signs
 poly = PolynomialFeatures(
 degree=degree,
 interaction_only=interaction_only,
 include_bias=False
 )

# Conversion
 X_poly = poly.fit_transform(X)

# the name of the sign
 feature_names = poly.get_feature_names_out(feature_cols)

 # create dataFrame
 poly_df = pd.dataFrame(X_poly, columns=feature_names, index=df.index)

# Association with original dataFrame
 df = pd.concat([df, poly_df], axis=1)

 return df

# Example of use
df = create_polynomial_features(df, ['feature1', 'feature2', 'feature3'], degree=2)
```

###3: Automatic creation of interactive features

```python
def create_interaction_features(df, feature_cols, max_interactions=10):
""create interactive features."
 from itertools import combinations

# creative all possible combinations
 interactions = []
 for r in range(2, min(len(feature_cols) + 1, max_interactions + 1)):
 interactions.extend(combinations(feature_cols, r))

# of interactive features
 for interaction in interactions:
 if len(interaction) == 2:
# Binary interactions
 col1, col2 = interaction
 df[f'{col1}_x_{col2}'] = df[col1] * df[col2]
 df[f'{col1}_div_{col2}'] = df[col1] / (df[col2] + 1e-8)
 df[f'{col1}_plus_{col2}'] = df[col1] + df[col2]
 df[f'{col1}_minus_{col2}'] = df[col1] - df[col2]
 elif len(interaction) == 3:
# Three relationships
 col1, col2, col3 = interaction
 df[f'{col1}_x_{col2}_x_{col3}'] = df[col1] * df[col2] * df[col3]
 df[f'{col1}_x_{col2}_div_{col3}'] = (df[col1] * df[col2]) / (df[col3] + 1e-8)

 return df

# Example of use
df = create_interaction_features(df, ['feature1', 'feature2', 'feature3'], max_interactions=5)
```

## The quality of the signs

### ~ metrics quality assessment of signs

```mermaid
graph TD
A[Greats] -> B {Quality assessment type}

B-------------------------------------------------------------------------------------------------
B--~~ML tests ~ D[ML tests]
B--~ ♪ Stability ♪ E [Stables]

C --> C1 [Colletion with target]
C --> C2 [Multicollinaryity]
C -> C3 [Distribution of topics]
C --> C4 [Emissions and anomalies]

D -> D1 [The importance of the signs]
 D --> D2[Feature Selection]
 D --> D3[Cross-validation]
 D --> D4[Permutation importance]

E --> E1 [Temporary stability]
E --> E2 [Distributional stability]
E --> E3 [Coordination stability]
E --> E4 [Drift of topics]

C1 -> F [Quality assessment]
 C2 --> F
 C3 --> F
 C4 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 D4 --> F
 E1 --> F
 E2 --> F
 E3 --> F
 E4 --> F

F --> G [Criteria of selection]
G -> H [High correlation > 0.1]
G -> I [Low multicollinearity < 0.8]
G --> J [Stability > 0.7]
G --> K [Axis > 0.01]

H -> L [Selection of topics]
 I --> L
 J --> L
 K --> L

L -> M [Final set of indicators]

M --> N[validation on test data]
N --> O[check performance]
O-> P[Monitoring in sales]

P --> Q {Quality acceptable?}
Q -->\\\\R[Identifiers ready for use]
Q --\\\\\\S[Revision and improve]
 S --> A

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style M fill:#a5d6a7
 style R fill:#4caf50
 style S fill:#ff9800
```

♪##1 ♪ Statistical tests

**Text of correlation:**

```python
def evaluate_correlation_features(df, target_col, threshold=0.1):
""""""""""""""""""
 correlations = df.corr()[target_col].abs().sort_values(ascending=False)

# Signs with high correlation
 high_corr = correlations[correlations > threshold]

# Signs with low correlation
 low_corr = correlations[correlations <= threshold]

 return {
 'high_correlation': high_corr,
 'low_correlation': low_corr,
 'correlation_stats': {
 'mean': correlations.mean(),
 'std': correlations.std(),
 'min': correlations.min(),
 'max': correlations.max()
 }
 }

# Example of use
correlation_results = evaluate_correlation_features(df, 'target', threshold=0.1)
```

** Multicollinearity test:**

```python
def evaluate_multicollinearity(df, threshold=0.8):
"Authorization of Multicollinearity."
 from sklearn.feature_selection import VarianceThreshold

# Calculation of correlation matrix
 corr_matrix = df.corr().abs()

# Searching for highly corroded steam
 high_corr_pairs = []
 for i in range(len(corr_matrix.columns)):
 for j in range(i+1, len(corr_matrix.columns)):
 if corr_matrix.iloc[i, j] > threshold:
 high_corr_pairs.append((
 corr_matrix.columns[i],
 corr_matrix.columns[j],
 corr_matrix.iloc[i, j]
 ))

# Remove signs with low dispersion
 selector = VarianceThreshold(threshold=0.01)
 X = df.select_dtypes(include=[np.number])
 X_selected = selector.fit_transform(X)

 return {
 'high_correlation_pairs': high_corr_pairs,
 'low_variance_features': X.columns[~selector.get_support()].toList(),
 'selected_features': X.columns[selector.get_support()].toList()
 }

# Example of use
multicollinearity_results = evaluate_multicollinearity(df, threshold=0.8)
```

♪##2 ♪ Machine test training ♪

** Test of importance of signs:**

```python
def evaluate_feature_importance(df, target_col, n_features=20):
""""""""""""""
 from sklearn.ensemble import RandomForestRegressor
 from sklearn.model_selection import train_test_split

# Data production
 X = df.drop(columns=[target_col])
 y = df[target_col]

# Separation on train/test
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model learning
 model = RandomForestRegressor(n_estimators=100, random_state=42)
 model.fit(X_train, y_train)

# The importance of signs
 feature_importance = pd.dataFrame({
 'feature': X.columns,
 'importance': model.feature_importances_
 }).sort_values('importance', ascending=False)

# The top of the signs
 top_features = feature_importance.head(n_features)

 return {
 'feature_importance': feature_importance,
 'top_features': top_features,
 'model_score': model.score(X_test, y_test)
 }

# Example of use
importance_results = evaluate_feature_importance(df, 'target', n_features=20)
```

** Test of stability of signs:**

```python
def evaluate_feature_stability(df, target_col, n_splits=5):
""""""""""""""
 from sklearn.model_selection import KFold
 from sklearn.ensemble import RandomForestRegressor

# Data production
 X = df.drop(columns=[target_col])
 y = df[target_col]

# K-fold cross-validation
 kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

# List for storing the importance of the signs
 feature_importances = []

 for train_idx, val_idx in kf.split(X):
 X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
 y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

# Model learning
 model = RandomForestRegressor(n_estimators=100, random_state=42)
 model.fit(X_train, y_train)

# Maintaining the importance of signs
 feature_importances.append(model.feature_importances_)

# Calculation of stability
 feature_importances = np.array(feature_importances)
 stability = np.std(feature_importances, axis=0)

 # create dataFrame
 stability_df = pd.dataFrame({
 'feature': X.columns,
 'stability': stability,
 'mean_importance': np.mean(feature_importances, axis=0)
 }).sort_values('stability')

 return stability_df

# Example of use
stability_results = evaluate_feature_stability(df, 'target', n_splits=5)
```

## Application of signs in AutoML Gluon

### 🔗 integration with AutoML Gluon

```mermaid
graph TD
A[Backgrounds] -> B [data preparation]
B -> C [Trin/test division]
 C --> D[create TabularPredictor]

D -> E [configration of parameters]
 E --> F[problem_type: regression/classification]
 E --> G[eval_metric: rmse/accuracy]
 E --> H[presets: best_quality]

F --> I [model training]
 G --> I
 H --> I

I -> J [Automatic choice of topics]
 J --> K[Mutual Information]
 J --> L[F-regression]
 J --> M[Random Forest importance]

K --> N [Selection of the best signs]
 L --> N
 M --> N

N -> O [Learning the Final Model]
O-> P [Treaties on the test]
P -> Q [Quality assessment]

 Q --> R[MSE/RMSE]
 Q --> S[R² Score]
 Q --> T[Feature importance]

R --> U [Results]
 S --> U
 T --> U

U --> V {Quality acceptable?}
V-~\\\\W[The Business Model]
V-~\\\\X[Optimization of topics]

X --> Y[add new signs]
Y --> Z[remove bad signs]
Z -> AA [configration of parameters]

 Y --> B
 Z --> B
 AA --> B

W --> BB [Monitoring in Sales]
BB --> CC [Drift tracking]
CC --> DD[retraining as required]

 style A fill:#e3f2fd
 style I fill:#c8e6c9
 style U fill:#a5d6a7
 style W fill:#4caf50
 style X fill:#ff9800
```

### 1. integration with AutoML Gluon

```python
def apply_features_to_autogluon(df, target_col, feature_cols, test_size=0.2):
"Applicability in AutoML Gluon""
 from autogluon.tabular import TabularPredictor

# Data production
 X = df[feature_cols]
 y = df[target_col]

# Separation on train/test
 from sklearn.model_selection import train_test_split
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

 # create train_data
 train_data = X_train.copy()
 train_data[target_col] = y_train

♪ Create pre-reactor
 predictor = TabularPredictor(
 label=target_col,
 problem_type='regression',
 eval_metric='rmse'
 )

# Training
 predictor.fit(
 train_data,
Time_limit=3600, #1 hour
 presets='best_quality'
 )

 # Prediction
 predictions = predictor.predict(X_test)

# Quality assessment
 from sklearn.metrics import mean_squared_error, r2_score
 mse = mean_squared_error(y_test, predictions)
 r2 = r2_score(y_test, predictions)

 return {
 'predictor': predictor,
 'predictions': predictions,
 'mse': mse,
 'r2': r2,
 'feature_importance': predictor.feature_importance()
 }

# Example of use
results = apply_features_to_autogluon(df, 'target', feature_cols, test_size=0.2)
```

♪##2 ♪ Automatic selection of signs

```python
def automatic_feature_selection(df, target_col, method='mutual_info', k=20):
"Automatic Signs Choice."
 from sklearn.feature_selection import (
 SelectKBest, mutual_info_regression, f_regression,
 SelectFromModel, RandomForestRegressor
 )

# Data production
 X = df.drop(columns=[target_col])
 y = df[target_col]

 if method == 'mutual_info':
 # Mutual Information
 selector = SelectKBest(score_func=mutual_info_regression, k=k)
 elif method == 'f_regression':
 # F-regression
 selector = SelectKBest(score_func=f_regression, k=k)
 elif method == 'random_forest':
 # Random Forest
 model = RandomForestRegressor(n_estimators=100, random_state=42)
 selector = SelectFromModel(model, max_features=k)
 else:
 raise ValueError("Method must be 'mutual_info', 'f_regression', or 'random_forest'")

# Selector application
 X_selected = selector.fit_transform(X, y)

# Obtaining selected topics
 selected_features = X.columns[selector.get_support()].toList()

 return {
 'selected_features': selected_features,
 'X_selected': X_selected,
 'selector': selector
 }

# Example of use
selected_features = automatic_feature_selection(df, 'target', method='mutual_info', k=20)
```

###3: Pipline of Signal Generation

### ♪ Pikeline of sign generation

```mermaid
graph TD
A [Reference data] --> B [Feature Generation Pipeline]

B -> C [Indicators Generators]
C -> D [Temporary signs]
C -> E [Statistical indicators]
C --> F[Technical indicators]
C --> G[Categorial characteristics]
C -> H [Text indicators]

D -> I [College of topics]
 E --> I
 F --> I
 G --> I
 H --> I

I -> J [Indicators selectors]
 J --> K[Mutual Information]
 J --> L[F-regression]
 J --> M[Random Forest]
 J --> N[Variance Threshold]

K --> O [Selection of topics]
 L --> O
 M --> O
 N --> O

O-> P[validation of topics]
 P --> Q[Cross-validation]
 P --> R[Stability testing]
 P --> S[Drift detection]

Q -> T [Final set of indicators]
 R --> T
 S --> T

T --> U [Applicable in AutoML Gluon]
U -> V [model training]
V --> W [Evaluation of performance]

W --> X {Result acceptable?}
X -->\\\\\Y[Business in Sales]
X-~ ♪ No ♪ Z [Pipline Optimization]

Z -> AA [configration of generators]
Z --> BB [configuring selections]
Z-> CC[add new methods]

 AA --> B
 BB --> B
 CC --> B

Y --> DD [Monitoring in Sales]
DD --> EE [Quality Monitoring]
EE --> FF[Automatic retraining]

 style A fill:#e3f2fd
 style B fill:#c8e6c9
 style T fill:#a5d6a7
 style Y fill:#4caf50
 style Z fill:#ff9800
```

```python
class FeatureGenerationPipeline:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self):
 self.feature_generators = []
 self.feature_selectors = []
 self.fitted = False

 def add_generator(self, generator_func, **kwargs):
""""""""""""""""
 self.feature_generators.append((generator_func, kwargs))

 def add_selector(self, selector_func, **kwargs):
""""""""""""""""""
 self.feature_selectors.append((selector_func, kwargs))

 def fit_transform(self, df, target_col):
"Learning and transformation."
 result_df = df.copy()

# Use of generators
 for generator_func, kwargs in self.feature_generators:
 result_df = generator_func(result_df, **kwargs)

# Use of selection devices
 for selector_func, kwargs in self.feature_selectors:
 result_df = selector_func(result_df, target_col, **kwargs)

 self.fitted = True
 return result_df

 def transform(self, df):
"Only transformation."
 if not self.fitted:
 raise ValueError("Pipeline must be fitted first")

 result_df = df.copy()

# Use of generators
 for generator_func, kwargs in self.feature_generators:
 result_df = generator_func(result_df, **kwargs)

 return result_df

# Example of use
pipeline = FeatureGenerationPipeline()

# add generators
pipeline.add_generator(create_lag_features, target_col='price', lags=[1, 2, 3, 7, 14, 30])
pipeline.add_generator(create_rolling_features, target_col='price', windows=[3, 7, 14, 30])
pipeline.add_generator(create_trend_features, target_col='price', windows=[7, 14, 30, 50, 200])

# add selections
pipeline.add_selector(automatic_feature_selection, method='mutual_info', k=50)

# Learning and transformation
df_transformed = pipeline.fit_transform(df, 'target')
```

## Monitoring and validation of features

♪##1 ♪ Monitoring drift of signs ♪

```python
def monitor_feature_drift(df_baseline, df_current, feature_cols, threshold=0.1):
"Monitoring the sign drift."
 from scipy import stats

 drift_results = {}

 for col in feature_cols:
# Statistical tests
 ks_stat, ks_pvalue = stats.ks_2samp(df_baseline[col], df_current[col])
 chi2_stat, chi2_pvalue = stats.chi2_contingency(
 pd.crosstab(df_baseline[col], df_current[col])
 )[0:2]

# Calculation of drift
 baseline_mean = df_baseline[col].mean()
 current_mean = df_current[col].mean()
 drift = abs(current_mean - baseline_mean) / baseline_mean

# Status determination
 if drift > threshold:
 status = 'DRIFT'
 elif ks_pvalue < 0.05:
 status = 'DISTRIBUTION_CHANGE'
 else:
 status = 'STABLE'

 drift_results[col] = {
 'drift': drift,
 'ks_stat': ks_stat,
 'ks_pvalue': ks_pvalue,
 'chi2_stat': chi2_stat,
 'chi2_pvalue': chi2_pvalue,
 'status': status
 }

 return drift_results

# Example of use
drift_results = monitor_feature_drift(df_baseline, df_current, feature_cols, threshold=0.1)
```

♪##2 ♪ Validation of features ♪

```python
def validate_features(df, target_col, feature_cols, validation_method='cross_validation'):
"Validation of the signs."
 from sklearn.model_selection import cross_val_score
 from sklearn.ensemble import RandomForestRegressor
 from sklearn.linear_model import LinearRegression

# Data production
 X = df[feature_cols]
 y = df[target_col]

# Models for validation
 models = {
 'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
 'LinearRegression': LinearRegression()
 }

 validation_results = {}

 for model_name, model in models.items():
# Cross-validation
 scores = cross_val_score(model, X, y, cv=5, scoring='r2')

 validation_results[model_name] = {
 'mean_score': scores.mean(),
 'std_score': scores.std(),
 'scores': scores
 }

 return validation_results

# Example of use
validation_results = validate_features(df, 'target', feature_cols, validation_method='cross_validation')
```

## Summary table of indicator generation parameters

### ♪ Basic {meters of the function of producing the signs

==============================================================================================================================)===================)===========)===============)==========================)==================================== ================================================================================================================================================================================================================================================================================
|---------|----------|----------------------|----------|------------------|
| **create_lag_features** | | | | |
♪ ♪ 'lags' ♪ [1, 2, 3, 7, 14, 30] ♪ List Lags for creation ♪ 1-365 days ♪
♪ ♪ 'fill_method' ♪ 'forward' ♪ Method of filling passes ♪ forward, backward, interpolate, zo ♪
♪ Include_riginal' ♪ False ♪ Inclusion of the original column ♪ True, False ♪
♪ ♪ 'lag_prefix' ♪ 'lag' ♪ Prefix for names ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `config.validation' ♪ True ♪ ♪ data validation ♪ True, False ♪
♪ `config.memory_officer' ♪ False ♪ memory-use ♪ True, Fales ♪
| **create_rolling_features** | | | | |
♪ o `windows' ♪ [3, 7, 14, 30] ♪ window dimensions ♪ 1-365 periods ♪
♪ 'statistics' ♪ ['mean', 'std', 'min', 'max', 'median'] ♪ Statistics for calculation ♪ mean, std, var, min, max, median, sum, count, skew, kurt, quantile ♪
♪ ♪ Min_periods' ♪ None ♪ Minimum number of observations ♪ 1-Window ♪
♪ ♪ 'center' ♪ False ♪ Centralize window ♪
== sync, corrected by elderman == @elder_man
♪ `config.quantiles' ♪ [0.25, 0.5, 0.75] ♪ Quantiles for the calculation of ~ 0.0-1.0 ♪
\\`config.custom_funds'\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
♪ `config.fill_method' ♪ 'forward' ♪ Method of filling passes ♪ forward, backward, interpolate, zo ♪
♪ `config.prefix' ♪ 'rolling' ♪ Prefix for names ♪ ♪ Str ♪
| **create_ewm_features** | | | | |
♪ o `alphas' ♪ [0.1, 0.3, 0.5, 0.7] ♪ smoothing rates ~ 0.0 to 1.0 ♪
~ `statistics' ♪ ['mean'] ♪ Statistics for the calculation of ♪ mean, std, var, min, max, sum, account ♪
== sync, corrected by elderman == @elder_man
♪ 'ignore_na' ♪ False ♪ Ignore NaN ♪ True, False ♪
♪ ♪ 'bias' ♪ False ♪ displaced variance estimate ♪ True, False ♪
♪ `config.span' ♪ None ♪ Alternative to alpha ♪ 1–100 ♪
♪ `config.halflife' ♪ ♪ None ♪ ♪ Alternative to alpha ♪ 1–1000 ♪
♪ ♪ `config.com' ♪ None ♪ ♪ Alternative to alpha ♪ 1–1000 ♪
♪ ♪ `config.prefix' ♪ 'ewm' ♪ Prefix for names ♪ ♪ Str ♪
| **create_seasonal_features** | | | | |
♪ 'feed', 'month', 'day', 'dayfweek', 'dayofyear', 'dayyear', 'week', 'quarter'] ♪ Seasonal signs ♪ year, year, day, day, day, day, week, week, week, quarter, day, day, day, day, day, day, day, day, day, night, day, day, day, day, day, day, day, day, day, day, day, day, day, day, day, day, day, day, 'day, 'week', 'week', 'quert, is_month_start, is_month_end, is_Quart, is_Quarter_end, is_year_start, is_year_end
♪ ♪ Cyclic_features' ♪ True ♪ ♪ create cyclical signs ♪ True, False ♪
♪ o `timezone' ♪ ♪ Time belt ♪ ♪ Time belt ♪ (UTC, Europe/Moscow, etc.)
♪ 'business_hours' ♪ False ♪ create signs of working hours ♪ True, Fales ♪
♪ ♪ 'holidays' ♪ None ♪ List of holidays ♪
♪ `config.cyclic_periods' ♪ {'month': 12, 'dayofweek': 7, 'hour': 24, 'dayofyear': 365} ♪ Periods for cyclical signs ♪ dick ♪ dick': 7, 'hour':24, 'dayofyer': 365} ¶
♪ `config.business_hours_start' ♪ 9 ♪ start hours ♪ 0-23 ♪
♪ 'config.business_hours_end' ♪ 17 ♪ End of working hours ♪ 0-23 ♪
♪ `config.business_days' [0, 1, 2, 3, 4] ♪ Workdays ♪ List of Int (0-6) ♪
♪ `config.prefix' ♪ 'seasonal' ♪ Prefix for names ♪
| **create_moment_features** | | | | |
♪ ♪ 'Windows' ♪ [7, 14, 30] ♪ Windows for calculation ♪ 1-365 periods ♪
♪ `config.prefix' ♪ 'moment' ♪ Prefix for names ♪ ♪ Str ♪
| **create_change_features** | | | | |
♪ o `periods' ♪ [1, 2, 3, 7, 14, 30] ♪ Times for change ♪ 1-365 periods ♪
♪ `config.prefix' ♪ 'change' ♪ Prefix for names ♪ ♪ Str ♪
| **create_volatility_features** | | | | |
♪ ♪ 'Windows' ♪ [7, 14, 30] ♪ Windows for volatility ♪ 1-365 periodes ♪
♪ ♪ `config.prefix' ♪ 'vol' ♪ Prefix for names ♪ ♪ Str ♪
| **create_trend_features** | | | | |
♪ ♪ 'windows' ♪ [7, 14, 30, 50, 200] ♪ Windows for trend indicators ♪ 1-365 periods ♪
♪ ♪ `config.prefix' ♪ 'trend' ♪ Prefix for names ♪ ♪ Str ♪
| **create_momentum_features** | | | | |
♪ ♪ 'Windows' ♪ [7, 14, 30] ♪ Windows for points of indicators ♪ 1-365 periods ♪
♪ `config.prefix' ♪ 'momentum' ♪ Prefix for names ♪ ♪ Str ♪
| **create_volatility_indicators** | | | | |
♪ ♪ 'Windows' ♪ [7, 14, 30] ♪ Windows for the volatility of indicators ♪ 1-365 periods ♪
♪ `config.prefix' ♪ 'vol_ind' ♪ Prefix for names ♪
| **create_categorical_features** | | | | |
♪ o `categorical_cols' ♪ ♪ List of categorical columns ♪ List of str ♪
♪ ♪ `config.prefix' ♪ 'cat' ♪ Prefix for names ♪ ♪ Str ♪
| **create_hierarchical_features** | | | | |
♪ o `hierarchical_cols' ♪ ♪ List of hierarchical columns ♪ List of string ♪
♪ ♪ `config.prefix' ♪ 'hier' ♪ Prefix for names ♪ ♪ Str ♪
| **create_text_features** | | | | |
== sync, corrected by elderman == @elder_man
♪ ♪ `config.prefix' ♪ 'text' ♪ Prefix for names ♪ ♪ Str ♪
| **create_tfidf_features** | | | | |
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `config.prefix' ♪ 'tfidf' ♪ Prefix for names ♪ ♪ Str ♪
| **create_word2vec_features** | | | | |
== sync, corrected by elderman == @elder_man
♪ o'vector_size' ♪ 100 ♪ vector size ♪ 50-500 ♪
♪ `config.prefix' ♪ 'w2v' ♪ Prefix for names ♪ ♪ Str ♪
| **genetic_feature_generation** | | | | |
Number of generations
♪ ♪ Population_size' ♪ 100 ♪ stock size ♪ 50 - 1,000 ♪
♪ `config.prefix' ♪ 'genetic' ♪ Prefix for names ♪
| **create_polynomial_features** | | | | |
♪ o `feature_cols' ♪ [] ♪ List signs for polynomial ♪ List of ♪
♪ ♪ 'Degree' ♪ 2 ♪ of polynomial ♪ 1 - 5 ♪
♪ ♪ Interaction_only ♪ ♪ False ♪ Only interactions ♪ True, False ♪
♪ `config.prefix' ♪ ♪ 'poly' ♪ Prefix for names ♪ ♪ Str ♪
| **create_interaction_features** | | | | |
♪ o `feature_cols' ♪ [] ♪ List signs for interactions ♪ List of str ♪
== sync, corrected by elderman == @elder_man
♪ `config.prefix' ♪ 'interaction' ♪ Prefix for names ♪ ♪ Str ♪

### ♪ Recommendations on setting parameters

##### For starters

- Use on default values for most parameters
- Adjust only the main parameters (lags, Windows, alphas)
- Include basic statistics (mean, std, min, max)
- Use simple methhods filling out passes (forward)

##### for experienced users

- Set all variables in line with your data.
- Add user functions and cyclical features
- Use expanded statistics (skew, kurt, quantile)
- Set up the validation and effective use of memory

#### # For sale

- Set all variables in line with SLA requirements
- Include all types of features (temporal, statistical, technical, categorical, textual)
- Use automatic event generation
- Set up the Monitoring and Identification of the Signs
- Turn on all security and performance checks.

## Conclusion

Feature Generation is the foundation of successful machine lightning. The correct generation of signs can:

1. ** Increase accuracy** models on 20-50%
2. ** Improve interpretation** of results
3. ** To increase the efficiency** of models
4. ** Reduce time**

### Key principles

1. ** Understanding data** - know with what Worknet is
2. ** Home knowledge** - Use of subject matter expertise
3. ** Automation** - automate routine processes
4. **validation** - Always check the quality of the signs
5. **Monitoring** - Monitor the stability of the signs

### Next steps

Once the signs have been developed, go to:

- [Becketting medics](./27_backtesting_methods.md)
- [Walk-forward analysis](./28_walk_forward_Anallysis.md)
- [Monte Carlo simulation](./29_monte_carlo_simulations.md)
- [Porthfolio Administration](./30_Porthfolio_Management.md)
