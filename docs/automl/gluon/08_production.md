# Sold and failed AutoML Gluon models

**Author:** Shcherbyna Rostyslav
**Date:** 2024

## Who's sold critical

**Why does 87% of ML models never get in sales?** Because their creators don't understand that model learning is only 20% of the work. The remaining 80% are product preparation, Monitoring and support.

### Catastrophic Consequences bad sales
- **Microsoft Tay**: AI chatbot became racist in 24 hours in sales.
- **Amazon HR**: AI-system discriminated against women in recruitment
- **Uber self-directed car**: pedestrian death due to model malfunction
- **Facebook algorithm**: Dissemination of fairy news due to poor validation

### The benefits of the right product
- **Stability**: The Workinget model with any data volume
- ** Reliability**: 99.9% uptime, automatic recovery
- **Monitoring**: Ongoing quality control of preferences
- ** Business value**: Real benefits for company and users

## Introduction in sales

<img src="images/optimized/production_architecture.png" alt="Style"="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 1: Architecture sold by AutoML Gluon*

Because the ML models are not just code, and the living systems that learn and change. It's like the difference between the plant and the garden is the Workinget on Plan, and the garden requires constant care.

**Unique features of ML sold:**
- **data changes**: The model can forget what it knew.
- ** Conceptual drift**: Reality changes faster than model
- **dependency from data**: No data = no preferences
- It's hard to understand why the model made the decision.

The sale of ML models is a critical step that requires careful Planning, Monitoring and Support. In this section, we will look at all aspects of AutoML Gloon models in sales.

## Preparation of the model for sale

<img src="images/optimized/performance_comparison.png" alt="Optimization of models" style="max-width: 100 per cent; exercise: auto; display: block; marguin: 20px auto;">
♪ Figure 2: Optimization of models for sales ♪

** Why is optimization of models for sales important?** Because the sales are completely different in terms of performance, memory and speed.

### ♪ Qualitative aspects of optimization

Why would a model that's great at Working in Jupyter fail in a sale?

- **Performance**: Speed of productions is critical
- ** Memory**: Limited server resources
- ** Model size**: To be placed in a container
- **Stability**: Working on different servers and environments
- ** Capacity**: Processing of large volumes of requests
- ** Reliability**: failure and recovery

### Model optimization

** Problems of non-optimized models in sales:**
- ** Slow predictions**: 5 seconds instead of 50ms - users will leave
- ** High memory consumption**: server drops under load
- ** Large model size**: not placed in container
- ** Instability**: The Workinget model is unstable on different servers

**methods model optimization:**
- **Quantification**: Reduction in balance accuracy (float32 \float16)
- **Pruning**: remove unimportant neurons
- **Distillation**: Learning a small model on a large
- **Optimization of architecture**: Selection of more effective algorithms

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# rent optimized model for sale
def create_production_model(train_data, target_col):
""create model optimized for sale""

 predictor = TabularPredictor(
 label=target_col,
 problem_type='auto',
 eval_metric='auto',
path='./production_models' # Separate folder for model sales
 )

# Learning with Optimization for Action
 predictor.fit(
 train_data,
== sync, corrected by elderman == @elder_man
Time_limit=3600, #1 hour - limitation of time of study
num_bag_folds=3, # Less folds for speed
 num_bag_sets=1,
 ag_args_fit={
'num_cpus': 4, #CPU restriction for stability
'num_gpus': 0, # Disable GPU for compatibility
'Memory_limit': 8 #Restriction of memory in GB
 }
 )

 return predictor
```

**/ Detailed descrie parameters for optimization of models for sale:**

**function create_production_model:**
- ** Designation**: creative model optimized for sale
- **parameters**:
- **'training_data'**: data for learning
-** Type**: DataFrame
- **describe**: Table with learning data
** Requirements**: Must contain a target variable
- **'target_col'**: Name of target variable
- **Typ**: str
- **describe**: Name of column with target variable
- **Return value**: TabularPredictor - Optimized Model

**parameters TabularPredictor:**
- **'label'**: Name of target variable
- **Typ**: str
- **describe**: Column with target variable for prediction
- **'problem_type'**: Type of task
- **Typ**: str
- ** Value**: 'auto', 'binary', 'multiclass', 'regression'
- **on default**: 'auto'
- **describe**: AutoGluon automatically determines the type of task
- ** `eval_metric'**: Meteric for quality assessment
- **Typ**: str
- ** Value**: 'auto', 'accuracy', 'f1', 'roc_auc', 'rmse', 'mae'
- **on default**: 'auto'
- **describe**: Automatic choice of methods on the type of task
- **'path'**: Path for model preservation
- **Typ**: str
- **describe**: Directorate for the preservation of model profiles
- ** Recommendations**: Use separate folder for model sales

**parameters predictor.fit():**
- **'presets'**: Pre-established Settings
- **Typ**: str
- ** Value**: 'optimize_for_development', 'best_quality', 'high_quality', 'good_quality', 'media_quality', 'optimise_for_sise'
- **describe**: 'optimise_for_development' optimizes the model for sale
- **'time_limit'**: Limiting time of study
- **Typ**:int
- ** Value range**: `[60, 86400] ` (1 minutes - 24 hours)
- **on default**: 3600 (1 hour)
- ** Recommendations**: For sale of Use 1-2 hours
- **'num_bag_folds'**: Number of folds for validation
- **Typ**:int
- ** Value range**: `[2, 10]' (recommended 3-5)
- **on default**: 8
- ** Recommendations**: for the sale of Use 3-5 folds
- **'num_bag_sets'**: Number of sets of folds
- **Typ**:int
- ** Value range**: `[1, 5] ` (recommended 1-2)
- **on default**: 1
- ** Recommendations**: for sale of Use 1 set

**parameters ag_args_fit:**
**'num_cpus'**: Number of KPU for training
- **Typ**:int
- ** Value range**: `[1, 32] ` (recommended 2-8)
- **on default**: 4
- ** Recommendations**: for sale to Us 2-4 CPU
- **'num_gpus'**: Number of GPUs for learning
- **Typ**:int
- ** Value range**: `[0,8]' (recommended 0-2)
- **on default**: 0
- ** Recommendations**: for sale turn off the GPU for compatibility
- **/memory_limit'**: Memory Restriction in GB
- **Typ**:int
- ** Value range**: `[1, 64] ` (recommended 4-16)
- **on default**: 8
- ** Recommendations**: for sale of Use 4-8 GB

