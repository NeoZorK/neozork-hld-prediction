# Troubleshooting AutoML Gluon

**Author:** Shcherbyna Rostyslav
**Date:** 2024

# Whoy Troubleshooting is critical

Because machine learning is a complex system where multiple components have to work together. It's like a diagnostic of a car -- you need to know where to find the problem.

### Catastrophic Consequences of Unsolved Problems
- ** Loss of time**: Days on simple problems
- **Team Frustration**: Developers drop project
- ** Bad results**: Working models are inefficient
- ** Losing trust**: Buyers lose faith in ML

♪## The benefits of system-based Troubleshooting
- ** Rapid solution**: Knowledge of typical problems and their solutions
- **Prevention**: Prevention of problems to be encountered
- ** Performance**: More time on development, less time on debugging
- **Confidence**: Team knows how to solve problems

## Introduction in Troubleshooting

<img src="images/optimized/Troubleshooting_flowchart.png" alt="Traubleshooting Style"="max-width: 100%; height: auto; Display: block; marguin: 20px auto;">
*Picture 16.1: AutoML Gluon, a systematic approach to diagnosis and solution*

Why is Troubleshooting an art and no science?

** Key principles of Troubleshooting:**
**Systhematic approach**: Step-by-step diagnostics of problems
- ** Documentation**: Recording all problems and solutions
- **Texting**: check the effectiveness of decisions
- **Prevention**: Prevention of recurring problems
- ** Team training**: Transfer of knowledge and experience

**Tips of problems in AutoML Gloon:**
- ** Problems in installation**: Conflicts dependencies, Python versions
- ** Data problems**: Formats, dimensions, quality
- **Performance problems**: Slow Working, memory deficit
- ** Model problems**: Poor accuracy, retraining

In this section, look at the typical problems encountered in the work of the AutoML Gluon and how to solve them. Each problem includes descrie, causes and step-by-step interventions on elimination.

## Problems of installation

<img src="images/optimized/installation_issues.png" alt="Problems of installation" style"="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 16.2: Diagnostics and solutions to problems of installation AutoML Gluon - types of problems and solutions*

Why are problems of installation the most frequent in ML?

**Tips of problems of installation:**
- **Dependency Conflicts**: Conflict with package versions
- **Python Version Issues**: Wrong Python version
- **CUDA Problems**: Issues with GPU support
- **Memorial Issues**: Lack of memory in installation
- **Permission Problems**: Lack of access rights
- **Virtual Environment Issues**: Issues with virtual environments

** Key aspects of problems of integration:**
- ** Conflicts dependencies**: Incompatible versions of packages
- **Issues with Python**: Wrong Python version
- **Issues with pip/conda**: Package managers conflicts
- **Issues with system libraries**: Missing systems dependencies
- **Issues with virtual environments**: Wrong configuring environment
- **Issues with access rights**: Insufficient rights to install

♪##1 ♪ Dependencies mistakes ♪

Because different libraries require different versions of the same packages, it's like trying to use details from different car models.

#### Problem: Conflict with package versions
```bash
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed.
This behaviour is the source of the following dependency conflicts.
```

Because the pip is trying to install packages that are conflicting with each other, it's like trying to set up simultaneous Windows and Linux.

**Decision:**
```bash
# a new environment - isolation from other projects
conda create -n autogluon python=3.9
conda activate autogluon

# in the right order - first basic, then specific
pip install --upgrade pip
pip install autogluon

# or installation of specific versions - fix compatible versions
pip install autogluon==0.8.2
pip install torch==1.13.1
pip install torchvision==0.14.1
```

** Detailed descriptions of conflict resolution parameters:**

- **'conda creation -n autogluon python=3.9'**: creation of an isolated environment
- `-n autogluon': Name of environment (may be any)
- `python= 3.9': Python version (3.8-3.11 supported)
- Benefits: total isolation from system packages

- **'conda activate autogluon'**: Activation of environment
- Activating the created environment.
- Isolating the installed bags
- Prevents conflicts with other projects

- **`pip install --upgrade pip`**: update pip
- Sets the last version of the pip.
- Improves dependencies resolution.
- Recommended before installation of packages

- **`pip install autogluon`**: installation AutoGluon
- Sets the last stable version.
- Automatically allows dependencies.
- It could take 5-15 minutes.

