# Guide on learning the textbook

**Author:** NeoZorK (Shcherbyna Rostyslav)
**Date:** 2025
** Location:** Ukraine, Zaporizhzhya
**Version:** 1.0

## Who Guide on Study Critical

**Why do 90% of people drop out of the ML study, not having a clear Plan?** Because they try to study everything at once, not understanding what to start with and how to move forward. It's like trying to build a house without drawings.

### Problems without a study guide
- ** Transfer of information**: Try to study everything at once
- ** Wrong sequence**: Studying complicated to simple
- ** Absence of practice**: Only theory without application
- ** Loss of motivation**: not seeing progress

### The benefits of good leadership
- ** Step-by-step study**: from simple to complex
- ** Practical focus**: The theory is applied immediately
- ** Measured progress**: See results on each stage
- **motivation**: a constant sense of achievement

## Introduction

Because it shows the best way to study, given your level of preparation and your goals.

This guide will help you to learn the AutoML Gloon in Dependencies from your level of training and goals as effectively as possible.

## for new recruits (0-6 months of experience)

Because they don't understand the basics of ML and can easily get confused in complex Conceptch. We need a step-by-step approach with quick results.

### ♪ The way to learn for the newbies

```mermaid
graph TD
A [Initiated] -> B {Selection of the path}
B--~~Quick start~ C[1-2 weeks]
B-~ ♪ Full study ♪ D[1-2 months]

C --> C1[Day 1-2: Basics]
C --> C2 [Day 3-4: Understanding]
C --> C3 [Day 5-7: validation]
C --> C4 [Day 8-10: Sales]
C --> C5 [Day 11-14: Deepening]

D -> D1 [ Week 1: Basics]
D -> D2 [Welcome 2: Evaluation and validation]
D -> D3 [week 3: Sales]
D -> D4 [week 4: advanced themes]

C1-> E[First example]
C2 --> F[create model]
C3 --> G[validation model]
C4 --> H [Business in sales]
C5 --> I [system with re-education]

D1 -> J[3-5 simple models]
D2 --> K [full validation]
D3 --> L [Sell system]
D4 -> M [Achievable objective]

E --> N [Success!]
 F --> N
 G --> N
 H --> N
 I --> N
 J --> N
 K --> N
 L --> N
 M --> N
```

### ♪ Quick start (1-2 weeks)

Because they have to see the results as quickly as possible in order not to lose motivation.

**Goal:** Start the first example as soon as possible

### Day 1-2: Basics

**Time:** 2-3 hours in day
**Focus:** installation and first Launch

1. **Section 1** - Introduction and establishment
 - **parameters installation:**
- `pip install autogluon.tabular[all]' - complete installation
`pip install autogluon.tabular' is the minimum installation
- `conda install - c conda-forge autogluon' - through conda
- ** Systems requirements:**
 - Python 3.8+
RAM: minimum 4GB, recommended 8GB+
- CPU: 2+ Cores
- Disc: 2GB available space

2. **Section 2** - Basic use
- ** Keys TabularPredictor:**
- `label': Target variable (mandatory)
 - `problem_type`: 'binary', 'multiclass', 'regression'
 - `eval_metric`: 'accuracy', 'f1', 'roc_auc', 'log_loss'
- `path': A way to preserve the model
- `verbosity': Output level (0-4)

3. **Practice: ** Install AutoML Gluon and launch the first example
 ```python
# Minimum example with parameters
 from autogluon.tabular import TabularPredictor
 import pandas as pd

# Parameters for rapid start
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy',
 path='quickstart_model',
 verbosity=2
 )
 ```

### Day 3-4: Understanding

**Time:** 2-3 hours in day
**Focus:** Understanding the parameters and making model

4. **Section 3** - Advanced Conference
- **pamesters of study:**
- `time_limit': Time limitation (seconds)
 - `presets`: 'best_quality', 'high_quality', 'medium_quality'
- `num_trials': Number of attempts
- `holdout_frac': Percentage of data for goldout recovery

5. **Section 4** - metrics and quality assessment
- ** Accessible metrics:**
- Classification: 'accuracy', 'f1', 'roc_auc', 'log_loss'
- Regression: 'rmse', 'mae', 'r2', 'pearsonr'
- **parameters estimate:**
- `silent=True/False': Quiet Mode
- `auxiliary_metrics=True/False': Additional metrics

6. **Practice:** Create your first model
 ```python
# Extended example with parameters
 predictor.fit(
 data,
 time_limit=300, # 5 minutes
== sync, corrected by elderman == @elder_man
num_trials=10, #10 attempts
holdout_frac=0.2, # 20% for validation
 verbosity=2
 )
 ```

#### Day 5-7: appreciation

**Time:** 2-3 hours in day
** Focus:** validation and quality assessment

**Section 5** - validation of models
- **parameters validation:**
- `num_bag_folds': Number of folds for bagging
- `num_stack_levels': Glassing levels
- `auto_stack': Automatic glassing
- `refit_full': retraining on all data

8. **Section 8** - Best practices
- **parameters of quality:**
- `feature_prene': Selection of topics
- `excluded_model_types':Excluded types of models
- `included_model_types': Model types included

9. **Practice:** Re-approve your model
 ```python
# Validation with parameters
 predictor.fit(
 data,
 time_limit=600, # 10 minutes
presets='high_quality', #High quality
num_bag_folds=5, #5-fold bagging
num_stack_levels=1, #1 level of glass
Auto_stack=True, #Automated glassing
refit_full=True, # retraining
Feature_prene=True # Selection of topics
 )
 ```

#### Day 8-10: Sales

**Time:** 3-4 hours in day
**Focus:** Deploy in sales

10. **Section 6** - Sales and Detail
- **parameters sold:**
- `presets='optimise_for_development': Optimizing for depletion
- 'save_space=True': Cost savings
== sync, corrected by elderman == @elder_man

11. **Section 12** - Simple example sold
 - **API parameters:**
- `HOST': server hosting
- `PORT': server port
- `DEBUG': debugging mode
- `MAX_BATCH_SIZE': Maximum dimensions of the booth

12. **Practice:** Hit the model in product
 ```python
# Sold configuration
 predictor.fit(
 data,
 presets='optimize_for_deployment',
 save_space=True,
 keep_only_best=True,
 time_limit=1200
 )
 ```

#### Day 11-14: Deepening

**Time:** 2-3 hours in day
**Focus:** Retraining and advanced technology

13. **Section 7** - Retraining models
- **parameters retraining:**
- `retrain_frequancy': Frequency retraining
== sync, corrected by elderman == @elder_man
- `Performance_threshold': The threshold of performance

14. **Section 9** - uses
- **Specialized parameters:**
- for time series: `time_limit' increased
- for big data: `num_cpus', `memory_limit'
 - for GPU: `num_gpus`

