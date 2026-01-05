# 04. ♪ Signs engineering

**Goal:** Learn to create effective signs for ML models in financial data.

♪ Necessary libraries and imports

**Theory:** Before starting work with the engineering of signs, all necessary libraries must be imported. In financial machine training, we Use specialized libraries for work with time series, technical indicators and statistical calculations.

** Why it's important to set the imports right:**

- **Compatibility:** The right versions of libraries ensure stability
- **Performance:** Optimized libraries accelerate calculations
- **Functionability:** Specialized libraries provide the necessary facilities
- ** Debugging:** Good imports make it easier to find mistakes

```python
# Basic libraries for work with data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Library for Technical Indicators
import talib
from scipy import stats
from scipy.signal import find_peaks

# Library for Machine Learning
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_Report

# Library for Automatic Engineering
import featuretools as ft
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute
import tsfresh.feature_extraction.Settings

# Library for Visualization
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Configuration of display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
plt.style.Use('seaborn-v0_8')
sns.set_palette("husl")

"All libraries are successfully imported!"
print(f"📊 Pandas Version: {pd.__version__}")
print(f"🔢 NumPy Version: {np.__version__}")
print(f"📈 Matplotlib Version: {plt.matplotlib.__version__}")
```

## creative test data

**Theory:** for the demonstration of engineering signs, we need realistic financial data. We will create synthetic data that simulate real market conditions, including trends, volatility, seasonality and noise.

**Why synthetic data is useful:**
- ** Verification:** We know the true pathers in the data
- **Preducibility: ** Results can be repeated
- ** Safety:**not need to use real trade data
- ** Flexibility: ** It is possible to test different scenarios.

```python
def create_sample_trading_data(n_days=1000, start_date='2020-01-01'):
 """
quality of synthetic trade data for the demonstration of engineering features

 parameters:
- n_days: number of data days
- Start_date: starting date

Returns:
- DataFrame with OHLCV data
 """
np.random.seed(42) #for reproduction

# rent temporary index
 dates = pd.date_range(start=start_date, periods=n_days, freq='D')

# Basic parameters
 initial_price = 100.0
trend = 0.0001 # Small upward trend
volatility = 0.02 # 2 % day volatility

# Price generation
 returns = np.random.normal(trend, volatility, n_days)
 prices = initial_price * np.exp(np.cumsum(returns))

# Create OHLCV data
 data = []
 for i, (date, price) in enumerate(zip(dates, prices)):
# add intra-day volatility
 intraday_vol = np.random.uniform(0.005, 0.015)

# Open
 open_price = price * (1 + np.random.normal(0, intraday_vol/2))

# High (maximum day)
 high_price = max(open_price, price) * (1 + np.random.uniform(0, intraday_vol))

# Lowe (minimum day)
 low_price = min(open_price, price) * (1 - np.random.uniform(0, intraday_vol))

# Close (closed day)
 close_price = price

# Volume
 base_volume = 1000000
 volume_multiplier = 1 + np.random.uniform(-0.5, 0.5)
 volume = int(base_volume * volume_multiplier * (1 + abs(returns[i]) * 10))

 data.append({
 'Date': date,
 'Open': round(open_price, 2),
 'High': round(high_price, 2),
 'Low': round(low_price, 2),
 'Close': round(close_price, 2),
 'Volume': volume
 })

 df = pd.dataFrame(data)
 df.set_index('Date', inplace=True)

# add seasonality (e.g. weekly patterns)
 df['DayOfWeek'] = df.index.dayofweek
 weekly_effect = np.sin(2 * np.pi * df['DayOfWeek'] / 7) * 0.01
 df['Close'] = df['Close'] * (1 + weekly_effect)

 return df

# Create testy data
print("\create synthetic trade data...")
sample_data = create_sample_trading_data(n_days=1000)
Print(f)\\\\\\en(sample_data}}days of data}
(sample_data.index[0].strftime('%Y-%m-%d')} - {sample_data.index[-1].strftime('%Y-%m-%d'}})
Price: {sample_data['Close'].iloc[0]:.2f} \\sample_data['Close']iloc[-1]:2f}}
average volume: {sample_data['Volume']mean(:,0f}})
The first five rows of data:
print(sample_data.head())
```

♪ What is sign engineering?

**Theory:** Significance engineering is a fundamental process in machine learning, which consists in creating, transforming and selecting signs for improving performance of ML models. In the financial sphere, this is particularly critical because the quality of the signs directly affects the accuracy of trade signals.

** Signs engineering** is a process of creating new indicators from existing data for improving performance of ML models.

**Why engineering is critical for financial systems:**
- ** Financial data are complex:** Require special processing for the identification of pathers
- ** High risks:** Bad signs can cause significant losses
- ** Competition advantage:** Qualitative features give an advantage on the market
- ** Regulatory requirements:** Financial regulators require transparency of features

♪ ♪ Why does it matter?

**Theory:** The quality of the indicators is the determining factor for the success of ML models. Studies show that qualitative indicators can improve model performance more than increasing the amount of data or complexity of the algorithm.

- ** Quantity of indicators** > ** Quantity of data**
- ** Why:** Good signs contain more information about target variable
- ** Plus:** Better use of data, better interpretation
- **Disadvantages:** Requires expertise, more time on development

- ** Regulatory signs** can double model accuracy
- **Why:** Relevant indicators are directly related with target variable
- ** Plus:** Substantial improve performance, risk reduction
- **Disadvantages:**Complicity of defining relevant topics

- ** Bad signs** can ruin even the best algorithms.
- ♪ Why: ♪ The noise in the signature transmits into the model and makes it worse ♪
- **plus:** Understanding the importance of data quality
- **Disadvantages:** Need for careful validation of features

** Additional aspects of importance:**
- ** Interpretation:** Good signs are easy to interpret
- **Stability:** Qualitative signs stable over time
- **Scalability:** Good signs Working on different data
- **Purity:** Qualitative signs resistant to emissions

## Types of signs

**Theory:** Signs in financial ML models can be classified on different criteria. Understanding the types of indicators is critical for effective models and error prevention.

♪## 1. Technical indicators

**Theory:**Technical indicators are mathematical transformations of price data that help to identify patterns and trends, based on years of experience of technical analysts, and are the standard in the financial industry.

**Why the Technical Indicators are important:**
- **Sureness of time:** Multi-year experience
- ** Standardization:** Universal metrics for Analysis
- ** Interpretation: ** Easily understood and explained
- ** Effectiveness: ** Proven efficiency in trade

**Typs of technical indicators:**
- **Trend:** SMA, EMA, MACD - show direction of trend
- **Oscillators:** RSI, Stochastic - indicate oversizing/resellability
- ** Volatility:** Bollinger Bands, ATR - show volatility
- ** Unit:** OBV, VWAP - account for tender volume

** Plus technical indicators:**
- Tested efficiency
- Standardized metrics
Easy interpretation.
- Broad support in instruments