- **'pip install autogluon==0.8.2'**: installation of a particular version
`0.8.2': Stable version (recommended)
`0.8.1': Previous version
- `0.9.0': Beta version (not recommended for sale)

- **`pip install torch==1.13.1`**: installation PyTorch
- `1.13.1': Combinable version with AutoGluon
`1.12.1': Previous stable version
`1.14.0': New version (may be incompatible)

- **`pip install torchvision==0.14.1`**: installation TorchVision
- `0.14.1': Combinable version with PyTorch 1.13.1
`0.13.1': Previous version
`0.15.0': New version (may be incompatible)

#### Problem: CUDA errors
```bash
RuntimeError: CUDA out of memory
```

**Decision:**
```python
# check CUDA
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA Version: {torch.version.cuda}")

# installation compatible version of PyTorch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117

# or shut down CUDA
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

** Detailed descriptions of CUDA problem management parameters:**

- **'torch.cuda.is_available()'**: check accessibility CUDA
- `True': CUDA is available and Worknet
- `False': CUDA not available or not installed
- False causes: incorrect installation, incompatible version

- **'torch.version.cuda'**: CUDA version
`11.7': CUDA 11.7 (recommended)
`11.6': CUDA 11.6 (supported)
- `12.0': CUDA 12.0 (may be incompatible)

- **`pip install torch==1.13.1+cu117`**: installation PyTorch with CUDA
`1.13.1': PyTorch version
- `+cu117': CUDA version (11.7)
- `--extra-index-url': Additional index packages

- **`torchvision==0.14.1+cu117`**: installation TorchVision with CUDA
- `0.14.1': TorchVision version
- `+cu117': CUDA version (11.7)
- Should match the PyTorch version.

- **'os.environ['CUDA_VISIBLE_DEVICES'] = `'**: CUDA Disablement
- `': An empty line shuts down all GPU
- `'0'': Use only GPU 0
- `'0.1'': Use GPU 0 and 1
Application: with GPU memory problems

###2.Issues with memory

#### Problem: Out of memory
```bash
MemoryError: Unable to allocate array
```

**Decision:**
```python
# Restricting the use of memory
import autogluon as ag
ag.set_config({'memory_limit': 4}) # 4GB

# Or via variable environments
import os
os.environ['AUTOGLUON_MEMORY_LIMIT'] = '4'

# Decreased data
train_data = tran_data.sample(frac=0.5) # Use 50% of data
```

** Detailed descriptions of how to solve problems with memory:**

- **'ag.set_config({'memory_limit': 4})'**: AutoGluon memory limitation
- `4': Memory Limited in GB (recommended 4-8 GB)
`2': Minimum limit for small data
`8': Maximum limit for big data
- `16+': for very big data

- **'os.environment['AUTOGLUON_MEMORY_LIMIT'] = `4'**: integration through variable environments
- `'4'': Memory Limited in GB (string)
- `'2'': Minimum limit
`'8': Maximum limit
- Benefits: global conference for all processes

- **'train_data.sample(frac=0.5)'**: Reduction in data size
`0.5': Use 50% of data (recommended)
`0.3': Use 30% of data (for very large datasets)
`0.7': Use 70 per cent of the data (compromise between quality and memory)
`0.1': Use 10% of the data (only for testing)

** Additional items of memory optimization:**

- **'ag.set_config({'num_cpus': 2})'**: CPU restriction
- `2': Use 2 CPUs
- `4': Use 4 CPU kernels (recommended)
- `8': Use 8 CPU kernels (for powerful systems)

- **'ag.set_config({'time_limit':300}) `**: Limiting time of study
`300': 5 minutes (for rapid testing)
`600': 10 minutes (standard time)
`1800': 30 minutes (for quality models)

## Learning problems

<img src="images/optimized/training_issues.png" alt="Learning problems" style="max-width: 100%; exercise: auto; display: block; marguin: 20px auto;">
*Picture 16.3: Diagnostics and solutions to the learning problems of AutoML Gloon - types of problems and methods of solutions*

# Why are learning problems so critical? # 'Cause they're influence quality and speed:

**Tips of learning problems:**
- **Slow Training**: Slow model learning
- **Pooor Model Quality**: Low model quality
- **Validation Errors**: Mistakes of appreciation
**data Quality Issues**: Issues with data quality
- **Resource Shortage**: Lack of computing resources
- **Configuring Procedures**: Issues with configuration

** Key aspects of learning problems:**
- **Sized training**: Neoptimal Settings, lack of resources
- ** Bad model quality**: Wrong data, retraining
- ** Mistakes of validation**: Wrong division of data
- **Issues with data**: Qualitative or inappropriate data
- **Issues with resources**: memory deficit, CPU, GPU
- **Issues with configuration**: Wrong learning options

*## 1. Slow learning

#### Problem: Learning takes too long
```python
# Diagnostics
import time
start_time = time.time()

