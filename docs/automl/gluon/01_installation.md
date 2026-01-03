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

<img src="images/optimized/architecture_diagram.png" alt="Архитектура AutoML Gluon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
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

<img src="images/optimized/performance_comparison.png" alt="Сравнение производительности" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 3: Comparison of AutoML Gluon performance on different configurations*

**Why is it important to understand performance?** BecaUse it helps to choose the optimal configuration for your tasks:

- **CPU vs GPU**: GPU speeds up learning in 10-100 times for neural networks
- **Memory**: More RAM = ability to handle large datasets
- **Cores**: More cores = parallel training of several models
- ** Training time **: from 10 minutes to several hours in dependencies from configuration

### Model Quality 🎯 Metrics

<img src="images/optimized/metrics_comparison.png" alt="Сравнение метрик" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
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

<img src="images/optimized/retraining_workflow.png" alt="Рабочий процесс переобучения" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
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

<img src="images/optimized/validation_methods.png" alt="Методы валидации" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Figure 6: Various model validation methods *

**Why is validation important?** BecaUse it ensures the reliability and quality of models:

- **Holdout Validation**: Simple separation on train/test (70/30)
- **Cross-Validation**: K-fold cross-validation for more reliable evaluation
- **Time Series Split**: Special validation for time series
- **Stratified Split**: Saving class proportions when splitting
- **Walk-Forward Analysis**: Sliding window for time series

### Troubleshooting 🔧 Diagram

<img src="images/optimized/Troubleshooting_flowchart.png" alt="Диаграмма устранения проблем" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
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
- **Оптимизация**: Автоматическая оптимизация градиентов
- **integration**: Хорошо Workingет with GluonTS

**Практические examples использования:**
```python
import mxnet as mx
from mxnet import gluon, autograd
import numpy as np

# create LSTM модели for временных рядов
class LSTMPredictor(gluon.Block):
 def __init__(self, hidden_size, output_size):
 super(LSTMPredictor, self).__init__()
 self.lstm = gluon.rnn.LSTM(hidden_size)
 self.dense = gluon.nn.Dense(output_size)

 def forward(self, x):
 output = self.lstm(x)
 return self.dense(output[-1])

# Обучение модели
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

**Statsmodels - Статистические модели for временных рядов**

**Назначение:**
- Классические статистические модели
- Анализ временных рядов
- Тестирование стационарности
- Сезонная декомпозиция

**Возможности:**
- **ARIMA/SARIMA**: Классические модели авторегрессии
- **ETS**: Exponential Smoothing модели
- **Сезонная декомпозиция**: STL, X-13ARIMA-SEATS
- **Тестирование**: ADF, KPSS тесты стационарности
- **Диагностика**: ACF, PACF, Ljung-Box тесты

**Практические examples использования:**
```python
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

# Анализ стационарности
def check_stationarity(timeseries):
 result = adfuller(timeseries)
 print(f'ADF Statistic: {result[0]}')
 print(f'p-value: {result[1]}')
 return result[1] < 0.05

# Сезонная декомпозиция
decomposition = seasonal_decompose(timeseries, model='additive')
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# ARIMA модель
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

**Сравнение библиотек for временных рядов:**

| Библиотека | Тип моделей | Сложность | Производительность | Точность |
|------------|-------------|-----------|-------------------|----------|
| **GluonTS** | Deep Learning | Высокая | Очень высокая | Очень высокая |
| **MXNet** | Custom Deep Learning | Очень высокая | Высокая | Высокая |
| **Statsmodels** | Statistical | Низкая | Средняя | Средняя |

**Рекомендации on выбору:**

**Use GluonTS если:**
- Нужны современные deep learning модели
- Workingете with большими объемами данных
- Нужны квантильные прогнозы
- Требуется высокая точность

**Use MXNet если:**
- Нужны кастомные архитектуры
- Требуется максимальная гибкость
- Workingете with GPU
- Нужно распределенное обучение

