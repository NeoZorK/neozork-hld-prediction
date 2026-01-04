# AutoML Gluon Best Practices

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Whoy best practices are critical

**Why 95 percent of the ML projects fail because they ignore the best practices?** Because machine learning is not just "learning the model," and a complex discipline that requires a variety of rules and principles.

### Catastrophic Consultations Bad Practices
- **Amazon AI-recruiting**: Discrimination due to lack of diversity in data
- **Microsoft Tay**: Racist tweets due to lack of modernization
- **Uber self-directed car**: Death of pedestrian due to insufficient testing
- **Facebook algorithm**: Social polarization due to incorrect optimization

### The benefits of following best practices
- ** Reliability**: The Workinget system is stable in all settings
- ** Capacity**: Easy to adapt to increased load
- ** Maintenance**: Command can easily develop system
- **Ethicity**: The Workinget system is fair and safe

## Introduction in best practices

<img src="images/optimized/performance_comparison.png" alt="Comparison performance" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 1: Comparson performance of different models*

<img src="images/optimized/robustness_Analesis.png" alt="Analysis of roboticity" style="max-width: 100%; light: auto; display: block; marguin: 20px auto;">
*Picture 2: Robabistic analysis - Robatic vs re-trained systems, stability performance*

It's a systematic approach to solving typical problems based on the experience of thousands of projects. It's like medical protocols -- they save lives.

**Why 80 percent of ML projects repeat the same mistakes?** Because team no know about the existence of proven solutions:
- **Issues with data**: Incorrect preparation, leaks, offsets
- **Issues with validation**: Wrong division, retraining
- **Issues with sold**: Unprepared for reality
- **Issues with ethics**: Discrimination, prejudice, security

The best practices are the experience gained in the use of AutoML Gluon, which will help to avoid typical errors and achieve maximum efficiency. This section will look at all aspects of the correct use of the tool.

## Data production

<img src="images/optimized/advanced_topics_overView.png" alt="data preparation" style="max-width: 100%; light: auto; display: block; marguin: 20px auto;">
*Figure 3: Best practices in producing data for ML*

** Why is correct data production critical?** Because data quality has a direct impact on model quality:

- **clean data**: remove noise, fix errors
- ** Pass processing**: Strategies for filling missing values
- **Normization**: Bringing data to a single scale
- **Feature Engineering**: new features
- **validation**: quality check and consistence
- ** Documentation**: Recording all changes

###1: Data quality

**Why is "incoming debris = exit debris" especially relevant for ML?** Because the model learns on data, and if data is bad, the model will make bad predictions. It's like teaching a doctor about wrong diagnoses.

♪ Why is 60% of the time of the ML project spent producing data? ♪
- ** No values**: 30-50% of data may be empty
- ** Uncorrect**: Errors, incorrect formats
- **Duplicates**: Same entries in different formats
- ** Emissions**: Extreme values that distort the model

**Tips of problems with data:**
- **Structural problems**: Incorrect data types, formats
- ** Semantic problems**: Uncorrect values, Logsal errors
- ** Statistical problems**: offsets, correlations, emissions
- **Ethical problems**: Discrimination, bias

```python
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

def data_quality_check(data: pd.dataFrame) -> Dict[str, Any]:
 """
Integrated heck of data quality is the first step to a successful ML

 Parameters:
 -----------
 data : pd.dataFrame
The data quality check date should contain:
- Numerical and categorical columns
- Target variable (if present)
- Time tags (for time series)

 Returns:
 --------
 Dict[str, Any]
Vocabulary with quality test results:
- Shape: tuple is the size of the dateset (rows, columns)
- Missing_valutes: dict = number of missing values on columns
- Missing_percent: dict - percentage of missing values on columns
- Data_types: dict - data types on columns
- poplicates: int = number of duplicated lines
- outliers: dict = emissions on numerical columns
- Correlations: dict - correlation matrix between numerical columns

 Notes:
 ------
function uses the following emission detectives:
 - IQR (Interquartile Range): Q1 - 1.5*IQR to Q3 + 1.5*IQR
- Correlations are calculated only for numerical columns
- Duplicates are defined on full match all values
 """

 quality_Report = {
'Shape': data.chape, #The size of the dateset (strings, columns)
'Missing_valutes': Data.isnull().sum(..to_dict(), # Missed values on columns
'data_types': Data.dtypes.to_dict(), #Column data types
'duplicates': data.duplicated(.sum), #Number of duplicate lines
'outliers': {}, # Emissions on numerical columns
'Correllations': {} # Correlations between numerical columns
 }

# sheck missing values
 Missing_percent = (data.isnull().sum() / len(data)) * 100
 quality_Report['Missing_percent'] = Missing_percent.to_dict()

# check emissions for numerical columns
 numeric_columns = data.select_dtypes(include=[np.number]).columns
 for col in numeric_columns:
 Q1 = data[col].quantile(0.25)
 Q3 = data[col].quantile(0.75)
 IQR = Q3 - Q1
 outliers = data[(data[col] < Q1 - 1.5 * IQR) | (data[col] > Q3 + 1.5 * IQR)]
 quality_Report['outliers'][col] = len(outliers)

# Check correlations
 if len(numeric_columns) > 1:
 correlation_matrix = data[numeric_columns].corr()
 quality_Report['correlations'] = correlation_matrix.to_dict()

 return quality_Report

# Use
quality_Report = data_quality_check(train_data)
print("data Quality Report:")
for key, value in quality_Report.items():
 print(f"{key}: {value}")
```

###2: Processing missing values