# Learning with Monitoring
standard.fit(training_data,time_limit=300) # 5 minutes for test

print(f"Training time: {time.time() - start_time:.2f} seconds")
```

**Decision:**
```python
# Optimization of parameters
predictor.fit(
 train_data,
"Presets"='optimize_for_development', #rapid learning
 time_limit=600, # 10 minutes
num_bag_folds=3, # Less folds
 num_bag_sets=1,
 ag_args_fit={
'num_cpus': 2, #CPU limit
'Memory_limit': 4 #Restriction of memory
 }
)
```

** Detailed descriptions of learning optimization parameters:**

- **'presets='optimise_for_development'**: Preface for rapid learning
`'optimize_for_development': Rapid learning (recommended)
- `best_quality': Maximum quality (slow)
- `'mediam_quality_faster_training': Quality and speed compromise
- `'fast': Very rapid learning (low quality)

- **'time_limit=600'**: Limiting time of study
`600': 10 minutes (standard time)
`300': 5 minutes (rapid testing)
`1800': 30 minutes (quality models)
`3600': 1 hour (maximum quality)

- **'num_bag_folds=3'**: Number of folds for bugging
`3': Rapid learning (recommended for optimization)
`5': Standard value
`10': High quality (slow)
`1': Minimum value (very fast)

- **'num_bag_sects=1'**: Number of model sets
- `1': One set (rapid learning)
- `2': Two sets (standard)
- `3': Three sets (high quality)
- `5': Five sets (maximum quality)

- **'ag_args_fit={'num_cpus': 2}'**: Additional teaching arguments
- `'num_cpus': 2': Use 2 CPU core
- `'num_cpus': 4': Use 4 CPU kernels (recommended)
- `'num_cpus': 8': Use 8 CPU kernels (for powerful systems)

- **'ag_args_fit={'memory_limit': 4} `**: Memory limitation
== sync, corrected by elderman == @elder_man
- `'memory_limit': 8': 8': 8 GB memory (recommended)
- `'memory_limit': 16': 16 GB memory (for big data)

♪##2 ♪ Bad model quality

#### Problem: Low model accuracy
```python
# Data quality diagnostics
def diagnose_data_quality(data):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""" """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 print("data shape:", data.shape)
 print("Missing values:", data.isnull().sum().sum())
 print("data types:", data.dtypes.value_counts())

# Check target variable
 if 'target' in data.columns:
 print("Target distribution:")
 print(data['target'].value_counts())

# Check on the imbalance
 target_counts = data['target'].value_counts()
 imbalance_ratio = target_counts.max() / target_counts.min()
 print(f"Imbalance ratio: {imbalance_ratio:.2f}")

 if imbalance_ratio > 10:
 print("WARNING: Severe class imbalance detected")

 return data
```

** Detailed descriptions of data quality diagnostics:**

- **'data.chape'**: Dimensions of the dataset
- `(1000, 10)': 1000 rows, 10 columns (small dataset)
- `(1000, 50)': 10,000 rows, 50 columns (average dateset)
- `(100,000, 100)': 100,000 lines, 100 columns (big dateset)
- Application: estimation of data for training

- **'data.isnull().sum().sum()'**: Total missing values
- `0': No missing values (ideal)
`100': 100 missing values (acceptable)
- `1000+': Many missing values (needs processing)
- `> 10%': Critical level of missing values

- **'data.dtypes.value_counts()'**: Distribution of data types
- `int64': Target data
- `float64': Material data
- `obproject': Static/category data
- `datetime64': Temporary data

- **'target_counts'**: Distribution of target variable
- `{0: 800, 1:200} `: Disbalance 4:1 (acceptable)
- `\\\\\\\\\\\\\\\\\\\\\\\$900,100}} `: Disparity 9:1 (to be considered)
- `\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\:950, 1:50}}=: Disparity 19:1 (critical)

- **'imbalance_ratio'**: Class imbalance factor
`1.0': Perfect balance (1:1)
- `2.0': Easy imbalance (2:1)
- `5.0': Moderate imbalance (5:1)
- `10.0+': Strong imbalance (10:1+)

