# installation AutoML Gluon

**Author:** NeoZorK (Shcherbyna Rostyslav)
**Date:** 2025
**Location:** Ukraine, Zaporizhzhya
**Version:** 1.0

## Why Proper installation is Critical

**Why is it that 70% of AutoML Gluon issues are related to improper installation?** BecaUse machine learning requires precise environment Settings. Incorrect installation can lead to unstable operation, errors and loss of time.

### 🚨 Real Consequences of Incorrect installation

**Case 1: NumPy Version Conflict **
```python
# What happens when there is a version conflict
import numpy as np
# Error: "numpy.core.multiarray failed to import"
# Result: AutoML Gluon not Launching
```

**Case 2: Issues with CUDA**
```python
# What happens without the right CUDA
import torch
print(torch.cuda.is_available()) # False
# Result: Learning 100x slower
```

**Case 3: Out of memory**
```python
# What happens when there is a shortage of RAM
import pandas as pd
df = pd.read_csv('large_dataset.csv') # MemoryError
# Result: Impossible to work with big data
```

### What Happens with Incorrect installation?
- ** Dependency conflicts **: Different versions of libraries caUse errors
- *example*: NumPy 1.19 vs 1.21 - different APIs, code breaks
- *Solution*: Use virtual environments
- **Issues with performance**: Models Working Slowly or Not Working at all
- *example*: Training 1 hour instead of 5 minutes
- *Reason*: Suboptimal versions of libraries
- ** Compilation errors **: Some algorithms cannot be compiled
- *example*: XGBoost is not compiled on older systems
- *Solution*: Update compiler and dependencies
- **Issues with GPU**: CUDA not Working, training is only on CPU
- *example*: Training 10 hours instead of 1 hour
- *Solution*: Correct installation of CUDA and cuDNN

### What does the right installation do?
- **Stable Working**: all components work without errors
- *Result*: 99.9% failure-free time
- *Save*: Don't waste time on debugging
- **Optimal performance**: Maximum learning speed
- *Result*: Learning 10-100 times faster
- *savings*: Hours instead of days
- **Ease of Use**: all functions are available out of the box
- *Result*: You can start ML projects right away
- *Savings*: Don't learn the setup
- **Easy to update**: Easy to update to new versions
- *Result*: Always up-to-date opportunities
- *Savings*: You don't have to reinstall everything

system requirements

<img src="images/optimized/installation_flowchart.png" alt="AutoML Gluon installation" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 1: AutoML Gluon installation Flowchart *

### AutoML Gluon 🏗️ Architecture

<img src="images/optimized/architecture_diagram.png" alt="Architecture AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 2: AutoML Gluon Architectural Diagram *

**Why is it important to understand architecture?** BecaUse it helps to understand how AutoML Gluon works inside and why it is so effective:

- **TabularPredictor**: The main component for Working with tabular data
- **TimeSeriesPredictor**: Specialized component for time series
- **ImagePredictor**: Component for Working with images
- **TextPredictor**: A component for word processing
- **Ensemble Methods**: Methods of combining models for improving accuracy
- **Feature Engineering**: Automatically create new features
- **Hyperparameter Tuning**: Automatic configuration of model parameters

Minimum requirements
**Why are minimum requirements important?** BecaUse they determine if you can run AutoML Gluon at all:

- **Python**: 3.7, 3.8, 3.9, 3.10, 3.11
- *Why these versions?* BecaUse AutoML Gluon Uses modern Python capabilities
- *What happens with Python 3.6?* Compilation errors, library incompatibilities
- *What's going on with Python 3.12?* Some dependencies are not yet supported
- *Recommendation*: Use Python 3.9 or 3.10 for stability
- **OS**: Linux, macOS, Windows
- *Why are all OS supported?* BecaUse ML development is carried out on different platforms
- *Linux*: Better performance, more features
- *macOS*: Ease of development, good performance
- *Windows*: Easy to Use but possible Issues with some libraries
- **RAM**: 4GB (8GB+ recommended)
- *Why do you need a lot of memory?* BecaUse ML models load large datasets in memory
- *What happens to 2GB RAM?* system freezes, training is interrupted
- *What happens to 16GB+ RAM?* You can process datasets in 10 times more
- *Practical example*: 1GB dataset requires 4GB RAM for processing
- **CPU**: 2 cores (4+ cores recommended)
- *Why are kernels important?* BecaUse AutoML Gluon Uses parallel computing
- *What happens to 1 core?* Training is 4 times slower
- *What happens to 8+ cores?* Training 4-8 times faster
- *Practical example*: Training 1 hour on 2 cores = 15 minutes on 8 cores
- **Disk**: 2GB free space
- *Why do we need space?* BecaUse models and data take up a lot of space
- *What takes up space?* Models (500MB-2GB), cache (1-5GB), data (depends on size)
- *Practical example*: A project with 10 models takes 5-10GB

Compare Performance

<img src="images/optimized/performance_comparison.png" alt="Comparison performance" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 3: Comparison of AutoML Gluon performance on different configurations*

**Why is it important to understand performance?** BecaUse it helps to choose the optimal configuration for your tasks:

- **CPU vs GPU**: GPU speeds up learning in 10-100 times for neural networks
- **Memory**: More RAM = ability to handle large datasets
- **Cores**: More cores = parallel training of several models
- ** Training time **: from 10 minutes to several hours in dependencies from configuration

### Model Quality 🎯 Metrics

<img src="images/optimized/metrics_comparison.png" alt="Metrics comparison" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 4: Comparison of different model quality metrics *

**Why is it important to understand metrics?** BecaUse different tasks require different metrics for quality assessment:

- **Accuracy**: Percentage of correct predictions (for balanced data)
- **Precision**: Accuracy of positive predictions (important at high cost of errors)
- **Recall**: Completeness of positive predictions (important not to miss important cases)
- **F1-Score**: Harmonic mean of precision and recall (balanced metric)
- **AUC-ROC**: Area under the ROC curve (quality of class separation)
- **RMSE**: Root of RMSE (for regression)

### Recommended requirements
**Why do the recommended requirements provide the best experience?** BecaUse they provide optimal performance:

- **Python**: 3.9 or 3.10
- *Why these versions?* BecaUse they are the most stable and fast
- *Benefits*: Better performance, stability, compatibility
- *Practical example*: Learning Python 3.10 on 15% faster than on 3.8
- **RAM**: 16GB+
- *Why a lot of memory?* BecaUse large datasets require a lot of RAM
- *What can I do with 16GB?* Process datasets up to 10GB, train complex models
- *What can I do with 32GB+?* Process datasets up to 50GB, train model ensembles
- *Practical example*: 5GB dataset requires 20GB RAM for comfortable operation
- **CPU**: 8+ cores
- *Why so many cores?* BecaUse AutoML Gluon Uses all available cores
- *What happens to the 8 cores?* Training 4-8 times faster than with 2 cores
- *What happens to 16+ cores?* Training is 8-16 times faster
- *Practical example*: Training 1 hour on 2 cores = 7 minutes on 16 cores
- **GPU**: NVIDIA GPU with CUDA support (optional)
- *Why is the GPU important?* BecaUse it speeds up learning in 10-100 times
- *Minimum GPU requirements *: GTX 1060 6GB or better
- *Recommended GPUs*: RTX 3070, RTX 4080, A100 for professional operation
- *Practical example*: Training 10 hours on CPU = 1 hour on RTX 3070
- **Disk**: 10GB+ free space
- *Why so much space?* BecaUse models and cache take up so much space
- *SSD vs HDD*: SSD in 5-10 times faster for data Loading
- *Practical example*: A project with 50 models takes 20-50GB

## AutoML Gluon 🔄 Workflows

<img src="images/optimized/retraining_workflow.png" alt="Workflow retraining" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 5: Model retraining workflow diagram *

**Why is it important to understand workflows?** BecaUse it helps to understand how AutoML Gluon automates the entire machine learning process:

- ** data preparation **: Automatic clean and preprocessing
- **Feature Engineering**: create new features from existing ones
- **Selection of algorithms**: Automatic selection of the best algorithms for the problem
- **training models**: parallel training of multiple models
- **Validation**: Automatic model quality assessment
- **Ensemble**: Combining the best models for improving accuracy
- **Deploy**: Ready-made models for production

## installation via pip

**Why is pip the most popular installation method?** BecaUse it is simple, reliable and automatically solves dependencies.

## 🚀 installation via uv (Recommended)

**Why is uv better than pip?** BecaUse uv is 10-100 times faster, more reliable, and better at managing addictions.

### What is uv?
**uv** is a modern Python package manager written on Rust. It solves all pip problems:

- **Speed**: in 10-100 times faster than pip
- **Reliability**: Better resolves dependency conflicts
- **Security**: checks package integrity
- **Compatibility**: Full compatibility with pip

### installation uv
```bash
# installation uv via pip (if you already have Python)
pip install uv

# or via curl (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# or via homebrew on macOS
brew install uv
```

**What happens when uv is installed?**
- DownLoading binary file uv (5-10MB)
- installed in system PATH
- Configuration file is created
- Configures the package cache

### AutoML Gluon installation via uv
```bash
# Basic installation
uv add autogluon

# installation with additional components
uv add autogluon.tabular
uv add autogluon.timeseries
uv add autogluon.vision

# installation in virtual environment
uv venv
uv pip install autogluon
```

**Advantages of uv over pip:**
- **Speed**: installation in 10 times faster
- **Reliability**: Fewer dependency conflicts
- **Caching**: Smart Packet Caching
- **Parallelism**: installation of multiple packages simultaneously

### 🚀 Basic installation
**Why start with a basic setup?** BecaUse it gives you everything you need to get started:

```bash
pip install autogluon
```

**What happens with this team?**
- main AutoML Gluon package is installed
- all necessary dependencies are automatically set
- An environment for Working with tabular data is created
- Basic configuration is configured

**Detailed installation process:**
```python
# What happens inside pip install autogluon
# 1 - Package Download (50-100MB)
# 2. installation of dependencies:
# - numpy, pandas, scikit-learn
# - xgboost, lightgbm, catboost
# - torch, torchvision
# - matplotlib, seaborn
# 3. check version compatibility
# 4. create configuration files
# 5. Unit testing
```

Set-up time
- Fast internet: 5-10 minutes
- Slow internet: 30-60 minutes
- First installation: Longer due to compilation
- Subsequent updates: Faster

### 🎯 installation with additional dependencies
**Why do I need additional components?** BecaUse different tasks require different tools:

#### 📊 for Working with tabular data
```bash
pip install autogluon.tabular
```

**What is autogluon.tabular?**
- Optimized algorithms for tabular data
- Automatic processing of categorical variables
- Built-in validation and metrics
- Support for large datasets

**Detailed Opportunities:**
```python
# What autogluon.tabular includes
from autogluon.tabular import TabularPredictor

algos
# - XGBoost, LightGBM, CatBoost
# - Random Forest, Extra Trees
# - Neural networks
# - Linear Models
# - Ensemble Methods

# Automatic Capabilities:
# - Feature Engineering
# - Hyperparameter Tuning
# - Model Selection
# - Cross-Validation
```

WHEN TO Use IT
- Classification and regression
- Tabular data (CSV, Excel, SQL)
- Structured data
Business <ph type="Structure-only" x="0"/>Analytics

#### ᐈ for Working with time series
```bash
pip install autogluon.timeseries
```

**What is autogluon.timeseries?**
- Special algorithms for time series
- Automatic determination of seasonality
- Multidimensional time series support
- Built-in Prediction

**Detailed Opportunities:**
```python
# What autogluon.timeseries includes
from autogluon.timeseries import TimeSeriesPredictor

algos
# - ARIMA, SARIMA
# - Prophet, ETS
# - Deep Learning (LSTM, Transformer)
# - Ensemble Methods

# Automatic Capabilities:
# - Seasonality Detection
# - Trend Analysis
# - Anomaly Detection
# - Multi-step Forecasting
```

WHEN TO Use IT
Sales forecasting
time series analysi
- Financial data
- IoT data

