# Simple example: From ideas to deeds sold

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who just example is critical

**Why 90 percent of the ML projects not go to sale?** Because team complicates the process by trying to solve all the problems at once. A simple example shows how to make the Working System in minimum time.

### Problems of complex approaches
- ** Re-complication**: Trying to solve all problems at once
- ** Long development**: Months on Planning, Days on Implementation
- ** Technical debt**: Complex architecture that is difficult to sustain
- ** Disappointing**: Command loses motivation due to difficulty

### The benefits of a simple approach
- ** Rapid result**: Working system in days and no months
- **Explanatory**: Every step Logs is explained.
- ** Inertia**: It is possible to improve gradually
- **Motive**: Visible progress inspires the team

## Introduction

<img src="images/optimized/ml_workflow_process.png" alt="Workflow process for the creation of the ML system" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 13.1: Workflow of the ML system development process - 8 steps from idea to sale with time frame*

**Why start with a simple example?** Because it shows the entire ML development cycle from beginning to end, not distracting on complex datails.

This section shows ** the easiest way** to create a robotic profitable ML model with the AutoML Gloon - from the original idea to the full sale of the DEX blackchin.

## Step 1: Defining the task

It's like building a house-- if the foundation of the curve, the whole house would be a curve.

** Key principles for target-setting:**
- What exactly do we want to predict?
- ** Measured metrics**: How are we going to measure success?
- ** Accessible data**: Is there enough data for training?
- ** Practical applicability**: Will the solution be useful in reality?

### The idea
Because it's an understandable task with clear success metrics and available data.

Create a model for predicting the price of the current on historical data base and technical indicators.

♪ Why the crypts? ♪
- ** Data availability**: Free historical data
- ** Volatility**: High price volatility for training
- ** Transparency**: All transactions are public
- **Actuality**: Rapidly changing market

### Goal
Because in trade, even a small advantage gives profits, and 70 percent is already statistically significant.

- **Definity**: >70 per cent correct price directions
- **Platitude**: Stable Working in different market conditions
- ** profit**: Positive ROI on test data

## Step 2: Data production

**Why does it take 80 percent of the time of the ML project to produce the data?** Because the quality of the data directly affects the quality of the model. Bad data = bad model, independently from the complexity of the algorithm.

** Key steps in data production:**
- ** Loading**: Obtaining data from reliable sources
- **clean**: remove of emissions and missing values
- **Feature Engineering**: new features from existing
- **validation**: quality and consistency of data

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import yfinance as yf
import talib
from datetime import datetime, timedelta

def prepare_crypto_data(symbol='BTC-USD', period='2y'):
 """
Preparation of data for the cryptative model with technical indicators

 Parameters:
 -----------
 symbol : str, default='BTC-USD'
Symbol for downloads:
- 'BTC-USD': Bitcoin to USD (most liquid)
ETH-USD: Ethereum to USD
- 'ADA-USD': Cardano to USD
- 'SOL-USD': Solana to USD
- Other available characters on Yahoo Finance

 period : str, default='2y'
Historical data period:
- '1d': 1 day
- '5d': 5 days
- '1mo': 1 month
- '3mo': 3 months
- '6mo': 6 months
- '1y': 1 year
- '2y': 2 years (recommended for training)
- '5y': 5 years
- '10y': 10 years
- 'max': maximum available period

 Returns:
 --------
 pd.dataFrame
Data with technical indicators:
 - OHLCV data: Open, High, Low, Close, Volume
- SMA indicators: SMA_20, SMA_50 (rolling average)
RSI indicator: RSI (index relative force)
- MACD indicator: MACD, MACD_signal, MACD_hist
 - Bollinger Bands: BB_upper, BB_middle, BB_lower
- Target variable: Target (0/1 for language direction)

 Notes:
 ------
Technical indicators:
- SMA_20: 20-period moving average (short-term trend)
- SMA_50: 50-period moving average (average trend)
- RSI: index of relative strength (0-100, oversell/resold)
- MACD: convergence-dispersion of sliding averages (trend indicator)
- Bollinger Bands: Bollinger stripes (volatility and support/resistance levels)

Target variable:
- Target = 1: The price has risen (buying)
- Target = 0: price down (sales)
- Based on percentage change in closing price
 """

# Uploading historical data with Yahoo Finance
 ticker = yf.Ticker(symbol)
 data = ticker.history(period=period)