**Mine of technical indicators:**
- Could be late.
- Could generate false signals.
- It requires Settings parameters.
- May be excessive.
```python
def calculate_rsi(prices, window=14):
 """
Calculation of the Real Strangth Index (RSI)

Theory: RSI is an oscillator that measures the speed and change of price movements.
Values from 0 to 100 where:
- RSI > 70: Oversizing (may turn downward)
- RSI < 30: resellability (upturn possible)
- RSI = 50: neutral zone

Formula: RSI = 100 - (100 / (1 + RS))
where RS = average increase / average loss over the period

 parameters:
- Prices: Closing price series
- Windows: Calculation period (on default 14)

Returns:
- Series with RSI values
 """
 delta = prices.diff()
 gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
 loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

# Avoid division on zero
 rs = gain / loss.replace(0, np.inf)
 rsi = 100 - (100 / (1 + rs))

 return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
 """
MACD Calculation

Theory: MACD is a trend indicator that shows the connection between two
It consists of three components:
- MACD line: EMA(fast) - EMA(slow)
- Signal line: EMA(MACD)
 - Histogram: MACD - signal

Signal:
- Intersection of MACD and signal: trend change
- Divergence: the difference between price and MACD
- Zero line: intersection indicates on change of trend

 parameters:
- Prices: Closing price series
- fast: fast EMA period (on default 12)
- slow: slow period EMA (on default 26)
- signal: signal line period (on default 9)

Returns:
 - tuple: (macd_line, signal_line, histogram)
 """
 ema_fast = prices.ewm(span=fast).mean()
 ema_slow = prices.ewm(span=slow).mean()
 macd_line = ema_fast - ema_slow
 signal_line = macd_line.ewm(span=signal).mean()
 histogram = macd_line - signal_line

 return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, window=20, num_std=2):
 """
Calculation of Bollinger Bands strips

Theory: Bollinger's hair consists of three lines:
- Middle line: SMA(period)
- Upper stripe: SMA + (std*num_std)
- Lower stripe: SMA - (std*num_std)

Use of:
- The price is on the top lane: possible turn-down.
- The price goes to the bottom: possible turning up.
- Strip compression: low volatility, possible breakthrough
- Extension of lanes: high volatility

 parameters:
- Prices: Closing price series
- Windows: period for SMA (on default 20)
- number_std: number of standard deviations (on default 2)

Returns:
 - tuple: (upper_band, lower_band, middle_band)
 """
 middle_band = prices.rolling(window=window).mean()
 std = prices.rolling(window=window).std()
 upper_band = middle_band + (std * num_std)
 lower_band = middle_band - (std * num_std)

 return upper_band, lower_band, middle_band

def calculate_stochastic(high, low, close, k_window=14, d_window=3):
 """
Calculation of the stochastic oscillator

Theory: Stochastic measures the current price position relative to range
It consists of two lines:
 - %K: (Close - Lowest Low) / (Highest High - Lowest Low) * 100
-%D: SMA(%K) - smooth version %K

Interpretation:
- %K > 80: over-storage
- %K < 20: resold
- Intersection %K and %D: Trade signals

 parameters:
- High: Maximum Price Series
- Low: Minimum Price Series
- lose: Series of closing prices
- k_window: period for %K (on default 14)
- d_window: period for %D (on default 3)

Returns:
 - tuple: (stoch_k, stoch_d)
 """
 lowest_low = low.rolling(window=k_window).min()
 highest_high = high.rolling(window=k_window).max()

 stoch_k = ((close - lowest_low) / (highest_high - lowest_low)) * 100
 stoch_d = stoch_k.rolling(window=d_window).mean()

 return stoch_k, stoch_d

def calculate_atr(high, low, close, window=14):
 """
Calculation of Average True Range (ATR)

Theory: ATR measures market volatility by showing average range
Use for:
- Definitions of stop-loss size
- Volatility estimates
- Weak signal filtering

 True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
 ATR = SMA(True Range)

 parameters:
- High: Maximum Price Series
- Low: Minimum Price Series
- lose: Series of closing prices
- Windows: period for SMA (on default 14)

Returns:
- Series with ATR values
 """
 tr1 = high - low
 tr2 = abs(high - close.shift(1))
 tr3 = abs(low - close.shift(1))

 tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
 atr = tr.rolling(window=window).mean()

 return atr

def create_Technical_indicators(df):
 """
full set of technical indicators

Theory: Technical indicators help to identify patharies in price data
And generate trade signals. We're Creating a variety of indicators for
Covering different aspects of market behaviour:
- Trend indicators (SMA, EMA, MACD)
- RSI, Stochastic
- Volatility (Bollinger Bands, ATR)
- Volumetric (OBV)

 parameters:
- df: DataFrame with OHLCV data

Returns:
- DataFrame with added technical indicators
 """
"preint("\create technical indicators...")

 # RSI (Relative Strength index)
 df['RSI'] = calculate_rsi(df['Close'])
 df['RSI_oversold'] = (df['RSI'] < 30).astype(int)
 df['RSI_overbought'] = (df['RSI'] > 70).astype(int)

 # MACD (Moving Average Convergence Divergence)
 macd_line, signal_line, histogram = calculate_macd(df['Close'])
 df['MACD'] = macd_line
 df['MACD_signal'] = signal_line
 df['MACD_Histogram'] = histogram
 df['MACD_Bullish'] = (macd_line > signal_line).astype(int)
 df['MACD_Bearish'] = (macd_line < signal_line).astype(int)

 # Bollinger Bands
 bb_upper, bb_lower, bb_middle = calculate_bollinger_bands(df['Close'])
 df['BB_Upper'] = bb_upper
 df['BB_lower'] = bb_lower
 df['BB_Middle'] = bb_middle
 df['BB_Width'] = (bb_upper - bb_lower) / bb_middle
 df['BB_Position'] = (df['Close'] - bb_lower) / (bb_upper - bb_lower)
 df['BB_Squeeze'] = (df['BB_Width'] < df['BB_Width'].rolling(20).mean()).astype(int)

 # Stochastic Oscillator
 stoch_k, stoch_d = calculate_stochastic(df['High'], df['Low'], df['Close'])
 df['Stoch_K'] = stoch_k
 df['Stoch_D'] = stoch_d
 df['Stoch_Oversold'] = (stoch_k < 20).astype(int)
 df['Stoch_Overbought'] = (stoch_k > 80).astype(int)

 # ATR (Average True Range)
 df['ATR'] = calculate_atr(df['High'], df['Low'], df['Close'])
 df['ATR_Percentile'] = df['ATR'].rolling(100).rank(pct=True)

 # Simple Moving Averages
 for window in [5, 10, 20, 50, 200]:
 df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']

 # Exponential Moving Averages
 for window in [5, 10, 20, 50]:
 df[f'EMA_{window}'] = df['Close'].ewm(span=window).mean()
 df[f'Price_vs_EMA_{window}'] = df['Close'] / df[f'EMA_{window}']

 # On-Balance Volume (OBV)
 df['OBV'] = (df['Volume'] * np.where(df['Close'] > df['Close'].shift(1), 1,
 np.where(df['Close'] < df['Close'].shift(1), -1, 0))).cumsum()

 # Williams %R
 df['Williams_R'] = ((df['High'].rolling(14).max() - df['Close']) /
 (df['High'].rolling(14).max() - df['Low'].rolling(14).min())) * -100

 # Commodity Channel index (CCI)
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 sma_tp = typical_price.rolling(20).mean()
 mad = typical_price.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())))
 df['CCI'] = (typical_price - sma_tp) / (0.015 * mad)

nint(f) is created {len([col for col in df.columns if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'DayOfWeek']]]}} technical indicators)

 return df

# Demonstration of the creation of technical indicators
print("\n" + "="*60)
"Prent("\Demonstration: creative technical indicators")
print("="*60)

# creative indicators for test data
df_with_indicators = create_Technical_indicators(sample_data.copy())

# Showing statistics on indicators
(f) Statistics on main indicators:)
print(f"RSI: {df_with_indicators['RSI'].mean():.2f} ± {df_with_indicators['RSI'].std():.2f}")
print(f"MACD: {df_with_indicators['MACD'].mean():.4f} ± {df_with_indicators['MACD'].std():.4f}")
print(f"BB Position: {df_with_indicators['BB_Position'].mean():.3f} ± {df_with_indicators['BB_Position'].std():.3f}")
print(f"Stochastic K: {df_with_indicators['Stoch_K'].mean():.2f} ± {df_with_indicators['Stoch_K'].std():.2f}")

# Showing the signals
(the last 5 days):)
recent_signals = df_with_indicators[['RSI_oversold', 'RSI_overbought', 'MACD_Bullish',
 'MACD_Bearish', 'Stoch_Oversold', 'Stoch_Overbought']].tail()
print(recent_signals)
```

###2: Statistical indicators

**Theory:** Statistical indicators are based on the mathematical properties of the data and help identify hidden patterns. They are particularly useful for ML models because they are based on statistical principles.

** Why the statistical signs matter:**
- ** Mathematical validity:** Based on statistical principles
- ** Universality:** Working on different types of data
- ** Interpretation: ** Easily understood and explained
- **Stability:** Less exposed to noise

**Schedule of statistical indicators:**
- ** Allocation periods:** Medium, dispersion, asymmetrical, extruded
- **Quantile:** Median, quartili, percentili
- **Correlations:** Linear and non-liner dependencies
- **According:**dependences over time

** Plus of statistical indicators:**
- Mathematical validity
Universality of application
Easy interpretation.
- Stability to noise

**Mine of statistical characteristics:**
- Could be less specific.
- Sufficient data required
- May not take into account the specifics of financial data
- May be excessive.
```python
def create_statistical_features(df):
 """
statistical indicators for financial data

Theory: Statistical indicators are based on the mathematical properties of data
And help identify hidden patterns. They're particularly useful for ML models.
Because they are based on statistical principles and less exposed to noise.

Types of statistical indicators:
1. Times of distribution (medium, dispersion, asymmetricality, excess)
2. Quantiles (mediana, quartili, per centili)
3. Correlations (line and non-liner dependencies)
4. Auto-correlations (dependences over time)
5. Rolling statistics (average, standard deviation)

 parameters:
- df: DataFrame with OHLCV data

Returns:
- DataFrame with added statistical signature
 """
"preint("\create statistics...")

1. Rolling average (various periods)
 for window in [5, 10, 20, 50, 100]:
 df[f'SMA_{window}'] = df['Close'].rolling(window).mean()
 df[f'EMA_{window}'] = df['Close'].ewm(span=window).mean()

# Price ratio to moving average
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']
 df[f'Price_vs_EMA_{window}'] = df['Close'] / df[f'EMA_{window}']

# Deviation from sliding average
 df[f'Deviation_SMA_{window}'] = (df['Close'] - df[f'SMA_{window}']) / df[f'SMA_{window}']
 df[f'Deviation_EMA_{window}'] = (df['Close'] - df[f'EMA_{window}']) / df[f'EMA_{window}']

# 2. Volatility (various periods)
 for window in [5, 10, 20, 50]:
 df[f'Volatility_{window}'] = df['Close'].rolling(window).std()
 df[f'Volatility_Annualized_{window}'] = df[f'Volatility_{window}'] * np.sqrt(252)

# Relative volatility
 df[f'Rel_Volatility_{window}'] = df[f'Volatility_{window}'] / df[f'SMA_{window}']

# Volatility of volatility
 df[f'Vol_of_Vol_{window}'] = df[f'Volatility_{window}'].rolling(window).std()

# 3. Times of distribution
 for window in [10, 20, 50]:
# Asymmetry (skewness) - asymmetrical distribution measure
 df[f'Skewness_{window}'] = df['Close'].rolling(window).skew()

# Excess (curtosis) is a measure of "almost" distribution
 df[f'Kurtosis_{window}'] = df['Close'].rolling(window).kurt()

# Media
 df[f'Median_{window}'] = df['Close'].rolling(window).median()

# Price to median ratio
 df[f'Price_vs_Median_{window}'] = df['Close'] / df[f'Median_{window}']

# 4. Quantiles and percentages
 for window in [20, 50]:
 for percentile in [25, 50, 75, 90, 95]:
 df[f'Percentile_{percentile}_{window}'] = df['Close'].rolling(window).quantile(percentile/100)

# Price position relative to percentiles
 df[f'Position_P{percentile}_{window}'] = (df['Close'] - df[f'Percentile_{percentile}_{window}']) / df[f'Percentile_{percentile}_{window}']

#5 Momentum and Rate of Change
 for period in [1, 2, 5, 10, 20]:
# Simple changes
 df[f'Price_Change_{period}'] = df['Close'] - df['Close'].shift(period)
 df[f'Price_Change_Pct_{period}'] = df['Close'].pct_change(period)

# Logarithmic changes (more stable)
 df[f'Log_Return_{period}'] = np.log(df['Close'] / df['Close'].shift(period))

# Momentum (ratio of current price to N periods back)
 df[f'Momentum_{period}'] = df['Close'] / df['Close'].shift(period)

 # Rate of Change (ROC)
 df[f'ROC_{period}'] = ((df['Close'] - df['Close'].shift(period)) / df['Close'].shift(period)) * 100

# 6. Autocorrelations (dependences over time)
 for lag in [1, 2, 5, 10]:
 df[f'Autocorr_{lag}'] = df['Close'].rolling(50).apply(
 lambda x: x.autocorr(lag=lag) if len(x) > lag else np.nan
 )

# 7. Rolling maximums and minimums
 for window in [10, 20, 50]:
 df[f'Max_{window}'] = df['High'].rolling(window).max()
 df[f'Min_{window}'] = df['Low'].rolling(window).min()

# Price position in range
 df[f'Position_in_Range_{window}'] = (df['Close'] - df[f'Min_{window}']) / (df[f'Max_{window}'] - df[f'Min_{window}'])

# Distance to maximum and minimum
 df[f'Distance_to_Max_{window}'] = (df[f'Max_{window}'] - df['Close']) / df['Close']
 df[f'Distance_to_Min_{window}'] = (df['Close'] - df[f'Min_{window}']) / df['Close']

#8 Volume statistics
 for window in [5, 10, 20]:
 df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window).mean()
 df[f'Volume_Std_{window}'] = df['Volume'].rolling(window).std()
 df[f'Volume_vs_Avg_{window}'] = df['Volume'] / df[f'Volume_SMA_{window}']

# Volume-weighted prices
 df[f'VWAP_{window}'] = (df['Close'] * df['Volume']).rolling(window).sum() / df['Volume'].rolling(window).sum()
 df[f'Price_vs_VWAP_{window}'] = df['Close'] / df[f'VWAP_{window}']

#9.Speed statistics (High - Low)
 for window in [5, 10, 20]:
 df[f'Range_{window}'] = (df['High'] - df['Low']).rolling(window).mean()
 df[f'Range_Std_{window}'] = (df['High'] - df['Low']).rolling(window).std()
 df[f'Range_vs_Price_{window}'] = df[f'Range_{window}'] / df['Close']

#10.Z-speed (standardization)
 for window in [20, 50]:
 rolling_mean = df['Close'].rolling(window).mean()
 rolling_std = df['Close'].rolling(window).std()
 df[f'Z_Score_{window}'] = (df['Close'] - rolling_mean) / rolling_std

# Absolute Z-soon
 df[f'Abs_Z_Score_{window}'] = np.abs(df[f'Z_Score_{window}'])

#11. Statistics of change (changes)
 for period in [1, 2, 5]:
 df[f'Change_of_Change_{period}'] = df['Close'].pct_change().pct_change(period)
 df[f'acceleration_{period}'] = df['Close'].diff().diff(period)

# 12. Rolling correlations
 for window in [20, 50]:
# Correlation between price and volume
 df[f'Price_Volume_Corr_{window}'] = df['Close'].rolling(window).corr(df['Volume'])

# Correlation between price and volatility
 df[f'Price_Vol_Corr_{window}'] = df['Close'].rolling(window).corr(df[f'Volatility_20'])

spring(f) is created {len([coll for col in df.columns if 'SMA_' in cool or 'Volatility_' in cool or 'Momentum_' in cool or 'ROC_' in cool or 'Skewness_' in cool or 'Kurtosis_' in cool or 'Percentile_' in cool or 'Autocorr_' in cool or 'Z_Score_' in cool]}}

 return df

# Demonstration of the creation of statistical indicators
print("\n" + "="*60)
"Prent("~ DEMONSTRUCTION: statistical profile")
print("="*60)

# statistical features
df_with_stats = create_statistical_features(sample_data.copy())

# Showing statistics on basic signature
(f) \n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)
Spring(f" Volatility (20 days): {df_with_stats['Volatility_20'].mean(:4f}{df_with_stats['Volatility_20'].std(:4f}})
Print(f"Z-Score (20 days): {df_with_stats['Z_Score_20'].mean(:3f}{df_with_stats['Z_Score_20'].std(:.3f}})
asymmetry (20 days): {df_with_stats['Skewness_20'].mean(:3f}{df_with_stats['Skewness_20'].std(:3f}})
print(f"Excess (20 days): {df_with_stats['Kurtosis_20'].mean(:3f}{df_with_stats['Kurtosis_20'].std(:3f}})

# Showing examples of signs
prent(f)\n\examples statistical signs (last 5 days):)
stats_examples = df_with_stats[['Volatility_20', 'Z_Score_20', 'Skewness_20', 'Position_in_Range_20', 'Price_Volume_Corr_20']].tail()
print(stats_examples)
```