#### 🖼️ for Working with images
```bash
pip install autogluon.vision
```

**What is autogluon.vision?**
- Ready-made CNN architectures
- Automatic data enlargement
- Prebuilt models
- GPU acceleration support

```bash
# for Working with text
pip install autogluon.text
```
**What is autogluon.text?**
- Modern NLP models
- Automatic tokenization
- Pre-purchased embeddings
- Support for Transformers

```bash
# Complete installation of all components
pip install autogluon[all]
```
**Why is full installation convenient?** BecaUse you get all the opportunities at once, but it takes more space and time.

## installation via conda

### create new environment
```bash
# create environments with Python 3.9
conda create -n autogluon python=3.9
conda activate autogluon

# installation AutoGluon
conda install -c conda-forge autogluon
```

### installation with GPU support
```bash
# create environments with CUDA
conda create -n autogluon-gpu python=3.9
conda activate autogluon-gpu

# installation PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# installation AutoGluon
pip install autogluon
```

## installation from source code

### Repository Cloning
```bash
git clone https://github.com/autogluon/autogluon.git
cd autogluon
```

### installation in development mode
```bash
# installation of dependencies
pip install -e .

# or for a specific module
pip install -e ./tabular
```

## Validation and testing 📋 Methods

<img src="images/optimized/validation_methods.png" alt="Methods validation" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 6: Various model validation methods *

**Why is validation important?** BecaUse it ensures the reliability and quality of models:

- **Holdout Validation**: Simple separation on train/test (70/30)
- **Cross-Validation**: K-fold cross-validation for more reliable evaluation
- **Time Series Split**: Special validation for time series
- **Stratified Split**: Saving class proportions when splitting
- **Walk-Forward Analysis**: Sliding window for time series

### Troubleshooting 🔧 Diagram

<img src="images/optimized/Troubleshooting_flowchart.png" alt="Troubleshooting diagram" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 7: installation Troubleshooting step-by-step diagram *

**Why do I need a Troubleshooting chart?** BecaUse it helps solve 90% of problems quickly:

- **Issues with dependencies**: Library version conflicts
- **Issues with memory**: Lack of RAM for large datasets
- **Issues with GPU**: Incorrect configuration CUDA
- **Issues with performance**: Suboptimal Settings

## installation checks

Baseline test
```python
import autogluon as ag
print(f"AutoGluon Version: {ag.__version__}")

# Core Module import Test
from autogluon.tabular import TabularPredictor
from autogluon.timeseries import TimeSeriesPredictor
from autogluon.vision import ImagePredictor
from autogluon.text import TextPredictor

print("all modules imported successfully!")
```

### Test with a simple example
```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# create test data
data = pd.dataFrame({
 'feature1': np.random.randn(100),
 'feature2': np.random.randn(100),
 'target': np.random.randint(0, 2, 100)
})

# Training Test
predictor = TabularPredictor(label='target')
predictor.fit(data, time_limit=10) # 10 seconds for a quick test
print("installation test passed!")
```

## installation of additional dependencies

### for Working with GPUs
```bash
# installation CUDA toolkit (Ubuntu/Debian)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repository-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo dpkg -i cuda-repository-ubuntu2004-11-8-local_11.8.0-520.61.05-1_amd64.deb
sudo apt-key add /var/cuda-repository-ubuntu2004-11-8-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

# installation PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### for Working with large datasets
```bash
# installation of additional libraries for big data processing
pip install dask[complete]
pip install ray[default]
pip install modin[all]
```

#### 📊 Detailed describe of libraries for large datasets

**Dask - Distributed Computing for Big data**

Intended purpose
- Parallel processing of data that is not stored in memory
- Distributed computing across multiple cores/nodes
- integration with pandas, numpy, scikit-learn

ADVANTAGES
- **Scalability**: data processing in 10-100 times more available memory
- **Compatibility**: API similar to on pandas/numpy, easy to migrate code
- **Flexibility**: Works on a single computer or cluster
- **integration**: Integrates well with AutoML Gluon
- **Failover**: Automatic disaster recovery

Deficiencies
- **Complexity of Settings**: Requires understanding of distributed systems
- **Overhead**: for small data may be slower than pandas
- **Debugging * *: It's harder to debug distributed code
- **dependencies**: Many additional packages

**Practical examples of Use:**
```python
# Processing large CSV files
import dask.dataframe as dd

# 50GB file upload (not fit in RAM)
df = dd.read_csv('huge_dataset.csv') # Loaded on parts

# Operations are performed lazily
result = df.groupby('category').sum().compute() # executed only when compute()

# integration with AutoML Gluon
from autogluon.tabular import TabularPredictor
predictor = TabularPredictor(label='target')
predictor.fit(df, time_limit=3600) # Works with Dask dataFrame
```

**Ray - Distributed Framework for ML**

Intended purpose
- Distributed machine learning
- Parallel task processing
- Management of resources in the cluster

ADVANTAGES
- **Performance**: Very fast distributed computing
- **ML optimization **: Specially created for machine learning
- **Automatic scaling**: Automatically Uses available resources
- **Fault tolerance**: Built-in error handling
- **Flexibility**: Supports any Python functions

Deficiencies
- **Difficulty**: Harder to learn than Dask
- **Resources**: Requires more memory for coordination
- **Debugging * *: It's harder to debug distributed tasks
- **dependencies**: Many system dependencies

**Practical examples of Use:**
```python
import ray
from autogluon.tabular import TabularPredictor

# Ray Initialization
ray.init()

# Distributed model training
@ray.remote
def train_model(data_chunk):
 predictor = TabularPredictor(label='target')
 predictor.fit(data_chunk, time_limit=1800)
 return predictor

# parallel training on different parts of the data
futures = [train_model.remote(chunk) for chunk in data_chunks]
models = ray.get(futures)

# Model Ensemble
ensemble_predictions = []
for model in models:
 pred = model.predict(test_data)
 ensemble_predictions.append(pred)