15. **Practice:** Create a system with re-education
 ```python
# Retraining system
 class Retrainingsystem:
 def __init__(self, retrain_frequency=1000):
 self.retrain_frequency = retrain_frequency
 self.performance_threshold = 0.8

 def should_retrain(self, performance):
 return performance < self.performance_threshold
 ```

### * full study (1-2 months)

**Goal:** Fully understood AutoML Gluon

### ~ metrics on learning progress

```mermaid
graph LR
A[level 0<br/> Newcomer] -> B[level 1<br/> Basics]
B -> C[Level 2<br/> Practice]
C -> D[Level 3<br/> Sale]
D -> E[Level 4<br/> Expert]

A1[0 per cent understanding<br/>0 models<br/>0 projects] -> A
B1[20% understanding<br/>1-3 model<br/>1 simple project] -> B
C1[50 per cent understanding<br/>5-10 models<br/>2-3 of the project] -> C
D1[80 per cent understanding<br/>10+ models<br/> System sold] --> D
E1[100 per cent understanding<br/> Complex systems<br/> Super system] --> E

 style A fill:#ffcccc
 style B fill:#ffffcc
 style C fill:#ccffcc
 style D fill:#ccccff
 style E fill:#ffccff
```

### Week 1: Basics
1. **Section 1** - Introduction and establishment
2. **Section 2** - Basic use
3. **Section 3** - Advanced Conference
4. ** Practice:** Create 3-5 simple models

#### Week 2: Evaluation and validation
5. **Section 4** - metrics and quality assessment
6. **Section 5** - model validation
7. **Section 8** - Best practices
8. ** Practice:** complete validation

### Week 3: Sales
9. **Section 6** - Sales and Detail
10. **Section 7** - Retraining models
11. **Section 12** - Simple example sold
12. **Practice:** Create a system sold

### Week 4: Advanced themes
13. ** Section 9** - examples of use
14. **Section 10**-Troubleshooting
15. **Section 13** - Complex example sold
16. **Practice: **

## for advanced users (6+ months of experience)

### ♪ The way for advanced users

```mermaid
graph TD
A [Proved user] --> B {Strategy selection}
B---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
B------------------------------------------

C --> C1[Day 1-2: Architecture]
C --> C2 [Day 3-4: validation]
C --> C3 [Day 5-7: Deploy]

D -> D1 [Welcome 1: Theory and Framework]
D -> D2 [ Week 2: Specialized indicators]
D -> D3 [week 3: Super System]

C1-> E1[architecture system]
C2 --> E2 [integrated validation]
C3 --> E3 [Selled system]

D1 -> F1 [Processed machinery]
D2 --> F2 [models for indicators]
D3 --> F3 [Super-system]

E1 --> G [Success!]
 E2 --> G
 E3 --> G
 F1 --> G
 F2 --> G
 F3 --> G
```

## # Focus on sales (1 week)

**Goal:** Create a robotic sale system

### Day 1-2: Architecture
1. **Section 6** - Sales and Detail
2. **Section 12** - Simple example sold
3. **Section 13** - Complex example sold
4. ** Practice:** Design the architecture of the system

#### Day 3-4: validation
5. **Section 5** - validation of models
6. ** Section 8** - Best practices
7. ** Practice:** Conduct comprehensive validation

### Day 5-7: Deploy
8. **Section 7** - Retraining models
9. **Section 9** - examples of use
10. **Practice:** Hit the system in sales

## ♪ In-depth study (2-3 weeks)

**Goal:** Become an expert in AutoML Gluon

#### Week 1: Theory and foundations
1. **Section 14** - AutoML theory and framework
2. **Section 15** - Inspirability and Explainability
3. **Section 16** - advanced topics
4. ** Practice:** Implement advanced technology

#### Week 2: Specialized indicators
5. **Section 19** - WAVE2 Indicator
6. **Section 20** - SCHR Levels
7. **Section 21** - SCHR SHORT3
8. ** Practice:** Create models for each indicator

### Week 3: Super System
9. **Section 22** - Super System
10. **Section 17** - Ethics and Responsible AI
11. **Section 18** - Case Studies
12. **Practice:** Create a super system

## for experts (2+ years of experience)

### ♪ Maximum efficiency (3-5 days)

♪ Goal: ♪ Quickly learn new techniques ♪

#### Day 1: Review
1. **Section 1** - Introduction and establishment (rapid)
2. **Section 14** - AutoML theory and framework
3. **Section 16** - advanced topics
4. **Practice: ** Assess new opportunities

#### Day 2: Specialized technicians
5. **Section 19** - WAVE2 Indicator
6. **Section 20** - SCHR Levels
7. **Section 21** - SCHR SHORT3
8. ** Practice:** Test new indicators

### Day 3: Super System
9. **Section 22** - Super System
10. **Section 18** - Case Studies (elected)
11. **Practice:** Create a prototype of a super system

#### Day 4-5: Deploy and Optimize
12. **Section 6** - Sales and Detail
13. **Section 7** - Retraining models
14. **Practice:** Hatch and optimize system

## Specialized ways to study

### ♪ Specialized route map

```mermaid
graph TD
A [Selection of specialization] -> B {Specialist type}

B---------------------------------------------------------------------------
B--~~ML engineer ~ D[~ ML engineer]
B--~ ~ Treider~ E[~ Trader]
B-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

C -> C1 [Focus: Understanding data and metric]
C -> C2 [Sections: 1.2, 4.5.15.8]
C --> C3 [Result: Expert on analysis]

D -> D1 [Focus: Production and Depletion]
D -> D2 [Sections: 1.2,6.7,12.13.22]
D -> D3 [Result: ML systems in sales]

E --> E1 [Focus: trading systems]
E --> E2 [Sections: 1.2.19.20.21.22.18]
E --> E3 [Result: Super-Trade System]

F --> F1 [Focus: Business Applications]
F -> F2 [Sections: 1,2,4,18,178]
F --> F3 [Result: Business decisions on AI]

 style C fill:#e1f5fe
 style D fill:#f3e5f5
 style E fill:#e8f5e8
 style F fill:#fff3e0
```

### for data analysts

** Focus: ** Data understanding and metric
**Time:** 2-3 weeks
** Key skills: ** Data analysis, interpretation of results, choice of metric

#### Parameters for Data Analysts

1. **Section 1** - Introduction and establishment
 - **parameters installation:**