**Use Statsmodels если:**
- Нужны классические статистические модели
- Требуется интерпретируемость
- Workingете with малыми данными
- Нужен детальный анализ

**integration with AutoML Gluon for временных рядов:**

```python
from autogluon.timeseries import TimeSeriesPredictor
import pandas as pd

# Подготовка данных
train_data = pd.dataFrame({
 'timestamp': pd.date_range('2020-01-01', periods=1000, freq='H'),
 'target': np.random.randn(1000).cumsum(),
 'feature1': np.random.randn(1000),
 'feature2': np.random.randn(1000)
})

# create предиктора
predictor = TimeSeriesPredictor(
 target="target",
 Prediction_length=24, # Прогноз on 24 часа
 freq="H", # Почасовые data
 eval_metric="MAPE"
)

# Обучение with различными моделями
predictor.fit(
 train_data,
 time_limit=3600, # 1 час
 presets="best_quality" # Лучшее качество
)

# Прогнозирование
predictions = predictor.predict(train_data)
print(f"predictions shape: {predictions.shape}")

# Оценка качества
performance = predictor.evaluate(train_data)
print(f"Model performance: {performance}")
```

## configuration окружения

### Переменные окружения
```bash
# installation переменных for оптимизации производительности
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4

# for GPU
export CUDA_VISIBLE_DEVICES=0

# for отладки
export AUTOGLUON_DEBUG=1
```

#### 🔧 Детальное describe переменных окружения

**OMP_NUM_THREADS - Контроль OpenMP потоков**

**Назначение:**
- Контролирует количество потоков for OpenMP операций
- Влияет on производительность numpy, scipy, scikit-learn
- Оптимизирует использование CPU ядер

**Рекомендуемые значения:**
- **2-4 ядра**: `OMP_NUM_THREADS=2`
- **4-8 ядер**: `OMP_NUM_THREADS=4`
- **8+ ядер**: `OMP_NUM_THREADS=6-8`

**Практические examples:**
```bash
# for системы with 8 ядрами
export OMP_NUM_THREADS=6 # Оставляем 2 ядра for системы

# for системы with 4 ядрами
export OMP_NUM_THREADS=3 # Оставляем 1 ядро for системы

# for системы with 16 ядрами
export OMP_NUM_THREADS=12 # Оставляем 4 ядра for системы
```

**Влияние on производительность:**
- **Слишком мало потоков**: Недоиспользование CPU
- **Слишком много потоков**: Конкуренция за ресурсы, снижение производительности
- **Оптимальное значение**: 70-80% from доступных ядер

**check эффективности:**
```python
import numpy as np
import time

# Тест производительности with разным количеством потоков
def test_omp_performance():
 # create большой матрицы
 size = 5000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

 # Измерение времени умножения матриц
 start_time = time.time()
 result = np.dot(a, b)
 end_time = time.time()

 print(f"Matrix multiplication time: {end_time - start_time:.2f} seconds")
 print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'default')}")

# Launch теста
test_omp_performance()
```

**MKL_NUM_THREADS - Контроль Intel MKL потоков**

**Назначение:**
- Контролирует количество потоков for Intel Math Kernel Library
- Влияет on производительность numpy, scipy, pandas
- Оптимизирует математические операции

**Рекомендуемые значения:**
- **Должно быть равно OMP_NUM_THREADS**: `MKL_NUM_THREADS=4`
- **for избежания конфликтов**: not должно превышать OMP_NUM_THREADS
- **for максимальной производительности**: Равно количеству физических ядер

**Практические examples:**
```bash
# Synchronization with OMP_NUM_THREADS
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4

# for систем with Intel CPU
export MKL_NUM_THREADS=4 # Use 4 ядра

# for систем with AMD CPU
export MKL_NUM_THREADS=2 # Меньше потоков for AMD
```