♪##3 ♪ Time signs ♪

**Theory:** Time indicators take into account the temporal structure of the data and help to identify time-related variables that are critical for financial data that have a strong time dependency.

** Why the time signs matter:**
- ** Time-dependency:** Financial data is highly dependent from time
- ** Seasonality:** Many pathites repeat in time
- **Trends:** Temporary signs help to identify trends
- **Cycles:** Financial markets have cyclical patterns

**Tips of time signs:**
- **Lags:** Values in previous times
- ** Varieties: ** Changes between times
- ** Sliding windows:** Statistics in time windows
- ** Seasonal:** Signs related to seasonality

** Plus temporary features:**
- Accounting for the temporary structure
- Identification of seasonal pathers
- improve prognosis capacity
- Better understanding of data

**Measures of time:**
- May cause data leaks
- They need caution when they're validating.
- May be excessive.
- Complexity of interpretation
```python
def create_time_features(df):
 """
time-marks for financial data

Theory: Time signs take into account the temporal structure of the data and help
They're critical for financial data.
which have a strong temporary dependency.

Types of time signs:
1. Legs (lag features) - values in previous times
2. Varieties - changes between times
3. Rolling windows - statistics in time windows
4. Seasonal characteristics - with seasonality
5. Cyclic signs - for the accounting of cycles
6. Trend indicators - for trend identification

 parameters:
- df: DataFrame with OHLCV data and Datameindex

Returns:
- DataFrame with added temporary subscriptions
 """
"preint("\\create time signs...")

# 1. Legi (lag features) - values in previous times
 for lag in [1, 2, 3, 5, 10, 20, 50]:
 df[f'Close_lag_{lag}'] = df['Close'].shift(lag)
 df[f'Volume_lag_{lag}'] = df['Volume'].shift(lag)
 df[f'High_lag_{lag}'] = df['High'].shift(lag)
 df[f'Low_lag_{lag}'] = df['Low'].shift(lag)

# Relationship to the lagoons
 df[f'Close_vs_lag_{lag}'] = df['Close'] / df[f'Close_lag_{lag}']
 df[f'Volume_vs_lag_{lag}'] = df['Volume'] / df[f'Volume_lag_{lag}']

# 2. Differentials - changes between times
 for diff in [1, 2, 5, 10, 20]:
 df[f'Close_diff_{diff}'] = df['Close'].diff(diff)
 df[f'Volume_diff_{diff}'] = df['Volume'].diff(diff)
 df[f'High_diff_{diff}'] = df['High'].diff(diff)
 df[f'Low_diff_{diff}'] = df['Low'].diff(diff)

# Normalized differences
 df[f'Close_diff_norm_{diff}'] = df[f'Close_diff_{diff}'] / df['Close'].shift(diff)
 df[f'Volume_diff_norm_{diff}'] = df[f'Volume_diff_{diff}'] / df['Volume'].shift(diff)

# 3. Percentage changes
 for period in [1, 2, 5, 10, 20]:
 df[f'Close_pct_{period}'] = df['Close'].pct_change(period)
 df[f'Volume_pct_{period}'] = df['Volume'].pct_change(period)
 df[f'High_pct_{period}'] = df['High'].pct_change(period)
 df[f'Low_pct_{period}'] = df['Low'].pct_change(period)

# Logarithmic changes (more stable)
 df[f'Close_log_{period}'] = np.log(df['Close'] / df['Close'].shift(period))
 df[f'Volume_log_{period}'] = np.log(df['Volume'] / df['Volume'].shift(period))

# 4. Rolling windows - statistics in time windows
 for window in [5, 10, 20, 50]:
# Sliding average
 df[f'Close_MA_{window}'] = df['Close'].rolling(window).mean()
 df[f'Volume_MA_{window}'] = df['Volume'].rolling(window).mean()

# Slipping standard deviations
 df[f'Close_Std_{window}'] = df['Close'].rolling(window).std()
 df[f'Volume_Std_{window}'] = df['Volume'].rolling(window).std()

# Rolling minimums and maximums
 df[f'Close_Min_{window}'] = df['Close'].rolling(window).min()
 df[f'Close_Max_{window}'] = df['Close'].rolling(window).max()
 df[f'Volume_Min_{window}'] = df['Volume'].rolling(window).min()
 df[f'Volume_Max_{window}'] = df['Volume'].rolling(window).max()

# Position in sliding window
 df[f'Close_Position_{window}'] = (df['Close'] - df[f'Close_Min_{window}']) / (df[f'Close_Max_{window}'] - df[f'Close_Min_{window}'])
 df[f'Volume_Position_{window}'] = (df['Volume'] - df[f'Volume_Min_{window}']) / (df[f'Volume_Max_{window}'] - df[f'Volume_Min_{window}'])

♪ 5. Seasonal signs - with seasonality
 if hasattr(df.index, 'hour'):
# An hour of day (for in-day data)
 df['Hour'] = df.index.hour
 df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
 df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)

# Day of the week
 df['DayOfWeek'] = df.index.dayofweek
 df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
 df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

# Day of the month
 df['DayOfMonth'] = df.index.day
 df['DayOfMonth_sin'] = np.sin(2 * np.pi * df['DayOfMonth'] / 31)
 df['DayOfMonth_cos'] = np.cos(2 * np.pi * df['DayOfMonth'] / 31)

# Month
 df['Month'] = df.index.month
 df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
 df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

# Quarter
 df['Quarter'] = df.index.quarter
 df['Quarter_sin'] = np.sin(2 * np.pi * df['Quarter'] / 4)
 df['Quarter_cos'] = np.cos(2 * np.pi * df['Quarter'] / 4)

# Day of the year
 df['DayOfYear'] = df.index.dayofyear
 df['DayOfYear_sin'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
 df['DayOfYear_cos'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)

# 6. Cyclic signs - to account for cycles
# Weekly cycles
 df['WeekOfYear'] = df.index.isocalendar().week
 df['WeekOfYear_sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
 df['WeekOfYear_cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)

# 7. Trend signs - for trend identification
# Linear trend
 for window in [20, 50, 100]:
 df[f'Trend_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )

# R-square of trend
 df[f'Trend_R2_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

# 8. Time interval
# Days with the last maximum/minimum
 for window in [20, 50]:
 df[f'Days_Since_High_{window}'] = df['Close'].rolling(window).apply(
 lambda x: len(x) - 1 - x.argmax() if len(x) == window else np.nan
 )
 df[f'Days_Since_Low_{window}'] = df['Close'].rolling(window).apply(
 lambda x: len(x) - 1 - x.argmin() if len(x) == window else np.nan
 )

♪ 9. Temporary Paterns
# Number of consecutive days of growth/fall
 df['Consecutive_Up'] = (df['Close'] > df['Close'].shift(1)).groupby(
 (df['Close'] > df['Close'].shift(1) != (df['Close'] > df['Close'].shift(1)).shift()).cumsum()
 ).cumsum()

 df['Consecutive_Down'] = (df['Close'] < df['Close'].shift(1)).groupby(
 (df['Close'] < df['Close'].shift(1) != (df['Close'] < df['Close'].shift(1)).shift()).cumsum()
 ).cumsum()

#10. Temporary statistics
# Sliding correlations with time
 for window in [20, 50]:
 df[f'Time_Corr_{window}'] = df['Close'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1] if len(x) == window else np.nan
 )

#11. Temporary indicators
# Whether the day is the end of the week/month/quarter
 df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
 df['Is_Month_End'] = (df.index.is_month_end).astype(int)
 df['Is_Quarter_End'] = (df.index.is_quarter_end).astype(int)
 df['Is_Year_End'] = (df.index.is_year_end).astype(int)

# 12. Time differences (various time points)
# The difference between the current and the previous day of the week
 df['DayOfWeek_Diff'] = df['DayOfWeek'].diff()

# The difference between the current month and the previous month
 df['Month_Diff'] = df['Month'].diff()

is created {len([coll for col in df.columns if 'lag_' in cool or 'diff_' in col or 'pct_' in col or 'MA_' in col or 'sin' in cool or 'cos' in cool or 'Trend_' in cool or 'Consecutive_' in cool or 'Is_' in coll]}}time signs}

 return df

# Demonstration of the creation of time signs
print("\n" + "="*60)
"Prent("♪ DEMONSTRUCTION: temporary signs")
print("="*60)

# the time sign
df_with_time = create_time_features(sample_data.copy())

# Showing statistics on basic time signature
pint(f)\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)})}\\\\\\\\\\\)}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)})})})})}) \\\)})}) \\\\\\\\\\\\\\\\\\\\\\\\\)})}=========)}===========)})})})})//((((((((((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)})})})})})})})})})})})
Print(f" Weekday (average): {df_with_time['DayOfWeek']mean(:2f}})
pint(f"Mean (average): {df_with_time['Month'].mean(:2f}})
print(f" Quarterly (average): {df_with_time['Quarter'].mean(:2f}})

# Showing examples of time signs
(the last five days):)
time_examples = df_with_time[['DayOfWeek', 'Month', 'Close_lag_1', 'Close_pct_1', 'Close_MA_20', 'Trend_20']].tail()
print(time_examples)
```

