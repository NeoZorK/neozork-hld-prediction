# Basic Usage of AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Why Start with Basic Usage

**Why do 80% of users start with basic usage?** Because it's the simplest way to understand how AutoML Gluon works. It's like learning to drive - first you learn the basics, then you move on to complex maneuvers.

### What does basic understanding provide?
- **Quick start**: From data to model in a few lines of code
- **Understanding principles**: How AutoML Gluon makes decisions
- **Confidence**: Knowing that everything works correctly
- **Foundation**: Basis for learning advanced techniques

### What happens without basic understanding?
- **Frustration**: You don't understand why the model doesn't work as expected
- **Errors**: Incorrect use of parameters
- **Inefficiency**: Wasting time on things that can be done simpler
- **Disappointment**: Complexity discourages learning

## Introduction to TabularPredictor

<img src="images/optimized/architecture_diagram.png" alt="Architecture AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 1: AutoML Gluon architecture with main components*

**Why is TabularPredictor the heart of AutoML Gluon?** Because it combines all capabilities in one simple interface. It's like a universal remote control - one button launches complex processes.

### 🎯 TabularPredictor Components

<img src="images/optimized/simple_production_flow.png" alt="TabularPredictor components" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 2: Detailed diagram of TabularPredictor components*

**Why is it important to understand components?** Because it helps understand how TabularPredictor automates the entire machine learning process:

- **Data Preprocessing**: Automatic cleaning and preprocessing of data
- **Feature Engineering**: Creating new features from existing ones
- **Model Selection**: Automatic selection of best algorithms
- **Hyperparameter Tuning**: Optimization of model parameters
- **Ensemble Creation**: Creating ensembles for improving accuracy
- **Model Evaluation**: Quality assessment and selection of best model
- **Prediction**: Generating predictions for new data

`TabularPredictor` is the main class for working with tabular data in AutoGluon. It automatically determines the task type (classification, regression) and selects the best algorithms.

### Why is TabularPredictor so important?
- **Automation**: No need to manually select algorithms
- **Intelligence**: Automatically determines task type and metrics
- **Flexibility**: Works with any tabular data
- **Simplicity**: One class solves all tasks

### Import and Create Basic Predictor

**Why start with import?** Because it's the foundation of any Python project. Proper import is like proper tool configuration.

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
```

**Why these specific imports?**
- `TabularPredictor` - main class for working with tabular data
- `pandas` - for working with data in tabular format
- `numpy` - for numerical computations

**Why not import everything at once?** Because it slows down loading and can cause conflicts.

```python
# Create predictor
predictor = TabularPredictor(
label='target_column', # Name of target variable
problem_type='auto', # Automatic task type detection
eval_metric='auto' # Automatic metric selection
)
```

**Parameter explanation:**
- `label='target_column'` - name of column with target variable (what we predict)
- `problem_type='auto'` - AutoML Gluon will automatically determine if it's classification or regression
- `eval_metric='auto'` - automatic selection of best metric for evaluation

**Why use 'auto'?** Because AutoML Gluon is smarter than us in choosing optimal parameters.

#### 🔧 Detailed Description of TabularPredictor Parameters

**Parameter `label`:**

- **What it means**: Name of column with target variable (what we predict)
- **Why it's needed**: Tells AutoML Gluon which variable to predict
- **Required parameter**: Yes, without it AutoML Gluon doesn't know what to predict
- **Naming rules**:
- **Latin letters**: `target`, `label`, `y`
- **With underscores**: `target_column`, `prediction_target`
- **Avoid**: Spaces, special characters, Cyrillic
- **Practical examples**:
- **Classification**: `'is_fraud'`, `'category'`, `'class'`
- **Regression**: `'price'`, `'sales'`, `'temperature'`
- **Time series**: `'value'`, `'forecast'`, `'target'`
- **Existence check**: AutoML Gluon will automatically check that the column exists
- **Error handling**: If column not found, AutoML Gluon will show a clear error

**Parameter `problem_type`:**

- **What it means**: Type of machine learning task
- **Why it's needed**: Determines which algorithms and metrics to use
- **Automatic detection**: `'auto'` - AutoML Gluon will automatically determine the type
- **Manual specification**: Can explicitly specify task type
- **Available values**: - **`'auto'`** - automatic detection (recommended)
- **`'binary'`** - binary classification (2 classes)
- **`'multiclass'`** - multiclass classification (3+ classes)
- **`'regression'`** - regression (predicting numbers)
- **How AutoML Gluon determines type**:
- **Data analysis**: Looks at unique values in target
- **Data type**: Checks if it's numbers or strings
- **Number of classes**: Counts unique values
- **Practical examples**:
- **2 unique values**: `'binary'` (yes/no, spam/not spam)
- **3+ unique values**: `'multiclass'` (categories, classes)
- **Many unique numbers**: `'regression'` (prices, temperatures)
- **Advantages of automatic detection**:
- **Simplicity**: No need to think about task type
- **Accuracy**: AutoML Gluon rarely makes mistakes
- **Flexibility**: Works with any data
- **When to specify manually**:
- **Specific tasks**: When auto detection is incorrect
- **Optimization**: When you know the exact task type
- **Debugging**: When you need to control the process

**Parameter `eval_metric`:**

- **What it means**: Metric for evaluating model quality
- **Why it's needed**: Determines how to measure model quality
- **Automatic selection**: `'auto'` - AutoML Gluon will choose the best metric
- **Manual specification**: Can explicitly specify metric
- **Available metrics by task type**:
- **Classification**: `'accuracy'`, `'f1'`, `'roc_auc'`, `'precision'`, `'recall'`
- **Regression**: `'rmse'`, `'mae'`, `'r2'`, `'mape'`
- **How AutoML Gluon chooses metric**:
- **Binary classification**: `'roc_auc'` (better for imbalanced data)
- **Multiclass classification**: `'accuracy'` (simple and understandable)
- **Regression**: `'rmse'` (standard metric)
- **Practical examples of metric selection**:
- **Medical diagnosis**: `'roc_auc'` (accuracy is important)
- **Recommendations**: `'f1'` (balance of precision and recall)
- **Price forecasting**: `'rmse'` (mean error)
- **Sentiment analysis**: `'accuracy'` (simplicity of interpretation)
- **Impact on training**:
- **Different metrics**: Can give different best models
- **Optimization**: AutoML Gluon optimizes the selected metric
- **Comparison**: Can compare models on different metrics

## Task Types

<img src="images/optimized/automl_theory.png" alt="Machine learning task types" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 3: Overview of machine learning task types in AutoML Gluon*

**Why is it important to understand task types?** Because different tasks require different approaches. It's like the difference between diagnosing a disease and measuring temperature - methods are different.

### 📊 Task Types Comparison

<img src="images/optimized/metrics_Detailed.png" alt="Task types comparison" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 4: Detailed comparison of task types and their metrics*

**Why is it important to compare task types?** Because it helps choose the right approach and metrics for your task:

- **Classification**: Predicting categories (spam/not spam, sick/healthy)
- **Regression**: Predicting numerical values (price, quantity, time)
- **Time series**: Predicting future values based on history
- **Multiclass classification**: Choosing from multiple categories
- **Binary classification**: Simple choice between two options

### Classification

**What is classification?** It's predicting a category or class. For example, spam/not spam, sick/healthy, buyer/not buyer.

**Why is classification so popular?** Because most business tasks are classification:
- Fraud detection
- Medical diagnosis
- Recommendation systems
- Sentiment analysis

```python
# Binary classification
predictor = TabularPredictor(
 label='is_fraud',
 problem_type='binary',
 eval_metric='accuracy'
)
```
**Why is binary classification simpler?** Because there are only two answer options - yes or no.

```python
# Multiclass classification
predictor = TabularPredictor(
 label='category',
 problem_type='multiclass',
 eval_metric='accuracy'
)
```
**Why is multiclass more complex?** Because you need to choose from multiple options, and errors are more costly.

### Regression

**What is regression?** It's predicting a numerical value. For example, house price, sales quantity, time to event.

**Why is regression important?** Because many business metrics are numbers:
- Sales forecasting
- Real estate valuation
- Time prediction
- Financial modeling

```python
# Regression
predictor = TabularPredictor(
 label='price',
 problem_type='regression',
 eval_metric='rmse'
)
```

## Model Training

### 🔄 Model Training Process

<img src="images/optimized/retraining_workflow.png" alt="Model training process" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 5: Detailed diagram of model training process in AutoML Gluon*

**Why is it important to understand the training process?** Because it helps understand what happens inside AutoML Gluon and how to optimize training:

- **Data Loading**: Loading and checking data
- **Feature Engineering**: Automatic feature creation
- **Model Training**: Parallel training of multiple models
- **Hyperparameter Tuning**: Parameter optimization
- **Model Validation**: Model quality assessment
- **Ensemble Creation**: Creating ensembles
- **Model Selection**: Selecting best model
- **Final Evaluation**: Final quality assessment

### Basic Training

```python
# Loading data
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Training model
predictor.fit(train_data)