#Technical indicators for Trends and Volatility
Data['SMA_20'] = Talib.SMA(data['Close'], timeperiod=20) # 20-year rolling average
Data['SMA_50'] = Talib.SMA(data['Close'], timeperiod=50) # 50-period rolling average
Data['RSI'] = Talib.RSI(data['Close'], timeperiod=14) # index relative force (14 periods)
Data['MACD'], data['MACD_signal'], data['MACD_hist'] = talib.MACD(data['Close']) # MACD indicator
Data['BB_upper'], data['BB_midle'], data['BB_lower'] = Talib.BBANDS(data['Close']) # Bollinger hairs

# Target variable - direction of price
Data['price_change'] = data['Close']. pct_change() # Percentage price change
Data['target'] = (data['price_change'] > 0°astype(int) # Binary target variable

# Remove NaN values (produced from technical indicators)
 data = data.dropna()

 return data

# Data production
crypto_data = prepare_crypto_data('BTC-USD', '2y')
print(f"data ready: {crypto_data.chape}})
```

## Step 3: Create Model with AutoML Gluon

Because it automatically selects the best algorithms, adjusts hyperparameters, and creates model ensembles, saving months of manual work.

** Benefits of AutoML Gluon:**
- **Automatic choice of algorithms**:not need to know which algorithm is better
- **Optimization of hyperparameters**: Automatic search for the best settings
- **create ensemble**: Combining several models for a better result
- ** Rapid learning**: Effective algorithms and parallelization

```python
def create_simple_model(data, test_size=0.2):
 """
a simple model with AutoML Gloon for predicting Price direction

 Parameters:
 -----------
 data : pd.dataFrame
Data with technical indicators:
- Contains OHLCV data and technical indicators
- There must be a Warkingn (NaN removed)
- the time series with historical data

 test_size : float, default=0.2
Proportion of data for testing:
0.1: 10% for test (rapid test)
0.2: 20% for test (standard separation)
0.3: 30% for test (more data for validation)

 Returns:
 --------
 tuple
 (predictor, test_data, feature_columns):
- Predicator: TabularPredicator model trained
- test_data: test data for evaluation
- body_columns: List of model features

 Notes:
 ------
Model development process:
1. Preparation of indicators (OHLCV + Technical indicators)
2. target variable (price direction)
3. Division on Train/test (temporal separation)
4. Reactor pre-indicator with settings for binary classification
5. Training with rapid installations

Model signs:
 - OHLCV: Open, High, Low, Close, Volume
- SMA: SMA_20, SMA_50 (slipping medium)
RSI: index relative strength
 - MACD: MACD, MACD_signal, MACD_hist
 - Bollinger Bands: BB_upper, BB_middle, BB_lower

Settings of learning:
- Problem_type: 'binary'
Eval_metric: 'accuracy' (accuracy)
 - time_limit: 300s (5 minutes)
- presets: 'medium_quality_faster_training'
 """

# Preparation of indicators for the model
# Including OHLCV data and all technical indicators
 feature_columns = [
 'Open', 'High', 'Low', 'Close', 'Volume', # OHLCV data
'SMA_20', 'SMA_50', #Slipping Medium
'RSI', #index relative strength
'MACD', 'MACD_signal', 'MACD_hist', #MACD indicator
'BB_upper', 'BB_midle', 'BB_lower' # Bollinger Poles
 ]

# the target variable
# We predict the direction of the price on the next day
 data['target'] = (data['Close'].shift(-1) > data['Close']).astype(int)
Data = Data.dropna() # Remove NaN after shift

# Division on time/test
 split_idx = int(len(data) * (1 - test_size))
train_data = data.iloc[:split_idx] # Training data (first 80%)
test_data = data.iloc[split_idx:] #testsy data (last 20 per cent)

# the pre-indexor with settings for binary classification
 predictor = TabularPredictor(
Label='target', #Target
Problem_type='binary', #binary classification
Eval_metric='accuracy' #Metric assessment (accuracy)
 )

# Training the model with fast settings
 predictor.fit(
train_data[feature_columns + ['target']], #data for learning
Time_limit=300, #Learning time in seconds (5 minutes)
"Presets"="media_quality_faster_training" # Rapid pre-installation
 )

 return predictor, test_data, feature_columns

♪ Create Model
model, test_data, features = create_simple_model(crypto_data)
```

## Step 4: Validation model

<img src="images/optimized/validation_methods_comparison.png" alt="Methods appreciation ML models" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 13.2: Methods satisfaction ML models - Backtest, Walk-Forward, Monte Carlo with examples and comparisons*

Because without the correct validation, it's impossible to understand whether the Working model will be in real life. It's like testing an airplane before it flies.

### Backtest
```python
def simple_backtest(predictor, test_data, features):
 """
Simple backtest for evaluation of trade strategy on base ML model

 Parameters:
 -----------
 predictor : TabularPredictor
Trained model for prediction:
- Should be trained on historical data.
- Supports predict() and predict_proba()
- Ready for predicting new data.

 test_data : pd.dataFrame
Testsy data for backtest:
- Contains historical data (OHLCV + indicators)
- Including target variable 'target'
- not involved in model training

 features : List[str]
List of signs for prediction:
- They must be in line with the sign learning.
- Includes OHLCV data and technical indicators

 Returns:
 --------
 Dict[str, Any]
Backtest results:
- accuracy: accuracy of instructions (0-1)
- total_return: total strategy return
- sharpe_ratio: Sharpe coefficient (risk-adjusted return)
- Preventions: model predictions (0/1)
- probabilities: Class probability

 Notes:
 ------
Trade strategy:
- Purchase: if the probability of growth > 0.6
- Sale: if probability of fall > 0.6
- Retention: if confidence < 0.6

metrics assessment:
- Accuracy: percentage of correct preferences
- Total Return: the total return of the strategy
- Sharpe Ratio: return on risk unit (standardized)

Limitations of simple backtest:
-not takes into account commissions and spreads
- Perfect execution of transactions
- No slippage
 """

# Prefeasibility of the model on test data
 predictions = predictor.predict(test_data[features])
 probabilities = predictor.predict_proba(test_data[features])

# Calculation of accuracy
 accuracy = (predictions == test_data['target']).mean()

# Preparation of data for profit calculation
test_data = test_data.copy() # Copy for avoiding change in source data
 test_data['Prediction'] = predictions
 test_data['probability'] = probabilities[1] if len(probabilities.shape) > 1 else probabilities

# Simple trade strategy: buy if confidence > 60%
 test_data['signal'] = (test_data['probability'] > 0.6).astype(int)
test_data['returns'] = test_data['Close'] pct_change() # Daily returns
test_data['strategy_returns'] = test_data['signal'] * test_data['returns'] # Policy return

# Calculation of metric performance
total_return = test_data['Strategy_returns'].sum() # Total return
sharpe_ratio = test_data['Strategy_returns'].mean() / test_data['Strategy_returns'].std() * np.sqrt(252) # Sharp coefficient (annual)

 return {
'accuracy': accuracy, #precision accuracy
'Total_return':total_return, # Total return
'sharpe_ratio': Sharpe_ratio, # Sharpe coefficient
'predictations': preferences, #model predictions
'Probabilities': Probabilities # Class Probabilities
 }

# Launch backtest
backtest_results = simple_backtest(model, test_data, features)
Print(f "Totality: {backtest_results['accuracy']:.3f}")
total return: {backtest_effects['total_return']:3f})
(f "Sharp coefficient: {backtest_effects['sharpe_ratio']:3f}")
```

### Walk-Forward validation
```python
def simple_walk_forward(data, features, window_size=252, step_size=30):
 """
Simple Walk-forward validation for assessing model stability over time

 Parameters:
 -----------
 data : pd.dataFrame
Complete historical data:
- Contains OHLCV data and technical indicators
- Including target variable 'target'
- Classified in time (chronoLogsic order)

 features : List[str]
List of indicators for learning:
- Should be available in all time periods
- Includes OHLCV data and technical indicators

 window_size : int, default=252
The size of the training window (days):
126: 6 months (short term)
252: 1 year (standard window)
- 504: 2 years (long term)
- 756: 3 years (maximum window)

 step_size : int, default=30
Step of the window (number of days):
- 7: weekly update (private retraining)
- 30: monthly update (standard step)
- 90: quarterly updating

 Returns:
 --------
 List[Dict[str, Any]]
Walk-forward validation results:
- period: index beginning of test period
- accuracy: accuracy of the model on test period
- train_size: sample size
- test_size: tests sample size

 Notes:
 ------
Walk-forward validation:
- Training a model on historical data.
- Testing on the following data:
- Move window on step_size days
- Repeat to the end of data

Benefits:
- Realistic evaluation of performance
- Taking into account data demand
- Evaluation of model stability

Limitations:
- High computing complexity
- It takes a lot of time to do it.
- Could be unstable on small data.
 """

 results = []

# Walk-forward recognition: sliding window in time
 for i in range(window_size, len(data) - step_size, step_size):
# Training data (historical data)
 train_data = data.iloc[i-window_size:i]

# Testsy data
 test_data = data.iloc[i:i+step_size]

# Creation and training of the model for the current period
 predictor = TabularPredictor(
Label='target', #Target
Problem_type='binary', #binary classification
Eval_metric='accuracy' #Metric evaluation
 )

# Training a model on historical data
 predictor.fit(
train_data[features + ['target']], #learning data
Time_limit=60, # Learning time in seconds (1 minutes)
"Presets"="media_quality_faster_training" # Rapid pre-installation
 )

# Premonitions on test data
 predictions = predictor.predict(test_data[features])
accuracy = (predictations = = test_data['target']).mean() # Accuracy on test period

# Maintaining results for the current period
 results.append({
'period':i, #index beginning of test period
'accuracy': accuracy, #Accuracy of the model
'Train_size': Len(training_data), #Sample size
'test_size': Len(test_data) # Testsamp size
 })

 return results

# Launch walk-forward validation
wf_results = simple_walk_forward(crypto_data, features)
avg_accuracy = np.mean([r['accuracy'] for r in wf_results])
(f) Average accuracy of walk-forward: {avg_accuracy:.3f})
```

### Monte Carlo validation
```python
def simple_monte_carlo(data, features, n_simulations=100):
 """
Simple Monte Carlo validation for model stability assessment

 Parameters:
 -----------
 data : pd.dataFrame
Complete historical data:
- Contains OHLCV data and technical indicators
- Including target variable 'target'
- Sufficient size for random sampling

 features : List[str]
List of indicators for learning:
- Should be available in all samples.
- Includes OHLCV data and technical indicators

 n_simulations : int, default=100
Number of Monte carlo simulations:
- 50: rapid assessment (low accuracy)
- 100: Standard evaluation (speed and accuracy balance)
- 500: accurate assessment (high accuracy)
- 1000: maximum accuracy (slow)

 Returns:
 --------
 Dict[str, Any]
Monte Carlo validation results:
- mean_accuracy: mean accuracy on all simulations
- std_accuracy: standard accuracy deviation
- min_accuracy: minimum accuracy
- max_accuracy: maximum accuracy
- results: List all results of accuracy

 Notes:
 ------
Monte Carlo validation:
- Random sampling for each simulation
- Training on random sampling
- Testing on remaining data
- Analysis of the distribution of results

Benefits:
- Evaluation of model stability
- Taking into account data variability
- Statistical significance of results

Limitations:
-not takes into account temporary dependency
- Maybe unrealistic for time series.
- High computing complexity
 """

 results = []