**Влияние on производительность:**
- **Synchronization with OMP**: Предотвращает перегрузку системы
- **Оптимизация MKL**: Максимальная производительность математических операций
- **Избежание конфликтов**: Предотвращает конкуренцию за ресурсы

**check Settings:**
```python
import numpy as np

# check текущих настроек
print(f"OMP_NUM_THREADS: {np.getenv('OMP_NUM_THREADS', 'not set')}")
print(f"MKL_NUM_THREADS: {np.getenv('MKL_NUM_THREADS', 'not set')}")

# Тест производительности
def test_mkl_performance():
 # create больших массивов
 a = np.random.randn(3000, 3000)
 b = np.random.randn(3000, 3000)

 # Тест различных операций
 start = time.time()
 result1 = np.dot(a, b) # Матричное умножение
 time1 = time.time() - start

 start = time.time()
 result2 = np.linalg.svd(a) # SVD разложение
 time2 = time.time() - start

 print(f"Matrix multiplication: {time1:.2f}s")
 print(f"SVD decomposition: {time2:.2f}s")

test_mkl_performance()
```

**OPENBLAS_NUM_THREADS - Контроль OpenBLAS потоков**

**Назначение:**
- Контролирует количество потоков for OpenBLAS библиотеки
- Альтернатива Intel MKL for систем без Intel CPU
- Влияет on производительность линейной алгебры

**Рекомендуемые значения:**
- **for систем with Intel MKL**: not используется (MKL имеет приоритет)
- **for систем без MKL**: `OPENBLAS_NUM_THREADS=4`
- **for AMD систем**: `OPENBLAS_NUM_THREADS=2-4`

**Практические examples:**
```bash
# for систем with Intel CPU (используется MKL)
export MKL_NUM_THREADS=4
# OPENBLAS_NUM_THREADS not нужен

# for систем with AMD CPU (используется OpenBLAS)
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4

# for систем без MKL
export OPENBLAS_NUM_THREADS=4
export OMP_NUM_THREADS=4
```

**check Useой библиотеки:**
```python
import numpy as np

# check какой BLAS используется
print(f"NumPy BLAS info: {np.__config__.blas_opt_info}")
print(f"NumPy LAPACK info: {np.__config__.lapack_opt_info}")

# Тест производительности
def test_blas_performance():
 # create больших матриц
 size = 2000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

 # Тест матричного умножения
 start = time.time()
 result = np.dot(a, b)
 end = time.time()

 print(f"Matrix multiplication time: {end - start:.2f} seconds")
 print(f"BLAS library: {np.__config__.blas_opt_info.get('libraries', ['unknown'])[0]}")

test_blas_performance()
```

**CUDA_VISIBLE_DEVICES - Контроль GPU устройств**

**Назначение:**
- Указывает What GPU устройства использовать
- Позволяет выбирать конкретные GPU
- Контролирует доступ к GPU ресурсам

**Рекомендуемые значения:**
- **Одна GPU**: `CUDA_VISIBLE_DEVICES=0`
- **Несколько GPU**: `CUDA_VISIBLE_DEVICES=0,1`
- **Отключить GPU**: `CUDA_VISIBLE_DEVICES=""`
- **Все GPU**: `CUDA_VISIBLE_DEVICES=0,1,2,3`

**Практические examples:**
```bash
# Использование первой GPU
export CUDA_VISIBLE_DEVICES=0

# Использование второй GPU
export CUDA_VISIBLE_DEVICES=1

# Использование двух GPU
export CUDA_VISIBLE_DEVICES=0,1

# Отключение GPU (только CPU)
export CUDA_VISIBLE_DEVICES=""

# Использование all доступных GPU
export CUDA_VISIBLE_DEVICES=0,1,2,3
```