```

**Modin - Accelerated Pandas**

Intended purpose
- acceleration of pandas operations by 2-10 times
- Automatic Use of all available cores
- Transparent pandas replacement

ADVANTAGES
- **Simplicity**: Direct replacement of pandas, minimal code changes
- **Speed**: Automatic acceleration of pandas operations
- **Compatibility**: Fully compatible with pandas API
- **Performance**: Uses all available cores
- **integration**: Easily integrates with existing code

Deficiencies
- **Limited functionality**: not all pandas functions are supported
- **Memory**: Can Use more memory than pandas
- **Stability**: Less stable than original pandas
- **dependencies**: Requires Ray or Dask as backend

**Practical examples of Use:**
```python
# Easy replacement of pandas on modin
import modin.pandas as pd # Instead of import pandas as pd

# all operations are automatically accelerated
df = pd.read_csv('large_dataset.csv') # 2-5 times faster
result = df.groupby('category').sum() # in 3-8 times faster

# integration with AutoML Gluon
from autogluon.tabular import TabularPredictor
predictor = TabularPredictor(label='target')
predictor.fit(df, time_limit=3600) # Works with Modin dataFrame
```

**Comparison of Libraries for Big data:**

| Library | data Size | Difficulty | Speed | Stability |
|------------|---------------|-----------|----------|--------------|
| **Dask** | 10GB - 1TB+ | Medium | High | High |
| **Ray** | 1GB - 100GB+ | High | Very High | Medium |
| **Modin** | 100MB - 10GB | Low | Medium | Medium |

**Recommendations for choosing:**

**Use Dask if:**
- data more available memory
- Maximum compatibility with pandas is required
- Working with a cluster
- Fault tolerance is required

**Use Ray if:**
- Maximum performance is required
- Working with ML tasks
- Experience with distributed systems
- Automatic scaling is required

**Use Modin if:**
- data are placed in memory
- Minimal code change required
- Working on one computer
- Need rapid prototyping

### for Working with time series
```bash
# Special libraries for time series
pip install gluonts
pip install mxnet
pip install statsmodels
```

#### # Detailed describe of libraries for time series

**GluonTS - Specialized Library for Time Series**

Intended purpose
- Deep learning for time series Prediction
- Ready-made models for various types of time series
- integration with MXNet and PyTorch
- Automatic detection of seasonality and trends

 Facilities
- **Finished models**: DeepAR, Transformer, WaveNet, MQ-CNN
- **Automatic processing**: Determination of seasonality, trends, anomalies
- **Multidimensional series**: Working with multiple linked time series
- **Uncertainty**: Quantile predictions and confidence intervals
- **Scalability**: Processing thousands of time series simultaneously

**Practical examples of Use:**
```python
import gluonts
from gluonts.dataset import common
from gluonts.model.deepar import DeepAREstimator
from gluonts.trainer import Trainer

# create dataset for time series
dataset = common.Listdataset(
 data_iter=[{"start": "2020-01-01", "target": [1, 2, 3, 4, 5]}],
 freq="D"
)

# DeepAR Model Training
estimator = DeepAREstimator(
 freq="D",
 Prediction_length=7,
 trainer=Trainer(epochs=10)
)

# Learning and Forecasting
predictor = estimator.train(dataset)
forecast = predictor.predict(dataset)

# integration with AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
 target="sales",
 Prediction_length=24,
 freq="H"
)
predictor.fit(train_data, time_limit=3600)
```

**MXNet - Deep Learning for Time Series**

Intended purpose
- Flexible framework for deep learning
- Optimization for time series
- GPU and distributed computing support
- integration with GluonTS

 Facilities
- **Flexible architecture**: create custom models for time series
- **GPU acceleration**: Quick learning on GPU
- **Distribution**: Training on the cluster
- **Optimization**: Automatic gradient optimization
- **Integration**: Works well with GluonTS

**Practical usage examples:**
```python
import mxnet as mx
from mxnet import gluon, autograd
import numpy as np

# Create LSTM model for time series
class LSTMPredictor(gluon.Block):
 def __init__(self, hidden_size, output_size):
 super(LSTMPredictor, self).__init__()
 self.lstm = gluon.rnn.LSTM(hidden_size)
 self.dense = gluon.nn.Dense(output_size)

 def forward(self, x):
 output = self.lstm(x)
 return self.dense(output[-1])

# Model training
model = LSTMPredictor(hidden_size=50, output_size=1)
model.initialize()

# integration with AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
 target="value",
 Prediction_length=12,
 freq="M"
)
predictor.fit(train_data, time_limit=1800)
```

**Statsmodels - Statistical Models for Time Series**

**Purpose:**
- Classical statistical models
- Time series analysis
- Stationarity testing
- Seasonal decomposition

**Capabilities:**
- **ARIMA/SARIMA**: Classical autoregression models
- **ETS**: Exponential Smoothing models
- **Seasonal decomposition**: STL, X-13ARIMA-SEATS
- **Testing**: ADF, KPSS stationarity tests
- **Diagnostics**: ACF, PACF, Ljung-Box tests

**Practical usage examples:**
```python
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Stationarity analysis
def check_stationarity(timeseries):
 result = adfuller(timeseries)
 print(f'ADF Statistic: {result[0]}')
 print(f'p-value: {result[1]}')
 return result[1] < 0.05

# Seasonal decomposition
decomposition = seasonal_decompose(timeseries, model='additive')
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# ARIMA model
model = ARIMA(timeseries, order=(1,1,1))
fitted_model = model.fit()
forecast = fitted_model.forecast(steps=12)

# integration with AutoML Gluon
from autogluon.timeseries import TimeSeriesPredictor
predictor = TimeSeriesPredictor(
 target="price",
 Prediction_length=30,
 freq="D"
)
predictor.fit(train_data, time_limit=3600)
```

**Comparison of libraries for time series:**

| Library | Model Type | Complexity | Performance | Accuracy |
|------------|-------------|-----------|-------------------|----------|
| **GluonTS** | Deep Learning | High | Very High | Very High |
| **MXNet** | Custom Deep Learning | Very High | High | High |
| **Statsmodels** | Statistical | Low | Medium | Medium |

**Recommendations for selection:**

**Use GluonTS if:**
- You need modern deep learning models
- Working with large volumes of data
- Need quantile forecasts
- High accuracy is required

**Use MXNet if:**
- You need custom architectures
- Maximum flexibility is required
- Working with GPU
- Need distributed training

**Use Statsmodels if:**
- You need classical statistical models
- Interpretability is required
- Working with small data
- Detailed analysis is needed

**Integration with AutoML Gluon for time series:**

```python
from autogluon.timeseries import TimeSeriesPredictor
import pandas as pd