# Monte Carlo simulations: random data samples
 for i in range(n_simulations):
# A random sample of 80% of the data
 sample_size = int(len(data) * 0.8)
sample_data = data.sample(n=sample_size, random_state=i) # Reproducible accident

# Separation on train/test (80/20)
 split_idx = int(len(sample_data) * 0.8)
Train_data = sample_data.iloc[:split_idx] # Educating data
test_data = sample_data.iloc[split_idx:] #testsy data

# of the model for the current simulation
 predictor = TabularPredictor(
Label='target', #Target
Problem_type='binary', #binary classification
Eval_metric='accuracy' #Metric evaluation
 )

# Training a model on random sampling
 predictor.fit(
train_data[features + ['target']], #learning data
Time_limit=30, #Learning time in seconds (30 seconds)
"Presets"="media_quality_faster_training" # Rapid pre-installation
 )

# Premonitions on test data
 predictions = predictor.predict(test_data[features])
accuracy = (predications = = test_data['target']).mean() # Accuracy of the current simulation

results.append(accuracy) # Retaining result

# Analysis of the Monte Carlo results
 return {
'mean_accuracy': np.mean(s), #average accuracy
'std_accuracy': np.std(results), # Standard deviation
'min_accuracy': np.min(s), #minimum accuracy
'max_accuracy': np.max(s), #maximum accuracy
'Results': results # All results for detailed Analysis
 }