**check GPU доступности:**
```python
import torch

# check доступности CUDA
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")

# Информация о GPU
if torch.cuda.is_available():
 for i in range(torch.cuda.device_count()):
 print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
 print(f"GPU {i} memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.1f} GB")

# Тест производительности GPU
def test_gpu_performance():
 if torch.cuda.is_available():
 device = torch.device('cuda')

 # create больших тензоров
 size = 2000
 a = torch.randn(size, size, device=device)
 b = torch.randn(size, size, device=device)

 # Тест матричного умножения on GPU
 start = time.time()
 result = torch.mm(a, b)
 torch.cuda.synchronize() # Ждем завершения
 end = time.time()

 print(f"GPU matrix multiplication: {end - start:.2f} seconds")
 else:
 print("GPU not available")

test_gpu_performance()
```

**AUTOGLUON_DEBUG - Режим отладки**

**Назначение:**
- Включает детальное Logsрование AutoML Gluon
- Помогает диагностировать проблемы
- Показывает внутренние процессы обучения

**Рекомендуемые значения:**
- **for отладки**: `AUTOGLUON_DEBUG=1`
- **for продакшена**: not устанавливать (on умолчанию выключен)
- **for development**: `AUTOGLUON_DEBUG=1`

**Практические examples:**
```bash
# Включение отладки
export AUTOGLUON_DEBUG=1

# Отключение отладки
unset AUTOGLUON_DEBUG

# Временное включение for одного Launchа
AUTOGLUON_DEBUG=1 python train_model.py
```

**Что показывает отладочный режим:**
```python
import os
os.environ['AUTOGLUON_DEBUG'] = '1'

from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# create testsых данных
data = pd.dataFrame({
 'feature1': np.random.randn(100),
 'feature2': np.random.randn(100),
 'target': np.random.randint(0, 2, 100)
})

# create предиктора with debugging
predictor = TabularPredictor(label='target')

# Обучение with детальным Logsрованием
predictor.fit(data, time_limit=60)
# Выведет детальную информацию о:
# - Выборе алгоритмов
# - Процессе обучения
# - Валидации моделей
# - Создании ансамблей
```

**Полная configuration переменных окружения:**

```bash
#!/bin/bash
# Скрипт for оптимальной Settings AutoML Gluon

# Определение количества ядер
CPU_CORES=$(nproc)
RECOMMENDED_THREADS=$((CPU_CORES - 2)) # Оставляем 2 ядра for системы

# configuration потоков
export OMP_NUM_THREADS=$RECOMMENDED_THREADS
export MKL_NUM_THREADS=$RECOMMENDED_THREADS
export OPENBLAS_NUM_THREADS=$RECOMMENDED_THREADS

# configuration GPU
if command -v nvidia-smi &> /dev/null; then
 export CUDA_VISIBLE_DEVICES=0
 echo "GPU detected, CUDA_VISIBLE_DEVICES=0"
else
 export CUDA_VISIBLE_DEVICES=""
 echo "No GPU detected, Using CPU only"
fi

# Отладочный режим (включить при необходимости)
# export AUTOGLUON_DEBUG=1

echo "Environment variables set:"
echo "OMP_NUM_THREADS=$OMP_NUM_THREADS"
echo "MKL_NUM_THREADS=$MKL_NUM_THREADS"
echo "OPENBLAS_NUM_THREADS=$OPENBLAS_NUM_THREADS"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
```

**check эффективности настроек:**

```python
import os
import time
import numpy as np
import pandas as pd
from autogluon.tabular import TabularPredictor

def benchmark_environment():
 """Тест производительности with текущими настройками"""

 print("=== Environment Benchmark ===")
 print(f"OMP_NUM_THREADS: {os.getenv('OMP_NUM_THREADS', 'default')}")
 print(f"MKL_NUM_THREADS: {os.getenv('MKL_NUM_THREADS', 'default')}")
 print(f"OPENBLAS_NUM_THREADS: {os.getenv('OPENBLAS_NUM_THREADS', 'default')}")
 print(f"CUDA_VISIBLE_DEVICES: {os.getenv('CUDA_VISIBLE_DEVICES', 'default')}")

 # Тест NumPy производительности
 print("\n=== NumPy Performance Test ===")
 size = 2000
 a = np.random.randn(size, size)
 b = np.random.randn(size, size)

 start = time.time()
 result = np.dot(a, b)
 numpy_time = time.time() - start
 print(f"Matrix multiplication: {numpy_time:.2f} seconds")

 # Тест AutoML Gluon
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

# Launch теста
benchmark_environment()
```