**Why are resource constraints important?** Because servers are sold with limited resources, and the model has to Work in this framework.

♪ ♪ Model compression ♪

```python
def compress_model(predictor, model_name):
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Maintaining a compressed model
 predictor.save(
 model_name,
 save_space=True,
 compress=True,
 save_info=True
 )

# Getting model size
 import os
 model_size = os.path.getsize(f"{model_name}/predictor.pkl") / (1024 * 1024) # MB
 print(f"Model size: {model_size:.2f} MB")

 return model_size
```

**/ Detailed descrie of model compression parameters: **/

**function compress_model:**
- ** Designation**: Compression of the model for reducing the size of the fillets
- **parameters**:
- ** `predicator'**: Trained model
- ** Type**: TabularPredictor
- **describe**: AutoGluon model trained
- **'model_name'**: Name for model retention
- **Typ**: str
- **describe**: Path and name for maintaining a compressed model
- **Return value**: float - model size in MB

**parameters predictor.save():**
- **'model_name'**: Model name
- **Typ**: str
- **describe**: Way to preserve the model
- ** Recommendations**: Use descriptive names with versions
- **'save_space'**: Size optimization
-**Teep**: bool
- **on default**: True
- **describe**: Removes temporary files for space saving
- **Effluence**: Decreases model size on 20-30%
- **/ `comppress'**: Files compression
-**Teep**: bool
- **on default**: True
- **describe**: uses gzip compression for file models
- **Effluence**: Decreases model size on 40-60%
- **'save_info'**: Retention of model information
-**Teep**: bool
- **on default**: True
- **describe**: Maintains metadata on the model
- ** Use**: Need for model loading and debugging

**methods compression:**
- **remove time files**: cross intermediate results
- **Gzip compression**: Model Files compression
- **Optimization of weights**: remove non-Use parameters
- **Quantification**: Reduction in balance accuracy (float32 \float16)

♪## Validation of the model

```python
def validate_production_model(predictor, test_data, performance_thresholds):
"Validation Model for Sale"

# Premonition
 predictions = predictor.predict(test_data)

# Quality assessment
 performance = predictor.evaluate(test_data)

# check threshold values
 validation_results = {}
 for metric, threshold in performance_thresholds.items():
 if metric in performance:
 validation_results[metric] = performance[metric] >= threshold
 else:
 validation_results[metric] = False

# Check stability preferences
 if hasattr(predictor, 'predict_proba'):
 probabilities = predictor.predict_proba(test_data)
 prob_std = probabilities.std().mean()
validation_results['stability'] = prob_std < 0.1 # Stability of probabilities

 return validation_results, performance
```

**/ Detailed describe parameters of validation model for sale:**

**function validate_production_model:**
- ** Designation**: Validation of the model prior to the performance in sales
- **parameters**:
- ** `predicator'**: Trained model
- ** Type**: TabularPredictor
- **describe**: Model for validation
- ** `test_data'**: test data
-** Type**: DataFrame
- **describe**: data for model testing
** Requirements**: Should contain a target variable
- ** `Performance_thresholds'**: Metric threshold values
- ** Type**: dict
- **describe**: dictionary with minimum metric values
 - **example**: {'accuracy': 0.85, 'f1': 0.80, 'roc_auc': 0.90}
- **Return value**: tuple - (validation_effects, performance)
- **/ `validation_results'**: dict - results of validation
- **`performance`**: dict - Metrics performance

**Structure validation_results:**
- **'metric_name'**: bool - results of the metrics test
- **True**: Meteric exceeds the threshold
- **False**: Metrique below threshold
- ** `Stability'**: bool - stability of preferences
- **True**: Standard probability deviation < 0.1
- **False**: High instability of preferences

**Structure performance:**
- **metrics classification**: accuracy, precion, recall, f1, roc_auc
- **metrics regression**: rmse, mae, r2, mape
- **Castom metrics**: Any metrics defined in training

**Validation checks:**
- ** Thresholds**: comparison metric with minimum requirements
- **Stability**: Analysis of the spread of probabilities
- **formance**: Speed evaluation of productions
- ** Memory**: heck of memory use
- **Compatibility**: Testing on different platforms

## API server for sale

###FastAPI server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from typing import Dict, List, Any
import asyncio
from datetime import datetime

# configuring Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI applications
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Global variable for the model
model = None

class PredictionRequest(BaseModel):
"The Request Scheme for Prophecy."
 data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
""Scheme of response with predictions."
 predictions: List[Any]
 probabilities: List[Dict[str, float]] = None
 model_info: Dict[str, Any]
 timestamp: str

class healthResponse(BaseModel):
"""""""""""""""""""
 Status: str
 model_loaded: bool
 model_info: Dict[str, Any] = None

** Detailed describe of FastAPI server parameters:**

**FastAPI application:**
- ** `title'**: Name of API
- **Typ**: str
- **describe**: Imaged in Swagger documentation
- ** Recommendations**: Use descriptive name
- ** `version'**: API version
- **Typ**: str
- **describe**: API version for tracking change
- ** Recommendations**: Us semantic versioning (1.0.0)

**Class PromotionRequest:**
- **'data'**: data for prediction
== sync, corrected by elderman == @elder_man
- **describe**: List of fortunes
- **Structure**: Every entry is a dictionary with signature
 - **example**: [{"feature1": 1.0, "feature2": 2.0}, {"feature1": 3.0, "feature2": 4.0}]

**Class PradicationResponse:**
- **'predications'**: Model predictions
- ** Type**: List[Any]
- **describe**: List instructions for each record
- **'probabyties'**: Probability of preferences
== sync, corrected by elderman == @elder_man
**describe**: Probability for each class (for classification only)
 - **Structure**: [{"class1": 0.8, "class2": 0.2}, ...]
- **'model_info'**: Model Information
- ** Type**: Dict[str, Any]
- **describe**: Metadata on the model
- **'timestamp'**: Time of prediction
- **Typ**: str
- **describe**: ISO prediction time format

**Class healthResponse:**
- ** `status'**: Status of API
- **Typ**: str
- ** Values**: "healthy", "unhealthy"
- **describe**: General status of API
- **'model_loaded'**: model loading status
-**Teep**: bool
- **describe**: Are the model loaded
- **'model_info'**: Model Information
== sync, corrected by elderman == @elder_man
- **describe**: Metadata on the model (only if the model is loaded)