# Use
diagnose_data_quality(train_data)
```

**Decision:**
```python
# Improve data quality
def improve_data_quality(data):
"""""""""""

# Processing missing values
 data = data.fillna(data.median())

# Emissions treatment
 numeric_columns = data.select_dtypes(include=[np.number]).columns
 for col in numeric_columns:
 if col != 'target':
 Q1 = data[col].quantile(0.25)
 Q3 = data[col].quantile(0.75)
 IQR = Q3 - Q1
 data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
 data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])

# new signs
 if 'feature1' in data.columns and 'feature2' in data.columns:
 data['feature_interaction'] = data['feature1'] * data['feature2']
 data['feature_ratio'] = data['feature1'] / (data['feature2'] + 1e-8)

 return data

# Use
train_data_improved = improve_data_quality(train_data)
```

♪## 3. ♪ Mistakes ♪

♪ ### Problem: Errors in calidization ♪
```python
# Diagnostics of falseisation
def diagnose_validation_issues(predictor, test_data):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""","""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 try:
# sheck data compatibility
 print("Test data shape:", test_data.shape)
 print("Test data columns:", test_data.columns.toList())

# Check data types
 print("data types:")
 print(test_data.dtypes)

# sheck missing values
 print("Missing values:")
 print(test_data.isnull().sum())

# Trying to predict
 predictions = predictor.predict(test_data)
 print("predictions shape:", predictions.shape)

 return True

 except Exception as e:
 print(f"Validation error: {e}")
 return False

# Use
if not diagnose_validation_issues(predictor, test_data):
 print("Validation issues detected")
```

**Decision:**
```python
# Fix problems of validation
def fix_validation_issues(test_data):
""fix problems of validation""

# Processing missing values
 test_data = test_data.fillna(test_data.median())

# Data Modeling
 for col in test_data.columns:
 if test_data[col].dtype == 'object':
# Attempted conversion in numerical type
 try:
 test_data[col] = pd.to_numeric(test_data[col])
 except:
# If no succeeds, let's leave it as it is
 pass

# Remove constant columns
 constant_columns = test_data.columns[test_data.nunique() <= 1]
 test_data = test_data.drop(columns=constant_columns)

 return test_data

# Use
test_data_fixed = fix_validation_issues(test_data)
```

## Problems of prevention

<img src="images/optimized/Predication_issues.png" alt="Predictions problems" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 16.4: Diagnostics and resolution of problems of preferences AutoML Gloon - types of errors and methhods corrections*

**Tips of problems of preferences:**
- **Predication Errors**: Errors in the execution of preferences
- **Unstable measures**: Unstable results
- **Slow preferences**: Slow predictions
- **Wrong Format**: Wrong data format
- **Missing Features**: Missing
- **data Type Mismatch**: Inconformance of data types

♪##1 ♪ Mistakes of preferences ♪

♪ ### Problem: Errors in the prediction
```python
# Diagnostics of preferences
def diagnose_Prediction_issues(predictor, data):
""""""""""""""""""""""""""""""

 try:
# Check input data
 print("Input data shape:", data.shape)
 print("Input data types:", data.dtypes)

# check compatibility with the model
 model_features = predictor.feature_importance().index.toList()
 data_features = data.columns.toList()

 Missing_features = set(model_features) - set(data_features)
 extra_features = set(data_features) - set(model_features)

 if Missing_features:
 print(f"Missing features: {Missing_features}")
 if extra_features:
 print(f"Extra features: {extra_features}")

# Trying to predict
 predictions = predictor.predict(data)
 print("predictions successful")

 return True

 except Exception as e:
 print(f"Prediction error: {e}")
 return False

# Use
if not diagnose_Prediction_issues(predictor, new_data):
 print("Prediction issues detected")
```

**Decision:**
```python
# Fix problems of selections
def fix_Prediction_issues(predictor, data):
""fix problems preventions""

# Obtaining expected signs
 expected_features = predictor.feature_importance().index.toList()

# add missing signs
 for feature in expected_features:
 if feature not in data.columns:
Data[feature] = 0 # Filling with zeros

# Remove extra signs
 data = data[expected_features]

# Processing missing values
 data = data.fillna(0)

 return data

# Use
new_data_fixed = fix_Prediction_issues(predictor, new_data)
predictions = predictor.predict(new_data_fixed)
```

###2 # Unstable predictions #

#### Problem: Unstable results
```python
# Diagnostics of stability
def diagnose_Prediction_stability(predictor, data, n_tests=5):
""""""""""""""""""""""""

 predictions = []

 for i in range(n_tests):
 pred = predictor.predict(data)
 predictions.append(pred)

# Check coherence
 predictions_array = np.array(predictions)
 consistency = np.mean(predictions_array == predictions_array[0])

 print(f"Prediction consistency: {consistency:.4f}")

 if consistency < 0.95:
 print("WARNING: Unstable predictions detected")

 return consistency

# Use
consistency = diagnose_Prediction_stability(predictor, test_data)
```

**Decision:**
```python
# Stabilization of preferences
def stabilize_predictions(predictor, data, n_samples=3):
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""."""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 predictions = []

 for _ in range(n_samples):
