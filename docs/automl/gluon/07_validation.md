# Calibration of models in AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who is critical

Why is 70% of the ML projects failing in sales because of bad validation? Because validation is the only way to make sure that your model really works.

### What's going on without the correct validation?
- ♪ Fake confidence ♪ ♪ The model seems good, but it's failing on new data ♪
- **retraining**: The model memorizes training data instead of learning pathers
- ** Wrong decisions**: Choose a bad model instead of a good one.
- ** Business failures**: Model not Working in real terms

### What gives you the right thing to do?
- ** Final assessment**: You know exactly how the model will behave on new data
- ** Prevention of retraining**: Model learning to generalize and not to remember
- **The right choice**: Choose the best model for the task
- **Authority in sales**: The model will really be Working

## Introduction in validation

<img src="images/optimized/validation_methods.png" alt="Methods validation" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 1: Methods appreciation in AutoML Gluon*

<img src="images/optimized/walk_forward_Analesis.png" alt="Walk-Forward Analysis" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 2: Walk-Forward validation - diagram, performance, choice of parameters*

*Why is validation not just "check model"?** It's a process that determines whether your model is ready for the real world. Imagine that you're preparing a pilot for flight - validation is a simulation that shows how it will behave in real terms.

validation is a critical process for assessing the quality of ML models and preventing re-training. In AutoML Gluon, various Methods validation for different types of tasks are available.

♪ ♪ Type of validation ♪

<img src="images/optimized/robustness_Analesis.png" alt="Tips validation" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 3: Different types of validation and their application*

**Why does AutoML Gluon offer different types of validation?** Because different tasks require different approaches. It's like different types of examinations for different subjects.

### ♪ key principles of appreciation

** Why is it important to understand the principles of validation?** Because the correct vilification is the basis of reliable ML models:

- **Holdout Planning**: Simple division on train/test (70/30)
- **Cross-Validation**: K-fold cross-evaluation for a more reliable assessment
**Time Series Split**: Special validation for time series
**Stratefied Split**: Maintaining the proportion of classes divided
**Walk-Forward Analysis**: Rolling window for time series
- **Bootstrap Planning**: Random sample with return
- **Monte Carlo Planning**: Multiple random divisions

### 1. Holdout validation

Because it's intuitively understandable: you just divide data on two parts - one for learning, the other for testing. It's like a test in school - you study on a textbook and you take a test on new tasks.

** Benefits of Goldout validation:**
- **Simple**: Easy to understand and implement
- **Speed**: Rapidly implemented
- ** Effectiveness**: Suitable for large datasets
- **Intuitivity**: It is clear to interested parties

** Deficiencies of Holdout validation:**
- ** Instability**: The result depends on from random separation
- ** Inefficiency**: 20% of data not participate in training
- ** Accident**: Bad separation can distort results

```python
from autogluon.tabular import TabularPredictor

# A simple holdout validation
predictor = TabularPredictor(label='target')
predictor.fit(
 train_data,
Holdout_frac=0.2 # 20% data for validation
)
```

**/ Detailed describe parameters Holdout validation:**

