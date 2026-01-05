# The correct use of probabilities in ML models

**Author:** NeoZorK (Shcherbyna Rostyslav)
**Date:** 2025
** Location:** Ukraine, Zaporizhzhya
**Version:** 1.0

## Whoy correct use of probabilities is critical

**Why 95 percent of ML models in sales misuse probabilities?** Because team focuses only on precision preferences, ignoring model confidence. It's like a doctor who diagnoses but not says how sure he is.

### Problems of misuse of probabilities

- ** False confidence**: Model says yes with 99% probability but wrong
- ** Bad risk-management**:not understood when model not is certain
- ** Wrong decisions**: Make decisions on baseline inaccurate probabilities
- ** Loss of trust**: Users not trust models

### The advantages of using the probabilities correctly

- ** Exact calibration**: Probabilities match reality
- ** Best risk management**: They understand when the model not is sure
- ** Regulatory decisions**: Make decisions on basis of exact probabilities
- ** User confidence**: The model is credible

## Introduction

Why is probability the heart of a ML model?

The correct use of probabilities is the key to the creation of robotic and profitable ML models. This section focuses on a deep understanding of how Working with Probabilities in AutoML Gloon and how to build efficient trading systems on their base.

♪ What is probability in ML?

**Why are probability not just numbers from 0 to 1?** Because they reflect model confidence and have to match reality. It's like a weather forecast -- if 90% of the rain says it should rain in 90% of the time.

### ♪ Concept probability in ML

```mermaid
graph TD
A [Induction data] -> B[ML Model]
 B --> C[Prediction]
B -> D [Approbability]

C -> E [Class/ Value]
D -> F [model confidence]

F --> G {Sureness level}
G -->\\\0.8\H[Reliable Pradition]
G--~ ~ Average 0.5-0.8~ I [Medated Pradition]
G--~ ~ Low < 0.5~ J [Unreliable Treatment]

H -> K [Trade action]
I-> L[Action: Careful]
J-> M[Action: no trade]

 style A fill:#e3f2fd
 style B fill:#f3e5f5
 style D fill:#e8f5e8
 style H fill:#c8e6c9
 style I fill:#fff3e0
 style J fill:#ffcdd2
```

### Definition

** Why is probability determination critical?** Because misapprehension leads to misuse.

Probabilities in machine learning are numerical estimates of the model's confidence in its predictions. They show how confident the model is in its answer.

### Types of probability

```python
# Example in AutoML Gluon
from autogluon.tabular import TabularPredictor

# the pre-indexor with the detailed parameters
predictor = TabularPredictor(
Label='target', #Target', #Target variable for prediction
Problem_type='binary', # Type of task: 'binary', 'multiclass', 'regression'
Eval_metric='accuracy', #Metrics assessment: 'accuracy', 'f1', 'roc_auc', 'log_loss'
path='./models', #A path for model conservation
verbosity=2, # Output level: 0-4 (0=silent, 4=detailed)
presets='best_quality' # Pre-installation: 'best_quality', 'high_quality', 'good_quality', 'mediam_quality'
)

# Training the model with parameters
predictor.fit(
Train_data, #Learning data
Time_limit=3600, #Restriction of learning time in seconds
presets='best_quality', #Preinstallation of quality
number_trials=10, #Number of optimization attempts
Hyperparameter_tune_kwargs={ #paraters Settings hyperparameters
 'scheduler': 'local',
 'searcher': 'auto'
 },
Goldout_frac=0.2, # Proportion of data for goldout validation
num_bag_folds=8, #Number of For Bagging Folds
num_stack_levels=1, #Number of glass levels
Auto_stack=True, #Automated glassing
number_gpus=1, #GPU number for learning
num_cpus=4, #Number of KPU for learning
memory_limit='8GB', #Rememorial Limited
Feature_prene=True, #Treatment of unimportant features
Excluded_model_types=, #Excluded types of models
including_model_types=[], # Model types included
refit_full=True, #retraining on all data
Set_best_to_refit_ful=True, #installation of the best model as refit_ful
Save_space=True, #savings space on disk
♪ Save_bag_folds=True, ♪ Save Bagging Folds
keep_only_best=True, #Save only the best model
num_bag_sects=1, #Number of Bagging Sets
Ag_args_fit={}, # Additional arguments for fat
Ag_args_ensemble={} # Additional arguments for band
)

# Retrieving preferences
predictions = predictor.predict(test_data)

# Getting the probabilities with parameters
probabilities = predictor.predict_proba(
test_data, #tests data
as_pandas=True, #Return in pandas dataFrame format
Transform_features=True # Application of transformations to signature
)

Print(Treathings:," Preventions)
"Probabilities:", probabilities
```

## The power of using probabilities

♪## 1. Calibration of confidence

### ♪ Methods calibration of probabilities

```mermaid
graph TD
A [Uncalibrated Probabilities] -> B {Selection of calibration method}

 B -->|Platt Scaling| C[Sigmoid function]
B -->\\Isotonic Regression\D[Monoton regression]
B -->Temperature Scaling~ E [Temperature scaling]

C --> C1 [Approves for most cases]
C --> C2 [Speed calibration]
C --> C3 [Good Workinget with Retraining]

D -> D1 [Non-parametric method]
D -> D2 [Monoton calibration]
D -> D3 [Better for small data]

E --> E1[for neural networks]
E --> E2 [One temperature parameter]
E --> E3 [Speed optimization]

C1-> F [Calibrated Probabilities]
 C2 --> F
 C3 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 E1 --> F
 E2 --> F
 E3 --> F

F --> G[check calibration]
G --> H {Calibrate good?}
H -->\\\\I[\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////\\\\\\\\\\\\\\\/////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\/\/\/\/\/\/\/\/\/\\\/\/\\\\\\\\\\\\\/\/\/\\\\\\\\\\\\\\\\\\\\\\\\\\/\/\/\/\/\/\/\/\/\/\/\\\/\/\/\/\/\/ }}}}}}}}/ } } } } } } } } } } } } } } } } } } } } } } \/ } } } } } } } } } } } \/ \/ } } } } } }
H- ♪ No ♪ J [Try another method]
 J --> B

 style A fill:#ffcdd2
 style F fill:#c8e6c9
 style I fill:#a5d6a7
```

```python
class ProbabilityCalibration:
""Calibration of Probabilities for Improvising Accuracy""

 def __init__(self, config=None):
 """
Initialization of the probability calibration system

 Args:
config (dict): configuration calibration
- calibration_methods: List of calibration methods
- cv_folds: Number of folds for cross-validation
-Temperature_init: Initial temperature for temperature scaling
- isotonic_bounds: Limits for isotonic regression
 """
 self.config = config or self._get_default_config()
 self.calibration_methods = {}
 self.calibrated_models = {}

 def _get_default_config(self):
"""""""" "Receive the default configuration"""
 return {
 'calibration_methods': ['platt', 'isotonic', 'temperature'],
 'cv_folds': 5,
 'temperature_init': 1.5,
 'isotonic_bounds': 'clip',
 'platt_method': 'sigmoid',
 'optimization_iterations': 50,
 'learning_rate': 0.01,
 'validation_split': 0.2,
 'random_state': 42
 }

 def calibrate_probabilities(self, probabilities, true_labels, method='all'):
 """
Calibration of probabilities

 Args:
Probabilities (array): Reference Probabilities (n_samples, n_classes)
rue_labels (array): True tags (n_samples,)
method (str): Calibration method ('all', 'platt', 'isotonic', 'temperature')

 Returns:
dict: dictionary with calibrated probabilities for each method
 """
 results = {}

 if method in ['all', 'platt']:
 results['platt'] = self.platt_scaling(probabilities, true_labels)

 if method in ['all', 'isotonic']:
 results['isotonic'] = self.isotonic_regression(probabilities, true_labels)

 if method in ['all', 'temperature']:
 results['temperature'] = self.temperature_scaling(probabilities, true_labels)

 return results

 def platt_scaling(self, probabilities, true_labels):
 """
Platt Scaling for Calibration

 Args:
Probabyties (array): Baseline probabilities
tree_labels (array): True tags

 Returns:
Array: Calibrated Probabilities
 """
 from sklearn.calibration import CalibratedClassifierCV

# Create of calibrated classification with parameters
 calibrated_clf = CalibratedClassifierCV(
Base_estimator=None, # AutoML Gluon Model
 method=self.config['platt_method'], # 'sigmoid' or 'isotonic'
cv=self.config['cv_folds'], #Number of folds
n_jobs=1, #The use of all kernels
ensemble=True # Use of ensemble
 )

# Calibration
 calibrated_clf.fit(probabilities.reshape(-1, 1), true_labels)
 calibrated_probs = calibrated_clf.predict_proba(probabilities.reshape(-1, 1))

# Maintaining the model
 self.calibrated_models['platt'] = calibrated_clf

 return calibrated_probs

 def isotonic_regression(self, probabilities, true_labels):
 """
Isotonic Regulation for Calibration

 Args:
Probabyties (array): Baseline probabilities
tree_labels (array): True tags

 Returns:
Array: Calibrated Probabilities
 """
 from sklearn.isotonic import IsotonicRegression

# Create isotonic regression with parameters
 isotonic_reg = IsotonicRegression(
 out_of_bounds=self.config['isotonic_bounds'], # 'clip' or 'nan'
increasing=True, # Monoton growth
y_min = None, #minimum y
y_max = None # Maximum y
 )

# Training on probability
 isotonic_reg.fit(probabilities, true_labels)
 calibrated_probs = isotonic_reg.transform(probabilities)

# Maintaining the model
 self.calibrated_models['isotonic'] = isotonic_reg

 return calibrated_probs

 def temperature_scaling(self, probabilities, true_labels):
 """
Temperature Scaling for Calibration

 Args:
Probabyties (array): Baseline probabilities
tree_labels (array): True tags

 Returns:
Array: Calibrated Probabilities
 """
 import torch
 import torch.nn as nn

# Transforming into Tensor
 probs_tensor = torch.tensor(probabilities, dtype=torch.float32)
 labels_tensor = torch.tensor(true_labels, dtype=torch.long)

# Temperature Scaling with parameters
 temperature = nn.Parameter(
 torch.ones(1) * self.config['temperature_init']
 )

# Temperature optimization
 optimizer = torch.optim.LBFGS(
 [temperature],
 lr=self.config['learning_rate'],
 max_iter=self.config['optimization_iterations']
 )

 def eval_loss():
 optimizer.zero_grad()
 loss = nn.CrossEntropyLoss()(
 probs_tensor / temperature,
 labels_tensor
 )
 loss.backward()
 return loss

 optimizer.step(eval_loss)

# Temperature application
 calibrated_probs = torch.softmax(probs_tensor / temperature, dim=1)

# Maintaining the model
 self.calibrated_models['temperature'] = temperature

 return calibrated_probs.detach().numpy()
```

