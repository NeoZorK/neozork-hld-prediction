# Optimization of AutoML Gluon for Apple Silicon (M1/M2/M3)

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who optimizes for Apple Silicon is critical

Why is Apple Silicon a revolution in machine learning?

### The benefits of Apple Silicon for ML

- **Unified Memory**: CPU and GPU use common memory (to 128GB)
- ** High energy efficiency**: in 2-3 times less energy consumption
- **Specialized kernels**: Natural Energy for ML operations
- **Metal Performance Shaders**: GPU acceleration for matrix operations

### Problems without optimization

- ** Slow Working**: By 3-5 times slower than it could be
- ** High energy consumption**: The battery is discharged per clock
- ** Reheating**: System braked due to thermal throttle
- ** Ineffective use of resources**: Only CPU, disregard of GPU

## Introduction in Optimization for Apple Silicon

<img src="images/optimized/apple_silicon_optimization.png" alt="Optimization for Apple Silicon" style"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 1: Optimizing AutoML Gluon for Apple Silicon*

**Why does Apple Silicon require a special approach?** Because it's artifacture ARM and not x86, and it requires special optimism for maximum performance.

Apple Silicon MacBook with M1, M2, M3 provides unique opportunities for acceleration machinin lightning via:

- **MLX** - Apple for Machine Learning on Apple Silicon
- **Ray** - distributed calculations with Apple Silicon support
- **OpenMP** - parallel calculations
- **Metal Performance Shaders (MPS)** - GPU acceleration

## installation for Apple Silicon

<img src="images/optimized/advanced_topics_overView.png" alt="installation for Apple Silicon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
== sync, corrected by elderman == @elder_man

**Why does installation for Apple Silicon require special attention?** Because most of the default packages are collected for x86, which leads to slow work through Rosetta emulation.

** Key aspects of optimized installation:**

- ** Anti-ARM64 packages**: Use of conda instead of pip
- **Optimized libraries**: NumPy, SciPy with support for the Accelerate
- **Metal Performance Shaders**: GPU acceleration for matrix operations
- **OpenMP**: Parallel calculations on CPU
- **MLX**: Specialized Framework Apple for ML
- **Ray**: Distributed calculations with Apple Silicon support

###1. Basic installation with optimization

Why is the conda better than the pip for Apple Silicon?

```bash
# Create conda environment with support for Apple Silicon
conda create -n autogluon-m1 python=3.9
conda activate autogluon-m1

# installation of basic dependencies - hard ARM64 versions
conda install -c conda-forge numpy pandas scikit-learn matplotlib seaborn

# Installation PyTorch with support for MPS
pip install torch torchvision torchaudio

# installation AutoGluon
pip install autogluon
```

### 2. installation MLX for Apple Silicon

Why is MLX the future of ML on Apple Silicon?

** Benefits of MLX:**

- **Intentional support**: Special for Apple Silicon
- High performance**: in 2-3 times faster than PyTorch
- ** Energy efficiency**: Less energy consumption
- **Simple use**: API is similar on NumPy

```bash
# Installation MLX - Apple for ML frame
pip install mlx mlx-lm

# Installation of additional MLX packages - Optimizers and Neuronets
pip install mlx-optimizers mlx-nn
```

### 3. installation Ray for Apple Silicon

```bash
# Installation Ray with support for Apple Silicon
pip install ray[default]

# Sheck of Apple Silicon support
python -c "import ray; print(ray.__version__)"
```

### 4. configuration OpenMP

```bash
# installation OpenMP for macOS
brew install libomp

# Installation Python Bindings
pip install openmp-python
```

## configuration for Apple Silicon

<img src="images/optimized/metrics_Detailed.png" alt="configuration for Apple Silicon" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 3: Optimized Conference AutoML Gloon for Apple Silicon*

**Why is the right conference for Apple Silicon important?** Because wrong Settings can reduce performance in 2-3 times:

** Key aspects of configuration:**

- ** CUDA**: Use of MPS instead of CUDA for GPU
- **configuring flows**: Optimal quantity of CPU flows
- **Management memory**: Effective use of unified memory
- **Metal Performance Shaders**: GPU acceleration for matrix operations
- **OpenMP**: Parallel calculations on CPU
- **MLX integration**: Use of specialized Apple libraries

###1. Disable CUDA and configuring MPS

```python
import os
import torch
import numpy as np

# CUDA shut down
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'

# Inclusion of MPS for Apple Silicon
if torch.backends.mps.is_available():
 os.environ['PYTORCH_ENABLE_MPS_FallBACK'] = '1'
 print("MPS (Metal Performance Shaders) available")
else:
 print("MPS not available")

# configuration OpenMP for Apple Silicon
os.environ['OMP_NUM_THREADS'] = str(torch.get_num_threads())
os.environ['MKL_NUM_THREADS'] = str(torch.get_num_threads())
os.environ['OPENBLAS_NUM_THREADS'] = str(torch.get_num_threads())

# check accessible devices
print(f"PyTorch Version: {torch.__version__}")
print(f"MPS available: {torch.backends.mps.is_available()}")
print(f"MPS built: {torch.backends.mps.is_built()}")
print(f"CPU threads: {torch.get_num_threads()}")
```

### 2. configuration AutoGluon for Apple Silicon

```python
from autogluon.tabular import TabularPredictor
import autogluon as ag

# configuration for Apple Silicon
def configure_apple_silicon():
 """
configuring AutoGluon for Best Work on Apple Silicon

 Returns:
 --------
 autogluon
AutoGluon with Optimization for Apple Silicon

 Notes:
 ------
Key Settings for Apple Silicon:
- number_gpus: 0 - CUDA shutdown (not supported on Apple Silicon)
- number_cpus: torch.get_num_threads() - use all available CPU kernels
== sync, corrected by elderman == @elder_man
- time_limit: 3600s = standard learning time (1 hour)

 MPS (Metal Performance Shaders) Settings:
Automatic definition of access to MPS
- Fallback on CPU if MPS not available
- Optimization for a unified Apple Silicon memory
 """

# CUDA shut down (not supported on Apple Silicon)
# Use of MPS instead of CUDA
 ag.set_config({
'num_gpus': 0, #CUDA GPU Disablement
'num_cpus': Torch.get_num_threads(), #All available CPU cores
'Memory_limit': 8, #Rememise in GB (optimal for Apple Silicon)
'time_limit': 3600 # Learning time in seconds (1 hour)
 })

 # configuration for MPS (Metal Performance Shaders)
# MPS is an Apple-specific buckend for GPU assessment
 if torch.backends.mps.is_available():
"Metal Performance Shaders")
# MPS provides a GPU acceleration for matrix operations
# Working with a unified Apple Silicon memory
 else:
print("Uses CPU (MPS not available)")
# Fallback on CPU if MPS not available
# All calculations will be done on CPU nuclei

 return ag

# Application of configuration
configure_apple_silicon()
```