@app.on_event("startup")
async def load_model():
"""""""""""""""""""""
 global model
 try:
 model = TabularPredictor.load('./production_models')
 logger.info("Model loaded successfully")
 except Exception as e:
 logger.error(f"Failed to load model: {e}")
 model = None

@app.get("/health", response_model=healthResponse)
async def health_check():
 """health check endpoint"""
 if model is None:
 return healthResponse(
 status="unhealthy",
 model_loaded=False
 )

 return healthResponse(
 status="healthy",
 model_loaded=True,
 model_info={
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric
 }
 )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
 """Endpoint for predictions"""
 if model is None:
 raise HTTPException(status_code=503, detail="Model not loaded")

 try:
# Data conversion in dataFrame
 df = pd.dataFrame(request.data)

# Premonition
 predictions = model.predict(df)

# Probabilities (if available)
 probabilities = None
 if hasattr(model, 'predict_proba'):
 proba = model.predict_proba(df)
 probabilities = proba.to_dict('records')

# Model information
 model_info = {
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric,
 "num_features": len(df.columns)
 }

 return PredictionResponse(
 predictions=predictions.toList(),
 probabilities=probabilities,
 model_info=model_info,
 timestamp=datetime.now().isoformat()
 )

 except Exception as e:
 logger.error(f"Prediction error: {e}")
 raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
""""""""" "model information"""
 if model is None:
 raise HTTPException(status_code=503, detail="Model not loaded")

 return {
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric,
 "feature_importance": model.feature_importance().to_dict()
 }

if __name__ == "__main__":
 import uvicorn
 uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Flask server

```python
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
import traceback

# configuring Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Global variable for the model
model = None

def load_model():
"""""""""""""
 global model
 try:
 model = TabularPredictor.load('./production_models')
 logger.info("Model loaded successfully")
 return True
 except Exception as e:
 logger.error(f"Failed to load model: {e}")
 return False

@app.route('/health', methods=['GET'])
def health_check():
 """health check endpoint"""
 if model is None:
 return jsonify({
 "status": "unhealthy",
 "model_loaded": False
 }), 503

 return jsonify({
 "status": "healthy",
 "model_loaded": True,
 "model_info": {
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric
 }
 })

@app.route('/predict', methods=['POST'])
def predict():
 """Endpoint for predictions"""
 if model is None:
 return jsonify({"error": "Model not loaded"}), 503

 try:
# Data acquisition
 data = request.get_json()

 if 'data' not in data:
 return jsonify({"error": "No data provided"}), 400

# Transforming in dataFrame
 df = pd.dataFrame(data['data'])

# Premonition
 predictions = model.predict(df)

# Probabilities (if available)
 probabilities = None
 if hasattr(model, 'predict_proba'):
 proba = model.predict_proba(df)
 probabilities = proba.to_dict('records')

 return jsonify({
 "predictions": predictions.toList(),
 "probabilities": probabilities,
 "model_info": {
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric
 },
 "timestamp": datetime.now().isoformat()
 })

 except Exception as e:
 logger.error(f"Prediction error: {e}")
 logger.error(traceback.format_exc())
 return jsonify({"error": str(e)}), 500

@app.route('/model/info', methods=['GET'])
def model_info():
""""""""" "model information"""
 if model is None:
 return jsonify({"error": "Model not loaded"}), 503

 return jsonify({
 "model_path": model.path,
 "problem_type": model.problem_type,
 "eval_metric": model.eval_metric,
 "feature_importance": model.feature_importance().to_dict()
 })

if __name__ == "__main__":
 if load_model():
 app.run(host="0.0.0.0", port=8000, debug=False)
 else:
 logger.error("Failed to start server - model not loaded")
```

## Docker containerization

<img src="images/optimized/simple_production_flow.png" alt="Containment and deplete" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Picture 3: Containerization and strategies for ML models*

**Why is containerization for ML models important?** Because it ensures consistency and isolation:

- **Consistence**: Same environment on all servers
- **Isolation**: Model nnot affects other applications
- ** Portability**: It's easy to move between servers
- ** Capacity**: Simple horizontal scale
- **Version**: Model version control and dependencies
- ** Safety**: Isolated implementation environment

### Dockerfile for sale

```dockerfile
# Dockerfile for sale
FROM python:3.9-slim

♪ system systems installation ♪
RUN apt-get update && apt-get install -y \
 gcc \
 g++ \
 && rm -rf /var/lib/apt/Lists/*

# Create Work Directorate
WORKDIR /app

# Copying copies
COPY requirements.txt .

# installation Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# creative User for security
RUN Useradd -m -u 1000 appUser && chown -R appUser:appUser /app
User appUser

# Opening the port
EXPOSE 8000

# Launch team
CMD ["python", "app.py"]
```

** Detailed describe of Docker containerization parameters:**

**Dockerfile instructions:**
- **'FROM python: 3.9-slim'**: Basic image
- **describe**: Using Python 3.9 on Debian slim
**Measurement**: ~150MB (compact image)
- ** Benefits**: Rapid loading, minimum surface attack
**/ `RUN apt-get update &&apt-get install -y'**: installation of system dependencies
- **'gcc'**: Compier C for Python Package Assembly
- **'g++'**: Compier C++ for Python Package Assembly
- **'&& rm -rf /var/lib/apt/Lists/***: clean cache apt for size reduction
- **/WORKDIR /app'**: Work Directorate
- **describe**: Sets /app as the work directorate
- ** Benefits**: Isolates application files
- **/COPY compilations.txt.'**: Copying file dependencies
- **describe**: Copys corrections.txt in container
- ** Benefits**: Cashing the Docker layers
- **`RUN pip install --no-cache-dir -r requirements.txt`**: installation Python dependencies
- **'--no-cache-dir'**: Disables cache pip for size reduction
- ** Benefits**: Decreases the size of the image on 50-100MB
- **'COPY ..'**: Copying the application code
- **describe**: Copys the entire application code in container
- ** Recommendations**: Use .dockerignore for the elimination of unnecessary files
- **`RUN Useradd -m -u 1000 appUser && chown -R appUser:appUser /app`**: create User
- **'-m'**: Creates a household directory
- ** `-u 1000'**: Sets UID 1000
- **///////: Changed owner of all files
- ** Safety**: Launch not from root User
- **'User appUser'**: Switch on User
- **describe**: Switched to created User
- ** Safety**: restricts access rights
- **'EXPOSE 8000'**: Opening port
- **describe**: Documents that port 8,000 uses application
- **Note**: not automatically opens port
- **/CMD ["python", "app.py"]**: Team Launch
- **describe**: Launch application when the container starts
- **Format**: JSON Set for Avoiding Shell Interpretation