♪##2 ♪ Adaptive Management Risks

### Management risks on basic probabilities

```mermaid
graph TD
A [Promise of Promise] --> B {Analysis of Confidence}

B --> High > 0.8~ C [High confidence]
B-~ ~ Average 0.5-0.8 ~ D [Medical confidence]
B--~ ~ Low < 0.5~ E [Low confidence]

C --> C1 [Increase entry size]
C --> C2 [Speed stop-loss]
C --> C3 [Less hedging]

D -> D1 [standard entry size]
D --> D2 [Normal freeze-loss]
D --> D3 [Measured hedging]

E --> E1 [Decrease the size of the entry]
E --> E2 [Narrow stop-loss]
E --> E3 [Active hedging]

C1-> F [Sizing of the entry]
C2 --> G[installation stop-loss]
C3-> H [Hedge strategy]

 D1 --> F
 D2 --> G
 D3 --> H

 E1 --> F
 E2 --> G
 E3 --> H

F --> I [final award]
 G --> I
 H --> I

I-> J[Monitorizing results]
J --> K {Result positive?}
K--~ ~ Yeah~ L [Corresponding parameters]
K --\\\\\No\M[The strategy has been revised]

 L --> A
 M --> A

 style A fill:#e3f2fd
 style C fill:#c8e6c9
 style D fill:#fff3e0
 style E fill:#ffcdd2
 style I fill:#f3e5f5
```

```python
class AdaptiveRiskManagement:
"Aptative Management Risks on Bases Probabilities."

 def __init__(self, config=None):
 """
Initiating a risk management system

 Args:
config (dict): configuring risk management
- base_position_size: Basic entry size (0.0-1.0)
- max_position_size: Maximum entry size (0.0-1.0)
- Conference_threshold: A threshold of confidence for increasing position
- Base_stop_loss: Base stop-loss in per cent
- volatility_multiplier: Multiplicity factor
- Hedging_threshold: Hedging activation threshold
 """
 self.config = config or self._get_default_config()
 self.risk_thresholds = {}
 self.position_sizing = {}
 self.hedging_strategies = {}

 def _get_default_config(self):
"""""""" "Receive the default configuration"""
 return {
'base_position_size': 0.1 # 10% from capital
'max_position_size': 0.2, # Maximum 20%
'min_position_size': 0.01, #minimum 1%
'confidence_threshold': 0.7, #Sureline
'base_stop_loss': 0.05, # 5% base freeze-loss
'max_stop_loss': 0.15, # 15% maximum stop-loss
'min_stop_loss': 0.02, #minimum 2% stop-loss
'volatility_multiplier': 0.5, # Vulnerability multiplier
'hedging_threshold': 0.3, #Hedge threshold
'risk_budget': 0.1 # Risk budget
'Correllation_threshold': 0.7, # Correlation threshold
'max_control': 0.9, #maximum correlation
'Rebalance_frequancy': 'daily', #Rebalance frequency
'Monitoring_window': 30, #Monitoring Window (days)
'Alert_threshold': 0.05, #Alternative threshold
'max_drawdown': 0.2, # Maximum draught
'var_confidence': 0.95, #Reliance level for VaR
'var_horizon': 1, #VaR Horizon (days)
'stress_test_scenarios': 5, #Number of stress-tests scenarios
'liquidity_buffer': 0.05, # Liquidity Buffer
'Transaction_costs': 0.001, #Travel costs
'slippage_factor': 0.0005 #Slip factor
'Market_impact_factor': 0.001, #market impact factor
'Regulatory_limits': { # Regulatory limits
'max_single_position': 0.1 # Maximum entry in one asset
'max_sector_exposure': 0.3, #maximum exposure on sector
'max_currency_exposure': 0.5 # Maximum foreign exchange exposure
 }
 }

 def calculate_position_size(self, probability, confidence_threshold=None,
 market_volatility=None, correlation_risk=None):
 """
Calculation of the size of the on base probability item

 Args:
Probability (float): Probability of success (0.0-1.0)
confidence_threshold (float): Confidence threshold (on default from config)
Market_volatility (float): Market volatility (0.0-1.0)
Correlation_risk (float): Correlation risk (0.0-1.0)

 Returns:
float: Size of entry (0.0-1.0)
 """
 if confidence_threshold is None:
 confidence_threshold = self.config['confidence_threshold']

# Basic position size
 base_size = self.config['base_position_size']

# Adjustment on basic probability
 if probability > confidence_threshold:
# High confidence - increasing size
 confidence_multiplier = probability / confidence_threshold
 position_size = base_size * confidence_multiplier
 else:
# Low confidence - reduced size
 confidence_multiplier = (probability / confidence_threshold) * 0.5
 position_size = base_size * confidence_multiplier

# Adjustment on volatility
 if market_volatility is not None:
 volatility_adjustment = 1 - (market_volatility * self.config['volatility_multiplier'])
 position_size *= volatility_adjustment

# Correlation adjustment
 if correlation_risk is not None:
 correlation_adjustment = 1 - (correlation_risk * 0.5)
 position_size *= correlation_adjustment

# Application of limits
 position_size = max(position_size, self.config['min_position_size'])
 position_size = min(position_size, self.config['max_position_size'])

 return position_size

 def dynamic_stop_loss(self, probability, entry_price, volatility=None,
 market_conditions=None, time_held=None):
 """
Dynamic stop-lose on base probability

 Args:
capacity (float): Probability of success
enry_price (float): Price of entry
volatility (float): Activability
Market_conditions (dict): Market conditions
Time_feld (int): Hold position time (days)

 Returns:
float: Stop-loss price
 """
# Basic stop-lose
 base_stop = self.config['base_stop_loss']

# Adjustment on basic probability
 if probability > 0.8:
# High confidence - wider stop-loss
 stop_loss_pct = base_stop * (1 - 0.4 * (1 - probability))
 elif probability > 0.6:
# Average confidence is a simple stop-loss
 stop_loss_pct = base_stop
 else:
# Low confidence is a narrower stop-loss
 stop_loss_pct = base_stop * (1 + 0.5 * (1 - probability))

# Adjustment on volatility
 if volatility is not None:
 volatility_adjustment = 1 + (volatility * self.config['volatility_multiplier'])
 stop_loss_pct *= volatility_adjustment

# Adjustment on market conditions
 if market_conditions:
 market_adjustment = self._calculate_market_adjustment(market_conditions)
 stop_loss_pct *= market_adjustment

# Adjustment on time holding
 if time_held is not None:
 time_adjustment = self._calculate_time_adjustment(time_held)
 stop_loss_pct *= time_adjustment

# Application of limits
 stop_loss_pct = max(stop_loss_pct, self.config['min_stop_loss'])
 stop_loss_pct = min(stop_loss_pct, self.config['max_stop_loss'])

# Calculation of the price of a stop-loss
 stop_loss_price = entry_price * (1 - stop_loss_pct)

 return stop_loss_price

 def probability_based_hedging(self, probabilities, market_conditions,
 Portfolio_state=None, risk_budget=None):
 """
Hedging on basic probabilities

 Args:
Probabilities (array): Probability Massive
Market_conditions (dict): Market conditions
Portfolio_state (dict): Portfolio status
Risk_budget (float): Risk budget

 Returns:
dict: Hedging strategy
 """
 if risk_budget is None:
 risk_budget = self.config['risk_budget']

# Analysis of probability distribution
 prob_distribution = self.analyze_probability_distribution(probabilities)

# Hedging needs to be determined
 hedging_needed = self.determine_hedging_need(
 prob_distribution,
 market_conditions,
 Portfolio_state
 )

 if hedging_needed:
# Calculation of the size of the hedge
 hedge_size = self.calculate_hedge_size(
 prob_distribution,
 risk_budget
 )

# Choice of hedging tools
 hedge_instruments = self.select_hedge_instruments(
 market_conditions,
 Portfolio_state
 )

# Calculation of hedging cost
 hedging_cost = self.calculate_hedging_cost(
 hedge_size,
 hedge_instruments
 )

 return {
 'hedge_needed': True,
 'hedge_size': hedge_size,
 'instruments': hedge_instruments,
 'cost': hedging_cost,
 'risk_reduction': self._calculate_risk_reduction(hedge_size),
 'expected_return_impact': self._calculate_return_impact(hedge_size)
 }

 return {'hedge_needed': False}

 def _calculate_market_adjustment(self, market_conditions):
"The calculation of adjustment on market conditions"
 adjustment = 1.0

# Adjustment on trend
 if market_conditions.get('trend') == 'bull':
extension *=1.1 # Increase stop-loss in the bull market
 elif market_conditions.get('trend') == 'bear':
extension * = 0.9 # Reduce stop-loss in the bear market

# Adjustment on volatility
 if market_conditions.get('volatility') == 'high':
 adjustment *= 1.2
 elif market_conditions.get('volatility') == 'low':
 adjustment *= 0.8

 return adjustment

 def _calculate_time_adjustment(self, time_held):
"The calculation of adjustment on time holding."
 if time_held < 1:
Return 1.0 # No adjustment for day-to-day items
 elif time_held < 7:
Return 0.95 # Small adjustment for short-term items
 else:
Return 0.9 #Big adjustment for long-term positions
```

###3: Ansemble on base probabilities

### ♪ methhods ensemble probabilities

```mermaid
graph TD
A [multiple models] -> B {type of ensemble}

B -->\\Weighted Ensemble\\C[weighted ensemble]
B -->Confidence Weighted\D[on confidence]
B -->♪ Bayesian Ensemble~ E[Bayesian]

C --> C1 [Fixed weights]
C --> C2 [Simple of implementation]
C --> C3 [A quick calculation]

D --> D1 [The weight on confidence]
D --> D2 [Adaptive weights]
D -> D3 [model quality accounting]

E -> E1 [Measurement of uncertainty]
E --> E2[Bayesian weights]
E --> E3 [Complicated implementation]

C1-> F [Comparison of probabilities]
 C2 --> F
 C3 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 E1 --> F
 E2 --> F
 E3 --> F

F --> G [Total probability]
G -> H [Esemble quality assessment]
H --> I {quality acceptable?}
I - ♪ Yeah ♪ J [♪ In sales]
I -->\\\K[configration of parameters]
 K --> B

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style G fill:#a5d6a7
 style J fill:#81c784
```