## integration with MLX

♪##1 ♪ of the MLX-optimized models

```python
import mlx.core as mx
import mlx.nn as nn
from autogluon.tabular import TabularPredictor
import numpy as np

class MLXOptimizedPredictor:
 """
MLX-optimized Prefector for Apple Silicon

 Parameters:
 -----------
 model_path : str
Path to a directory with AutoGluon model:
- Should contain model files (.pkl)
- May contain MLX weights (mlx_whites.npz)
- Metadata model (model_info.json)

 Attributes:
 -----------
 model_path : str
Path to directory with model

 mlx_model : MLXTabularModel or None
MLX Model for Accelerated Inference
None if model not loaded

 feature_names : List[str] or None
List of topics
None if not defined

 Notes:
 ------
MLX (Machine Learning eXtended) is an Apple for ML:
- It's a special time for Apple Silicon.
- in 2-3 times faster than PyTorch on Apple Silicon
- Using Metal Performance Shaders for GPU assessment
- Optimized for Unified Memory
- API is similar on NumPy for ease of use.
 """

 def __init__(self, model_path: str):
 self.model_path = model_path
 self.mlx_model = None
 self.feature_names = None

 def load_mlx_model(self):
 """
Loading the model in MLX for fast-track Inference

 Returns:
 --------
 bool
True if the model is successfully loaded, False in otherwise

 Notes:
 ------
Model MLX loading process:
1. Loading weights from mlx_whites.npz file
2. creative architecture of the model with loaded weights
3. Initiating the MLX model for inference
4. the heck of architecture compatibility

Weight file requirements:
- Format: .npz
- Contains: layers weight, displacement, metadata
- Structure: dictionary with keys for each layer
 """
 try:
# Uploading MLX model weights
# mlx_whites.npz contains weights in format optimized for MLX
 weights = mx.load(f"{self.model_path}/mlx_weights.npz")

# creative architecture of the model with loaded weights
# Architecture is automatically determined on base weights
 self.mlx_model = self.create_mlx_architecture(weights)

"MLX model loaded successfully"
 return True

 except Exception as e:
print(f) Model MLX upload error: {e})
# Fallback: You can use a standard AutoGluon model
 return False

 def create_mlx_architecture(self, weights):
 """
MLX model on mass upload architecture

 Parameters:
 -----------
 weights : Dict[str, mx.array]
Vocabulary with model weights:
Keys: Plate names (e.g. 'layer_0.white', 'layer_0.bias')
- Values: MLX arrays with weights and offsets

 Returns:
 --------
 MLXTabularModel
MLX Model Class for Table Data

 Notes:
 ------
Architecture MLX models:
- Intake layer: Linear(input_size, hidden_sizes[0])
- Hidden layers: Linear + ReLU activation
- Output layer: Linear(hidden_sizes[-1], output_size)

Benefits of the MLX architecture:
- Optimized for Apple Silicon
- Using Metal Performance Shaders
- Effective Working with Unified Memory
- Automatic optimization for GPU/CPU
 """

 class MLXTabularModel(nn.Module):
 """
MLX Model for Table Data

 Parameters:
 -----------
 input_size : int
Size of inlet layer (number of topics)

 hidden_sizes : List[int]
Dimensions of hidden layers:
- [64, 32]: Two hidden layers (64 and 32 neurons)
- [128, 64, 32]: Three hidden layers
- [256]: One hidden layer (256 neurons)

 output_size : int
Dimensions of the output layer:
- 1: Regression or binic classification
- 2+: Multi-class classification
 """
 def __init__(self, input_size, hidden_sizes, output_size):
 super().__init__()
 self.layers = []

# The input layer
# Transforms input in hidden representation
 self.layers.append(nn.Linear(input_size, hidden_sizes[0]))

# Hidden layers with activation
# Each layer: Linear + ReLU for non-linearity
 for i in range(len(hidden_sizes) - 1):
 self.layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
Self.layers.append(n.ReLU()) #ReLU activation for non-linearity

# The output layer
# Final transformation in Treatment
 self.layers.append(nn.Linear(hidden_sizes[-1], output_size))

 def __call__(self, x):
 """
Direct passage through the model

 Parameters:
 -----------
 x : mx.array
Incoming data (batch_size, input_size)

 Returns:
 --------
 mx.array
End-of-life predictions (batch_sise, output_size)
 """
 for layer in self.layers:
 x = layer(x)
 return x

 return MLXTabularModel

 def predict_mlx(self, data: np.ndarray) -> np.ndarray:
 """
Implementation with the use of MLX for accelerated inference

 Parameters:
 -----------
 data : np.ndarray
Incoming data for prediction:
Format: (n_samples, n_features)
Type: float32 (optimal for MLX)
- Normalized data (recommended)

 Returns:
 --------
 np.ndarray
Model predictions:
Format: (n_samples, n_outputs)
Type: float32
- Values: Forecasts for each sample

 Raises:
 -------
 ValueError
If the MLX model not loaded

 Notes:
 ------
MLX projection process:
1. Conversion of NumPy in MLX array
2. Implementation of a direct passage through the model
3. Processing results with mx.eval()
4. Conversion back into NumPy

The benefits of MLX are:
- in 2-3 times faster than PyTorch on Apple Silicon
- Automatic use of GPU/CPU
- Optimization for Unified Memory
- Low energy consumption
 """
 if self.mlx_model is None:
Raise ValueError ("MLX model not loaded")

# Transforming in MLX array
# MLX Workinget with flat32 for optimal performance
 mlx_data = mx.array(data.astype(np.float32))

 # Prediction with MLX
#mx.eval() ensures lazy execution and optimization
 with mx.eval():
 predictions = self.mlx_model(mlx_data)

# Transforming back into NumPy for compatibility
 return np.array(predictions)

# Use of the MLX pre-indexor
def create_mlx_predictor(model_path: str):
""create MLX pre-indexor."
 predictor = MLXOptimizedPredictor(model_path)

 if predictor.load_mlx_model():
 return predictor
 else:
 return None
```