# Data preparation
train_data = pd.dataFrame({
 'timestamp': pd.date_range('2020-01-01', periods=1000, freq='H'),
 'target': np.random.randn(1000).cumsum(),
 'feature1': np.random.randn(1000),
 'feature2': np.random.randn(1000)
})

# Create predictor
predictor = TimeSeriesPredictor(
 target="target",
Prediction_length=24, # Forecast for 24 hours
freq="H", # Hourly data
 eval_metric="MAPE"
)

# Training with various models
predictor.fit(
 train_data,
time_limit=3600, # 1 hour
presets="best_quality" # Best quality
)

# Forecasting
predictions = predictor.predict(train_data)
print(f"predictions shape: {predictions.shape}")

# Quality assessment
performance = predictor.evaluate(train_data)
print(f"Model performance: {performance}")
```

## Environment Configuration

### Environment Variables
```bash
# Set variables for performance optimization
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4

# For GPU
export CUDA_VISIBLE_DEVICES=0

# For debugging
export AUTOGLUON_DEBUG=1
```

#### 🔧 Detailed Description of Environment Variables

**OMP_NUM_THREADS - OpenMP Thread Control**

**Purpose:**
- Controls the number of threads for OpenMP operations
- Affects performance of numpy, scipy, scikit-learn
- Optimizes CPU core usage

**Recommended values:**
- **2-4 cores**: `OMP_NUM_THREADS=2`
- **4-8 cores**: `OMP_NUM_THREADS=4`
- **8+ cores**: `OMP_NUM_THREADS=6-8`

**Practical examples:**
```bash
# For systems with 8 cores
export OMP_NUM_THREADS=6 # Leave 2 cores for system

# For systems with 4 cores
export OMP_NUM_THREADS=3 # Leave 1 core for system

# For systems with 16 cores
export OMP_NUM_THREADS=12 # Leave 4 cores for system
```

**Impact on performance:**
- **Too few threads**: Underutilization of CPU
- **Too many threads**: Resource competition, performance degradation
- **Optimal value**: 70-80% of available cores

**Efficiency check:**
```python
import numpy as np
import time

# Performance test with different number of threads
def test_omp_performance():
# Create large matrix
 size = 5000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

# Measure matrix multiplication time
 start_time = time.time()
 result = np.dot(a, b)
 end_time = time.time()

 print(f"Matrix multiplication time: {end_time - start_time:.2f} seconds")
 print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'default')}")

# Run test
test_omp_performance()
```

**MKL_NUM_THREADS - Intel MKL Thread Control**

**Purpose:**
- Controls the number of threads for Intel Math Kernel Library
- Affects performance of numpy, scipy, pandas
- Optimizes mathematical operations

**Recommended values:**
- **Should equal OMP_NUM_THREADS**: `MKL_NUM_THREADS=4`
- **To avoid conflicts**: Should not exceed OMP_NUM_THREADS
- **For maximum performance**: Equal to number of physical cores

**Practical examples:**
```bash
# Synchronization with OMP_NUM_THREADS
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# For systems with Intel CPU
export MKL_NUM_THREADS=4 # Use 4 cores

# For systems with AMD CPU
export MKL_NUM_THREADS=2 # Fewer threads for AMD
```

**Impact on performance:**
- **Synchronization with OMP**: Prevents system overload
- **MKL optimization**: Maximum performance of mathematical operations
- **Conflict avoidance**: Prevents resource competition

**Settings check:**
```python
import numpy as np

# Check current settings
print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'not set')}")
print(f"MKL_NUM_THREADS: {np.getenv('MKL_NUM_THREADS', 'not set')}")

# Performance test
def test_mkl_performance():
# Create large arrays
 a = np.random.randn(3000, 3000)
 b = np.random.randn(3000, 3000)

# Test various operations
 start = time.time()
result1 = np.dot(a, b) # Matrix multiplication
 time1 = time.time() - start

 start = time.time()
result2 = np.linalg.svd(a) # SVD decomposition
 time2 = time.time() - start

 print(f"Matrix multiplication: {time1:.2f}s")
 print(f"SVD decomposition: {time2:.2f}s")

test_mkl_performance()
```

**OPENBLAS_NUM_THREADS - OpenBLAS Thread Control**

**Purpose:**
- Controls the number of threads for OpenBLAS library
- Alternative to Intel MKL for systems without Intel CPU
- Affects linear algebra performance

**Recommended values:**
- **For systems with Intel MKL**: Not used (MKL has priority)
- **For systems without MKL**: `OPENBLAS_NUM_THREADS=4`
- **For AMD systems**: `OPENBLAS_NUM_THREADS=2-4`

**Practical examples:**
```bash
# For systems with Intel CPU (MKL is used)
export MKL_NUM_THREADS=4
# OPENBLAS_NUM_THREADS not needed

# For systems with AMD CPU (OpenBLAS is used)
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4

# For systems without MKL
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
```

**Check which library is used:**
```python
import numpy as np

# Check which BLAS is used
print(f"NumPy BLAS info: {np.__config__.blas_opt_info}")
print(f"NumPy LAPACK info: {np.__config__.lapack_opt_info}")

# Performance test
def test_blas_performance():
# Create large matrices
 size = 2000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

# Test matrix multiplication
 start = time.time()
 result = np.dot(a, b)
 end = time.time()

 print(f"Matrix multiplication time: {end - start:.2f} seconds")
 print(f"BLAS library: {np.__config__.blas_opt_info.get('libraries', ['unknown'])[0]}")

