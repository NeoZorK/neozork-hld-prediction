# Retraining AutoML Gluon models

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who retraining is critical

**Why do 90% of ML models lose accuracy after six months in sales?** Because the world is changing and models remain static. Retraining is a process of "renewing knowledge" model, like a doctor who studies new methhods treatment.

### Catastrophic CONSEQUENCES OF OLD MODELS
- **Netflix Recommendations**: 2010 model not understood 2020 series
- **Google Translate**: Old models gave inaccurate translations of new slanges
- **Bank systems**: No models recognized new types of fraud
- **Medical diagnosis**: Old models missing new symptoms of disease

### The benefits of the right retraining
- **Activity**: The model always Works with relevant data
- ** Adaptation**: Automatically adjusted to change
- ** Competitiveness**: remains effective in a dynamic environment
- ** User confidence**: Results remain accurate and useful

## Introduction in retraining

<img src="images/optimized/retraining_workflow.png" alt="process retraining" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 1: process retraining of AutoML Gloon models*

*Why is retraining just not just "update the model"? ** It's a process of adapting the model to a changing world.

# Why are models getting older in sales? #
- ** Conceptual drift**: Reality changes faster than model
**data drift**: New types of data not available during training
People change behaviors and tastes.
- **Technical Changes**: New Devices, Platforms, Interface

Retraining is a critical process for maintaining the relevance of ML models in sales. In this section, we will look at all aspects of automated retraining models.

## Retraining strategies

<img src="images/optimized/walk_forward_Analesis.png" alt="Stile retraining strategies"="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
♪ Figure 2: Different retraining strategies ♪

**Why are different retraining strategies important?** Because different types of data and tasks require different approaches:

- **Periodic retraining**: Regular updates on schedule
- ** Drift-trigger retraining**: update when changes are detected
- **Inframental retraining**: progressive update with new data
- ** Full retraining**: complete remodeling with zero
- ** Adaptation**: Automatic adaptation to change
- ** Hybrid strategies**: Combination of different approaches

###1. Periodic retraining

*Why is periodic retraining the simplest and most reliable approach?** Because it's Working on a schedule, like an alarm clock that reminds you of updating knowledge, it's like regular refresher courses for doctors.

** Benefits of periodic retraining:**
- **Simple**: Easy to adjust and maintain
- ** Reliability**: Regular updates prevent degradation
- **Planibility**: Resources may be prepared in advance
- ** Quality control**: Time on testing before implementation

** Retraining interval selection:**
- ** Daily**: For fast-changing data (finance, news)
- ** Weekly**: For most business tasks
- ** Monthly**: for stable domains (health, education)
- **on demand**: With significant changes in data

```python
import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
from autogluon.tabular import TabularPredictor
import logging

class PeriodicRetraining:
""""" "Periodic retraining models"""

 def __init__(self, model_path: str, retraining_interval: int = 7):
 """
Initiating periodic retraining

 Parameters:
 -----------
 model_path : str
The path to the directory with the AutoGluon model should contain:
- Model files (.pkl)
- Metadata model
- The configuration files
 example: "./models/production_model_v1"

 retraining_interval : int, default=7
Retraining interval in days. Determines automatic frequency
Retraining models:
- 1: Daily retraining (for fast-changing data)
- 7: Weekly retraining (recommended for most tasks)
- 30: Monthly retraining (for stable domains)
- 90: Quarterly retraining (for very stable systems)
 """
 self.model_path = model_path
Self.retraining_interval = retraining_interval # days
 self.logger = logging.getLogger(__name__)

 def schedule_retraining(self):
"Planning Retraining""
# Weekly retraining is the main mechanism
 schedule.every().week.do(self.retrain_model)

# Daily heck of need retraining - Monitoring
 schedule.every().day.do(self.check_retraining_need)

# Launch Planner is an endless cycle
 while True:
 schedule.run_pending()
Time.sleep(3600) # check every hour

 def retrain_model(self):
""retraining the model - the main process of renewal""
 try:
 self.logger.info("starting model retraining...")
# Logs to start the Monitoring process

# Uploading of new data
 new_data = self.load_new_data()

# a new model
 predictor = TabularPredictor(
 label='target',
 path=f"{self.model_path}_new"
 )

# Training on new data
#time_limit=3600: Maximum learning time in seconds (1 hour)
# It prevents endless learning and controls resources
 predictor.fit(new_data, time_limit=3600)

# Validation of the new model
 if self.validate_new_model(predictor):
# Replacement of the old model
 self.deploy_new_model(predictor)
 self.logger.info("Model retraining COMPLETED successfully")
 else:
 self.logger.warning("New model validation failed, keeping old model")

 except Exception as e:
 self.logger.error(f"Model retraining failed: {e}")

 def check_retraining_need(self):
""Check Retraining""
# Check quality of current model
 current_performance = self.evaluate_current_model()

# Check data drift
 data_drift = self.check_data_drift()

# Check time of last retraining
 last_retraining = self.get_last_retraining_time()
 days_since_retraining = (datetime.now() - last_retraining).days

# Criteria for retraining
# Current_performance < 0.8: Model accuracy dropped below 80%
# Data_draft > 0.1: Data drift exceeded 10% (significant changes)
# Days_since_retraining > = Self.retraining_interval: It's been enough time
 if (current_performance < 0.8 or
 data_drift > 0.1 or
 days_since_retraining >= self.retraining_interval):
 self.logger.info("Retraining needed based on criteria")
 self.retrain_model()
```