♪## 4. Interactive signs

**Theory:** Interactive features are created by combining existing features and helping to identify complex non-liner dependencies. They are particularly important for financial data, where many pathites are the result of the interaction of different factors.

**Why interactive signs are important:**
- **Nelina dependencies:** Financial data often have non-linear dependencies
- ** Synergy: ** A combination of topics can provide more information
- ** Context:** Interactive topics take into account context
- **Complicity: ** Helps to model complex pathers

**Tips of interactive features:**
- ** Productions:** Multiplies
- ** Relationships: **
- **Staffs:** Creation in degree
- **Logs:** Logs

** Plus interactive features:**
- Identification of non-linear dependencies
- improve prognosis capacity
- Consideration of context
- More complete modelling

**Minuses of interactive features:**
- May create excess
- Complexity of interpretation
- Risk retraining
- High computing costs
```python
def create_interaction_features(df):
 """
on-line indicators for financial data

Theory: Interactive features are created by combining existing
They help to identify complex non-linear dependencies.
are important for financial data, where many pathologies are the result
The interaction of different factors.

Types of interactive features:
1. Productions - Multipliers
2. Relationships - division of topics
3. Stepeni - In-degree construction
4. Logs - Logs
5. Polynomial - combination of degrees
6. Conditional - signs on basis of conditions

 parameters:
- df: DataFrame with basic signature

Returns:
- DataFrame with added interactive signature
 """
"preint("\create interactive signs...")

# 1. Signs (multiplicative interactions)
# RSI * MACD - combination of oscillator and trend indicator
 if 'RSI' in df.columns and 'MACD' in df.columns:
 df['RSI_MACD'] = df['RSI'] * df['MACD']
 df['RSI_MACD_signal'] = df['RSI'] * df['MACD_signal']

# Volume * Price Change - Volume-weighted price changes
 df['Volume_Price_Change'] = df['Volume'] * df['Close'].pct_change()
 df['Volume_Price_Change_2'] = df['Volume'] * df['Close'].pct_change(2)

♪ 2. Signal relationships (different interactions)
# Band Position - price position in stripes
 if 'BB_Upper' in df.columns and 'BB_lower' in df.columns:
 df['BB_Position'] = (df['Close'] - df['BB_lower']) / (df['BB_Upper'] - df['BB_lower'])
 df['BB_Squeeze_Intensity'] = df['BB_Width'] / df['Close']

# Price vs Moving Overages - Price ratio to moving average
 for window in [20, 50, 200]:
 if f'SMA_{window}' in df.columns:
 df[f'Price_vs_SMA_{window}'] = df['Close'] / df[f'SMA_{window}']
 df[f'Price_vs_SMA_{window}_squared'] = (df[f'Price_vs_SMA_{window}'] - 1) ** 2

# 3. Stepenal signs (polynomial interactions)
# Quadrates of main indicators
 if 'RSI' in df.columns:
 df['RSI_squared'] = df['RSI'] ** 2
 df['RSI_cubed'] = df['RSI'] ** 3
 df['RSI_sqrt'] = np.sqrt(df['RSI'])

 if 'MACD' in df.columns:
 df['MACD_squared'] = df['MACD'] ** 2
 df['MACD_abs'] = np.abs(df['MACD'])

# 4. Logistic combinations
# Combination of purchase/reselling conditions
 if 'RSI' in df.columns:
 df['RSI_Stoch_Overbought'] = ((df['RSI'] > 70) & (df['Stoch_K'] > 80)).astype(int)
 df['RSI_Stoch_Oversold'] = ((df['RSI'] < 30) & (df['Stoch_K'] < 20)).astype(int)

# Combinations of trend signals
 if all(col in df.columns for col in ['SMA_20', 'SMA_50', 'SMA_200']):
 df['all_MA_Bullish'] = ((df['Close'] > df['SMA_20']) &
 (df['SMA_20'] > df['SMA_50']) &
 (df['SMA_50'] > df['SMA_200'])).astype(int)

 df['all_MA_Bearish'] = ((df['Close'] < df['SMA_20']) &
 (df['SMA_20'] < df['SMA_50']) &
 (df['SMA_50'] < df['SMA_200'])).astype(int)

♪ 5. Conditional signs
# Signs on baseline volatility
 if 'Volatility_20' in df.columns:
 high_vol_mask = df['Volatility_20'] > df['Volatility_20'].rolling(50).quantile(0.8)
 df['High_Vol_RSI'] = df['RSI'].where(high_vol_mask, 0)
 df['Low_Vol_RSI'] = df['RSI'].where(~high_vol_mask, 0)

# 6. Temporary interactions
# The interaction with day of the week
 if 'DayOfWeek' in df.columns:
 df['RSI_Weekend'] = df['RSI'] * (df['DayOfWeek'] >= 5).astype(int)
 df['Volume_Weekend'] = df['Volume'] * (df['DayOfWeek'] >= 5).astype(int)

#7. Cruise-price interactions
# Volume-weighted indicators
 if 'Volume' in df.columns:
 df['Volume_Weighted_RSI'] = df['RSI'] * (df['Volume'] / df['Volume'].rolling(20).mean())
 df['Volume_Weighted_MACD'] = df['MACD'] * (df['Volume'] / df['Volume'].rolling(20).mean())

# 8. Polynomial signs
# RSI interaction with its lagoons
 if 'RSI' in df.columns:
 for lag in [1, 2, 5]:
 df[f'RSI_lag_{lag}'] = df['RSI'].shift(lag)
 df[f'RSI_RSI_lag_{lag}'] = df['RSI'] * df[f'RSI_lag_{lag}']
 df[f'RSI_minus_lag_{lag}'] = df['RSI'] - df[f'RSI_lag_{lag}']

#9 Statistical interactions
# Interacting with Z-Speed
 if 'Z_Score_20' in df.columns:
 df['RSI_Z_Score'] = df['RSI'] * df['Z_Score_20']
 df['MACD_Z_Score'] = df['MACD'] * df['Z_Score_20']

# 10. Complex combinations
# Combination of trend, volatility and volume
 if all(col in df.columns for col in ['Trend_20', 'Volatility_20', 'Volume']):
 df['Trend_Vol_Volume'] = (df['Trend_20'] * df['Volatility_20'] *
 (df['Volume'] / df['Volume'].rolling(20).mean()))

# RSI, MACD and Bollinger Bands
 if all(col in df.columns for col in ['RSI', 'MACD', 'BB_Position']):
 df['RSI_MACD_BB'] = df['RSI'] * df['MACD'] * df['BB_Position']
 df['RSI_MACD_BB_norm'] = df['RSI_MACD_BB'] / df['RSI_MACD_BB'].rolling(20).std()

nint(f) is created {len([col for col in df.columns if any(x in col for x in ['_', 'Weighted', 'Combined', 'Interaction'])]} interactive signs")

 return df

# Demonstration of interactive features
print("\n" + "="*60)
"Prent("♪ DEMONSTRUCTION: cut interactive signs")
print("="*60)

# of interactive features
df_with_interactions = create_interaction_features(df_with_time.copy())

# Showing statistics on interactive signature
(f) Statistics on interactive signature:)
interaction_cols = [col for col in df_with_interactions.columns if any(x in col for x in ['_', 'Weighted', 'Combined', 'Interaction'])]
pprint(f) Created interactive features: {len(interaction_cols)}}

# Show examples of interactive features
pprint(f)(n\n\examples interactive signs (last 5 days):)
interaction_examples = df_with_interactions[['RSI_MACD', 'BB_Position', 'Price_vs_SMA_20', 'Volume_Weighted_RSI', 'RSI_Stoch_Overbought']].tail()
print(interaction_examples)
```

## Specialized features for trade

**Theory:** Specialized trade features are based on the patterns and strategies used by professional traders, which encode market wisdom and time-tested trade concepts.

**Why specialized features are important:**
- **Sureness of time:** Based on years of experience of traders
- ** Interpretation: ** Easily understood and explained
- ** Effectiveness: ** Proven efficiency in real trade
- ** Context: ** Address the specificities of financial markets

♪##1 ♪ Price parters

**Theory:** Price patches are graphical shapes that are repeated on price schedules and often predict certain price movements, based on the psychoLogs of the market and participants' behaviour.