### Docker Composition for sale

```yaml
# docker-compose.prod.yml
Version: '3.8'

services:
 autogluon-api:
 build: .
 ports:
 - "8000:8000"
 environment:
 - MODEL_PATH=/app/models
 - LOG_LEVEL=INFO
 volumes:
 - ./models:/app/models
 - ./Logs:/app/Logs
 restart: unless-stopped
 healthcheck:
 test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
 interval: 30s
 timeout: 10s
 retries: 3
 start_period: 40s

 nginx:
 image: nginx:alpine
 ports:
 - "80:80"
 - "443:443"
 volumes:
 - ./nginx.conf:/etc/nginx/nginx.conf
 - ./ssl:/etc/nginx/ssl
 depends_on:
 - autogluon-api
 restart: unless-stopped

 redis:
 image: redis:alpine
 ports:
 - "6379:6379"
 volumes:
 - redis_data:/data
 restart: unless-stopped

volumes:
 redis_data:
```

** Detailed describe parameters Docker Compose:**

**Docker Compose version:**
- ** 'Version: `3.8''**: File format version
- **describe**: Uses the Docker Composition version 3.8 format
- ** Benefits**: Support for new functions and improved compatibility

** Services autogluon-api:**
- **'bueld: ..'**: Image collection
- **describe**: Collects an image from Dockerfile in the current directory.
- ** Alternatives**: Can use `image: name_form' for ready image
- **'ports'**: Ports
- ** `"8000:8000'"**: Throws through port 8,000 containers on port 8,000
- **Format**: Host: Container.
- ** `environment'**: Changing environment
- ** `MODEL_PATH=/app/models'**: Path to models in container
- **'LOG_LEVEL=INFO'**: Logs level
- **'volumes'**: To complete volumes
- ** `./models:/app/models'**: Mounts a local folder of models in container
- ** `./Logs:/app/Logs'**: Mounts a local Logs folder in a container
- **/restart: unless-stepped'**: OverLaunch policy
- **describe**: OverLaunch container in failure other than manual stop
- ** Alternatives**: allways, on-failure, no
- **`healthcheck`**: health check
- ** `test'**: Health Check Team
- **'interval: 30s'**: Verification interval
- **'timeout: 10s'**: Timeout team
- **'retries: 3'**: Number of attempts
- **'start_period: 40s'**: waiting time before first check

** Service nginx:**
- **'image: nginx:alpine'**: Ready image of Nginx
- **describe**: Using Alpine Linux version of Nginx
- ** Measure**: ~15MB (compact image)
- **'ports'**: Ports
- **'80:80'**: HTTP port
- **'443:443'**: HTTPS port
- **/volumes'**: configuration
 - **`./nginx.conf:/etc/nginx/nginx.conf`**: configuration Nginx
- **/ssl:/etc/nginx/ssl'**: SSL certificates
- **`depends_on`**: dependencies
- **'autogluon-api'**: Nginx Launch after API service

** Service redis:**
- **'image: redis:alpine'**: Ready image of Redis
- **describe**: uses the Alpine Linux version of Redis
- **Measure**: ~7MB (compact image)
- ** `volumes'**: Permanent storage
**'redis_data:/data'**: Named volume for data Redis

**Toma:**
**'redis_data'**: Named volume
- **describe**: Creates a permanent volume for Redis data
- ** Benefits**: data retained by overLaunch containers

## Kubernetes is good

###Deployment manifesto

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: deployment
metadata:
 name: autogluon-api
 labels:
 app: autogluon-api
spec:
 replicas: 3
 selector:
 matchLabels:
 app: autogluon-api
 template:
 metadata:
 labels:
 app: autogluon-api
 spec:
 containers:
 - name: autogluon-api
 image: autogluon-api:latest
 ports:
 - containerPort: 8000
 env:
 - name: MODEL_PATH
 value: "/app/models"
 - name: LOG_LEVEL
 value: "INFO"
 resources:
 requests:
 memory: "1Gi"
 cpu: "500m"
 limits:
 memory: "2Gi"
 cpu: "1000m"
 livenessProbe:
 httpGet:
 path: /health
 port: 8000
 initialDelaySeconds: 30
 periodseconds: 10
 readinessProbe:
 httpGet:
 path: /health
 port: 8000
 initialDelaySeconds: 5
 periodseconds: 5
 volumeMounts:
 - name: model-storage
 mountPath: /app/models
 - name: log-storage
 mountPath: /app/Logs
 volumes:
 - name: model-storage
 persistentVolumeClaim:
 claimName: model-pvc
 - name: log-storage
 persistentVolumeClaim:
 claimName: log-pvc
---
apiVersion: v1
kind: service
metadata:
 name: autogluon-api-service
spec:
 selector:
 app: autogluon-api
 ports:
 - protocol: TCP
 port: 80
 targetPort: 8000
 type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
 name: model-pvc
spec:
 accessModes:
 - ReadWriteOnce
 resources:
 requests:
 storage: 10Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
 name: log-pvc
spec:
 accessModes:
 - ReadWriteOnce
 resources:
 requests:
 storage: 5Gi