# Predictions
predictions = predictor.predict(test_data)
```

### Training with Time Limit

```python
# Training with time limit (in seconds)
predictor.fit(
 train_data,
time_limit=3600 # 1 hour
)

# Training with memory limit
predictor.fit(
 train_data,
 memory_limit=8 # 8GB RAM
)
```

#### 🔧 Detailed Description of fit() Method Parameters

**Parameter `time_limit`:**

- **What it means**: Maximum training time in seconds
- **Why it's needed**: Controls training time, prevents infinite training
- **Default**: `None` (no limits)
- **Recommended values**:
- **Quick experiments**: `600` (10 minutes)
- **Standard tasks**: `3600` (1 hour)
- **Important tasks**: `7200` (2 hours)
- **Maximum quality**: `14400` (4 hours)
- **Impact on quality**:
- **Short time**: Basic accuracy, quick results
- **Medium time**: Good accuracy, balanced approach
- **Long time**: Maximum accuracy, best models
- **Optimization by resources**:
- **CPU only**: Increase time by 2-3 times
- **GPU available**: Decrease time by 2-3 times
- **Many cores**: Decrease time by 30-50%
- **Practical examples**:
- **Prototyping**: `time_limit=300` (5 minutes)
- **Development**: `time_limit=1800` (30 minutes)
- **Production**: `time_limit=7200` (2 hours)

**Parameter `memory_limit`:**

- **What it means**: Maximum RAM usage in gigabytes
- **Why it's needed**: Prevents memory overflow, controls resources
- **Default**: `None` (no limits)
- **Recommended values**:
- **Small data (< 1MB)**: `2-4` GB
- **Medium data (1-100MB)**: `4-8` GB
- **Large data (100MB-1GB)**: `8-16` GB
- **Very large data (> 1GB)**: `16-32` GB
- **Impact on performance**:
- **Low memory**: Slow operation, possible errors
- **Sufficient memory**: Fast operation, stability
- **High memory**: Maximum speed, large data processing
- **Optimization by task type**:
- **Classification**: 2-4x data size
- **Regression**: 3-5x data size
- **Time series**: 4-6x data size
- **Usage monitoring**:
 - **Check**: `import psutil; print(f"RAM: {psutil.virtual_memory().percent}%")`
- **Optimal**: 70-80% of available memory
- **Critical**: > 90% of available memory

**Parameter `holdout_frac`:**

- **What it means**: Fraction of data for holdout validation (from 0.0 to 1.0)
- **Why it's needed**: Creates a separate dataset for final model evaluation
- **Default**: `None` (cross-validation is used)
- **Recommended values**:
- **Small data (< 1000 rows)**: `0.1-0.2` (10-20%)
- **Medium data (1000-10000 rows)**: `0.15-0.25` (15-25%)
- **Large data (> 10000 rows)**: `0.2-0.3` (20-30%)
- **Impact on training**:
- **Small holdout**: More data for training, but less reliable evaluation
- **Large holdout**: Less data for training, but more reliable evaluation
- **Practical examples**:
- **Quick testing**: `holdout_frac=0.1` (10%)
- **Standard validation**: `holdout_frac=0.2` (20%)
- **Thorough validation**: `holdout_frac=0.3` (30%)
- **When to use**:
- **Quick evaluation**: When you need to quickly assess quality
- **Large data**: When there's enough data for holdout
- **Final evaluation**: For obtaining objective model assessment

**Parameter `num_bag_folds`:**

- **What it means**: Number of folds for bagging
- **Why it's needed**: Creates an ensemble of models for increased stability
- **Default**: `8` (8 folds)
- **Recommended values**:
- **Quick training**: `3-5` folds
- **Standard training**: `5-8` folds
- **Quality training**: `8-12` folds
- **Maximum quality**: `12-20` folds
- **Impact on quality**:
- **Few folds**: Faster training, but less stable results
- **Many folds**: Slower training, but more stable results
- **Time optimization**:
- **Limited time**: `num_bag_folds=3`
- **Standard time**: `num_bag_folds=5-8`
- **Plenty of time**: `num_bag_folds=10-15`
- **Practical examples**:
- **Prototyping**: `num_bag_folds=3`
- **Development**: `num_bag_folds=5`
- **Production**: `num_bag_folds=8-10`

**Parameter `num_bag_sets`:**

- **What it means**: Number of bagging sets (number of ensembles)
- **Why it's needed**: Creates several independent ensembles for improved quality
- **Default**: `1` (one ensemble)
- **Recommended values**:
- **Quick training**: `1` set
- **Standard training**: `1-2` sets
- **Quality training**: `2-3` sets
- **Maximum quality**: `3-5` sets
- **Impact on quality**:
- **One set**: Faster, but may be less stable
- **Multiple sets**: Slower, but more stable results
- **Resource optimization**:
- **Limited time**: `num_bag_sets=1`
- **Standard time**: `num_bag_sets=1-2`
- **Plenty of time**: `num_bag_sets=2-3`
- **Practical examples**:
- **Quick experiments**: `num_bag_sets=1`
- **Standard tasks**: `num_bag_sets=1-2`
- **Important tasks**: `num_bag_sets=2-3`

**Parameter `num_stack_levels`:**

- **What it means**: Number of stacking levels
- **Why it's needed**: Creates multi-level ensembles for improved quality
- **Default**: `0` (no stacking)
- **Recommended values**:
- **Quick training**: `0` (no stacking)
- **Standard training**: `0-1` level
- **Quality training**: `1-2` levels
- **Maximum quality**: `2-3` levels
- **Impact on quality**:
- **Without stacking**: Faster, but may be less accurate
- **With stacking**: Slower, but often more accurate results
- **Time optimization**:
- **Limited time**: `num_stack_levels=0`
- **Standard time**: `num_stack_levels=1`
- **Plenty of time**: `num_stack_levels=2`
- **Practical examples**:
- **Prototyping**: `num_stack_levels=0`
- **Development**: `num_stack_levels=1`
- **Production**: `num_stack_levels=1-2`

**Parameter `verbosity`:**

- **What it means**: Output detail level (from 0 to 4)
- **Why it's needed**: Controls amount of information output during training
- **Default**: `2` (medium level)
- **Available levels**:
- **`0`** - Errors only
- **`1`** - Minimal information
- **`2`** - Standard information (default)
- **`3`** - Detailed information
- **`4`** - Maximum detail
- **Practical examples**:
- **Production**: `verbosity=1` (minimal output)
- **Development**: `verbosity=2` (standard output)
- **Debugging**: `verbosity=3-4` (detailed output)
- **Impact on performance**:
- **High verbosity**: May slow down training due to large amount of output
- **Low verbosity**: Faster, but less information about the process

**Parameter `callbacks`:**

- **What it means**: List of callback functions for training monitoring
- **Why it's needed**: Allows tracking training progress and performing additional actions
- **Default**: `None` (no callback functions)
- **Callback function types**:
- **Progress monitoring**: Tracking training time
- **Saving intermediate results**: Saving models at each stage
- **Early stopping**: Stopping when certain quality is reached
- **Logging**: Writing information to files
- **Practical examples**:
 - **Monitoring**: `callbacks=[progress_callback]`
- **Saving**: `callbacks=[save_callback]`
- **Early stopping**: `callbacks=[early_stopping_callback]`
- **Callback function examples**:
- **Progress**: Output percentage completion
- **Time**: Tracking training time for each model
- **Quality**: Monitoring metric improvements
- **Resources**: Tracking memory and CPU usage

### Training with Presets

```python
# Different quality presets
presets = [
'best_quality', # Best quality (takes long)
'high_quality', # High quality
'good_quality', # Good quality
'medium_quality', # Medium quality
'optimize_for_deployment' # Optimization for deployment
]