- `pip install autogluon.tabular[all]' is the complete installation with visualization
- `pip install matplotlib seaborn tablely' - additional visualization libraries
- ** Systems requirements:**
- RAM: 8GB+ (for large datasets)
- Disc: 5GB+ (for data and models)

2. **Section 2** - Basic use
- ** Keys for Analysis:**
 ```python
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='roc_auc', # ROC-AUC for Analysis
 path='Analysis_model',
verbosity=3, # Detailed Conclusion
best_quality' # Better quality for Analysis
 )
 ```

3. **Section 4** - metrics and quality assessment
- **parameters metric for Analysis:**
 - `eval_metric`: 'roc_auc', 'f1', 'precision', 'recall'
- `auxiliary_metrics=True': Additional metrics
- `silent=False': Detailed output of metric
- ** Analise performance:**
 ```python
# Detailed assessment with parameters
 performance = predictor.evaluate(
 test_data,
 silent=False,
 auxiliary_metrics=True,
 Detailed_Report=True
 )
 ```

**Section 5** - validation of models
- **parameters validation for Analysis:**
- `num_bag_folds=10': More folks for stability
- `holdout_frac=0.3': More data for validation
- 'auto_stack=True': Automatic glassing
- **Cross-validation:**
 ```python
 predictor.fit(
 data,
 num_bag_folds=10, # 10-fold CV
 holdout_frac=0.3, # 30% for holdout
Auto_stack=True, #Stacking
refit_full=True # retraining
 )
 ```

5. **Section 15** - Inspirability and Explainability
- **parameters interpretation:**
- `feature_importance=True': Importance of topics
- `permutation_importance'=True': Reshuffling importance
- `shap_valutes=True': SHAP values
- **Analysis of importance:**
 ```python
# The importance of signs
 importance = predictor.feature_importance(data)

# SHAP values
 explainer = predictor.get_explainer()
 shap_values = explainer.shap_values(data)
 ```

6. ** Section 8** - Best practices
- **quality parameters for Analysis:**
- `feature_prene=True': Selection of topics
- `excluded_model_types=['KNN'] `: Deletion of Slow Models
- `included_model_types=['RF', 'GBM', 'XGB'] `: Inclusion of interpreted models

### for ML engineers

**Focus:** Sold and delivered
**Time:** 2-3 weeks
** Key skills:**Deploy, Monitoring, scaling, DevOPs

#### parameters for ML engineers

1. **Section 1** - Introduction and establishment
- **parameters installation for sale:**
- `pip install autogluon.tabular[all]' - complete installation
- 'pip install gunicorn uwsgi' - WSGI servers
- `pip install docker kubernetes' - containerization
- ** Systems requirements:**
RAM: 16GB+ (for sale)
- CPU: 8+ kernels
- Disc: 20GB+ (for models and logs)

2. **Section 2** - Basic use
- **parameters for sale:**
 ```python
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy',
 path='production_model',
verbosity=1, #Minimum output in sales
priorities='optimise_for_deployment' # Optimization for Depletion
 )
 ```

3. **Section 6** - Sales and Detail
- **parameters optimization:**
- `presets='optimise_for_development': Optimizing for depletion
- 'save_space=True': Cost savings
== sync, corrected by elderman == @elder_man
- `refit_ful=False': Disabled retraining
- **configuring for sale:**
 ```python
 predictor.fit(
 data,
 presets='optimize_for_deployment',
 save_space=True,
 keep_only_best=True,
 refit_full=False,
Time_limit=3600, #1 hour maximum
num_trials=50, # More attempts
 hyperparameter_tune_kwargs={
 'scheduler': 'local',
 'searcher': 'bayes',
 'num_trials': 50
 }
 )
 ```

4. **Section 7** - Retraining models
- **parameters retraining:**
- `retrain_frequancy=1000': Frequency retraining
== sync, corrected by elderman == @elder_man
- `Performance_threshold=0.8': Performance threshold
- `adaptation_rate=0.1': Adaptation speed
- ** Retraining system:**
 ```python
 class ProductionRetrainingsystem:
 def __init__(self):
 self.retrain_frequency = 1000
 self.drift_threshold = 0.1
 self.performance_threshold = 0.8
 self.adaptation_rate = 0.1

 def should_retrain(self, performance, drift_score):
 return (performance < self.performance_threshold or
 drift_score > self.drift_threshold)
 ```

5. **Section 12** - Simple example sold
 - **API parameters:**
- `HOST='0.0.0.0': Link to all interfaces
- `PORT=5000': server port
- `DEBUG=False': Disablement of debug in sales
- `MAX_BATCH_SIZE=1000': Maximum dimensions of the batch
- `REQUEST_TIMEOUT=30': Request Timeout
 - **configuration API:**
 ```python
 class ProductionConfig:
 HOST = '0.0.0.0'
 PORT = 5000
 DEBUG = False
 MAX_BATCH_SIZE = 1000
 REQUEST_TIMEOUT = 30
 API_KEY = os.getenv('API_KEY')
 RATE_LIMIT = 100
 ENABLE_METRICS = True
 ```

6. **Section 13** - Complex example sold
- **parameters scale:**
- `num_workers=4': Number of vorkers
- `max_connections=1000': Maximum connections
- `memory_limit'='2GB': Memory Limited
== sync, corrected by elderman ==
 - **Docker configuration:**
 ```dockerfile
 FROM python:3.9-slim
 WORKDIR /app
 COPY requirements.txt .
 RUN pip install --no-cache-dir -r requirements.txt
 COPY . .
 EXPOSE 5000
 CMD ["gunicorn", "--bind", "0.0.0.0:5000",
 "--workers", "4", "--timeout", "30", "app:app"]
 ```

7. **Section 22** - Super System
- **parameters supersystems:**
 - `ensemble_methods=['adaptive', 'context', 'temporal']`
 - `weight_update_frequency=100`
 - `confidence_threshold=0.7`
 - `min_models_agreement=2`
- **configuring supersystems:**
 ```python
 super_system_config = {
 'ensemble_methods': ['adaptive', 'context', 'temporal'],
 'weight_update_frequency': 100,
 'confidence_threshold': 0.7,
 'min_models_agreement': 2,
 'performance_window': 500,
 'context_sensitivity': 0.8
 }
 ```

### for traders

**Focus:** Trading systems
**Time:** 3-4 weeks
** Key skills:** Trade indicators, risk management, trade automation

#### parameters for traders

1. **Section 1** - Introduction and establishment
 - **parameters installation for trading:**
- `pip install autogluon.tabular[all]' - complete installation
- `pip install youthccxt' - data with exchanges
- `pip install ta-lib' - Technical indicators
- ** Systems requirements:**
- RAM: 16GB+ (for large volume processing)
- CPU: 8+ kernels (for rapid calculations)
- Disc: 50GB+ (for historical data)