###2: Optimization of data for MLX

```python
def optimize_data_for_mlx(data: pd.dataFrame) -> np.ndarray:
 """
Optimizing data for MLX on Apple Silicon

 Parameters:
 -----------
 data : pd.dataFrame
Reference data for optimization:
- Contains numerical and categorical characteristics
- May contain missing values
- Different types of data (int, float, object)

 Returns:
 --------
 np.ndarray
Optimized data for MLX:
Format: (n_samples, n_features)
Type: float32 (optimal for MLX)
- Normalized values (mean=0, std=1)
- No missing values

 Notes:
 ------
Optimization process for MLX:
1. Selection of numbers only
2. Conversion in flat32 (optimal for Apple Silicon)
3. Normalization (z-score) for school stability
4. Processing of missing values

Benefits of optimization:
- Accelerating calculations in 2-3 times
- Stability of education
- Effective use of memory
- Optimization for Metal Performance Shaders
 """

# Transforming in numpy with the right type
# MLX Works faster with flat32 on Apple Silicon
 data_array = data.select_dtypes(include=[np.number]).values.astype(np.float32)

# Normalization for MLX (z-score normalization)
# Provides learning stability and better performance
 mean_values = data_array.mean(axis=0)
 std_values = data_array.std(axis=0)

# Avoid division on zero
 data_array = (data_array - mean_values) / (std_values + 1e-8)

 return data_array

# Use
def train_with_mlx_optimization(train_data: pd.dataFrame):
 """
Learning with MLX Optimization for Apple Silicon

 Parameters:
 -----------
 train_data : pd.dataFrame
data for learning:
- Contains target variable 'target'
- Mixed data types (numerical and categorical)
- May contain missing values

 Returns:
 --------
 TabularPredictor
Trained Prover with Optimisation for Apple Silicon

 Notes:
 ------
MLX optimization:
1. Optimization of data for MLX
2. configurization of a predictor for Apple Silicon
3. Training with optimized parameters
4. Maintenance of the model in MLX compatible format

Parameters Optimization:
- num_cpus: all available CPU kernels
- number_gpus: 0 (CUDA shut-off)
- memory_limit: 8GB (optimal for Apple Silicon)
- time_limit: 3,600s (1 hour of study)
 """

# Data Optimization for MLX
# Transforming in format, optimized for Apple Silicon
 optimized_data = optimize_data_for_mlx(train_data)

# a pre-indexor with optimization for Apple Silicon
 predictor = TabularPredictor(
Label='target', #Target
Problem_type='auto', #Automated definition of task type
Eval_metric='auto', #Automated choice of metrics
path='./mlx_models' #A path for maintaining MLX-compatible models
 )

# Learning to optimize for Apple Silicon
 predictor.fit(
Train_data, # Reference data (not optimized for compatibility)
 ag_args_fit={
'num_cpus': Torch.get_num_threads(), #All available CPU cores
'num_gpus': 0, #CUDA Disablement (not supported on Apple Silicon)
'Memory_limit': 8 #Rememation in GB (optimal for Apple Silicon)
 },
Time_limit=3600 # Learning time in seconds (1 hour)
 )

 return predictor
```

## configuration Ray for Apple Silicon

###1. configuring Ray cluster

```python
import ray
from ray import tune
import autogluon as ag

def configure_ray_apple_silicon():
 """
Conference Ray for Best Work on Apple Silicon

 Returns:
 --------
 ray
Initiated Ray cluster with optimization for Apple Silicon

 Notes:
 ------
 Ray configuration for Apple Silicon:
- num_cpus: all available CPU kernels
- num_gpus: 0 (CUDA GPU shut-down)
== sync, corrected by elderman == @elder_man
- ignore_reinit_error:True

Benefits of Ray on Apple Silicon:
- Distributed calculations on CPU kernels
- Effective use of unified memory
- Parallel data processing
Scaling up on multiple processes
 """

# Initiating Ray with settings for Apple Silicon
 ray.init(
num_cpus=torch.get_num_threads(), #All available CPU cores
num_gpus=0, #GPU for Apple Silicon (CUDA no supported)
object_store_memory=2 * 1024 * 1024 * 1024 #2GB object storage
ignore_reinit_error=True # Ignore reinitiation errors
 )

spring(f"Ray cluster initiated: {ray.is_initiated()}})
prent(f) "Absentible resources: {ray.clutter_resources()}")

 return ray

# Initiating Ray
ray_cluster = configure_ray_apple_silicon()
```

♪##2 ♪ Sent out with Ray ♪