```python
class ProbabilityEnsemble:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""A""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, config=None):
 """
Initialization of the ensemble system

 Args:
config (dict): configuring ensemble
- ensemble_methods: List of ensemble techniques
- wight_calculation: Weight calculation method
- unceertainty_estimation: Method of assessing uncertainty
- Model_selection: Criteria for sampling models
 """
 self.config = config or self._get_default_config()
 self.ensemble_methods = {}
 self.weight_calculation = {}
 self.ensemble_models = {}

 def _get_default_config(self):
"""""""" "Receive the default configuration"""
 return {
 'ensemble_methods': ['weighted', 'confidence_weighted', 'bayesian'],
 'weight_calculation': 'performance_based',
 'uncertainty_estimation': 'variance',
 'model_selection': {
'min_performance': 0.6, #minimum performance
'max_control': 0.8, #maximum correlation between models
'min_diversity': 0.3, #Minimum diversity
'max_models': 10 # Maximum number of models
 },
'weight_regulation': 0.01, #Regularization of weights
'uncertainty_threshold': 0.1 #Speed threshold
'confidence_threshold': 0.7, #Sureline
'Diversity_night': 0.3, # Weight of diversity
'Performance_light': 0.7, # Weight of performance
'uncertainty_light': 0.2, #The weight of uncertainty
'Adaptive_weights':tree, #Adaptive weights
'Weight_update_frequancy': 100, # Weight updating frequency
'ensemble_size': 5, #The size of the ensemble
 'selection_criteria': ['accuracy', 'f1', 'roc_auc'],
'Weight_normalitation': 'Softmax', #Normation of weights
'uncertainty_combination': 'overage', # Combination of uncertainty
'Model_validation': True, #validation models
'cross_validation_folds': 5, #Folds for cross-validation
'Bootstrap_samples': 1000, #Number of bootstrap samples
'monte_carlo_samples': 1000, #Number of Monte carlo samples
'Bayesian_prior': 'uniform', # Bayesian aprior
'Bayesian_alpha': 1.0, #parameter alpha for Bayes
'Bayesian_beta': 1.0, #parameter beta for Bayes
'Temperature_scaling':True, #temperature scaling
'Temperature_value': 1.0, # Temperature value
'ensemble_validation': True, #galidation ensemble
 'performance_metrics': ['accuracy', 'f1', 'roc_auc', 'log_loss'],
 'uncertainty_metrics': ['entropy', 'variance', 'mutual_info'],
'weight_constrals': { #weight restrictions
'min_white': 0.01, # Minimum weight
'max_light': 0.5, # Maximum weight
'sum_constrint': 1.0 #weight sum should be 1
 }
 }

 def weighted_ensemble(self, model_probabilities, model_weights,
 performance_metrics=None, regularization=None):
 """
Weighted ensemble on basic probabilities

 Args:
model_probabilities (array): Probabilities from different models (n_models, n_samples, n_classes)
model_weights (array): Model weight (n_models,)
performance_metrics (dict): Metrics performance models
Regulation (float): Weights regularization factor

 Returns:
Array: Ansamble Probabilities (n_samples, n_classes)
 """
 if regularization is None:
 regularization = self.config['weight_regularization']

# Normalization of weights with regularization
 if self.config['weight_normalization'] == 'softmax':
# Softmax normalization
 weights_exp = np.exp(model_weights - np.max(model_weights))
 normalized_weights = weights_exp / np.sum(weights_exp)
 else:
# L1 Normalization
 normalized_weights = model_weights / np.sum(model_weights)

# Application of weight limits
 normalized_weights = self._apply_weight_constraints(normalized_weights)

# Weighted probability association
 ensemble_probability = np.average(
 model_probabilities,
 weights=normalized_weights,
 axis=0
 )

# Retaining information about the ensemble
 self.ensemble_models['weighted'] = {
 'weights': normalized_weights,
 'performance': performance_metrics,
 'regularization': regularization
 }

 return ensemble_probability

 def confidence_weighted_ensemble(self, model_probabilities, model_confidences,
 confidence_threshold=None, uncertainty_weight=None):
 """
Ensemble with weights on basis of confidence

 Args:
model_probabilities (array): Probabilities from different models
Model_confidences (array): Model confidence (n_models,)
confidence_threshold (float): Confidence threshold
unceertainty_night (float): Weight of uncertainty

 Returns:
Array: Ansamble Probabilities
 """
 if confidence_threshold is None:
 confidence_threshold = self.config['confidence_threshold']
 if uncertainty_weight is None:
 uncertainty_weight = self.config['uncertainty_weight']

# Calculation of weights on basis of confidence
 confidence_weights = self.calculate_confidence_weights(
 model_confidences,
 confidence_threshold
 )

# Adjustment on uncertainty
 if uncertainty_weight > 0:
 uncertainty_weights = self.calculate_uncertainty_weights(
 model_probabilities
 )
 confidence_weights = (1 - uncertainty_weight) * confidence_weights + \
 uncertainty_weight * uncertainty_weights

# Weighted association
 ensemble_probability = np.average(
 model_probabilities,
 weights=confidence_weights,
 axis=0
 )

# Retaining information about the ensemble
 self.ensemble_models['confidence_weighted'] = {
 'weights': confidence_weights,
 'confidences': model_confidences,
 'threshold': confidence_threshold
 }

 return ensemble_probability

 def bayesian_ensemble(self, model_probabilities, model_uncertainties,
 prior_type=None, alpha=None, beta=None):
 """
Bayesian ensemble

 Args:
model_probabilities (array): Probabilities from different models
model_uncertainties (array): Uncertainty of models (n_models,)
prior_type (str): Type of a priori distribution
Alpha (float): parameter alpha for Bayes
beta (float): parameter beta for Bayes

 Returns:
dict: Ansemble probability and uncertainty
 """
 if prior_type is None:
 prior_type = self.config['bayesian_prior']
 if alpha is None:
 alpha = self.config['bayesian_alpha']
 if beta is None:
 beta = self.config['bayesian_beta']

# Bayesian association
 bayesian_weights = self.calculate_bayesian_weights(
 model_uncertainties,
 prior_type,
 alpha,
 beta
 )

# Merging with uncertainty
 ensemble_probability = np.average(
 model_probabilities,
 weights=bayesian_weights,
 axis=0
 )

# add uncertainty
 ensemble_uncertainty = self.calculate_ensemble_uncertainty(
 model_probabilities,
 model_uncertainties,
 bayesian_weights
 )

# Retaining information about the ensemble
 self.ensemble_models['bayesian'] = {
 'weights': bayesian_weights,
 'uncertainties': model_uncertainties,
 'prior': prior_type,
 'alpha': alpha,
 'beta': beta
 }

 return {
 'probability': ensemble_probability,
 'uncertainty': ensemble_uncertainty,
 'weights': bayesian_weights
 }

 def calculate_confidence_weights(self, model_confidences, threshold):
""""" "The calculation of weights on basis of confidence"""
# Filtering models on the confidence threshold
 valid_models = model_confidences >= threshold

 if not np.any(valid_models):
# If there are no models above the threshold, Use all
 valid_models = np.ones_like(model_confidences, dtype=bool)

# Normalization of weights
 weights = np.zeros_like(model_confidences)
 weights[valid_models] = model_confidences[valid_models]
 weights = weights / np.sum(weights)

 return weights

 def calculate_uncertainty_weights(self, model_probabilities):
""""""" "The calculation of weights on basic uncertainty"""
# Calculation of entropy for each model
 entropies = []
 for probs in model_probabilities:
 entropy = -np.sum(probs * np.log(probs + 1e-10), axis=1)
 entropies.append(np.mean(entropy))

# Invert entropy (less entropy = more weight)
 weights = 1.0 / (np.array(entropies) + 1e-10)
 weights = weights / np.sum(weights)

 return weights

 def calculate_bayesian_weights(self, model_uncertainties, prior_type, alpha, beta):
""""""" "The Bayesian Balance"""
 if prior_type == 'uniform':
# Equivalent a prior
 prior_weights = np.ones(len(model_uncertainties)) / len(model_uncertainties)
 elif prior_type == 'dirichlet':
# Dirichle aprior
 prior_weights = np.random.dirichlet([alpha] * len(model_uncertainties))
 else:
# on default is even
 prior_weights = np.ones(len(model_uncertainties)) / len(model_uncertainties)

# Bayesian extradate balance
 likelihood = 1.0 / (model_uncertainties + 1e-10)
 posterior_weights = prior_weights * likelihood
 posterior_weights = posterior_weights / np.sum(posterior_weights)

 return posterior_weights

 def calculate_ensemble_uncertainty(self, model_probabilities, model_uncertainties, weights):
"The calculation of uncertainty in the ensemble."
 if self.config['uncertainty_combination'] == 'average':
# Average arithmetic uncertainty
 ensemble_uncertainty = np.average(model_uncertainties, weights=weights)
 elif self.config['uncertainty_combination'] == 'weighted_variance':
# Weighted dispersion
 ensemble_uncertainty = np.average(model_uncertainties**2, weights=weights)
 else:
# on default average
 ensemble_uncertainty = np.average(model_uncertainties, weights=weights)

 return ensemble_uncertainty

 def _apply_weight_constraints(self, weights):
"The Application of Weight Limitations""
 constraints = self.config['weight_constraints']

# Minimum weight
 weights = np.maximum(weights, constraints['min_weight'])

# Maximum weight
 weights = np.minimum(weights, constraints['max_weight'])

# Normalization to amount 1
 weights = weights / np.sum(weights)

 return weights
```

###4. Monitoring the probability drift

### Monitoring the probability drift

```mermaid
graph TD
A[Base probability] -> B [current probability]
B --> C {comparison distributions}

C--------------to---to--what---to---to---to---to--to---to--to--to---to---to---to---to---to---to--to--to---to---to---to-be--to-be--to-be--to-be-to-be--to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-be-to-to-be-to-be-to-be-to-be-to-to-to-be-to-to-to-to-to-to-to-to-to-to-to-to-to-be-be-be-be-be-to-to-to-be-to-be-be-be-be-be-be-be-to-to-to-to-to-to-to-to-to-to-be-be-be-be-be-be-to-to-be-be-to-to-be-be-to-to-be-to-to-to-to-to-to-to-be-to-to-to-to-be-to-be-be-to-be-be-be-be-be-be-be-be-be-to-to-to-to-to-to-to-to-be-to-to-to-to-to-be-be-be-be-be-be-be-be-be-be-to-to-to-to-to-to-to-to-be-be-be-be-be-be-be-be-to-to-be-be-to-to-to-to-to-be-be-be-to
C--~~ KS test ~ E [Colmogorov-Smirn]
C-~ ~ Wasserstein~ F [Vasserstein distance]

D --> D1[comparison medium]
 D --> D2[p-value < 0.05]
D -> D3 [Drift detection]

E --> E1 [comparson distributions]
E --> E2[KS statistics]
E --> E3 [critical]

F --> F1 [Lateral Meter]
F --> F2 [Target]
F --> F3 [form change]

D1-> G[Analysis of results]
 D2 --> G
 D3 --> G
 E1 --> G
 E2 --> G
 E3 --> G
 F1 --> G
 F2 --> G
 F3 --> G

G --> H {Drift detected?}
H-~ ~ Yeah~ I [Alert on Drift]
H-~ ~ No~ J [To continue Monitoring]

I -> K[Analysis of the causes of drift]
K --> L [model correction]
L --> M[retraining]
M --> N[update base line]
 N --> A

J --> O [Next check]
 O --> A

 style A fill:#e3f2fd
 style B fill:#f3e5f5
 style I fill:#ffcdd2
 style J fill:#c8e6c9
 style M fill:#fff3e0
```