```

**/ Detailed describe of the Kubernetes parameters:**

**deployment manifesto:**
- **'apiVersion: Apps/v1'**: API version
- **describe**: Uses a stable version of API for release
- **'kind: release'**: Resource type
- **describe**: Creates a déployment for the management of subs.
- **'metadata.name'**: Name
- **describe**: Unique name for identification
- **'spec.replicas: 3'**: Number of replicas
- **describe**: Creates 3 copies of the application
- ** Benefits**: High accessibility and load capacity
- **'spec.selector.matchLabels'**: Substrate Selector
- **describe**: Selects sub-marks with appropriate labels
- **'spec.template'**: Shablon pump
- **describe**: Determines the configuration of the substrates

**Container:**
- **'name: autogluon-api'**: Name of container
- **describe**: Unique name of the container in subpoena
- **'image: autogluon-api:latest'**: Image of container
- **describe**:Docker image for Launch
- ** Recommendations**: Use specific tags of versions instead of latest
- **'ports.containerPort: 8,000'**: Port container
- **describe**: Port that listens to application
- ** `env'**: Changing environment
- **'MODEL_PATH'**: Path to models in container
- **'LOG_LEVEL'**: Logs level

** Resources:**
- **/resources.requests'**: Minimum resources
- **/memory: "1Gi"'**: Minimum 1GB RAM
- **'cpu: "500m"'**: Minimum 0.5 CPU
- **/resources.limits'**: Maximum resources
- **/memory: "2Gi"'**: Maximum 2GB RAM
- **'cpu: "1000m"'**: Maximum 1 CPU

** Checks health:**
- ** 'LifeProbe'**: check viability
- ** `httpGet'**: HTTP request for verification
- **/path: /health'**: Path for verification
- **'port: 8,000'**: Port for inspection
- **'InitialDelaySeends: 30'**: Delay before first check
- **'periodseconds: 10'**: Verification interval
- **/'re-businessProbe'**: check ready
- **describe**: Checks whether the container is ready to accept traffic
- **'InitialDelaySeends: 5'**: Rapid check readiness

**Toma:**
- **'volumeMounts'**: In-containers booking
- **'model-storage'**: Tom for models
- **'log-storage'**: Tom for logs
- **/volumes'**: Definition of volumes
**/ `Persistent VolumeClaim'**: Use of PVC for permanent storage

**service:**
- **'kind: service'**: Resource type
- **describe**: Creates a service for access to the pens
- **'spec.selector'**: Substrate Selector
- **describe**: Picks for load balancing
- **'spec.ports'**: Ports Probe
- **'port: 80'**: External port
- **'targetPort: 8,000'**: Port container
- **'type: LoadBalencer'**: Type of service
- **describe**: Creates external LoadBalencer

**PersistentVolumeClaim:**
- **'kind: Personal VolumeClaim'**: Resource type
- **describe**: Request for permanent storage
- **'spec.accessModes'**: Access modes
- **'ReadWriteOnce'**: Reading/recording by one node
- **'spec.resources.requests.storage'**: Warehouse size
- **'10Gi'**: 10GB for models
- **'5Gi'**: 5GB for logs

♪ Monitoring and Logsting

<img src="images/optimized/addianced_production_flow.png" alt="Monitoring and Logsrration" style="max-width: 100 per cent; height: auto; display: block; marguin: 20px auto;">
*Picture 4: Monitoring and Logs in Production*

Because models can degenerate over time:

** Drift Detective**: Change in input data distribution
- **Monitoring performance**: Speed and accuracy tracking
**Alerting**: notes on real-time problems
- **Logstration**: Detailed information for debugging
- **metrics business**: Technical metrics with business outcomes
- **Automatic recovery**: Response on the problem without human intervention

### The Monitoring System

```python
import logging
import time
from datetime import datetime
import psutil
import requests
from typing import Dict, Any

class ProductionMonitor:
"Monitoring the system sold."

 def __init__(self, log_file='production.log'):
 self.log_file = log_file
 self.setup_logging()
 self.metrics = {}

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

 def log_Prediction(self, input_data: Dict, Prediction: Any,
 processing_time: float, model_info: Dict):
""Logsrance of Promise""
 log_entry = {
 'timestamp': datetime.now().isoformat(),
 'input_data': input_data,
 'Prediction': Prediction,
 'processing_time': processing_time,
 'model_info': model_info
 }
 self.logger.info(f"Prediction: {log_entry}")

 def log_error(self, error: Exception, context: Dict):
""Logsir of Mistakes""
 error_entry = {
 'timestamp': datetime.now().isoformat(),
 'error': str(error),
 'context': context,
 'traceback': traceback.format_exc()
 }
 self.logger.error(f"Error: {error_entry}")

 def get_system_metrics(self) -> Dict[str, Any]:
"Getting System Metericks."
 return {
 'cpu_percent': psutil.cpu_percent(),
 'memory_percent': psutil.virtual_memory().percent,
 'disk_percent': psutil.disk_usage('/').percent,
 'timestamp': datetime.now().isoformat()
 }

 def check_model_health(self, model) -> Dict[str, Any]:
""Health check model""
 try:
# Testsy Pradition
 test_data = pd.dataFrame({'feature1': [1.0], 'feature2': [2.0]})
 start_time = time.time()
 Prediction = model.predict(test_data)
 processing_time = time.time() - start_time

 return {
 'status': 'healthy',
 'processing_time': processing_time,
 'timestamp': datetime.now().isoformat()
 }
 except Exception as e:
 return {
 'status': 'unhealthy',
 'error': str(e),
 'timestamp': datetime.now().isoformat()
 }
```

**/ Detailed describe parameters of Monitoring system:**

**Class ProductionMonitor:**
- ** Designation**: Monitoring sold by AutoML Gluon
- **parameters of design**:
- **'log_file'**: Path to log file
- **Typ**: str
- **on default**: 'production.log'
- **describe**: File for recording Monitoring's logs

** Method setup_logging():**
- ** Designation**: configuring Logs
- **parameters logging.basicConfig():**
- **'level=logging.INFO'**: Logs level
- **Typ**:int
- ** Values**: DEBUG(10), INFO(20), WARNING(30), EROR(40), CRITICAL(50)
- **describe**: Logs messages at INFO level and above
- ** `format'**: Log format
- **Typ**: str
- **describe**: Log formatting template
- **components**: Time, logger name, level, message
- ** `handlers'**: Lair processors
- **'FileHandler'**: Record in file
- **'StreamHandler'**: Conclusion in console