```python
@ray.remote
def train_model_remote(data_chunk, model_config):
 """
Remote learning of the model with Ray on Apple Silicon

 Parameters:
 -----------
 data_chunk : pd.dataFrame
Part of the data for training:
- A subset of the original dataset
- Contains a target variable
- Maybe pre-Workingn.

 model_config : Dict[str, Any]
configuration model:
- label: str is the name of the target variable
- problem_type: str - task type ('auto', 'binary', 'multiclass', 'regression')
- eval_metric: str - evaluation metrics ('auto', 'accuracy', 'f1', 'rmse')
- time_limit: int = learning time in seconds
- presets: str - pre-installation of quality ('mediam_quality', 'high_quality')

 Returns:
 --------
 TabularPredictor
Trained Prover on Part of Data

 Notes:
 ------
Ray remote function for distributed education:
- Implemented on a separate process
- Uses the allocated resources of the CPU
- Optimized for Apple Silicon
- Returns a trained model.
 """

 from autogluon.tabular import TabularPredictor

# the pre-indexor with configuration
 predictor = TabularPredictor(
Label=model_config['label'], # Target variable
Problem_type=model_config['problem_type'], # Task type
eval_metric=model_config['eval_metric'] #Metric evaluation
 )

# Training on part of the data
 predictor.fit(
Data_chunk, #Part of data for learning
Time_limit=model_config['time_limit'], #Learning time
presets=model_config['presets'] #Preinstallation of quality
 )

 return predictor

def distributed_training_apple_silicon(data: pd.dataFrame, n_workers: int = 4):
 """
Distribution of training for Apple Silicon with Ray

 Parameters:
 -----------
 data : pd.dataFrame
Data for distributed education:
- Contains target variable 'target'
- Mixed data types
- May contain missing values

 n_workers : int, default=4
Number of Vorcers for distributed education:
- 2-4: for small datasets (<10K samples)
- 4-8: for medium datasets (10K-100K samples)
- 8-16: for large datasets (>100K samples)

 Returns:
 --------
 List[TabularPredictor]
List of trained pre-indicators on data parts

 Notes:
 ------
Progress in the distribution of education:
1. Segregation of data into part
2. model core configuration
3. Launch remote learning challenges
4. Waiting for completion of all tasks
5. Return of trained models

Benefits of distributed training:
- Parallel data processing
- Use of all CPU kernels
- Scale on large datasets
- Optimization for Apple Silicon
 """

# Disaggregation of data on part
# Every thief gets about the same amount of data
 chunk_size = len(data) // n_workers
 data_chunks = [data.iloc[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

# configuring model for all vorkers
 model_config = {
'label': 'barget', #Target variable
'Problem_type': 'auto', #Automated definition of task type
'Eval_metric': 'auto', #Automated choice of metrics
'time_limit': 1800, #Learning time in seconds (30 minutes)
'Presets': 'media_quality' # Preinstallation of quality
 }

# Launch Remote Learning Challenges
# Each task is done on a separate process
 futures = []
 for chunk in data_chunks:
 future = train_model_remote.remote(chunk, model_config)
 futures.append(future)

# Waiting to finish all tasks
#Ray automatically manages resources and processes
 results = ray.get(futures)

 return results

# Use of distributed education
def run_distributed_training(data: pd.dataFrame):
""Launch distributed learning."

 # configuration Ray
 configure_ray_apple_silicon()

# Launch distributed
 models = distributed_training_apple_silicon(data, n_workers=4)

Print(f) Models trained)

 return models
```

## Optimizing OpenMP

<img src="images/optimized/performance_comparison.png" alt="OpenMP" stile" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 4: Optimizing OpenMP for Apple Silicon*

**Why is it important to optimize OpenMP for Apple Silicon?** Because the right conference can accelerate calculations in 2-4 times:

** The key aspects of OpenMP optimization:**

- **configuring flows**: Optimal quantity of CPU flows
** Flow-linking**: Processor-specific reference
- **Management memory**: Effective use of cache
- ** Parallel algorithms**: Optimization for multi-nuclear systems
- ** Profiling**: Identification of bottlenecks in performance
- **Monitoring**: Resource tracking

### 1. configuration OpenMP for Apple Silicon

```python
import os
import multiprocessing as mp

def configure_openmp_apple_silicon():
 """
Conference OpenMP for Best Work on Apple Silicon

 Returns:
 --------
 int
Number of CPU kernels available

 Notes:
 ------
 OpenMP configuration for Apple Silicon:
- OMP_NUM_THIREDS: number of flows for OpenMP
- MKL_NUM_THIREDS: number of flows for Intel MKL
- OPENBLAS_NUM_THIREADS: number of flows for OpenBLAS
- VECLIB_MAXIMUM_THIREADS: number of flows for Apple Accelerate

Parameters Optimization:
- OMP_SCHEDULE: 'dynamic' - Dynamic distribution of tasks
- OMP_DYNAMIC: 'TRUE' - Dynamic Management Flows
- OMP_NESTED: 'TRUE' - an input parallelism

Benefits of OpenMP on Apple Silicon:
- Parallel calculations on all kernels
- Optimization for multi-nuclear systems
- Efficient use of resources
- Acceleration of matrix operations
 """

# Collection of number of kernels
# Apple Silicon M1/M2/M3 has 8-16 kernels
 num_cores = mp.cpu_count()
"Prent(f"Accepted kernel: {num_cores}")

# configuring the variables of the environment for OpenMP
# All libraries use the same number of flows
os.environment['OMP_NUM_THIREDS'] = st(num_cores) # Main OpenMP flows
os.environment['MKL_NUM_THIREDS'] = st(num_cores) #Intel MKL Flows
os.environment['OPENBLAS_NUM_THREADS'] = str(num_cores) # OpenBLAS Flows
os.environment['VECLIB_MAXIMUM_THEEADS'] = str(num_cores) # Apple Accelerate Flows

 # configuration for Apple Silicon
# Optimization for Apple Silicon multi-nuclear systems
os.environment['OMP_SCHEDULE'] = `dynamic' # Dynamic task allocation
os.environment['OMP_DYNAMIC'] = `TRUE' # Dynamic Management Flows
os.environ['OMP_NESTED'] = `TRUE' #Approved parallelism

OpenMP is set for Apple Silicon.

 return num_cores