```python
class ProbabilityDriftMonitor:
"Monitoring Drift of Probabilities."

 def __init__(self, config=None):
 """
Initiating the Monitoring Drift System

 Args:
config (dict): configuring Monitoring
- drift_threshold: Drift detection threshold
- test_methods: List of test methods
- Windows_size: Window size for Analysis
- update_frequancy: Update frequency
 """
 self.config = config or self._get_default_config()
 self.drift_detectors = {}
 self.baseline_distribution = None
 self.drift_history = []
 self.alert_thresholds = {}

 def _get_default_config(self):
"""""""" "Receive the default configuration"""
 return {
'drift_threshold': 0.05, #Drift detection threshold
 'test_methods': ['statistical', 'ks', 'wasserstein', 'psi'],
'Window_size': 1000, # Window size for Analysis
'Update_freequancy': 'daily', #Renewal frequency
'baseline_period': 30, # Period for base line (days)
'min_samples': 100, #minimum number of samples
'max_samples': 10,000, #maximum number of samples
 'statistical_tests': {
'Ttest_alpha': 0.05, # Alpha for t-test
'Mannwitney_alpha': 0.05, # Alpha for Manna Whitney Test
'ks_alpha': 0.05, # Alpha for KS test
'psi_threshold': 0.2, #PSI threshold
'Wasserstein_threshold': 0.1 #Wasserstein threshold
 },
 'alert_Settings': {
'Enable_alerts':True, #Locking allergets
'alert_threshold': 0.1 #Target for Alerts
'alert_frequancy': 'immediate', #Alternative frequency
 'alert_channels': ['email', 'slack', 'webhook'],
'alert_recipients':[], #Alternators
'Alert_template': 'Default' # An allerant's sword
 },
 'Monitoring_metrics': {
'mean_drift': True, # Middle drift
'Variance_drift':True, # Drift variance
'distribution_draft': True, # Distribution Drift
'Correllation_draft': True, # Correlation drift
'entropy_drift': True # Drift entropy
 },
 'adaptation_Settings': {
'auto_adapt':False, #Automated adaptation
'adaptation_threshold': 0.15, #The threshold for adaptation
'adaptation_method': 'retrain', #A method of adaptation
'Adaptation_frequancy': 'weekly', # Frequency of adaptation
'Model_backup':True, #Reserve Model
'Rollback_threshold': 0.2 #Rollback threshold
 },
 'visualization': {
'Enable_plots': True, #Checking
'plot_frequancy': 'daily', #Plot_frequancy
'Save_plotts':True, #Plots saved
'plot_format': 'png', # Graphic format
'plot_dpi': 300, #DPI graphs
'plot_size': (12, 8) # Graphic size
 },
 'data_quality': {
'Check_Missing':True, #check missing values
'Check_outliers': True, #check emissions
'outlier_threshold': 3.0, # Emission threshold
'Missing_threshold': 0.1 # Threshold for missing values
'data_validation': True # data validation
 },
 'performance': {
'parallel_processing': True, # Parallel processing
'n_jobs': -1, #Number of processes
'Memory_limit': '2GB', #Rememorial Limited
'Cache_results':True, #Cashing results
'Cache_size': 1000 # Cache size
 }
 }

 def detect_probability_drift(self, current_probabilities, baseline_probabilities=None,
 drift_threshold=None, test_methods=None):
 """
Detecting a drift of probabilities

 Args:
Current_probabilities (array): Current Probabilities
Baseline_probabilities (array): Baseline probability (if None, retained)
drift_threshold (float): Threshold for drift detection
test_methods (List): List of test methods

 Returns:
dict: Drift detection results
 """
 if baseline_probabilities is None:
 baseline_probabilities = self.baseline_distribution

 if baseline_probabilities is None:
 raise ValueError("Baseline probabilities not provided and not stored")

 if drift_threshold is None:
 drift_threshold = self.config['drift_threshold']

 if test_methods is None:
 test_methods = self.config['test_methods']

# validation of data
 self._validate_probabilities(current_probabilities, baseline_probabilities)

 results = {}
 drift_detected = False

# Statistical tests
 if 'statistical' in test_methods:
 statistical_drift = self.statistical_drift_test(
 current_probabilities,
 baseline_probabilities,
 drift_threshold
 )
 results['statistical'] = statistical_drift
 drift_detected = drift_detected or statistical_drift

# Kolmogorov-Smirnov test
 if 'ks' in test_methods:
 ks_drift = self.ks_drift_test(
 current_probabilities,
 baseline_probabilities,
 drift_threshold
 )
 results['ks'] = ks_drift
 drift_detected = drift_detected or ks_drift

# Wasserstein test
 if 'wasserstein' in test_methods:
 wasserstein_drift = self.wasserstein_drift_test(
 current_probabilities,
 baseline_probabilities,
 drift_threshold
 )
 results['wasserstein'] = wasserstein_drift
 drift_detected = drift_detected or wasserstein_drift

# PSI test
 if 'psi' in test_methods:
 psi_drift = self.psi_drift_test(
 current_probabilities,
 baseline_probabilities,
 drift_threshold
 )
 results['psi'] = psi_drift
 drift_detected = drift_detected or psi_drift

# Merging results
 results['drift_detected'] = drift_detected
 results['timestamp'] = pd.Timestamp.now()
 results['current_samples'] = len(current_probabilities)
 results['baseline_samples'] = len(baseline_probabilities)

# Maintaining history
 self.drift_history.append(results)

# Check allergic
 if self.config['alert_Settings']['enable_alerts']:
 self._check_alerts(results)

 return results

 def statistical_drift_test(self, current, baseline, drift_threshold=None):
 """
Drift statistical test

 Args:
Current (array): Current probability
baseline (array): Baseline probability
drift_threshold (float): Threshold for drift detection

 Returns:
BOOL: Is drift detected
 """
 if drift_threshold is None:
 drift_threshold = self.config['drift_threshold']

 from scipy import stats

# t-test for medium
 t_stat, t_pvalue = stats.ttest_ind(current, baseline)

# Manna Whitney test
 u_stat, u_pvalue = stats.mannwhitneyu(current, baseline)

# Drift criterion
 alpha = self.config['statistical_tests']['ttest_alpha']
 drift_detected = (t_pvalue < alpha) or (u_pvalue < alpha)

 return drift_detected

 def ks_drift_test(self, current, baseline, drift_threshold=None):
 """
Kolmogorov-Smirnov test

 Args:
Current (array): Current probability
baseline (array): Baseline probability
drift_threshold (float): Threshold for drift detection

 Returns:
BOOL: Is drift detected
 """
 if drift_threshold is None:
 drift_threshold = self.config['drift_threshold']

 from scipy import stats

# KS test
 ks_stat, ks_pvalue = stats.ks_2samp(current, baseline)

# Drift criterion
 alpha = self.config['statistical_tests']['ks_alpha']
 drift_detected = ks_pvalue < alpha

 return drift_detected

 def wasserstein_drift_test(self, current, baseline, drift_threshold=None):
 """
Wasserstein Test

 Args:
Current (array): Current probability
baseline (array): Baseline probability
drift_threshold (float): Threshold for drift detection

 Returns:
BOOL: Is drift detected
 """
 if drift_threshold is None:
 drift_threshold = self.config['drift_threshold']

 from scipy.stats import wasserstein_distance

# Calculation of Vasserstein's distance
 wasserstein_dist = wasserstein_distance(current, baseline)

# Drift criterion
 threshold = self.config['statistical_tests']['wasserstein_threshold']
 drift_detected = wasserstein_dist > threshold

 return drift_detected

 def psi_drift_test(self, current, baseline, drift_threshold=None):
 """
PSI Test

 Args:
Current (array): Current probability
baseline (array): Baseline probability
drift_threshold (float): Threshold for drift detection

 Returns:
BOOL: Is drift detected
 """
 if drift_threshold is None:
 drift_threshold = self.config['drift_threshold']

# PSI calculation
 psi_value = self._calculate_psi(current, baseline)

# Drift criterion
 threshold = self.config['statistical_tests']['psi_threshold']
 drift_detected = psi_value > threshold

 return drift_detected

 def _calculate_psi(self, current, baseline, bins=10):
""""""""""" "PSI"""
# Create beans
 min_val = min(np.min(current), np.min(baseline))
 max_val = max(np.max(current), np.max(baseline))
 bin_edges = np.linspace(min_val, max_val, bins + 1)

# Calculation of histograms
 current_hist, _ = np.histogram(current, bins=bin_edges)
 baseline_hist, _ = np.histogram(baseline, bins=bin_edges)

# Normalization
 current_hist = current_hist / np.sum(current_hist)
 baseline_hist = baseline_hist / np.sum(baseline_hist)

# PSI calculation
 psi = 0
 for i in range(len(current_hist)):
 if current_hist[i] > 0 and baseline_hist[i] > 0:
 psi += (current_hist[i] - baseline_hist[i]) * np.log(current_hist[i] / baseline_hist[i])

 return psi

 def _validate_probabilities(self, current, baseline):
"Validation of Probabilities."
# check on missing values
 if self.config['data_quality']['check_Missing']:
 Missing_current = np.isnan(current).sum()
 Missing_baseline = np.isnan(baseline).sum()

 if Missing_current > len(current) * self.config['data_quality']['Missing_threshold']:
 raise ValueError(f"Too many Missing values in current probabilities: {Missing_current}")

 if Missing_baseline > len(baseline) * self.config['data_quality']['Missing_threshold']:
 raise ValueError(f"Too many Missing values in baseline probabilities: {Missing_baseline}")

# check on emissions
 if self.config['data_quality']['check_outliers']:
 current_outliers = self._detect_outliers(current)
 baseline_outliers = self._detect_outliers(baseline)

if Len(surrent_outliers) > Len(surrent) * 0.1: # 10% emissions
 print(f"Warning: High number of outliers in current probabilities: {len(current_outliers)}")

 if len(baseline_outliers) > len(baseline) * 0.1:
 print(f"Warning: High number of outliers in baseline probabilities: {len(baseline_outliers)}")

 def _detect_outliers(self, data, threshold=None):
"Emission detection""
 if threshold is None:
 threshold = self.config['data_quality']['outlier_threshold']

 mean = np.mean(data)
 std = np.std(data)

 outliers = np.abs(data - mean) > threshold * std

 return np.where(outliers)[0]

 def _check_alerts(self, results):
"Check Alerts."
 if results['drift_detected']:
 alert_threshold = self.config['alert_Settings']['alert_threshold']

# Check altar threshold
 if any(results.get(method, False) for method in self.config['test_methods']):
 self._send_alert(results)

 def _send_alert(self, results):
"Sent an allergic."
# Taking out allergies
 print(f"ALERT: Probability drift detected at {results['timestamp']}")
 print(f"Drift details: {results}")
```