```python
def handle_Missing_values(data: pd.dataFrame, strategy: str = 'auto') -> pd.dataFrame:
 """
Processing of missing values in the dataset

 Parameters:
 -----------
 data : pd.dataFrame
Data frame with missing values for processing

 strategy : str, default='auto'
Strategy for processing missing values:
- 'auto': Automatic choice of strategy on data type
* for absolute (object) - fashion (most frequently)
* for numerical - median (sustainable to emissions)
- 'drop': remove all line with missing values
* Used when the pass is low (< 5%)
* May significantly reduce the size of the dateset
- 'interpolate': Linear interpolation for time series
* Fits for time data with trend
* Maintains the temporal structure of the data
- 'mean': Filling with average value (only for numerical values)
- 'mode': Fashion filling (most frequently)
- 'forward_fill': Filling in previous value
- 'backward_fill': Filling with the following value

 Returns:
 --------
 pd.dataFrame
Date frame with missing values

 Notes:
 ------
Recommendations on the choice of strategy:
- auto: Universal strategy for most cases
- Drop: When passes are small and data critical
- Interpolate: for time series with trend
- mean/model: When statistical properties need to be preserved
 """

 if strategy == 'auto':
# Automatic strategy - choice on data type
 for col in data.columns:
 if data[col].dtype == 'object':
# for categorical variables - fashion (most common)
# If fashion is empty, Use 'Unknown'
 data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else 'Unknown', inplace=True)
 else:
# for numerical variables - median (sustainable to emissions)
 data[col].fillna(data[col].median(), inplace=True)

 elif strategy == 'drop':
# Remove line with missing values
# Used when the pass is low (< 5%)
 data = data.dropna()

 elif strategy == 'interpolate':
# Interpolation for Time Series
# Maintains the time structure of data
 data = data.interpolate(method='linear')

 elif strategy == 'mean':
# Filling the average value (only for numerical values)
 numeric_cols = data.select_dtypes(include=[np.number]).columns
 data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

 elif strategy == 'mode':
# Fashion filling (most frequently)
 for col in data.columns:
 mode_value = data[col].mode()[0] if not data[col].mode().empty else 'Unknown'
 data[col].fillna(mode_value, inplace=True)

 elif strategy == 'forward_fill':
# Filling in the previous value
 data = data.fillna(method='ffill')

 elif strategy == 'backward_fill':
# Filling in the following value
 data = data.fillna(method='bfill')

 return data

# Use
train_data_clean = handle_Missing_values(train_data, strategy='auto')
```

♪##3 ♪ Emissions treatment

```python
def handle_outliers(data: pd.dataFrame, method: str = 'iqr') -> pd.dataFrame:
 """
Treatment of emissions in numerical data

 Parameters:
 -----------
 data : pd.dataFrame
Data frame with numerical data for emission processing

 method : str, default='iqr'
Emission treatment method:
- 'iqr': Interquartile Wave (IQR)
* Emissions: values < Q1 - 1.5*IQR or > Q3 + 1.5*IQR
* Replaced on boundary values (capping)
Moderate conservative approach
- 'zscore': Z-speed method
* Emissions: ≤z-score ≥ 3 (standard deviation)
* Completely removed from the dateset
:: Aggressive approach, may lose important information
- 'winsorize': Winsorization (restriction)
* Replaces 5% of the lowest and 5% of the highest values
* Maintains the size of the dateset
Conservative approach
- 'solation_forest': Isolation forest
* Using ML for anomaly detectives
:: More complex but precise method
- 'local_outlier_factor': LOF method
* Reflects local data density
* Good for cluster data

 Returns:
 --------
 pd.dataFrame
Date frame with Working emissions

 Notes:
 ------
Recommendations on choice of method:
- iqr: Universal method for most cases
- zscore: When emissions are clearly wrong
- Winsorize: When to save all data
- identification_forest: for complex emission patterns
- Local_outlier_factor: for data with clusters
 """

 numeric_columns = data.select_dtypes(include=[np.number]).columns

 if method == 'iqr':
# Interquartile scale method (IQR)
# Q1 = 25th percentile, Q3 = 75th percentile
 for col in numeric_columns:
Q1 = data[col]. Quantile(0.25) # First quartile
Q3 = data[col]. Quantile(0.75) # Third quartile
IQR = Q3 - Q1 # Interquartile Wave
Lower_bound = Q1 - 1.5 * IQR # Lower border
top_bound = Q3 + 1.5 * IQR # Upper limit

# Replacement of emissions on boundary values
 data[col] = np.where(data[col] < lower_bound, lower_bound, data[col])
 data[col] = np.where(data[col] > upper_bound, upper_bound, data[col])

 elif method == 'zscore':
# Z-speed method (standardized deviation)
# Z-score = (value - average) / standard_deviation
 for col in numeric_columns:
 z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
# Remove lines with ~z-score ~ 3 (aggression approach)
 data = data[z_scores < 3]

 elif method == 'winsorize':
# Vinzorization - limit extreme values
# Replaces 5% of lowest and 5% of highest values
 for col in numeric_columns:
Lower_percentile = data[col]. Quantile(0.05) # 5th percentile
percentile = data[col]. quantile(0.95) #95th percentile
# Replacement of extreme values on percentile
 data[col] = np.where(data[col] < lower_percentile, lower_percentile, data[col])
 data[col] = np.where(data[col] > upper_percentile, upper_percentile, data[col])

 elif method == 'isolation_forest':
# Isolation forest - ML method for the detection of anomalies
 from sklearn.ensemble import IsolationForest
 for col in numeric_columns:
 iso_forest = IsolationForest(contamination=0.1, random_state=42)
 outlier_mask = iso_forest.fit_predict(data[[col]]) == -1
# Replacement of emissions on the median
 data.loc[outlier_mask, col] = data[col].median()

 elif method == 'local_outlier_factor':
# Local Outlier Factor - takes into account local density
 from sklearn.neighbors import LocalOutlierFactor
 for col in numeric_columns:
 lof = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
 outlier_mask = lof.fit_predict(data[[col]]) == -1
# Replacement of emissions on the median
 data.loc[outlier_mask, col] = data[col].median()

 return data

# Use
train_data_no_outliers = handle_outliers(train_data, method='iqr')
```

♪ The choice of metrics

♪##1. metrics for classification

```python
def select_classification_metrics(problem_type: str, data_balance: str = 'balanced') -> List[str]:
 """
Selection of optimal metrics for classification tasks

 Parameters:
 -----------
 problem_type : str
Type of classification task:
- 'binary': Binary classification (2 classes)
- 'multi-class': Multi-class classification (3+ classes)
- 'multibel': Multidimensional classification (a few simultaneous tags)

 data_balance : str, default='balanced'
In-data class balance:
- 'Balanced': Balanced classes (approximately equal number)
- 'imbalanced': Unbalanced classes (one class much larger)
- 'Higly_imbalanced': Strongly unbalanced classes (ratio 1:100+)

 Returns:
 --------
 List[str]
List of recommended metrics for model evaluation:

for binary classification:
- accuracy: Total accuracy (right predictions / all predictions)
- f1: F1-measures (harmonic mean precision and recall)
- roc_auc: Area under ROC-creve (grade separation quality)
- precision: Accuracy (right positive / all positive)
- Recall: Complete (right positive / all real positive)
- Balanced_accuracy: Balanced accuracy (resilient to imbalance)

for multi-class classification:
- f1_macro: F1 measures with macro-averaging (medium on classes)
- f1_micro: F1 measures with micro-averaging (global TP, FP, FN)
- precinct_macro/recall_macro: Macro-average precinct and recall

 Notes:
 ------
Recommendations on choice of metric:
- Balanced data: accuracy, f1, roc_auc
- Unbalanced data: f1, roc_auc, ballanced_accuracy
- Critical cases: precinct
- No major cases allowed: recall
 """

 if problem_type == 'binary':
 if data_balance == 'balanced':
# Balanced data - standard metrics
 return ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']
 elif data_balance == 'imbalanced':
# Unbalanced data - metrics resistant to imbalance
 return ['f1', 'roc_auc', 'precision', 'recall', 'balanced_accuracy']
 else:
# Universal Set for Binary Classification
 return ['accuracy', 'f1', 'roc_auc']

 elif problem_type == 'multiclass':
 if data_balance == 'balanced':
# Balanced multiclass data
 return ['accuracy', 'f1_macro', 'f1_micro', 'precision_macro', 'recall_macro']
 elif data_balance == 'imbalanced':
# Unbalanced multiclass data
 return ['f1_macro', 'f1_micro', 'balanced_accuracy', 'precision_macro', 'recall_macro']
 else:
# Universal Set for Multiclass Classification
 return ['accuracy', 'f1_macro', 'f1_micro']

 else:
# Fallback for unknown types of tasks
 return ['accuracy', 'f1', 'roc_auc']

# Use
metrics = select_classification_metrics('binary', 'imbalanced')
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
Eval_metric=metrics[0] # Basic metric
)
```