**parameter holdout_frac:**
- ** Designation**: Percentage of data allocated for validation
- **Typ**: float
- ** Value range**: `[0.0, 1.0)' (0% - 100%)
**on default**: 0.1 (10%)
- ** Recommended values**:
- ** Small datasets (< 1000 examples)**: 0.2-0.3 (20-30%)
- ** Average datasets (1000 to 10,000 examples)**: 0.15 to 0.25 (15-25 per cent)
- ** Large datasets (> 10,000 examples)**: 0.1-0.2 (10-20%)
- **Effects on learning**:
- **Big goldout_frac**: Less data for learning, but more reliable validation
- ** Less goldout_frac**: More data for learning, but less reliable validation
- ** Selection of optimal value**:
- ** Data size analysis**: Make sure the validation sample is large enough
- **Stability of results**: Check the stability of the metric on validation
- **Balance**: Enough data for training and validation
- ** Specialities**:
- ** Accidental separation**: data divided randomly
- **Stratification**: Proportion of classes retained if necessary
** Temporary data**: Time series use temporary separation

**Why 20 per cent for validation?** It's a compromise between sufficient data for learning and enough for validation.

###2. K-Fold cross-validation

<img src="images/optimized/metrics_comparison.png" alt="K-Fold cross-validation" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 4: K-Fold Cross-Validation - Scheme of Work and Benefits*

**Why is K-Fold cross-validation more reliable than Goldout?** Because it uses all data and for learning, and for satisfaction. It's like taking five exams instead of one - the result will be more accurate.

### ♪ K-Fold working principles

**Why does K-Fold produce more stable results?** Because each data point is involved in both learning and development:

- ** Full use of data**: All data are involved in training and validation
- **Statistical stability**: result n depends on from random separation
- ** variance assessment**: Model stability can be assessed
- ** Best assessment of synthesis**: Better assessment of quality on new data

** Like Worknet K-Fold Cross-Validation:**
1. ** Division on K Parts:** Data divided on K equal parts (usually K=5 or K=10)
2. **K iterations**: in each iteration one part is used for validation, the remaining K-1 for learning
3. ** Model learning**: Model learning on K-1 parts
** Test**: Model to be tested on the remaining part
5. **Averaging results**: Final evaluation - average on all K iterations

** Benefits K-Fold validation:**
- ** Use all data**: Each data point participates in both learning and in validation
- **Stability**: result n depends on from random separation
- ** variance assessment**: Shows how stable the model is
- ** Reliability**: More accurate assessment of model quality

** Shortcomings K-Fold validation:**
- **Time**: Implemented in K times longer
- **Complicity**: requires more computing resources
- ** Memory**: K models to be stored

```python
# K-fold cross-validation
predictor.fit(
 train_data,
 num_bag_folds=5, # 5-fold CV
 num_bag_sets=1
)
```

**/ Detailed describe parameters K-Fold validation:**

**parameter num_bag_folds:**
- ** Designation**: Number of Folds for Cross-Validation
- **Typ**:int
- ** Value range**: `[2, 20]' (recommended 3-10)
- **on default**: 8
- ** Recommended values**:
- ** Small datasets (< 1000 examples)**: 3-5 folds
- ** Average datasets (1000 to 10,000 examples)**: 5-7 folds
- **Big datasets (> 10,000 examples)**: 7-10 folds
- **Effects on learning**:
- **Big Folds**: A more stable rating, but more learning time
- ** Less folds**: Faster education, but less stable rating
- ** Selection of optimal value**:
- ** Data measurement**: Make sure every fold is large enough
- **Learning time**: Take into account restrictions in time
- **Stability**: More folds = more stable results
- ** Specialities**:
- **Stratification**: Proportion of classes retained if necessary
** Temporary data**: Time series use temporary separation
- ** Memory**: Needs more memory for model storage

**parameter num_bag_sets:**
- ** Designation**: Number of sets of folks for additional stability
- **Typ**:int
- ** Value range**: `[1, 10] ` (recommended 1-3)
- **on default**: 1
- ** Recommended values**:
- ** Rapid validation**: 1 set
- ** Stabilisation**: 2-3 sets
- ** Maximum stability**: 3-5 sets
- **Effects on learning**:
- **Big sets**: A more stable assessment, but much more time
- ** Less sets**: Faster learning, but less stable rating
- ** Use**:
- ** Research phase**: 1 set for rapid testing
- ** Final validation**: 2-3 sets for reliable evaluation
- ** Critical projects**: 3-5 sets for maximum stability

Because it's the best balance between accuracy and speed.

###3: Strategized validation

**Why is stratification critical for unbalanced data?** Because conventional calidization can produce distorted results when one class is in 100 times larger than the other; it's how to measure the quality of a doctor only on healthy patients.

** Unbalanced data problem:**
- **Medical diagnosis**: 99 per cent healthy, 1 per cent ill
- ** Fraud detection**: 99.9 per cent legal transactions, 0.1 per cent fraud
- **Spam filters**: 90% regular letters, 10% spam

** Like Working Stratification:**
1. ** Distribution analysis**: AutoML Gluon analyses class proportions
2. **Save ratio**: in each folda the reference distribution is maintained
3. ** Balanced assessment**: Model evaluated on representative data
4. **Correctic metrics**: Receive accurate estimates for all classes

** When to use stratification:**
- ** Use**: When classes are unbalanced (ratio > 10:1)
- ** Use**: When all classes are important (health, safety)
- **not use**: When data are balanced
- **not use**: When only majoritarian classes are important

```python
# Stylized validation for unbalanced data
predictor.fit(
 train_data,
 num_bag_folds=5,
 num_bag_sets=1,
stratehy=True # Maintain class proportions in each fold
)
```

**/ Detailed describe parameters of stabilised validation:**

**parameter stratify:**
- ** Designation**: Maintaining the proportion of classes in each fold of validation
-**Teep**: bool
- **on default**: False
- ** When to use**:
- ** Unbalanced data**: Ratio of classes > 10:1
- ** Critical classes**: When all classes are important (health, safety)
- ** Small classes**: When minority classes have < 100 examples
**comparison of models**: for fair comparison of algorithms
- ** When not used**:
- ** Balanced data**: Ratio of classes < 3:1
- ** Majoritarian classes only**: When only basic classes are important
- **Regression**: Stratification not applicable to regression tasks
- ** Impact on validation**:
- **Equitable assessment**: Each class is represented in each fold
- **Metric stability**: More stable results for minority classes
- **Correctic metrics**: Precise estimates of precision, recall, F1-score
- ** Particulars of implementation**:
- ** Automatic definition**: AutoGluon automatically determines the need for stratification
- ** Minimum size**: Each class shall have a minimum of 2 examples on bear
- ** Error processing**: Where stratification is not possible, normal vilification is used