# add a little noise for stabilization
 noisy_data = data.copy()
 for col in noisy_data.columns:
 if noisy_data[col].dtype in [np.float64, np.int64]:
 noise = np.random.normal(0, 0.01, len(noisy_data))
 noisy_data[col] += noise

 pred = predictor.predict(noisy_data)
 predictions.append(pred)

# Average preferences
 if predictor.problem_type == 'regression':
 stable_predictions = np.mean(predictions, axis=0)
 else:
# for classification - voting
 stable_predictions = []
 for i in range(len(predictions[0])):
 votes = [pred[i] for pred in predictions]
 stable_predictions.append(max(set(votes), key=votes.count))

 return stable_predictions

# Use
stable_predictions = stabilize_predictions(predictor, test_data)
```

## Problems of performance

<img src="images/optimized/performance_issues.png" alt="Performance problems" style="max-width: 100 per cent; lead: auto; display: lock; marguin: 20px auto;">
*Picture 16.5: Diagnostics and solutions to problems of performance AutoML Gluon - metrics and optimization*

Why are the problems of performance critical for sale?

**Tips of problems performance:**
- **Slow preferences**: Slow predictions
- **High Memorial Use**: High use of memory
- **GPU Problems**: Issues with GPU
- **CPU Bottlenecks**: CPU bottlenecks
- **network Issues**: Issues with network
- **Disk I/O Problems**: Issues with disk

** Key aspects of the problem of performance:**
- **Sized predictions**: Unoptimized models, inefficient algorithms
- ** High use of memory**: Memory leaks, inefficient Management resources
- **Issues with GPU**: Incorrect configuring GPU, inefficient use
- **Issues with CPU**: Neoptimal configuring flows, bottlenecks
- **Issues with network**: Slow data transmission, ineffective protocols
- **Issues with disk**: Slow I/O, inefficient cache

*## 1. Slow predictions

#### Problem: Slow predictions
```python
# Diagnostics performance
import time

def diagnose_Prediction_performance(predictor, data):
""Dignostics performance preferences""

# Test on a small sample
 small_data = data.head(100)

 start_time = time.time()
 predictions = predictor.predict(small_data)
 Prediction_time = time.time() - start_time

 print(f"Prediction time for 100 samples: {Prediction_time:.4f} seconds")
 print(f"Prediction time per sample: {Prediction_time/100:.6f} seconds")

# Estimation of time for full dateset
 estimated_time = Prediction_time * len(data) / 100
 print(f"Estimated time for full dataset: {estimated_time:.2f} seconds")

 return Prediction_time

# Use
Prediction_time = diagnose_Prediction_performance(predictor, test_data)
```

**Decision:**
```python
# Optimizing performance
def optimize_Prediction_performance(predictor, data):
"Optimization performance preferences"

# Package processing
 batch_size = 1000
 predictions = []

 for i in range(0, len(data), batch_size):
 batch = data.iloc[i:i+batch_size]
 batch_predictions = predictor.predict(batch)
 predictions.extend(batch_predictions)

 return predictions
```

** Detailed description of optimization parameters:**

- **'batch_size = 1000'**: Size of package for processing
- `1000': Standard package size (recommended)
- `500': Smaller package (for limited memory)
- `2000': Large package (for fast systems)
- `100': Minimum package (for very slow systems)

- **'range(0, Len(data), batch_size)'**: Iteration on data
- `0': Initial index
- `len(data)': Final index
- `batch_size': Iteration step
- Application: processing of data on parts

- **'data.iloc[i:i+batch_size] `**: Data sample
- `i': Initial index package
== sync, corrected by elderman == @elder_man
- `iloc': Positional access to data
- Benefits: Effective Working with large datasets

** Additional parameters optimization:**