###2. metrics for regression

```python
def select_regression_metrics(problem_type: str, target_distribution: str = 'normal') -> List[str]:
 """
Selection of optimal metrics for regression tasks

 Parameters:
 -----------
 problem_type : str
Type of regression task (in this context always 'regression')

 target_distribution : str, default='normal'
Distribution of target variable:
- 'normal': Normal distribution (symmetrical, no emissions)
- 'skewed': Asymmetrical distribution (logarithmic, exponential)
- 'outliers': distribution with emissions (extremum values)
- 'multimedial': Multi-model distribution (a few peaks)
- 'uniform': Equal distribution

 Returns:
 --------
 List[str]
List of recommended metric for the evaluation of the regression model:

Basic metrics:
- rmse: Root Mean Square Error
* Emission sensitive in the same units as the target variable
* Fails big mistakes stronger than small ones
- Mae: Mean Absolute Error (average absolute error)
* Sustainable to emissions, simple for interpretation
* All errors have the same weight
- r2: Determination coefficient (R-squared)
* Proportion of explained variance (0-1, the better)
* Shows model quality relative to average

Specialized devices:
- Mape: Mean Absolute Percentage Error (average absolute percentage error)
* In % expressed, easily interpreted
* Problems in dividing on zero and very small values
 - smape: Symmetric Mean Absolute Percentage Error
* Symmetric version of MAPE, more stable
- Huber_loss: Fuction of Huber's losses
*MAE and MSE combination, emission-resilient
- Mape_log: MAPE on logarithmic scale
* for multiplicative errors

 Notes:
 ------
Recommendations on choice of metric:
- Normal distribution: rmse, mae, r2 (standard set)
- Asymmetrical distribution: mae, mape, smape (per cent metrics)
- Data with emissions: mee, Huber_loss
- Multi-mode distribution: mae, r2
- Equivalent distribution: rmse, mae (standard metrics)
 """

 if target_distribution == 'normal':
# Normal distribution - standard metrics
 return ['rmse', 'mae', 'r2']
 elif target_distribution == 'skewed':
# Asymmetrical distribution - percentage metrics
 return ['mae', 'mape', 'smape']
 elif target_distribution == 'outliers':
# Distribution with emissions - sustainable metrics
 return ['mae', 'huber_loss']
 elif target_distribution == 'multimodal':
# Multi-model distribution - basic metrics
 return ['mae', 'r2', 'rmse']
 elif target_distribution == 'uniform':
# Equivalent distribution - standard metrics
 return ['rmse', 'mae', 'r2']
 else:
# Fallback for unknown distribution types
 return ['rmse', 'mae']

# Use
metrics = select_regression_metrics('regression', 'normal')
predictor = TabularPredictor(
 label='target',
 problem_type='regression',
 eval_metric=metrics[0]
)
```

## configurization of hyperparameters

###1: hyperparameter search strategy

```python
def create_hyperparameter_strategy(data_size: int, problem_type: str) -> Dict[str, Any]:
 """
a strategy to search for hyperparameters on database of data size

 Parameters:
 -----------
 data_size : int
The size of the training dataset (number of lines):
< 1000: Small dataset - simple models, rapid convergence
- 1000-10000: Medium dataset - moderate complexity, quality balance and speed
- > 10000: Large dataset - complex models, high quality

 problem_type : str
The type of task that has to be done is:
- 'binary': Binary classification
- 'multi-class': Multi-class classification
- 'Regression': Regression
- 'multibel': Multi-digit classification

 Returns:
 --------
 Dict[str, Any]
Vocabulary with hyperparameter configurations for different algorithms:

 GBM (Gradient Boosting Machine):
- num_boost_round: Number of iterations of buzting (100-1000)
- Learning_rate: Learning speed (0.01-0.3)
- max_dept: Maximum tree depth (3-12)
- subsample: Proportion of samples for each iteration (0.5-1.0)
- Colsample_bytree: Percentage of signs for each tree (0.5-1.0)

 RF (Random Forest):
- n_estimators: Number of trees (100-1000)
- max_dept: Maximum tree depth (5-25)
- min_samples_split: Minimum sample for knot separation (2-20)
- min_samples_leaf: Minimum sample in sheet (1-10)
- max_features: Number of topics for separation ('sqrt', 'log2', None)

 XGB (XGBoost):
- n_estimators: Number of iterations (100-1000)
- max_dept: Maximum tree depth (3-12)
- Learning_rate: Learning speed (0.01-0.3)
- subsample: Percentage of samples (0.5-1.0)
- Colsample_bytree: Percentage of topics (0.5-1.0)
- reg_alpha: L1 regularization (0-10)
- reg_lambda: L2 regularization (0-10)

 CAT (CatBoost):
- Iterations: Number of iterations (100-1000)
- Learning_rate: Learning speed (0.01-0.3)
- Depth: Tree depth (3-12)
- l2_leaf_reg: L2 regularization (1-10)
- Border_account: Number of boundaries for numbers (32-255)

 Notes:
 ------
Hyperparameter selection strategy:
- Small datasets: Simple models, rapid convergence, avoidance of retraining
- Medium datasets: Balance between quality and speed, moderate complexity
- Large datasets: Complex models, high quality, use of all data
 """

 if data_size < 1000:
# A little dataset - simple models, quick convergence
# Avoid retraining, Use simple configurations
 return {
 'GBM': [{'num_boost_round': 100, 'learning_rate': 0.1, 'max_depth': 3}],
 'RF': [{'n_estimators': 100, 'max_depth': 10, 'min_samples_split': 5}],
 'XGB': [{'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1}]
 }

 elif data_size < 10000:
# Medium dataset - moderate complexity, quality balance and speed
# Use multiple configurations for optimal search
 return {
 'GBM': [
 {'num_boost_round': 200, 'learning_rate': 0.1, 'max_depth': 6},
 {'num_boost_round': 300, 'learning_rate': 0.05, 'max_depth': 8}
 ],
 'RF': [
 {'n_estimators': 200, 'max_depth': 15, 'min_samples_split': 3},
 {'n_estimators': 300, 'max_depth': 20, 'min_samples_split': 2}
 ],
 'XGB': [
 {'n_estimators': 200, 'max_depth': 8, 'learning_rate': 0.1},
 {'n_estimators': 300, 'max_depth': 10, 'learning_rate': 0.05}
 ]
 }

 else:
# Big dateset - complex models, high quality
# Use all available algorithms with optimal parameters
 return {
 'GBM': [
 {'num_boost_round': 500, 'learning_rate': 0.1, 'max_depth': 8},
 {'num_boost_round': 1000, 'learning_rate': 0.05, 'max_depth': 10}
 ],
 'RF': [
 {'n_estimators': 500, 'max_depth': 20, 'min_samples_split': 2},
 {'n_estimators': 1000, 'max_depth': 25, 'min_samples_split': 1}
 ],
 'XGB': [
 {'n_estimators': 500, 'max_depth': 10, 'learning_rate': 0.1},
 {'n_estimators': 1000, 'max_depth': 12, 'learning_rate': 0.05}
 ],
 'CAT': [
 {'iterations': 500, 'learning_rate': 0.1, 'depth': 8},
 {'iterations': 1000, 'learning_rate': 0.05, 'depth': 10}
 ]
 }

# Use
hyperparameters = create_hyperparameter_strategy(len(train_data), 'binary')
predictor.fit(train_data, hyperparameters=hyperparameters)
```