# Application of settings
num_cores = configure_openmp_apple_silicon()
```

###2: Parallel Data Processing

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import numpy as np

def parallel_data_processing(data: pd.dataFrame, n_workers: int = None):
 """
Parallel Data Processing for Apple Silicon with OpenMP

 Parameters:
 -----------
 data : pd.dataFrame
Data for parallel processing:
- Contains numerical and categorical characteristics
- May contain missing values
- Different types of data

 n_workers : int, optional
Number of vorcers for parallel processing:
- None: Automatic definition (all CPU kernels)
- 2-4: for small datasets
- 4-8: for medium datasets
- 8-16: for large datasets

 Returns:
 --------
 pd.dataFrame
OWorking data with new signature:
- Missed values filled
- New features added (feature_sum, feature_mean)
- Optimized for Apple Silicon

 Notes:
 ------
parallel processing process:
1. Segregation of data into part
2. Parallel processing of each part
3. New features
4. Merging results

Benefits of parallel processing:
- Use of all CPU kernels
- Accelerating data processing
- Optimization for Apple Silicon
- Effective use of memory
 """

 if n_workers is None:
n_workers = mp.cpu_account() # Use of all available kernels

 def process_chunk(chunk):
 """
Processing of part of data

 Parameters:
 -----------
 chunk : pd.dataFrame
Part of data for processing

 Returns:
 --------
 pd.dataFrame
OWorking Part of Data
 """
# Normalization and completion of missing values
# Use the median for numerals
 chunk = chunk.fillna(chunk.median())

# new signs
# add aggregates for quality improvement
 if len(chunk.columns) > 1:
chunk['feature_sum'] = chunk.sum(axis=1) #A sum of all features
chunk['feature_mean'] = chunk.mean(axis=1) #Medial all features

 return chunk

# Disaggregation of data on part
# Every thief gets about the same amount of data
 chunk_size = len(data) // n_workers
 chunks = [data.iloc[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

# Parallel processing with ThreadPoolExector
# ThreadPoolExector optimized for I/O operations
 with ThreadPoolExecutor(max_workers=n_workers) as executor:
 processed_chunks = List(executor.map(process_chunk, chunks))

# Merging results
# Concatenation all overWorking Parts
 processed_data = pd.concat(processed_chunks, ignore_index=True)

 return processed_data

# Use of parallel processing
def optimize_data_processing(data: pd.dataFrame):
"Optimization of Data Processing""

 # configuration OpenMP
 configure_openmp_apple_silicon()

# Parallel processing
 processed_data = parallel_data_processing(data)

 return processed_data
```

## Full optimization for Apple Silicon

###1. Integrated configration system

```python
class AppleSiliconOptimizer:
 """
Apple Silicon optimization with integrated system settings

 Attributes:
 -----------
 num_cores : int
Number of CPU kernels available:
- M1: 8 kernels (4 production + 4 energy efficient)
- M2: 8-10 kernels (4-6 production + 4 energy efficient)
- M3: 8 to 12 kernels (4 to 6 production + 4 to 6 energy efficient)

 mps_available : bool
Access to MPS:
- True: GPU acceleration available
- False: only CPU calculations

 ray_initialized : bool
Initialization status of Ray Cluster:
- True: Ray cluster active
- False: Ray cluster not initiated

 Notes:
 ------
AppleSiliconOptimizer provides:
- Integrated system settings for Apple Silicon
- Optimization of all components (OpenMP, PyTorch, AutoGluon, Ray)
- Automatic determination of optimum parameters
- Monitoring performance
- Management resources
 """

 def __init__(self):
Self.num_cores = mp.cpu_account() #Number of CPU kernels
Self.mps_available = Torch.backends.mps.is_available() # Access to MPS
Self.ray_initialized = False #Ray Cluster Status

 def configure_system(self):
 """
Integrated configuring system for Apple Silicon

 Notes:
 ------
System process Settings:
1. Disablement of CUDA (not supported on Apple Silicon)
2. Conference OpenMP for parallel calculations
 3. configuration PyTorch for MPS acceleration
 4. configuration AutoGluon for Apple Silicon
5. Conference Ray for distributed calculations

Settings result:
- Optimized system for Apple Silicon
- Maximum performance
- Efficient use of resources
- Readiness to learn models
 """

# CUDA shut down (not supported on Apple Silicon)
# Use of MPS instead of CUDA
 os.environ['CUDA_VISIBLE_DEVICES'] = ''

#configuring OpenMP for parallel calculations
# Optimization for Apple Silicon multi-nuclear systems
 self.configure_openmp()

 # configuration PyTorch for MPS acceleration
# Inclusion of Metal Performance Shaders for GPU Assessment
 self.configure_pytorch()

 # configuration AutoGluon for Apple Silicon
#configuring for Best Work on Apple Silicon
 self.configure_autogluon()

#configuring Ray for distributed calculations
# Initiating cluster for parallel processing
 self.configure_ray()

"The system is optimized for Apple Silicon"

 def configure_openmp(self):
 """configuration OpenMP"""
 os.environ['OMP_NUM_THREADS'] = str(self.num_cores)
 os.environ['MKL_NUM_THREADS'] = str(self.num_cores)
 os.environ['OPENBLAS_NUM_THREADS'] = str(self.num_cores)
 os.environ['VECLIB_MAXIMUM_THREADS'] = str(self.num_cores)

 def configure_pytorch(self):
 """configuration PyTorch"""
 if self.mps_available:
 os.environ['PYTORCH_ENABLE_MPS_FallBACK'] = '1'
Print("MPS acceleration on")
 else:
print("MPS not available, used by CPU")

 def configure_autogluon(self):
 """configuration AutoGluon"""
 ag.set_config({
 'num_cpus': self.num_cores,
 'num_gpus': 0,
 'memory_limit': 8,
 'time_limit': 3600
 })

 def configure_ray(self):
 """configuration Ray"""
 try:
 ray.init(
 num_cpus=self.num_cores,
 num_gpus=0,
 object_store_memory=2 * 1024 * 1024 * 1024,
 ignore_reinit_error=True
 )
 self.ray_initialized = True
"Ray cluster initialized"
 except Exception as e:
Print(f) "The error of initialization Ray: {e}")

 def get_optimal_config(self, data_size: int) -> dict:
 """
Getting optimal configuration for Apple Silicon

 Parameters:
 -----------
 data_size : int
Dateset size for optimization:
<1000: Small datasets (rapid learning)
- 1000-10000: average datesets (quality and speed balance)
- >10000: large datasets (maximum quality)

 Returns:
 --------
 dict
Optimal conference for Apple Silicon:
- pre-installation of quality
- number_bag_folds: number of folds for bagging
- number_bag_sects: number of sets for bagging
- time_limit: learning time in seconds

 Notes:
 ------
Data Size Optimization Strategy:
- Small data networks: rapid learning, basic quality
- Medium datasets: balance of quality and speed
- Large datasets: maximum quality, long-term learning

Parameters Optimization:
- presets: model quality (deployment, medium, high)
- num_bag_folds: number of folds (3-5)
- num_bag_sects: number of sets (1-2)
- time_limit: time of study (10-60 minutes)
 """

 if data_size < 1000:
# Small datasets: rapid learning
 return {
'Presets': 'optimize_for_development', # Rapid deployment
'num_bag_folds': 3, #minimum number of folds
'num_bag_sets': 1, #One set for bagging
'time_limit': 600 #10 minutes learning
 }
 elif data_size < 10000:
# Medium datasets: balance of quality and speed
 return {
'Presets': 'mediam_quality', #Medial quality
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 1, #One set for bagging
'time_limit': 1800 #30 minutes of learning
 }
 else:
# Large datasets: maximum quality
 return {
'Presets': 'high_quality', #High quality
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 2, # Two sets for Bagging
'time_limit': 3600 #60 minutes of learning
 }

# Use of an optimist
optimizer = AppleSiliconOptimizer()
optimizer.configure_system()
```