- **'predictor.predict(batch)'**:Pension for package
- `batch': data package
- Returns: the array of preferences
- Optimization: processing multiple samples simultaneously

- **'predications.extend(batch_predations)'**: Merging results
- `extend()': Adds all elements of the list
- `append()': Adds one element
- Benefits: Effective array integration

# or use a simpler model
def create_fast_model(predictor, data):
""create fast model."

 fast_predictor = TabularPredictor(
 label=predictor.label,
 problem_type=predictor.problem_type,
 eval_metric=predictor.eval_metric,
 path='./fast_models'
 )

# Training only on fast algorithms
 fast_predictor.fit(
 data,
 hyperparameters={
 'GBM': [{'num_boost_round': 50}],
 'RF': [{'n_estimators': 50}]
 },
 time_limit=300
 )

 return fast_predictor
```

** Detailed description of rapid model parameters:**

- **'label=predictor.label'**: Target variable
- Copys the target variable from the original model
- Ensure compatibility with data
- Application: Maintaining the task structure

- **'problem_type=predictor.problem_type'**: Type of task
- `'binary': Binary classification
``multi-class': Multi-class classification
- ``regression':
`'Quantile': Quantile regression

- **'eval_metric=predictor.eval_metric'**:Metric evaluation
- ``accuracy': Accuracy (classification)
- `'rmse'': RMSE (recession)
- `'mae'': MAE (recession)
- `'f1'': F1-score (classification)

- **'path='./fast_models'**: Path for model preservation
- `'./fast_models': Local folder
- `'./models/fast': Added folder
- `'/tmp/fast_models': Time folder
- Application: isolation of quick models

- **'hyperparameters={'GBM':{'num_boost_round': 50}}**: Hyperparameters
 - `'GBM'`: Gradient Boosting Machine
== sync, corrected by elderman == @elder_man
 - `'RF'`: Random Forest
- `'n_estimators': 50': 50 trees (rapid)

- **'time_limit=300'**: Limiting time of study
`300': 5 minutes (rapid learning)
`600': 10 minutes (standard time)
`1800': 30 minutes (quality models)
Application: monitoring of the time of instruction

# Use
fast_predictor = create_fast_model(predictor, train_data)
fast_predictions = fast_predictor.predict(test_data)
```

###2. High use of memory

#### Problem: High use of memory
```python
# Memory Diagnostics
import psutil
import gc

def diagnose_memory_usage():
"The Diagnosis of Memory Use""

 process = psutil.Process()
 memory_info = process.memory_info()

 print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
 print(f"Memory percent: {process.memory_percent():.2f}%")

 return memory_info.rss / 1024 / 1024

# Use
memory_usage = diagnose_memory_usage()
```

**Decision:**
```python
# Memory Optimization
def optimize_memory_usage(predictor, data):
"Optimization of memory use""

# Data processing on parts
 chunk_size = 1000
 predictions = []

 for i in range(0, len(data), chunk_size):
 chunk = data.iloc[i:i+chunk_size]
 chunk_predictions = predictor.predict(chunk)
 predictions.extend(chunk_predictions)

# Clear memory
 del chunk
 gc.collect()

 return predictions

# or use more effective data types
def optimize_data_types(data):
"Optimization of Data Types""

 for col in data.columns:
 if data[col].dtype == 'float64':
 data[col] = data[col].astype('float32')
 elif data[col].dtype == 'int64':
 data[col] = data[col].astype('int32')

 return data

# Use
data_optimized = optimize_data_types(data)
```

# The problems are sold

<img src="images/optimized/production_issues.png" alt="Problems sold" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 16.6: Diagnostics and solutions to problems produced by AutoML Gluon - criticalities and solutions*

Because they're real users and business:

**Tips of problems sold:**
- **Model Loading Errors**: Model upload errors
- **API Errors**: API errors
- **InfraStructure Procedures**: Issues with infrastructure
- **Monitoring Issues**: Issues with Monitoring
- **Security Vulnerabilities**: Vulnerability to safety
- **Scaling Problems**: Scaling Problems

** Key aspects of sales problems:**
- ** Model download errors**: Issues with seriesization, incompatible versions
- **API Errors**: Wrong configuring API, Issues with data formats
- **Issues with infrastructure**: Lack of resources, Issues with network
- **Issues with Monitoring**: Absence of allers, incorrect metrics
- **Issues with safety**: Vulnerability, incorrect Autification
- **Issues with scaling**: Ineffective scaling, bottlenecks

###1. Model upload errors

#### Problem: Model upload errors
```python
# Model loading diagnostics
def diagnose_model_Loading(model_path):
"""""""" "model download diagnostics"""

 try:
# Check existence files
 import os
 if not os.path.exists(model_path):
 print(f"Model path does not exist: {model_path}")
 return False

# Check model structure
 required_files = ['predictor.pkl', 'metadata.json']
 for file in required_files:
 file_path = os.path.join(model_path, file)
 if not os.path.exists(file_path):
 print(f"required file Missing: {file_path}")
 return False

# Trying to load
 predictor = TabularPredictor.load(model_path)
 print("Model loaded successfully")
 return True

 except Exception as e:
 print(f"Model Loading error: {e}")
 return False

# Use
if not diagnose_model_Loading('./models'):
 print("Model Loading issues detected")
```

**Decision:**
```python
# fix model download problems
def fix_model_Loading_issues(model_path):
""fix loading problems of the model."

 try:
# Check version of AutoGluon
 import autogluon as ag
 print(f"AutoGluon Version: {ag.__version__}")

# Loading with compatibility check
 predictor = TabularPredictor.load(
 model_path,
Require_version_match=False # Ignore inconsistent versions
 )

 return predictor

 except Exception as e:
 print(f"Failed to load model: {e}")

# Trying to recreate the model
 print("Attempting to recreate model...")
# There's gotta be a Logsto remodel
 return None

# Use
predictor = fix_model_Loading_issues('./models')
```

###2, API errors

#### Problem: Errors in API
```python
# API diagnostics
def diagnose_api_issues(api_url, test_data):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""A"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 try:
 # health check
 response = requests.get(f"{api_url}/health")
 if response.status_code != 200:
 print(f"health check failed: {response.status_code}")
 return False

# A prophecy test
 response = requests.post(f"{api_url}/predict", json=test_data)
 if response.status_code != 200:
 print(f"Prediction failed: {response.status_code}")
 print(f"Error: {response.text}")
 return False

 print("API Working correctly")
 return True

 except Exception as e:
 print(f"API error: {e}")
 return False

# Use
if not diagnose_api_issues("http://localhost:8000", test_data):
 print("API issues detected")
```

**Decision:**
```python
# Fix API problems
def fix_api_issues(api_url, test_data):
""fix problems API""

 try:
# API access check
 response = requests.get(f"{api_url}/health", timeout=5)

 if response.status_code == 200:
 health_data = response.json()
 print(f"API Status: {health_data['status']}")

# Check loaded models
 if 'loaded_models' in health_data:
 print(f"Loaded models: {health_data['loaded_models']}")

 return True
 else:
 print(f"API not healthy: {response.status_code}")
 return False

 except requests.exceptions.Timeout:
 print("API timeout - server may be overloaded")
 return False
 except requests.exceptions.ConnectionError:
 print("API connection error - server may be down")
 return False
 except Exception as e:
 print(f"API error: {e}")
 return False

# Use
if fix_api_issues("http://localhost:8000", test_data):
 print("API issues resolved")
else:
 print("API issues persist")
```

## Useful diagnostic tools

<img src="images/optimized/diagnostic_tools.png" alt="diagnosis tools" style="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
*Picture 16.7: Useful diagnostic and monitoring tools AutoML Gluon - components and benefits*

**Why do diagnostic tools matter?** Because they help to quickly identify and solve problems:

**Tips of diagnostic tools:**
- **system Monitoring**: Monitoring systems in real time
- **Logging system**: Logs system
- **PerformanceProfiling**: Profiling performance
- **Metrics Collection**: Collection of metrics
- **Alerting system**: Notification system
- **Dashboard Visualization**: Visualization of data

** Key aspects of diagnostic tools:**
- ** Monitoring system**: Real-time tracking
- ** Logs system**: Detailed recording of all events and errors
- ** Profiling**: Identification of bottlenecks in performance
- **metrics**: Quantification of system quality
**Alerting**: notes on real-time problems
- ** Dashboard**: Visualization of the system

♪##1 ♪ Monitoring system
```python
class AutoGluonMonitor:
"Monitoring AutoGluon System"

 def __init__(self):
 self.metrics = {}
 self.alerts = []

 def check_system_health(self):
""Health check system."

# Check memory
 memory = psutil.virtual_memory()
 if memory.percent > 90:
 self.alerts.append("High memory usage")

 # check CPU
 cpu = psutil.cpu_percent()
 if cpu > 90:
 self.alerts.append("High CPU usage")