###2: Optimizing learning time

```python
def optimize_training_time(data_size: int, available_time: int) -> Dict[str, Any]:
 """
Optimizing learning time on basis of data size and available time

 Parameters:
 -----------
 data_size : int
The size of the training dataset (number of lines):
< 1000: Small dataset - rapid learning, simple models
- 1000-10000: Average dateset - moderate education, quality balance and speed
- > 10000: Large dataset - quality learning, complex models

 available_time : int
Available time for learning in seconds:
- < 1800 (30 minutes): Rapid learning, simple models
- 1800-7200 (30 minutes - 2 hours): Moderate training
- > 7200 (2+hours): Quality training, complex models

 Returns:
 --------
 Dict[str, Any]
configuring for optimizing learning time:

 time_limit : int
Maximum learning time of one model in seconds
Calculated as available_time / number_models

 presets : str
AutoGluon preset configuration:
- 'optimize_for_development': Rapid learning, simple models
Minimum time, basic quality
* Fits for prototypes and rapid experiments
- 'mediam_quality': Moderate quality, time balance and quality
* Good quality in a reasonable time
:: Suitable for most tasks
- 'high_quality': High quality, long-term learning
* Maximum quality, more time
* Suitable for products and critical tasks
- 'best_quality': Best quality, very long learning
* Maximum quality, very long
:: Fit for research and competition

 num_bag_folds : int
Number of For Bagging Folds (3-10):
- 3: Rapid learning, basic quality
- 5: Standard quality, moderate time
- 10: High quality, long time

 num_bag_sets : int
Bagging sets (1-3):
- 1: Standard Bagging
- 2: Double Bagging for Better Quality
- 3: Triple bagging for maximum quality

 num_stack_levels : int
Number of glass levels (0-2):
- 0: No glassing (rapid learning)
- 1: One level of glassing (moderate quality)
- 2: Two levels of glass (high quality)

 Notes:
 ------
Time optimization strategy:
- Small Datasets: Rapid learning, avoidance of retraining
- Medium datasets: Balance between quality and time
- Large datasets: Quality training, all data use
- Limited time: Simple models, rapid convergence
- Enough time: Complex models, high quality
 """

# Calculation of time on model (10 models on default)
# You can set up the number of models in dependencies from available time
num_models = min(10, max(3, avalable_time //300)) # 3-10 models, minimum 5 minutes on model
 time_per_model = available_time // num_models

 if data_size < 1000:
# Rapid learning for small datasets
# Avoid retraining, Use simple models
 return {
 'time_limit': time_per_model,
 'presets': 'optimize_for_deployment',
'num_bag_folds': 3, #minimum number of folds
'num_bag_sets': 1, #One set of bagging
'num_stack_levels': 0 # Without glassing
 }

 elif data_size < 10000:
# Moderate learning for medium-sized datasets
# Balance between quality and time
 return {
 'time_limit': time_per_model,
 'presets': 'medium_quality',
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 1, #One set of bagging
'num_stack_levels': 1 # One level of glass
 }

 else:
# Qualitative training for large datasets
# Maximum quality, use all data
 return {
 'time_limit': time_per_model,
 'presets': 'high_quality',
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 2, #Double Bagging for Better Quality
'num_stack_levels': 2 # Two levels of glass
 }

# Use
training_config = optimize_training_time(len(training_data), 3600) #1 hour
predictor.fit(train_data, **training_config)
```

## validation and testing

<img src="images/optimized/validation_methods.png" alt="validation and testing" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 4: Best practices in performance and testing of ML models*

**Why is correct validation critical?** Because incorrect validation leads to re-learning and unrealistic estimates:

- **Validation strategies**: Choosing the appropriate method for task
- ** Data division**: Correct division on train/validation/test
- **Cross-validation**: Reliable assessment of performance
** Temporary series**: Special methods for time data
**A/B Testing**: Comparson of models in real world conditions
- **Statistical tests**: heck of differences

♪##1 ♪ ♪ ♪ strategy ♪ ♪ ♪ strategy ♪