2. **Section 2** - Basic use
- **passers for trading systems:**
 ```python
 predictor = TabularPredictor(
 label='target',
Problem_type='binary', # Buying/selling
 eval_metric='f1', # F1 for trading
 path='trading_model',
 verbosity=2,
"Presets"='best_quality' # Best quality critical
 )
 ```

3. **Section 19** - WAVE2 Indicator
 - **parameters WAVE2:**
== sync, corrected by elderman == @elder_man
- `max_wave_length=50': Maximum wave length
- `amplitude_threshold=0.02': Amplitude threshold (2 per cent)
- `frequancy_threshold=0.1': Frequency threshold
- `phase_threshold=0.3': Phase threshold
 - **configuration WAVE2:**
 ```python
 wave2_config = {
 'min_wave_length': 5,
 'max_wave_length': 50,
 'amplitude_threshold': 0.02,
 'frequency_threshold': 0.1,
 'phase_threshold': 0.3,
 'signal_threshold': 0.6,
 'risk_reward_ratio': 2.0
 }
 ```

4. **Section 20** - SCHR Levels
 - **parameters SCHR Levels:**
- `lookback_period=50': Period of Analysis levels
- `min_touches=3': Minimum touching
- `tolerance=0.001': Tolerance (0.1 per cent)
- `pressure_threshold=0.7': Pressure threshold
- `breakout_threshold=0.8': Passage threshold
 - **configuration SCHR Levels:**
 ```python
 schr_config = {
 'lookback_period': 50,
 'min_touches': 3,
 'tolerance': 0.001,
 'pressure_threshold': 0.7,
 'breakout_threshold': 0.8,
 'volume_weight': 0.3,
 'volume_confirmation': True
 }
 ```

5. **Section 21** - SCHR SHORT3
 - **parameters SCHR SHORT3:**
- `short_period=3': Short term
- `volatility_Window=10': Velocity Window
- `momentum_threshold=0.5': Time threshold
- `volatility_threshold=0.02': Volatility threshold (2 per cent)
- `signal_strength=0.6': Signal strength
 - **configuration SCHR SHORT3:**
 ```python
 short3_config = {
 'short_period': 3,
 'volatility_window': 10,
 'momentum_threshold': 0.5,
 'volatility_threshold': 0.02,
 'signal_strength': 0.6,
 'pattern_types': ['candlestick', 'price_action'],
 'min_pattern_strength': 0.7
 }
 ```

6. **Section 22** - Super System
- **parameters super systems for trading:**
 - `ensemble_methods=['adaptive', 'context', 'temporal']`
- `weight_update_freequancy=50': Frequent extradate balance
- `confidence_threshold=0.8': High threshold of confidence
== sync, corrected by elderman == @elder_man
- ** Trade configuring:**
 ```python
 trading_system_config = {
 'ensemble_methods': ['adaptive', 'context', 'temporal'],
 'weight_update_frequency': 50,
 'confidence_threshold': 0.8,
 'min_models_agreement': 2,
 'risk_Management': {
'max_position_size': 0.1 # 10% capital
'stop_loss_threshold': 0.02, #2% stop-loss
'take_profit_threshold': 0.04, # 4% teak profile
'max_drawdown': 0.05 # 5% maximum draught
 },
 'trading_hours': {
 'start': '09:00',
 'end': '17:00',
 'timezone': 'UTC'
 }
 }
 ```

7. **Section 18** - Case Studies (crypto-trade)
- **parameters for crypto-trade:**
- `Timeframe='1h' ': Timeframe (1 hour)
- `lookback_days=365': Year of Historical Data
- `volatility_adjustment=True': Adjustment on volatility
- `Market_hours_24_7=True': 24-hour trade
- **Crypto configuring:**
 ```python
 crypto_config = {
 'Timeframe': '1h',
 'lookback_days': 365,
 'volatility_adjustment': True,
 'market_hours_24_7': True,
 'exchanges': ['binance', 'coinbase', 'kraken'],
 'pairs': ['BTC/USDT', 'ETH/USDT', 'ADA/USDT'],
 'risk_Management': {
'max_position_size': 0.05, #5 percent for crypto
'stop_loss_threshold': 0.03, #3% stop-loss
'take_profit_threshold': 0.06, #6% teak profile
'max_drawdown': 0.03 # 3% maximum draught
 }
 }
 ```

### for business analysts

**Focus:** Business applications
**Time:** 2-3 weeks
** Key skills:** Business metrics, interpretation of results, ROI, AI ethics

#### parameters for business analysts

1. **Section 1** - Introduction and establishment
- **parameters installation for business:**
- `pip install autogluon.tabular[all]' - complete installation
- `pip install flatly dash' - interactive dashboards
- `pip install jupyter voila' - presentations
- ** Systems requirements:**
- RAM: 8GB+
- CPU: 4+ Cores
- Disc: 10GB+ (for data and Reports)

2. **Section 2** - Basic use
- **parameters for Business Anallysis:**
 ```python
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
Eval_metric='roc_auc', #ROC-AUC for Business
 path='business_model',
 verbosity=2,
presets='high_quality' #High quality
 )
 ```

3. **Section 4** - metrics and quality assessment
- ** Business-metrics:**
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
- `auxiliary_metrics=True': Additional metrics
- **Analysis of ROI:**
 ```python
# Business-metics
 business_metrics = {
 'roi': 0.15, # 15% ROI
'cost_per_Predication': 0.01, # $0.01 for Prevention
'accuracy_threshold': 0.85, #85% accuracy
'False_positive_cost': 10.0, # $10 for false positive
'False_negative_cost': 50.0 # $50 for false negative
 }
 ```