```python
def create_price_patterns(df):
 """
quality of price tags

Theory: Price Patters reflect the psychoLogs of the market and often predict
They're based on the relationship analysis.
Between Open, High, Low, Close prices.

Type of Pattern:
1. Reversal - predict a change in trend
2. Continuing - confirms the current trend
3. Uncertainties - indicate on market uncertainty

 parameters:
- df: DataFrame with OHLC data

Returns:
- DataFrame with added parters
 """
"preint("\\create price slipters...")

♪ 1 ♪ Turners ♪

# Doji - market uncertainty
 body_size = abs(df['Open'] - df['Close'])
 total_range = df['High'] - df['Low']
 df['Doji'] = (body_size <= 0.1 * total_range).astype(int)

# Hammer is a bald turn
 lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
 upper_shadow = df['High'] - df[['Open', 'Close']].max(axis=1)
 df['Hammer'] = ((lower_shadow > 2 * body_size) &
 (upper_shadow <= 0.1 * lower_shadow)).astype(int)

# Shooting Star - Bear Turn
 df['Shooting_Star'] = ((upper_shadow > 2 * body_size) &
 (lower_shadow <= 0.1 * upper_shadow)).astype(int)

 # Engulfing patterns
♪ Bold absorption ♪
 df['Bullish_Engulfing'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Open'] < df['Close'].shift(1)) &
 (df['Close'] > df['Open'].shift(1))).astype(int)

# Bear absorption
 df['Bearish_Engulfing'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Open'] > df['Close'].shift(1)) &
 (df['Close'] < df['Open'].shift(1))).astype(int)

# 2. Continuing pathetics

# Marubozu is a strong trend
 df['Bullish_Marubozu'] = ((df['Close'] > df['Open']) &
 (df['Open'] == df['Low']) &
 (df['Close'] == df['High'])).astype(int)

 df['Bearish_Marubozu'] = ((df['Close'] < df['Open']) &
 (df['Open'] == df['High']) &
 (df['Close'] == df['Low'])).astype(int)

# 3. Patterns of uncertainty

# Spinning Top - Uncertainty
 df['Spinning_Top'] = ((body_size < 0.3 * total_range) &
 (lower_shadow > body_size) &
 (upper_shadow > body_size)).astype(int)

#4 Combination Pathers

# Three white soldiers (3 days in a row)
 df['Three_White_Soldiers'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Close'].shift(2) > df['Open'].shift(2)) &
 (df['Close'] > df['Close'].shift(1)) &
 (df['Close'].shift(1) > df['Close'].shift(2))).astype(int)

# Three black crows (3 days in a row)
 df['Three_Black_Crows'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Close'].shift(2) < df['Open'].shift(2)) &
 (df['Close'] < df['Close'].shift(1)) &
 (df['Close'].shift(1) < df['Close'].shift(2))).astype(int)

#5: Statistical Pathers

# High volatility
 df['High_Volatility_Day'] = (total_range > total_range.rolling(20).quantile(0.8)).astype(int)

# Low volatility
 df['Low_Volatility_Day'] = (total_range < total_range.rolling(20).quantile(0.2)).astype(int)

# 6. Patterns of scale

# A narrow range
 df['Narrow_Range'] = (total_range < total_range.rolling(10).mean() * 0.5).astype(int)

# Broad range
 df['Wide_Range'] = (total_range > total_range.rolling(10).mean() * 1.5).astype(int)

==History====History=====Printures======Printures======Printures=====Printures=====Printures======Printures=======Printures======Printures========Printures========Printures========Printures===========Printures=========Printures===========Prin(f)=====Prin=====Prin(f)=======================Prin(f)============================Prin===========================================================================================================================================================================================================================================================================

 return df

# Showing the creation of price patches
print("\n" + "="*60)
"Prent("♪ DEMONSTRUCTURE: price cutter")
print("="*60)

# rent price patches
df_with_patterns = create_price_patterns(sample_data.copy())

# Showing statistics on pathites
(f) \n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////)/)/)/)/////////)//)//)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/)/===============
pattern_cols = [col for col in df_with_patterns.columns if col in ['Doji', 'Hammer', 'Shooting_Star', 'Bullish_Engulfing', 'Bearish_Engulfing']]
for col in pattern_cols:
 count = df_with_patterns[col].sum()
((account/len(df_with_patterns)*100:.1f}%))

# Showing examples of pathers
(the last 10 days):)
pattern_examples = df_with_patterns[['Doji', 'Hammer', 'Bullish_Engulfing', 'High_Volatility_Day', 'Narrow_Range']].tail(10)
print(pattern_examples)
```

♪##2 ♪ Volume indicators ♪

**Theory:** Volume indicators analyse the number of shares/contracts traded and help confirm the strength of price movements. Volume often precedes price changes and is an important indicator of market sentiment.

```python
def create_volume_features(df):
 """
volume of indicators for financial data

Theory: The volume of trade is a key indicator of the power of price movements.
High volume confirms trends, and low volume can indicate on
The volumetric indicators help:

1. Confirm the strength of trends
2. Identify divergents
3. Identify entry/exit points
4. Assess market liquidity

 parameters:
- df: DataFrame with OHLCV data

Returns:
- DataFrame with added volume signature
 """
"preint("\create volume signs...")

1. Basic volume statistics

# Volume Rate of Change - Volume Speed
 df['Volume_ROC'] = df['Volume'].pct_change()
 df['Volume_ROC_5'] = df['Volume'].pct_change(5)
 df['Volume_ROC_10'] = df['Volume'].pct_change(10)

# Volume Moving Overages - moving average volumes
 for window in [5, 10, 20, 50]:
 df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window).mean()
 df[f'Volume_EMA_{window}'] = df['Volume'].ewm(span=window).mean()

# Current volume to average
 df[f'Volume_vs_SMA_{window}'] = df['Volume'] / df[f'Volume_SMA_{window}']
 df[f'Volume_vs_EMA_{window}'] = df['Volume'] / df[f'Volume_EMA_{window}']

♪ 2. Volume indicators

# On-Balance Volume (OBV) - Accumulated volume
 price_change = df['Close'].diff()
 volume_direction = np.where(price_change > 0, 1,
 np.where(price_change < 0, -1, 0))
 df['OBV'] = (df['Volume'] * volume_direction).cumsum()

 # OBV Rate of Change
 df['OBV_ROC'] = df['OBV'].pct_change()
 df['OBV_ROC_5'] = df['OBV'].pct_change(5)

 # Volume Price Trend (VPT)
 df['VPT'] = (df['Volume'] * df['Close'].pct_change()).cumsum()

# Money Flow Index (MFI) - Wave-weighted RSI
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 money_flow = typical_price * df['Volume']

 positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
 negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

 positive_flow_ma = positive_flow.rolling(14).sum()
 negative_flow_ma = negative_flow.rolling(14).sum()

 mfi = 100 - (100 / (1 + positive_flow_ma / negative_flow_ma))
 df['MFI'] = mfi

# 3. Volume-value ratios

# Volume vs Price Correlation - volume and price correlation
 for window in [10, 20, 50]:
 df[f'Volume_Price_Corr_{window}'] = df['Volume'].rolling(window).corr(df['Close'])
 df[f'Volume_Price_Corr_Change_{window}'] = df[f'Volume_Price_Corr_{window}'].pct_change()

 # Volume Weighted Average Price (VWAP)
 for window in [10, 20, 50]:
 typical_price = (df['High'] + df['Low'] + df['Close']) / 3
 df[f'VWAP_{window}'] = (typical_price * df['Volume']).rolling(window).sum() / df['Volume'].rolling(window).sum()
 df[f'Price_vs_VWAP_{window}'] = df['Close'] / df[f'VWAP_{window}']

# 4. Volume-sized pathers

# Volume Spices - Volume Splashes
 volume_mean = df['Volume'].rolling(20).mean()
 volume_std = df['Volume'].rolling(20).std()

 df['Volume_Spike'] = (df['Volume'] > volume_mean + 2 * volume_std).astype(int)
 df['Volume_Dry'] = (df['Volume'] < volume_mean - volume_std).astype(int)
 df['Volume_Extreme'] = (df['Volume'] > volume_mean + 3 * volume_std).astype(int)

# Volume Breakout is a volume breakthrough
 df['Volume_Breakout'] = ((df['Volume'] > df['Volume'].rolling(20).quantile(0.8)) &
 (df['Close'] > df['High'].rolling(20).max().shift(1))).astype(int)

♪ 5. Massive diversification ♪

 # Volume-Price Divergence
 price_trend = df['Close'].rolling(10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
 volume_trend = df['Volume'].rolling(10).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])

 df['Volume_Price_Divergence'] = ((price_trend > 0) & (volume_trend < 0)).astype(int)
 df['Volume_Price_Convergence'] = ((price_trend > 0) & (volume_trend > 0)).astype(int)

# 6. Mass oscillators

 # Volume Oscillator
 df['Volume_Oscillator'] = df['Volume_EMA_10'] - df['Volume_EMA_20']
 df['Volume_Oscillator_Pct'] = df['Volume_Oscillator'] / df['Volume_EMA_20'] * 100

 # Volume Rate of Change Oscillator
 df['Volume_ROC_Oscillator'] = df['Volume_ROC'].rolling(5).mean() - df['Volume_ROC'].rolling(20).mean()

♪ 7. Volume percentiles

# Volume Percentile is the current volume position
 for window in [20, 50, 100]:
 df[f'Volume_Percentile_{window}'] = df['Volume'].rolling(window).rank(pct=True)
 df[f'Volume_Percentile_Change_{window}'] = df[f'Volume_Percentile_{window}'].diff()

♪ 8. Volume trends

 # Volume Trend Strength
 for window in [10, 20]:
 df[f'Volume_Trend_{window}'] = df['Volume'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )
 df[f'Volume_Trend_R2_{window}'] = df['Volume'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

nint(f) is created {len([col for col in df.columns if 'Volume' in col or 'OBV' in cool or 'VPT' in cool or 'MFI' in cool or 'VWAP' in cool]}} volumetric topics}

 return df

# Demonstration of the development of broad features
print("\n" + "="*60)
print("\Demonstration: cut of volume)
print("="*60)

# of the volume signs
df_with_volume = create_volume_features(sample_data.copy())

# Showing statistics on volume signature
pint(f"\n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\))
average volume: {df_with_volume['Volume']mean(:,0f}})
Splashes: {df_with_volume['Volume_Spice'].sum()}
dry volume: {df_with_volume['Volume_Dry'].sum()}
Print(f"MFI (average): {df_with_volume['MFI']mean(: 2f}})

# Showing examples of volumetric features
(the last 5 days):)
volume_examples = df_with_volume[['Volume_ROC', 'Volume_vs_SMA_20', 'OBV_ROC', 'MFI', 'Volume_Spike']].tail()
print(volume_examples)
```

### 3: Volatility of the signs

**Theory:** Volatility measures price volatility and is a key factor in risk assessment. High volatility indicates market instability and low volatility. Volatility tends to cluster and often precedes significant price movements.