** Method log_Predication():**
- ** Designation**: Logs of model preferences
- **parameters**:
- **/input_data'**: input data
- ** Type**: Dict
- **describe**: Data, popata on model input
- **'Predition'**:Pedication model
-** Type**: Any
- **describe**: The result of the prediction
- ** `Processing_time'**: Processing time
- **Typ**: float
- **describe**: Time to execute prediction in seconds
- **'model_info'**: Model Information
- ** Type**: Dict
- **describe**: Metadata on the model

** Method log_error():**
- ** Designation**: System error logs
- **parameters**:
- ** `error'**: exclusion
- ** Type**: Exception
- **describe**: Error that occurred
- ** `contect'**: Context of error
- ** Type**: Dict
- **describe**: Additional information on error

** Get_system_metrics method():**
- ** Designation**: Acquisition of system metrics
- **Return value**: Dict[str, Any] - System metrics
- **metrics**:
- **'cpu_percent'**: Loading CPU
- **Typ**: float
- **band**: 0.0-100.0
- **describe**: Percentage of use of CPU
- **/memory_percent'**: Use of memory
- **Typ**: float
- **band**: 0.0-100.0
- **describe**: Percentage use of RAM
- **'disk_percent'**: Use of disc
- **Typ**: float
- **band**: 0.0-100.0
- **describe**: Percentage use of disk
- ** `timestamp'**: Time of measurement
- **Typ**: str
- **describe**: ISO time format

**Heck_model_health():**
- ** Designation**: health check model
- **parameters**:
- **'model'**: Model for verification
- ** Type**: TabularPredictor
- **describe**: AutoGluon for testing
- **Return value**: Dict[str, Any] - health status
- **Structure result**:
- ** `status'**: Model status
- **Typ**: str
- ** Values**: 'healthy', 'unhealthy'
- ** `Processing_time'**: Time to process test request
- **Typ**: float
- **describe**: Time to perform testis prophecy
- **'error'**: describe errors (if present)
- **Typ**: str
- **describe**: Mischecked error text

♪ ♪ Alerts and notes ♪

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class Alertsystem:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""Alerts for sales"""""""" """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, smtp_server, smtp_port, email, password):
 self.smtp_server = smtp_server
 self.smtp_port = smtp_port
 self.email = email
 self.password = password

 def send_email_alert(self, subject: str, message: str, recipients: List):
""Send e-mail allergic."
 try:
 msg = MIMEMultipart()
 msg['From'] = self.email
 msg['To'] = ', '.join(recipients)
 msg['Subject'] = subject

 msg.attach(MIMEText(message, 'plain'))

 server = smtplib.SMTP(self.smtp_server, self.smtp_port)
 server.starttls()
 server.login(self.email, self.password)
 server.send_message(msg)
 server.quit()

 print(f"Email alert sent to {recipients}")
 except Exception as e:
 print(f"Failed to send email alert: {e}")

 def send_slack_alert(self, webhook_url: str, message: str):
"Sent Sluck Alert."
 try:
 payload = {
 "text": message,
 "Username": "AutoML Gluon Monitor",
 "icon_emoji": ":robot_face:"
 }

 response = requests.post(webhook_url, json=payload)
 response.raise_for_status()

 print("Slack alert sent successfully")
 except Exception as e:
 print(f"Failed to send Slack alert: {e}")

 def check_performance_thresholds(self, metrics: Dict[str, float],
 thresholds: Dict[str, float]):
"Check threshold values performance""
 alerts = []

 for metric, threshold in thresholds.items():
 if metric in metrics and metrics[metric] < threshold:
 alerts.append(f"{metric} is below threshold: {metrics[metric]} < {threshold}")

 return alerts
```

**/ Detailed descrie parameters of the allernet system: **/

** Class Alertsysystem:**
- ** Designation**: Notification system for sales of Monitoringa
- **parameters of design**:
- **'smtp_server'**: SMTP server
- **Typ**: str
- **describe**: SMTP server address for email
 - **examples**: 'smtp.gmail.com', 'smtp.yandex.ru'
- **'smtp_port'**: SMTP server port
- **Typ**:int
- **on default**: 587 (TLS), 465 (SSL)
- **describe**: Port for SMTP server
- ** `email'**: Email sender
- **Typ**: str
- **describe**: Email address for sending notifications
- **'password'**: e-mail password
- **Typ**: str
- **describe**: Password for authentication on SMTP server

** Method send_email_alert():**
- ** Designation**: Send e-mail notifications
- **parameters**:
- **/ `subproject'**: Subject of the letter
- **Typ**: str
- **describe**: Email notes
 - **examples**: "Model Performance Alert", "system health Warning"
- ** `message'**: Text messages
- **Typ**: str
- **describe**: Content of e-mail notes
- **/recipients'**: List of recipients
- ** Type**: List
- **describe**: List email addresses of recipients
 - **example**: ['admin@company.com', 'devops@company.com']

** Method send_slack_alert():**
- ** Designation**: Sending notifications in Slack
- **parameters**:
 - **`webhook_url`**: URL webhook
- **Typ**: str
- **describe**: UrL Slack webhook for sending messages
- **Format**: https://hawks.slack.com/services/...
- ** `message'**: Text messages
- **Typ**: str
- **describe**: Content of Slack notes
- **Structure payload**:
- ** `text'**: Text messages
- ** `Username'**: Name of sender
- **'icon_emoj'**: sender's icon

**Check_performance_thresholds():**
- ** Designation**: check metric thresholds
- **parameters**:
- **'metrics'**: Current metrics
- ** Type**: Dict[str, float]
- **describe**: dictionary with current metric values
 - **example**: {'accuracy': 0.85, 'response_time': 0.5}
- ** `thresholds'**: Thresholds
- ** Type**: Dict[str, float]
- **describe**: dictionary with minimum metric values
 - **example**: {'accuracy': 0.90, 'response_time': 1.0}
- **Return value**: List - List allerts
- **Logs check**:
- Compares current metrics with thresholds
- Creates allerte if the metric is below the threshold.
- Returns the List line with the description of the problems

## Scale

<img src="images/optimized/producation_comparison.png" alt="ML systems scale" style="max-width: 100 per cent; light: auto; display: lock; marguin: 20px auto;">
♪ Figure 5: ML scaling strategies ♪

**Why is it important to scale ML systems correctly?** Because ML models have unique resource requirements:

- ** Horizontal scale**: add new servers for load processing
- ** Vertical scaling**: Increased resources of existing servers
- ** Automatic scaling**: Dynamic resource change on load
- ** Load budgeting**: Equitable distribution of queries between servers
- **Cashing**: Retaining results for validation of responses
- ** Asynchronous treatment**: Non-locking request processing

### Horizontal scale

```python
#configuring for horizontal scaling
import asyncio
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class Scalablepredictionservice:
"""""""" "Stop-up "predations""""

 def __init__(self, max_workers=4):
 self.max_workers = max_workers
 self.executor = ThreadPoolExecutor(max_workers=max_workers)
 self.request_queue = queue.Queue()
 self.result_queue = queue.Queue()

 async def process_Prediction(self, data: Dict) -> Dict:
"The Asynchronous Prophecy Processing."
 loop = asyncio.get_event_loop()

# The fulfillment of the prediction in a separate stream
 result = await loop.run_in_executor(
 self.executor,
 self._predict_sync,
 data
 )

 return result

 def _predict_sync(self, data: Dict) -> Dict:
"Synchronous Pride."
# Your Logs of Prophecy
 pass

 def batch_predict(self, batch_data: List[Dict]) -> List[Dict]:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 results = []

# Division on Batch
 batch_size = 100
 for i in range(0, len(batch_data), batch_size):
 batch = batch_data[i:i+batch_size]

# Side treatment of the batch
 with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
 futures = [executor.submit(self._predict_sync, data) for data in batch]
 batch_results = [future.result() for future in futures]
 results.extend(batch_results)

 return results
```

**/ Detailed describe scale parameters:**

** Class Scalablepredationservice:**
- ** Designation**: Large-scale service for processing preferences
- **parameters of design**:
- ** `max_workers'**: Maximum flow
- **Typ**:int
- **on default**: 4
- ** Value range**: `[1, 32] ` (recommended 2-16)
- **describe**: Number of parallel flows for processing
- ** Recommendations**: Use number of CPU kernels x 2

** Method of process_Predication():**
- ** Designation**: Asynchronous processing of prediction
- **parameters**:
- **'data'**: data for prediction
- ** Type**: Dict
- **describe**: input data for the model
- **Return value**: Dict - prediction result
- ** Specialities**:
- **Asynchronity**: not blocking the main flow
- ** Parallarity**: Using a separate flow for calculations
- ** Capacity**: Supports multiple requests

** Method _predict_sync():**
- ** Designation**: Synchronization of the prophecy
- **parameters**:
- **'data'**: data for prediction
- ** Type**: Dict
- **describe**: input data for the model
- **Return value**: Dict - prediction result
- ** Specialities**:
- ** Synchronity**: Blocking performance
- ** Flow safety**: May be performed in different flows
- ** Performance**: Optimized for rapid implementation

**Batch_predict():**
- ** Designation**: Multiplies package processing
- **parameters**:
- **'batch_data'**: List of data for prediction
- ** Type**: List[Dict]
- **describe**: List of input data
- **Return value**: List[Dict] - List of results
- **parameters processing**:
- **'batch_size'**: The dimensions of the batch
- **Typ**:int
- **on default**: 100
- ** Value range**: ` [10, 1000] ` (recommended 50-200)
- **describe**: Number of requests in one booth
- ** Specialities**:
- **Package**: Groupes requests for efficiency
- **Parallarity**: Processing boots in parallel
- ** Memory**: Controls the use of memory through the size of the batch

### Cashing

```python
import redis
import json
import hashlib
from typing import Any, Optional

class Predictioncache:
"Cash for Preventions."

 def __init__(self, redis_host='localhost', redis_port=6379, ttl=3600):
 self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
 self.ttl = ttl

 def _generate_cache_key(self, data: Dict) -> str:
""""""""""" "Cache key genetics""""
 data_str = json.dumps(data, sort_keys=True)
 return hashlib.md5(data_str.encode()).hexdigest()

 def get_Prediction(self, data: Dict) -> Optional[Dict]:
"To receive a prediction from cache."
 cache_key = self._generate_cache_key(data)
 cached_result = self.redis_client.get(cache_key)

 if cached_result:
 return json.loads(cached_result)

 return None

 def set_Prediction(self, data: Dict, Prediction: Dict):
"The preservation of the prediction in Cash."
 cache_key = self._generate_cache_key(data)
 self.redis_client.setex(
 cache_key,
 self.ttl,
 json.dumps(Prediction)
 )

 def invalidate_cache(self, pattern: str = "*"):
 """clean cache"""
 keys = self.redis_client.keys(pattern)
 if keys:
 self.redis_client.delete(*keys)
```

**/ Detailed describe cache parameters: **/

**Class Praditioncache:**
- ** Designation**: Cashing preferences for the collection of responses
- **parameters of design**:
- **'redis_host'**: Host Redis server
- **Typ**: str
- **on default**: 'localhost'
- **describe**: Redis server address for cache
- **'redis_port'**: Port Redis server
- **Typ**:int
- **on default**: 6379
- **describe**: Port for Redis connection
- ** `ttl'**: Lifetime cache
- **Typ**:int
- **on default**: 3600 (1 hour)
- ** Value range**: `[60, 86400] ` (1 minutes - 24 hours)
- **describe**: Time in seconds when the cache runs out

** Method _generate_cache_key():**
- ** Designation**: Generation of a unique key for cache
- **parameters**:
- **'data'**: data for prediction
- ** Type**: Dict
- **describe**: Entry data for key generation
- **Return value**: str - MD5 hash key
- **Algorithm**:
- Serializes data in JSON with key sorting
- Creates MD5 hash from data lines
- Returns 32-symbol hash.

** Get_Predication method():**
- ** Designation**: Retrieving a prediction from cache
- **parameters**:
- **'data'**: data for searching
- ** Type**: Dict
- **describe**: Incoming data for cache searches
- **Return value**: Operational[Dict] - result from cache or None
- **Logsty work**:
- Generates the cache key from the data.
- Looking for a value in Redis
- Deserializes JSON in dictionary
- Returns None if the key is not present.

** Method set_Predication():**
- ** Designation**: Retaining prediction in Cash
- **parameters**:
- **'data'**: input data
- ** Type**: Dict
- **describe**: data for key generation
- **'Predication'**: The result of the prediction
- ** Type**: Dict
- **describe**: Implementation for preservation
- ** Specialities**:
- Uses `setex' to install TTL
- Serialized Selection in JSON
- Automatically expires via TTL