## Weaknesses in using probabilities

###1. Retraining on probability

```python
class ProbabilityOverfittingPrevention:
"Prevention of retraining on probability."

 def __init__(self):
 self.regularization_methods = {}

 def prevent_overfitting(self, probabilities, true_labels):
"Prevention of Retraining"

# L1 Regularization
 l1_regularized = self.l1_regularization(probabilities, true_labels)

# L2 Regularization
 l2_regularized = self.l2_regularization(probabilities, true_labels)

# Dropout for Probabilities
 dropout_regularized = self.dropout_regularization(probabilities, true_labels)

 return {
 'l1': l1_regularized,
 'l2': l2_regularized,
 'dropout': dropout_regularized
 }

 def l1_regularization(self, probabilities, true_labels):
""L1 Regularization""

# add L1 fine
 l1_penalty = np.sum(np.abs(probabilities))

# Update probability
 regularized_probs = probabilities - 0.01 * l1_penalty

 return regularized_probs

 def dropout_regularization(self, probabilities, true_labels):
"Dropout regularization."

# Random down part of the probabilities
 dropout_mask = np.random.binomial(1, 0.5, probabilities.shape)
 regularized_probs = probabilities * dropout_mask

 return regularized_probs
```

###2, misinterpretation of probabilities

```python
class ProbabilityInterpretation:
"The correct interpretation of probability."

 def __init__(self):
 self.interpretation_guidelines = {}

 def interpret_probabilities(self, probabilities, context):
"The correct interpretation of probability."

# Context analysis
 context_Analysis = self.analyze_context(context)

# Interpretation adjustment
 corrected_interpretation = self.correct_interpretation(
 probabilities,
 context_Analysis
 )

 return corrected_interpretation

 def analyze_context(self, context):
"Analysis of context for interpretation"

# Market conditions
 market_conditions = context.get('market_conditions', {})

# Temporary factors
 temporal_factors = context.get('temporal_factors', {})

# External factors
 external_factors = context.get('external_factors', {})

 return {
 'market': market_conditions,
 'temporal': temporal_factors,
 'external': external_factors
 }

 def correct_interpretation(self, probabilities, context_Analysis):
""""" "Corresponding"""

# Adjustment on market conditions
 market_corrected = self.market_correction(probabilities, context_Analysis['market'])

# Adjustment on time factors
 temporal_corrected = self.temporal_correction(market_corrected, context_Analysis['temporal'])

# Adjustment on external factors
 external_corrected = self.external_correction(temporal_corrected, context_Analysis['external'])

 return external_corrected
```

### 3. Issues with calibration

```python
class CalibrationIssues:
"Issues with probabilities calibration."

 def __init__(self):
 self.calibration_problems = {}

 def identify_calibration_issues(self, probabilities, true_labels):
""Identification of calibration problems""

# Analysis of the calibration curve
 calibration_curve = self.analyze_calibration_curve(probabilities, true_labels)

# Reliability analysis
 reliability_Analysis = self.analyze_reliability(probabilities, true_labels)

# Analysis of the Resolution
 resolution_Analysis = self.analyze_resolution(probabilities, true_labels)

 return {
 'calibration_curve': calibration_curve,
 'reliability': reliability_Analysis,
 'resolution': resolution_Analysis
 }

 def analyze_calibration_curve(self, probabilities, true_labels):
"Analysis of the calibration curve."

 from sklearn.calibration import calibration_curve

# Building a calibration curve
 fraction_of_positives, mean_predicted_value = calibration_curve(
 true_labels,
 probabilities,
 n_bins=10
 )

# Analysis of variations
 deviations = np.abs(fraction_of_positives - mean_predicted_value)

# Bad calibration criterion
 bad_calibration = np.mean(deviations) > 0.1

 return {
 'curve': (fraction_of_positives, mean_predicted_value),
 'deviations': deviations,
 'bad_calibration': bad_calibration
 }
```

## Best practices in using probabilities

### 1. Validation of probabilities

### ♪ Metrics validation of probabilities

```mermaid
graph TD
A [model probability] --> B{type validation}

B--~♪ Cross-Validation~C[Cross-validation]
B -->\\TemporalValidation\D[Temporal validation]
B --> [Stochastic Planning] E [Stochastic validation]

C --> C1 [Section on Folds]
C --> C2 [Learning on each fold]
C --> C3 [Texting on the rest]

D -> D1 [Temporary rows]
D -> D2 [Learning on the past]
D -> D3 [Text on the future]

E --> E1 [multiple Launchi]
E --> E2 [Incident break-ups]
E --> E3 [Statistical significance]

C1 -> F[metrics of quality]
 C2 --> F
 C3 --> F
 D1 --> F
 D2 --> F
 D3 --> F
 E1 --> F
 E2 --> F
 E3 --> F

 F --> G[Log Loss]
 F --> H[Brier Score]
 F --> I[Calibration Error]

G -> J [Quality assessment]
 H --> J
 I --> J

J --> K {Quality acceptable?}
K--~ ♪ Yeah ♪ L [model ready]
K--~ ~ No~ M[improve model]
 M --> A

 style A fill:#e3f2fd
 style F fill:#c8e6c9
 style J fill:#a5d6a7
 style L fill:#81c784
```

```python
class ProbabilityValidation:
"Validation of Probabilities."

 def __init__(self):
 self.validation_methods = {}

 def validate_probabilities(self, probabilities, true_labels):
"Validation of Probabilities."

# Cross-validation
 cv_validation = self.cross_validation(probabilities, true_labels)

# Temporary validation
 temporal_validation = self.temporal_validation(probabilities, true_labels)

# Stochastic validation
 stochastic_validation = self.stochastic_validation(probabilities, true_labels)

 return {
 'cv': cv_validation,
 'temporal': temporal_validation,
 'stochastic': stochastic_validation
 }

 def cross_validation(self, probabilities, true_labels):
"The Cross-Validation of Probabilities."

 from sklearn.model_selection import cross_val_score

# Cross-validation with calibration
 cv_scores = cross_val_score(
 probabilities,
 true_labels,
 cv=5,
 scoring='neg_log_loss'
 )

 return {
 'scores': cv_scores,
 'mean_score': np.mean(cv_scores),
 'std_score': np.std(cv_scores)
 }
```

### 2. Monitoring performance

```python
class ProbabilityMonitoring:
"Monitoring performance of probability."

 def __init__(self):
 self.Monitoring_metrics = {}

 def monitor_performance(self, probabilities, true_labels):
"""Monitoring performance"""

# Logarithmic loss
 log_loss = self.calculate_log_loss(probabilities, true_labels)

 # Brier Score
 brier_score = self.calculate_brier_score(probabilities, true_labels)

# Sizing error
 calibration_error = self.calculate_calibration_error(probabilities, true_labels)

 return {
 'log_loss': log_loss,
 'brier_score': brier_score,
 'calibration_error': calibration_error
 }

 def calculate_log_loss(self, probabilities, true_labels):
"The calculation of the logarithmic loss."

 from sklearn.metrics import log_loss

# Logarithmic loss
 loss = log_loss(true_labels, probabilities)

 return loss

 def calculate_brier_score(self, probabilities, true_labels):
""Brier Score""

 from sklearn.metrics import brier_score_loss

 # Brier Score
 score = brier_score_loss(true_labels, probabilities)

 return score
```

## Practical examples

♪##1, trading system on probability ♪

### ♪ trading system on basic probabilities

```mermaid
graph TD
A[market data] -> B[ML Model]
B -> C [Prospects of prediction]

C --> D {Analysis of probability}
D--~ ~ 0.8~ E [High confidence]
D -->0.6-0.8\F[Medial confidence]
D -->0.4-0.6\G[Low confidence]
D-~ ~ 0.4~ H [Very low confidence]

E --> E1[BUY Strong Signal]
E --> E2 [Big size of entry]
E --> E3 [Sirocular freeze-loss]

F --> F1[Memature BUY signal]
F --> F2 [average size of entry]
F --> F3 [Normal freeze-loss]

G --> G1 [HOLD weak signal]
G --> G2 [Low size of entry]
G --> G3 [Narrow stop-loss]

H-> H1[SELL signal]
H -> H2 [minimum size]
H --> H3 [Very narrow stop-loss]

E1-> I [Trade Signal Genetics]
 E2 --> I
 E3 --> I
 F1 --> I
 F2 --> I
 F3 --> I
 G1 --> I
 G2 --> I
 G3 --> I
 H1 --> I
 H2 --> I
 H3 --> I

I-> J[Management risk]
J --> K [Secure of the transaction]
K --> L[Monitoring Position]
L --> M {Cancellation}
M--~ ~ Import ~ N[Correction of parameters]
M --\\\\\\O[Analysis of errors]
 N --> A
 O --> A

 style A fill:#e3f2fd
 style C fill:#f3e5f5
 style E fill:#c8e6c9
 style F fill:#fff3e0
 style G fill:#ffe0b2
 style H fill:#ffcdd2
 style I fill:#e1f5fe
```