```python
def create_volatility_features(df):
 """
risk of volatility for financial data

Theory: Volatility is a risk measure and uncertainty on the market.
It helps:

1. Assess investment risk
2. Determine the size of the entries
3. Identify periods of instability
4. To anticipate future price movements
5. Adjust trade strategies

Types of volatility:
1. Historical - on historical data
2. Implicit - from options
3. Realized - actual volatility
4. Relative - price volatility

 parameters:
- df: DataFrame with OHLCV data

Returns:
- DataFrame with added high volatility
 """
"preint("\\create signs of volatility...")

# 1. Historical Volatility

# Simple volatility (standard deviation)
 for window in [5, 10, 20, 50, 100]:
 df[f'HV_{window}'] = df['Close'].rolling(window).std()
 df[f'HV_Annualized_{window}'] = df[f'HV_{window}'] * np.sqrt(252)

# Logarithmic volatility (more precise)
 log_returns = np.log(df['Close'] / df['Close'].shift(1))
 df[f'Log_HV_{window}'] = log_returns.rolling(window).std()
 df[f'Log_HV_Annualized_{window}'] = df[f'Log_HV_{window}'] * np.sqrt(252)

# 2. Overage True Range (ATR) - Average True Range

# ATR for different periods
 for window in [5, 10, 14, 20]:
 df[f'ATR_{window}'] = calculate_atr(df['High'], df['Low'], df['Close'], window)
 df[f'ATR_Percent_{window}'] = df[f'ATR_{window}'] / df['Close'] * 100

# 3. Volatility of Volatility

# VoV is the variability of the most volatile
 for window in [10, 20]:
 df[f'VoV_{window}'] = df['HV_20'].rolling(window).std()
 df[f'VoV_Percentile_{window}'] = df[f'VoV_{window}'].rolling(50).rank(pct=True)

# 4. Relative volatility

# Volatility Ratio - the ratio of short-term to long-term volatility
 df['Vol_Ratio_5_20'] = df['HV_5'] / df['HV_20']
 df['Vol_Ratio_10_50'] = df['HV_10'] / df['HV_50']
 df['Vol_Ratio_20_100'] = df['HV_20'] / df['HV_100']

# Volatility Percentile is the current volatility position
 for window in [20, 50, 100]:
 df[f'Vol_Percentile_{window}'] = df['HV_20'].rolling(window).rank(pct=True)
 df[f'Vol_Percentile_Change_{window}'] = df[f'Vol_Percentile_{window}'].diff()

# 5. Volatility on scale (Rage-based Volatility)

# Parkinson Volatility - Using High and Low
 for window in [5, 10, 20]:
 df[f'Parkinson_Vol_{window}'] = np.sqrt(
 (1 / (4 * np.log(2))) *
 (np.log(df['High'] / df['Low']) ** 2).rolling(window).mean()
 )

# Garman-Klass Volatility - uses OHLC
 for window in [5, 10, 20]:
 df[f'GK_Vol_{window}'] = np.sqrt(
 (0.5 * (np.log(df['High'] / df['Low']) ** 2) -
 (2 * np.log(2) - 1) * (np.log(df['Close'] / df['Open']) ** 2)
 ).rolling(window).mean()
 )

# 6. Volatility on database of day-to-day data

# Realized Volatility - Realized Volatility
 for window in [5, 10, 20]:
 df[f'Realized_Vol_{window}'] = np.sqrt(
 (df['Close'].pct_change() ** 2).rolling(window).sum()
 )

# 7. Cluster volatility

# Volatility Clustering is a tendency for volatility to clusterize
 for window in [10, 20]:
 vol_returns = df['HV_20'].pct_change()
 df[f'Vol_Clustering_{window}'] = vol_returns.rolling(window).std()
 df[f'Vol_Clustering_Autocorr_{window}'] = vol_returns.rolling(window).apply(
 lambda x: x.autocorr(lag=1) if len(x) > 1 else np.nan
 )

♪ 8, trend volatility

# Volatility Trend - trend of volatility
 for window in [10, 20]:
 df[f'Vol_Trend_{window}'] = df['HV_20'].rolling(window).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == window else np.nan
 )
 df[f'Vol_Trend_R2_{window}'] = df['HV_20'].rolling(window).apply(
 lambda x: np.corrcoef(range(len(x)), x)[0, 1]**2 if len(x) == window else np.nan
 )

# 9. Fracture volatility (Gaps)

# Gap Volatility - Fracture volatility
 gap = df['Open'] - df['Close'].shift(1)
 df['Gap_Volatility'] = gap.rolling(20).std()
 df['Gap_Volatility_Pct'] = df['Gap_Volatility'] / df['Close'] * 100

# 10. Volume volatility

 # Volume-Weighted Volatility
 for window in [10, 20]:
 df[f'Volume_Weighted_Vol_{window}'] = (
 (df['Close'].pct_change() ** 2 * df['Volume']).rolling(window).sum() /
 df['Volume'].rolling(window).sum()
 )

♪ 11 ♪ Pathtern volatility ♪

# High Volatility Days - High Volatility Days
 df['High_Vol_Day'] = (df['HV_20'] > df['HV_20'].rolling(50).quantile(0.8)).astype(int)
 df['Low_Vol_Day'] = (df['HV_20'] < df['HV_20'].rolling(50).quantile(0.2)).astype(int)

# Volatility Breakout - a breakthrough in volatility
 df['Vol_Breakout'] = (df['HV_20'] > df['HV_20'].rolling(20).max().shift(1)).astype(int)
 df['Vol_Breakdown'] = (df['HV_20'] < df['HV_20'].rolling(20).min().shift(1)).astype(int)

♪ 12 ♪ The volatility of correlations

 # Volatility-Price Correlation
 for window in [20, 50]:
 df[f'Vol_Price_Corr_{window}'] = df['HV_20'].rolling(window).corr(df['Close'])
 df[f'Vol_Volume_Corr_{window}'] = df['HV_20'].rolling(window).corr(df['Volume'])

nint(f) is created {len([coll for col in df.columns if 'HV_' in cool or 'ATR_' in cool or 'Vol_' in cool or 'Vov_' in cool or 'Parkinson_' in cool or 'GK_' in cool or 'Realized_' in cool]}}}

 return df

def calculate_atr(high, low, close, window=14):
 """
Calculation of Average True Range (ATR)

Theory: ATR measures market volatility by showing average range
Use for:
- Definitions of stop-loss size
- Volatility estimates
- Weak signal filtering

 True Range = max(High-Low, |High-PrevClose|, |Low-PrevClose|)
 ATR = SMA(True Range)

 parameters:
- High: Maximum Price Series
- Low: Minimum Price Series
- lose: Series of closing prices
- Windows: period for SMA (on default 14)

Returns:
- Series with ATR values
 """
 tr1 = high - low
 tr2 = abs(high - close.shift(1))
 tr3 = abs(low - close.shift(1))

 tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
 atr = tr.rolling(window=window).mean()

 return atr

# Showing signs of volatility
print("\n" + "="*60)
Print("~ DEMONSTRUCTION: risk of volatility")
print("="*60)

# of the signs of volatility
df_with_volatility = create_volatility_features(sample_data.copy())

# Showing statistics on volatility
Print(f"\n\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\) \\\\\\\) \) \\\\\\\\\\\\\\\\\\\\\) \) \) \\) \) \(((\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\) \) \) \) \) \) \) \) \) \) \) \) \) \) \\\\/) \/) \) \)
(f "Medial volatility (20 days): {df_with_volatility['HV_20']mean(: 4f}}")
print(f"ATR (14 days): {df_with_volatility['ATR_14']mean(:4f}})
"High volatility days: {df_with_volatility['High_Vol_Day'].sum()})
"Low_Vol_Day']sum()}

# Showing examples of signs of volatility
Spring(f"\n\\\\\\ examples signs of volatility (last 5 days):")
volatility_examples = df_with_volatility[['HV_20', 'ATR_14', 'Vol_Ratio_5_20', 'Vol_Percentile_50', 'High_Vol_Day']].tail()
print(volatility_examples)
```

## Signs for different Times

**Theory:** MultiTimeframe analysis is a powerful tool in technical analysis and machine learning; it takes into account the different time horizons and identifies the variables that are only visible on certain Timeframes.

**Why a multi-timeframe analysis is important:**
- ** Full picture: ** Different Times show different aspects of the market
- ** Confirmation of the signals:** Signs on different Times confirm each other.
- ** Noise filtering:** Long-term trends filter short-term noise
- **Best entry points:** The Timeframes combination gives the best entry points.

♪##1 ♪ MultiTimeframes ♪

```python
def create_multiTimeframe_features(df, Timeframes=['1H', '4H', '1D']):
 """
specified multi-Timeframe features

Theory: MultiTimeframe analysis allows for consideration of different
Time horizons in one set of topics.

1. See the full picture of the market
2. Confirm signals on different levels
3. Filter noise of short-term movements
4. Find the best entry and exit points

Principles:
- Higher Times determine the overall trend
- Middle Timeframes give entry points
- Low Timeframes ensure accuracy

 parameters:
- df: DataFrame with OHLCV data
 - Timeframes: List Timeframes for Analysis

Returns:
- DataFrame with multi-Timeframes
 """
print("\\create multiTimeframe signs...")

# creative copies for work
 result_df = df.copy()

 for tf in timeframes:
Print(f" ♪ Timeframe processing: {tf}}

# Resample for different Times
 resampled = df.resample(tf).agg({
 'Open': 'first',
 'High': 'max',
 'Low': 'min',
 'Close': 'last',
 'Volume': 'sum'
 })

# Remove line with NaN
 resampled = resampled.dropna()

if Len(resampled) < 50: # Minimum data for indicators
nint(f" ♪ insufficient data for Timeframe {tf})
 continue

# 1. Technical indicators for each Timeframe
 resampled[f'RSI_{tf}'] = calculate_rsi(resampled['Close'])
 macd_line, signal_line, histogram = calculate_macd(resampled['Close'])
 resampled[f'MACD_{tf}'] = macd_line
 resampled[f'MACD_signal_{tf}'] = signal_line
 resampled[f'MACD_Histogram_{tf}'] = histogram

 # Bollinger Bands
 bb_upper, bb_lower, bb_middle = calculate_bollinger_bands(resampled['Close'])
 resampled[f'BB_Upper_{tf}'] = bb_upper
 resampled[f'BB_lower_{tf}'] = bb_lower
 resampled[f'BB_Middle_{tf}'] = bb_middle
 resampled[f'BB_Position_{tf}'] = (resampled['Close'] - bb_lower) / (bb_upper - bb_lower)

 # Stochastic
 stoch_k, stoch_d = calculate_stochastic(resampled['High'], resampled['Low'], resampled['Close'])
 resampled[f'Stoch_K_{tf}'] = stoch_k
 resampled[f'Stoch_D_{tf}'] = stoch_d

# 2. Rolling average
 for window in [10, 20, 50]:
 resampled[f'SMA_{window}_{tf}'] = resampled['Close'].rolling(window).mean()
 resampled[f'EMA_{window}_{tf}'] = resampled['Close'].ewm(span=window).mean()

# 3. Volatility
 resampled[f'Volatility_{tf}'] = resampled['Close'].rolling(20).std()
 resampled[f'ATR_{tf}'] = calculate_atr(resampled['High'], resampled['Low'], resampled['Close'])

♪ 4. Volume indicators
 resampled[f'Volume_SMA_{tf}'] = resampled['Volume'].rolling(20).mean()
 resampled[f'Volume_vs_Avg_{tf}'] = resampled['Volume'] / resampled[f'Volume_SMA_{tf}']

♪ 5. Treadmarks
 resampled[f'Trend_{tf}'] = resampled['Close'].rolling(20).apply(
 lambda x: np.polyfit(range(len(x)), x, 1)[0] if len(x) == 20 else np.nan
 )

# 6. Synchronization with the original Timeframe
 for col in resampled.columns:
 if col not in ['Open', 'High', 'Low', 'Close', 'Volume']:
# Forward falls for sync
 result_df[col] = resampled[col].reindex(df.index).fillna(method='ffill')

# 7. Inter-Timeframes relationships
 if 'RSI_1D' in result_df.columns and 'RSI_1H' in result_df.columns:
 result_df['RSI_Daily_vs_Hourly'] = result_df['RSI_1D'] / result_df['RSI_1H']
 result_df['RSI_Divergence'] = (result_df['RSI_1D'] > 70) & (result_df['RSI_1H'] < 30)

 if 'MACD_1D' in result_df.columns and 'MACD_1H' in result_df.columns:
 result_df['MACD_Daily_vs_Hourly'] = result_df['MACD_1D'] / result_df['MACD_1H']

♪ 8. Tread coherence
 trend_cols = [col for col in result_df.columns if 'Trend_' in col]
 if len(trend_cols) >= 2:
 result_df['Trend_Consistency'] = result_df[trend_cols].apply(
 lambda x: (x > 0).sum() if x.notna().all() else np.nan, axis=1
 )

== sync, corrected by elderman == @elder_man

 return result_df

# Demonstration of the creation of multi-Timeframe features
print("\n" + "="*60)
"Printh("♪ Demonstration: cute multi-Timeframe signs")
print("="*60)

# creative multi-Timeframe features
df_multiTimeframe = create_multiTimeframe_features(sample_data.copy(), ['1D', '1W'])

# Showing statistics on multi-Timeframe
(f) \n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\)}=============)
multiTimeframe_cols = [col for col in df_multiTimeframe.columns if any(tf in col for tf in ['_1D', '_1W', '_1H', '_4H'])]
== sync, corrected by elderman == @elder_man

# Showing examples of multi-Timeframe features
prent(f"\n\\\\\\\\\\\\examples MultiTimeframe signs (last 5 days):")
multiTimeframe_examples = df_multiTimeframe[['RSI_1D', 'MACD_1D', 'RSI_1W', 'MACD_1W', 'Trend_Consistency']].tail()
print(multiTimeframe_examples)
```