###2: Optimized learning

```python
def train_optimized_apple_silicon(data: pd.dataFrame, target_col: str):
"Optimized Learning for Apple Silicon""

# configuring system
 optimizer = AppleSiliconOptimizer()
 optimizer.configure_system()

# Getting optimum configuration
 config = optimizer.get_optimal_config(len(data))

♪ Create pre-reactor
 predictor = TabularPredictor(
 label=target_col,
 problem_type='auto',
 eval_metric='auto',
 path='./apple_silicon_models'
 )

# Data optimization
 optimized_data = optimize_data_for_mlx(data)

# Training with optimization
 predictor.fit(
 data,
 presets=config['presets'],
 num_bag_folds=config['num_bag_folds'],
 num_bag_sets=config['num_bag_sets'],
 time_limit=config['time_limit'],
 ag_args_fit={
 'num_cpus': optimizer.num_cores,
 'num_gpus': 0,
 'memory_limit': 8
 }
 )

 return predictor

# Use
def run_optimized_training():
""Launch Optimized Learning."

# Create testy data
 from sklearn.datasets import make_classification
 X, y = make_classification(n_samples=10000, n_features=20, n_classes=2, random_state=42)

 data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(20)])
 data['target'] = y

# Optimized learning
 predictor = train_optimized_apple_silicon(data, 'target')

# Testing
 test_data = data.sample(1000)
 predictions = predictor.predict(test_data)

(f) "Learning COMPLETED, Forecasts: {len(predictations)}")

 return predictor

# Launch
if __name__ == "__main__":
 predictor = run_optimized_training()
```

## Monitoring performance

###1. Monitoring for Apple Silicon

```python
import psutil
import time
from datetime import datetime

class AppleSiliconMonitor:
 """
Monitoring performance for Apple Silicon

 Attributes:
 -----------
 start_time : float
Start time Monitoring (timestamp)

 metrics : List[Dict[str, Any]]
List metric performance:
- timestamp: time of measurement
- cpu_percent: use of CPU (%)
- cpu_freq: CPU frequency (MHz)
- memory_percent: use of memory (%)
- memory_available: accessible memory (GB)
-disk_percent: use of disc (%)
- cpu_temp: temperature CPU (°C)
- elapped_time: time of execution (seconds)

 Notes:
 ------
AppleSiliconMonitor provides:
- Monitoring systems resources
- Traceability of training
- Analysis of use of CPU, memory, disk
- CPU temperature control
- Generation of Performance Reports
 """

 def __init__(self):
Self.start_time = time.time() # Start time Monitoring
Self.metrics = [] #List metric performance

 def get_system_metrics(self):
 """
Receive system metrics for Apple Silicon

 Returns:
 --------
 Dict[str, Any]
Vocabulary with system metrics:
- timetamp: time of measurement (ISO format)
- cpu_percent: use of CPU (%)
- cpu_freq: CPU frequency (MHz)
- memory_percent: use of memory (%)
- memory_available: accessible memory (GB)
-disk_percent: use of disc (%)
- cpu_temp: temperature CPU (°C)
- elapped_time: time of execution (seconds)

 Notes:
 ------
Metrics performance:
- CPU: use and frequency of the processor
- Memory: use and accessible memory
- Disk: use of disk space
- Temperature: overheating control (if available)
- Time: tracking the duration of implementation

Apple Silicon features:
- Unified Memory (CPU and GPU)
- Energy efficient kernels
- Temperature control for prevention of throttle
 """

# CPU metrics
# Measurement of the use of CPU in 1 second
 cpu_percent = psutil.cpu_percent(interval=1)
cpu_freq = psutil.cpu_freq() #CPU frequency

# Memory
# Information on the use of memory
 memory = psutil.virtual_memory()

# Disk
# Use of disk space
 disk = psutil.disk_usage('/')

# Temperature (if available)
# Temperature control for preventing overheating
 try:
 temps = psutil.sensors_temperatures()
 cpu_temp = temps.get('cpu_thermal', [{}])[0].get('current', 0)
 except:
cpu_temp = 0 # Temperature not available

 return {
'TIMESTamp': Datatime.now().isoformat(), #Measurement time
'cpu_percent': cpu_percent, # Use of CPU (%)
'cpu_freq': cpu_freq.current if cpu_freq else 0, #CPU frequency (MHz)
'Memorry_percent': memory.percent, #Memorial use (%)
'Memory_available': memory.available / (1024**3), # Available memory (GB)
'disk_percent':disk.percent, # Use of disk (%)
'cpu_temp': cpu_temp, # CPU temperature (°C)
'Elapsed_time': time.time() - Self.start_time # Time (seconds)
 }

 def monitor_training(self, predictor, data):
"Monitoring Learning."

"Monitoring began..."

# Primary metrics
 initial_metrics = self.get_system_metrics()
 self.metrics.append(initial_metrics)

# Learning with Monitoring
 start_time = time.time()
 predictor.fit(data, time_limit=3600)
 training_time = time.time() - start_time

# Final metrics
 final_metrics = self.get_system_metrics()
 final_metrics['training_time'] = training_time
 self.metrics.append(final_metrics)

(f) "Learning COMPLETED in two seconds")

 return final_metrics

 def generate_Report(self):
 """
Generation Report on performance for Apple Silicon

 Returns:
 --------
 Dict[str, Any] or str
Report on performance or error report:
- total_time: total time (seconds)
- Training_time: time of study (seconds)
- avg_cpu_use: average use of CPU (%)
- max_cpu_use: maximum use of CPU (%)
- avg_memory_use: average memory use (%)
- max_memory_use: maximum use of memory (%)
- cpu_temp: temperature CPU (°C)

 Notes:
 ------
Performance analysis:
- Time of completion: total and time of training
- Use of CPU: average and maximum
- Memory use: average and maximum
- Temperature: overheating control

Recommendations on optimization:
- High use of CPU: increase the number of kernels
- High use of memory: reduce the size of the booth
- High temperature: decrease load or improve cooling
 """

 if not self.metrics:
no data for Reporta

# The metric analysis performance
 cpu_usage = [m['cpu_percent'] for m in self.metrics]
 memory_usage = [m['memory_percent'] for m in self.metrics]

# Generation of the Performance Report
 Report = {
'Total_time': Self.metrics[1]['elapsed_time'], #Total time
'training_time': Self.metrics[-1].get('training_time', 0), #Learning time
'avg_cpu_usage': sum(cpu_usage) / Len(cpu_usage), #Medial use of CPU
'max_cpu_usage': max(cpu_usage), # Maximum use of CPU
'avg_memory_use': sum(memory_use) / Len(memory_use), #Medial use of memory
'max_memory_use': max(memory_use), # Maximum use of memory
'cpu_temp': Self.metrics[1]['cpu_temp'] # CPU temperature
 }

 return Report

# Use of Monitoring
def run_with_Monitoring():
"Launch with Monitoring."

# Create monitor
 monitor = AppleSiliconMonitor()

# data quality
 from sklearn.datasets import make_classification
 X, y = make_classification(n_samples=5000, n_features=20, n_classes=2, random_state=42)
 data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(20)])
 data['target'] = y

♪ Create pre-reactor
 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
 )

# Learning with Monitoring
 final_metrics = monitor.monitor_training(predictor, data)

#Report generation
 Report = monitor.generate_Report()
"Report on performance:")
 for key, value in Report.items():
 print(f"{key}: {value}")

 return predictor, Report
```

