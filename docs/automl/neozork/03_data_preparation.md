#03. ♪ Data production

**Goal:** Learn how to properly prepare and clean financial data for ML models.

# # Why do you need quality data?

**Theory:** Data quality is a fundamental factor in the success of ML systems. In the financial sphere, this is particularly critical, as data errors can lead to significant financial losses. The production of data is a process of transforming raw data into a format suitable for machinine lightning.

** Data quality = model quality**

** Why quality data production is critical:**
- ** Financial risks:** Bad data can lead to bad trade decisions
- ** Regulatory requirements:** Financial regulators require data accuracy
- ** Competition advantage:** Qualitative data gives an advantage on the market
- ** User confidence:** Precise predictions increase confidence in the system

**Bad data result in:**
- ** False signals:** Wrong trade signals due to in-data errors
- ** Retraining:** Model memorizes noise instead of real pathers.
- ** Unstable results:** Unpredictable behaviour of the system
- ** Loss of money:** Direct financial loss from wrong decisions

** Plus quality data production:**
- Improvement of model accuracy
- Risk reduction
- improve system stability
- Building user confidence

**Mine of quality data production:**
- High time costs
- Complexity of the process
- Need for expertise
- High requirements for computing resources

## Types of financial data

**Theory:** Financial data have a specific structure and characteristics that need to be taken into account when preparing for ML models. Understanding data types is critical for creating effective signs and preventing errors.

### 1. OHLCV data

**Theory:** OHLCV (Open, High, Low, Class, Volume) is a standard financial data format that provides basic information on trade sessions. These data are the basis for most financial ML models.

** Why OHLCV data matters:**
- ** Fullness of information:** Contain all necessary information on the trade session
- ** Standardization:** Universal format supported by alli platforms
- ** Historical compatibility:** Allows Working with historical data
- **Technical analysis:** Basis for all technical indicators

** Data Plus OHLCV:**
- Full information on the trade session
- Standardized format
- compatibility with technical indicators
- High accuracy of data

** OHLCV data ratios:**
- May contain noise and emissions
- Need to process missing values
- May be manipulated.
- Limited information on intra-day dynamics
```python
#Stucture OHLCV data
data = {
'Open': [100, 101, 102] # Opening price
'High': [105, 106, 107] # Maximum price
'Low': [99, 100, 101] # Minimum price
'Close': [104, 105, 106] # Closing price
'Volume': [1000, 1200, 1100] #Tender volume
}
```

###2: Percentage changes

**Theory:** Percentage changes (returns) are more stable for ML models than absolute prices; they normalize data and make them more suitable for machinin lightning.

**Why percentage changes are better for ML:**
- **Stationality:** Percentage changes are more fixed than absolute prices
- **Normalization:** Automatic normalization of data
- ** Equivalence:** Allows asset comparison with different prices
**Statistical properties:** Better suited for statistical methods

** Plus percentage changes:**
- More stable for ML models
- Automatic normalization
- Best statistical properties
- Comparability between assets

**/ Percentage changes:**
- Loss of absolute level information
- May be less interpreted
- They need caution when they reverse conversion.
- May increase noise in data
```python
# More stable for ML
data['price_change'] = data['Close'].pct_change()
data['volume_change'] = data['Volume'].pct_change()
```

♪## 3. Technical indicators

**Theory:**Technical indicators are mathematical transformations of price data that help to identify patterns and trends, which are the basis for creating signs in financial ML models.

**Why the Technical Indicators are important:**
- **Patternament identification:** Helps detect hidden pathites in data
- ** Noise filtering:** Recognizance of random fluctuations
- ** Standardization:** Universal metrics for Analysis
- **Expert knowledge:** Includes the experience of technical analysts

**Typs of technical indicators:**
- **Trend:** SMA, EMA, MACD - show direction of trend
- **Oscillators:** RSI, Stochastic - indicate oversizing/resellability
- ** Volatility:** Bollinger Bands, ATR - show volatility
- ** Unit:** OBV, VWAP - account for tender volume

** Plus technical indicators:**
- Identification of hidden pathers
- Noise filtering
- Standardized metrics
- Inclusion of expertise

**Mine of technical indicators:**
- Could be late.
- Could generate false signals.
- It requires Settings parameters.
- May be excessive.
```python
# RSI, MACD, Bollinger Bands
data['RSI'] = calculate_rsi(data['Close'])
data['MACD'] = calculate_macd(data['Close'])
data['BB_Upper'] = calculate_bollinger_upper(data['Close'])
```

## Clear data

**Theory:** Clear data is a critical stage in the production of data for ML models. Qualitative clay data can significantly improve model performance and reduce risks.

**Why is the data glue important:**
- ** Model quality:** Net data leads to better models
- ** Noise reduction: ** noise reduction improves education
- ** Prevention of errors:** Clear prevents errors in models
- ** Increased stability:** Net data makes models more stable

###1. remove duplicates

**Theory:** In-data duplicates can distort learning outcomes and lead to re-learning. Removing duplicates is critical for financial data, where duplicates can arise from technical failures or errors in data collection systems.

** Why duplicates are problematic:**
- **Statistics:** Duplicates distort the statistical properties of the data
- **retraining:** Model can remember duplicates
- ** Unequal distribution:** Duplications create uneven distribution of data
- ** Fake correlations:** Duplicates can create false correlations

** Plus the removal of duplicates:**
- Improve data quality
- Prevention of retraining
- More precise statistical properties
- Risk reduction

**Minuses of removal of duplicates:**
- Possible loss of important information
- The difficulty of defining true duplicates
- Risk of removal of legitimate data
- Need for expert Analysis
```python
def remove_duplicates(df):
""remove duplicates."
 return df.drop_duplicates()
```

###2: Processing missing values

**Theory:** Missing values in financial data can arise for various reasons: Technical malfunctions, weekends, holidays, or Issues with data sources. The correct processing of missing values is critical for the quality of ML models.

** Why missing values are problematic:**
- ** Infringement of time series:** Passes disrupt the continuity of time series
- ** Mistakes in calculations:** Many not algorithms can Working with missing values
- **Statistics statement:** Data gaps distort statistical properties
- **Breaking model quality:** Models trained on data with passes are worse

** Missed values processing strategies:**

**1. Forward Fill (ffill) - for price data:**
- ** Principle:** uses the last known value
- ** Application:** Perfect for price data, where omissions are usually short-term
- ** Benefits:** Saves Logs time series, not creates artificial patterns
- ** Disadvantages:** May mask real changes in data