# Check disc
 disk = psutil.disk_usage('/')
 if disk.percent > 90:
 self.alerts.append("High disk usage")

 return len(self.alerts) == 0
```

** Detailed descriptions of Monitoring system parameters:**

- **'memory.percent > 90'**: heck use of memory
`90': Critical threshold (90% use)
`80': Warning threshold (80 per cent use)
- `95': Extreme threshold (95 per cent use)
- Application: Prevention of memory shortages

- **'cpu > 90'**: check use of CPU
`90': Critical threshold (90% use)
`80': Warning threshold (80 per cent use)
- `95': Extreme threshold (95 per cent use)
- Application: Prevention of overloading CPU

- **'disk.percent > 90'**: check disk use
`90': Critical threshold (90% use)
`80': Warning threshold (80 per cent use)
- `95': Extreme threshold (95 per cent use)
- Application: preventing a lack of space on disk

- **'self.alerts.append()'**: ad dealers
- `High memory use': "Alert of High Memory"
- `High CPU use': High-load dealer for CPU
- `High disk use': "Alert for high-loading disc
- Application: notes on problems

- **'len(self.alerts) ==0'**: sheck availability
- `True': No allergics (health system)
- `False': There are allertes.
- Application: general assessment of the state of the system

 def check_model_performance(self, predictor, test_data):
"Check performance model."

 try:
# A prophecy test
 start_time = time.time()
 predictions = predictor.predict(test_data.head(100))
 Prediction_time = time.time() - start_time

# Check time
ifPedication_time > 10: #10 seconds for 100 samples
 self.alerts.append("Slow Prediction performance")

# Check quality
 performance = predictor.evaluate(test_data.head(100))
 if performance.get('accuracy', 0) < 0.8:
 self.alerts.append("Low model accuracy")

 return True

 except Exception as e:
 self.alerts.append(f"Model performance error: {e}")
 return False

 def generate_Report(self):
""""""" "Generation Report"""

 Report = {
 'timestamp': datetime.now().isoformat(),
 'system_health': self.check_system_health(),
 'alerts': self.alerts,
 'metrics': self.metrics
 }

 return Report

# Use
monitor = AutoGluonMonitor()
Report = monitor.generate_Report()
print("Monitoring Report:", Report)
```

###2, Logsoring system
```python
import logging
from datetime import datetime

class AutoGluonLogger:
""The Logs for AutoGluon System""

 def __init__(self, log_file='autogluon.log'):
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
```

** Detailed description of the Logsoring system parameters:**

- **'level=logging.INFO'**: Logs level
- `logging.DEBUG': Debugging information (all communications)
- `logging.INFO': Information messages (recommended)
- `logging.WARNING': Warnings and Errors
- `logging.EROR': Only errors
- `logging.CRITICAL': Only critical errors

- **'format='%(asctime)s -%(name)s -%(levelname)s -%(message)s''**: Log format
- `%(asctime)s': Time of event
- `%(name)s': Logger's name
- `%(levelname)s': Logstration level
- `%(message)s': Message
Application: Structured Logs

- **'logging.FileHandler(self.log_file)'**: File handler
- `self.log_file': Path to log file
- ``autogluon.log': Standard file name
- `'./Logs/autogluon.log': Added folder
- Application: Save logs in file

- **'logging.StreamHandler()'**: Consolidater
- Brings out Logs in the console.
- Useful for debugging.
Application: Monitoring in real time

- **'logging.getLogger(__name__)'**: creative logger
- `_name_': Name of the current module
- Creates a unique logger.
- Application: identification of source of lairs

 def log_training_start(self, data_info):
"Logsrance of Starting Learning."
 self.logger.info(f"Training started: {data_info}")

 def log_training_complete(self, results):
""Logsrance of Completion""
 self.logger.info(f"Training COMPLETED: {results}")

 def log_Prediction(self, input_data, Prediction, processing_time):
""Logsrance of Promise""
 self.logger.info(f"Prediction: input={input_data}, Prediction={Prediction}, time={processing_time}")

 def log_error(self, error, context):
""Logsir of Mistakes""
 self.logger.error(f"Error: {error}, context: {context}")

# Use
logger = AutoGluonLogger()
logger.log_training_start({'data_size': len(train_data)})
```

## Next steps

Once the problems have been solved, go to:
- [best practice](.08_best_practices.md)
- [Examples of use](./09_examples.md)