♪##2 ♪ Seasonal signs

**Theory:** Seasonal indicators take into account cyclical variables in financial data associated with time. Financial markets show different seasonal effects that can be used to improve model predictive capacity.

```python
def create_seasonal_features(df):
 """
seasonal signs for financial data

Theory: Seasonal characteristics take into account cyclical variables in financial
Financial markets show different types of data associated with time.
seasonal effects:

1. Intra-daughter hours (tender hours)
2. Weekly tolls (days of weeks)
3. Monthly commons (days of the month)
4. Quarter (seasons)
5. Annual commons (months of the year)

 parameters:
 - df: dataFrame with Datetimeindex

Returns:
- DataFrame with added seasonal signature
 """
"preint("\\create seasonal signs...")

# 1. Basic time signs

# An hour of day (for in-day data)
 if hasattr(df.index, 'hour'):
 df['Hour'] = df.index.hour
 df['Hour_sin'] = np.sin(2 * np.pi * df['Hour'] / 24)
 df['Hour_cos'] = np.cos(2 * np.pi * df['Hour'] / 24)

# Day periods
 df['Morning'] = ((df['Hour'] >= 6) & (df['Hour'] < 12)).astype(int)
 df['Afternoon'] = ((df['Hour'] >= 12) & (df['Hour'] < 18)).astype(int)
 df['Evening'] = ((df['Hour'] >= 18) & (df['Hour'] < 24)).astype(int)
 df['Night'] = ((df['Hour'] >= 0) & (df['Hour'] < 6)).astype(int)

# Day of the week
 df['DayOfWeek'] = df.index.dayofweek
 df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
 df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)

# Day of the month
 df['DayOfMonth'] = df.index.day
 df['DayOfMonth_sin'] = np.sin(2 * np.pi * df['DayOfMonth'] / 31)
 df['DayOfMonth_cos'] = np.cos(2 * np.pi * df['DayOfMonth'] / 31)

# Month
 df['Month'] = df.index.month
 df['Month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
 df['Month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)

# Quarter
 df['Quarter'] = df.index.quarter
 df['Quarter_sin'] = np.sin(2 * np.pi * df['Quarter'] / 4)
 df['Quarter_cos'] = np.cos(2 * np.pi * df['Quarter'] / 4)

# Day of the year
 df['DayOfYear'] = df.index.dayofyear
 df['DayOfYear_sin'] = np.sin(2 * np.pi * df['DayOfYear'] / 365)
 df['DayOfYear_cos'] = np.cos(2 * np.pi * df['DayOfYear'] / 365)

# 2. Special calendar features

# Week of the Year
 df['WeekOfYear'] = df.index.isocalendar().week
 df['WeekOfYear_sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
 df['WeekOfYear_cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)

# 3. Trade days and weekends

# Weekends
 df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
 df['Is_Monday'] = (df['DayOfWeek'] == 0).astype(int)
 df['Is_Friday'] = (df['DayOfWeek'] == 4).astype(int)

# End of month/quarter/year
 df['Is_Month_End'] = (df.index.is_month_end).astype(int)
 df['Is_Quarter_End'] = (df.index.is_quarter_end).astype(int)
 df['Is_Year_End'] = (df.index.is_year_end).astype(int)

# 4. Seasonal periods

# Times of the year (for the northern hemisphere)
 df['Spring'] = ((df['Month'] >= 3) & (df['Month'] <= 5)).astype(int)
 df['Summer'] = ((df['Month'] >= 6) & (df['Month'] <= 8)).astype(int)
 df['Autumn'] = ((df['Month'] >= 9) & (df['Month'] <= 11)).astype(int)
 df['Winter'] = ((df['Month'] == 12) | (df['Month'] <= 2)).astype(int)

♪ 5. Financial seasons

# Quarterly Reports (last month of quarter)
 df['Earnings_Season'] = ((df['Month'] % 3 == 0) & (df['DayOfMonth'] >= 15)).astype(int)

# January effect (first days of January)
 df['January_Effect'] = ((df['Month'] == 1) & (df['DayOfMonth'] <= 15)).astype(int)

# Summer decline (July-August)
 df['Summer_Doldrums'] = ((df['Month'] >= 7) & (df['Month'] <= 8)).astype(int)

# 6. Celebrating periods

# Christmas period (December)
 df['Holiday_Season'] = (df['Month'] == 12).astype(int)

♪ 7. Seasonal statistics

# Averages on days of the week
 for col in ['Close', 'Volume']:
 if col in df.columns:
 for day in range(7):
 day_mask = df['DayOfWeek'] == day
 df[f'{col}_DayOfWeek_{day}_Mean'] = df[col].where(day_mask).rolling(50).mean()
 df[f'{col}_DayOfWeek_{day}_Std'] = df[col].where(day_mask).rolling(50).std()

# 8. Seasonal de-tranding

# Remove seasonal trends
 for col in ['Close', 'Volume']:
 if col in df.columns:
# Seasonal degradation (simplified)
 monthly_avg = df[col].groupby(df.index.month).transform('mean')
 df[f'{col}_Deseasonalized'] = df[col] - monthly_avg + df[col].mean()

#9 Seasonal indicators

# Seasonal power (seasonal variability)
 for season_col in ['Spring', 'Summer', 'Autumn', 'Winter']:
 if season_col in df.columns:
 season_mask = df[season_col] == 1
 if 'Close' in df.columns:
 df[f'Seasonal_Strength_{season_col}'] = df['Close'].where(season_mask).rolling(50).std()

(f) is created {len([coll for col in df.columns if any(x in col for x in ['Hour', 'DayOfWeek', 'Month', 'Quarter', ` Season', `Holiday', 'Desonasonized'])]})}seasonal signs")

 return df

# Showing seasonal signs
print("\n" + "="*60)
"Prent("♪ DEMONSTRUCTION: Create of seasonal signs")
print("="*60)

# Create of seasonal signs
df_seasonal = create_seasonal_features(sample_data.copy())

# Showing statistics on seasonal signature
(f) \n\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\) \\\\\\\\\\\) \) \) \) \) \) \)/)/=============)
pint(f" Weekday (average): {df_seasonal['DayOfWeek']mean(:2f}})
pint(f"Mean (average): {df_seasonal['Month'].mean(: 2f}})
pprint(f) "Exit: {df_seasonal['Is_Weekend'].sum()}days")
spring(f" End of month: {df_seasonal['Is_Month_End'].sum()}days")

# Showing examples of seasonal signs
(the last five days):)
seasonal_examples = df_seasonal[['DayOfWeek', 'Month', 'Is_Weekend', 'Spring', 'Summer', 'Holiday_Season']].tail()
print(seasonal_examples)
```

♪ ♪ Selection of signs

*## 1. Correlative analysis
```python
def remove_correlated_features(df, threshold=0.95):
""remove correlate features""

# Calculation of correlation matrix
 corr_matrix = df.select_dtypes(include=[np.number]).corr().abs()

# Finding steam with high correlation
 upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Remove signs with high correlation
 to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]

 return df.drop(columns=to_drop)
```

###2 # The importance of signs #
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression

def select_important_features(X, y, k=20):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""".""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Random Forest is important
 rf = RandomForestRegressor(n_estimators=100, random_state=42)
 rf.fit(X, y)
 feature_importance = rf.feature_importances_

# F test
 selector = SelectKBest(score_func=f_regression, k=k)
 X_selected = selector.fit_transform(X, y)

 return X_selected, selector.get_support()
```

## Automatic engineering of the signs

### 1. FeatureTools
```python
import featuretools as ft

def automated_feature_engineering(df):
"Automatic engineering of the signs with FeatureTools."

 # create EntitySet
 es = ft.EntitySet(id="trading_data")
 es = es.add_dataframe(
 dataframe_name="trades",
 dataframe=df,
 index="timestamp",
 time_index="timestamp"
 )

♪ Create signs
 feature_matrix, feature_defs = ft.dfs(
 entityset=es,
 target_dataframe_name="trades",
 max_depth=2,
 verbose=True
 )

 return feature_matrix, feature_defs
```

### 2. TSFresh
```python
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute

def extract_time_series_features(df):
"""" "Extracting signs of time series"""

# The extraction of signs
 extracted_features = extract_features(
 df,
 column_id="id",
 column_sort="timestamp",
 default_fc_parameters=tsfresh.feature_extraction.Settings.ComprehensiveFCParameters()
 )

# Simulation of missing values
 extracted_features = impute(extracted_features)

 return extracted_features
```

## Complete workflow example: Integrated engineering of topics

**Theory:** Now we're gonna combine all the engineering techniques we've learned in one complex example, which will show how to apply the different methods to create an effective set of features for financial engineering.

** Why an integrated approach is important:**
- ** Synergy: ** Different types of indicators complement each other
- **Pativity:** Illustrative diversity increases model stability
- ** Interpretability: ** Different types of indicators help to understand model behaviour
- ** Adaptability:** Integrated Workinget approach on different data types