♪##2. ♪ Adaptive retraining ♪

<img src="images/optimized/monte_carlo_Analisis.png" alt="Adaptive retraining" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 3: Adaptive retraining and data drift detective*

**Why is adaptive retraining important?** Because it reacts to change in real time:

- ** Drift Detective**: Automatic detection of changes in data
- ** Triggers retraining**: Conditions for Launch retraining process
- **Monitoring performance**: Model quality tracking
- **Statistical tests**: heck of change
- ** Adaptive thresholds**: Dynamic configuration of sensitivity
- **integration with Monitoring**: Communication with observation systems

```python
class AdaptiveRetraining:
"Aptative retraining on basic performance"

 def __init__(self, model_path: str, performance_threshold: float = 0.8):
 """
Initiating adaptive retraining

 Parameters:
 -----------
 model_path : str
The path to the directory with the current AutoGluon model.
Used for downloading and updating the model.

 performance_threshold : float, default=0.8
Minimum threshold performance model (0.0 - 1.0).
Falling performance below this value
automatically Launche retraining:
- 0.9: Very high requirements (critical systems)
- 0.8: High requirements (recommended for sale)
- 0.7: Average requirements (development and testing)
- 0.6: Low requirements (experimental models)
 """
 self.model_path = model_path
 self.performance_threshold = performance_threshold
 self.performance_history = []
 self.logger = logging.getLogger(__name__)

 def monitor_performance(self, predictions: List, actuals: List):
"Monitoring Performance Model."
# Calculation of current performance
 current_performance = self.calculate_performance(predictions, actuals)

# add in history
 self.performance_history.append({
 'timestamp': datetime.now(),
 'performance': current_performance
 })

# Check trend performance
 if self.detect_performance_degradation():
 self.logger.warning("Performance degradation detected")
 self.trigger_retraining()

 def detect_performance_degradation(self) -> bool:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 if len(self.performance_history) < 10:
 return False

# Trends analysis for the last 10 measurements
# A sliding window for Analysis trend performance is used
 recent_performance = [p['performance'] for p in self.performance_history[-10:]]

# Check reduction performance
# Conditions for Launch retraining:
# 1. Current performance below the threshold
# 2. Performance has deteriorated to the beginning of the period
 if (recent_performance[-1] < self.performance_threshold and
 recent_performance[-1] < recent_performance[0]):
 return True

 return False

 def trigger_retraining(self):
"""Launch retraining"""
 self.logger.info("Triggering adaptive retraining...")

# Loading data for retraining
 retraining_data = self.load_retraining_data()

# creative and learning the new model
 predictor = TabularPredictor(
 label='target',
 path=f"{self.model_path}_adaptive"
 )

 predictor.fit(retraining_data, time_limit=3600)

# Calidation and decoupling
 if self.validate_new_model(predictor):
 self.deploy_new_model(predictor)
Self.performance_history = [] # History drop
```

♪##3 ♪ Incretional retraining ♪

```python
class IncrementalRetraining:
"Inframental retraining with knowledge preservation."

 def __init__(self, model_path: str, batch_size: int = 1000):
 """
Initiating an institutional retraining system

 Parameters:
 -----------
 model_path : str
The path to the directory with the current AutoGluon model.
The model will be updated internally with new data.

 batch_size : int, default=1000
Size of booth for processing new data.
- Memory consumption: More batch_size = more memory
- Processing speed: Optimal size accelerates learning
- Model quality: Too small/big may affect quality
Recommendations:
- 100-500: for small datasets (< 10K records)
- 1000-5000: for medium datasets (10K-100K records)
- 5000-10000: for large datasets (> 100K records)
 """
 self.model_path = model_path
 self.batch_size = batch_size
 self.logger = logging.getLogger(__name__)

 def incremental_update(self, new_data: pd.dataFrame):
""""""""""""""""""""""
 try:
# Loading the current model
 current_predictor = TabularPredictor.load(self.model_path)

# Combining old and new data
 combined_data = self.combine_data(current_predictor, new_data)

# Training on integrated data
 updated_predictor = TabularPredictor(
 label='target',
 path=f"{self.model_path}_updated"
 )

 updated_predictor.fit(combined_data, time_limit=3600)

♪ validation of the updated model
 if self.validate_updated_model(updated_predictor):
 self.deploy_updated_model(updated_predictor)
 self.logger.info("Incremental update COMPLETED")
 else:
 self.logger.warning("Updated model validation failed")

 except Exception as e:
 self.logger.error(f"Incremental update failed: {e}")

 def combine_data(self, current_predictor, new_data: pd.dataFrame) -> pd.dataFrame:
""""""""""""""""""
# Collection of old data from the model (if available)
 old_data = self.extract_old_data(current_predictor)

# Data integration
 if old_data is not None:
 combined_data = pd.concat([old_data, new_data], ignore_index=True)
 else:
 combined_data = new_data

 return combined_data
```