test_blas_performance()
```

**CUDA_VISIBLE_DEVICES - GPU Device Control**

**Purpose:**
- Specifies which GPU devices to use
- Allows selecting specific GPUs
- Controls access to GPU resources

**Recommended values:**
- **Single GPU**: `CUDA_VISIBLE_DEVICES=0`
- **Multiple GPUs**: `CUDA_VISIBLE_DEVICES=0,1`
- **Disable GPU**: `CUDA_VISIBLE_DEVICES=""`
- **All GPUs**: `CUDA_VISIBLE_DEVICES=0,1,2,3`

**Practical examples:**
```bash
# Use first GPU
export CUDA_VISIBLE_DEVICES=0

# Use second GPU
export CUDA_VISIBLE_DEVICES=1

# Use two GPUs
export CUDA_VISIBLE_DEVICES=0,1

# Disable GPU (CPU only)
export CUDA_VISIBLE_DEVICES=""

# Use all available GPUs
export CUDA_VISIBLE_DEVICES=0,1,2,3
```

**Check GPU availability:**
```python
import torch

# Check CUDA availability
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")

# GPU information
if torch.cuda.is_available():
 for i in range(torch.cuda.device_count()):
 print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
 print(f"GPU {i} memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.1f} GB")

# GPU performance test
def test_gpu_performance():
 if torch.cuda.is_available():
 device = torch.device('cuda')

# Create large tensors
 size = 2000
 a = torch.randn(size, size, device=device)
 b = torch.randn(size, size, device=device)

# Test matrix multiplication on GPU
 start = time.time()
 result = torch.mm(a, b)
torch.cuda.synchronize() # Wait for completion
 end = time.time()

 print(f"GPU matrix multiplication: {end - start:.2f} seconds")
 else:
 print("GPU not available")

test_gpu_performance()
```

**AUTOGLUON_DEBUG - Debug Mode**

**Purpose:**
- Enables detailed logging of AutoML Gluon
- Helps diagnose problems
- Shows internal training processes

**Recommended values:**
- **For debugging**: `AUTOGLUON_DEBUG=1`
- **For production**: Do not set (disabled by default)
- **For development**: `AUTOGLUON_DEBUG=1`

**Practical examples:**
```bash
# Enable debugging
export AUTOGLUON_DEBUG=1

# Disable debugging
unset AUTOGLUON_DEBUG

# Temporary enable for single run
AUTOGLUON_DEBUG=1 python train_model.py
```

**What debug mode shows:**
```python
import os
os.environ['AUTOGLUON_DEBUG'] = '1'

from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Create test data
data = pd.dataFrame({
 'feature1': np.random.randn(100),
 'feature2': np.random.randn(100),
 'target': np.random.randint(0, 2, 100)
})

# Create predictor with debugging
predictor = TabularPredictor(label='target')

# Training with detailed logging
predictor.fit(data, time_limit=60)
# Will output detailed information about:
# - Algorithm selection
# - Training process
# - Model validation
# - Ensemble creation
```

**Complete environment variables configuration:**

```bash
#!/bin/bash
# Script for optimal AutoML Gluon settings

# Determine number of cores
CPU_CORES=$(nproc)
RECOMMENDED_THREADS=$((CPU_CORES - 2)) # Leave 2 cores for system

# Thread configuration
export OMP_NUM_THREADS=$RECOMMENDED_THREADS
export MKL_NUM_THREADS=$RECOMMENDED_THREADS
export OPENBLAS_NUM_THREADS=$RECOMMENDED_THREADS

# GPU configuration
if command -v nvidia-smi &> /dev/null; then
 export CUDA_VISIBLE_DEVICES=0
 echo "GPU detected, CUDA_VISIBLE_DEVICES=0"
else
 export CUDA_VISIBLE_DEVICES=""
 echo "No GPU detected, Using CPU only"
fi

# Debug mode (enable if needed)
# export AUTOGLUON_DEBUG=1

echo "Environment variables set:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "OPENBLAS_NUM_THREADS=$OPENBLAS_NUM_THREADS"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
```

**Check settings effectiveness:**

```python
import os
import time
import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor

def benchmark_environment():
"""Performance test with current settings"""

 print("=== Environment Benchmark ===")
 print(f"OMP_NUM_THREADS: {os.getenv('OMP_NUM_THREADS', 'default')}")
 print(f"MKL_NUM_THREADS: {os.getenv('MKL_NUM_THREADS', 'default')}")
 print(f"OPENBLAS_NUM_THREADS: {os.getenv('OPENBLAS_NUM_THREADS', 'default')}")
 print(f"CUDA_VISIBLE_DEVICES: {os.getenv('CUDA_VISIBLE_DEVICES', 'default')}")

# NumPy performance test
 print("\n=== NumPy Performance Test ===")
 size = 2000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

 start = time.time()
 result = np.dot(a, b)
 numpy_time = time.time() - start
 print(f"Matrix multiplication: {numpy_time:.2f} seconds")

# AutoML Gluon test
 print("\n=== AutoML Gluon Test ===")
 data = pd.dataFrame({
 'feature1': np.random.randn(1000),
 'feature2': np.random.randn(1000),
 'target': np.random.randint(0, 2, 1000)
 })

 predictor = TabularPredictor(label='target')

 start = time.time()
 predictor.fit(data, time_limit=30)
 autogluon_time = time.time() - start
 print(f"AutoML training: {autogluon_time:.2f} seconds")

 return numpy_time, autogluon_time

# Run test
benchmark_environment()
```

### 📋 Configuration File
**Why is a configuration file needed?** Because it allows you to configure AutoML Gluon for your resources and tasks without changing code.

Create file `~/.autogluon/config.yaml`:
```yaml
# AutoGluon configuration
default:
time_limit: 3600 # 1 hour by default
 memory_limit: 8 # 8GB RAM
num_cpus: 4 # Number of CPU cores
num_gpus: 1 # Number of GPUs