4. **Section 18** - Case Studies
- **parameters for Case Studies:**
- `time_limit= 1800': 30 minutes on education
- `presets='best_quality':
- `holdout_frac=0.2`: 20% for validation
- `feature_prene=True': Selection of topics
- **configuring the case:**
 ```python
 case_study_config = {
 'time_limit': 1800,
 'presets': 'best_quality',
 'holdout_frac': 0.2,
 'feature_prune': True,
 'business_context': {
 'industry': 'finance',
 'Use_case': 'credit_scoring',
 'stakeholders': ['risk_team', 'business_team'],
 'compliance_required': True
 }
 }
 ```

5. **Section 17** - Ethics and Responsible AI
- **parameters ethics:**
- `fairness_metrics=True': metrics justice
- `bias_detection=True': Detection of displacements
- `explainability=True': Explainability of decisions
- `Privacy_preserving'=True': Maintaining privacy
- **Ethical conference:**
 ```python
 ethics_config = {
 'fairness_metrics': True,
 'bias_detection': True,
 'explainability': True,
 'privacy_preserving': True,
 'protected_attributes': ['age', 'gender', 'race'],
 'fairness_threshold': 0.8,
 'bias_threshold': 0.1
 }
 ```

6. ** Section 8** - Best practices
- **quality tools for business:**
- `feature_prene=True': Selection of topics
- `excluded_model_types=['KNN'] `: Deletion of Slow Models
- `Included_model_types=['RF', 'GBM', 'XGB'] `: Inspired models
- `refit_full=True': Retraining on all data
- ** Business-configuring:**
 ```python
 business_config = {
 'feature_prune': True,
 'excluded_model_types': ['KNN', 'NN_TORCH'],
 'included_model_types': ['RF', 'GBM', 'XGB', 'CAT'],
 'refit_full': True,
 'business_requirements': {
'max_inference_time': 0.1 #100m maximum
'min_accuracy': 0.85, #85% minimum
'max_model_size': 100, #100MB maximum
 'interpretability_required': True
 }
 }
 ```

## Practical recommendations

♪ ## ♪ Note keeping

1. ** Create a note file** for each section
2. ** Write down the code** you're trying.
3. **Fix the errors** and their decisions
4. ** Note important points** for future use

### ♪ Practical exercises

### ♪ Practical exercise block

```mermaid
graph TD
A [Initiated] --> B [Exercise 1: First model<br/>30 minutes]
B --> C {Workinget Model?}
C -->\\\\D[Exercise 2: appreciation\br/>1 hour]
C -->\\\No\E[fix errors\br/>15 minutes]
 E --> B

D --> F {validation gone?}
F -->\\\\\G[Exercise 3: Sales >br/>2 hours]
F -->\\\\\H[Analysis of problems\br/>30 minutes]
 H --> D

G --> I {API Workinget?}
I --\\\\\\\J[Achieves!\br/> Ready for real tasks]
I--~ ~ No ~ K[Delete sold <br/>1 hour]
 K --> G

 style A fill:#e3f2fd
 style B fill:#f3e5f5
 style D fill:#e8f5e8
 style G fill:#fff3e0
 style J fill:#e0f2f1
```

#### Exercise 1: First model (30 minutes)

**Goal:** Create the first AutoML Gluon with understanding all parameters

```python
# Create a simple model on Iris's dateset
from autogluon.tabular import TabularPredictor
import pandas as pd
from sklearn.datasets import load_iris

# Loading data
iris = load_iris()
data = pd.dataFrame(iris.data, columns=iris.feature_names)
data['target'] = iris.target

# creative models with detailed parameters
predictor = TabularPredictor(
Label='target', #Target (compulsory parameter)
program_type='multiclass', # Task type: 'binary', 'multiclass', 'regression'
Eval_metric='accuracy', #Metrics assessment: 'accuracy', 'f1', 'roc_auc', 'log_loss'
path='iris_model', #The way to preserve the model
verbosity=2, # Output level: 0-4 (0=silent, 4=detailed)
presets='media_quality_caster_inference' #Preinstallation of quality
)

# Training the model with parameters
predictor.fit(
Data, #Learning Data
Time_limit=60, #Little time of study (seconds)
model quality: 'best_quality', 'high_quality', 'mediam_quality', 'optimise_for_development'
num_trials=10, #Number of attempts for Hyperparameter tuning
Hyperparameter_tune_kwargs={ #paraters Settings hyperparameters
'Scheduler': 'local', #Planner: 'local', 'ray'
'Searcher': 'auto', #Surveyer: 'auto', 'random', 'bayes'
'num_trials': 10, #Number of attempts
'Search_space': 'Default' # Search Space
 },
Goldout_frac=0.2, # Proportion of data for goldout validation
num_bag_folds=0, #Number of folks for bagging (0=unset)
num_stack_levels=0, #Number of glass levels (0=unplug)
Auto_stack=True, #Automated glassing
number_gpus=0, #GPU number for learning
num_cpus = Non, # Quantity of CPU (none=autodefinition)
memory_limit=None, #None=no limit
Feature_prene=True, #Selection of topics
Excluded_model_types=, #Excluded types of models
including_model_types=[], # Model types included[]=all
refit_full=True, #retraining on all data
Set_best_to_refit_ful=True, #installation of the best model as refit_ful
Save_space=True, #savings space on disk
♪ Save_bag_folds=True, ♪ Save Bagging Folds
keep_only_best=True, #Save only the best model
num_bag_sects=1, #Number of Bagging Sets
num_stack_levels=0, #Number of glass levels
num_bag_folds=0, #Number of Bagging Folds
ag_args_fit={# Additional arguments for fat
 'num_gpus': 0,
 'num_cpus': None,
 'time_limit': 60
 },
ag_args_ensemble={# Arguments for an ensemble
 'num_gpus': 0,
 'num_cpus': None
 }
)

# Model evaluation
predictions = predictor.predict(data)
Print(f) "Totality: {predicator.evaluate(data)}")

# Further information on the model
print(f) "Best model: {predictor.get_model_best()}")
print(f) "Acceptance models: {predictor.get_model_names()}")
(f "The importance of the signs: {predictor.feature_importance(data)}")
```

#### Exercise 2: appreciation (1 hour)

**Goal:** To fully validate the model with understanding all parameters validation

```python
# Do a full model validation
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_Report, confusion_matrix
import numpy as np

# Data split with parameters
train_data, test_data = train_test_split(
 data,
test_size=0.2, # Testsy share (20%)
Random_state=42, # Random state for reproduction
stratehy=data['target'] #Stratification on target variable
)

♪ Create model with parameters of validation
predictor = TabularPredictor(
 label='target',
 problem_type='multiclass',
 eval_metric='accuracy',
 path='iris_validation_model',
 verbosity=2
)

# Training with parameters of validation
predictor.fit(
 train_data,
Time_limit=120, #Augmented time for better quality
== sync, corrected by elderman == @elder_man
Holdout_frac=0.2, # 20% data for goldout validation
num_bag_folds=5, #5-fold bagging for stability
num_stack_levels=1, #1 level of glass
Auto_stack=True, #Automated glassing
num_trials=20, # More attempts for Hyperparameter tuning
 hyperparameter_tune_kwargs={
 'scheduler': 'local',
'Searcher': 'Bayes', # Bayesian search for better results
 'num_trials': 20,
 'search_space': 'default'
 },
Feature_prene=True, #Selection of topics
refit_full=True, #retraining on all data
 set_best_to_refit_full=True
)