## Automation retraining

<img src="images/optimized/addianced_production_flow.png" alt="Automatization" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
*Picture 4: Automated Model Retraining System*

**Why is automation of retraining important?** Because manual retraining is inefficient and subject to errors:

- **Automatic triggers**: Launch retraining on conditions
- **niplines CI/CD**: integration with development processes
- **A/B testing**:comparison of old and new models
- **Rollback changes**: Possible quick return to previous version
- **Monitoring process**: Retraining status tracking
- **notifications**: Alerts on status and results

### Automatic retraining system

```python
import asyncio
import aiohttp
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta

class AutomatedRetrainingsystem:
""Automated Retraining System""

 def __init__(self, config: Dict[str, Any]):
 """
Initiating automatic retraining

 Parameters:
 -----------
 config : Dict[str, Any]
The configuration dictionary with the system parameters:
- Data_quality_threshold: float = minimum data quality threshold (0.0-1.0)
- Performance_threshold: float = minimum threshold of performance (0.0-1.0)
- drift_threshold: float is the threshold for data drift detection (0.0-1.0)
- max_retraining_time:int = maximum time retraining in seconds
- Retraining_interval:int is the time required to retrain
- model_path: STR is the path to the directory with models
- Backup_path: STR is the path for backup copies
 """
 self.config = config
 self.logger = logging.getLogger(__name__)
 self.retraining_queue = asyncio.Queue()
 self.is_retraining = False

 async def start_Monitoring(self):
""Launch Monitoring System."
 tasks = [
 self.monitor_data_quality(),
 self.monitor_model_performance(),
 self.monitor_data_drift(),
 self.process_retraining_queue()
 ]

 await asyncio.gather(*tasks)

 async def monitor_data_quality(self):
"Monitorizing Data Quality."
 while True:
 try:
# Check quality of new data
 data_quality = await self.check_data_quality()

# Check data quality
# Data_quality_threshold: Data quality threshold (0.0-1.0)
# 0.9: Very high quality requirements
# 0.8: High requirements (recommended)
#0.7: Average requirements
# 0.6: Low requirements
 if data_quality['score'] < self.config['data_quality_threshold']:
 self.logger.warning(f"data quality issue: {data_quality}")
 await self.trigger_retraining('data_quality')

await asyncio.sleep(3600) # check every hour

 except Exception as e:
 self.logger.error(f"data quality Monitoring error: {e}")
 await asyncio.sleep(300)

 async def monitor_model_performance(self):
"Monitoring Performance Model."
 while True:
 try:
# Getting a metric performance
 performance = await self.get_model_performance()

# Check performance model
# Performance_threshold: Minimum threshold of accuracy (0.0-1.0)
# 0.95: Critical systems (health, finance)
# 0.9: High requirements (recommendation systems)
#0.8: Standard requirements (most tasks)
#0.7: Low requirements (experimental models)
 if performance['accuracy'] < self.config['performance_threshold']:
 self.logger.warning(f"Performance degradation: {performance}")
 await self.trigger_retraining('performance')

await asyncio.sleep(1800) # check every 30 minutes

 except Exception as e:
 self.logger.error(f"Performance Monitoring error: {e}")
 await asyncio.sleep(300)

 async def monitor_data_drift(self):
"Monitoring Data Drift."
 while True:
 try:
# Check data drift
 drift_score = await self.check_data_drift()

# Check data drift
# Drift_threshold: Drift detection threshold (0.0-1.0)
# 0.1: Very sensitive detective (rapid reaction)
# 0.2: Standard sensitivity (recommended)
# 0.3: Low sensitivity (stable systems)
# 0.5: Very low sensitivity (critical changes only)
 if drift_score > self.config['drift_threshold']:
 self.logger.warning(f"data drift detected: {drift_score}")
 await self.trigger_retraining('data_drift')

await asyncio.sleep(7200) # check every 2 hours

 except Exception as e:
 self.logger.error(f"data drift Monitoring error: {e}")
 await asyncio.sleep(300)

 async def trigger_retraining(self, reason: str):
"""Launch retraining"""
 if self.is_retraining:
 self.logger.info("Retraining already in progress")
 return

 retraining_request = {
 'timestamp': datetime.now().isoformat(),
 'reason': reason,
 'priority': self.get_retraining_priority(reason)
 }

 await self.retraining_queue.put(retraining_request)
 self.logger.info(f"Retraining queued: {retraining_request}")

 async def process_retraining_queue(self):
""""""""""""""""""""""""""""""""""Retraining""""""""
 while True:
 try:
# Receive request on retraining
 request = await self.retraining_queue.get()

# Retraining
 await self.execute_retraining(request)

 self.retraining_queue.task_done()

 except Exception as e:
 self.logger.error(f"Retraining processing error: {e}")
 await asyncio.sleep(300)

 async def execute_retraining(self, request: Dict[str, Any]):
"To retrain"
 self.is_retraining = True

 try:
 self.logger.info(f"starting retraining: {request}")

 # Loading data
 data = await self.load_retraining_data()

# a new model
 predictor = TabularPredictor(
 label='target',
 path=f"./models/retrained_{request['timestamp']}"
 )

# Training
 predictor.fit(data, time_limit=3600)

# validation
 if await self.validate_new_model(predictor):
# A new model
 await self.deploy_new_model(predictor)
 self.logger.info("Retraining COMPLETED successfully")
 else:
 self.logger.warning("New model validation failed")

 except Exception as e:
 self.logger.error(f"Retraining execution failed: {e}")
 finally:
 self.is_retraining = False
```