### 📋 Конфигурационный файл
**Почему нужен конфигурационный файл?** Потому что он позволяет настроить AutoML Gluon под ваши ресурсы and задачи без изменения кода.

Создайте файл `~/.autogluon/config.yaml`:
```yaml
# configuration AutoGluon
default:
 time_limit: 3600 # 1 час on умолчанию
 memory_limit: 8 # 8GB RAM
 num_cpus: 4 # Количество CPU ядер
 num_gpus: 1 # Количество GPU

# Settings for different tasks
```

#### 🔧 Детальное describe параметров конфигурации

**parameter `time_limit`:**

- **Что означает**: Максимальное время обучения in секундах
- **Зачем нужен**: Предотвращает бесконечное обучение, контролирует ресурсы
- **Рекомендуемые значения**:
 - `3600` (1 час) - for быстрых экспериментов
 - `7200` (2 часа) - for средних задач
 - `14400` (4 часа) - for сложных задач
- **Что происходит при превышении**: Обучение останавливается, возвращается лучшая модель
- **Практический example**: Если у вас есть 2 часа on задачу, install `time_limit: 7200`
- **Детальная configuration on типам задач**:
 - **Классификация (малые data < 10K строк)**: `1800` (30 minutes)
- **Классификация (средние data 10K-100K строк)**: `3600` (1 час)
- **Классификация (большие data > 100K строк)**: `7200` (2 часа)
- **Регрессия (малые data < 10K строк)**: `1800` (30 minutes)
- **Регрессия (средние data 10K-100K строк)**: `5400` (1.5 часа)
- **Регрессия (большие data > 100K строк)**: `10800` (3 часа)
- **Временные ряды (короткие серии < 1K точек)**: `3600` (1 час)
- **Временные ряды (длинные серии > 1K точек)**: `7200` (2 часа)
- **Влияние on качество модели**:
 - **Короткое время (30 мин)**: Базовая точность, быстрые результаты
- **Среднее время (1-2 часа)**: Хорошая точность, сбалансированный подход
- **Длинное время (4+ часов)**: Максимальная точность, лучшие модели
- **Оптимизация on ресурсам**:
 - **CPU только**: Увеличить время in 2-3 раза
- **GPU доступна**: Уменьшить время in 2-3 раза
- **Много ядер (8+)**: Уменьшить время on 30-50%
- **Мало памяти (< 8GB)**: Увеличить время из-за ограничений

**parameter `memory_limit`:**

- **Что означает**: Максимальное использование RAM in гигабайтах
- **Зачем нужен**: Предотвращает переполнение памяти, контролирует ресурсы
- **Рекомендуемые значения**:
 - `4` - for систем with 8GB RAM
 - `8` - for систем with 16GB RAM
 - `16` - for систем with 32GB RAM
- **Что происходит при превышении**: Обучение останавливается with ошибкой памяти
- **Практический example**: Если у вас 16GB RAM, install `memory_limit: 12` (оставляя 4GB for системы)
- **Детальная configuration on размеру данных**:
 - **Малые data (< 1MB)**: `2-4` GB
- **Средние data (1-100MB)**: `4-8` GB
- **Большие data (100MB-1GB)**: `8-16` GB
- **Очень большие data (> 1GB)**: `16-32` GB
- **Влияние on производительность**:
 - **Мало памяти**: Медленная Working, возможные ошибки
- **Достаточно памяти**: Быстрая Working, стабильность
- **Много памяти**: Максимальная скорость, обработка больших данных
- **Оптимизация on типу задач**:
 - **Классификация**: 2-4x размер данных