**Why does stratification always need a note?** Because it adds complexity, but it's always necessary.
```

## Backtest validation

<img src="images/optimized/monte_carlo_Analesis.png" alt="validation of time series" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 5: time series development and backtest analysis*

**Why should the timing of time series require a special approach?** Because time data have a structure that cannot be broken:

- ** Time sequence**: data should remain in chronoLogsch order
- ** Prevention of data leakage**: Future data not should influence past predictions
- ** Realistic evaluation**: validation should simulate actual conditions of use
- ** Seasonality and trends**: Accounting for time variables in data

### Temporary validation for time series

```python
from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import numpy as np

def time_series_backtest(data, target_col, n_splits=5):
"Backtest validation for time series"

# Sorting in time
 data = data.sort_values('timestamp')

♪ Time-folds-create
 tscv = TimeSeriesSplit(n_splits=n_splits)

 results = []

 for fold, (train_idx, val_idx) in enumerate(tscv.split(data)):
 print(f"Fold {fold + 1}/{n_splits}")

# Data sharing
 train_fold = data.iloc[train_idx]
 val_fold = data.iloc[val_idx]

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_fold, time_limit=300)

# Premonition
 predictions = predictor.predict(val_fold)

# Quality assessment
 performance = predictor.evaluate(val_fold)

 results.append({
 'fold': fold + 1,
 'performance': performance,
 'predictions': predictions
 })

 return results

# Use
backtest_results = time_series_backtest(data, 'target', n_splits=5)
```

**/ Detailed describe parameters temporial validation:**

**function time_series_backtest:**
- ** Designation**: Backtest validation for time series with maintenance of time sequence
- **parameters**:
- **'data'**: time series
-** Type**: DataFrame
- **describe**: Table with provisional data
- ** Demands**: Must contain the column 'timestamp' or temporary index
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
 - **examples**: 'price', 'return', 'target'
- ** `n_splits'**: Number of temporary folds
- **Typ**:int
- ** Value range**: `[2, 20]' (recommended 3-10)
- **on default**: 5
- ** Recommended values**:
- ** Short rows (< 1,000 points)**: 3-5 folds
- ** Average rows (1000 to 10,000 points)**: 5-7 folds
- ** Long rows (> 10,000 points)**: 7-10 folds
- **Return value**: List - List of results for each fold
- **Structure of results**:
- **'fold'**: Fold number (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- ** Specialities of temporary validation**:
- ** Order preservation**: data remain in chronoLogsch order
- ** Prevention of leakage**: Future data not influence past predictions
- ** Realistic evaluation**: Simulates the actual conditions of use
- ** Seasonality**: Take into account time-frames in data

**parameter n_splits (TimeSeriesSplit):**
- ** Designation**: Number of temporary folds for validation
- **Typ**:int
- ** Value range**: `[2, 20]' (recommended 3-10)
- ** Impact on validation**:
- **Big Folds**: More detailed assessment, but less data on Fold
- ** Less fold**: More data on fold, but less detailed evaluation
- ** Selection of optimal value**:
- ** Data measurement**: Make sure every fold is large enough
- **temporary period**: Take into account seasonality and trends
- ** Computation resources**: More folds = more time of study

### Extended backtest

```python
def advanced_backtest(data, target_col, window_size=1000, step_size=100):
""The Extended Backtest with a sliding window""

 results = []
 n_samples = len(data)

 for start in range(0, n_samples - window_size, step_size):
 end = start + window_size

# Separation on train/validation
 train_data = data.iloc[start:end-100]
 val_data = data.iloc[end-100:end]

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_data, time_limit=300)

# Premonition
 predictions = predictor.predict(val_data)

# Quality assessment
 performance = predictor.evaluate(val_data)

 results.append({
 'start': start,
 'end': end,
 'performance': performance,
 'predictions': predictions
 })

 return results
```

**/ Detailed describe parameters extended backtest:**