```python
def select_validation_strategy(data_size: int, problem_type: str,
 data_type: str = 'tabular') -> Dict[str, Any]:
 """
Selection of the best strategy for the validation on data characteristics

 Parameters:
 -----------
 data_size : int
The size of the training dataset (number of lines):
- < 1000: Small dataset - Holdout validation
- 1000-10000: Medium Dateset - k-fold validation (5 folds)
- > 10000: Large dataset - k-fold validation (10 folds)

 problem_type : str
The type of task that has to be done is:
- 'binary': Binary classification
- 'multi-class': Multi-class classification
- 'Regression': Regression
- 'multibel': Multi-digit classification

 data_type : str, default='tabular'
Data type:
- 'tabular': Table data
- 'time_series': Time series
- 'image': Images
- 'text': Textal data

 Returns:
 --------
 Dict[str, Any]
configurization strategy:

 validation_strategy : str
Type of strategy:
- 'holdout': Simple division on train/validation
* Faster, suitable for big datesets
* May be unstable for small datasets
- 'kfold': K-fold cross-validation
:: More stable rating of performance
* Suitable for medium and large datasets
- 'time_series_split': Temporary validation
* Maintains the temporal structure of the data
* Suitable for time series and forecasting
- 'stratified_kfold': Strategized recovery
* Maintains the proportion of classes in each folde
* Suitable for unbalanced data

 n_splits : int
Number of folds for k-fold validation (3-10):
- 3: Rapid validation, basic quality
- 5: Standard validation, good quality
- 10: Careful satisfaction, high quality

 test_size : float
Proportion of data for testing (0.1-0.3):
0.1: 10% for testing (more data for learning)
0.2: 20% for testing (standard separation)
0.3: 30% for testing (more data for testing)

 holdout_frac : float
Proportion of data for coldout recovery (0.2-0.4):
0.2: 20% for training
0.3: 30 per cent for validation
0.4: 40% for validation (more data for validation)

 num_bag_folds : int
Number of For Bagging Folds (3-10):
- 3: Rapid learning, basic quality
- 5: Standard quality, moderate time
- 10: High quality, long time

 num_bag_sets : int
Bagging sets (1-3):
- 1: Standard Bagging
- 2: Double Bagging for Better Quality
- 3: Triple bagging for maximum quality

 Notes:
 ------
Recommendations on the choice of strategy for validation:
Time series: time_series_split
- Small datasets: Holdout (more data for training)
Medium datasets: k-fold 5 (balance of stability and time)
- Large datasets: k-fold 10 (maximum stability)
- Unbalanced data: stratefied_kfold
 """

 if data_type == 'time_series':
# Time series - special validation
# Keep the time structure of the data
 return {
 'validation_strategy': 'time_series_split',
'n_splits': 5, #The standard number of folds
'test_size': 0.2 # 20% for testing
 }

 elif data_size < 1000:
# A little dataset - Holdout validation
# More data for learning, simple validation
 return {
 'validation_strategy': 'holdout',
'holdout_frac': 0.3 # 30% for validation
 }

 elif data_size < 10000:
# Medium Dateset - k-fold validation
# Balance between stability and time
 return {
 'validation_strategy': 'kfold',
'num_bag_folds': 5, #5 for stability
'num_bag_sets': 1 # One set of bagging
 }

 else:
# Big dateset - expanded k-fold vilification
# Maximum stability of assessment
 return {
 'validation_strategy': 'kfold',
'num_bag_folds': 10, #10 for maximum stability
'num_bag_sets': 1 # One set of bagging
 }

# Use
validation_config = select_validation_strategy(len(train_data), 'binary')
predictor.fit(train_data, **validation_config)
```

♪## 2. Cross-validation ♪

```python
def perform_cross_validation(predictor, data: pd.dataFrame,
 n_folds: int = 5) -> Dict[str, Any]:
♪ Cross-validation performance ♪

 from sklearn.model_selection import KFold
 import numpy as np

 kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

 fold_results = []

 for fold, (train_idx, val_idx) in enumerate(kf.split(data)):
# Data sharing
 train_fold = data.iloc[train_idx]
 val_fold = data.iloc[val_idx]

# Model learning
 fold_predictor = TabularPredictor(
 label=predictor.label,
 problem_type=predictor.problem_type,
 eval_metric=predictor.eval_metric
 )

 fold_predictor.fit(train_fold, time_limit=300)

# Premonition
 predictions = fold_predictor.predict(val_fold)

# Quality assessment
 performance = fold_predictor.evaluate(val_fold)

 fold_results.append({
 'fold': fold + 1,
 'performance': performance
 })

# Aggregation of results
 all_metrics = {}
 for result in fold_results:
 for metric, value in result['performance'].items():
 if metric not in all_metrics:
 all_metrics[metric] = []
 all_metrics[metric].append(value)

# Statistics
 cv_results = {}
 for metric, values in all_metrics.items():
 cv_results[metric] = {
 'mean': np.mean(values),
 'std': np.std(values),
 'min': np.min(values),
 'max': np.max(values)
 }

 return cv_results

# Use
cv_results = perform_cross_validation(predictor, train_data, n_folds=5)
print("Cross-validation results:")
for metric, stats in cv_results.items():
 print(f"{metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

# Working with ensembles

###1. configuring ensemble

```python
def configure_ensemble(data_size: int, problem_type: str) -> Dict[str, Any]:
""Conference ensemble""

 if data_size < 1000:
# Simple ensemble
 return {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0
 }

 elif data_size < 10000:
# Moderate ensemble
 return {
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1
 }

 else:
# A complex ensemble
 return {
 'num_bag_folds': 5,
 'num_bag_sets': 2,
 'num_stack_levels': 2
 }

# Use
ensemble_config = configure_ensemble(len(train_data), 'binary')
predictor.fit(train_data, **ensemble_config)
```

♪##2 ♪ An ensemble analysis ♪

```python
def analyze_ensemble(predictor) -> Dict[str, Any]:
"The Analise of the Ensemble."

# Model leader
 leaderboard = predictor.leaderboard()

# Performance analysis
 ensemble_Analysis = {
 'total_models': len(leaderboard),
 'best_model': leaderboard.iloc[0]['model'],
 'best_score': leaderboard.iloc[0]['score_val'],
 'model_diversity': calculate_model_diversity(leaderboard),
 'performance_gap': leaderboard.iloc[0]['score_val'] - leaderboard.iloc[-1]['score_val']
 }

 return ensemble_Analysis

def calculate_model_diversity(leaderboard: pd.dataFrame) -> float:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Diversity on Model Types
 model_types = leaderboard['model'].str.split('_').str[0].value_counts()
 diversity = len(model_types) / len(leaderboard)

 return diversity

# Use
ensemble_Analysis = analyze_ensemble(predictor)
print("Ensemble Analysis:")
for key, value in ensemble_Analysis.items():
 print(f"{key}: {value}")