## Validation of retrained models

♪## ♪ Validation system ♪

```python
class RetrainingValidator:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")")")")")")")")")")")")")")")")")")")")")")")")")""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, validation_config: Dict[str, Any]):
 """
Initiating a re-trained model driver

 Parameters:
 -----------
 validation_config : Dict[str, Any]
configuring validation with parameters:
- Improvement_threshold: float = minimum improve for model adoption (0.0-1.0)
- performance_metrics: List[str] - List metric for comparison
- minimum_requirements: Dict[str, float] - Minimum requirements for metrics
- stability_threshold: float is the threshold for stability preferences (0.0-1.0)
- required_Version: str - required version of AutoGluon
 """
 self.config = validation_config
 self.logger = logging.getLogger(__name__)

 async def validate_new_model(self, new_predictor, old_predictor=None) -> bool:
"Validation of the New Model."
 try:
# Loading test data
 test_data = await self.load_test_data()

# The new model's predictions
 new_predictions = new_predictor.predict(test_data)
 new_performance = new_predictor.evaluate(test_data)

# Comparison with the old model (if available)
 if old_predictor is not None:
 old_predictions = old_predictor.predict(test_data)
 old_performance = old_predictor.evaluate(test_data)

# Check improvement performance
 if not self.check_performance_improvement(new_performance, old_performance):
 self.logger.warning("New model doesn't improve performance")
 return False

# Check minimum requirements
 if not self.check_minimum_requirements(new_performance):
 self.logger.warning("New model doesn't meet minimum requirements")
 return False

# Check stability
 if not self.check_model_stability(new_predictor, test_data):
 self.logger.warning("New model is not stable")
 return False

# Check compatibility
 if not self.check_compatibility(new_predictor):
 self.logger.warning("New model is not compatible")
 return False

 return True

 except Exception as e:
 self.logger.error(f"Model validation failed: {e}")
 return False

 def check_performance_improvement(self, new_perf: Dict, old_perf: Dict) -> bool:
 """
check improvements of the new model

 Parameters:
 -----------
 new_perf : Dict
Metrics performance of the new model
 old_perf : Dict
Metrics performance of the old model

 Returns:
 --------
 bool
True if the new model shows improve on all metrics

 Notes:
 ------
Improvement_threshold: minimum improve for model adoption
0.01 (1 per cent): Minimum improve (conservative approach)
- 0.02 (2 per cent): Standard improve (recommended)
- 0.05 (5 per cent): Significant improve (aggressive approach)
- 0.0: Any improve (experimental approach)
 """
 improvement_threshold = self.config.get('improvement_threshold', 0.02)

 for metric in self.config['performance_metrics']:
 if metric in new_perf and metric in old_perf:
 improvement = new_perf[metric] - old_perf[metric]
 if improvement < improvement_threshold:
 return False

 return True

 def check_minimum_requirements(self, performance: Dict) -> bool:
"The check of minimum requirements."
 for metric, threshold in self.config['minimum_requirements'].items():
 if metric in performance and performance[metric] < threshold:
 return False

 return True

 def check_model_stability(self, predictor, test_data: pd.dataFrame) -> bool:
 """
model stability

 Parameters:
 -----------
 predictor : TabularPredictor
Model for stability testing
 test_data : pd.dataFrame
test data for verification

 Returns:
 --------
 bool
True if the model is stable (predicted)

 Notes:
 ------
stability_threshold: consistency threshold of preferences (0.0-1.0)
- 0.99: Very high stability (critical systems)
- 0.95: High stability (recommended for sale)
- 0.90: Average stability (acceptable for most tasks)
- 0.85: Low stability (for experiments only)
 """
# Multiple predictions on the same data
# 5 iterations for reproducibility testing
 predictions = []
 for _ in range(5):
 pred = predictor.predict(test_data)
 predictions.append(pred)

# Check consistency preferences
# High coherence = stable model
 consistency = self.calculate_Prediction_consistency(predictions)
 return consistency > self.config.get('stability_threshold', 0.95)

 def check_compatibility(self, predictor) -> bool:
""Check model compatibility""
# Check version of AutoGluon
 if hasattr(predictor, 'version'):
 if predictor.version != self.config.get('required_version'):
 return False

# Check model format
 if not self.check_model_format(predictor):
 return False

 return True
```