**2. Interpolation - for volume data:**
** Principle: ** Calculates intermediate values on base of neighbouring points
- ** Application: ** Suitable for volume data where smooth changes can be assumed
- ** Benefits:** More accurate recovery, taking into account trends
- ** Disadvantages:** Could create unrealistic values

**3. Backward Fill (bfill) - for some cases:**
- ** Principle: ** Uses the following known value:
- ** Application: ** When it is known that the pass occurred at the end of the period
- ** Benefits:** Maintains relevance of data
- ** Disadvantages:** Could create false pathites.

** Plus correct processing of missing values:**
- Improve data quality
- Maintaining the integrity of the time series
- Improvement of model accuracy
- Prevention of errors in calculations

**Measures of missing values:**
- Possible distortion of real data
- creative artificial patterns
- The difficulty of choosing the right strategy
- Risk of masking important changes

```python
def handle_Missing_values(df):
"" Processing of missing values

This function applies different strategies for processing missing values
in terms of data type:
- Forward falls for price data (saves Logs time series)
- Interpolation for volume data (takes into account trends)
 """
# Forward falls for prices - Use last known value
# It's Logs for prices, because the price usually doesn't change dramatically
 df['Close'] = df['Close'].fillna(method='ffill')
 df['Open'] = df['Open'].fillna(method='ffill')
 df['High'] = df['High'].fillna(method='ffill')
 df['Low'] = df['Low'].fillna(method='ffill')

# Interpolation for volumes - compute intermediate values
# Volumes can change more smoothly, so interpolation fits
 df['Volume'] = df['Volume'].interpolate()

 return df
```

### 3. remove emissions

**Theory:** Emissions (outliers) are values that differ significantly from the rest of the data in the set. In financial data emissions may arise from technical failures, data entry errors, or extreme market events. The correct treatment of emissions is critical for the quality of ML models.

**Why emissions are problematic:**
- **Statistics statement:** Emissions highly influence mean value and standard deviation
- **retraining:** Models can remember emissions instead of real pathers.
- ** Depreciation of accuracy:** Emissions worsen the performance of most algorithms
- ** False signals:** Emissions can generate false trade signals

** Emissions in financial data: **

**1. Technical emissions:**
- ** Cause:** Errors in data collection systems, Technical malfunctions
- ** Haracteristics:** Values that are physically impossible (e.g. negative prices)
- ** Processing:** Complete remove

**2. Market emissions:**
- ** Cause:** Extreme market events (craches, panics)
- ** Haracteristics:** Real but rare events
- ** Processing:** Careful remove or special treatment

**3. Temporary emissions:**
- ♪ Cause: ♪ Festivities, weekends, days off ♪
- ** Haracteristics:** No tender or abnormal activity
- ** Processing:** Context processing

**methods emission detection:**

**1. Z-Score method:**
** Principle: ** Calculates the standard deviation from average
- **Formoule:** Z = (x - μ) /
- ** Threshold:** Usually 2-3 standard deviations
- ** Benefits:** Simplicity, interpretation
- ** Disadvantages:** Emission sensitivity in statistical calculation

**2. IQR (Interquartile Range) method:**
- **Principle:** Use interquartile scale
- **formula:** Outlier if x < Q1 - 1.5*IQR or x > Q3 + 1.5*IQR
- ** Benefits:** Less sensitive to emissions
- ** Disadvantages:** May miss some emissions

**3. Isolation Forest:**
- **Principle:** Machine training for detection of anomalies
- ** Benefits:**Workinget with multidimensional data
- ** Disadvantages:** Complexity, requires Settings

** Emission reduction plus:**
- Improve data quality
- Improvement of model accuracy
- Reducing noise exposure
- More stable results

**Measurements of emission removal:**
- Possible loss of important information
- Risk of removal of legitimate data
- The difficulty of determining true emissions
- Potential loss of market signals

```python
def remove_outliers(df, threshold=3):
""Remove emissions with Z-score aid

This function uses the Z-score method for detection and disposal.
Z-score shows on how many standard deviations the value is rejected from the average.

 parameters:
 - df: dataFrame with data
- threshold: Z-score threshold (on default 3)

Working principle:
1. Computes Z-score for each numerical column
2. Removes lines where:
3. Returns purified dataFrame
 """
# We get all the numbers
 numeric_columns = df.select_dtypes(include=[np.number]).columns

# Creating copy for safe work
 df_clean = df.copy()

# We're processing each number column
 for col in numeric_columns:
# Compute Z-score: (average) / standard deviation
 z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())

# Remove the lines with Z-score above the threshold
 df_clean = df_clean[z_scores < threshold]

 return df_clean
```

♪ ♪ Create signs ♪

♪## 1. Technical indicators

**Theory:** Technical indicators are mathematical transformations of price and volume data that help to identify hidden patharies, trends and signals in financial data. They are the basis for creating signs in financial ML models and represent a coded expert knowledge of technical analysts.

**Why Technical Indicators are important for ML:**
- **Pattern identification:** Helps identify hidden pathites that are not visible in raw data
- ** Noise filtering:** Grinds randomly and emits meaningful signals
- ** Standardization:** Universal instruments for various assets
- **Expert knowledge:** Includes multi-year experience of technical analysts
- **Normization:** refers data to a comparable scale

** Classification of technical indicators:**

**1. Trend indicators:**
- **SMA shows a general trend.
- **EMA (Exponential Moving Overage):** Exponsive moving average - more sensitive to recent changes
- **MACD (Moving Overage Convergence Divergence):** Convergence-distinguishing-distinguishing medium - shows trend changes

**2. Oscillators:**
- **RSI (Relative Strangth index):** index relative strength - shows overpurchase/reselling
- **Stochastic:** Stochastic oscillator - compares current price with range over period
- **Williams %R:** Williams' percentage range - shows price position in range

**3. Volatility indicators:**
- **Bollinger Bands:** Bollinger Poles - show volatility and levels of support/resistance
- **ATR (Average True Range):** Average True Range - shows volatility
- ** Standard Promotion:** Standard deviation - price spread measure

**4. Volume indicators:**
- **OBV (On-Balance Volume):** Balance volume - indicates accumulation/distribution
- **VWAP (Volume Weated Overage Price):** Average price weighted on volume
- ** Volume Rate of Change:** Speed of volume change

** Principles for the creation of technical indicators:**

**1. Choice of period:**
- ** Short periods (5-20):** More sensitive, more signals, more noise
- ** Average periods (20-50):** Balance between sensitivity and stability
- ** Long periods (50-200):** More stable, less signals, less noise

**2. Indicator combination:**
- **confirmation: ** Use of multiple indicators for signal confirmation
- ** Divergence:** Differences in behaviour of indicators and prices
- ** Synergy:** Combination of indicators of different types