- **Регрессия**: 3-5x размер данных
- **Временные ряды**: 4-6x размер данных
- **Изображения**: 6-10x размер данных
- **Monitoring использования памяти**:
 - **check**: `import psutil; print(f"RAM usage: {psutil.virtual_memory().percent}%")`
- **Оптимальное использование**: 70-80% from доступной памяти
- **Критическое использование**: > 90% from доступной памяти

**parameter `num_cpus`:**

- **Что означает**: Количество CPU ядер for параллельных вычислений
- **Зачем нужен**: Ускоряет обучение, использует все доступные ядра
- **Рекомендуемые значения**:
 - `2` - for систем with 4 ядрами
 - `4` - for систем with 8 ядрами
 - `8` - for систем with 16+ ядрами
- **Что происходит при превышении**: Используется только доступное количество ядер
- **Практический example**: Если у вас 8 ядер, install `num_cpus: 6` (оставляя 2 for системы)
- **Детальная configuration on типам задач**:
 - **Классификация (малые data)**: `2-4` ядра
- **Классификация (большие data)**: `4-8` ядер
- **Регрессия (малые data)**: `2-4` ядра
- **Регрессия (большие data)**: `6-12` ядер
- **Временные ряды**: `4-8` ядер
- **Изображения**: `8-16` ядер
- **Влияние on скорость обучения**:
 - **1 ядро**: Базовая скорость (100%)
- **2 ядра**: Ускорение in 1.5-1.8 раза
- **4 ядра**: Ускорение in 2.5-3.5 раза
- **8 ядер**: Ускорение in 4-6 раз
- **16+ ядер**: Ускорение in 6-10 раз
- **Оптимизация on алгоритмам**:
 - **XGBoost**: Эффективно использует 4-8 ядер
- **LightGBM**: Эффективно использует 4-12 ядер
- **CatBoost**: Эффективно использует 2-8 ядер
- **Neural networks**: Эффективно использует 8-16 ядер
- **Monitoring использования CPU**:
 - **check**: `import psutil; print(f"CPU usage: {psutil.cpu_percent()}%")`
- **Оптимальное использование**: 80-90% from доступных ядер
- **Перегрузка**: > 95% from доступных ядер

**parameter `num_gpus`:**

- **Что означает**: Количество GPU for acceleration обучения
- **Зачем нужен**: Ускоряет обучение нейронных networks in 10-100 раз
- **Рекомендуемые значения**:
 - `0` - если нет GPU or for CPU-only задач
 - `1` - for одной GPU
 - `2+` - for нескольких GPU (требует специальной Settings)
- **Что происходит при неправильном значении**: AutoML Gluon автоматически определяет доступные GPU
- **Практический example**: Если у вас RTX 3070, install `num_gpus: 1`
- **Детальная configuration on типам GPU**:
 - **Нет GPU**: `num_gpus: 0` - обучение только on CPU
- **GTX 1060 6GB**: `num_gpus: 1` - базовая поддержка GPU
- **RTX 3070 8GB**: `num_gpus: 1` - хорошая производительность
- **RTX 4080 16GB**: `num_gpus: 1` - высокая производительность
- **A100 40GB**: `num_gpus: 1` - профессиональная Working
- **Несколько GPU**: `num_gpus: 2+` - for large models
- **Влияние on скорость обучения**:
 - **CPU только**: Базовая скорость (100%)
- **GTX 1060**: Ускорение by 3-5 times
- **RTX 3070**: Ускорение in 8-15 раз
- **RTX 4080**: Ускорение in 15-25 раз
- **A100**: Ускорение in 25-50 раз
- **Оптимизация on типам задач**:
 - **Классификация (табличные data)**: GPU not критична
- **Регрессия (табличные data)**: GPU not критична
- **Временные ряды**: GPU ускоряет in 2-5 раз
- **Изображения**: GPU критична, ускорение in 10-50 раз
- **Текст**: GPU ускоряет in 5-20 раз
- **Требования to memory GPU**:
 - **Малые модели (< 1M параметров)**: 2-4 GB VRAM