```

## Optimizing performance

<img src="images/optimized/metrics_Detained.png" alt="Optimization of performance" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 5: Best Practices for Optimizing Performance ML Models*

Because slow models are inefficient in sales:

- **configuring resources**: Optimal use of CPU, memory, GPU
- ** Parallelization**: Accelerating learning and inference
- ** Cashing**: Maintaining results for reuse
- ** Profiling**: Identification of bottlenecks in performance
- **Monitoring**: Tracing metric performance
- ** Stabbing**: Adapting to increased load

###1. configuring resources

```python
def optimize_resources(data_size: int, available_resources: Dict[str, int]) -> Dict[str, Any]:
 """
Optimizing the use of systemic resources for AutoGluon learning

 Parameters:
 -----------
 data_size : int
The size of the training dataset (number of lines):
< 1000: Small dataset - Minimum resources
- 1000-10000: Medium dataset - Moderate resources
- > 10000: Large Dataset - Maximum Resources

 available_resources : Dict[str, int]
Available systems resources:
- 'cpus':int = number of CPU kernels available (1-64)
- 'memory': int is an accessible memory in GB (4-256)
- 'gpus':int is the number of GPUs available (0-8)
- 'disk': int is an accessible place on disk in GB (100-10000)

 Returns:
 --------
 Dict[str, Any]
Optimized configurization of resources:

 num_cpus : int
Number of CPUs for learning (1-8):
- 1-2: Small datasets, quick experiments
3-4: Secondary, standard training
- 5-8: Large datasets, intensive training
- >8: Very large datasets, maximum performance

 num_gpus : int
Number of GPU for learning (0-8):
- 0: CPU-only training (universal)
- 1: One GPU for accreditation (recommended)
- 2-4: Multiple GPUs for large models
- >4: Extremely large models

 memory_limit : int
Memory Limited in GB (4-64):
- 4-8: Small datasets, simple models
- 8-16: Medium datasets, standard models
- 16-32: Large datasets, complex models
- 32-64: Very large datasets, maximum models

 disk_space : int
Space required on disk in GB (1-100):
- 1-5: Simple models, minimum space
- 5-20: Standard models, moderate place
- 20-50: Complex models, lots of space.
- 50-100: Very complex models, maximum space

 parallel_folds : bool
Simultaneous Folding:
- True: Speeding up learning, more resources
- False: Consistent implementation, less resources

 parallel_models : bool
parallel training models:
- True: Maximum acceleration, lots of resources
- False: sequential training, less resources

 Notes:
 ------
Resource optimization strategy:
- Small Datasets: Minimum Resources, Avoiding Excess
- Medium datasets: Balance between productivity and resources
- Large datasets: Maximum use of resources
- Limited resources: consistent implementation, memory optimization
- Excess resources: parallel implementation, maximum speed
 """

# Calculation of optimal parameters on basis of data size
 if data_size < 1000:
# A little dataset - minimal resources
# Avoid overuse of resources
 num_cpus = min(2, available_resources.get('cpus', 4))
 memory_limit = min(4, available_resources.get('memory', 8))
paralle_folds = False # Consecutive execution
 parallel_models = False # sequential training
Disk_space = 5 # Minimum place on disk

 elif data_size < 10000:
# Medium dataset - Moderate resources
# Balance between productivity and resources
 num_cpus = min(4, available_resources.get('cpus', 8))
 memory_limit = min(8, available_resources.get('memory', 16))
paralle_folds = True # Parallel Folds
paralle_models = Fales # Consequent models
Disk_space = 20 # Moderate place on disk

 else:
# Big dataset - maximum resources
# Use all available resources
 num_cpus = min(8, available_resources.get('cpus', 16))
 memory_limit = min(16, available_resources.get('memory', 32))
paralle_folds = True # Parallel Folds
paralle_models = True # Parallel models
Disk_space = 50 # A lot of space on disk

# Additional optimization on base of available resources
 if available_resources.get('cpus', 0) < 4:
# Limited CPU - Disable parallelism
 parallel_folds = False
 parallel_models = False
 elif available_resources.get('memory', 0) < 8:
# Limited memory - reduce limits
 memory_limit = min(memory_limit, 4)
 parallel_models = False

 return {
 'num_cpus': num_cpus,
 'num_gpus': available_resources.get('gpus', 0),
 'memory_limit': memory_limit,
 'disk_space': disk_space,
 'parallel_folds': parallel_folds,
 'parallel_models': parallel_models
 }

# Use
resources = optimize_resources(len(train_data), {'cpus': 8, 'memory': 16, 'gpus': 1})
predictor.fit(train_data, ag_args_fit=resources)
```

###2, parallelization

```python
def configure_parallelization(data_size: int, problem_type: str) -> Dict[str, Any]:
""configuring parallelization""

 if data_size < 1000:
 # sequential training
 return {
 'parallel_folds': False,
 'parallel_models': False
 }

 elif data_size < 10000:
# Moderate parallelization
 return {
 'parallel_folds': True,
 'parallel_models': False
 }

 else:
# Full parallelization
 return {
 'parallel_folds': True,
 'parallel_models': True
 }

# Use
parallel_config = configure_parallelization(len(train_data), 'binary')
# Application of configuration through ag_args_fit
```

♪ Monitoring and Logsting

<img src="images/optimized/production_architecture.png" alt="Monitoring and Logsrration" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
♪ Figure 6: Best Practices Monitoring and Logging ML Systems ♪

Because models can degradate and Working isn't right:

- ** Logs system**: Detailed fixation of all events
- **Monitorizing quality**: Tracing metric performance
- ** Drift Detective**: Detection of changes in data
**Alerting**: notes on real-time problems
- ** Dashboard**: Visualization of the system
- **Analysis of logs**: Finding causes of problems and optimization

###1: Logsoring system

```python
import logging
from datetime import datetime
import json

class AutoGluonLogger:
""The Logs for AutoGluon System""

 def __init__(self, log_file: str = 'autogluon.log'):
 self.log_file = log_file
 self.setup_logging()

 def setup_logging(self):
""Conference Logs""
 logging.basicConfig(
 level=logging.INFO,
 format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 handlers=[
 logging.FileHandler(self.log_file),
 logging.StreamHandler()
 ]
 )
 self.logger = logging.getLogger(__name__)

 def log_training_start(self, data_info: Dict[str, Any]):
"Logsrance of Starting Learning."
 self.logger.info(f"Training started: {data_info}")

 def log_training_progress(self, progress: Dict[str, Any]):
"Logsuring the progress of learning."
 self.logger.info(f"Training progress: {progress}")

 def log_training_complete(self, results: Dict[str, Any]):
""Logsrance of Completion""
 self.logger.info(f"Training COMPLETED: {results}")

 def log_Prediction(self, input_data: Dict, Prediction: Any,
 processing_time: float):
""Logsrance of Promise""
 log_entry = {
 'timestamp': datetime.now().isoformat(),
 'input_data': input_data,
 'Prediction': Prediction,
 'processing_time': processing_time
 }
 self.logger.info(f"Prediction: {log_entry}")

 def log_error(self, error: Exception, context: Dict[str, Any]):
""Logsir of Mistakes""
 error_entry = {
 'timestamp': datetime.now().isoformat(),
 'error': str(error),
 'context': context
 }
 self.logger.error(f"Error: {error_entry}")

# Use
logger = AutoGluonLogger()
logger.log_training_start({'data_size': len(train_data), 'features': len(train_data.columns)})
```

### 2. Monitoring performance

```python
import psutil
import time
from typing import Dict, Any