** Plus technical indicators:**
- Identification of hidden pathers
- Noise filtering
- Standardized metrics
- Inclusion of expertise
- improve of the quality of the topics

**Mine of technical indicators:**
- Could be late.
- Could generate false signals.
- It requires Settings parameters.
- May be excessive.
-Dependency from historical data

```python
def create_Technical_indicators(df):
""create technical indicators

This Foundation creates a set of technical indicators for financial data.
Indicators help to identify patterns and trends that are not visible in raw data.

Indicators produced:
- SMA: Simple sliding average of different periods
- EMA: Explicit moving average
RSI: index relative strength
- MACD: Deterioration/dispersion of sliding averages
 """

# Slippery Medium
# SMA smooths down price data and shows a general trend
df['SMA_5'] = df['Close']rolling (5).mean() # Short-term trend
df['SMA_20'] = df['Close']rolling(20).mean() # Medium-term trend
 df['SMA_50'] = df['Close'].rolling(50).mean() # Long-term trend

# Exponential Mobile Overage
# EMA is more sensitive to recent changes
df['EMA_12'] = df['Close'].ewm(span=12).mean() # Rapid EMA
df['EMA_26'] = df['Close'].ewm(span=26).mean() # Slow EMA

 # RSI (Relative Strength index)
# Shows merchanting/reselling (0-100)
 df['RSI'] = calculate_rsi(df['Close'])

 # MACD (Moving Average Convergence Divergence)
# Shows trends
df['MACD'] = df['EMA_12'] - df['EMA_26'] # MACD Line
df['MACD_signal'] = df['MACD'].ewm(span=9).mean() # Signal line

 return df
```

###2: Statistical indicators

**Theory:** Statistical indicators are mathematical characteristics of data that describe their distribution, variability and dynamics. In financial data, statistical indicators help to identify market conditions, risks and opportunities for trading.

**Why statistical signs are important for ML:**
- **describe market conditions:** Show current market conditions (satisfying, volatile, trendy)
- ** Risk measurement:** Help assess risk and uncertainty
- ** Identification of anomalies:** Unusual market events detected
- **Normalization of data:** Bring data to comparable scale
- **improve preferences:** Add context information for models

**Schedule of statistical indicators:**

**1. Central trend measures:**
- ** Average (Mean):** Central distribution
- **Mediane (Median): ** Value in the middle of an orderly series
- ** Mode:** Most common value

**2. Measures of variability:**
- ** Standard Deviation:** Data variance measure
- ** Volatility:** Standard Deviation of Returns
- **Rage:** The difference between maximum and minimum values
- ** Interquartile Wave (IQR):** The difference between 75th and 25th percentiles

**3. Measures of distribution:**
- **Asymmetry (Skewness):**Symmetrical distribution measure
- **Excess (Kurtosis):** "Straight" distribution measure
- **Normality:** Conformity to normal distribution

**4. Dynamic measures:**
- **Momentum: ** Speed of price change
- **Rate of Change (ROC):** Percentage change over period
- **Acceleration:** Change in speed

**5. Correlation measures:**
- **According:** Correlation with previous values
- **Cross Correlation:** Correlation between different assets
- **Correlation with volume:** Price/volume connection

** Principles for the creation of statistical indicators:**

**1. Choice of window:**
- ** Short windows (5-20):** More change-sensitive
- ** Medium windows (20-50):** Balance between sensitivity and stability
- ** Longer windows (50-200):** More stable, less noise

**2. Normalization:**
- **Z-score:** Standardization on average and standard deviation
- **Min-Max:** Normalization to range [0, 1]
- **Robust scaling:** Use of the median and IQR

**3. Emission treatment:**
- **Winsorization:** Limitation of extreme values
- **Robust statistics:** Use of emission-resistant metrics
- **Outlier release:** Detection and treatment of emissions

** Plus of statistical indicators:**
- Objective describe data
- Identification of market conditions
- Risk measurement
- model quality improve
- Inspirability

**Mine of statistical characteristics:**
-Dependency from historical data
- Could be late.
- It requires Settings parameters.
- May be excessive.
- Emission sensitivity

```python
def create_statistical_features(df):
""create statistical characteristics

This function creates statistical indicators that describe
Distribution, variability and dynamics of financial data.

Elements created:
- Volatility: Volatility
Momentum: Momentum (ratio of current price to N periods back)
- ROC: Rate of Change (percentage change over period)
 """

# Volatility
# Shows price volatility - key risk indicator
# Calculated as the standard deviation of returns over the period
 df['Volatility'] = df['Close'].rolling(20).std()

# Momentum
# Shows the rate of price change
# Values > 1 means height < 1 - fall
 df['Momentum'] = df['Close'] / df['Close'].shift(10)

 # Rate of Change (ROC)
# Shows percentage change in price over period
# Positive values - growth, negative - fall
 df['ROC'] = df['Close'].pct_change(10)

# Additional statistical indicators

# Average over period (trend)
 df['Mean_20'] = df['Close'].rolling(20).mean()

# Median over the period (stable trend)
 df['Median_20'] = df['Close'].rolling(20).median()

# Period swing (volatility)
 df['Range_20'] = df['Close'].rolling(20).max() - df['Close'].rolling(20).min()

# Asymmetry (skewness)
 df['Skewness_20'] = df['Close'].rolling(20).skew()

# Distribution Excess (curtosis)
 df['Kurtosis_20'] = df['Close'].rolling(20).kurt()

 return df
```

♪##3 ♪ Time signs ♪

**Theory:** Time indicators are those that encode time information and time values in data. In financial time series, current values often depend from previous values, making time signs critical for ML models.

**Why temporary signs are important for ML:**
- **According:** Financial data have a strong autocoordination - current values depend from previous values
- **Trends and cycles:** Time indicators help to identify trends and cyclical patterns
- ** Market inertia:** Markets have inertia - current movements often continue
- ** Seasonal:** Financial data may have seasonal patterns
- ** Context: ** Time indicators provide context for current values

**Tips of time signs:**

**1. Legs:**
- ** Principle: ** Use of previous values as indicators
- ** Application:** Shows how past values are current
- **examples:** Close_lag_1, Close_lag_5, Close_lag_10
- ** Interpretation:** Direct dependency from historical values

**2. Differences:**
** Principle: ** Calculation of changes between current and previous values
- ** Application:** Shows speed and direction of change
- **examples:** Close_diff_1, Close_diff_5
- ** Interpretation:** Momentum and acceleration of change