- **Средние модели (1-10M параметров)**: 4-8 GB VRAM
- **Большие модели (10-100M параметров)**: 8-16 GB VRAM
- **Очень большие модели (> 100M параметров)**: 16+ GB VRAM
- **check доступности GPU**:
 - **check CUDA**: `python -c "import torch; print(torch.cuda.is_available())"`
- **Количество GPU**: `python -c "import torch; print(torch.cuda.device_count())"`
- **Информация о GPU**: `python -c "import torch; print(torch.cuda.get_device_name(0))"`
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

#### 🎯 Детальное describe параметров for табличных данных

**parameter `presets`:**

- **Что означает**: Предустановленные конфигурации качества модели
- **Зачем нужен**: Упрощает выбор между скоростью and качеством
- **Детальное describe каждого preset**: **`best_quality`:**
- **Что делает**: Максимальное качество модели
- **Время обучения**: 4-8 часов
- **Использует**: Все доступные алгоритмы, ансамбли, тюнинг гиперпараметров
- **Когда использовать**: for продакшена, когда качество критично
- **Результат**: Лучшая точность, но долгое обучение

 **`high_quality`:**
- **Что делает**: Высокое качество with разумным временем
- **Время обучения**: 2-4 часа
- **Использует**: Основные алгоритмы + ансамбли
- **Когда использовать**: for большинства задач
- **Результат**: Хорошая точность за разумное время

 **`good_quality`:**
- **Что делает**: Хорошее качество за короткое время
- **Время обучения**: 30-60 minutes
- **Использует**: Основные алгоритмы без ансамблей
- **Когда использовать**: for быстрых экспериментов
- **Результат**: Приемлемая точность быстро

 **`medium_quality`:**
- **Что делает**: Среднее качество за очень короткое время
- **Время обучения**: 10-30 minutes
- **Использует**: Только быстрые алгоритмы
- **Когда использовать**: for прототипирования
- **Результат**: Базовая точность очень быстро

 **`optimize_for_deployment`:**
- **Что делает**: Оптимизация for продакшена
- **Время обучения**: 1-2 часа
- **Использует**: Быстрые алгоритмы with оптимизацией
- **Когда использовать**: for продакшена with ограничениями ресурсов
- **Результат**: Быстрые предсказания, хорошая точность

**parameter `num_trials`:**

- **Что означает**: Количество попыток тюнинга гиперпараметров
- **Зачем нужен**: Больше попыток = лучше качество, но дольше время
- **Рекомендуемые значения**:
 - `5` - for быстрых экспериментов
 - `10` - for стандартных задач
 - `20` - for важных задач
 - `50+` - for максимального качества
- **Практический example**: Если у вас есть 2 часа, install `num_trials: 10`

**parameter `scheduler`:**

- **Что означает**: Planировщик for распределения задач
- **Зачем нужен**: Управляет параллельным выполнением
- **Доступные значения**:
 - `'local'` - локальное выполнение (on умолчанию)
 - `'ray'` - распределенное выполнение через Ray
 - `'dask'` - распределенное выполнение через Dask
- **Практический example**: for одного компьютера Use `'local'`

#### ⏰ Детальное describe параметров for временных рядов

**parameter `Prediction_length`:**

- **Что означает**: Количество будущих точек for прогнозирования
- **Зачем нужен**: Определяет горизонт прогнозирования
- **Рекомендуемые значения**:
 - `24` - for почасовых данных (прогноз on сутки)
 - `7` - for дневных данных (прогноз on неделю)
 - `30` - for дневных данных (прогноз on месяц)
- **Практический example**: for прогноза продаж on неделю install `Prediction_length: 7`

**parameter `freq`:**