predictor.fit(
 train_data,
 presets='high_quality',
 time_limit=1800 # 30 minutes
)
```

#### 🔧 Detailed Description of Preset Parameters

**Parameter `presets`:**

- **What it means**: Pre-configured model quality settings
- **Why it's needed**: Simplifies choice between speed and quality
- **Default**: `None` (standard configuration)
- **Available presets**: **`'best_quality'`:**
- **What it does**: Maximum model quality
- **Training time**: 4-8 hours
- **Uses**: All available algorithms, ensembles, hyperparameter tuning
- **When to use**: For production, when quality is critical
- **Result**: Best accuracy, but long training time
- **Algorithms**: XGBoost, LightGBM, CatBoost, Neural networks, Ensemble
- **Validation**: 5-fold CV + Holdout
- **Tuning**: 50+ optimization attempts

**`'high_quality'`:**
- **What it does**: High quality with reasonable time
- **Training time**: 2-4 hours
- **Uses**: Main algorithms + ensembles
- **When to use**: For most tasks
- **Result**: Good accuracy in reasonable time
- **Algorithms**: XGBoost, LightGBM, CatBoost, Ensemble
- **Validation**: 3-fold CV + Holdout
- **Tuning**: 20+ optimization attempts

**`'good_quality'`:**
- **What it does**: Good quality in short time
- **Training time**: 30-60 minutes
- **Uses**: Main algorithms without ensembles
- **When to use**: For quick experiments
- **Result**: Acceptable accuracy quickly
- **Algorithms**: XGBoost, LightGBM, CatBoost
- **Validation**: 3-fold CV
- **Tuning**: 10+ optimization attempts

**`'medium_quality'`:**
- **What it does**: Medium quality in very short time
- **Training time**: 10-30 minutes
- **Uses**: Only fast algorithms
- **When to use**: For prototyping
- **Result**: Basic accuracy very quickly
- **Algorithms**: XGBoost, LightGBM
- **Validation**: Holdout
- **Tuning**: 5+ optimization attempts

**`'optimize_for_deployment'`:**
- **What it does**: Optimization for production
- **Training time**: 1-2 hours
- **Uses**: Fast algorithms with optimization
- **When to use**: For production with resource constraints
- **Result**: Fast predictions, good accuracy
- **Algorithms**: XGBoost, LightGBM (optimized)
- **Validation**: 3-fold CV
- **Tuning**: 15+ optimization attempts
- **Features**: Smaller model size, fast predictions

## Model Quality Evaluation

### 📊 Validation and Evaluation Methods

<img src="images/optimized/validation_methods.png" alt="Validation methods" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 6: Different validation and evaluation methods for model quality*

**Why is proper validation important?** Because it ensures reliability and quality of models:

- **Holdout Validation**: Simple train/test split (70/30)
- **Cross-Validation**: K-fold cross-validation for more reliable evaluation
- **Time Series Split**: Special validation for time series
- **Stratified Split**: Preserving class proportions when splitting
- **Walk-Forward Analysis**: Sliding window for time series
- **Bootstrap Validation**: Random sampling with replacement
- **Monte Carlo Validation**: Multiple random splits

### Basic Metrics

```python
# Evaluation on test data
performance = predictor.evaluate(test_data)
print(f"Model performance: {performance}")

# Getting detailed report
performance = predictor.evaluate(
 test_data,
 Detailed_Report=True
)
```

#### 🔧 Detailed Description of evaluate() Method Parameters

**Parameter `Detailed_Report`:**

- **What it means**: Whether to include detailed information in report
- **Why it's needed**: Allows getting detailed information about performance
- **Default**: `False` (basic report)
- **Available values**:
- **`False`** - Basic report (only main metrics)
- **`True`** - Detailed report (all available metrics)
- **Practical examples**:
- **Quick evaluation**: `Detailed_Report=False`
- **Thorough analysis**: `Detailed_Report=True`
- **Impact on result**:
- **Basic report**: Only main metric (accuracy, rmse, etc.)
- **Detailed report**: All available metrics + statistics
- **When to use**:
- **Quick check**: `Detailed_Report=False`
- **Quality analysis**: `Detailed_Report=True`
- **Model debugging**: `Detailed_Report=True`

**Parameter `silent`:**

- **What it means**: Whether to disable information output during evaluation
- **Why it's needed**: Controls amount of output information
- **Default**: `False` (output information)
- **Available values**:
- **`False`** - Output process information
- **`True`** - Perform evaluation silently
- **Practical examples**:
- **Interactive work**: `silent=False`
- **Automated scripts**: `silent=True`
- **Impact on performance**:
- **silent=False**: Slightly slower due to output
- **silent=True**: Faster, but without process information
- **When to use**:
- **Development and debugging**: `silent=False`
- **Production and automation**: `silent=True`

**Parameter `auxiliary_metrics`:**

- **What it means**: Whether to include additional metrics in evaluation
- **Why it's needed**: Allows getting extended set of metrics
- **Default**: `True` (include additional metrics)
- **Available values**:
- **`False`** - Only main metric
- **`True`** - Main + additional metrics
- **Practical examples**:
- **Quick evaluation**: `auxiliary_metrics=False`
- **Full analysis**: `auxiliary_metrics=True`
- **Impact on result**:
- **Without additional metrics**: Only main metric
- **With additional metrics**: Full set of metrics
- **When to use**:
- **Quick check**: `auxiliary_metrics=False`
- **Detailed analysis**: `auxiliary_metrics=True`

**Parameter `as_pandas`:**

- **What it means**: Return result as pandas DataFrame or dictionary
- **Why it's needed**: Controls format of returned data
- **Default**: `True` (pandas DataFrame)
- **Available values**:
- **`True`** - pandas DataFrame (recommended)
- **`False`** - Python dictionary
- **Practical examples**:
- **Data analysis**: `as_pandas=True` (convenient for analysis)
- **Integration with code**: `as_pandas=False` (dictionary)
- **Impact on result**:
- **pandas DataFrame**: Convenient for analysis and visualization
- **Dictionary**: Convenient for programmatic processing
- **When to use**:
- **Analysis and visualization**: `as_pandas=True`
- **Programmatic processing**: `as_pandas=False`

**Parameter `transform_features`:**

- **What it means**: Whether to apply feature transformation before evaluation
- **Why it's needed**: Ensures proper data processing
- **Default**: `True` (apply transformation)
- **Available values**:
- **`True`** - Apply transformation (recommended)
- **`False`** - Do not apply transformation
- **Practical examples**:
- **Raw data**: `transform_features=True`
- **Preprocessed data**: `transform_features=False`
- **Impact on result**:
- **With transformation**: Correct evaluation
- **Without transformation**: May be incorrect evaluation
- **When to use**:
- **New data**: `transform_features=True`
- **Processed data**: `transform_features=False`

**Practical examples of parameter usage:**

```python
# Basic evaluation
performance = predictor.evaluate(test_data)