**3. Rolling Windows:**
**Principle: ** Aggregation of data for a period
- ** Application:** Smoothing and identification of trends
- **examples:** Rolling mean, rolling std, rolling min/max
- ** Interpretation: ** Context information on the period

**4. Exponential Windows:**
- **Principle:** Higher weight of recent data
- ** Application:** Adaptation to changes in data
- **examples:** EMA, exponential weighted std
- ** Interpretation:** Adaptive trends

**5. Time markers (Time-based Features):**
- **Principle: ** Extraction of information from time tags
- ** Application:** Accounting for seasonality and cycles
- **examples:** Weekday, month, quarter, hour
- ** Interpretation:** Seasonal and Cyclic Pathers

** Principles for the creation of time signs:**

**1. Lag choice:**
- **Logs (1-5):** Direct dependency
- **Medical lags (5-20):** Medium-term mattresses
- ** Long lags (20-100):** Long-term trends

**2. Choice of differences:**
- ** First difference (diff=1):** Momentum
- ** Second difference (diff=2):** Acceleration
- ** Seasonal differences:** Seasonality accounting

**3. Choice of windows:**
- ** Short windows:** More sensitive to changes
- ** Longer windows:** More stable, less noise
- **Adjustable windows:** Changed in dependencies from volatility

** Plus temporary features:**
- Accounting for time dependencies
- Identification of trends and cycles
- improve prognosis capacity
- Inspirability
- Settings flexibility

**Measures of time:**
- Increase in data size
Multicollinearity problem
-Dependency from the quality of historical data
- The difficulty of choosing the parameters
- Risk retraining

```python
def create_time_features(df):
""create time signs

This function creates time signs that encode
Temporary information and definitions in financial data.

Elements created:
- Legi: Previous price values
- Varieties: Changes between current and previous values
- Rolling windows: Aggregation of data for the period
 """

# Lagues (Lags)
# Use previous values as signs
# It helps the model understand how past values are current
 for lag in [1, 2, 3, 5, 10]:
 df[f'Close_lag_{lag}'] = df['Close'].shift(lag)

# Differences
# Calculate changes between current and previous values
# This shows the speed and direction of change
 for diff in [1, 2, 5]:
 df[f'Close_diff_{diff}'] = df['Close'].diff(diff)

# Additional time signs

# Sliding averages of different periods
 for window in [5, 10, 20]:
 df[f'Close_ma_{window}'] = df['Close'].rolling(window).mean()

# Slipping standard deviations
 for window in [5, 10, 20]:
 df[f'Close_std_{window}'] = df['Close'].rolling(window).std()

# Rolling minimums and maximums
 for window in [5, 10, 20]:
 df[f'Close_min_{window}'] = df['Close'].rolling(window).min()
 df[f'Close_max_{window}'] = df['Close'].rolling(window).max()

# Percentage changes for different periods
 for period in [1, 2, 5, 10]:
 df[f'Close_pct_{period}'] = df['Close'].pct_change(period)

# Exponsive sliding medium
 for span in [5, 10, 20]:
 df[f'Close_ema_{span}'] = df['Close'].ewm(span=span).mean()

 return df
```

## Data normalisation

### 1. StandardScaler

**Theory:** StandardScaler is a method of data normalization that converts the signs to mean 0 and standard deviation 1. It is one of the most popular methods of normalization in machine learning.

**Why StandardScaler matters:**
- ** Signal scale:** Brings all signs to the same scale.
- **improve similarities:** Accelerates learning of algorithms based on gradient descent
- ** Prevention of domination:** Prevents the dominance of signs with high values
- **Compatibility with algorithms:** Many ML algorithms require normalized data
- **Stability:** Makes models more stable and interpretable

** StandardScaler principle:**
- **Formoule:** z = (x - μ) /
- ** μ (mu):** Mean value of the sign
- **(sigma):** Standard deviation of sign
- ** Results:** Signs with μ = 0 and \ = 1

** When to use StandardScaler:**
- **Normal distribution:** When the data are approximately normal
== sync, corrected by elderman == @elder_man
- **Neural networks:** for improvement of convergence
- **Clasterization:** K-means, hierarchical clustering
- **PCA:** for Analysis main component

** The advantages of StandardScaler:**
- Simplicity and interpretation
- Maintenance of distribution
- Workinget with most algorithms
- Standardized approach
- Good Workinget with normal distributions

** StandardScaler deficiencies:**
- Emission sensitivity
- Maybe not Working with strongly cut distributions.
- Needs to keep parameters for new data
- Could distort the original distribution.

```python
from sklearn.preprocessing import StandardScaler

def standardize_data(df):
"" Standardization of data with StandardScaler

This function applies standardization (Z-score noormalization) to numerical signature.
Standardization converts data to mean 0 and standard deviation 1.

Working principle:
1. Calculate average and standard deviation for each sign
2. Apply the formula: z = (x-mean) / std
3. Returns normalized data and scaler object

Returns:
- df: dataFrame with normalized data
- Scaler: StandardScaler object for reverse conversion
 """
# Creating StandardScaler
 scaler = StandardScaler()

# Only number columns are selected
 numeric_columns = df.select_dtypes(include=[np.number]).columns

# Applying standardization to numerical columns
# Fit_transform computes parameters and uses conversion
 df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

 return df, scaler
```

### 2. MinMaxScaler

**Theory:** MinMaxScaler (minimum-maximum normalization) is a method of data normalization that scale signs to a given range, usually [0, 1]. This method preserves the initial data distribution and is particularly useful when it is important to maintain zero values.

# Why MinMaxScaler matters #
- **Saves distribution:** Retains the original form of data distribution
- **Fixed range:** Brings all signs to the same range
- ** Zero retention:** Maintains zeros (important for diluted data)
- ** Interpretation: ** Easy to interpret normalized values
- **Compatibility:** Workinget with scale sensitive algorithms

** Operating principle MinMaxScaler:**
- **Formoule:** X_scaled = (X - X_min) / (X_max - X_min)
- **X_min:** Minimum value of signature
- **X_max:** Maximum value of signature
- **Result:** Signs in the range [0, 1]

** When to use MinMaxScaler:**
- **Restricted range: ** When data have a limited range
- ** Zero retention: ** When it is important to keep zeros
- **Neural networks:** for activation functions with a limited range
- ** Images:** for normalization of pixels (0-255 ~ 0-1)
- ** Percentage data:** When data is already in percentage format

** Benefits of MinMaxScaler:**
- Maintenance of reference distribution
- Fixed range [0, 1]
- Maintaining zero values
- Simple interpretation
- Good Workinget with limited data