**function advanced_backtest:**
- ** Designation**: Extended backtest with sliding window for a more detailed Analysis
- **parameters**:
- **'data'**: time series
-** Type**: DataFrame
- **describe**: Table with provisional data
- ** Requirements**: To be sorted in time
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
** `Window_size'**: Size of sliding window
- **Typ**:int
- ** Value range**: `[100, 10,000] ` (recommended 500-2000)
- **on default**: 1000
- ** Recommended values**:
- **Short rows**: 200-500 points
- **Medial rows**: 500-1000 points
- ** Long rows**: 1000-2000 points
- **'step_size'**: Step of the window
- **Typ**:int
- ** Value range**: `[10, Windows_size//2] ` (recommended 50-200)
- **on default**: 100
- ** Recommended values**:
- ** Detailed analysis**: 50-100 points
- ** Rapid analysis**: 100-200 points
- ** General analysis**: 200-500 points
- **Return value**: List - List of results for each window
- **Structure of results**:
** `start'**: Initial Index of Windows (int)
- **'end'**: Final index of windows (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- ** The benefits of sliding windows**:
- ** Detailed analysis**: More points of validation
- ** Adaptation**: The model adapts to changes in data
- **Stability**: More stable quality assessment
- **Trends**: Identification of changes in model performance

**parameter window_size:**
- ** Designation**: Size of the model training window
- ** Impact on validation**:
- **Big window**: More data for learning, but less adaptive model
Less window**: Less data for learning, but more adaptive model
- ** Selection of optimal value**:
- ** Data stability**: for stable data Use large windows
- ** Data variability**: for variable Us data, smaller windows
- ** Seasonality**: Take into account seasonal periods in data

**parameter step_size:**
- ** Designation**: Step of the window to create new points of validation
- ** Impact on validation**:
- ** Less step**: More points of validation, but more time of calculation
- **Big step**: Less points of validation but faster of calculation
- ** Selection of optimal value**:
- **detail**: for a detailed Analysis Use, smaller steps
- **Speed**: for rapid Analysis Use, big steps
- ** Cover**: Take into account the closure between windows

## Walk-Forward validation

### Basic Walk-Forward appreciation

```python
def walk_forward_validation(data, target_col, train_size=1000, test_size=100):
"""Walk-Forward validation"""

 results = []
 n_samples = len(data)

 for i in range(train_size, n_samples - test_size, test_size):
# Teaching sample
 train_data = data.iloc[i-train_size:i]

# Testsy sample
 test_data = data.iloc[i:i+test_size]

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_data, time_limit=300)

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

 results.append({
 'train_start': i-train_size,
 'train_end': i,
 'test_start': i,
 'test_end': i+test_size,
 'performance': performance,
 'predictions': predictions
 })

 return results

# Use
wf_results = walk_forward_validation(data, 'target', train_size=1000, test_size=100)
```

**/ Detailed describe of Walk-Forward parameters:**

**function walk_forward_validation:**
- ** Designation**: Walk-Forward satisfaction with fixed size of instruction and tests sample
- **parameters**:
- **'data'**: time series
-** Type**: DataFrame
- **describe**: Table with provisional data
- ** Requirements**: To be sorted in time
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
**'training_size'**: The size of the training sample
- **Typ**:int
- ** Value range**: `[100, 10,000] ` (recommended 500-2000)
- **on default**: 1000
- ** Recommended values**:
- **Short rows**: 200-500 points
- **Medial rows**: 500-1000 points
- ** Long rows**: 1000-2000 points
- ** `test_size'**: Tests sample size
- **Typ**:int
- ** Value range**: `[10, tran_size//2] ` (recommended 50-200)
- **on default**: 100
- ** Recommended values**:
- ** Detailed assessment**: 50-100 points
- ** Rapid assessment**: 100-200 points
- ** Overall assessment**: 200-500 points
- **Return value**: List - List of results for each step
- **Structure of results**:
**'training_start'**: Initial training sample index (int)
- **'training_end'**: Final training sample index (int)
- ** `test_start'**: Initial index testsy sample (int)
** `test_end'**: Final index tests sample (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- ** Benefits of Walk-Forward validation**:
- ** Reality**: Simulates actual conditions of use
- ** Adaptation**: The model adapts to changes in data
- **Stability**: More stable quality assessment
- **Trends**: Identification of changes in model performance

**parameter train_size:**
** Designation**: Size of the training sample for each iteration
- ** Impact on validation**:
- **Big size**: More data for learning but less adaptive model
- ** Less size**: Less data for learning but more adaptive model
- ** Selection of optimal value**:
- ** Data stability**: large dimensions for stable Use data
- ** Data variability**: for variable Use data, smaller dimensions
- ** Seasonality**: Take into account seasonal periods in data

**parameter test_size:**
- ** Designation**: Testsample size for each iteration
- ** Impact on validation**:
- ** Large**: A more reliable estimate, but less iteration
- ** Less size**: More iterations but less reliable rating
- ** Selection of optimal value**:
- ** Reliability**: for a reliable evaluation of Use large dimensions
- **detail**: for detailed Analysis Use smaller dimensions
- **Balance**: Take into account the balance between reliability and detail

### Adaptive Walk-Forward appreciation

```python
def adaptive_walk_forward(data, target_col, min_train_size=500, max_train_size=2000):
""Aptative Walk-Forward representation with variable window size""

 results = []
 n_samples = len(data)
 current_train_size = min_train_size

 for i in range(min_train_size, n_samples - 100, 100):
# Adaptation of the teaching sample size
 if i > n_samples // 2:
 current_train_size = min(max_train_size, current_train_size + 100)

# Teaching sample
 train_data = data.iloc[i-current_train_size:i]

# Testsy sample
 test_data = data.iloc[i:i+100]

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_data, time_limit=300)

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

 results.append({
 'train_size': current_train_size,
 'performance': performance,
 'predictions': predictions
 })

 return results
```

**/ Detailed descrie parameters of adaptive Walk-Forward validation:**