# validation on test data
test_predictions = predictor.predict(test_data)
test_accuracy = predictor.evaluate(test_data, silent=True)

# Detailed assessment of performance
pprint(f "Treat on test: {test_accuracy}")

# Cross-validation on learning data
cv_scores = []
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(train_data.drop('target', axis=1), train_data['target']):
 cv_train = train_data.iloc[train_idx]
 cv_val = train_data.iloc[val_idx]

# Learning on the Fold
 cv_predictor = TabularPredictor(
 label='target',
 problem_type='multiclass',
 eval_metric='accuracy',
 path=f'cv_model_{len(cv_scores)}',
 verbosity=0
 )
 cv_predictor.fit(cv_train, time_limit=60, presets='medium_quality')

# Assessment on validation fold
 cv_pred = cv_predictor.predict(cv_val)
 cv_acc = cv_predictor.evaluate(cv_val, silent=True)
 cv_scores.append(cv_acc)

Print(f" Average accuracy CV: {np.mean(cv_scores): 4f} (+/- {np.std(cv_scores*2:4f}})

# Detailed Classification Report
Print("nReport on classification:")
print(classification_Report(test_data['target'], test_predictions))

# A matrix of errors
Print('nMart of Errors: )
print(confusion_matrix(test_data['target'], test_predictions))

# Analysis of the importance of the signs
feature_importance = predictor.feature_importance(test_data)
the importance of the signs:)
print(feature_importance)

# Analysis of performance on classes
class_names = iris.target_names
for i, class_name in enumerate(class_names):
 class_mask = test_data['target'] == i
 if np.sum(class_mask) > 0:
 class_accuracy = np.mean(test_predictions[class_mask] == test_data['target'][class_mask])
print(f) "Treatness for class {class_name}: {class_accuracy:4f}")

# A confidence analysis of preferences
pred_proba = predictor.predict_proba(test_data)
confidence = np.max(pred_proba, axis=1)
(f) Average confidence preferences:(np.mean(confidence): 4f})
(f "Minimum confidence: {np.min(confidence): 4f}")
(f "Maximal confidence: {np.max(confidence): 4f}")

# Mistake analysis
errors = test_predictions != test_data['target']
if np.sum(errors) > 0:
((np.sum(errors)} from {len(test_data)})
 error_indices = np.where(errors)[0]
for idx in error_indices[:5]: # Shows the first 5 errors
 true_class = class_names[test_data['target'].iloc[idx]]
 pred_class = class_names[test_predictions[idx]]
 confidence_error = confidence[idx]
Print(f) index {idx}: Truth= {true_class}, Pradition={pred_class}, Confidence={confidence_error:.4f}}
```

#### Exercise 3: Sales (2 hours)

**Goal:** Create full-scale API with understanding all parameters

```python
# Create a simple API for a model
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import logging
import os
import time
from datetime import datetime
import json
from functools import wraps
import traceback

# configuring Logs
logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[
 logging.FileHandler('api.log'),
 logging.StreamHandler()
 ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app) # Inclusion of CORS for Frontend

# configuring application
class Config:
# Parameters Model
 MODEL_PATH = os.getenv('MODEL_PATH', 'iris_validation_model')
 MODEL_TYPE = os.getenv('MODEL_TYPE', 'TabularPredictor')

 # parameters API
 HOST = os.getenv('HOST', '0.0.0.0')
 PORT = int(os.getenv('PORT', 5000))
 DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# parameters performance
 MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 1000))
 MAX_REQUEST_SIZE = int(os.getenv('MAX_REQUEST_SIZE', 1024 * 1024)) # 1MB
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEUT', 30)) #30 seconds

# Parameters Monitoring
 ENABLE_METRICS = os.getenv('ENABLE_METRICS', 'True').lower() == 'true'
METRICS_INTERVAL = int(os.getenv('METRICS_INTERVAL', 60)) #60 seconds

# Parameters of safety
 API_KEY = os.getenv('API_KEY', None)
RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100)) # requests in minutes

# parameters validation
 required_FEATURES = ['sepal length (cm)', 'sepal width (cm)',
 'petal length (cm)', 'petal width (cm)']
 FEATURE_RANGES = {
 'sepal length (cm)': (4.0, 8.0),
 'sepal width (cm)': (2.0, 4.5),
 'petal length (cm)': (1.0, 7.0),
 'petal width (cm)': (0.1, 2.5)
 }

app.config.from_object(Config)

# Global variables for Monitoring
request_count = 0
error_count = 0
total_Prediction_time = 0
start_time = time.time()

# Loading the model with error processing
try:
 predictor = TabularPredictor.load(Config.MODEL_PATH)
logger.info(f" Model downloaded from {Config.MODEL_PATH}")
logger.info(f) Accessible models: {predictor.get_model_names()})
logger.info(f "Best Model: {predicator.get_model_best()}")
except Exception as e:
logger.error(f Model upload error: {e})
 predictor = None

# Decorators for Error Processing and Monitoring
def handle_errors(f):
 @wraps(f)
 def decorated_function(*args, **kwargs):
 global error_count
 try:
 return f(*args, **kwargs)
 except Exception as e:
 error_count += 1
logger.error(f" Mistake in {f._name__}: {str(e)}})
 logger.error(traceback.format_exc())
 return jsonify({
 'error': 'Internal Server Error',
 'message': str(e),
 'timestamp': datetime.now().isoformat()
 }), 500
 return decorated_function

def monitor_performance(f):
 @wraps(f)
 def decorated_function(*args, **kwargs):
 global request_count, total_Prediction_time
 start_time = time.time()
 request_count += 1

 result = f(*args, **kwargs)

 Prediction_time = time.time() - start_time
 total_Prediction_time += Prediction_time

logger.info(f) Request {request_account}: time of execution {Predication_time:.4f}with)
 return result
 return decorated_function

def validate_api_key(f):
 @wraps(f)
 def decorated_function(*args, **kwargs):
 if Config.API_KEY:
 api_key = request.headers.get('X-API-Key')
 if not api_key or api_key != Config.API_KEY:
 return jsonify({'error': 'Invalid API Key'}), 401
 return f(*args, **kwargs)
 return decorated_function

def validate_input_data(data):
"Validation of input data."
 if not isinstance(data, (List, dict)):
Raise ValueError("data should be a list or dictionary")

 if isinstance(data, dict):
 data = [data]

 if len(data) > Config.MAX_BATCH_SIZE:
raise ValueError(f"Exceeded maximum fatch size: {len(data)} > {Config.MAX_BATCH_SIZE})

 validated_data = []
 for i, item in enumerate(data):
 if not isinstance(item, dict):
Raise ValueError(f "Element {i} shall be a dictionary")

# Check mandatory signs
 for feature in Config.required_FEATURES:
 if feature not in item:
Raise ValueError(f "No mandatory topic: {feature}")

# sheck types and range of values
 validated_item = {}
 for feature, value in item.items():
 if feature in Config.required_FEATURES:
 try:
 float_value = float(value)
 min_val, max_val = Config.FEATURE_RANGES[feature]
 if not (min_val <= float_value <= max_val):
raise ValueError(f"Purity {feature}={float_value} outside [{min_val}, {max_val}]]
 validated_item[feature] = float_value
 except (ValueError, TypeError):
Raise ValueError(f" Uncorrect value for {feature}: {value})
 else:
 validated_item[feature] = value

 validated_data.append(validated_item)

 return validated_data

@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
 """health check API"""
 global request_count, error_count, total_Prediction_time, start_time

 uptime = time.time() - start_time
 avg_Prediction_time = total_Prediction_time / max(request_count, 1)
 error_rate = error_count / max(request_count, 1)

 health_status = {
 'status': 'healthy' if predictor is not None else 'unhealthy',
 'timestamp': datetime.now().isoformat(),
 'uptime_seconds': uptime,
 'model_loaded': predictor is not None,
 'metrics': {
 'total_requests': request_count,
 'total_errors': error_count,
 'error_rate': error_rate,
 'average_Prediction_time': avg_Prediction_time
 }
 }

 status_code = 200 if predictor is not None else 503
 return jsonify(health_status), status_code

@app.route('/predict', methods=['POST'])
@handle_errors
@monitor_performance
@validate_api_key
def predict():
""The Basic Endpoint for Preventions""
 if predictor is None:
 return jsonify({'error': 'Model not loaded'}), 503

# Calidation of the size of the request
 content_length = request.content_length
 if content_length and content_length > Config.MAX_REQUEST_SIZE:
 return jsonify({'error': 'Request too large'}), 413

# Collection and validation of data
 try:
 data = request.get_json()
 if not data:
 return jsonify({'error': 'No JSON data provided'}), 400

 validated_data = validate_input_data(data)
 except ValueError as e:
 return jsonify({'error': f'Validation error: {str(e)}'}), 400
 except Exception as e:
 return jsonify({'error': f'data processing error: {str(e)}'}), 400

# Transforming in dataFrame
 df = pd.dataFrame(validated_data)

# Premonition
 try:
 predictions = predictor.predict(df)
 probabilities = predictor.predict_proba(df)

# Forming the answer
 results = []
 for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
 result = {
 'index': i,
 'Prediction': int(pred),
 'Prediction_class': ['setosa', 'versicolor', 'virginica'][int(pred)],
 'probabilities': {
 'setosa': float(prob[0]),
 'versicolor': float(prob[1]),
 'virginica': float(prob[2])
 },
 'confidence': float(np.max(prob))
 }
 results.append(result)

 response = {
 'predictions': results,
 'metadata': {
 'model_name': predictor.get_model_best(),
 'timestamp': datetime.now().isoformat(),
 'total_predictions': len(results)
 }
 }

 return jsonify(response)

 except Exception as e:
logger.error(f "The prediction error: {str(e)}")
 return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
@handle_errors
def model_info():
""""""""" "model information"""
 if predictor is None:
 return jsonify({'error': 'Model not loaded'}), 503

 info = {
 'model_type': 'TabularPredictor',
 'best_model': predictor.get_model_best(),
 'available_models': predictor.get_model_names(),
 'feature_importance': predictor.feature_importance().to_dict() if hasattr(predictor, 'feature_importance') else None,
 'model_path': Config.MODEL_PATH,
 'timestamp': datetime.now().isoformat()
 }

 return jsonify(info)

@app.route('/metrics', methods=['GET'])
@handle_errors
def get_metrics():
"""Metrics performance"""
 if not Config.ENABLE_METRICS:
 return jsonify({'error': 'Metrics disabled'}), 403

 global request_count, error_count, total_Prediction_time, start_time

 uptime = time.time() - start_time
 avg_Prediction_time = total_Prediction_time / max(request_count, 1)
 error_rate = error_count / max(request_count, 1)
 requests_per_second = request_count / max(uptime, 1)

 metrics = {
 'uptime_seconds': uptime,
 'total_requests': request_count,
 'total_errors': error_count,
 'error_rate': error_rate,
 'average_Prediction_time': avg_Prediction_time,
 'requests_per_second': requests_per_second,
 'timestamp': datetime.now().isoformat()
 }

 return jsonify(metrics)

if __name__ == '__main__':
logger.info(f"Launch API server on {Config.HOST}: {Config.PORT}})
logger.info(f"Debug mode: {Config.DEBUG}}
logger.info(f "model: {Config.MODEL_PATH}")

 app.run(
 host=Config.HOST,
 port=Config.PORT,
 debug=Config.DEBUG,
True, # Multiaccuracy
Use_reloader=False # Disabled auto reload in sales
 )
```

### Additional files for sale

#### requirements.txt
```txt
flask==2.3.3
flask-cors==4.0.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
autogluon.tabular==0.8.2
gunicorn==21.2.0
```

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "30", "app:app"]
```

#### docker-compose.yml
```yaml
Version: '3.8'
services:
 api:
 build: .
 ports:
 - "5000:5000"
 environment:
 - MODEL_PATH=/app/models/iris_validation_model
 - DEBUG=False
 - API_KEY=your-secret-key
 - MAX_BATCH_SIZE=1000
 - RATE_LIMIT=100
 volumes:
 - ./models:/app/models
 restart: unless-stopped
 healthcheck:
 test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
 interval: 30s
 timeout: 10s
 retries: 3
```

### ♪ Inertial approach

### ♪ Learning cycle

```mermaid
graph LR
A[Read section<br/>10-15 min] -> B[Ask code<br/>20-30 min]
B -> C[Analyze the results<br/>5-10 min]
C --> D[Do notes<br/>5 min]
D -> E [Go to the next section]
 E --> A

B --> F {Workinget Code?}
F --\\\\\\G[Rectify errors\br/>10-15 min]
 G --> B
F -->\\\\\\\C

C --> H {\cHFFFFFF}
H -->\\\\\I[Reread section\br/>10 min]
 I --> A
H - ♪ Yes ♪ D

 style A fill:#e3f2fd
 style B fill:#f3e5f5
 style C fill:#e8f5e8
 style D fill:#fff3e0
 style E fill:#e0f2f1
```

1. **Read section** (10-15 minutes)
2. ** Try the code** (20-30 minutes)
3. ** Analyze the results** (5-10 minutes)
4. ** Make notes** (5 minutes)
5. ** Move to the next section**

### ♪ Target setting

### ♪ Timetable for learning goals

```mermaid
gantt
Title Timetable of Learning Purposes AutoML Gluon
 dateFormat X
 axisFormat %s

Section Short-term (1-2 weeks)
Launch first example: done, short1, 0, 1
Understanding the basics :done, short2, 1, 2
core simple model :done, short3, 2, 3

Medium term (1-2 months)
Sold system :active, medium1, 3, 5
Advanced technology :medium2, 5, 7
Real challenge :mediam3, 7, 9

Long-term (3-6 months)
Expert in AutoML Gluon :long1, 9, 12
Super system :long2, 12, 15
Knowledge sharing :long3, 15, 18
```

#### Short-term targets (1-2 weeks)
- Start the first example
- Understand the basic concepts
- Create a simple model

#### Medium-term objectives (1-2 months)
- Create a sold system
- Understand advanced techniques
- To solve a real problem.

#### Long-term goals (3-6 months)
- To become an expert in AutoML Gluon
- Create a super-system
- Share knowledge with others

## Resources for Deepening

### ♪ Additional literature
- "AutoML: Methods, systems, Challenges" - Frank Hutter
- "Hands-On Machine Learning" - Aurélien Géron
- "The Elements of Statistical Learning" - Hastie, Tibshirani, Friedman

### ♪ Online resources
- [AutoML Gluon Documentation](https://auto.gluon.ai/)
- [Amazon SageMaker](https://aws.amazon.com/sagemaker/)
- [Kaggle Learn](https://www.kaggle.com/learn)

### ♪ Commons
- [AutoML Gluon GitHub](https://github.com/autogluon/autogluon)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/autogluon)
- [Reddit r/MachineLearning](https://www.reddit.com/r/MachineLearning/)

## Conclusion

♪ ♪ The way to success

```mermaid
graph TD
A [Initiated] -> B [Selection of the appropriate path]
B -> C [Follow-up to practical recommendations]
C -> D [Continuing practice]
D -> E [Achieving objectives]
E -> F[Standing by an expert]
F --> G[create supersystem]
G --> H [Success! ♪]

B -> B1[New: 1-2 months]
B -> B2 [Processed: 2-3 weeks]
B --> B3 [Expert: 3-5 days]

C --> C1 [Inertial approach]
C --> C2 [Practice exercise]
C --> C3 [Maintaining notes]

D --> D1[create models]
D --> D2 [validation of results]
D --> D3 [Sales in sales]

 style A fill:#e3f2fd
 style H fill:#e8f5e8
 style F fill:#fff3e0
 style G fill:#f3e5f5
```

## Reference table of parameters on levels

### parameters for different levels of preparation

♪ ♪ Newcomer ♪ ♪ Advanced ♪ Expert ♪ Describe ♪
|----------|---------|-------------|---------|----------|
*time_limit** * 60-300 * 600-800 * 3600+ * Limited learning time (s) *
*Presets*** ♪ medium_quality' ♪ 'high_quality' ♪ 'best_quality' ♪ model quality ♪
♪ ♪ number_trials** ♪ 5 - 10 ♪ 20 - 50 ♪ 100+ ♪ number of attempts ♪
*oldout_frac** * 0.2 * 0.2-0.3 * 0.1-0.2 * Data share for validation  *
♪ ♪ number_bag_folds** ♪ 0-3 ♪ 5 ♪ 10+ ♪ Number of bagging folds ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
*False *True * True * Selection of features *
*Refit_full** * False * True * True * retraining on all data *

### pagers on specialization

♪ The analyst ♪ ♪ ML engineer ♪ Trader ♪ ♪ Business analyst ♪
|----------|----------|------------|---------|-----------------|
| **eval_metric** | 'roc_auc' | 'accuracy' | 'f1' | 'roc_auc' |
| **presets** | 'best_quality' | 'optimize_for_deployment' | 'best_quality' | 'high_quality' |
| **verbosity** | 3 | 1 | 2 | 2 |
| **auxiliary_metrics** | True | False | True | True |
| **feature_prune** | True | True | True | True |
| **excluded_model_types** | ['KNN'] | ['KNN', 'NN_TORCH'] | [] | ['KNN', 'NN_TORCH'] |
| **included_model_types** | ['RF', 'GBM', 'XGB'] | [] | [] | ['RF', 'GBM', 'XGB', 'CAT'] |

### System requirements on levels

♪ The newcomer ♪ ♪ The advanced expert ♪ Sold ♪
|-----------|---------|-------------|---------|-----------|
| **RAM** | 4-8GB | 8-16GB | 16-32GB | 32GB+ |
*CPU** 2-4 nuclei 4-8 nuclei 8-16 nuclei 16+
♪ Disc** ♪ 2-5GB ♪ 5-20GB ♪ 20-50GB ♪ 50GB+ ♪
*GPU** * not required *

### parameters performance

== sync, corrected by elderman ==
|----------|----------|----------|---------|
♪ ♪ Time_limit** ♪ 60-3600 ♪ Limited learning time ♪ ♪ quality vs speed ♪
♪ ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh o o o ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh ooh o
*num_bag_folds** * 0-20 * Quantity of folds * Stable vs time *
== sync, corrected by elderman == @elder_man
♪ ♪ Holdout_frac** ♪ 0.1-0.3 ♪ share of validation ♪ Reliability vs data ♪

### Recommendations on the choice of parameters

#### for rapid prototype

```python
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy',
 presets='medium_quality',
 time_limit=300,
 num_trials=10,
 verbosity=2
)
```

#### # For sale

```python
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy',
 presets='optimize_for_deployment',
 time_limit=3600,
 num_trials=50,
 feature_prune=True,
 save_space=True,
 keep_only_best=True,
 verbosity=1
)
```

##### For research

```python
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='roc_auc',
 presets='best_quality',
 time_limit=7200,
 num_trials=100,
 num_bag_folds=10,
 num_stack_levels=2,
 feature_prune=True,
 refit_full=True,
 verbosity=3
)
```

## Conclusion

This textbook is designed on different levels of training. Choose the appropriate way to study and follow the practical recommendations. Remember: The best way to learn AutoML Gluon is practice.

** Key principles for successful learning:**
1. ** Start with simple** - Use alternatives on default
2. ** Practice constantly** - Make models every day
3. **Experition with parameters** - study their influence
4. ** Document the results** - Record the experiments
5. ** Apply on real tasks** - Address practical problems