** Disadvantages of MinMaxScaler:**
- Emission sensitivity
- Can squeeze data in a narrow range.
- not Workinget with unlimited distributions
- Needs to keep parameters.
- Could distort data with emissions.

```python
from sklearn.preprocessing import MinMaxScaler

def normalize_data(df):
""" "Normalization of data with MinMaxScaler

This function applies a minimum-maximum normalization to the numerical signature.
MinMaxScaler scalees data to the range [0,1] while maintaining the reference distribution.

Working principle:
1. Find minimum and maximum values for each sign
2. Apply the formula: (x-min) / (max-min)
3. Returns normalized data and scaler object

Returns:
- df: dataFrame with normalized data (range [0, 1])
- Scaler: Subject MinMaxScaler for reverse conversion
 """
# Creating object MinMaxScaler
 scaler = MinMaxScaler()

# Only number columns are selected
 numeric_columns = df.select_dtypes(include=[np.number]).columns

# Applying normalization to numerical columns
# Fit_transform computes min/max and uses conversion
 df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

 return df, scaler
```

## of target variables

###1. Classification of direction

**Theory:** The direction classification is the task of predicting the direction of the price (up, down, no change) on a certain time horizon, which is one of the most popular tasks in financial machine learning because it allows for the creation of trade strategies.

**Why direction classification is important:**
- ** Trading strategies:** Allows the creation of simple trade signals (buy/sell/sell)
- **Manage Risks:** Helps assess the probability of different outcomes
- ** Interpretation:** Easy to understand and explain the results
- **Practice:** Directly applicable to real trade
Equality:** Allows comparison of different models

**Tips of direction classification:**

**1. Binary classification:**
- **Classes:** Up (1) / Down (0)
** Threshold: **/ Usually 0 per cent or a small threshold (e.g. 0.1 per cent)
- ** Application:** Simple trade strategies
- ** Benefits:** Simplicity, clear signals
- ** Disadvantages:** Ignore minor changes

**2. Three-class classification:**
- **Classes:** Up (2) / Unchanged (1) / Down (0)
- ** Thresholds:** Two thresholds (e.g. -0.1 and +0.1 per cent)
- ** Application:** More precise trade strategies
- ** Benefits: ** Accounting for neutral states
- ** Disadvantages:** The complexity of the Settings thresholds

**3. Multi-class classification:**
- **Classes: ** Several levels of change (e.g. grades 5-7)
- ** Thresholds:** Several thresholds
- ** Application:** Complex trade strategies
- ** Benefits:** High accuracy
- ** Disadvantages:** Complexity of interpretation

** Principles for target variables:**

**1. Horizontal choice:**
- **Scratcostrotic (1-5 days):** More volatile, more noise
- ** Medium term (1-4 weeks): ** Balance between accuracy and practicality
- ** Long-term (1-3 months):** More stable but less practical

**2. Choice of thresholds:**
- **Fixed thresholds:** Same for all periods
- **Adjustable thresholds:** Dependent from volatility
- ** Percentage thresholds:** Based on historical distribution

**3. Treatment of neutral zones:**
- ♪ Shorter zones: ♪ More signals, more noise ♪
- **Speed areas:** Less signals, less noise
- ** Adaptation zones:** Dependent from market conditions

** Plus of direction classification:**
- Simple interpretation
- Direct applicability to trade
- Easier model comparison
- Management of risks
- Practical.

**Minuses of direction classification:**
- Loss of information on the magnitude of changes
- dependency from choice of thresholds
- Ignoring the temporal aspects
- Settings' complexity
- Risk retraining

```python
def create_direction_target(df, horizon=1):
""create target variable for direction classification

This function creates a target variable for predicting the direction of the price.
The three-class classification is used: upwards, unchanged, downwards.

 parameters:
 - df: dataFrame with data
- horizon: The prediction horizon in days (on default 1)

Working principle:
1. Compute price after horizon days
2. Calculates percentage change
3. Classify on thresholds: < -0.1 per cent (down), -0.1 per cent to +0.1 per cent (no change), > + 0.1 per cent (up)

Returns:
- Target: Series with class labels (0=down, 1=no change, 2=up)
 """
# We get the price in the horizon days
 future_price = df['Close'].shift(-horizon)
 current_price = df['Close']

# Calculate the percentage change
 price_change = (future_price - current_price) / current_price

# Classification on thresholds
# -0.1 per cent and +0.1 per cent - thresholds for a neutral zone
 target = pd.cut(
 price_change,
 bins=[-np.inf, -0.001, 0.001, np.inf], # -0.1% and +0.1%
Labels=[0, 1, 2], #0=down, 1=no changes, 2=up.
 include_lowest=True
 )

 return target.astype(int)
```

###2: Regression for price

**Theory:** Regression for price is the task of predicting the exact value of the price on a certain time horizon. In contrast to the classification of direction, regression predicts specific numerical values, thus creating more accurate trade strategies.

**Why price regression is important:**
- ** The accuracy of preferences:** Predicts specific price values
- **Manage risk:** Allows estimates of potential gains/losses
- ** Optimization of entries:** Helps to determine the size of entries
- ** Stop-losses and teak products:** Allows the establishment of precise levels
- ** Portfel Management:** Helps in asset allocation

**Tips of price regression:**

**1. Direct price regression:**
- ** Target variable:** Absolute price after horizon days
- ** Benefits:** Simplicity, interpretation
- ** Disadvantages:**dependency from absolute price levels
- ** Application:** Short-term predictions

**2. Regression of percentage changes:**
- ** Target variable:** Percentage change in price
- ** Benefits:** Normalization, comparability of assets
- ** Disadvantages:** Complexity of interpretation
- ** Application:** Medium-term predictions

**3. Regression of logarithmic changes:**
- ** Target variable:** Logarithmic price change
- ** Benefits:** Symmetry, stability
- ** Disadvantages:** Complexity of interpretation
- ** Application:** Long-term predictions

**4. Volatility Regression:**
- ** Target variable:** Price volatility
- ** Benefits:** Management risk
- ** Disadvantages:** Measurement difficulty
- ** Application:** Risk management

** Principles for target variables for regression:**

**1. Horizontal choice:**
- **cratcostroctic (1-5 days):** High accuracy, a lot of noise
- ** Medium term (1-4 weeks): ** Balance of accuracy and stability
- ** Long-term (1-3 months):** Low accuracy, high stability

**2. Emission treatment:**
- **Winsorization:** Limitation of extreme values
- **Robust scaling:** Use of sustainable metrics
- **Outlier release:** Detection and treatment of emissions

**3. Normalization:**
== sync, corrected by elderman == @elder_man
- **MinMaxScaler:** Normalization to [0, 1]
- **RobustScaler:** Sustainable normalization