## Monitoring retraining

<img src="images/optimized/production_architecture.png" alt="Monitoring retraining" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Picture 5: Monitoring process retraining system*

Why is Monitoring retraining critical?

- **Monitoring performance**: Monitoring the quality of the new model
- **comparison of models**: A/B testing old and new versions
- ** Problem Detective**: Early detection of deterioration of quality
- **metrics drift**: Tracking changes in data
- ** Resource consumption**: Monitoring use of CPU, memory, GPU
**Temporary metrics**: Traceability of learning time and inference

### The Monitoring System

```python
class RetrainingMonitor:
"Monitoring Retraining"

 def __init__(self, Monitoring_config: Dict[str, Any]):
 """
Initiating Monitoring Retraining

 Parameters:
 -----------
 Monitoring_config : Dict[str, Any]
configuring Monitoring with parameters:
- max_retraining_time:int = maximum time retraining in seconds
- cpu_threshold: float - CPU threshold (0.0-1.0)
- memory_threshold: float is the storage threshold (0.0-1.0)
- Disk_threshold: float - disc threshold (0.0-1.0)
- check_interval: int = resource in seconds test interval
 """
 self.config = Monitoring_config
 self.logger = logging.getLogger(__name__)
 self.metrics = {}

 def start_Monitoring(self, retraining_process):
"Launch Monitoring."
# Monitoring resources
 self.monitor_resources()

# Monitoring progress
 self.monitor_progress(retraining_process)

# Monitoring quality
 self.monitor_quality(retraining_process)

 def monitor_resources(self):
"Monitoring Systems Resources"
 import psutil

 while True:
 try:
# CPU use
 cpu_percent = psutil.cpu_percent()

# Memory
 memory = psutil.virtual_memory()
 memory_percent = memory.percent

# Disk
 disk = psutil.disk_usage('/')
 disk_percent = disk.percent

# Logslation of metric
 self.logger.info(f"Resources - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")

# Check resource limits
# Thresholds in Monitoring configuration
 cpu_threshold = self.config.get('cpu_threshold', 0.9) * 100
 memory_threshold = self.config.get('memory_threshold', 0.9) * 100
 disk_threshold = self.config.get('disk_threshold', 0.9) * 100

 if cpu_percent > cpu_threshold:
 self.logger.warning(f"High CPU usage detected: {cpu_percent}% > {cpu_threshold}%")

 if memory_percent > memory_threshold:
 self.logger.warning(f"High memory usage detected: {memory_percent}% > {memory_threshold}%")

 if disk_percent > disk_threshold:
 self.logger.warning(f"High disk usage detected: {disk_percent}% > {disk_threshold}%")

Time.sleep(60) # check every minutes

 except Exception as e:
 self.logger.error(f"Resource Monitoring error: {e}")
 time.sleep(300)

 def monitor_progress(self, retraining_process):
"Monitoring Progress Retraining"
 start_time = datetime.now()

 while retraining_process.is_alive():
 elapsed_time = datetime.now() - start_time

# Check time of execution
# max_retraining_time: maximum time retraining in seconds
# 3600 (1 hour): Rapid retraining for simple models
# 7200 (2 hours): Standard Time (recommended)
# 14400 (4 hours): Long-term retraining for complex models
# 28800 (8 hours): Very long retraining
 max_time = self.config.get('max_retraining_time', 7200)
 if elapsed_time.total_seconds() > max_time:
 self.logger.error(f"Retraining timeout exceeded: {elapsed_time} > {max_time}s")
 retraining_process.terminate()
 break

# Logs of progress
 self.logger.info(f"Retraining progress: {elapsed_time}")

Time.sleep(300) # check every 5 minutes

 def monitor_quality(self, retraining_process):
"Monitoring Quality Retraining"
# Monitoring quality metric
 quality_metrics = {
 'accuracy': [],
 'precision': [],
 'recall': [],
 'f1_score': []
 }

 while retraining_process.is_alive():
 try:
# Getting current metrics
 current_metrics = self.get_current_metrics()

# add in history
 for metric, value in current_metrics.items():
 if metric in quality_metrics:
 quality_metrics[metric].append(value)

# Trends analysis
 self.analyze_quality_trend(quality_metrics)

Time.sleep(600) # check every 10 minutes

 except Exception as e:
 self.logger.error(f"Quality Monitoring error: {e}")
 time.sleep(300)
```

## Rollback models

### Rollback system