# Detailed evaluation
Detailed_performance = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 silent=False,
 auxiliary_metrics=True
)

# Quick evaluation
quick_performance = predictor.evaluate(
 test_data,
 Detailed_Report=False,
 silent=True,
 auxiliary_metrics=False
)

# Evaluation for analysis
Analysis_performance = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 silent=False,
 auxiliary_metrics=True,
 as_pandas=True
)

# Evaluation for programmatic processing
programmatic_performance = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 silent=True,
 auxiliary_metrics=True,
 as_pandas=False
)

# Result analysis
print("Basic performance:", performance)
print("Detailed performance shape:", Detailed_performance.shape)
print("Quick performance keys:", quick_performance.keys())
```

**Evaluation performance optimization:**

```python
# Quick evaluation (minimum time)
fast_evaluation = predictor.evaluate(
 test_data,
 Detailed_Report=False,
 silent=True,
 auxiliary_metrics=False,
 as_pandas=False
)

# Full evaluation (maximum information)
full_evaluation = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 silent=False,
 auxiliary_metrics=True,
 as_pandas=True
)

# Evaluation for production (balance of speed and information)
production_evaluation = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 silent=True,
 auxiliary_metrics=True,
 as_pandas=True
)
```

**Evaluation result interpretation:**

```python
# Getting detailed report
performance = predictor.evaluate(
 test_data,
 Detailed_Report=True,
 auxiliary_metrics=True
)

# Main metrics analysis
print("Main metrics:")
print(f"Accuracy: {performance['accuracy']:.4f}")
print(f"F1-score: {performance['f1']:.4f}")
print(f"ROC-AUC: {performance['roc_auc']:.4f}")

# Additional metrics analysis
print("\nAdditional metrics:")
print(f"Precision: {performance['precision']:.4f}")
print(f"Recall: {performance['recall']:.4f}")
print(f"Log Loss: {performance['log_loss']:.4f}")

# Comparison with baseline
baseline_accuracy = 0.5 # for binary classification
improvement = (performance['accuracy'] - baseline_accuracy) / baseline_accuracy * 100
print(f"\nImprovement over baseline: {improvement:.2f}%")
```

### Validation

```python
# Holdout validation
predictor.fit(
 train_data,
holdout_frac=0.2 # 20% of data for validation
)

# K-fold cross-validation
predictor.fit(
 train_data,
 num_bag_folds=5, # 5-fold CV
 num_bag_sets=1
)
```

#### 🔧 Detailed Description of Validation Parameters

**Parameter `holdout_frac` - Holdout validation**

- **What it means**: Fraction of data allocated for holdout validation (from 0.0 to 1.0)
- **Why it's needed**: Creates a separate dataset for final model evaluation
- **Default**: `None` (cross-validation is used)
- **Recommended values**:
- **Small data (< 1000 rows)**: `0.1-0.2` (10-20%)
- **Medium data (1000-10000 rows)**: `0.15-0.25` (15-25%)
- **Large data (> 10000 rows)**: `0.2-0.3` (20-30%)
- **Impact on training**:
- **Small holdout**: More data for training, but less reliable evaluation
- **Large holdout**: Less data for training, but more reliable evaluation
- **Practical examples**:
- **Quick testing**: `holdout_frac=0.1` (10%)
- **Standard validation**: `holdout_frac=0.2` (20%)
- **Thorough validation**: `holdout_frac=0.3` (30%)
- **When to use**:
- **Quick evaluation**: When you need to quickly assess quality
- **Large data**: When there's enough data for holdout
- **Final evaluation**: For obtaining objective model assessment

**Parameter `num_bag_folds` - Number of bagging folds**

- **What it means**: Number of folds for bagging validation
- **Why it's needed**: Creates an ensemble of models for increased stability
- **Default**: `8` (8 folds)
- **Recommended values**:
- **Quick training**: `3-5` folds
- **Standard training**: `5-8` folds
- **Quality training**: `8-12` folds
- **Maximum quality**: `12-20` folds
- **Impact on quality**:
- **Few folds**: Faster training, but less stable results
- **Many folds**: Slower training, but more stable results
- **Time optimization**:
- **Limited time**: `num_bag_folds=3`
- **Standard time**: `num_bag_folds=5-8`
- **Plenty of time**: `num_bag_folds=10-15`
- **Practical examples**:
- **Prototyping**: `num_bag_folds=3`
- **Development**: `num_bag_folds=5`
- **Production**: `num_bag_folds=8-10`

**Parameter `num_bag_sets` - Number of bagging sets**

- **What it means**: Number of bagging sets (number of ensembles)
- **Why it's needed**: Creates several independent ensembles for improved quality
- **Default**: `1` (one ensemble)
- **Recommended values**:
- **Quick training**: `1` set
- **Standard training**: `1-2` sets
- **Quality training**: `2-3` sets
- **Maximum quality**: `3-5` sets
- **Impact on quality**:
- **One set**: Faster, but may be less stable
- **Multiple sets**: Slower, but more stable results
- **Resource optimization**:
- **Limited time**: `num_bag_sets=1`
- **Standard time**: `num_bag_sets=1-2`
- **Plenty of time**: `num_bag_sets=2-3`
- **Practical examples**:
- **Quick experiments**: `num_bag_sets=1`
- **Standard tasks**: `num_bag_sets=1-2`
- **Important tasks**: `num_bag_sets=2-3`

**Parameter `num_stack_levels` - Stacking levels**

- **What it means**: Number of stacking levels for validation
- **Why it's needed**: Creates multi-level ensembles for improved quality
- **Default**: `0` (no stacking)
- **Recommended values**:
- **Quick training**: `0` (no stacking)
- **Standard training**: `0-1` level
- **Quality training**: `1-2` levels
- **Maximum quality**: `2-3` levels
- **Impact on quality**:
- **Without stacking**: Faster, but may be less accurate
- **With stacking**: Slower, but often more accurate results
- **Time optimization**:
- **Limited time**: `num_stack_levels=0`
- **Standard time**: `num_stack_levels=1`
- **Plenty of time**: `num_stack_levels=2`
- **Practical examples**:
- **Prototyping**: `num_stack_levels=0`
- **Development**: `num_stack_levels=1`
- **Production**: `num_stack_levels=1-2`

**Validation strategies:**

```python
# Strategy 1: Quick validation
predictor.fit(
 train_data,
 holdout_frac=0.2,
 num_bag_folds=3,
 num_bag_sets=1,
 num_stack_levels=0
)

# Strategy 2: Standard validation
predictor.fit(
 train_data,
 holdout_frac=0.2,
 num_bag_folds=5,
 num_bag_sets=1,
 num_stack_levels=1
)

# Strategy 3: Quality validation
predictor.fit(
 train_data,
 holdout_frac=0.2,
 num_bag_folds=8,
 num_bag_sets=2,
 num_stack_levels=1
)

# Strategy 4: Maximum quality
predictor.fit(
 train_data,
 holdout_frac=0.2,
 num_bag_folds=10,
 num_bag_sets=3,
 num_stack_levels=2
)
```

**Validation optimization by data size:**

```python
# Small data (< 1000 rows)
small_data_validation = {
 'holdout_frac': 0.1, # 10% for holdout
 'num_bag_folds': 3, # 3-fold CV
'num_bag_sets': 1, # 1 ensemble
'num_stack_levels': 0 # No stacking
}

# Medium data (1000-10000 rows)
medium_data_validation = {
 'holdout_frac': 0.2, # 20% for holdout
 'num_bag_folds': 5, # 5-fold CV
'num_bag_sets': 1, # 1 ensemble
'num_stack_levels': 1 # 1 stacking level
}

# Large data (> 10000 rows)
large_data_validation = {
 'holdout_frac': 0.2, # 20% for holdout
 'num_bag_folds': 8, # 8-fold CV
'num_bag_sets': 2, # 2 ensembles
'num_stack_levels': 1 # 1 stacking level
}
```

**Impact of validation parameters on performance:**

```python
# Parameter impact analysis
def analyze_validation_impact():
"""Analysis of validation parameter impact on time and quality"""