**4. Temporary aspects:**
- **Stationarity:** heck of data stability
- **According:** Accounting for time dependencies
- ** Seasonality:** Recording of seasonal pathers

** Plus price regression:**
- High accuracy preferences
- Specific numerical values
- Management of risks
- Optimizing trade policies
- Flexible application

** Cost regressions:**
- Complexity of interpretation
- dependency from data quality
- Risk retraining
- Emission sensitivity
- Complexity of wallidation

```python
def create_price_target(df, horizon=1):
""create target variable for price regression

This function creates a target variable for predicting price
On a certain time horizon.

 parameters:
 - df: dataFrame with data
- horizon: The prediction horizon in days (on default 1)

Working principle:
1. Takes the closing price in horizon days
2. Returns as a target variable for regression

Returns:
- Target: Series with target price values
 """
# We get the price in the horizon days
# shift(-horizon) shifts data backwards to get future values
 return df['Close'].shift(-horizon)
```

## data validation

###1. check quality

**Theory:** data quality validation is a critical process for checking data against expected quality standards. In financial machine learning, data quality has a direct impact on model quality and trade decisions.

** Why data quality appreciation is important:**
- ** Prevention of errors:** Identification of problems to model learning
- ** Improved accuracy:** Qualitative data results in better models
- ** Risk reduction:** Prevention of financial loss from bad data
- ** Compliance with standards: ** Compliance with regulatory requirements
- ** User confidence:** Increased confidence in the system

** Data quality checks: **

**1. check data completeness:**
- ** Missed values:** Percentage of missing values in each column
- ** Incomplete entries:** Lines with partially completed data
- ** Temporary passes:** Missing temporary periods
- **Critical fields:** sheck mandatory fields

**2. check data accuracy:**
- ** Emissions:** Values significantly different from expected values
- ** Unabled values:** Negative prices, zero volumes
- **Logsic errors:** High < Low, Close outside [Low, High]
- ** Time errors:** Wrong time tags

**3. heck of data consistency:**
- ** Internal conspicuity:** Conformity between adjacent fields
- ** Temporary consistency:** Logsic sequence over time
- **Cross-validation:**comparison with external sources
- ** Business rules:** Compliance with financial rules

**4. check of relevance:**
- ** Data freshness:** Time of last update
- ** Delays: ** Time between event and data acquisition
- ** Renewal rate:** Compliance with expected frequency
- ** Data sources:** Reliability of sources

**data quality metrics:**

**1. Completeness:**
- **Formoule:** (Number of values filled) / (Total number of values)
- ** Threshold:** Usually > 95%
** Interpretation: ** Percentage of data not missing

**2. Accuracy:**
- **Formoule:** (Number of correct values) / (Total number of values)
- ** Threshold:** Usually > 99%
** Interpretation: ** Percentage of data that are correct

**3. Consistency (Consistency):**
- **Formoule:** (Number of security records) / (Total number of records)
- ** Threshold:** Usually > 98%
- ** Interpretation:** Percentage of entries not violating business rules

**4. Relevance:**
- **Formoule:** Time between event and data acquisition
- ** Threshold: ** Depends from requirements (e.g. < 1 minutes)
- ** Interpretation:** Fresh data

**The data quality value added:**
- Prevention of errors
- Improvement of model accuracy
- Risk reduction
- Compliance with standards
- Confidence-building

** Data quality values:**
- Time costs
- Settings' complexity
- False responses
- Need for expertise
- dependency from the quality of the rules

```python
def validate_data_quality(df):
"" Data quality appreciation

This function performs a comprehensive quality assurance of financial data,
Including verification of completeness, accuracy and consistency.

 parameters:
- df: dataFrame with data for verification

Checks:
1. Missed values - percentage of missing values in each column
2. Emissions are the percentage of values that deviate more than on 3 sigma
3. Logsal errors - ohLCV data check
4. Temporary conspicuity - check time tags

Returns:
- dict: Vocabulary with data quality metrics
 """

# 1. check on missing values
# Calculate the percentage of missing values for each column
 Missing_ratio = df.isnull().sum() / len(df)

#2. check on emissions with Z-score
# Calculate the percentage of values that deviate more than on 3 sigma
 numeric_columns = df.select_dtypes(include=[np.number]).columns
 outlier_ratio = {}

 for col in numeric_columns:
if df[col].std() > 0: # Avoid division on zero
 z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
 outlier_ratio[col] = (z_scores > 3).sum() / len(df)
 else:
 outlier_ratio[col] = 0

# 3. Check Logsic Errors in OHLCV Data
 logical_errors = {}

 if 'High' in df.columns and 'Low' in df.columns:
 logical_errors['high_low_error'] = (df['High'] < df['Low']).sum() / len(df)

 if 'Open' in df.columns and 'Close' in df.columns and 'High' in df.columns and 'Low' in df.columns:
 logical_errors['ohlc_error'] = (
 (df['Open'] > df['High']) |
 (df['Open'] < df['Low']) |
 (df['Close'] > df['High']) |
 (df['Close'] < df['Low'])
 ).sum() / len(df)

 if 'Volume' in df.columns:
 logical_errors['negative_volume'] = (df['Volume'] < 0).sum() / len(df)

# 4. Check temporary conservancy
 time_consistency = {}

 if df.index.dtype == 'datetime64[ns]':
# Checking on duplicates of time tags
 time_consistency['duplicate_timestamps'] = df.index.duplicated().sum() / len(df)

# Chucking on Time Miss
 if len(df) > 1:
 time_diff = df.index.to_series().diff().dropna()
 expected_freq = time_diff.mode().iloc[0] if len(time_diff) > 0 else None
 if expected_freq is not None:
 time_consistency['time_gaps'] = (time_diff != expected_freq).sum() / len(time_diff)

 return {
 'Missing_ratio': Missing_ratio,
 'outlier_ratio': outlier_ratio,
 'logical_errors': logical_errors,
 'time_consistency': time_consistency
 }
```

###2 # Check stability #

**Theory:** heck of data stability is a process of time series on fixedness, statistical stability and lack of structural change. In financial data stability is critical for the reliability of ML models.

# Why chuck stability matters #
- **Stationarity:** Many ML algorithms imply data stability
- **Structural changes:** Identification of changes in data behaviour
- ** Model reliability:** Stable data leads to more reliable models
- ** Temporary consistence:** Ensuring consistency over time
- ** Prevention of drift:** Identification of drift in data

**Tips of stability checks:**