```python
def create_comprehensive_features(df):
 """
comprehensive features for financial engineering

Theory: This function brings together all the engineering techniques that have been studied.
It includes:

1. Technical indicators (RSI, MACD, Bollinger Bands, etc.)
2. Statistical indicators (points, quantiles, correlations)
3. Time indicators (lags, seasonality, trends)
4. Interactive indicators (mark combinations)
5. Specialized trade features
6. Selection and clearance of topics

 parameters:
- df: DataFrame with OHLCV data and Datameindex

Returns:
- DataFrame with complex set of topics
- Vocabulary with information on created primaries
 """
"Prent("♪ ♪ The beginning of complex engineering signs... ♪
 print("="*60)

# Retaining source data
 original_columns = df.columns.toList()
 feature_info = {
 'original_features': len(original_columns),
 'Technical_indicators': 0,
 'statistical_features': 0,
 'time_features': 0,
 'interaction_features': 0,
 'trading_features': 0,
 'final_features': 0
 }

♪ 1. Technical indicators
"pint("\1.create technical indicators...")
 df = create_Technical_indicators(df)
 Technical_cols = [col for col in df.columns if col not in original_columns]
 feature_info['Technical_indicators'] = len(Technical_cols)
Print(f" ) is created {len(Technical_cols} technical indicators)

# 2. Statistical indicators
"preint("\2.create statistical signs...")
 df = create_statistical_features(df)
 stats_cols = [col for col in df.columns if col not in original_columns + Technical_cols]
 feature_info['statistical_features'] = len(stats_cols)
{len(stats_cols)} of statistical topics}

♪ 3. Temporary signs
"print("♪ 3. cute time signs...")
 df = create_time_features(df)
 time_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols]
 feature_info['time_features'] = len(time_cols)
print(f) is created {len(time_cols)}time signs}

# 4. Interactive signs
"preint("~ 4. cut interactive signs...")
 df = create_interaction_features(df)
 interaction_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols + time_cols]
 feature_info['interaction_features'] = len(interaction_cols)
== sync, corrected by elderman == @elder_man

#5 Specialized trade features
"spint("\ 5. trade mark...")
 df = create_trading_features(df)
 trading_cols = [col for col in df.columns if col not in original_columns + Technical_cols + stats_cols + time_cols + interaction_cols]
 feature_info['trading_features'] = len(trading_cols)
print(f) is created {len(trade_cols}}trade marks}

# 6. Clear and selection of topics
"spint(" . . . . . . . . . . .
 df_cleaned = clean_and_select_features(df)
 feature_info['final_features'] = len(df_cleaned.columns)
Print(f) left {len(df_cleaned.columns)}final signs}

 print("="*60)
"Prent("♪ Comprehensive Design of Signs Completed! ")
Total created: {feature_info['final_features']}}
(print(f" - Technical indicators: {feature_info['Technical_indicators']}})
pprint(f" - Statistical indicators: {feature_info['statistical_features']}}
prent(f" - Temporary signs:}}
(print(f" - Interactive topics: {feature_info['interaction_features']}})
Spring(f" - Trademarks:}}

 return df_cleaned, feature_info

def create_trading_features(df):
 """
special trade features

Theory: Trade features are specific to financial markets and include:
Pathers that traders use for decision-making.
 """
"spint(" ~ trade features...")

# Price tablets
# Doji (small body candle)
 df['Doji'] = (abs(df['Open'] - df['Close']) <= 0.1 * (df['High'] - df['Low'])).astype(int)

# Hammer
 body = abs(df['Close'] - df['Open'])
 lower_shadow = df[['Open', 'Close']].min(axis=1) - df['Low']
 upper_shadow = df['High'] - df[['Open', 'Close']].max(axis=1)

 df['Hammer'] = ((lower_shadow > 2 * body) & (upper_shadow <= 0.1 * lower_shadow)).astype(int)

 # Engulfing patterns
 df['Bullish_Engulfing'] = ((df['Close'] > df['Open']) &
 (df['Close'].shift(1) < df['Open'].shift(1)) &
 (df['Open'] < df['Close'].shift(1)) &
 (df['Close'] > df['Open'].shift(1))).astype(int)

 df['Bearish_Engulfing'] = ((df['Close'] < df['Open']) &
 (df['Close'].shift(1) > df['Open'].shift(1)) &
 (df['Open'] > df['Close'].shift(1)) &
 (df['Close'] < df['Open'].shift(1))).astype(int)

# The volume of signs
 df['Volume_Spike'] = (df['Volume'] > df['Volume'].rolling(20).mean() * 2).astype(int)
 df['Volume_Dry'] = (df['Volume'] < df['Volume'].rolling(20).mean() * 0.5).astype(int)

# Volatility of the signs
 df['High_Volatility'] = (df['Volatility_20'] > df['Volatility_20'].rolling(50).quantile(0.8)).astype(int)
 df['Low_Volatility'] = (df['Volatility_20'] < df['Volatility_20'].rolling(50).quantile(0.2)).astype(int)

# Trend signs
 df['Strong_Uptrend'] = ((df['Close'] > df['SMA_20']) &
 (df['SMA_20'] > df['SMA_50']) &
 (df['SMA_50'] > df['SMA_200'])).astype(int)

 df['Strong_Downtrend'] = ((df['Close'] < df['SMA_20']) &
 (df['SMA_20'] < df['SMA_50']) &
 (df['SMA_50'] < df['SMA_200'])).astype(int)

 return df

def clean_and_select_features(df, correlation_threshold=0.95, Missing_threshold=0.5):
 """
Clear and selection of topics

Theory: Once a large number of signs have been created, it is necessary to:
1. Remove signs with more missing values
2. Remove correlate features
3. Remove constants
4. Remove signs with endless values
 """
"Print(" ~ clay and selection of topics...")

# 1. remove signs with more missing values
 Missing_ratio = df.isnull().sum() / len(df)
 cols_to_drop = Missing_ratio[Missing_ratio > Missing_threshold].index
 df = df.drop(columns=cols_to_drop)
nint(f" ) Deleted {len(cols_to_drop)} signs with >{Missing_threshold*100} % passes}

# 2. Remove constant signs
 constant_cols = df.columns[df.nunique() <= 1]
 df = df.drop(columns=constant_cols)
Print(f) removed {len(constant_cols)} Constant signs}

# 3. remove signs with endless values
 inf_cols = df.columns[df.isin([np.inf, -np.inf]).any()]
 df = df.drop(columns=inf_cols)
nint(f" ♪ removed {len(inf_cols)} signs with endless values ♪

♪ 4. Filling out the remaining passes
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# 5. remove correlate features
 corr_matrix = df[numeric_cols].corr().abs()
 upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
 high_corr_cols = [column for column in upper_tri.columns if any(upper_tri[column] > correlation_threshold)]
 df = df.drop(columns=high_corr_cols)
prent(f" ♪ Removed {len(high_corr_cols)} correlate features (>{correllation_threshold*100}}}

 return df

# Demonstration of integrated engineering features
print("\n" + "="*80)
"Prent("♪ DEMONSTRUCTION: Integrated Engineering of the Signs")
print("="*80)

# of the complex set of topics
enhanced_data, feature_info = create_comprehensive_features(sample_data.copy())

# Analysis of results
Print(f)(n\\\\n\ANALYSIS OF RESULTS:)
spring(f "Basemarks: {feature_info['riginal_features']}})
(f) "Principle signs: {feature_info['final_features']}")
print(f" Extension factor: {feature_info['final_features'] /feature_info['riginal_features']:.1f}x)

# Showing examples of final features
(the last five days):)
final_examples = enhanced_data.select_dtypes(include=[np.number]).iloc[:, :10].tail()
print(final_examples)

# Statistics on types of indicators
(f) \n\\\\\\\\\\\\\\\\\\\\\\\\\\\\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\) \) \) \) \)
(f "Technical indicators: {feature_info['Technical_indicators']}})
(f "Statistical indicators: {feature_info['statistical_features']}})
(f "Temporary signs: {feature_info['time_features']}")
(f "Interactive topics: {feature_info['interaction_features']}})
(f "Trademarks: {feature_info['trade_features']}})

# Check data quality
Prent(f)\n\QUALITY OF DATA:)
print(f) "Dismissed values: {enhanced_data.isnull(.sum(.sum()}})
np.isinf(enhanced_data.select_dtypes(include=[np.number]].sum(.sum()})
pprint(f"Continuing characteristics: {(enhanced_data.nunique() <=1.sum()}})

"Prent(f"\n~ Integrated Design of Signs has been successfully completed!")
print(f"\\data ready for ML models)
```

## validation and sign testing

**Theory:** Once the signs have been created, they need to be validated to ensure that they are of good quality and suitability for machining.

```python
def validate_features(df, target_col='Close'):
 """
validation of the features created

Theory: Validation of topics includes checking:
1. Data quality (delays, emissions, distributions)
2. Statistical properties (correlation, stability)
3. Information (important for target variable)
4. Stability (time changes)
 """
"prent("\\calidation of topics...")

1. Basic statistics
("\n\l. Basic statistics:")
print(f" Data size: {df.scape}")
print(f" Missed values: {df.isnull(.sum(.sum()}})
Infinite values: {np.isinf(df.select_dtypes(include=[np.number]].sum(.sum()})

♪ 2. Correlation analysis
Print("\n\2: Correlation analysis:")
 numeric_cols = df.select_dtypes(include=[np.number]).columns
 corr_matrix = df[numeric_cols].corr()

# Find high correlations
 high_corr_pairs = []
 for i in range(len(corr_matrix.columns)):
 for j in range(i+1, len(corr_matrix.columns)):
 if abs(corr_matrix.iloc[i, j]) > 0.9:
 high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

(f) Highly corroded vapours (>0.9): {len(high_corr_pairs)}

# 3. Analysis of the importance of the topics
 if target_col in df.columns:
Print("\n~ 3. Analysis of the importance of the signs:")

# Data production
 feature_cols = [col for col in numeric_cols if col != target_col]
 X = df[feature_cols].fillna(0)
 y = df[target_col]

# Remove lines with blanks in target variable
 mask = ~y.isnull()
 X = X[mask]
 y = y[mask]

 if len(X) > 0:
# Random Forest is important
 rf = RandomForestRegressor(n_estimators=100, random_state=42)
 rf.fit(X, y)

# The top 10 of the important signs
 feature_importance = pd.dataFrame({
 'feature': feature_cols,
 'importance': rf.feature_importances_
 }).sort_values('importance', ascending=False)

"Top-10 important signs:")
 for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
 print(f" {i+1:2d}. {row['feature']:<30} {row['importance']:.4f}")

# 4. Distribution analysis
Spring("\n\4: Distribution analysis:")
for wheel in fire_cols[:5]: # Only the first 5
 if col in df.columns:
 print(f" {col}:")
(f "Medical: {df[col].mean(:4f}")
pprint(f" Std.out: {df[col].std(:4f}})
Min: {df[col].min(:4f}})
Max: {df[col].max(:4f}})
asymmetry: {df[col].skew(:4f}})
Print(f"Excess: {df[col]. kurtosis(:4f}})

 return {
 'shape': df.shape,
 'Missing_values': df.isnull().sum().sum(),
 'infinite_values': np.isinf(df.select_dtypes(include=[np.number])).sum().sum(),
 'high_correlations': len(high_corr_pairs),
 'feature_importance': feature_importance if 'feature_importance' in locals() else None
 }

# Calidation of the features created
print("\n" + "="*60)
"prent("\\calidation of the signs")
print("="*60)

validation_results = validate_features(enhanced_data)
```

## Next steps

Once the signs have been created and validated, go to:
- **[05_model_training.md](05_model_training.md)** - Training ML models
- **[06_backtesting.md](06_backtesting.md)** - Becketting strategies

## Key findings

1. ** Quantity of signs** is more important than number
2. ** Home knowledge** critical for creating effective signs
3. ** Automation** may help, but not replace the examination
4. **validation** indicators mandatory prior to model training
5. ** Interpretation** indicators are important for understanding the model
6. ** The integrated approach** produces better results than individual machines

---

The good signs are the basis of a successful ML model.