# Configurations for testing
 configs = [
{'name': 'Quick', 'holdout_frac': 0.2, 'num_bag_folds': 3, 'num_bag_sets': 1, 'num_stack_levels': 0},
{'name': 'Standard', 'holdout_frac': 0.2, 'num_bag_folds': 5, 'num_bag_sets': 1, 'num_stack_levels': 1},
{'name': 'Quality', 'holdout_frac': 0.2, 'num_bag_folds': 8, 'num_bag_sets': 2, 'num_stack_levels': 1},
{'name': 'Maximum', 'holdout_frac': 0.2, 'num_bag_folds': 10, 'num_bag_sets': 3, 'num_stack_levels': 2}
 ]

 for config in configs:
print(f"\n{config['name']} validation:")
 print(f" Holdout: {config['holdout_frac']*100}%")
 print(f" Bag folds: {config['num_bag_folds']}")
 print(f" Bag sets: {config['num_bag_sets']}")
 print(f" Stack levels: {config['num_stack_levels']}")

# Time estimation (approximate)
 time_multiplier = (config['num_bag_folds'] * config['num_bag_sets'] *
 (2 ** config['num_stack_levels']))
print(f" Approximate time: {time_multiplier}x baseline")

# Run analysis
analyze_validation_impact()
```

**Recommendations for choosing validation strategy:**

```python
# Recommendations for strategy selection
def choose_validation_strategy(data_size, time_limit, quality_requirement):
"""Choose validation strategy based on requirements"""

 if data_size < 1000:
# Small data - simple validation
 return {
 'holdout_frac': 0.1,
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0
 }
 elif data_size < 10000:
# Medium data - balanced validation
if time_limit < 1800: # Less than 30 minutes
 return {
 'holdout_frac': 0.2,
 'num_bag_folds': 3,
 'num_bag_sets': 1,
 'num_stack_levels': 0
 }
 else:
 return {
 'holdout_frac': 0.2,
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1
 }
 else:
# Large data - quality validation
 if quality_requirement == 'high':
 return {
 'holdout_frac': 0.2,
 'num_bag_folds': 8,
 'num_bag_sets': 2,
 'num_stack_levels': 1
 }
 else:
 return {
 'holdout_frac': 0.2,
 'num_bag_folds': 5,
 'num_bag_sets': 1,
 'num_stack_levels': 1
 }

# Usage examples
small_data_config = choose_validation_strategy(500, 600, 'medium')
medium_data_config = choose_validation_strategy(5000, 1800, 'high')
large_data_config = choose_validation_strategy(50000, 3600, 'high')

print("Configuration for small data:", small_data_config)
print("Configuration for medium data:", medium_data_config)
print("Configuration for large data:", large_data_config)
```

## Predictions

### Basic Predictions

```python
# Class/value predictions
predictions = predictor.predict(test_data)

# Probabilities (for classification)
probabilities = predictor.predict_proba(test_data)
```

#### 🔧 Detailed Description of Prediction Method Parameters

**Method `predict()` - Main Predictions**

**Parameter `include_confidence`:**

- **What it means**: Whether to include confidence intervals in result
- **Why it's needed**: Allows assessing prediction uncertainty
- **Default**: `False` (without confidence intervals)
- **Available values**:
- **`False`** - Only predictions
- **`True`** - Predictions + confidence intervals
- **Practical examples**:
- **Standard predictions**: `include_confidence=False`
- **Risk analysis**: `include_confidence=True`
- **Impact on result**:
- **Without intervals**: Simple array of predictions
- **With intervals**: DataFrame with columns Prediction, lower, upper
- **When to use**:
- **Fast predictions**: When uncertainty assessment is not needed
- **Risk analysis**: When it's important to understand prediction reliability
- **Business decisions**: When uncertainty needs to be considered

**Parameter `as_pandas`:**

- **What it means**: Return result as pandas DataFrame or numpy array
- **Why it's needed**: Controls format of returned data
- **Default**: `True` (pandas DataFrame)
- **Available values**:
- **`True`** - pandas DataFrame (recommended)
 - **`False`** - numpy array
- **Practical examples**:
- **Data analysis**: `as_pandas=True` (convenient for analysis)
- **Integration with other libraries**: `as_pandas=False` (numpy array)
- **Impact on performance**:
- **pandas DataFrame**: Slightly slower, but more convenient
- **numpy array**: Faster, but less convenient for analysis
- **When to use**:
- **Analysis and visualization**: `as_pandas=True`
- **High performance**: `as_pandas=False`
 - **Integration with scikit-learn**: `as_pandas=False`

**Parameter `transform_features`:**

- **What it means**: Whether to apply feature transformation before prediction
- **Why it's needed**: Ensures proper processing of new data
- **Default**: `True` (apply transformation)
- **Available values**:
- **`True`** - Apply transformation (recommended)
- **`False`** - Do not apply transformation
- **Practical examples**:
- **New data**: `transform_features=True` (required)
- **Already processed data**: `transform_features=False`
- **Impact on result**:
- **With transformation**: Correct predictions
- **Without transformation**: May be incorrect predictions
- **When to use**:
- **Raw data**: `transform_features=True`
- **Preprocessed data**: `transform_features=False`

**Method `predict_proba()` - Prediction Probabilities**

**Parameter `as_pandas`:**

- **What it means**: Return result as pandas DataFrame or numpy array
- **Why it's needed**: Controls format of returned probabilities
- **Default**: `True` (pandas DataFrame)
- **Available values**:
- **`True`** - pandas DataFrame with class names
- **`False`** - numpy array with class indices
- **Practical examples**:
- **Probability analysis**: `as_pandas=True` (convenient to read)
- **Mathematical computations**: `as_pandas=False` (faster)
- **Impact on result**:
- **pandas DataFrame**: Columns with class names
- **numpy array**: Columns with class indices
- **When to use**:
- **Result interpretation**: `as_pandas=True`
- **Computations**: `as_pandas=False`

**Parameter `transform_features`:**

- **What it means**: Whether to apply feature transformation before prediction
- **Why it's needed**: Ensures proper processing of new data
- **Default**: `True` (apply transformation)
- **Available values**:
- **`True`** - Apply transformation (recommended)
- **`False`** - Do not apply transformation
- **Practical examples**:
- **New data**: `transform_features=True`
- **Preprocessed data**: `transform_features=False`

### Predictions with Additional Information

```python
# Predictions with confidence intervals
predictions_with_intervals = predictor.predict(
 test_data,
 include_confidence=True
)

# Predictions from individual models
individual_predictions = predictor.predict_multi(test_data)
```

#### 🔧 Detailed Description of Additional Prediction Methods

**Method `predict_multi()` - Predictions from Individual Models**

**Parameter `as_pandas`:**

- **What it means**: Return result as pandas DataFrame or numpy array
- **Why it's needed**: Controls format of returned predictions
- **Default**: `True` (pandas DataFrame)
- **Available values**:
- **`True`** - pandas DataFrame with model names
- **`False`** - numpy array with model indices
- **Practical examples**:
- **Model analysis**: `as_pandas=True` (convenient to compare)
- **Computations**: `as_pandas=False` (faster)
- **Impact on result**:
- **pandas DataFrame**: Columns with model names
- **numpy array**: Columns with model indices
- **When to use**:
- **Model comparison**: `as_pandas=True`
- **Ensembling**: `as_pandas=False`

**Parameter `transform_features`:**

- **What it means**: Whether to apply feature transformation before prediction
- **Why it's needed**: Ensures proper processing of new data
- **Default**: `True` (apply transformation)
- **Available values**:
- **`True`** - Apply transformation (recommended)
- **`False`** - Do not apply transformation
- **Practical examples**:
- **New data**: `transform_features=True`
- **Preprocessed data**: `transform_features=False`

**Method `predict_proba_multi()` - Probabilities from Individual Models**

**Parameter `as_pandas`:**

- **What it means**: Return result as pandas DataFrame or numpy array
- **Why it's needed**: Controls format of returned probabilities
- **Default**: `True` (pandas DataFrame)
- **Available values**:
- **`True`** - pandas DataFrame with model and class names
- **`False`** - numpy array with model and class indices
- **Practical examples**:
- **Probability analysis**: `as_pandas=True` (convenient to read)
- **Computations**: `as_pandas=False` (faster)
- **Impact on result**:
- **pandas DataFrame**: Multi-level columns (model, class)
- **numpy array**: 3D array (samples, models, classes)
- **When to use**:
- **Interpretation**: `as_pandas=True`
- **Computations**: `as_pandas=False`

**Practical examples of parameter usage:**

```python
# Basic predictions
predictions = predictor.predict(test_data)