## examples of use

*## 1. Complete example optimization

```python
def complete_apple_silicon_example():
"A full example optimization for Apple Silicon""

"print("===AutoML Gloon optimization for Apple Silicon====)

# 1. configurization system
 optimizer = AppleSiliconOptimizer()
 optimizer.configure_system()

# 2. data quality
 from sklearn.datasets import make_classification
 X, y = make_classification(
 n_samples=10000,
 n_features=50,
 n_informative=30,
 n_redundant=10,
 n_classes=2,
 random_state=42
 )

 data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(50)])
 data['target'] = y

Print(f) Dateset created: {data.chape})

# 3. Optimization of data
 optimized_data = optimize_data_for_mlx(data)
"data optimized for MLX"

# 4. Learning with Monitoring
 monitor = AppleSiliconMonitor()

 predictor = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy',
 path='./apple_silicon_optimized'
 )

# Training
 final_metrics = monitor.monitor_training(predictor, data)

♪ 5. Testing
 test_data = data.sample(1000)
 predictions = predictor.predict(test_data)

# 6. Quality assessment
 performance = predictor.evaluate(test_data)

"Results:")
print(f"performance: {performance}")
pint(f) "Learning time: 2 (f} seconds")

# 7. Report on performance
 Report = monitor.generate_Report()
"Report on performance:")
 for key, value in Report.items():
 print(f" {key}: {value}")

 return predictor, Report

# Launch full example
if __name__ == "__main__":
 predictor, Report = complete_apple_silicon_example()
```

### 2. Comparison performance

```python
def compare_performance():
"Comparison performance with optimization and without."

# data quality
 from sklearn.datasets import make_classification
 X, y = make_classification(n_samples=5000, n_features=20, n_classes=2, random_state=42)
 data = pd.dataFrame(X, columns=[f'feature_{i}' for i in range(20)])
 data['target'] = y

# Test without optimization
"print("==A test without optimization===)
 start_time = time.time()

 predictor_basic = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
 )

 predictor_basic.fit(data, time_limit=600)
 basic_time = time.time() - start_time

# Test with optimization
"print("===A test with optimization===)
 start_time = time.time()

 optimizer = AppleSiliconOptimizer()
 optimizer.configure_system()

 predictor_optimized = TabularPredictor(
 label='target',
 problem_type='binary',
 eval_metric='accuracy'
 )

 predictor_optimized.fit(
 data,
 time_limit=600,
 ag_args_fit={
 'num_cpus': optimizer.num_cores,
 'num_gpus': 0,
 'memory_limit': 8
 }
 )
 optimized_time = time.time() - start_time

# Comparson of results
Print(f"Time without optimization: {Basic_time:.2f}seconds")
Print(f"Time with optimization: {optimized_time:.2f}seconds")
"Acceleration: {Basic_time/optimized_time:.2f}x")

 return {
 'basic_time': basic_time,
 'optimized_time': optimized_time,
 'speedup': basic_time/optimized_time
 }

# Launch comparison
if __name__ == "__main__":
 results = compare_performance()
```

## Troubleshooting for Apple Silicon

###1: Typical problems and solutions

```python
def troubleshoot_apple_silicon():
"A solution to typical problems for Apple Silicon."

 print("=== Troubleshooting for Apple Silicon ===")

# Check access to the MPS
 if torch.backends.mps.is_available():
 print("✓ MPS available")
 else:
 print("✗ MPS not available - Use CPU")

 # check Ray
 try:
 ray.init(ignore_reinit_error=True)
 print("✓ Ray initialized")
 ray.shutdown()
 except Exception as e:
Print(f"\test Ray: {e}})

 # check OpenMP
 import os
 if 'OMP_NUM_THREADS' in os.environ:
OpenMP is set to: {os.environ['OM_NUM_THIREDS'}}flows}
 else:
"Print("\openMP not set")

# Check memory
 memory = psutil.virtual_memory()
print(f) Memory: {memory.percent}% used, {memory.available/(1024**3:1f}GB available)

 # check CPU
 cpu_count = mp.cpu_count()
(pint(f"CPU kernels: {cpu_account}})

# Launch diagnostics
if __name__ == "__main__":
 troubleshoot_apple_silicon()
```