# Settings for different tasks
```

#### 🔧 Detailed Description of Configuration Parameters

**Parameter `time_limit`:**

- **What it means**: Maximum training time in seconds
- **Why it's needed**: Prevents infinite training, controls resources
- **Recommended values**:
- `3600` (1 hour) - for quick experiments
- `7200` (2 hours) - for medium tasks
- `14400` (4 hours) - for complex tasks
- **What happens when exceeded**: Training stops, best model is returned
- **Practical example**: If you have 2 hours for a task, set `time_limit: 7200`
- **Detailed configuration by task type**:
- **Classification (small data < 10K rows)**: `1800` (30 minutes)
- **Classification (medium data 10K-100K rows)**: `3600` (1 hour)
- **Classification (large data > 100K rows)**: `7200` (2 hours)
- **Regression (small data < 10K rows)**: `1800` (30 minutes)
- **Regression (medium data 10K-100K rows)**: `5400` (1.5 hours)
- **Regression (large data > 100K rows)**: `10800` (3 hours)
- **Time series (short series < 1K points)**: `3600` (1 hour)
- **Time series (long series > 1K points)**: `7200` (2 hours)
- **Impact on model quality**:
- **Short time (30 min)**: Basic accuracy, quick results
- **Medium time (1-2 hours)**: Good accuracy, balanced approach
- **Long time (4+ hours)**: Maximum accuracy, best models
- **Optimization by resources**:
- **CPU only**: Increase time by 2-3 times
- **GPU available**: Decrease time by 2-3 times
- **Many cores (8+)**: Decrease time by 30-50%
- **Low memory (< 8GB)**: Increase time due to limitations

**Parameter `memory_limit`:**

- **What it means**: Maximum RAM usage in gigabytes
- **Why it's needed**: Prevents memory overflow, controls resources
- **Recommended values**:
- `4` - for systems with 8GB RAM
- `8` - for systems with 16GB RAM
- `16` - for systems with 32GB RAM
- **What happens when exceeded**: Training stops with memory error
- **Practical example**: If you have 16GB RAM, set `memory_limit: 12` (leaving 4GB for system)
- **Detailed configuration by data size**:
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
- **Images**: 6-10x data size
- **Memory usage monitoring**:
 - **Check**: `import psutil; print(f"RAM usage: {psutil.virtual_memory().percent}%")`
- **Optimal usage**: 70-80% of available memory
- **Critical usage**: > 90% of available memory

**Parameter `num_cpus`:**

- **What it means**: Number of CPU cores for parallel computation
- **Why it's needed**: Speeds up training, uses all available cores
- **Recommended values**:
- `2` - for systems with 4 cores
- `4` - for systems with 8 cores
- `8` - for systems with 16+ cores
- **What happens when exceeded**: Only available number of cores is used
- **Practical example**: If you have 8 cores, set `num_cpus: 6` (leaving 2 for system)
- **Detailed configuration by task type**:
- **Classification (small data)**: `2-4` cores
- **Classification (large data)**: `4-8` cores
- **Regression (small data)**: `2-4` cores
- **Regression (large data)**: `6-12` cores
- **Time series**: `4-8` cores
- **Images**: `8-16` cores
- **Impact on training speed**:
- **1 core**: Base speed (100%)
- **2 cores**: 1.5-1.8x speedup
- **4 cores**: 2.5-3.5x speedup
- **8 cores**: 4-6x speedup
- **16+ cores**: 6-10x speedup
- **Optimization by algorithms**:
- **XGBoost**: Efficiently uses 4-8 cores
- **LightGBM**: Efficiently uses 4-12 cores
- **CatBoost**: Efficiently uses 2-8 cores
- **Neural networks**: Efficiently uses 8-16 cores
- **CPU usage monitoring**:
 - **Check**: `import psutil; print(f"CPU usage: {psutil.cpu_percent()}%")`
- **Optimal usage**: 80-90% of available cores
- **Overload**: > 95% of available cores

**Parameter `num_gpus`:**

- **What it means**: Number of GPUs for training acceleration
- **Why it's needed**: Speeds up neural network training by 10-100 times
- **Recommended values**:
- `0` - if no GPU or for CPU-only tasks
- `1` - for single GPU
- `2+` - for multiple GPUs (requires special settings)
- **What happens with incorrect value**: AutoML Gluon automatically detects available GPUs
- **Practical example**: If you have RTX 3070, set `num_gpus: 1`
- **Detailed configuration by GPU type**:
- **No GPU**: `num_gpus: 0` - training on CPU only
- **GTX 1060 6GB**: `num_gpus: 1` - basic GPU support
- **RTX 3070 8GB**: `num_gpus: 1` - good performance
- **RTX 4080 16GB**: `num_gpus: 1` - high performance
- **A100 40GB**: `num_gpus: 1` - professional operation
- **Multiple GPUs**: `num_gpus: 2+` - for large models
- **Impact on training speed**:
- **CPU only**: Base speed (100%)
- **GTX 1060**: 3-5x speedup
- **RTX 3070**: 8-15x speedup
- **RTX 4080**: 15-25x speedup
- **A100**: 25-50x speedup
- **Optimization by task type**:
- **Classification (tabular data)**: GPU not critical
- **Regression (tabular data)**: GPU not critical
- **Time series**: GPU speeds up by 2-5 times
- **Images**: GPU critical, 10-50x speedup
- **Text**: GPU speeds up by 5-20 times
- **GPU memory requirements**:
- **Small models (< 1M parameters)**: 2-4 GB VRAM
- **Medium models (1-10M parameters)**: 4-8 GB VRAM
- **Large models (10-100M parameters)**: 8-16 GB VRAM
- **Very large models (> 100M parameters)**: 16+ GB VRAM
- **Check GPU availability**:
 - **Check CUDA**: `python -c "import torch; print(torch.cuda.is_available())"`
- **GPU count**: `python -c "import torch; print(torch.cuda.device_count())"`
- **GPU information**: `python -c "import torch; print(torch.cuda.get_device_name(0))"`
tabular:
 presets: ['best_quality', 'high_quality', 'good_quality', 'medium_quality', 'optimize_for_deployment']
 hyperparameter_tune_kwargs:
 num_trials: 10
 scheduler: 'local'
 searcher: 'auto'

timeseries:
 Prediction_length: 24
 freq: 'H'
 target_column: 'target'
```