```python
class ProbabilityTradingsystem:
"""""""""""""""""""""

 def __init__(self, config=None):
 """
Initiating the trading system

 Args:
config (dict): configuring the trading system
- Probability_thresholds: Probability thresholds for signals
- Risk_Management: risk management options
- Signal_energy: parameters of signal generation
- Market_conditions: Market conditions
 """
 self.config = config or self._get_default_config()
 self.probability_thresholds = {}
 self.risk_Management = {}
 self.signal_history = []
 self.performance_metrics = {}

 def _get_default_config(self):
"""""""" "Receive the default configuration"""
 return {
 'probability_thresholds': {
'strong_buy': 0.8, #A strong purchase signal
'Moderate_buy': 0.6, #Memature purchase signal
'Weak_buy': 0.5, #Sweak buying signal
'hold': 0.4, #Keeping position
'Weak_sell': 0.3, # Slow sales signal
'Moderate_sell': 0.2, #Memature sales signal
'strong_sell': 0.1 # Strong sales signal
 },
 'risk_Management': {
'max_position_size': 0.2, # Maximum entry size
'min_position_size': 0.01, #minimum entry size
'stop_loss_threshold': 0.05, #stop-loss threshold
'take_profit_threshold': 0.1 #Take-profit threshold
'max_drawdown': 0.15, # Maximum draught
'risk_per_trade': 0.02, # Risk on the deal
'max_control': 0.7, #maximum correlation
'volatility_threshold': 0.3, #Vulnerability threshold
'liquidity_threshold': 1000000, # Liquidity threshold
'slippage_tolerance': 0.001, #Slipability
'Transaction_costs': 0.001, #Travel costs
'Margin_requirement': 0.1 # Marge requirements
'Leverage_limit': 3.0, # Shoulder Limited
'position_limits': { #Limites of positions
'max_single_position': 0.1 # Maximum entry in one asset
'max_sector_exposure': 0.3, #maximum exposure on sector
'max_currency_exposure': 0.5 # Maximum foreign exchange exposure
 }
 },
 'signal_generation': {
 'signal_types': ['BUY', 'SELL', 'HOLD'],
 'signal_strengths': ['STRONG', 'MODERATE', 'WEAK', 'NONE'],
 'confidence_levels': [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
'signal_validation':rue, #validation signals
'signal_filtering': True, #signal filtering
'signal_aggregation': 'weighted', # Signal Aggregation
'signal_service': 5, #signal intensity (minutes)
'signal_decay': 0.1 # Signal blackout
'signal_memory': 1000, #signal memory
'Signal_learning': True, # Training on signals
'signal_adaptation':True, #Adjusting signals
'signal_optimization': True # Optimization of signals
 },
 'market_conditions': {
'Trend_Analysis':True, # trend analysis
'volatility_Analysis':True, #Vulnerability analysis
'Liquidity_Analysis': True, # Liquidity analysis
'Correllation_Analysis': True, # Correlation analysis
'Momentum_Analysis': True, #Memorandum Analysis
'Support_resistance': True, #Support/Resistance Analysis
'volume_Analysis': True, #volume analysis
'Market_microStructure': True, # MicroStructure Market
'news_sentiment': True, # News sentiment
'Economic_indicators': True, #Economic indicators
'Central_bank_policy':rue, #the central bank policy
'geopolitical_events': True, #geopolitical events
'seasonal_patterns': True, # Seasonal Pathers
'Market_regime': 'normal' # Market mode
 },
 'performance_Monitoring': {
'real_time_Monitoring': True, # Monitoring in real time
 'performance_metrics': ['sharpe', 'sortino', 'calmar', 'max_drawdown'],
'Benchmark_comparison': True, #comparison with benchmarking
'Risk_adjusted_returns':True, #Risk-corrected returns
'attribution_Analisis':True, #Attribution analysis
'stress_testing': True, # Stress testing
'Scenario_Analisis': True, #Scenario Analysis
'Monte_carlo_simulation': True, #Monte Carlo simulation
'Backtesting': True, #Backetsting
'Walk_forward_analysis': True, # Walk-forward analysis
'out_of_sample_testing': True # Extra-sampling testing
 },
 'execution': {
'execution_algorithm': 'TWAP', #performance algorithm
'execution_priority': 'price', #Priority
'execution_time': 'immediate', # Time of execution
'Execution_venue': 'Primary', #The Sign of Performance
'execution_quality': 'high', #performance quality
'execution_cost': 'minimize', #Minimation of value
'execution_risk': 'minimize', #Minimation of risk
'execution_speed': 'fast', #performance speed
'execution_reliability': 'high', #Reliability of performance
'execution_transparency': 'full' # Transparency of performance
 },
 'compliance': {
'Regulatory_compliance': True, #Regulatory compliance
'Risk_limits': True, # Risk Limites
'position_limits': True, #Limites of positions
'Concentration_limites': True, # Concentration limits
'Leverage_limites': True, # Shoulder limits
'liquidity_requirements': True, # Liquidity requirements
'Capital_requirements': True, # Capital requirements
'Reporting_requirements': True, #Reporting requirements
'Audit_trail': True, #Audit-trail
'data_retention': 7, # Data storage (years)
'Privacy_protection': True, #Protection of confidentiality
'data_security': True, #data security
'access_control': True, # Access control
'Encryption': True, #Checking
'backup_recovery': True # Backup
 }
 }

 def generate_trading_signals(self, probabilities, market_data,
 signal_config=None, risk_config=None):
 """
Trade signal generation

 Args:
Probabyties (array): Probability of prediction
Market_data (dict): Market data
Signal_config (dict): configration of signals
Risk_config (dict): configration of risks

 Returns:
List: List of trade signals
 """
 if signal_config is None:
 signal_config = self.config['signal_generation']
 if risk_config is None:
 risk_config = self.config['risk_Management']

# Probability analysis
 prob_Analysis = self.analyze_probabilities(probabilities)

# Signal generation
 signals = self.generate_signals(prob_Analysis, market_data, signal_config)

# Management risks
 risk_adjusted_signals = self.adjust_for_risk(signals, probabilities, risk_config)

# Validation of signals
 if signal_config.get('signal_validation', True):
 validated_signals = self.validate_signals(risk_adjusted_signals)
 else:
 validated_signals = risk_adjusted_signals

# Signal filtering
 if signal_config.get('signal_filtering', True):
 filtered_signals = self.filter_signals(validated_signals)
 else:
 filtered_signals = validated_signals

# Maintaining signal history
 self.signal_history.extend(filtered_signals)

 return filtered_signals

 def analyze_probabilities(self, probabilities):
 """
Probability analysis

 Args:
Probabilities (array): Probability Massive

 Returns:
dict: Probability analysis
 """
# Statistical characteristics
 mean_prob = np.mean(probabilities)
 std_prob = np.std(probabilities)
 max_prob = np.max(probabilities)
 min_prob = np.min(probabilities)
 median_prob = np.median(probabilities)

# Distribution of probabilities
 prob_distribution = self.analyze_distribution(probabilities)

# Confidence analysis
 confidence_Analysis = self.analyze_confidence(probabilities)

# Uncertainties analysis
 uncertainty_Analysis = self.analyze_uncertainty(probabilities)

 return {
 'probabilities': probabilities,
 'mean': mean_prob,
 'std': std_prob,
 'max': max_prob,
 'min': min_prob,
 'median': median_prob,
 'distribution': prob_distribution,
 'confidence': confidence_Analysis,
 'uncertainty': uncertainty_Analysis
 }

 def generate_signals(self, prob_Analysis, market_data, signal_config):
 """
Signal generation

 Args:
prob_Analisis (dict): Probability analysis
Market_data (dict): Market data
Signal_config (dict): configration of signals

 Returns:
List: List signals
 """
 signals = []
 thresholds = self.config['probability_thresholds']

 for i, prob in enumerate(prob_Analysis['probabilities']):
# Definition of the type of signal
 if prob >= thresholds['strong_buy']:
 signal_type = 'BUY'
 strength = 'STRONG'
 confidence = prob
 elif prob >= thresholds['moderate_buy']:
 signal_type = 'BUY'
 strength = 'MODERATE'
 confidence = prob
 elif prob >= thresholds['weak_buy']:
 signal_type = 'BUY'
 strength = 'WEAK'
 confidence = prob
 elif prob <= thresholds['strong_sell']:
 signal_type = 'SELL'
 strength = 'STRONG'
 confidence = 1 - prob
 elif prob <= thresholds['moderate_sell']:
 signal_type = 'SELL'
 strength = 'MODERATE'
 confidence = 1 - prob
 elif prob <= thresholds['weak_sell']:
 signal_type = 'SELL'
 strength = 'WEAK'
 confidence = 1 - prob
 else:
 signal_type = 'HOLD'
 strength = 'NONE'
 confidence = 0.5

# it's the signal
 signal = {
 'type': signal_type,
 'strength': strength,
 'confidence': confidence,
 'timestamp': market_data.get('timestamp', pd.Timestamp.now()),
 'probability': prob,
 'market_conditions': self.analyze_market_conditions(market_data),
 'risk_metrics': self.calculate_risk_metrics(prob, market_data),
 'signal_id': f"signal_{i}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}",
 'generation_time': pd.Timestamp.now(),
 'expiry_time': pd.Timestamp.now() + pd.Timedelta(minutes=signal_config.get('signal_persistence', 5)),
 'priority': self.calculate_signal_priority(signal_type, strength, confidence),
 'metadata': {
 'prob_Analysis': prob_Analysis,
 'market_data': market_data,
 'signal_config': signal_config
 }
 }

 signals.append(signal)

 return signals

 def adjust_for_risk(self, signals, probabilities, risk_config):
 """
Adjustment of risk signals

 Args:
Signals (List): List signals
Probabilities (array): Probabilities
Risk_config (dict): configration of risks

 Returns:
List: Adjusted signals
 """
 adjusted_signals = []

 for signal in signals:
# Calculation of the size of the position
 position_size = self.calculate_position_size(
 signal['probability'],
 risk_config
 )

# Stop-loss calculation
 stop_loss = self.calculate_stop_loss(
 signal['probability'],
 risk_config
 )

# Take-profite calculation
 take_profit = self.calculate_take_profit(
 signal['probability'],
 risk_config
 )

# Update signal
 signal['position_size'] = position_size
 signal['stop_loss'] = stop_loss
 signal['take_profit'] = take_profit
 signal['risk_metrics'] = self.calculate_risk_metrics(
 signal['probability'],
 signal.get('market_conditions', {})
 )

 adjusted_signals.append(signal)

 return adjusted_signals

 def calculate_position_size(self, probability, risk_config):
""""""""""""""""
# Basic position size
 base_size = risk_config.get('risk_per_trade', 0.02)

# Adjustment on Probability
 if probability > 0.8:
 size_multiplier = 1.5
 elif probability > 0.6:
 size_multiplier = 1.0
 elif probability > 0.4:
 size_multiplier = 0.5
 else:
 size_multiplier = 0.1

 position_size = base_size * size_multiplier

# Application of limits
 position_size = max(position_size, risk_config.get('min_position_size', 0.01))
 position_size = min(position_size, risk_config.get('max_position_size', 0.2))

 return position_size

 def calculate_stop_loss(self, probability, risk_config):
"""""" "Stop-Loss"""
 base_stop = risk_config.get('stop_loss_threshold', 0.05)

# Adjustment on Probability
 if probability > 0.8:
step_multiplier = 0.8 # Broader stop-loss
 elif probability > 0.6:
step_multiplier = 1.0 # Conventional Stop-Loss
 else:
step_multiplier = 1.2 #Later stop-loss

 return base_stop * stop_multiplier

 def calculate_take_profit(self, probability, risk_config):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""",""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 base_take = risk_config.get('take_profit_threshold', 0.1)

# Adjustment on Probability
 if probability > 0.8:
Take_multiplier = 1.5 #Big Take Profile
 elif probability > 0.6:
Take_multiplier = 1.0 # Conventional Take Profile
 else:
Take_multiplier = 0.8 #Lower Take Profile

 return base_take * take_multiplier

 def calculate_signal_priority(self, signal_type, strength, confidence):
""""""" "The priority of the signal."
 priority = 0

# Priority on type
 if signal_type == 'BUY':
 priority += 3
 elif signal_type == 'SELL':
 priority += 2
 else:
 priority += 1

# Priority on force
 if strength == 'STRONG':
 priority += 3
 elif strength == 'MODERATE':
 priority += 2
 elif strength == 'WEAK':
 priority += 1

# Priority on confidence
 priority += int(confidence * 5)

 return priority

 def analyze_market_conditions(self, market_data):
"Analysis of Market Conditions"
 conditions = {}

# Trends analysis
 if 'price' in market_data:
 price = market_data['price']
 if len(price) > 1:
 trend = 'up' if price[-1] > price[0] else 'down'
 conditions['trend'] = trend

# Vulnerability analysis
 if 'volatility' in market_data:
 conditions['volatility'] = market_data['volatility']

# Volume analysis
 if 'volume' in market_data:
 conditions['volume'] = market_data['volume']

 return conditions

 def calculate_risk_metrics(self, probability, market_conditions):
""""""" "The calculation of the risk metric."
 metrics = {}

 # VaR (Value at Risk)
 metrics['var_95'] = self.calculate_var(probability, 0.95)
 metrics['var_99'] = self.calculate_var(probability, 0.99)

 # Expected Shortfall
 metrics['expected_shortfall'] = self.calculate_expected_shortfall(probability)

# Maximum tarmac
 metrics['max_drawdown'] = self.calculate_max_drawdown(probability)

 return metrics

 def calculate_var(self, probability, confidence_level):
"" "VaR""
# Simplified calculation of VaR
 return (1 - probability) * (1 - confidence_level)

 def calculate_expected_shortfall(self, probability):
"""""""""""""""
# Simplified calculation of the ES
 return (1 - probability) * 0.5

 def calculate_max_drawdown(self, probability):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Simplified calculation of maximum draught
 return (1 - probability) * 0.3

 def validate_signals(self, signals):
"Validation signals."
 validated_signals = []

 for signal in signals:
# Check mandatory fields
 required_fields = ['type', 'strength', 'confidence', 'timestamp']
 if all(field in signal for field in required_fields):
 validated_signals.append(signal)
 else:
 print(f"Warning: signal Missing required fields: {signal}")

 return validated_signals

 def filter_signals(self, signals):
"Filtration of signals."
 filtered_signals = []

 for signal in signals:
# Filtering on Confidence
if signature['confidence'] > 0.3: # Minimum confidence
 filtered_signals.append(signal)

 return filtered_signals
```

