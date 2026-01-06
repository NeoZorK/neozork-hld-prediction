# SCHR Livels AutoML - Guide on Use

## ♪ Review

SCHR Livels AutoML is an automated user-based modeling for data analysis by SCHR Lovels indicators.

1. ** `Pressure_vector_sign'**-Pedication sign PRESURE_VECTOR (positive/negative)
2. **'preception_direction_5periods'**-Pedication priority for 5 periods forward
3. **'level_breakout'** - PREDICTED_HIGH/PREDICTED_LOW

## 🚀 Quick start

###1 # A simple test
```bash
cd /Users/rostsh/Documents/DIS/REPO/neozork-hld-Prediction
uv run python test_schr_pipeline.py
```

♪##2 ♪ Full analysis
```bash
uv run python schr-levels-gluon.py
```

## ♪ The results of the last Analisis

### Model 1: Presure_vector_sign
- **Definity**: 61.76 per cent
- **Precision**: 68.68%
- **Recall**: 61.76%
- **F1-score**: 56.23%
- **Walk Forward**: 61.90% ± 13.61%
- **Monte Carlo**: 63.57% ± 10.14%
- **Stability**: 84.05 per cent

### Model 2: Price_direction_5periods
- **Definity**: 14.71%
- **Precision**: 2.16%
- **Recall**: 14.71%
- **F1-score**: 3.77%
- **Walk Forward**: 28.57% ± 7.01%
- **Monte Carlo**: 35.35% ± 16.40%
- **Stability**: 53.60%

### Model 3: Live_breakout
- **Definity**: 67.65 per cent
- **Precision**: 68.26%
- **Recall**: 67.65%
- **F1-score**: 67.66%
- **Walk Forward**: 63.49% ± 2.24%
- **Monte Carlo**: 52.80% ± 12.09%
- ** Stability**: 77.10 per cent

## ♪ Use in code

### Basic use
```python
from schr_levels_gluon import SCHRLevelsAutoMLPipeline

# Creating Pipeline
pipeline = SCHRLevelsAutoMLPipeline()

# Loading data
data = pipeline.load_schr_data('BTCUSD', 'MN1')

# Creating target variables
data = pipeline.create_target_variables(data)

# Creating the signs
data = pipeline.create_features(data)

# Learning the model
results = pipeline.train_model(data, 'pressure_vector_sign')
pint(f "Totality: {results['metrics']['accuracy':2%}")

# We're doing Predation
Prediction = pipeline.predict(data.tail(1), 'pressure_vector_sign')
print(f"Prediction: {Prediction.iloc[0]}")
```

### Premonitions for trading
```python
# Detailed predictions with probabilities
trading_pred = pipeline.predict_for_trading(data.tail(1), 'pressure_vector_sign')
print(f"Prediction: {trading_pred['predictions'].iloc[0]}")
Print(f"Probability: {trade_pred['probabilities'].iloc[0].to_dict()})
```

♪# # Validation of models
```python
# Walk Forward validation
wf_results = pipeline.walk_forward_validation(data, 'pressure_vector_sign', n_splits=5)
prent(f"Average accuracy: {wf_results['mean_accuracy']:2%}})

# Monte Carlo validation
mc_results = pipeline.monte_carlo_validation(data, 'pressure_vector_sign', n_iterations=10)
prent(f"Average accuracy: {mc_results['mean_accuracy']:2%}})
```

## 📁 File Structure

```
models/schr_levels_production/
== sync, corrected by elderman == @elder_man
♪ Price_direction_5periods_model.pkl # Model for predicting pric direction
# Model for predicting levels
== sync, corrected by elderman == @elder_man

Logs/
== sync, corrected by elderman == @elder_man

results/
* Graphs and visualizations
```

## ♪ Accessible data

### Symbols
- BTCUSD, GBPUSD, EURUSD, and others

### Timeframes
- MN1 (monthly), W1 (weekly), D1 (day)
- H4 (4-hour), H1 (hour)
- M15 (15-minutes), M5 (5-minutes), M1 (minutes)

### uploading different data
```python
# Different symbols
data_btc = pipeline.load_schr_data('BTCUSD', 'MN1')
data_gbp = pipeline.load_schr_data('GBPUSD', 'MN1')

# Different Timeframes
data_daily = pipeline.load_schr_data('BTCUSD', 'D1')
data_hourly = pipeline.load_schr_data('BTCUSD', 'H4')
```

## \configuring parameters

### Time of study
```python
# Rapid learning (5 minutes)
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=300)

# Quality education (30 minutes)
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=1800)
```

### Deletion of models
```python
# In Schr-levels-gluon.py file you can set:
fit_args = {
'Excluded_model_types': ['NN_TORCH', 'FASTAI'] # Delete neural networks
'Use_gpu':False, # Disable GPU
 'num_gpus': 0
}
```

♪ ♪ Analysis of results

### check data quality
```python
# Statistics on target variables
"Target_pv_sign:")
print(data['target_pv_sign'].value_counts())