class PerformanceMonitor:
"""Monitoring performance"""

 def __init__(self):
 self.metrics_history = []

 def get_system_metrics(self) -> Dict[str, Any]:
"Getting System Metericks."
 return {
 'cpu_percent': psutil.cpu_percent(),
 'memory_percent': psutil.virtual_memory().percent,
 'disk_percent': psutil.disk_usage('/').percent,
 'timestamp': datetime.now().isoformat()
 }

 def monitor_training(self, predictor, data: pd.dataFrame):
"Monitoring Learning."
 start_time = time.time()

# Primary metrics
 initial_metrics = self.get_system_metrics()
 self.metrics_history.append(initial_metrics)

# Learning with Monitoring
 predictor.fit(data, time_limit=3600)

# Final metrics
 final_metrics = self.get_system_metrics()
 final_metrics['training_time'] = time.time() - start_time
 self.metrics_history.append(final_metrics)

 return final_metrics

 def analyze_performance(self) -> Dict[str, Any]:
"Analysis performance."
 if len(self.metrics_history) < 2:
 return {}

# Analysis of resource utilization
 cpu_usage = [m['cpu_percent'] for m in self.metrics_history]
 memory_usage = [m['memory_percent'] for m in self.metrics_history]

 return {
 'avg_cpu_usage': sum(cpu_usage) / len(cpu_usage),
 'max_cpu_usage': max(cpu_usage),
 'avg_memory_usage': sum(memory_usage) / len(memory_usage),
 'max_memory_usage': max(memory_usage),
 'training_time': self.metrics_history[-1].get('training_time', 0)
 }

# Use
monitor = PerformanceMonitor()
final_metrics = monitor.monitor_training(predictor, train_data)
performance_Analysis = monitor.analyze_performance()
print(f"Performance Analysis: {performance_Analysis}")
```

♪ ♪ Mistake processing ♪

###1, processing exceptions

```python
def safe_training(predictor, data: pd.dataFrame, **kwargs) -> Dict[str, Any]:
"Safe learning with error processing."

 try:
# Model learning
 predictor.fit(data, **kwargs)

# Validation model
 if hasattr(predictor, 'evaluate'):
 performance = predictor.evaluate(data)
 return {
 'status': 'success',
 'performance': performance,
 'error': None
 }
 else:
 return {
 'status': 'success',
 'performance': None,
 'error': None
 }

 except MemoryError as e:
 return {
 'status': 'error',
 'performance': None,
 'error': f'Memory error: {str(e)}',
 'suggestion': 'Reduce data size or increase memory'
 }

 except TimeoutError as e:
 return {
 'status': 'error',
 'performance': None,
 'error': f'Timeout error: {str(e)}',
 'suggestion': 'Increase time_limit or reduce model complexity'
 }

 except Exception as e:
 return {
 'status': 'error',
 'performance': None,
 'error': f'Unexpected error: {str(e)}',
 'suggestion': 'check data quality and parameters'
 }

# Use
result = safe_training(predictor, train_data, time_limit=3600)
if result['status'] == 'success':
 print(f"Training successful: {result['performance']}")
else:
 print(f"Training failed: {result['error']}")
 print(f"Suggestion: {result['suggestion']}")
```

###2: Recovery from error

```python
def resilient_training(predictor, data: pd.dataFrame,
 fallback_strategies: List[Dict[str, Any]]) -> Dict[str, Any]:
"Sustainable Learning With Fallback Strategies"

 for i, strategy in enumerate(fallback_strategies):
 try:
# Attempted learning with the current strategy
 predictor.fit(data, **strategy)

# validation
 if validate_model(predictor):
 return {
 'status': 'success',
 'strategy_Used': i,
 'strategy_config': strategy
 }
 else:
 continue

 except Exception as e:
 print(f"Strategy {i} failed: {str(e)}")
 continue

 return {
 'status': 'error',
 'error': 'all strategies failed',
 'suggestions': [
 'check data quality',
 'Reduce model complexity',
 'Increase time limits',
 'Use simpler algorithms'
 ]
 }

# Fallback strategy
fallback_strategies = [
 {'presets': 'best_quality', 'time_limit': 3600},
 {'presets': 'high_quality', 'time_limit': 1800},
 {'presets': 'medium_quality', 'time_limit': 900},
 {'presets': 'optimize_for_deployment', 'time_limit': 300}
]

result = resilient_training(predictor, train_data, fallback_strategies)
```

## Optimization for sales

♪##1 ♪ Model compression

```python
def optimize_for_production(predictor, target_size_mb: int = 100) -> Dict[str, Any]:
"Optimization of the Model for Production"

# Getting the size of the current model
 current_size = get_model_size(predictor)

 if current_size <= target_size_mb:
 return {
 'status': 'already_optimized',
 'current_size': current_size,
 'target_size': target_size_mb
 }

# Optimization strategies
 optimization_strategies = [
 {
 'name': 'reduce_models',
 'config': {
 'excluded_model_types': ['KNN', 'NN_TORCH'],
 'presets': 'optimize_for_deployment'
 }
 },
 {
 'name': 'compress_models',
 'config': {
 'save_space': True,
 'compress': True
 }
 },
 {
 'name': 'simplify_ensemble',
 'config': {
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0
 }
 }
 ]

 for strategy in optimization_strategies:
 try:
# Application of the strategy
 optimized_predictor = apply_optimization_strategy(predictor, strategy)

# Sheck size
 optimized_size = get_model_size(optimized_predictor)

 if optimized_size <= target_size_mb:
 return {
 'status': 'optimized',
 'strategy': strategy['name'],
 'original_size': current_size,
 'optimized_size': optimized_size,
 'compression_ratio': optimized_size / current_size
 }

 except Exception as e:
 print(f"Optimization strategy {strategy['name']} failed: {e}")
 continue

 return {
 'status': 'failed',
 'error': 'Could not achieve target size',
 'suggestions': [
 'Increase target size',
 'Use simpler algorithms',
 'Reduce training data',
 'Use model compression techniques'
 ]
 }

# Use
optimization_result = optimize_for_production(predictor, target_size_mb=50)
print(f"Optimization result: {optimization_result}")
```

♪##2 ♪ Cashing preferences ♪

```python
import hashlib
import json
from typing import Optional