♪##2 ♪ ♪ portfolio management ♪

```python
class ProbabilityPortfolioManagement:
"Management portfolio on base probability."

 def __init__(self):
 self.Portfolio_weights = {}
 self.risk_budget = {}

 def optimize_Portfolio(self, asset_probabilities, risk_budget):
"Optimization of the portfolio."

# Calculation of weights on basic probabilities
 weights = self.calculate_weights(asset_probabilities)

# Risk adjustment
 risk_adjusted_weights = self.adjust_for_risk(weights, risk_budget)

# Optimization of distribution
 optimized_weights = self.optimize_allocation(risk_adjusted_weights)

 return optimized_weights

 def calculate_weights(self, asset_probabilities):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Normalization of probabilities
 normalized_probs = asset_probabilities / np.sum(asset_probabilities)

# Adjustment on variance
 variance_adjusted = self.adjust_for_variance(normalized_probs)

 return variance_adjusted

 def adjust_for_risk(self, weights, risk_budget):
"Corresponding on Risk."

# Calculation of portfolio risk
 Portfolio_risk = self.calculate_Portfolio_risk(weights)

# Weight adjustment
 if Portfolio_risk > risk_budget:
# Decrease in weights
 adjustment_factor = risk_budget / Portfolio_risk
 adjusted_weights = weights * adjustment_factor
 else:
 adjusted_weights = weights

 return adjusted_weights
```

## Conclusion

The correct use of probabilities is the key to creating robotic and profitable ML models. Understanding the strengths and weaknesses allows for more efficient trading systems.

### ♪ Qualitative principles for using probabilities

```mermaid
graph TD
A [The correct use of probabilities] --> B [Calibration]
A --> C[validation]
 A --> D[Monitoring]
A -> E [Interpretation]
A-> F[Risk Management]

 B --> B1[Platt Scaling]
 B --> B2[Isotonic Regression]
 B --> B3[Temperature Scaling]
B1-> G[Exact probability]
 B2 --> G
 B3 --> G

 C --> C1[Cross-Validation]
 C --> C2[Temporal Validation]
 C --> C3[Stochastic Validation]
C1-> H [Reliable assessment]
 C2 --> H
 C3 --> H

D -> D1 [Statistical tests]
D --> D2[KS test]
D --> D3 [Wasserstein distance]
D1-> I [Drift detection]
 D2 --> I
 D3 --> I

E --> E1 [Context analysis]
E --> E2 [market conditions]
E --> E3 [Temporary factors]
E1 -> J [Regulations]
 E2 --> J
 E3 --> J

F --> F1 [Package size]
F --> F2 [Stop-loss]
F --> F3 [Hedging]
F1 -> K [Optimal risk]
 F2 --> K
 F3 --> K

G --> L [Successed ML system]
 H --> L
 I --> L
 J --> L
 K --> L

 style A fill#e3f2fd
 style L fill:#c8e6c9
 style B fill:#f3e5f5
 style C fill:#e8f5e8
 style D fill:#fff3e0
 style E fill:#ffe0b2
 style F fill:#ffcdd2
```

### Key principles

1. ** Calibration** - Always calibrate probability
2. **validation** - Check the probabilities
3. **Monitoring** - monitor probability drift
4. ** Interpretation** - interpret the results correctly
5. ** Risk management** - Use probability for risk management

By following these principles, you can create more accurate and profitable trading systems.

## Summary table of parameters

### parameters calibration probabilities

== sync, corrected by elderman == @elder_man
|----------|----------------------|----------|----------|
&lt; &lt; calibration_methods &&&&&&&&&&&&&&&&&&&&&&& 'temperature' &&&&&\\\\\ &gt;methhods calibrating `&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&}}}}}}}}}}}}}}}}}}}&&&&&&&&&&&&&&&&&&&&'}}}}}}}&&&&&&&&&&}}}}}}}}}}}}}}}}}}}}}}=============='/'
♪ `cv_folds' ~ `5' ♪ Amount of folks for cross-validation ♪ `3-10' ♪
===Temperature ========Temperature_init=====================================================================================================================================================================)==================================================================================================================================================================================================================================================================================================================================
&lt; &lt; isotonic_bounds &gt; &gt; &gt; &gt; &gt; &gt; boundaries for isotonic regression &gt; &gt;['cllip' , 'nan'] &gt;
♪ 'platt_method' ♪ '`sigmoid''' ♪ Method for Platt Scaling ♪ ['sigmoid', 'isotonic'] ♪
♪ `optimization_items' ♪ ♪ 50' ♪ Amount of iterations of optimization ♪ `10-200' ♪
~ `learning_rate' ~ `0.01' ~ learning rate ~ `0.001-0.1' ~
===Reception====================================================================================================================================================)================)===============================)====================================== ============================================================================================================================================================================================================================================================================
== sync, corrected by elderman == @elder_man

♪## risk management parameters

== sync, corrected by elderman == @elder_man
|----------|----------------------|----------|----------|
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman ==
♪ `confidence_threshold' ♪ `0.7' ♪ The confidence threshold ♪ `0.5-0.9' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `hedging_threshold' ♪ `0.3' ♪ Hedging threshold ♪ `0.1-0.5' ♪
♪ `risk_budget' ♪ `0.1' ♪ Risk reserve ♪ `0.01-0.3' ♪
&lt; &lt; correlation_threshold &gt; &gt; &lt; 0.7 &gt; ♪ correlation threshold &gt; &0.3-0.9 &gt; ♪
== sync, corrected by elderman == @elder_man
♪ "rebasement_frequancy" ♪ ♪ rebalancing frequency ♪ ['howly', 'daily', 'weekly'] ♪
♪ `Monitoring_Window' ♪ `30' ♪ Monitoring window(s) ♪ `7-365' ♪
♪ 'alert_threshold' ♪ `0.05' ♪ A threshold for allers ♪ `0.01-0.2' ♪
== sync, corrected by elderman == @elder_man
&lt; &lt;var_confidence &gt; &gt; `0.95 &gt; &gt; &gt; &gt; confidence level for VaR &gt; `0.9-0.99 &gt;
== sync, corrected by elderman == @elder_man
Number of stress-tests scenarios
♪ "liquidity_buffer" ♪ "0.05" ♪ Liquidity Buffer ♪ "0.01-0.2" ♪
♪ `transaction_costs' ♪ `0.001' ♪ Transit costs ♪ `0.001' -0.01' ♪
== sync, corrected by elderman == @elder_man
♪ `market_impact_factor' ♪ `0.001' ♪ Market impact factor ♪ `0.001' ♪

### parameters ensemble

== sync, corrected by elderman == @elder_man
|----------|----------------------|----------|----------|
♪ 'ensemble_methods' ♪ ['weated', 'confidence_weighted', 'bayesian'] ♪ methhods ensemble ♪ ['weighted', 'confidence_weated', 'bayesian'] ♪
&lt; &lt; performance_based &gt; &gt; &gt; &gt; &gt; Method of calculating weights &gt; &gt; &gt; &gt; &lt; conference_based &gt; , &lt; uncertainty_based &gt; &gt;
&lt; `uncertainty_estimation && &gt; &lt; `variance' &gt; &gt; &gt; &gt; &gt; &gt; &gt;
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman ==
== sync, corrected by elderman == @elder_man
♪ `weight_regulation' ♪ ♪ `0.01' ♪ Regularization of weights ♪ `0.01-0.1' ♪
&lt; `uncertainty_threshold &gt; &gt; &lt; 0.1 &gt; \ &lt; &lt;0.01-0.5 &gt; \ &gt;
♪ `confidence_threshold' ♪ `0.7' ♪ The confidence threshold ♪ `0.5-0.9' ♪
&lt; `divesity_weight &gt; &lt; &0.3 &gt; \ &lt; 0.1-0.8 &gt; \ &gt; \ &lt; 0.1 &gt; \ &gt; \ &gt;
~ `Performance_white' ~ `0.7' ~ Weight of performance ~ `0.2-0.9' ~
♪ `uncertainty_weight' ♪ `0.2' ♪ The weight of uncertainty ♪ `0.1-0.5' ♪
&lt; &lt; &lt;adaptive_whites &gt; &gt; &gt; `True &gt; &gt; adaptive weights &gt; `True/False &gt;
~ `weight_update_frequancy' ~ `100' ~ frequency of updates of weights ~ `10-1000' ~
== sync, corrected by elderman == @elder_man
~ `selection_criteria', `['accuracy', 'f1', 'roc_auc'] ``s selection criteria', ``accuracy', 'f1', 'roc_auc', 'log_loss']
&lt; weight_normalitation &gt; &gt; &gt; &lt; softmax &gt; &gt; &gt; &gt; &gt; &gt; &lt; softmax &gt;, &lt; l1', &lt; l2'] &gt; &gt;
== sync, corrected by elderman == @elder_man
? `model_validation' ~ `True' ~ validation of models ~ `True/False' ~
♪ Cross_validation_folds' ♪ ♪ Folds for Cross-Validation ♪ 3-10 ♪
♪ 'bootstrap_samples' ♪ `1000' ♪ Amount of bootstrap samples ♪ `100-10000' ♪
== sync, corrected by elderman == @elder_man
♪ 'Bayesian_prior' ♪ ``uniform''' ♪ Bayesian aprior ♪ ['uniform', 'dirichlet']
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
~ `Temperature_scaling' ~ `True' ~ Temperature scaling ~ `True/False' ~
~ `termerature_value' ~ `1.0' ~ temperature value ~ `0.1-5.0' ~
♪ 'ensemble_validation' ♪ 'True' ♪ ♪ ♪ ♪ True/False' ♪
===Min_weight===The minimum weight is `0.01-0.1'
♪ `max_white' ♪ ♪ `0.5' ♪ ♪ `0.1-0.8' ♪
The sum of the weights should be 1.

### Parameters Monitoring drift

== sync, corrected by elderman == @elder_man
|----------|----------------------|----------|----------|
&lt; &lt; drift_threshold &gt; &lt; 0.05 &gt; &gt; &gt; &gt; &gt; &gt; = &lt;0.01-0.2 &gt;
♪ 'test_methods' ♪ '['statistical', 'ks', 'wasserstein', 'pi'] ♪ testing ♪ ['statistical', 'ks', 'wasserstein', 'psi'] ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `baseline_period' ♪ `30' ♪ period for reference line(s) ♪ `7-365' ♪
== sync, corrected by elderman ==
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `psi_threshold' ♪ `0.2' ♪ The threshold for PSI ♪ `0.1-0.5' ♪
♪ `wasserstein_threshold' ♪ `0.1' ♪ The threshold for Wasserstein ♪ `0.05-0.3' ♪
== sync, corrected by elderman == @elder_man
♪ 'alert_threshold' ♪ `0.1' ♪ Threshold for alllers ♪ `0.05-0.3' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ 'entropy_draft' ♪ 'True' ♪ Drift entropy ♪ 'True/False' ♪
♪ 'auto_adapt' ♪ `False' ♪ Automated adaptation ♪ `True/False' ♪
"Adaptation_threshold" ♪ `0.15' ♪ The threshold for adaptation ♪ `0.05-0.3' ♪
&lt; &lt; adaptation_method &gt; &gt; &gt; &gt; &lt; &lt; &lt; retrain &gt; , `fine_tune &gt; , `transfer &gt; &gt;
~ `adaptation_frequancy' ~ ``weekly'''' `\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ `daily', `weekly', `monthly''}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
== sync, corrected by elderman == @elder_man
♪ `Rollback_threshold' ♪ `0.2' ♪ The threshold for Rollback ♪ `0.1-0.5' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ 'save_plott' ♪ 'True' ♪ 'True/False' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
~ `Check_outliers' ~ `True' ~ check emissions ~ `True/False' ~
~ `outlier_threshold' ~ `3.0' ~ Emission threshold `2.0-5.0' ~
♪ `Missing_threshold' ♪ `0.1' ♪ The threshold for missing values ♪ `0.05-0.3' ♪
~ `data_validation' ~ `True' ~ data validation ~ `True/False' ~
== sync, corrected by elderman == @elder_man
♪ `n_jobs' ~ `-1' ♪ Number of processes ~ `-1, 1-32' ♪
== sync, corrected by elderman == @elder_man
♪ 'cause_results' ♪ 'True' ♪ Cashing results ♪ 'True/False' ♪
♪ 'cause_size' ♪ '1000' ♪ the size of cache ♪ '100-10000' ♪