**function adaptive_walk_forward:**
- ** Designation**: Adaptive Walk-Forward validation with variable learning size
- **parameters**:
- **'data'**: time series
-** Type**: DataFrame
- **describe**: Table with provisional data
- ** Requirements**: To be sorted in time
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
**'min_training_size'**: Minimum sample size
- **Typ**:int
- ** Value range**: `[100, 1000] ` (recommended 200-500)
- **on default**: 500
- ** Recommended values**:
- **Short rows**: 100-200 points
- **Medial rows**: 200-500 points
- ** Long row**: 500-1000 points
- **'max_training_size'**: Maximum sample size
- **Typ**:int
- ** Value range**: `[min_training_size, 10,000] ` (recommended 1000-5000)
- **on default**: 2000
- ** Recommended values**:
- **Short rows**: 500-1000 points
- **Medial rows**: 1000-2000 points
- ** Long rows**: 2,000 to 5,000 points
- **Return value**: List - List of results for each step
- **Structure of results**:
**'training_size'**: Current teaching sample size (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- ** The benefits of adaptive validation**:
** Adaptation**: Window size adapts to data
- ** Effectiveness**: Uses more data on the extent to which they are stored
- **Stability**: More stable quality assessment
- ** Reality**: Simulates actual conditions of use

**parameter min_train_size:**
- ** Designation**: Minimum sample size in beginning of validation
- ** Impact on validation**:
- ** Large**: A more stable initial assessment, but less adaptive
- ** Less size**: More adaptive but less stable in the beginning
- ** Selection of optimal value**:
- **Stability**: for stable initial evaluation of the Use large size
- ** Adaptation**: for adaptive evaluation of the Use, smaller size
- **Balance**: Consider the balance between stability and adaptation

**parameter max_train_size:**
- ** Designation**: Maximum sample size at end of validation
- ** Impact on validation**:
- **Big size**: More stable final evaluation, but more learning time
- ** Less size**: Faster learning but less stable final evaluation
- ** Selection of optimal value**:
- **Stability**: For a stable final evaluation of Use large dimensions
- **Speed**: for rapid learning of Use, smaller
- ** Resources**: Please consider available computing resources

## Monte Carlo validation

### Basic Monte Carlo

```python
def monte_carlo_validation(data, target_col, n_iterations=100, train_frac=0.8):
"Monte Carlo falseisation with random data separation."

 results = []

 for iteration in range(n_iterations):
# Random data separation
 train_data = data.sample(frac=train_frac, random_state=iteration)
 test_data = data.drop(train_data.index)

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_data, time_limit=300)

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

 results.append({
 'iteration': iteration,
 'performance': performance,
 'predictions': predictions
 })

 return results

# Use
mc_results = monte_carlo_validation(data, 'target', n_iterations=100)
```

** Detailed describe parameters Monte Carlo validation:**

**function monte_carlo_validation:**
- ** Designation**: Monte Carlo representation with multiple random data divides
- **parameters**:
- **`data`**: data for validation
-** Type**: DataFrame
- **describe**: Table with data for validation
** Requirements**: Must contain a target variable
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
- ** `n_eaters'**: Number of iterations validation
- **Typ**:int
- ** Value range**: ` [10, 1000] ` (recommended 50-200)
- **on default**: 100
- ** Recommended values**:
- ** Rapid recovery**: 20-50 iterations
- ** Standard valuation**: 50-100 iterations
- **Footening**: 100-200 iterations
**'training_frac'**: Percentage of data for training
- **Typ**: float
- ** Value range**: `[0.5, 0.9] ` (recommended 0.7-0.8)
- **on default**: 0.8
- ** Recommended values**:
- **Lowered dataset**: 0.7-0.8 (70-80 per cent)
- **Medical dataset**: 0.8-0.85 (80-85 per cent)
- **Big dataset**: 0.85-0.9 (85-90 per cent)
- **Return value**: List - List of results for each iteration
- **Structure of results**:
- ** `acteration'**: Iteration number (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- ** Benefits of Monte Carlo validation**:
- **Statistical reliability**: Multiple random divisions
- ** variance assessment**: Shows model stability
- ** Confidence**: Better quality assessment
- ** Robinity**: Resistance to accidental fluctuations

**parameter n_iterations:**
- ** Designation**: Number of iterations for Monte Carlo validation
- ** Impact on validation**:
- ** More iteration**: A more reliable estimate, but more time
- ** Less iteration**: Faster appreciation but less reliable evaluation
- ** Selection of optimal value**:
- **Statistical significance**: For significant results of Use 100+ iterations
- **Time**: for rapid recovery Use 20-50 iterations
- ** Resources**: Please consider available computing resources

**parameter train_frac:**
- ** Designation**: Percentage of data for learning in each iteration
- ** Impact on validation**:
- **Big share**: More data for learning but less for testing
- ** Less**: Less data for learning but more for testing
- ** Selection of optimal value**:
- ** Data measurement**: Make sure the test sample is large enough
- **Stability**: For a stable evaluation of Use 0.8-0.85
- **Balance**: Take into account the balance between learning and testing

### Bootstrap validation

```python
def bootstrap_validation(data, target_col, n_bootstrap=100):
"""Bootstrap validation"""

 results = []
 n_samples = len(data)

 for i in range(n_bootstrap):
# Bootstrap sample
 bootstrap_indices = np.random.choice(n_samples, size=n_samples, replace=True)
 bootstrap_data = data.iloc[bootstrap_indices]

# Out-of-bag sample
 oob_indices = np.setdiff1d(np.arange(n_samples), np.unique(bootstrap_indices))
 oob_data = data.iloc[oob_indices]

 if len(oob_data) == 0:
 continue

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(bootstrap_data, time_limit=300)

# Data forecasts on OOB
 predictions = predictor.predict(oob_data)

# Quality assessment
 performance = predictor.evaluate(oob_data)

 results.append({
 'bootstrap': i,
 'performance': performance,
 'predictions': predictions
 })

 return results
```

**/ Detailed describe of Bootstrap parameters:**

**function bootstrap_validation:**
- ** Designation**: Bootstrap satisfaction with random sample with return
- **parameters**:
- **`data`**: data for validation
-** Type**: DataFrame
- **describe**: Table with data for validation
** Requirements**: Must contain a target variable
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
- ** `n_bootstrap'**: Quantity of bootstrap iterations
- **Typ**:int
- ** Value range**: ` [10, 1000] ` (recommended 50-200)
- **on default**: 100
- ** Recommended values**:
- ** Rapid recovery**: 20-50 iterations
- ** Standard valuation**: 50-100 iterations
- **Footening**: 100-200 iterations
- **Return value**: List - List of results for each Bootstrap iteration
- **Structure of results**:
- **'bootstrap'**: Bootstrap number iteration (int)
**/ `Performance'**: Vocabulary with quality metrics (dict)
- **'predications'**: Model fortunes (array)
- **Bootstrap features:**
- **A random sample with return**: Each bootstrap sample is created randomly
- **Out-of-bag evaluation**: Model tested on data not involved in training
- **Statistical reliability**: Shows model stability
- ** variance assessment**: Allows assessment of uncertainty of preferences

**parameter n_bootstrap:**
- ** Designation**: Number of Bootstrap iterations for validation
- ** Impact on validation**:
- ** More iteration**: A more reliable estimate, but more time
- ** Less iteration**: Faster appreciation but less reliable evaluation
- ** Selection of optimal value**:
- **Statistical significance**: For significant results of Use 100+ iterations
- **Time**: for rapid recovery Use 20-50 iterations
- ** Resources**: Please consider available computing resources
- **Bootstrap features**:
- ** Accident**: Each iteration uses random sampling
- ** Cover**: Some data may be involved in several iterations
- **Out-of-bag**: data not in bootstrap sample used for testing

♪ ♪ Combined validation ♪

### Ensemble validation

```python
def ensemble_validation(data, target_col, validation_methods=['holdout', 'kfold', 'monte_carlo']):
"Compiled validation with several methods."

 results = {}

# Holdout validation
 if 'holdout' in validation_methods:
 predictor = TabularPredictor(label=target_col)
 predictor.fit(data, holdout_frac=0.2)
 results['holdout'] = predictor.evaluate(data)

# K-fold validation
 if 'kfold' in validation_methods:
 predictor = TabularPredictor(label=target_col)
 predictor.fit(data, num_bag_folds=5, num_bag_sets=1)
 results['kfold'] = predictor.evaluate(data)

# Monte Carlo validation
 if 'monte_carlo' in validation_methods:
 mc_results = monte_carlo_validation(data, target_col, n_iterations=50)
 results['monte_carlo'] = mc_results

 return results
```

## financial disclosure

### Financial appreciation

```python
def financial_validation(data, target_col, lookback_window=252, forward_window=21):
"Specialized appreciation for financial data"

 results = []
 n_samples = len(data)

 for i in range(lookback_window, n_samples - forward_window, forward_window):
# Learning sample (lookback_wind days)
 train_data = data.iloc[i-lookback_window:i]

# Testsample (forward_window days)
 test_data = data.iloc[i:i+forward_window]

# Model learning
 predictor = TabularPredictor(label=target_col)
 predictor.fit(train_data, time_limit=300)

# Premonition
 predictions = predictor.predict(test_data)

# Financial metrics
 returns = test_data[target_col].pct_change().dropna()
 predicted_returns = predictions.pct_change().dropna()

 # Sharpe Ratio
 sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)

 # Maximum Drawdown
 cumulative_returns = (1 + returns).cumprod()
 peak = cumulative_returns.expanding().max()
 drawdown = (cumulative_returns - peak) / peak
 max_drawdown = drawdown.min()

 results.append({
 'start_date': test_data.index[0],
 'end_date': test_data.index[-1],
 'sharpe_ratio': sharpe_ratio,
 'max_drawdown': max_drawdown,
 'predictions': predictions
 })

 return results
```

## Analysis of results of validation

### Statistical analysis

```python
def analyze_validation_results(results):
"Analysis of the results of validation."

# The extraction of metrics
 metrics = []
 for result in results:
 if 'performance' in result:
 metrics.append(result['performance'])

# Statistical analysis
 Analysis = {}

 for metric in metrics[0].keys():
 values = [m[metric] for m in metrics]
 Analysis[metric] = {
 'mean': np.mean(values),
 'std': np.std(values),
 'min': np.min(values),
 'max': np.max(values),
 'median': np.median(values),
 'q25': np.percentile(values, 25),
 'q75': np.percentile(values, 75)
 }

 return Analysis

# Use
Analysis = analyze_validation_results(backtest_results)
print("Validation Analysis:")
for metric, stats in Analysis.items():
 print(f"{metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")
```

**/ Detailed describe parameters Analysis of validation results:**

**function analyze_validation_results:**
- ** Designation**: Statistical analysis of results of validation
- **parameters**:
- **/ `Results'**: Results of validation
- ** Type**: List
- **describe**: List of results
- **Structure**: Each element must contain 'performance' with metrics
- **Return value**: dict - statistical analysis dictionary
- **Structure Analysis**:
- **'mean'**: Average metrics (float)
- **'std'**: Standard deviation metrics (float)
- **'min'**: Minimum value of metrics (float)
- ** `max'**: Maximum value of metrics (float)
- **'median'**: Median metrics (float)
- **'q25'**: 25th percentile metrics (float)
- ** `q75'**: 75th percentile metrics (float)
- ** Use**:
- ** Stability assessment**: Meteric dispersion analysis
- **comparison of methods**: comparison of different methods of validation
- ** Identification of problems**: Search for abnormal values
- **Reportability**: quality review reports

**Statistics:**
- ** `mean'**: Average metrics
** Interpretation**: Central model quality trend
- ** Use**: Basic quality assessment
- **'std'**: Standard deviation metrics
** Interpretation**: model stability
- ** Use**: Evaluation of model reliability
- ** `min'/ `max'**: Minimum/maximum value
** Interpretation**: Model quality range
- ** Use**: Assessment of extreme values
- **'median'**: Median metrics
** Interpretation**: Sustainable quality assessment
- ** Use**: Alternative to average
- ** `q25'/ `q75'**: 25th/75th percentile
** Interpretation**: model quality distribution
- ** Use**: Assessment of the variation of values

### Visualization of results

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_validation_results(results, metric='accuracy'):
"""""""""""""""""""""""""""""""""""""Visualization of results of validation"""""""

# The extraction of metrics
 values = []
 for result in results:
 if 'performance' in result and metric in result['performance']:
 values.append(result['performance'][metric])

# Graph
 plt.figure(figsize=(12, 8))

# temporary row metrics
 plt.subplot(2, 2, 1)
 plt.plot(values)
 plt.title(f'{metric} over time')
 plt.xlabel('Fold/Iteration')
 plt.ylabel(metric)

# Distribution of metrics
 plt.subplot(2, 2, 2)
 plt.hist(values, bins=20, alpha=0.7)
 plt.title(f'Distribution of {metric}')
 plt.xlabel(metric)
 plt.ylabel('Frequency')

 # Box plot
 plt.subplot(2, 2, 3)
 plt.boxplot(values)
 plt.title(f'Box plot of {metric}')
 plt.ylabel(metric)

# Statistics
 plt.subplot(2, 2, 4)
 stats_text = f"""
 Mean: {np.mean(values):.4f}
 Std: {np.std(values):.4f}
 Min: {np.min(values):.4f}
 Max: {np.max(values):.4f}
 """
 plt.text(0.1, 0.5, stats_text, transform=plt.gca().transAxes, fontsize=12)
 plt.axis('off')

 plt.tight_layout()
 plt.show()

# Use
plot_validation_results(backtest_results, metric='accuracy')
```

** Detailed descrie parameters for visualization of validation results:**

**function plot_validation_results:**
- ** Designation**: Visualization of performance with different types of graphs
- **parameters**:
- **/ `Results'**: Results of validation
- ** Type**: List
- **describe**: List of results
- **Structure**: Each element must contain 'performance' with metrics
- ** `metric'**: Name of devices for visualization
- **Typ**: str
- **describe**: Name of display metrics
 - **examples**: 'accuracy', 'f1', 'roc_auc', 'rmse', 'mae'
- **on default**: 'accuracy'
- **Return value**: None (shows graph)
- ** Graphic charts**:
- **temporary row**: Shows change in metrics in time
** Histogram**: Shows distribution of metrics
- **Box Platform**: Shows metrics statistics (media, quarts, emissions)
- **Statisticians**: Textual presentation of key statisticians
- ** Use**:
- ** Trends Analysis**: Identification of changes in model quality
- ** Stability assessment**: Analysis of the dispersion of metrics values
- ** Emission identification**: Search for abnormal values
- **Reportability**: review of visual reports

**parameter metric:**
- ** Designation**: Choice of devices for visualization
- ** Accessible metrics**:
- ** Classification**: 'accuracy', 'f1', 'precision', 'recall', 'roc_auc'
== sync, corrected by elderman == @elder_man
- **Castom**: Any metrics present in the results
- ** Selection of optimum metrics**:
- ** Basic metric**: Use main metric of wallidation
- **comparison**: For comparison Use are the same metrics
- **Analysis**: Choose metrics important for your task

## Practical examples

### Full example validation

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# data quality
X, y = make_classification(
 n_samples=10000,
 n_features=20,
 n_informative=15,
 n_redundant=5,
 n_classes=2,
 random_state=42
)

data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# add temporary tags
data['timestamp'] = pd.date_range('2020-01-01', periods=len(data), freq='D')
data = data.set_index('timestamp')

# Various Methods appreciation
print("=== Holdout Validation ===")
predictor_holdout = TabularPredictor(label='target')
predictor_holdout.fit(data, holdout_frac=0.2, time_limit=300)
holdout_performance = predictor_holdout.evaluate(data)
print(f"Holdout Performance: {holdout_performance}")

print("\n=== K-Fold Validation ===")
predictor_kfold = TabularPredictor(label='target')
predictor_kfold.fit(data, num_bag_folds=5, num_bag_sets=1, time_limit=300)
kfold_performance = predictor_kfold.evaluate(data)
print(f"K-Fold Performance: {kfold_performance}")

print("\n=== Time Series Backtest ===")
backtest_results = time_series_backtest(data, 'target', n_splits=5)
backtest_Analysis = analyze_validation_results(backtest_results)
print(f"Backtest Analysis: {backtest_Analysis}")

print("\n=== Monte Carlo Validation ===")
mc_results = monte_carlo_validation(data, 'target', n_iterations=50)
mc_Analysis = analyze_validation_results(mc_results)
print(f"Monte Carlo Analysis: {mc_Analysis}")

# Visualization of results
plot_validation_results(backtest_results, metric='accuracy')
```

## Best practices of vilification

<img src="images/optimized/advanced_topics_overView.png" alt="Best practices of recovery" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 6: Best practices and recommendations on validation*

# Why are best practices of validation important? # 'Cause the right thing to do is the foundation of reliable ML models:

- ** Selection of method of validation**: Correct method for data type and task
- ** Unbalanced data processing**: Special equipment for uneven classes
- **validation ensemble**: Features of calidization of complex models
- **Monitoring validation**: Quality tracking in learning
- ** Interpretation of results**: Correct understanding of metric validation
- ** Avoiding errors**: Typical errors and ways to prevent them

### Choice of the method of validation

```python
def choose_validation_method(data_type, problem_type, data_size):
"Selection of the best method of validation""

 if data_type == 'time_series':
 return 'time_series_backtest'
 elif data_size < 1000:
 return 'kfold'
 elif data_size < 10000:
 return 'holdout'
 else:
 return 'monte_carlo'
```

## configurization parameters halidation

```python
def optimize_validation_params(data, target_col):
"Optimization of Validation Parameters"

# Determination of the optimum number of folds
 n_samples = len(data)
 if n_samples < 100:
 n_folds = 3
 elif n_samples < 1000:
 n_folds = 5
 else:
 n_folds = 10

# The definition of the size of the goldout
 if n_samples < 1000:
 holdout_frac = 0.3
 else:
 holdout_frac = 0.2

 return {
 'n_folds': n_folds,
 'holdout_frac': holdout_frac,
 'n_monte_carlo': min(100, n_samples // 10)
 }
```

## Overcoming problems of validation

<img src="images/optimized/Troubleshooting_flowchart.png" alt="Valification problems" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 7: Problem-solving diagram*

** Why is it important to know how to solve problems of validation?** Because validation is a complex process, and problems arise often:

- **retraining**: The model memorizes training data
- ** Lack of education**: too easy for data
- ** Unstable results**: Large dispersion between folds
- ** Data leak (data Leakage)**: Future data influence past predictions
- ** Wrong choice of metric**: metrics not match business objectives
- **Issues with data**: Qualitative or unbalanced data

### ♪ Typical problems and solutions

# Why are there problems of validation? # 'Cause validation is a complex process with lots of underwater stones:

- **Problem**: Retraining ♪ ** Decision**: Regularization, more data, easier model
- **Challenge**: Lack of education ♪** Decision**: More complex model, more signs, more data
- **Problem**: Instability ♪ ** Decision**: More folds, stratification, more data
- **The problem**: Data leak * ***: Correct separation, temporary validation
- **Challenge**: Wrong metrics * ** Decision**: Selecting a metric on business objectives

## Next steps

Once applied, go to:
- [Selled by default](./06_production.md)
- [model re-training](./07_retraining.md)
- [best practice](.08_best_practices.md)