- **Что означает**: Частота временного ряда
- **Зачем нужен**: Определяет интервал между точками
- **Доступные значения**:
 - `'H'` - почасовые data
 - `'D'` - дневные data
 - `'W'` - недельные data
 - `'M'` - месячные data
- **Практический example**: for дневных продаж install `freq: 'D'`

**parameter `target_column`:**

- **Что означает**: Название столбца with целевой переменной
- **Зачем нужен**: Указывает, что предсказывать
- **Практический example**: Если у вас есть столбец 'sales', install `target_column: 'sales'`
```

## Устранение проблем при установке

### Issues with зависимостями
```bash
# clean cache pip
pip cache purge

# reinstall with игнорированием cache
pip install --no-cache-dir autogluon

# installation конкретной версии
pip install autogluon==0.8.2
```

### Issues with CUDA
```bash
# check версии CUDA
nvidia-smi

# check совместимости PyTorch
python -c "import torch; print(torch.cuda.is_available())"

# installation совместимой версии PyTorch
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 --extra-index-url https://download.pytorch.org/whl/cu117
```

### Issues with памятью
```bash
# installation with ограничением памяти
pip install --no-cache-dir --no-deps autogluon
pip install -r requirements.txt
```

## check работоспособности

### Полный тест installation
```python
import autogluon as ag
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

def test_installation():
 """Полный тест installation AutoGluon"""

 # create testsых данных
 np.random.seed(42)
 n_samples = 1000
 data = pd.dataFrame({
 'feature1': np.random.randn(n_samples),
 'feature2': np.random.randn(n_samples),
 'feature3': np.random.randn(n_samples),
 'target': np.random.randint(0, 2, n_samples)
 })

 # Разделение on train/test
 train_data = data[:800]
 test_data = data[800:]

 # create and обучение модели
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
 )

 # Обучение with ограничением времени
 predictor.fit(
 train_data,
 time_limit=60, # 1 minutesа
 presets='medium_quality'
 )

 # Предсказания
 predictions = predictor.predict(test_data)

 # Оценка качества
 performance = predictor.evaluate(test_data)

 print(f"Model performance: {performance}")
 print("installation test COMPLETED successfully!")

 return True

if __name__ == "__main__":
 test_installation()
```

## 🚀 Архитектура продакшена

<img src="images/optimized/production_architecture.png" alt="Архитектура продакшена" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 8: Архитектура deployment AutoML Gluon in продакшене*

**Почему важно понимать архитектуру продакшена?** Потому что это помогает правильно сPlanировать развертывание:

- **Модель**: Обученная модель AutoML Gluon
- **API Gateway**: Точка входа for запросов
- **Load Balancer**: Распределение нагрузки между инстансами
- **Monitoring**: Monitoring производительности and качества
- **Scaling**: Автоматическое масштабирование под нагрузку
- **data Pipeline**: Поток данных for переобучения

### 📊 Сравнение продакшен решений

<img src="images/optimized/production_comparison.png" alt="Сравнение продакшен решений" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 9: Сравнение различных подходов к deployment*

**Почему важно сравнивать решения?** Потому что разные задачи требуют разных подходов:

- **Batch Processing**: Обработка данных пакетами (for больших объемов)
- **Real-time API**: Мгновенные предсказания (for интерактивных приложений)
- **Edge deployment**: Развертывание on периферийных устройствах
- **Cloud deployment**: Развертывание in облаке (масштабируемость)
- **Hybrid Approach**: Комбинированный подход (гибкость)

## Следующие шаги

После успешной installation переходите к:
- [Базовому использованию](./02_basic_usage.md)
- [Продвинутой конфигурации](./03_advanced_configuration.md)
- [Работе with метриками](./04_metrics.md)

## Полезные ссылки

- [Официальная documentation](https://auto.gluon.ai/)
- [GitHub репозиторий](https://github.com/autogluon/autogluon)
- [examples использования](https://github.com/autogluon/autogluon/tree/master/examples)
- [Форум сообщества](https://discuss.autogluon.ai/)