#### 🎯 Detailed Description of Parameters for Tabular Data

**Parameter `presets`:**

- **What it means**: Pre-configured model quality settings
- **Why it's needed**: Simplifies choice between speed and quality
- **Detailed description of each preset**: **`best_quality`:**
- **What it does**: Maximum model quality
- **Training time**: 4-8 hours
- **Uses**: All available algorithms, ensembles, hyperparameter tuning
- **When to use**: For production, when quality is critical
- **Result**: Best accuracy, but long training time

 **`high_quality`:**
- **What it does**: High quality with reasonable time
- **Training time**: 2-4 hours
- **Uses**: Main algorithms + ensembles
- **When to use**: For most tasks
- **Result**: Good accuracy in reasonable time

 **`good_quality`:**
- **What it does**: Good quality in short time
- **Training time**: 30-60 minutes
- **Uses**: Main algorithms without ensembles
- **When to use**: For quick experiments
- **Result**: Acceptable accuracy quickly

 **`medium_quality`:**
- **What it does**: Medium quality in very short time
- **Training time**: 10-30 minutes
- **Uses**: Only fast algorithms
- **When to use**: For prototyping
- **Result**: Basic accuracy very quickly

 **`optimize_for_deployment`:**
- **What it does**: Optimization for production
- **Training time**: 1-2 hours
- **Uses**: Fast algorithms with optimization
- **When to use**: For production with resource constraints
- **Result**: Fast predictions, good accuracy

**Parameter `num_trials`:**

- **What it means**: Number of hyperparameter tuning attempts
- **Why it's needed**: More attempts = better quality, but longer time
- **Recommended values**:
- `5` - for quick experiments
- `10` - for standard tasks
- `20` - for important tasks
- `50+` - for maximum quality
- **Practical example**: If you have 2 hours, set `num_trials: 10`

**Parameter `scheduler`:**

- **What it means**: Task distribution scheduler
- **Why it's needed**: Manages parallel execution
- **Available values**:
- `'local'` - local execution (by default)
- `'ray'` - distributed execution via Ray
- `'dask'` - distributed execution via Dask
- **Practical example**: For single computer use `'local'`

#### ⏰ Detailed Description of Parameters for Time Series

**Parameter `Prediction_length`:**

- **What it means**: Number of future points for forecasting
- **Why it's needed**: Defines forecasting horizon
- **Recommended values**:
- `24` - for hourly data (forecast for 1 day)
- `7` - for daily data (forecast for 1 week)
- `30` - for daily data (forecast for 1 month)
- **Practical example**: For sales forecast for 1 week set `Prediction_length: 7`

**Parameter `freq`:**

- **What it means**: Time series frequency
- **Why it's needed**: Defines interval between points
- **Available values**:
- `'H'` - hourly data
- `'D'` - daily data
- `'W'` - weekly data
- `'M'` - monthly data
- **Practical example**: For daily sales set `freq: 'D'`

**Parameter `target_column`:**

- **What it means**: Name of column with target variable
- **Why it's needed**: Specifies what to predict
- **Practical example**: If you have column 'sales', set `target_column: 'sales'`
```

## Troubleshooting Installation Issues

### Issues with Dependencies
```bash
# Clean pip cache
pip cache purge

# Reinstall ignoring cache
pip install --no-cache-dir autogluon

# Install specific version
pip install autogluon==0.8.2
```

### Issues with CUDA
```bash
# Check CUDA version
nvidia-smi

# Check PyTorch compatibility
python -c "import torch; print(torch.cuda.is_available())"

# Install compatible PyTorch version
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
```

### Issues with Memory
```bash
# Install with memory limit
pip install --no-cache-dir --no-deps autogluon
pip install -r requirements.txt
```

## Functionality Check

### Complete Installation Test
```python
import autogluon as ag
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

def test_installation():
"""Complete AutoGluon installation test"""

# Create test data
 np.random.seed(42)
 n_samples = 1000
 data = pd.dataFrame({
 'feature1': np.random.randn(n_samples),
 'feature2': np.random.randn(n_samples),
 'feature3': np.random.randn(n_samples),
 'target': np.random.randint(0, 2, n_samples)
 })

# Split into train/test
 train_data = data[:800]
 test_data = data[800:]

# Create and train model
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
 )

# Training with time limit
 predictor.fit(
 train_data,
time_limit=60, # 1 minute
 presets='medium_quality'
 )

# Predictions
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

 print(f"Model performance: {performance}")
 print("Installation test completed successfully!")

 return True

if __name__ == "__main__":
 test_installation()
```

## 🚀 Production Architecture

<img src="images/optimized/production_architecture.png" alt="Production architecture" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 8: AutoML Gluon deployment architecture in production*

**Why is it important to understand production architecture?** Because it helps properly plan deployment:

- **Model**: Trained AutoML Gluon model
- **API Gateway**: Entry point for requests
- **Load Balancer**: Load distribution between instances
- **Monitoring**: Performance and quality monitoring
- **Scaling**: Automatic scaling under load
- **Data Pipeline**: Data flow for retraining

### 📊 Production Solutions Comparison

<img src="images/optimized/production_comparison.png" alt="Production solutions comparison" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 9: Comparison of different deployment approaches*

**Why is it important to compare solutions?** Because different tasks require different approaches:

- **Batch Processing**: Data processing in batches (for large volumes)
- **Real-time API**: Instant predictions (for interactive applications)
- **Edge deployment**: Deployment on edge devices
- **Cloud deployment**: Deployment in cloud (scalability)
- **Hybrid Approach**: Combined approach (flexibility)

## Next Steps

After successful installation, proceed to:
- [Basic Usage](./02_basic_usage.md)
- [Advanced Configuration](./03_advanced_configuration.md)
- [Working with Metrics](./04_metrics.md)

## Useful Links

- [Official Documentation](https://auto.gluon.ai/)
- [GitHub Repository](https://github.com/autogluon/autogluon)
- [Usage Examples](https://github.com/autogluon/autogluon/tree/master/examples)
- [Community Forum](https://discuss.autogluon.ai/)