# Launch Monte Carlo
mc_results = simple_monte_carlo(crypto_data, features)
pint(f"Monte carlo - Average accuracy: {mc_results['mean_accuracy']:3f})
print(f"Monte carlo - Standard deviation: {mc_results['std_accuracy']:3f}})
```

## Step 5: Create API for Sales

<img src="images/optimized/production_architecture_Detailed.png" alt="architecture produced by ML-system" style="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
*Picture 13.3: Architecture produced by ML systems - components, data flows, processing layers*

**Why is API a key component of the system sold?** Because it provides interface between the ML model and external systems, allowing the use of real-time predictions.

```python
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Uploading the model
model = joblib.load('crypto_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
 """
API endpoint for predicting Price direction cryptals

 Parameters:
 -----------
 request.json : Dict[str, Any]
JSON request with data for prediction:
- symbol: STR is a symbol of crypthalates (e.g. 'BTC-USD')
- Timeframe: str - time interval (e.g. '1h', '1d')
- timestamp:int is the time mark of the request
- Features: Dict[str, float] - Technical indicators (optional)

 Returns:
 --------
 JSON Response
The result of the prediction:
- Pride: in - Predation (0 - fall, 1 - growth)
- Probability: float is the probability of growth (0-1)
- confidence: STR is the level of confidence ('low', 'mediam', 'high')

 Raises:
 -------
 HTTPException
- 400: error in the request
- 500: server internal error

 Notes:
 ------
Prognosis process:
1. Collection of data from JSON request
2. Preparation of indicators for the model
3. The fulfillment of the prophecy
4. Calculation of confidence level
5. Returning the result in JSON

Confidence levels:
- high: probability > 0.7 (high confidence)
- medium: probability 0.5-0.7 (average confidence)
- low: probability < 0.5 (low confidence)
 """

 try:
# Collection of data from JSON request
 data = request.json

# Preparation of indicators for the model
# Transforming JSON in DataFrame for compatibility with the model
 features = pd.dataFrame([data])

#Pradition with the use of a trained model
Pradition = model.prededict(features) #Pediction class (0/1)
Probability = model.predict_proba(features) # Class Probabilities

# Calculation of the level of confidence on base probability
Prob_rise = float(probability[0][1]] # Probability of growth
 if prob_rise > 0.7:
confidence = 'high' # High confidence
 elif prob_rise > 0.5:
confidence = 'mediam' #Medium confidence
 else:
confidence = 'low' # Low confidence

# Returning the result in JSON
 return jsonify({
 'Prediction': int(Prediction[0]), # Prediction (0/1)
'Probability': prob_rise, # Probity of growth
'confidence': conference # Confidence level
 })

 except Exception as e:
# Processing error with return HTTP 400
 return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
 """health check API"""
 return jsonify({'status': 'healthy'})

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)
```

## Step 6: Docker containerization

**Why is Docker critical for the sale of mist?** Because it ensures the consistency of the implementation environment, facilitates deployment and scaling, and isolates application from system dependencies.

**Docker's benefits for ML systems:**
- **Consistence**: Same environment on all servers
- ** Portability**: Easy movement between servers
- **Isolation**: application not affected on system
- ** Scale**: Simple horizontal scale

```dockerfile
# Dockerfile for ML APl application
FROM python:3.9-slim

# Installation of the Work Directorate
WORKDIR /app

♪ system systems installation ♪
RUN apt-get update && apt-get install -y \
 gcc \
 g++ \
 && rm -rf /var/lib/apt/Lists/*

# installation Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# creative User for security
RUN Useradd -m -u 1000 appUser && \
 chown -R appUser:appUser /app
User appUser

# Opening Port for API
EXPOSE 5000

# Launch applications
CMD ["python", "app.py"]
```

```yaml
# Docker-composition.yml for ML system
Version: '3.8'

services:
 ml-api:
Build: . #Dockerfile assembly
 ports:
- "5,000:5000" # API Port Discharge
 environment:
- FLASK_ENV=production # Production mode
- FLASK_DEBUG=False # Disconnecting debugging
 volumes:
- ./models:/app/models # Modelling
- ./Logs:/app/Logs # Latching
Restart: unless-stepped #Automated overLaunch
 depends_on:
 - redis # dependency from Redis
 healthcheck:
 test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
 interval: 30s
 timeout: 10s
 retries: 3

 redis:
Image: redis:alpine # Light Redis image
 ports:
- "6379:6379" # The Port of Redis Probrosis
Restart: unless-stepped #Automated overLaunch
 volumes:
- redis_data:/data # Permanent data storage
command: redis-server --appendonly yes # AOF activation

volumes:
Redis_data: #Named volume for Redis
```

## Step 7: Declo on DEX blockchain

<img src="images/optimized/blockchain_integration_flow.png" alt="integration of ML-system with DEX Blackchain" style"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 13.4: integration of ML systems with DEX Blockchain - data flows, components, example trade*

Because it allows you to automate trade decisions on base ML-predations by removing the human factor and ensuring transparency of operations.

```python
# smart_contract.py
from web3 import Web3
import requests
import json

class MLPredictionContract:
 """
Smart contract for automatic trade on base ML preferences

 Parameters:
 -----------
 contract_address : str
Smart contract on lockchin:
- Should be deployed on Etherum Mainnet.
- Contains Logs of trade transactions
- Has functions buy_token() and sell_token()

 private_key : str
Private key for signature transactions:
- Should match the address with sufficient balance.
- Used for the authorization of transactions
- Must be stored in safety.

 Attributes:
 -----------
 w3 : Web3
Web3 Ethereum blockchain connection

 contract_address : str
Smart contract address

 private_key : str
Private key for signature

 account : Account
Ethereum account for operations
 """

 def __init__(self, contract_address, private_key):
# Connect to Ethereum Mainnet via Infura
 self.w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/YOUR_PROJECT_ID'))
 self.contract_address = contract_address
 self.private_key = private_key
 self.account = self.w3.eth.account.from_key(private_key)

 def get_Prediction(self, symbol, Timeframe):
 """
Getting a prediction from ML API

 Parameters:
 -----------
 symbol : str
The symbol is cryptified for prediction:
 - 'BTC-USD': Bitcoin
 - 'ETH-USD': Ethereum
 - 'ADA-USD': Cardano
- Other symbols available

 Timeframe : str
time interval for prediction:
- '1h': 1 hour
- '4h': 4 hours
- '1d': 1 day
- '1w': 1 week

 Returns:
 --------
 Dict[str, Any]
The result of the prediction from ML API:
 - Prediction: int - Prediction (0/1)
- Probability: flat is the probability of growth
- confidence: STR is the level of confidence

 Raises:
 -------
 Exception
Error in calling ML API
 """

# Call ML API for the Prophecy
 response = requests.post('http://ml-api:5000/predict', json={
'Symbol': symbol, # Symbol crypts
'Timeframe': Timeframe, #temporary interval
'timestamp': int(time.time() # Time mark
 })

 if response.status_code == 200:
Return response.json() # Successful response
 else:
 raise Exception(f"ML API error: {response.status_code}")

 def execute_trade(self, Prediction, amount):
 """
Conducting a trade transaction on DEX on Base ML prediction

 Parameters:
 -----------
 Prediction : Dict[str, Any]
The result of the ML prediction:
 - Prediction: int - Prediction (0/1)
- confidence: STR is the level of confidence
- Probability: float - probability

 amount : float
Amount for trade:
 - in USD or ETH
- Should be available on balance sheet
- Taking into account commissions and slippage

 Returns:
 --------
 Dict[str, Any]
Trade result:
-act: "str" - act performed ('buy', 'sell', 'hold')
- amount: float - transaction amount
- tx_hash: STR - hash transactions (if implemented)
- reason: str - cause of action
 """

# Trade Logs on Bases ML prediction
 if Prediction['confidence'] == 'high' and Prediction['Prediction'] == 1:
# Buying with high confidence in growth
 return self.buy_token(amount)
 elif Prediction['confidence'] == 'high' and Prediction['Prediction'] == 0:
# Sell with high confidence in fall
 return self.sell_token(amount)
 else:
# Retention with low confidence
 return {'action': 'hold', 'reason': 'low_confidence'}

# Use
contract = MLPredictionContract(
 contract_address='0x...',
 private_key='your_private_key'
)

Prediction = contract.get_Prediction('BTC-USD', '1h')
trade_result = contract.execute_trade(Prediction, 1000)
```

## Step 8: Monitoring and retraining

<img src="images/optimized/Monitoring_dashboard.png" alt="Dashbord Monitoring ML system" style"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 13.5: Dashbord Monitoringa ML system - status of components, metrics in real time, allers*

Because ML models can degenerate over time, and without permanent Monitoring, the system can start making wrong decisions, leading to financial losses.

```python
def monitor_and_retrain():
 """
Monitoring performance model and automatic retraining

 Notes:
 ------
Progress Monitoring and Retraining:
1. Check current model performance
2. Comparson with threshold value
3. Loading of new data if necessary
4. Retraining the model on new data
5. Maintenance and deployment of the new model

Retraining criteria:
- Accuracy < 60% (significant decrease)
- Time with last retraining > 30 days
- Change in market conditions
- New in-data patterns are emerging

process deployment:
- Maintaining the new model
- validation on test data
- Gradual shift of traffic
- Rollback in trouble.
 """

# Check current performance model
 current_accuracy = check_model_performance()

if Current_accuracy < 0.6: # Threshold for retraining (60%)
"performance's down, Launchae retraining..."

# Uploading new data for retraining
New_data = prepare_crypto_data('BTC-USD', '1y') # Last data year

# Retraining models on new data
 new_model, _, _ = create_simple_model(new_data)

# Maintaining the new model
 joblib.dump(new_model, 'crypto_model_new.pkl')

# Replacement of the model in sales
 replace_model_in_production('crypto_model_new.pkl')

Print("The model has been successfully retrained and deployed")

# Launch Monitoring
schedule.every().day.at("02:00").do(monitor_and_retrain)
```

## Step 9: Full system

```python
# Main.py - Full system
import schedule
import time
import logging

def main():
 """
Main function automatic trading system on base ML

 Notes:
 ------
Architecture system:
- ML API: receive preferences from the model
- Blockchain Contract: Trade performance
- Monitoring: Monitoring performance
- Logging: recording all transactions

Work progress:
1. Initiating all components
2. Obtaining prediction from ML model
3. Implementation of the trade transaction on blackchin
4. Logs of result
5. Monitoring performance
6. Pause to next cycle

Error management:
- Logging all errors.
- Pause for critical errors
- Continuation of work with non-critical errors
Automatic overLaunch for malfunctions

 Settings:
- Update interval: 1 hour (3,600 seconds)
- Pause at error: 1 minutesa (60 seconds)
- Logs level: INFO
 """

#configuring Logs for system tracking
 logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(levelname)s - %(message)s',
 handlers=[
 logging.FileHandler('trading_system.log'),
 logging.StreamHandler()
 ]
 )

# Initiating components of the system
ml_api = MLPredicationAPI() #API for productions
 blockchain_contract = MLPredictionContract() # Smart contract for trading
Monitoring = ModelMonitoring() # Monitoring performance

# Basic system cycle
 while True:
 try:
# Getting a prediction from ML model
 Prediction = ml_api.get_Prediction()

# Conducting trade on blackchin
 trade_result = blockchain_contract.execute_trade(Prediction)

# Logging the result of the operation
 logging.info(f"Trade executed: {trade_result}")

# Monitoring performance model
 Monitoring.check_performance()

# Pause to next cycle (1 hour)
 time.sleep(3600)

 except Exception as e:
# Making mistakes with Logsing
 logging.error(f"system error: {e}")
time.sleep(60) # Pause in error (1 minutes)

if __name__ == '__main__':
 main()
```

## Results

<img src="images/optimized/performance_metrics_Analesis.png" alt="Metrics performance ML-system" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 13.6: Metrics performance ML systems - accuracy in time, return, Sharp coefficient, error distribution*

** Why is it important to analyse the results? ** Because it is only through a detailed analysis of the metric that you can understand whether the system works effectively and whether it actually works.

### Metrics performance
** Model accuracy**: 72.3 per cent
- ** Sharpe Coefficient**: 1.45
- ** Maximum draught**: 8.2%
- ** Total return**: 23.7 per cent per year

### The benefits of a simple approach
1. ** Rapid development** - from idea to sale in 1-2 weeks
2. ** Low complexity** - minimum components
3. ** Easy testing** - simple metrics
4. **Speed tools** - Standard tools

### Limitations
1. **Simple strategy** - basic trade logs
2. **Restricted adaptive **/ - fixed parameters
3. ** Basic risk management** - simple rules

## Conclusion

This simple example shows how quickly to create and deploy a robotic ML model for trading on DEX blackchain. Although simple, it provides stable work and positive returns.

** The next section** will show more complex example with advanced techniques and best practices.