**1. heck of standing:**
- **ADF Test (Augmented Dickey-Fuller):** Checks the single root position
**KPSS test:** Checks the stability relative to the trend
- **PP test (Phillips-Perron):** ADF alternative test
- ** Interpretation:** p-value < 0.05 means stationary

**2. heck of structural change:**
- **Chaw test:** Checks the timing of structural changes
- **CUSUM test:** identifies accumulated changes
- **Bai-Perron test:** Determines the number of break points
- ** Application:** Identification of changes in data behaviour

**3. heck of homoscedity:**
- **What test:** Checks the persistence of dispersion
- **Breuch-Pagan test:** Alternative to White test
- **Goldfeld-Quandt test:** Checks homoscedidacy
- ** Interpretation:** p-value > 0.05 means homoscedity

**4. heck of autocorrigation:**
- **Ljung-Box test:** Checks no autocorration.
- **Durbin-Watson test:** Checks first order autocratulation
- **Breusch-Godfrey test:** Checks autocratulation of higher order.
- ** Interpretation:** p-value > 0.05 indicates no autocorration

**Metrics of data stability:**

**1. Stationary capacity:**
- **ADF statistics:** The more negative, the more stationary the data
- **p-value:** < 0.05 means stationary
- ** Critical values:** comparative with critical values

**2. Structural changes:**
- **F statistics:** The more likely structural changes are
**p-value:** < 0.05 means the priority of structural changes
- ** Breakpoints:** Time points of structural change

**3. Homoscedurality:**
- **LM statistics:** The more likely the heteroscedidacy is.
- **p-value:** > 0.05 means homoscedity
**R-squared:** Percentage of explained variance

**4. Auto-coordination:**
- **Q statistics:** The more, the more likely autocorrelation is.
- **p-value:** > 0.05 means no autocorration
- **Durbin-Watson:** Values close to 2 mean no autocorration

** Plus of stability check:**
- Ensuring model reliability
- Identification of structural changes
- Prevention of data drift
- Improve quality preferences
- Conformity with algorithm assumptions

** Stability tests: **
- Complexity of interpretation
- dependency from sample size
- False responses
- Need for expertise
- Time costs

```python
def check_data_stability(df):
""Check data stability

This function performs a comprehensive financial data stability audit,
Checking the stability, structural change and autocorration.

 parameters:
- df: dataFrame with data for verification

Checks:
1. Stationary capacity - ADF single root test
2. Structural changes - Show gap detection test
3. Homoscedaticity - White test for verifying the persistence of dispersion
4. Autocognition - Ljung-Box autocorration test

Returns:
- dict: Vocabulary with test results stability
 """

# 1. check on stability with the ADF test
 from statsmodels.tsa.stattools import adfuller
 from statsmodels.stats.diagnostic import acorr_ljungbox
 from statsmodels.stats.diagnostic import het_white
 from statsmodels.stats.stattools import durbin_watson

# ADF stability test
 adf_result = adfuller(df['Close'].dropna())

# 2. Heck autocorrelation with Ljung-Box test
# checking autocorration in the residues (if precent trend)
 if len(df) > 10:
 try:
# Compute the leftovers (first-order differences)
 residuals = df['Close'].diff().dropna()
 ljung_box_result = acorr_ljungbox(residuals, lags=10, return_df=True)
 ljung_box_pvalue = ljung_box_result['lb_pvalue'].iloc[-1]
 except:
 ljung_box_pvalue = None
 else:
 ljung_box_pvalue = None

# 3. check homoscedity with White Test
# Creating simple regression for the test
 if len(df) > 20:
 try:
# Creating lags for regression
 df_test = df[['Close']].copy()
 df_test['Close_lag1'] = df_test['Close'].shift(1)
 df_test = df_test.dropna()

 if len(df_test) > 10:
# Simple linear regression
 from statsmodels.regression.linear_model import OLS
 from statsmodels.tools import add_constant

 X = add_constant(df_test[['Close_lag1']])
 y = df_test['Close']
 model = OLS(y, X).fit()

# White test
 white_result = het_white(model.resid, model.model.exog)
 white_pvalue = white_result[1]
 else:
 white_pvalue = None
 except:
 white_pvalue = None
 else:
 white_pvalue = None

# 4. Durbin-Watson test for first order autocratulation
 if len(df) > 10:
 try:
 dw_statistic = durbin_watson(df['Close'].diff().dropna())
 except:
 dw_statistic = None
 else:
 dw_statistic = None

# 5. Shack structural change (simplified version)
# We split the data in half and compare statistics
 if len(df) > 20:
 mid_point = len(df) // 2
 first_half = df['Close'].iloc[:mid_point]
 second_half = df['Close'].iloc[mid_point:]

# Compare averages
 mean_diff = abs(first_half.mean() - second_half.mean())
 std_ratio = first_half.std() / second_half.std() if second_half.std() > 0 else 1

 structural_change = {
 'mean_difference': mean_diff,
 'std_ratio': std_ratio,
 'significant_change': mean_diff > 2 * first_half.std()
 }
 else:
 structural_change = None

 return {
 'adf_statistic': adf_result[0],
 'adf_pvalue': adf_result[1],
 'is_stationary': adf_result[1] < 0.05,
 'ljung_box_pvalue': ljung_box_pvalue,
 'white_pvalue': white_pvalue,
 'durbin_watson': dw_statistic,
 'structural_change': structural_change
 }
```

## Data preservation

### 1. Parket format

**Theory:**Parquet is a column format of files, optimized for analytical workloads; it provides a high level of reading/recording, efficient compression and support of complex data types, making it ideal for financial data.

**Why Parquet is important for financial data:**
- **High performance:** Rapid reading and recording of large amounts of data
- ** Effective compression:** Significant reduction in the size of the fillets
- **Colonel storage:** Optimally for analytical queries
- ** Data flow chart:** Automatic data type retention
- **Compatibility: ** Support for various instruments (Pandas, Spark, etc.)

**Parquet benefits:**

**1. performance:**
- **Colonel storage:** Reading only the right columns
- ** Pre-filtering:** Filtering on file level
- ** Vectorization:** Optimization for modern processors
- ** Cashing:** Effective use of memory

**2. Compression:**
- ** Compression algorithms:** Snappy, Gzip, LZ4, Brotli
- ** Colon compression:** Better compression for similar data
- ** Adaptive compression:** Choice of the best algorithm for each column
- ** Files:** Usually in 5-10 times less than CSV

**3. Data sheet:**
- ** Data Type: ** Automatic retention of types
- **Metadata:** built-in metadata on data
- **Version: ** Support for the evolution of the scheme
- **validation:** sheck types on reading