class Predictioncache:
 """
Cashing system for selections for assessment inference

 Parameters:
 -----------
 cache_size : int, default=1000
Maximum cache size:
- 100-500: Small Cash for Simple Systems
- 500-1000: Standard Cash for most tasks
- 1000-5000: Big Cash for Highly Loaded Systems
- 5000+: Very large cache for extreme loads

 Attributes:
 -----------
 cache : Dict[str, Any]
Cashed preferences dictionary
Key: MD5 hash input data
Value: The result of the prediction

 access_count : Dict[str, int]
Caller for each cache element
Used for LRU (Least Recently Used)

 cache_size : int
Maximum cache size

 Notes:
 ------
Cashing strategy:
- LRU (Least Recently Used): remove the least Use elements
- MD5 hashing: Rapid comparison of input data
- Automatic Management Size: Preventing Overcrowding
- Use statistics: Monitoring the effectiveness of cache
 """

 def __init__(self, cache_size: int = 1000):
 self.cache_size = cache_size
 self.cache = {}
 self.access_count = {}

 def _generate_cache_key(self, data: Dict) -> str:
 """
Generating a unique key cache on base input data

 Parameters:
 -----------
 data : Dict
Incoming data for prediction

 Returns:
 --------
 str
MD5 hash input data, Use as cache key

 Notes:
 ------
Key generation algorithm:
1. Serialization of data in JSON with key sorting
2. Coding in UTF-8
3. Calculation of the MD5 hash
4. Return of the sixteenth submission

Benefits of MD5:
- Quick calculation.
- Fixed length (32 symbol)
- Low probability of conflict
- Deterministicity (the same data = the same hash)
 """
 data_str = json.dumps(data, sort_keys=True)
 return hashlib.md5(data_str.encode()).hexdigest()

 def get_Prediction(self, data: Dict) -> Optional[Any]:
 """
Getting a Prophecy From Cache

 Parameters:
 -----------
 data : Dict
Incoming Data for In Cash Search

 Returns:
 --------
 Optional[Any]
Cashed Predation or None if not presento

 Notes:
 ------
Search algorithm:
1. Cache key generation from input data
2. Searching for a key in a cache dictionary
3. Upload call-back counter (LRU)
4. Return of result or None
 """
 cache_key = self._generate_cache_key(data)

 if cache_key in self.cache:
# Update access counter for LRU policy
 self.access_count[cache_key] = self.access_count.get(cache_key, 0) + 1
 return self.cache[cache_key]

 return None

 def set_Prediction(self, data: Dict, Prediction: Any):
 """
Save In Cash Forecast

 Parameters:
 -----------
 data : Dict
Incoming data for caches

 Prediction : Any
The result of the prediction for preservation

 Notes:
 ------
Save algorithm:
1. Cache key generation from input data
2. Check the size of the cache
3. remove the leastUSe element (LRU) if necessary
4. The preservation of a new prophecy
5. Initiating a referral counter
 """
 cache_key = self._generate_cache_key(data)

# Check the size of cache
 if len(self.cache) >= self.cache_size:
# remove the least Use element (LRU)
 least_Used_key = min(self.access_count.keys(), key=self.access_count.get)
 del self.cache[least_Used_key]
 del self.access_count[least_Used_key]

# Add a new element
 self.cache[cache_key] = Prediction
 self.access_count[cache_key] = 1

 def get_cache_stats(self) -> Dict[str, Any]:
 """
Collection of cache use statistics

 Returns:
 --------
 Dict[str, Any]
A dictionary with cache statistics:
- cache_size:int is the current size of cache
== sync, corrected by elderman == @elder_man
- hit_rate: float = impact coefficient (0.0-1.0)
- most_accused: tuple is the mostUSe element
- total_accesses: int - total number of calls
- memory_use: flat - approximate use of memory in MB

 Notes:
 ------
metrics efficiency cache:
- hit_rate: Percentage of queries that were background in cash
- most_accused: The most popular element of cache
- memory_usement: Assessment of memory use
 """
 return {
 'cache_size': len(self.cache),
 'max_cache_size': self.cache_size,
 'hit_rate': self.calculate_hit_rate(),
 'most_accessed': max(self.access_count.items(), key=lambda x: x[1]) if self.access_count else None,
 'total_accesses': sum(self.access_count.values()) if self.access_count else 0,
 'memory_usage': self.estimate_memory_usage()
 }

 def calculate_hit_rate(self) -> float:
 """
Calculation of the cache hit coefficient (hit rate)

 Returns:
 --------
 float
Casualties (0.0-1.0):
- 0.0: No hits (kash ineffective)
0.5: 50% impact (moderate efficiency)
0.8: 80 per cent hits (good performance)
- 0.9+: 90%+ impact (excellent performance)

 Notes:
 ------
Calculation formula:
hit_rate = number of hits / total_number of messages

Where:
number of hits = size_cache
- total_number_transmissions = sum_all_accounts_transmissions
 """
 if not self.access_count:
 return 0.0

 total_accesses = sum(self.access_count.values())
 cache_hits = len(self.cache)
 return cache_hits / total_accesses if total_accesses > 0 else 0.0

 def estimate_memory_usage(self) -> float:
 """
Assessment of the use of caches

 Returns:
 --------
 float
Estimated use of memory in MB

 Notes:
 ------
The assessment is based on:
- The size of the cache dictionary
Average prediction size (approximately 1KB)
- Overhead costs on keys and enumerators
 """
# Indicative estimate: 1KB on Implementation + overhead
 estimated_size_per_item = 1024 # 1KB
 total_items = len(self.cache)
 return (total_items * estimated_size_per_item) / (1024 * 1024) # MB

# Use
cache = Predictioncache(cache_size=1000)

def cached_predict(predictor, data: Dict) -> Any:
"Cashed Pride."
 # check cache
 cached_Prediction = cache.get_Prediction(data)
 if cached_Prediction is not None:
 return cached_Prediction

# The fulfillment of the prophecy
 Prediction = predictor.predict(pd.dataFrame([data]))

# Save in Cash
 cache.set_Prediction(data, Prediction)

 return Prediction
```

♪ Ethics and safety

<img src="images/optimized/metrics_comparison.png" alt="Ethics and safety" style="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
♪ Figure 7: Best practices of ethics and security in ML ♪

**Why is ethics and safety in ML critical?** Because wrong decisions can cause serious harm:

- **justice**: Prevention of discrimination and bias
- ** Transparency**: Explainability of model decisions
- ** Confidentiality**: Personal data protection
- ** Safety**: Protection from attack and abuse
- ** Responsibility**: Clear definition of responsibility for decisions
- ** Regulation**: Compliance with legal requirements

### ♪ Key principles of ethics ML

Because it's the foundation of trust and long-term success:

- ** Principle of justice**: Equal treatment of all groups
- ** Transparency principle**: Understanding solutions for users
- ** Principle of Confidentiality**: Protection of personal data
- ** Safety principle**: Protection from misuse
- ** Principle of responsibility**: clear definition of liability
- ** Principle of "Humanity":** Respect for human rights and dignity

## Next steps

Once you have mastered the best practices, go to:
- [Examples of use](./09_examples.md)
- [Troubleshooting](./10_Troubleshooting.md)