```python
class ModelRollback:
"Rollback Model System""

 def __init__(self, Rollback_config: Dict[str, Any]):
 """
Initialization of the Rollback model system

 Parameters:
 -----------
 Rollback_config : Dict[str, Any]
configuring Rollback with parameters:
- Current_model_path: STR - route to the current active model
- Backup_model_path: STR is the path for storing backup copies
- max_versions:int = maximum number of storage versions
- Backup_retention_days:int = number of days of backup storage
 """
 self.config = Rollback_config
 self.logger = logging.getLogger(__name__)
 self.model_versions = []

 def create_backup(self, model_path: str):
""create backup model""
 backup_path = f"{model_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

 try:
# Copying the model
 import shutil
 shutil.copytree(model_path, backup_path)

# Retaining version information
 version_info = {
 'timestamp': datetime.now().isoformat(),
 'path': backup_path,
 'original_path': model_path
 }

 self.model_versions.append(version_info)

 self.logger.info(f"Model backup created: {backup_path}")
 return backup_path

 except Exception as e:
 self.logger.error(f"Backup creation failed: {e}")
 return None

 def Rollback_model(self, target_Version: str = None):
"Rollback to the previous version of the model."
 try:
 if target_version is None:
# Rollback to the latest version
 if len(self.model_versions) < 2:
 self.logger.warning("No previous version available for Rollback")
 return False

 target_version = self.model_versions[-2]['path']
 else:
# Rollback to specified version
 target_version = self.find_version_path(target_version)
 if target_version is None:
 self.logger.error(f"Version {target_version} not found")
 return False

# Restoration of the model
 current_path = self.config['current_model_path']
 backup_path = self.config['backup_model_path']

# of the backup of the current model
 self.create_backup(current_path)

# Recovery from backup
 import shutil
 shutil.copytree(target_version, current_path, dirs_exist_ok=True)

 self.logger.info(f"Model rolled back to: {target_version}")
 return True

 except Exception as e:
 self.logger.error(f"Model Rollback failed: {e}")
 return False

 def find_version_path(self, version_id: str) -> str:
"Looking for a model version."
 for version in self.model_versions:
 if version_id in version['path']:
 return version['path']
 return None
```

## examples of use

### Full example retraining system