# Predictions with confidence intervals
predictions_with_confidence = predictor.predict(
 test_data,
 include_confidence=True,
 as_pandas=True
)

# Predictions as numpy array
predictions_numpy = predictor.predict(
 test_data,
 as_pandas=False
)

# Probabilities for classification
probabilities = predictor.predict_proba(test_data)

# Probabilities as numpy array
probabilities_numpy = predictor.predict_proba(
 test_data,
 as_pandas=False
)

# Predictions from individual models
individual_predictions = predictor.predict_multi(test_data)

# Probabilities from individual models
individual_probabilities = predictor.predict_proba_multi(test_data)

# Result analysis
print("Predictions shape:", predictions.shape)
print("Confidence intervals shape:", predictions_with_confidence.shape)
print("Individual predictions shape:", individual_predictions.shape)
print("Individual probabilities shape:", individual_probabilities.shape)
```

**Prediction performance optimization:**

```python
# Fast predictions (without confidence intervals)
fast_predictions = predictor.predict(
 test_data,
 include_confidence=False,
 as_pandas=False,
 transform_features=True
)

# Detailed predictions (with full information)
Detailed_predictions = predictor.predict(
 test_data,
 include_confidence=True,
 as_pandas=True,
 transform_features=True
)

# Predictions for model analysis
model_Analysis = predictor.predict_multi(
 test_data,
 as_pandas=True,
 transform_features=True
)
```

## Working with Features

### Automatic Feature Processing

```python
# AutoGluon automatically processes:
# - Categorical variables (one-hot encoding, label encoding)
# - Missing values (filling, indicators)
# - Numerical variables (normalization, scaling)
# - Text variables (TF-IDF, embeddings)
```

### Manual Feature Configuration

```python
from autogluon.features import FeatureGenerator

# Create feature generator
feature_generator = FeatureGenerator(
 enable_nan_handling=True,
 enable_categorical_encoding=True,
 enable_text_special_features=True,
 enable_text_ngram_features=True
)

# Apply to data
train_data_processed = feature_generator.fit_transform(train_data)
test_data_processed = feature_generator.transform(test_data)
```

## Saving and Loading Models

### Saving Model

```python
# Save model
predictor.save('my_model')

# Save with additional information
predictor.save(
 'my_model',
save_space=True, # Save space
save_info=True # Save metadata
)
```

### Loading Model

```python
# Load saved model
predictor = TabularPredictor.load('my_model')

# Load with compatibility check
predictor = TabularPredictor.load(
 'my_model',
 require_version_match=True
)
```

## Working with Ensembles

### 🤝 Ensemble Working Principles

<img src="images/optimized/robustness_Analysis.png" alt="Ensemble working" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 7: Ensemble working scheme and their advantages*

**Why are ensembles so effective?** Because they combine strengths of different models and compensate for their weaknesses:

- **Bagging**: Training multiple models on different data subsets
- **Boosting**: Sequential training of models focusing on errors
- **Stacking**: Training meta-model on base model predictions
- **Voting**: Simple voting between models
- **Blending**: Weighted combination of predictions
- **Diversity**: Model diversity improves ensemble quality

### Ensemble Configuration

```python
# Training with ensemble
predictor.fit(
 train_data,
num_bag_folds=5, # Number of bagging folds
num_bag_sets=2, # Number of bagging sets
num_stack_levels=1 # Stacking levels
)
```

### Ensemble Analysis

```python
# Information about models in ensemble
leaderboard = predictor.leaderboard()
print(leaderboard)

# Detailed performance information
leaderboard = predictor.leaderboard(
 test_data,
 extra_info=True,
 silent=False
)
```

## Advanced Settings

### ⚙️ Hyperparameter Configuration

<img src="images/optimized/monte_carlo_Analysis.png" alt="Hyperparameter configuration" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 8: Hyperparameter configuration and optimization process*

**Why is hyperparameter configuration important?** Because correct parameters can improve model quality by 10-30%:

- **Grid Search**: Systematic search on parameter grid
- **Random Search**: Random search in parameter space
- **Bayesian Optimization**: Smart search using previous results
- **Evolutionary Algorithms**: Genetic algorithms for optimization
- **Multi-Objective Optimization**: Optimizing multiple metrics simultaneously
- **Early Stopping**: Stopping when no improvements
- **Resource allocation**: Distributing resources between different algorithms

### Hyperparameter Configuration

```python
# Dictionary with settings for different algorithms
hyperparameters = {
 'GBM': [
 {'num_boost_round': 100, 'num_leaves': 31},
 {'num_boost_round': 200, 'num_leaves': 63}
 ],
 'CAT': [
 {'iterations': 100, 'learning_rate': 0.1},
 {'iterations': 200, 'learning_rate': 0.05}
 ],
 'XGB': [
 {'n_estimators': 100, 'max_depth': 6},
 {'n_estimators': 200, 'max_depth': 8}
 ]
}