###2: Optimizing for different data sizes

```python
def get_optimal_config_apple_silicon(data_size: int, data_type: str = 'tabular'):
 """
Getting optimal configuration for Apple Silicon

 Parameters:
 -----------
 data_size : int
Dateset size for optimization:
<1000: Small datasets (rapid learning)
- 1000-10000: average datesets (quality and speed balance)
- >10000: large datasets (maximum quality)

 data_type : str, default='tabular'
Data type for optimization:
- 'tabular': table data (on default)
- 'time_series': time series
- 'image': images
- 'text': text data

 Returns:
 --------
 Dict[str, Any]
Optimal conference for Apple Silicon:
- pre-installation of quality
- number_bag_folds: number of folds for bagging
- number_bag_sects: number of sets for bagging
- time_limit: learning time in seconds
- ag_args_fit: parameters for AutoGluon

 Notes:
 ------
Data Size Optimization Strategy:
- Small data networks: rapid learning, minimal resources
- Medium datasets: balance of quality and speed
- Large datasets: maximum quality, all resources

Resource parameters:
- num_cpus: number of CPU kernels (2-16)
- number_gpus: 0 (CUDA shut-off)
- memory_limit: memory limit in GB (4-16)
- time_limit: time of study (5-60 minutes)
 """

 if data_size < 1000:
# Small datasets: rapid learning
 return {
'Presets': 'optimize_for_development', # Rapid deployment
'num_bag_folds': 3, #minimum number of folds
'num_bag_sets': 1, #One set for bagging
'time_limit': 300, #5minutes of learning
 'ag_args_fit': {
'num_cpus': min(4, pmp.cpu_account(), #to 4 kernels
'num_gpus': 0, #CUDA Disable
'Memory_limit': 4 #4GB memory
 }
 }
 elif data_size < 10000:
# Medium datasets: balance of quality and speed
 return {
'Presets': 'mediam_quality', #Medial quality
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 1, #One set for bagging
'time_limit': 1800, #30 minutes of learning
 'ag_args_fit': {
'num_cpus': min(8), pmp.cpu_account(), # to 8 kernels
'num_gpus': 0, #CUDA Disable
'Memory_limit': 8 #8GB memory
 }
 }
 else:
# Large datasets: maximum quality
 return {
'Presets': 'high_quality', #High quality
'num_bag_folds': 5, # Standard number of folds
'num_bag_sets': 2, # Two sets for Bagging
'time_limit': 3600, #60 minutes of learning
 'ag_args_fit': {
'num_cpus': mp.cpu_account(), #All available kernels
'num_gpus': 0, #CUDA Disable
'Memory_limit': 16 #16GB memory
 }
 }

# Use
def train_with_optimal_config(data: pd.dataFrame, target_col: str):
"Learning with optimal configuration""

# Getting a configuration
 config = get_optimal_config_apple_silicon(len(data))

♪ Create pre-reactor
 predictor = TabularPredictor(
 label=target_col,
 problem_type='auto',
 eval_metric='auto'
 )

# Training with optimal configuration
 predictor.fit(
 data,
 presets=config['presets'],
 num_bag_folds=config['num_bag_folds'],
 num_bag_sets=config['num_bag_sets'],
 time_limit=config['time_limit'],
 ag_args_fit=config['ag_args_fit']
 )

 return predictor
```

## GPU Acceleration and Metal Performance Shaders

<img src="images/optimized/production_architecture.png" alt="GPU acceleration for Apple Silicon" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 5: GPU Acceleration and Metal Performance Shaders for Apple Silicon*

**Why is it important to use the GPU acceleration on Apple Silicon?** Because the GPU can accelerate matrix operations in 5-10 times:

** Key aspects of GPU accreditation:**

- **Metal Performance Shaders**: Specialized GPU operations
- **MPS Backend**: PyTorch with Apple GPU support
- **MLX**: Specialized Framework Apple for ML
- **Unified Memory**: Effective Data Exchange between CPU and GPU
- **Neural Engineering**: Specialized kernels for ML operations
**Optification of memory**: Minimalization of copying of data

## Best Practices for Apple Silicon

<img src="images/optimized/robustness_Analysis.png" alt="Best Practices for Apple Silicon" style"="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 6: Best Practices for Optimizing for Apple Silicon*

**Why are best practices for Apple Silicon important?** Because they help to achieve maximum performance:

** The key principles of optimization:**

- ** Anti-ARM64 packages**: Use of conda instead of pip
- ** Correct configration**: CUDA Disablement, configuring MPS
- **Optification of Flows**: configuring OpenMP for Multi-nuclear Systems
- **Management memory**: Effective use of unified memory
- **GPU acceleration**: Use of Metal Performance Shaders
- **Monitoring performance**: Resource tracking

### # ♪ recommendations to be made

* Why follow these recommendations?** Because they're tested by experience and give maximum duration:

- ** Principle of "Vulnerability":** Use of ARM64 packages instead of x86
- ** "Specialization" principle**: Use of Apple-specific libraries
- ** "Optimization" principle:** configurization under a specific architecture
- ** "Monitoringa" principle**: Ongoing tracking of performance
- ** "Texting" principle**: Regular heck of effectiveness
- ** "Renewals" principle**: Use of the latest versions of libraries

## Conclusion

This section provides a complete optimization of AutoML Gluon for Apple Silicon MacBook M1/M2/M3, including:

- **MLX Integration** for calculation
- **Ray setup** for distributed calculations
- **OpenMP optimization** for parallel calculations
- ** CUDA** and MPS settings
- **Monitoring performance** for Apple Silicon
- **Troubleshooting** typical problems

All Settings are optimized for maximum performance on Apple Silicon with the features of the M1/M2/M3 chip architecture.