```python
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from autogluon.tabular import TabularPredictor

# configuring Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompleteRetrainingsystem:
"The Full Retraining System."

 def __init__(self, config: Dict[str, Any]):
 self.config = config
 self.logger = logging.getLogger(__name__)
 self.current_model = None
 self.retraining_history = []

 async def initialize(self):
"Initiating the system."
# Loading the current model
 self.current_model = TabularPredictor.load(self.config['model_path'])

# Launch Monitoring
 await self.start_Monitoring()

 async def start_Monitoring(self):
"Launch Monitoring."
 tasks = [
 self.monitor_performance(),
 self.monitor_data_drift(),
 self.monitor_schedule()
 ]

 await asyncio.gather(*tasks)

 async def monitor_performance(self):
"""Monitoring performance"""
 while True:
 try:
# Getting a metric performance
 performance = await self.get_current_performance()

# Check degradation
 if performance['accuracy'] < self.config['performance_threshold']:
 self.logger.warning(f"Performance degradation detected: {performance}")
 await self.trigger_retraining('performance_degradation')

await asyncio.sleep(1800) # check every 30 minutes

 except Exception as e:
 self.logger.error(f"Performance Monitoring error: {e}")
 await asyncio.sleep(300)

 async def monitor_data_drift(self):
"Monitoring Data Drift."
 while True:
 try:
# Check data drift
 drift_score = await self.check_data_drift()

 if drift_score > self.config['drift_threshold']:
 self.logger.warning(f"data drift detected: {drift_score}")
 await self.trigger_retraining('data_drift')

await asyncio.sleep(3600) # check every hour

 except Exception as e:
 self.logger.error(f"data drift Monitoring error: {e}")
 await asyncio.sleep(300)

 async def monitor_schedule(self):
"Monitoring Schedules."
 while True:
 try:
# Check time of last retraining
 last_retraining = self.get_last_retraining_time()
 days_since_retraining = (datetime.now() - last_retraining).days

 if days_since_retraining >= self.config['retraining_interval']:
 self.logger.info("Scheduled retraining triggered")
 await self.trigger_retraining('scheduled')

await asyncio.sleep(3600) # check every hour

 except Exception as e:
 self.logger.error(f"Schedule Monitoring error: {e}")
 await asyncio.sleep(300)

 async def trigger_retraining(self, reason: str):
"""Launch retraining"""
 self.logger.info(f"Triggering retraining: {reason}")

 try:
# Create backup
 backup_path = self.create_model_backup()

# Uploading of new data
 new_data = await self.load_new_data()

# a new model
 new_predictor = TabularPredictor(
 label=self.config['target_column'],
 path=f"{self.config['model_path']}_new"
 )

# Training
 new_predictor.fit(new_data, time_limit=3600)

# validation
 if await self.validate_new_model(new_predictor):
# A new model
 await self.deploy_new_model(new_predictor)

# Update story
 self.retraining_history.append({
 'timestamp': datetime.now().isoformat(),
 'reason': reason,
 'backup_path': backup_path,
 'status': 'success'
 })

 self.logger.info("Retraining COMPLETED successfully")
 else:
# Rollback to the previous version
 self.Rollback_model(backup_path)

 self.retraining_history.append({
 'timestamp': datetime.now().isoformat(),
 'reason': reason,
 'backup_path': backup_path,
 'status': 'failed'
 })

 self.logger.warning("Retraining failed, rolled back to previous version")

 except Exception as e:
 self.logger.error(f"Retraining failed: {e}")

# Rollback in case of error
 if 'backup_path' in locals():
 self.Rollback_model(backup_path)

 async def validate_new_model(self, new_predictor) -> bool:
"Validation of the New Model."
 try:
# Loading test data
 test_data = await self.load_test_data()

# The new model's predictions
 new_predictions = new_predictor.predict(test_data)
 new_performance = new_predictor.evaluate(test_data)

# Comparison with the current model
 current_predictions = self.current_model.predict(test_data)
 current_performance = self.current_model.evaluate(test_data)

# Check improvement
 improvement = new_performance['accuracy'] - current_performance['accuracy']

 if improvement < self.config.get('improvement_threshold', 0.01):
 self.logger.warning(f"Insufficient improvement: {improvement}")
 return False

# Check minimum requirements
 if new_performance['accuracy'] < self.config.get('minimum_accuracy', 0.8):
 self.logger.warning(f"Accuracy below minimum: {new_performance['accuracy']}")
 return False

 return True

 except Exception as e:
 self.logger.error(f"Model validation failed: {e}")
 return False

 async def deploy_new_model(self, new_predictor):
"The New Model's Business."
 try:
# Stopping the current service
 await self.stop_current_service()

# Replacement of the model
 import shutil
 shutil.copytree(new_predictor.path, self.config['model_path'], dirs_exist_ok=True)

# Update current model
 self.current_model = new_predictor

# Launch updated service
 await self.start_updated_service()

 self.logger.info("New model deployed successfully")

 except Exception as e:
 self.logger.error(f"Model deployment failed: {e}")
 raise

 def create_model_backup(self) -> str:
""create backup model""
 backup_path = f"{self.config['model_path']}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

 import shutil
 shutil.copytree(self.config['model_path'], backup_path)

 return backup_path

 def Rollback_model(self, backup_path: str):
"Rollback to the previous version."
 import shutil
 shutil.copytree(backup_path, self.config['model_path'], dirs_exist_ok=True)

# Update current model
 self.current_model = TabularPredictor.load(self.config['model_path'])

 self.logger.info(f"Model rolled back to: {backup_path}")

# Configuring the retraining system
config = {
'Model_path': './production_models', #The way to the directory with models
'Target_column': 'target', #The name of the target variable
'Performance_threshold': 0.8, # Minimum threshold performance (80%)
'drift_threshold': 0.1 # Data drift detection threshold (10%)
'retraining_interval': 7, #Retraining in Days
'improvement_threshold': 0.01, #minimum improve for model adoption (1 per cent)
'minimum_accuracy': 0.8, # Minimum model accuracy (80%)

# Additional parameters Monitoring
'data_quality_threshold': 0.8, # Data quality threshold (80%)
'max_retraining_time': 7,200, # Maximum time retraining (2 hours)
'Stability_threshold': 0.95, #Sustainability threshold (95 %)

# Parameters resources
'cpu_threshold': 0.9, #CPU use threshold (90%)
'memory_threshold': 0.9, #Relaying threshold (90%)
'disk_threshold': 0.9, # Disc threshold (90%)

# Parameters Rollback
'backup_path': '../model_backups', #A way for backup copies
'max_versions': 10, # Maximum number of versions
'backup_retention_days': 30 #Reserve copy days
}

# Launch system
async def main():
 system = CompleteRetrainingsystem(config)
 await system.initialize()

if __name__ == "__main__":
 asyncio.run(main())
```

## Best practices retraining

<img src="images/optimized/robustness_Analesis.png" alt="Best practices retraining" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Figure 6: Best practices and recommendations for retraining models*

# Why are best practices retraining important? # 'Cause wrong retraining can compromise model quality:

- **Planning**: Careful Planning Retraining Strategy
**Texting**: Integrated testing of new models
- **validation**: quality check on independent data
- **documentation**: Detailed documentation of the process
**Version**: Monitoring model and data versions
- **Rollback**: Possible rapid return to previous version
- **Monitoring**: Continuous quality tracking

### ♪ Key principles for successful retraining

♪ Why do you follow the best practices ♪ ♪ 'Cause they're tested by experience and help avoid problems ♪

- ** The principle of "stability"**: progressive introduction of changes
- ** "validation" principle**: Mandatory heck of quality
- ** Rollback principle**: Opportunity for rapid return
- **Monitoringa principle**: Continuous monitoring of the process
- ** Documentation principle**: Detailed fixation of all changes
- ** "Texting" principle**: Integrated check before implementation

### ♪ Detailed guide on setting parameters

**Why is it important to set the parameters right?** Because incorrect configurization can lead to inefficient re-learning or deterioration of model quality.

#### parameters performance

##### performance_threshold (0.0-1.0)

- **0.95-0.99**: Critical systems (health, finance, safety)
- **.90-0.94**: Highly loaded systems (recommendations, search)
- **0.80-0.89**: Standard Business Tasks (classification, regression)
- **0.70-0.79**: Experimental models (A/B testing)
- **0.60-0.69**: Prototypes and research