### parts of the trading system

== sync, corrected by elderman == @elder_man
|----------|----------------------|----------|----------|
♪ `strong_buy' ♪ ♪ `0.8' ♪ Strong purchase signal ♪ `0.7-0.9' ♪
♪ `moderate_buy' ♪ ♪ `0.6' ♪ Moderate purchase signal ♪ `0.5-0.8' ♪
== sync, corrected by elderman == @elder_man
&lt; &lt; &lt; &lt; &lt; 0.4 &gt; &gt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &gt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &lt; &gt; , &lt; &lt; &lt; &lt; &gt; , &lt; &gt; &gt; , &gt; &gt; &gt; , &gt; &gt; , &gt; &gt; &gt; &gt; , &gt; , &gt; &gt; , &gt; &gt; &gt; , &gt; &gt; &gt; , &gt; , &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt;
♪ `weak_sell' ♪ `0.3' ♪ ♪ the in-hand sales signal ♪ `0.2-0.5' ♪
♪ `moderate_sell' ♪ `0.2' ♪ Moderate sales signal ♪ `0.1-0.4' ♪
♪ 'strong_sell' ♪ `0.1' ♪ Strong sales signal ♪ `0.05-0.3' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman ==
~ `stop_loss_threshold' ~ `0.05' ~ Stop-loss threshold ~ `0.01-0.2' ~
~ `take_profit_threshold' ~ `0.1' ~ Take-profit threshold ~ `0.05-0.3' ~
== sync, corrected by elderman == @elder_man
♪ `risk_per_trade' ♪ `0.02' ♪ Risk on the deal ♪ `0.005' ♪
== sync, corrected by elderman == @elder_man
&lt; `volatility_threshold &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &lt; 0.1-0.5 &gt; &gt;
♪ "liquidity_threshold" ♪ "1000000" ♪ Liquidity threshold ♪ "100,000-10000000" ♪
♪ 'slippage_tolerance' ♪ `0.001' ♪ Tolerance for slipping ♪ `0.001' ♪
♪ `transaction_costs' ♪ `0.001' ♪ Transit costs ♪ `0.001' -0.01' ♪
♪ `margin_requirement' ♪ `0.1' ♪ Margin requirements ♪ `0.05-0.5' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ o `signal_validation' ♪ `True' ♪ ♪ signation signals ♪ ♪ 'True/False' ♪
♪ "signal_filtering" ♪ "True" ♪ "True/False" ♪
♪ `signal_aggregation' ♪ ``weighted''' ♪ Aggregation of signals ♪
♪ "signal_service" ♪ "five" ♪ signal intensity (minutes) ♪ "1-60" ♪
&lt; `signal_decay &gt; &gt; &gt; &lt; 0.1 &gt; &gt; &gt; &gt; &gt; &gt; &lt; 0.01-0.5 &gt; &gt;
♪ "signal_memory" ♪ "1000" ♪ Signal memory ♪ "100-10000" ♪
? `signal_learning' ~ `True' ~ training on signals ~ `True/False' ~
♪ "signal_adaptation" ♪ "True" ♪ adaptation of the signals ♪ "True/False" ♪
♪ "signal_optimization" ♪ "True" ♪ "True/False" ♪
♪ "Trend_Analisis" ♪ ♪ "True" ♪ ♪ trend analysis ♪ "True/False" ♪
~ `volatility_Analysis' ~ `True' ~ Volatility analysis ~ `True/False' ~
~ `liquidity_Analysis' ~ `True' ~ Liquidity analysis ~ `True/False' ~
== sync, corrected by elderman ==
== sync, corrected by elderman == @elder_man
Analysis of support/resistance
♪ o `volume_analysis' ♪ o `True' ♪ ♪ Volume analysis ♪ `True/False' ♪
== sync, corrected by elderman == @elder_man
♪ "news_sentiment" ♪ "True" ♪ "True/False" ♪
♪ `economic_indicators' ♪ ♪ `True' ♪ economic indicators ♪ ♪ ‘True/False' ♪
♪ Central_bank_policy ♪ ♪ Central bank policy ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ `market_registry', `growth'] ♪
♪ Real_time_Monitoring' ♪ `True' ♪ Monitoring in real time ♪ `True/False' ♪
| `performance_metrics` | `['sharpe', 'sortino', 'calmar', 'max_drawdown']` | Metrics performance | `['sharpe', 'sortino', 'calmar', 'max_drawdown', 'var', 'es']` |
== sync, corrected by elderman == @elder_man
♪ `risk_adjusted_returs' ♪ `True' ♪ Risk-adjusted returns ♪ `True/False' ♪
The analysis of attribution of `True/False'
♪ Strueze_testing' ♪ ♪ True's Stress Test ♪ ♪ True/False' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ 'backtesting' ♪ ♪ 'True' ♪ Becketting ♪ 'True/False' ♪
== sync, corrected by elderman == @elder_man
~ `out_of_sample_testing' ~ `True' ~ Non-selection testing ~ `True/False' ~
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ 'execution_venue' ♪ ''premary'' ♪ ♪ Performance ♪ ['premary', 'secondary', 'dark_pol'] ♪
\ `execution_quality' ``high'' `\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/ `mediam', `hygh''}\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\&&&&&&&&&&&\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Minimumization of value
Minimumization of risk
♪ 'execution_speed' ♪ ``fast''' ♪ performance rate ♪ ['slow', 'mediam', 'fast'] ♪
"Execution_reliability ``high''' `Reliability of performance' `['low', `mediam', 'hygh'] `
~ `execution_transparency' ~ `full'' '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\, `partial', `full'} \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
"Regulatory_compliance" ♪ "True" ♪ Regulator's compliance ♪ "True/False" ♪
♪ 'Risk_limits' ♪ 'True' ♪ Risk limits ♪ 'True/False' ♪
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
== sync, corrected by elderman == @elder_man
♪ "liquidity_requirements" ♪ "True" ♪ liquidity requirements ♪ "True/False" ♪
♪ capital requirements ♪ `True/False' ♪
~ `Reporting_requirements' ~ `True' ~ requirements for `True/False' ~
♪ 'Audit_trail' ♪ `True' ♪ Audith-treil ♪ 'True/False' ♪
~ `data_retention' ~ `7' ~ Storage of data (years) ~ `1-10' ~
&lt; `privacy_protection &gt; &gt; `True &gt; ♪ Protection of confidentiality &gt; `True/False &gt; ♪
~ `data_security' ~ `True' / data security ~ `True/False' ~
♪ "access_control" ♪ "True" ♪ access controls ♪ "True/False" ♪
♪ "encryption" ♪ ♪ "True" ♪ ♪ "True/Fales" ♪
♪ 'backup_recovery' ♪ 'True' ♪ Reserve copying ♪ 'True/False' ♪

### Recommendations on setting parameters

##### For starters

- Use on default values
- Start with simple calibration methods
- Install conservative risk limits
- Turn on all security checks.

##### for experienced users

- Set the parameters to your data.
- Use advanced methhods ensemble
- Activate adaptive algorithms.
- Set up the Monitoring Drift.

#### # For sale

- Install strict risk limits
- Activate all conformity checks
- Set up allertes and Monitoring.
- Use high-quality performance methods