predictor.fit(
 train_data,
 hyperparameters=hyperparameters
)
```

#### 🔧 Detailed Description of Hyperparameters Structure

**General Structure of Hyperparameters Dictionary:**

```python
hyperparameters = {
 'algorithm_name': [
{'param1': value1, 'param2': value2}, # Option 1
{'param1': value3, 'param2': value4}, # Option 2
# ... more options
 ],
# ... more algorithms
}
```

**Why list of dictionaries?** Because AutoML Gluon will test each option and choose the best one.

**XGBoost (XGB) - Extreme Gradient Boosting**

**Main parameters:**
- **`n_estimators`**: Number of trees (100-1000)
- **`max_depth`**: Maximum tree depth (3-10)
- **`learning_rate`**: Learning rate (0.01-0.3)
- **`subsample`**: Fraction of samples for each tree (0.5-1.0)
- **`colsample_bytree`**: Fraction of features for each tree (0.5-1.0)

**Practical examples:**
```python
'XGB': [
# Fast model
 {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1},
# Balanced model
 {'n_estimators': 200, 'max_depth': 8, 'learning_rate': 0.05},
# Thorough model
 {'n_estimators': 500, 'max_depth': 10, 'learning_rate': 0.01},
# Regularized model
 {'n_estimators': 300, 'max_depth': 6, 'learning_rate': 0.1,
 'subsample': 0.8, 'colsample_bytree': 0.8}
]
```

**LightGBM (GBM) - Gradient Boosting**

**Main parameters:**
- **`num_boost_round`**: Number of boosting iterations (100-1000)
- **`num_leaves`**: Number of leaves in tree (31-255)
- **`learning_rate`**: Learning rate (0.01-0.3)
- **`feature_fraction`**: Fraction of features for each iteration (0.5-1.0)
- **`bagging_fraction`**: Fraction of samples for each iteration (0.5-1.0)

**Practical examples:**
```python
'GBM': [
# Fast model
 {'num_boost_round': 100, 'num_leaves': 31, 'learning_rate': 0.1},
# Balanced model
 {'num_boost_round': 200, 'num_leaves': 63, 'learning_rate': 0.05},
# Thorough model
 {'num_boost_round': 500, 'num_leaves': 127, 'learning_rate': 0.01},
# Regularized model
 {'num_boost_round': 300, 'num_leaves': 63, 'learning_rate': 0.1,
 'feature_fraction': 0.8, 'bagging_fraction': 0.8}
]
```

**CatBoost (CAT) - Categorical Boosting**

**Main parameters:**
- **`iterations`**: Number of iterations (100-1000)
- **`learning_rate`**: Learning rate (0.01-0.3)
- **`depth`**: Tree depth (4-10)
- **`l2_leaf_reg`**: L2 regularization (1-10)
- **`border_count`**: Number of borders for numerical features (32-255)

**Practical examples:**
```python
'CAT': [
# Fast model
 {'iterations': 100, 'learning_rate': 0.1, 'depth': 6},
# Balanced model
 {'iterations': 200, 'learning_rate': 0.05, 'depth': 8},
# Thorough model
 {'iterations': 500, 'learning_rate': 0.01, 'depth': 10},
# Regularized model
 {'iterations': 300, 'learning_rate': 0.1, 'depth': 6,
 'l2_leaf_reg': 3, 'border_count': 128}
]
```

**Random Forest (RF) - Random Forest**

**Main parameters:**
- **`n_estimators`**: Number of trees (100-1000)
- **`max_depth`**: Maximum tree depth (10-50)
- **`min_samples_split`**: Minimum samples for split (2-20)
- **`min_samples_leaf`**: Minimum samples in leaf (1-10)
- **`max_features`**: Number of features for split ('sqrt', 'log2', int)

**Practical examples:**
```python
'RF': [
# Fast model
 {'n_estimators': 100, 'max_depth': 20, 'min_samples_split': 5},
# Balanced model
 {'n_estimators': 200, 'max_depth': 30, 'min_samples_split': 10},
# Thorough model
 {'n_estimators': 500, 'max_depth': 40, 'min_samples_split': 15},
# Regularized model
 {'n_estimators': 300, 'max_depth': 25, 'min_samples_split': 10,
 'min_samples_leaf': 5, 'max_features': 'sqrt'}
]
```

**Extra Trees (XT) - Extra Trees**

**Main parameters:**
- **`n_estimators`**: Number of trees (100-1000)
- **`max_depth`**: Maximum tree depth (10-50)
- **`min_samples_split`**: Minimum samples for split (2-20)
- **`min_samples_leaf`**: Minimum samples in leaf (1-10)
- **`max_features`**: Number of features for split ('sqrt', 'log2', int)

**Practical examples:**
```python
'XT': [
# Fast model
 {'n_estimators': 100, 'max_depth': 20, 'min_samples_split': 5},
# Balanced model
 {'n_estimators': 200, 'max_depth': 30, 'min_samples_split': 10},
# Thorough model
 {'n_estimators': 500, 'max_depth': 40, 'min_samples_split': 15}
]
```

**Neural Networks (NN_TORCH) - Neural Networks**

**Main parameters:**
- **`num_epochs`**: Number of epochs (10-100)
- **`learning_rate`**: Learning rate (0.001-0.1)
- **`batch_size`**: Batch size (32-512)
- **`hidden_size`**: Hidden layer size (64-512)
- **`num_layers`**: Number of layers (2-5)

**Practical examples:**
```python
'NN_TORCH': [
# Fast model
 {'num_epochs': 20, 'learning_rate': 0.01, 'batch_size': 64, 'hidden_size': 128},
# Balanced model
 {'num_epochs': 50, 'learning_rate': 0.005, 'batch_size': 128, 'hidden_size': 256},
# Thorough model
 {'num_epochs': 100, 'learning_rate': 0.001, 'batch_size': 256, 'hidden_size': 512},
# Deep model
 {'num_epochs': 80, 'learning_rate': 0.005, 'batch_size': 128, 'hidden_size': 256,
 'num_layers': 4}
]
```

**Linear Models (LR) - Linear Models**

**Main parameters:**
- **`C`**: Inverse regularization strength (0.01-100)
- **`penalty`**: Regularization type ('l1', 'l2', 'elasticnet')
- **`solver`**: Optimization algorithm ('liblinear', 'lbfgs', 'saga')
- **`max_iter`**: Maximum number of iterations (100-1000)

**Practical examples:**
```python
'LR': [
# L2 regularization
 {'C': 1.0, 'penalty': 'l2', 'solver': 'liblinear', 'max_iter': 1000},
# L1 regularization
 {'C': 0.1, 'penalty': 'l1', 'solver': 'liblinear', 'max_iter': 1000},
# ElasticNet regularization
 {'C': 0.5, 'penalty': 'elasticnet', 'solver': 'saga', 'max_iter': 1000},
# Strong regularization
 {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs', 'max_iter': 2000}
]
```

**K-Nearest Neighbors (KNN) - K Nearest Neighbors**

**Main parameters:**
- **`n_neighbors`**: Number of neighbors (3-20)
- **`weights`**: Weight function ('uniform', 'distance')
- **`algorithm`**: Search algorithm ('auto', 'ball_tree', 'kd_tree', 'brute')
- **`metric`**: Distance metric ('euclidean', 'manhattan', 'minkowski')

**Practical examples:**
```python
'KNN': [
# Fast model
 {'n_neighbors': 5, 'weights': 'uniform', 'algorithm': 'auto'},
# Balanced model
 {'n_neighbors': 10, 'weights': 'distance', 'algorithm': 'auto'},
# Thorough model
 {'n_neighbors': 15, 'weights': 'distance', 'algorithm': 'ball_tree'},
# Specialized model
 {'n_neighbors': 8, 'weights': 'distance', 'algorithm': 'kd_tree',
 'metric': 'manhattan'}
]
```

**Complete Example of Hyperparameter Settings:**

```python
# Comprehensive hyperparameter configuration
hyperparameters = {
# XGBoost - fast and thorough options
 'XGB': [
 {'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1},
 {'n_estimators': 300, 'max_depth': 8, 'learning_rate': 0.05},
 {'n_estimators': 500, 'max_depth': 10, 'learning_rate': 0.01}
 ],

# LightGBM - balanced options
 'GBM': [
 {'num_boost_round': 200, 'num_leaves': 63, 'learning_rate': 0.1},
 {'num_boost_round': 400, 'num_leaves': 127, 'learning_rate': 0.05},
 {'num_boost_round': 600, 'num_leaves': 255, 'learning_rate': 0.01}
 ],

# CatBoost - for categorical data
 'CAT': [
 {'iterations': 200, 'learning_rate': 0.1, 'depth': 6},
 {'iterations': 400, 'learning_rate': 0.05, 'depth': 8},
 {'iterations': 600, 'learning_rate': 0.01, 'depth': 10}
 ],

# Random Forest - for interpretability
 'RF': [
 {'n_estimators': 200, 'max_depth': 25, 'min_samples_split': 10},
 {'n_estimators': 400, 'max_depth': 35, 'min_samples_split': 15},
 {'n_estimators': 600, 'max_depth': 45, 'min_samples_split': 20}
 ],

# Neural networks - for complex patterns
 'NN_TORCH': [
 {'num_epochs': 50, 'learning_rate': 0.01, 'batch_size': 128, 'hidden_size': 256},
 {'num_epochs': 100, 'learning_rate': 0.005, 'batch_size': 256, 'hidden_size': 512},
 {'num_epochs': 150, 'learning_rate': 0.001, 'batch_size': 512, 'hidden_size': 1024}
 ]
}

# Training with hyperparameter tuning
predictor.fit(
 train_data,
 hyperparameters=hyperparameters,
time_limit=3600 # 1 hour
)
```

**Hyperparameter Setting Strategies:**

```python
# Strategy 1: Quick testing
quick_hyperparameters = {
 'XGB': [{'n_estimators': 100, 'max_depth': 6, 'learning_rate': 0.1}],
 'GBM': [{'num_boost_round': 200, 'num_leaves': 63, 'learning_rate': 0.1}],
 'CAT': [{'iterations': 200, 'learning_rate': 0.1, 'depth': 6}]
}

# Strategy 2: Balanced
balanced_hyperparameters = {
 'XGB': [
 {'n_estimators': 200, 'max_depth': 6, 'learning_rate': 0.1},
 {'n_estimators': 300, 'max_depth': 8, 'learning_rate': 0.05}
 ],
 'GBM': [
 {'num_boost_round': 300, 'num_leaves': 63, 'learning_rate': 0.1},
 {'num_boost_round': 400, 'num_leaves': 127, 'learning_rate': 0.05}
 ]
}

# Strategy 3: Maximum quality
quality_hyperparameters = {
 'XGB': [
 {'n_estimators': 500, 'max_depth': 8, 'learning_rate': 0.05},
 {'n_estimators': 800, 'max_depth': 10, 'learning_rate': 0.01},
 {'n_estimators': 1000, 'max_depth': 12, 'learning_rate': 0.005}
 ],
 'GBM': [
 {'num_boost_round': 600, 'num_leaves': 127, 'learning_rate': 0.05},
 {'num_boost_round': 800, 'num_leaves': 255, 'learning_rate': 0.01},
 {'num_boost_round': 1000, 'num_leaves': 511, 'learning_rate': 0.005}
 ]
}
```

### Excluding Algorithms

```python
# Exclude certain algorithms
excluded_model_types = ['KNN', 'NN_TORCH']

predictor.fit(
 train_data,
 excluded_model_types=excluded_model_types
)
```

### Validation Configuration

```python
# Validation strategy configuration
from autogluon.tabular.models import AbstractModel

class CustomValidationStrategy(AbstractModel):
 def _get_default_resources(self):
 return {'num_cpus': 2, 'num_gpus': 0}

predictor.fit(
 train_data,
 validation_strategy='custom',
 custom_validation_strategy=CustomValidationStrategy()
)
```

## Working with Different Data Types

### 📊 Processing Different Data Types

<img src="images/optimized/advanced_topics_overView.png" alt="Data type processing" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 9: Diagram of different data type processing in AutoML Gluon*

**Why is proper data processing important?** Because data quality directly affects model quality:

- **Numerical data**: Numerical data (age, price, quantity)
- **Categorical data**: Categorical data (color, category, status)
- **Text data**: Text data (descriptions, reviews, comments)
- **DateTime data**: Temporal data (dates, time, timestamps)
- **Mixed data**: Mixed data types in one dataset
- **Missing data**: Handling missing values
- **Outliers**: Detection and handling of outliers

### Categorical Data

```python
# AutoGluon automatically detects categorical variables
# But can specify them explicitly
categorical_columns = ['category', 'brand', 'region']

predictor.fit(
 train_data,
 categorical_columns=categorical_columns
)
```

### Text Data

```python
# For text columns AutoGluon automatically creates features
text_columns = ['description', 'review_text']

predictor.fit(
 train_data,
 text_columns=text_columns
)
```

### Temporal Data

```python
# Specify temporal columns
time_columns = ['date', 'timestamp']

predictor.fit(
 train_data,
 time_columns=time_columns
)
```

## Training Monitoring

### 📈 Training Monitoring System

<img src="images/optimized/interpretability_overView.png" alt="Training monitoring" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 10: Training monitoring and interpretation system*

**Why is training monitoring important?** Because it helps control the process and identify problems:

- **Progress Tracking**: Tracking training progress
- **Performance Monitoring**: Monitoring model performance
- **Resource Usage**: Controlling resource usage (CPU, RAM, GPU)
- **Error Detection**: Detecting errors and problems
- **Quality Metrics**: Tracking quality metrics
- **Model Comparison**: Comparing different models
- **Early Stopping**: Automatic stopping when no improvements

### Logging

```python
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Training with detailed logging
predictor.fit(
 train_data,
verbosity=2 # Detailed logging
)
```

### Callback Functions

```python
def training_callback(model_name, model_path, model_info):
"""Callback function for training monitoring"""
 print(f"Training {model_name}...")
 print(f"Model path: {model_path}")
 print(f"Model info: {model_info}")

predictor.fit(
 train_data,
 callbacks=[training_callback]
)
```

## Usage Examples

### Complete Classification Example

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Create synthetic data
X, y = make_classification(
 n_samples=10000,
 n_features=20,
 n_informative=15,
 n_redundant=5,
 n_classes=2,
 random_state=42
)

# Create DataFrame
data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Split into train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Create and train predictor
predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
)

# Training
predictor.fit(
 train_data,
 time_limit=300, # 5 minutes
 presets='medium_quality'
)

# Predictions
predictions = predictor.predict(test_data)
probabilities = predictor.predict_proba(test_data)

# Quality evaluation
performance = predictor.evaluate(test_data)
print(f"Accuracy: {performance['accuracy']}")

# Leaderboard analysis
leaderboard = predictor.leaderboard()
print(leaderboard)
```

### Complete Regression Example

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

# Create synthetic data
X, y = make_regression(
 n_samples=10000,
 n_features=20,
 n_informative=15,
 noise=0.1,
 random_state=42
)

# Create DataFrame
data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Split into train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Create and train predictor
predictor = TabularPredictor(
 label='target',
 problem_type='regression',
 eval_metric='rmse'
)

# Training
predictor.fit(
 train_data,
 time_limit=300, # 5 minutes
 presets='high_quality'
)

# Predictions
predictions = predictor.predict(test_data)

# Quality evaluation
performance = predictor.evaluate(test_data)
print(f"RMSE: {performance['rmse']}")
print(f"MAE: {performance['mae']}")

# Feature importance analysis
feature_importance = predictor.feature_importance()
print(feature_importance)
```

## Best Practices

### 🎯 Usage Recommendations

<img src="images/optimized/case_studies_overView.png" alt="Best practices" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 11: Best practices and recommendations for using AutoML Gluon*

**Why are best practices important?** Because they help avoid common mistakes and achieve maximum quality:

- **Data Quality**: Ensuring data quality before training
- **Feature Engineering**: Creating informative features
- **Model Selection**: Choosing appropriate algorithms
- **Validation Strategy**: Proper validation strategy
- **Hyperparameter Tuning**: Effective parameter configuration
- **Ensemble Methods**: Using ensembles to improve quality
- **Monitoring**: Constant performance monitoring

### Data Preparation

```python
# 1. Check data quality
print("Data shape:", train_data.shape)
print("Missing values:", train_data.isnull().sum().sum())
print("Data types:", train_data.dtypes.value_counts())

# 2. Handle missing values
train_data = train_data.dropna() # or filling

# 3. Remove constant features
constant_columns = train_data.columns[train_data.nunique() <= 1]
train_data = train_data.drop(columns=constant_columns)
```

### Metric Selection

```python
# For classification
classification_metrics = [
 'accuracy', 'balanced_accuracy', 'f1', 'f1_macro', 'f1_micro',
 'precision', 'precision_macro', 'recall', 'recall_macro',
 'roc_auc', 'log_loss'
]

# For regression
regression_metrics = [
 'rmse', 'mae', 'mape', 'smape', 'r2', 'pearsonr', 'spearmanr'
]
```

### Training Time Optimization

```python
# Quick training for experiments
predictor.fit(
 train_data,
time_limit=60, # 1 minute
 presets='optimize_for_deployment'
)

# Quality training for final model
predictor.fit(
 train_data,
time_limit=3600, # 1 hour
 presets='best_quality'
)
```

## Next Steps

After mastering basic usage, proceed to:
- [Advanced Configuration](./03_advanced_configuration.md)
- [Working with Metrics](./04_metrics.md)
- [Validation Methods](./05_validation.md)