##### drift_threshold (0.0-1.0)

- **.05-0.10**: Very sensitive detective (rapidly changing data)
**0.10-0.20**: Standard sensitivity (recommended)
**0.20-0.30**: Low sensitivity (stable systems)
- **0.30-0.50**: Very low sensitivity (critical only)

#### Parameters of time

##### Retraining_interval days

- **1**: Daily - for fast-changing data (finance, news, social media)
- **3-7**: Weekly - for most business tasks (recommendations, forecasting)
**14-30**: Monthly - for stable domains (health, education)
**60-90**: Quarterly - for very stable systems (scientific research)

##### max_retraining_time (seconds)

**1800 (30 minutes)**: Simple models on small data
**3600 (1 hour)**: Standard models (recommended)
**7200 (2 hours)**: Complex models on Big Data
- **14400 (4 hours)**: Very complex models (deep learning)
- **28800 (8 hours)**: Extremely large datasets

#### quality parameters

##### improvement_threshold (0.0-1.0)

- **0.0**: Any improv (pilot approach)
**0.01 (1 per cent)**: Minimum improve (conservative approach)
**.02 (2 per cent)**: Standard improve (recommended)
**.05 (5 per cent)**: Significant improve (aggressive approach)
**0.10 (10%)**: Only significant improvements (very conservative)

##### stability_threshold (0.0-1.0)

- **0.99**: Very high stability (critical systems)
- **0.95**: High stability (recommended for sale)
**0.90**: Average stability (acceptable for most tasks)
- **0.85**: Low stability (for experiments only)

#### parameters resources

##### cpu_threshold, memory_threshold, disk_threshold (0.0-1.0)

- **0.95**: Critically high thresholds (maximum use of resources)
- **0.90**: High thresholds (recommended for sale)
- **0.80**: Average thresholds (maturity and stability balance)
- **0.70**: Low thresholds (conservative approach)

#### Parameters Rollback

##### max_versions (number)

- **5**: Minimum number of versions (savings of space)
**10**: Standard quantity (recommended)
- **20**: A large number of versions (detail history)
**50**: Maximum quantity (full history of changes)

#### Backup_retention_days (days)

- **7**: Short-term storage (rapid remove)
- **30**: Standard storage (recommended)
**90**: Long-term storage (detail history)
- **365**: Maximum storage (full history)

#### # Table of recommendations on choice of parameters

♪ Type of system ♪ ♪ performance_threshold ♪ ♪ drift_threshold ♪ retraining_interval ♪ max_retraining_time ♪
|-------------|----------------------|-----------------|-------------------|-------------------|---------------------|
♪ Critical** (medical, financial) ♪ 0.95-0.99 ♪ 0.05-0.10 ♪ 1-3 days ♪ 3600-7200s ♪ 0.01-0.02 ♪
* High load** (recommendations, search) * 0.90-0.94 * 0.10-0.15 * 3-7 days * 3600-14400s * 0.02-0.05
♪ Standard business** (classification, regression) ♪ 0.80-0.89 ♪ 0.15-0.25 7-14 days ♪ 7200-14400s ♪ 0.02-0.05 ♪
*Experimental** (A/B testing) *0.70-0.79 * 0.20-0.30 * 14-30 days * 14400-28800s * 0.05-0.10
* Research** (prototypes, R&D) * 0.60-0.69 * 0.25-0.40 * 30-90 days * 28,800s + ~ 0.10+ ~ ~ ~ ~

#### * examples configuration for different scenarios

**configuring for financial systems (high accuracy, rapid response):**

```python
financial_config = {
 'performance_threshold': 0.95,
 'drift_threshold': 0.08,
'retraining_interval': 1, # every day
'max_retraining_time': 3600, #1 hour
 'improvement_threshold': 0.01,
 'stability_threshold': 0.99,
 'cpu_threshold': 0.95,
 'memory_threshold': 0.90,
 'disk_threshold': 0.85
}
```

**configuring for recommendatory systems (balance of accuracy and performance):**

```python
recommendation_config = {
 'performance_threshold': 0.85,
 'drift_threshold': 0.15,
'retraining_interval': 7, #weekly
'max_retraining_time': 7,200, #2 hours
 'improvement_threshold': 0.02,
 'stability_threshold': 0.95,
 'cpu_threshold': 0.90,
 'memory_threshold': 0.85,
 'disk_threshold': 0.80
}
```

**configuring for research projects (flexibility and experiments):**

```python
research_config = {
 'performance_threshold': 0.70,
 'drift_threshold': 0.30,
'retraining_interval': 30, # monthly
'max_retraining_time': 14400, #4 hours
 'improvement_threshold': 0.05,
 'stability_threshold': 0.90,
 'cpu_threshold': 0.80,
 'memory_threshold': 0.75,
 'disk_threshold': 0.70
}
```

## Next steps

Once re-training models have been developed, go to:
- [best practice](.08_best_practices.md)
- [Examples of use](./09_examples.md)
- [Troubleshooting](./10_Troubleshooting.md)