"Target_price_direction:")
print(data['target_price_direction'].value_counts())
```

### The importance of signs
```python
# Get the importance of the signs
feature_importance = pipeline.get_feature_importance('pressure_vector_sign')
print(feature_importance.head(10))
```

## ♪ Overcoming problems

### Mistake "No dry file or direction"
```bash
# Check the file files
ls data/cache/csv_converted/
```

### Mistake "Not Enough Data"
```python
# Check the data size
"data measurement: {len(data)} records")
(pint(f"Calls: {List(data.columns)})
```

### Low model accuracy
```python
# Try to increase your learning time
results = pipeline.train_model(data, 'pressure_vector_sign', time_limit=3600) #1 hour
```

## * * examples of use

### Daily analysis
```python
# Loading fresh data
data = pipeline.load_schr_data('BTCUSD', 'D1')
data = pipeline.create_target_variables(data)
data = pipeline.create_features(data)

# Learning the model
results = pipeline.train_model(data, 'pressure_vector_sign')

# We're doing Predation on tomorrow
tomorrow_Prediction = pipeline.predict(data.tail(1), 'pressure_vector_sign')
"Tomorrow PRESURE_VECTOR will be: {'positive' if tomorrow_Predication.iloc[0] = = 1 else 'negative'})
```

### Analysis of different Times
```python
Timeframes = ['MN1', 'W1', 'D1', 'H4']

for tf in timeframes:
 data = pipeline.load_schr_data('BTCUSD', tf)
 data = pipeline.create_target_variables(data)
 data = pipeline.create_features(data)

 results = pipeline.train_model(data, 'pressure_vector_sign')
Print(f) {tf}: Accuracy {results['metrics']['accuracy':2%}})
```

♪ ♪ Ready scripts ♪

♪ ♪ Quick test
```bash
uv run python test_schr_pipeline.py
```

### Full analysis
```bash
uv run python schr-levels-gluon.py
```

### Castle analysis
```python
# Make your script
from schr_levels_gluon import SCHRLevelsAutoMLPipeline

pipeline = SCHRLevelsAutoMLPipeline()
data = pipeline.load_schr_data('BTCUSD', 'MN1')
data = pipeline.create_target_variables(data)
data = pipeline.create_features(data)

# Learning all 3 models
for task in ['pressure_vector_sign', 'price_direction_5periods', 'level_breakout']:
 results = pipeline.train_model(data, task)
Print(f) {task}: Accuracy {results['metrics']['accuracy': 2 per cent}})
```

## ♪ Support

In case of problems:
1. Check Logs in `Logs/' folder
2. Make sure the data are loaded correctly
3. Check the priority all dependencies: `uv run pip List'

---

** Last update**: 28 September 2025
** Version**: 1.0.0