** Method of invalidate_cache():**
- ** Designation**: clean cache
- **parameters**:
- **'pattern'**: Pattern for key search
- **Typ**: str
- **on default**: "*" (all keys)
- **describe**: Pattern for key search in Redis
 - **examples**: "*", "Prediction:*", "model_v1:*"
- ** Specialities**:
- Using `keys()' for key search
- Removes all forward keys.
- Supports Wildcard Pathers

## Safety

###Authentication and authorisation

```python
from functools import wraps
import jwt
from datetime import datetime, timedelta
import secrets

class SecurityManager:
"The Safety Manager."

 def __init__(self, secret_key: str):
 self.secret_key = secret_key
 self.api_keys = {}

 def generate_api_key(self, User_id: str) -> str:
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 api_key = secrets.token_urlsafe(32)
 self.api_keys[api_key] = {
 'User_id': User_id,
 'created_at': datetime.now(),
 'permissions': ['predict', 'model_info']
 }
 return api_key

 def validate_api_key(self, api_key: str) -> bool:
"Validation API Key"
 return api_key in self.api_keys

 def get_User_permissions(self, api_key: str) -> List:
"Acquiring User Permits""
 if api_key in self.api_keys:
 return self.api_keys[api_key]['permissions']
 return []

 def require_auth(self, permissions: List = None):
""Dorator for authentication checks""
 def decorator(f):
 @wraps(f)
 def decorated_function(*args, **kwargs):
# Check API key
 api_key = request.headers.get('X-API-Key')
 if not api_key or not self.validate_api_key(api_key):
 return jsonify({'error': 'Invalid API key'}), 401

# Check permits
 if permissions:
 User_permissions = self.get_User_permissions(api_key)
 if not any(perm in User_permissions for perm in permissions):
 return jsonify({'error': 'Insufficient permissions'}), 403

 return f(*args, **kwargs)
 return decorated_function
 return decorator
```

### falseization of input data

```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Union
import numpy as np

class InputValidator:
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""Ink""""""""""""""""""""""""")""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""")""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

 def __init__(self, feature_schema: Dict[str, Any]):
 self.feature_schema = feature_schema

 def validate_input(self, data: List[Dict[str, Any]]) -> bool:
"Validation of input data."
 try:
 for record in data:
# check all mandatory features
 for feature, schema in self.feature_schema.items():
 if feature not in record:
 raise ValueError(f"Missing required feature: {feature}")

# Check data type
 if not isinstance(record[feature], schema['type']):
 raise ValueError(f"Invalid type for feature {feature}")

# sheck range
 if 'min' in schema and record[feature] < schema['min']:
 raise ValueError(f"Value too small for feature {feature}")

 if 'max' in schema and record[feature] > schema['max']:
 raise ValueError(f"Value too large for feature {feature}")

 return True
 except Exception as e:
 print(f"Validation error: {e}")
 return False

 def sanitize_input(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
""Clean input data."
 sanitized_data = []

 for record in data:
 sanitized_record = {}
 for feature, value in record.items():
# Clear from potentially dangerous symbols
 if isinstance(value, str):
 sanitized_record[feature] = value.strip()
 else:
 sanitized_record[feature] = value

 sanitized_data.append(sanitized_record)

 return sanitized_data
```

♪ ♪ System sales test ♪

### Load test

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import statistics

class LoadTester:
""API Load Test""

 def __init__(self, base_url: str):
 self.base_url = base_url
 self.results = []

 async def single_request(self, session: aiohttp.ClientSession,
 data: Dict[str, Any]) -> Dict[str, Any]:
"One Request."
 start_time = time.time()

 try:
 async with session.post(
 f"{self.base_url}/predict",
 json={"data": [data]}
 ) as response:
 result = await response.json()
 processing_time = time.time() - start_time

 return {
 'status_code': response.status,
 'processing_time': processing_time,
 'success': response.status == 200,
 'result': result
 }
 except Exception as e:
 return {
 'status_code': 0,
 'processing_time': time.time() - start_time,
 'success': False,
 'error': str(e)
 }

 async def load_test(self, concurrent_Users: int,
 requests_per_User: int,
 test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
"The Load Test""
 async with aiohttp.ClientSession() as session:
 tasks = []

 for User in range(concurrent_Users):
 for request in range(requests_per_User):
 data = test_data[request % len(test_data)]
 task = self.single_request(session, data)
 tasks.append(task)

 results = await asyncio.gather(*tasks)

# Analysis of results
 successful_requests = [r for r in results if r['success']]
 failed_requests = [r for r in results if not r['success']]

 processing_times = [r['processing_time'] for r in successful_requests]

 return {
 'total_requests': len(results),
 'successful_requests': len(successful_requests),
 'failed_requests': len(failed_requests),
 'success_rate': len(successful_requests) / len(results),
 'avg_processing_time': statistics.mean(processing_times),
 'min_processing_time': min(processing_times),
 'max_processing_time': max(processing_times),
 'p95_processing_time': statistics.quantiles(processing_times, n=20)[18]
 }
```

♪ Best practices sold

<img src="images/optimized/retraining_workflow.png" alt="Best practices sold" style="max-width: 100 per cent; light: auto; display: block; marguin: 20px auto;">
*Figure 6: Best practices and recommendations for the sale of ML models*

**Why are best practices sold important?** Because they help avoid typical mistakes and ensure reliability:

- **Planning**: Careful Planning of Architecture and Resources
- ** Test**: Integrated pre-depletion testing
- **Monitoring**: Continuous Monitoring Quality and Performance
- **documentation**: Detailed documentation for team
- ** Safety**: Data and model protection
- **Version**: Control of model versions and code
- **Rollback**: Rapid Rollback for problems

### ♪ The key principles of successful sales

Because they're time-tested and help avoid problems:

- ** "Fail Fast" principle**: Rapid detection and fix problems
- ** Graceful Degration principle**: Floating functional loss due to malfunctions
- ** "Observability" principle**: Full visibility of the system state
- ** Automation principle**: Automation of routine processes
- ** Principle "Security by Design"**: Safety with the beginning
- **Continuous Implementation principle**: Permanent improve system

## Next steps

Once you've mastered it, you'll have to go to:
- [model re-training](./07_retraining.md)
- [best practice](.08_best_practices.md)
- [Examples of use](./09_examples.md)