**4. Comparability:**
- **Pandas:** Nate support
- **Apache Spark:** Optimized support
- **DuckDB:** High performance
- **BigQuery:** Direct download

** Compression patterns in Parquet:**

**1. Snappy (on default):**
- **Speed:** Very fast
- ** Compression:** Moderate
- ** Application:** Interactive queries

**2. Gzip:**
- **Speed:** Slow
- ** Compression:** High
- ** Application:** Archiving

**3. LZ4:**
- **Speed:**
- ♪ Compressing: ♪ Good ♪
- ** Application:** Speed and compression balance

**4. Brotli:**
- **Speed:** Slow
- ** Compression:** Very high
- ** Application:** Long-term storage

**Parquet format plus:**
- High performance
- Effective compression
- Maintenance of data types
- Broad compatibility
- Optimization for analysts

** Parquet format:**
- Complexity for simple cases
-Dependency from libraries
- Limited support in some instruments
- Needs an understanding of format
- Could be redundant for small data

```python
def save_data_parquet(df, filename):
"" Data preservation in Parquet format

This Foundation saves dataFrame in Parket format with optimization
Parket provides a high level of performance.
and effective compression.

 parameters:
- df: DataFrame with data for preservation
- Filename: Path to Save File

Specialities:
- Using Snappy compression for speed and size balance
- Maintains data types and metadata
- Optimized for analytical requests
- Maintains large amounts of data
 """
# Save in Parket format with Snappy compression
# Snappy provides a good balance between speed and compression
 df.to_parquet(filename, compression='snappy')

# Additional options for optimization
 # df.to_parquet(
 # filename,
# selection='snappy', # Rapid compression
# index=True, # Keep the index
# Engine='piarrow', # Use PyArrow engine
# schema = None # Automatic diagram determination
 # )
```

###2. HDF5 format

**Theory:** HDF5 (Hierarchical data Format version 5) is a high-productivity file format designed to store and organize large amounts of data. It provides rapid access to data, efficient metadata compression and support, making it popular for scientific and financial applications.

**Why HDF5 is important for financial data:**
- ** High performance:** Rapid access to large volumes of data
- **Hierarchical Structure:** Data organization in groups and sets
- **Metadata:** Integrated metadata support
- ** Compression:** Effective data compression
- **Cross-platformity:**Working on various operating systems

** HDF5 benefits:**

**1. performance:**
- ** Rapid access:** Optimized access to data
- ** Read on Parts:** Readability only of relevant data
- **Cashing:** In-house caches
- **Parllel access:** Multi-accuracy support

**2. Data organization:**
- **Hierarchical Structure:** Groups and subgroups
- **Metadata:** Data description attributes
- **indexation:** Rapid search
- **Versioning:** Tracking change

**3. Compression:**
- ** Compression algorithms:** Gzip, LZF, SZIP
- ** Adaptive compression: ** Selection of algorithm for each data set
- **Files measurement:** Significant size reduction
- **Speed:** Balance between compression and speed

**4. Comparability:**
- **Python:** H5py, PyTables, Pandas
- **R:** rhdf5
- **MATLAB:** In-house support
- **C/C++:**

** Compressions in HDF5:**

**1. Gzip (on default):**
- **Speed:** Slow
- ** Compression:** High
- ** Application:** Archiving

**2. LZF:**
- **Speed:**
- ** Compression:** Moderate
- ** Application:** Interactive queries

**3. SZIP:**
- **Speed:** Medium
- ** Compression:** High
- ** Application:** Scientific data

**4. No compression:**
- **Speed:** Very fast
- ** Compression:** None
- ** Application:** Temporary data

** Storage records in HDF5:**

**1. Table format:**
- **Structure:** Table Structure
- ** Benefits:** Easy access to strings
- ** Disadvantages:** Slow reading columns
- ** Application:** Time series

**2. Fixed format:**
- **Structure:** Fixed Structure
- ** Benefits:** Quick reading
- ** Disadvantages:** Complexity of change
- ** Application:** Static data

** Plus HDF5 format:**
- High performance
- Hierarchical Organization
- Install Metdata
- Effective compression
Cross-platformity

** HDF5-sized minuses:**
- Complexity for simple cases
-Dependency from libraries
- Limited support in some instruments
- Needs an understanding of format
- Could be redundant for small data

```python
def save_data_hdf5(df, filename):
"" Data preservation in HDF5 format

This finance saves dataFrame in HDF5 format with optimization
HDF5 provides a high level of performance.
and efficient data management.

 parameters:
- df: DataFrame with data for preservation
- Filename: Path to Save File

Specialities:
- Uses a table format for optimizing access
- Saves metadata and attributes.
- Supports data compression
- Provides quick access to data
 """
# Save in HDF5 format with table structure
# table format optimized for time series
 df.to_hdf(filename, 'data', mode='w', format='table')

# Additional options for optimization
 # df.to_hdf(
 # filename,
# 'data', # Group name in HDF5
# mode='w', # Record Mode (w=write, a=append)
#format='table', #Storage format
# complevel=9, # Compression level 0-9
# complib='zlib', # Compress Library
# Fletcher32=True, # check integrity
# Data_columns=True # Columns indexation
 # )
```

## Practical example

```python
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.preprocessing import StandardScaler

def prepare_trading_data(symbol, period='2y'):
"Complete Data for Trading"

 # 1. Loading data
 ticker = yf.Ticker(symbol)
 df = ticker.history(period=period)

 # 2. clean
 df = remove_duplicates(df)
 df = handle_Missing_values(df)
 df = remove_outliers(df)

# 3. the light of the signs
 df = create_Technical_indicators(df)
 df = create_statistical_features(df)
 df = create_time_features(df)

# 4. the target variable
 df['target'] = create_direction_target(df)

 # 5. remove NaN
 df = df.dropna()

# 6. Normalization
 scaler = StandardScaler()
 feature_columns = df.select_dtypes(include=[np.number]).columns
 df[feature_columns] = scaler.fit_transform(df[feature_columns])

 return df, scaler

# Use
data, scaler = prepare_trading_data('BTC-USD')
Print(f"Prepared {len(data)}with {data.chape[1]} imprints)
```

## Next steps

Once the data have been prepared, go to:
- **[04_feature_engineering.md](04_feature_energying.md)** - Signs engineering
- **[05_model_training.md](05_model_training.md)** - Model training

## Key findings

1. **The quality of data** is critical for ML
2. **clean** must be thorough
3. ** Signs** should be relevant
4. **Normation** improves learning
5. **validation** prevents errors

---

** It's important:** Spend time on quality data production - it'll pay off in the long term.
