# Продакшен и деплой AutoML Gluon моделей

## Введение в продакшен

Продакшен деплой ML-моделей - это критически важный этап, который требует тщательного планирования, мониторинга и поддержки. В этом разделе рассмотрим все аспекты деплоя AutoML Gluon моделей в продакшен.

## Подготовка модели к продакшену

### Оптимизация модели

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np

# Создание оптимизированной модели для продакшена
def create_production_model(train_data, target_col):
    """Создание модели, оптимизированной для продакшена"""
    
    predictor = TabularPredictor(
        label=target_col,
        problem_type='auto',
        eval_metric='auto',
        path='./production_models'
    )
    
    # Обучение с оптимизацией для деплоя
    predictor.fit(
        train_data,
        presets='optimize_for_deployment',
        time_limit=3600,  # 1 час
        num_bag_folds=3,   # Меньше фолдов для скорости
        num_bag_sets=1,
        ag_args_fit={
            'num_cpus': 4,
            'num_gpus': 0,
            'memory_limit': 8
        }
    )
    
    return predictor
```

### Сжатие модели

```python
def compress_model(predictor, model_name):
    """Сжатие модели для продакшена"""
    
    # Сохранение сжатой модели
    predictor.save(
        model_name,
        save_space=True,
        compress=True,
        save_info=True
    )
    
    # Получение размера модели
    import os
    model_size = os.path.getsize(f"{model_name}/predictor.pkl") / (1024 * 1024)  # MB
    print(f"Model size: {model_size:.2f} MB")
    
    return model_size
```

### Валидация модели

```python
def validate_production_model(predictor, test_data, performance_thresholds):
    """Валидация модели для продакшена"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Проверка пороговых значений
    validation_results = {}
    for metric, threshold in performance_thresholds.items():
        if metric in performance:
            validation_results[metric] = performance[metric] >= threshold
        else:
            validation_results[metric] = False
    
    # Проверка стабильности предсказаний
    if hasattr(predictor, 'predict_proba'):
        probabilities = predictor.predict_proba(test_data)
        prob_std = probabilities.std().mean()
        validation_results['stability'] = prob_std < 0.1  # Стабильность вероятностей
    
    return validation_results, performance
```

## API сервер для продакшена

### FastAPI сервер

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

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Глобальная переменная для модели
model = None

class PredictionRequest(BaseModel):
    """Схема запроса для предсказания"""
    data: List[Dict[str, Any]]
    
class PredictionResponse(BaseModel):
    """Схема ответа с предсказаниями"""
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class HealthResponse(BaseModel):
    """Схема ответа для health check"""
    status: str
    model_loaded: bool
    model_info: Dict[str, Any] = None

@app.on_event("startup")
async def load_model():
    """Загрузка модели при запуске сервера"""
    global model
    try:
        model = TabularPredictor.load('./production_models')
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if model is None:
        return HealthResponse(
            status="unhealthy",
            model_loaded=False
        )
    
    return HealthResponse(
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
    """Endpoint для предсказаний"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Преобразование данных в DataFrame
        df = pd.DataFrame(request.data)
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        # Информация о модели
        model_info = {
            "model_path": model.path,
            "problem_type": model.problem_type,
            "eval_metric": model.eval_metric,
            "num_features": len(df.columns)
        }
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities,
            model_info=model_info,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
async def model_info():
    """Информация о модели"""
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

### Flask сервер

```python
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
import traceback

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание Flask приложения
app = Flask(__name__)

# Глобальная переменная для модели
model = None

def load_model():
    """Загрузка модели"""
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
    """Health check endpoint"""
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
    """Endpoint для предсказаний"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        # Получение данных
        data = request.get_json()
        
        if 'data' not in data:
            return jsonify({"error": "No data provided"}), 400
        
        # Преобразование в DataFrame
        df = pd.DataFrame(data['data'])
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        return jsonify({
            "predictions": predictions.tolist(),
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
    """Информация о модели"""
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

## Docker контейнеризация

### Dockerfile для продакшена

```dockerfile
# Dockerfile для продакшена
FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание пользователя для безопасности
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "app.py"]
```

### Docker Compose для продакшена

```yaml
# docker-compose.prod.yml
version: '3.8'

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
      - ./logs:/app/logs
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

## Kubernetes деплой

### Deployment манифест

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
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
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
        - name: log-storage
          mountPath: /app/logs
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
      - name: log-storage
        persistentVolumeClaim:
          claimName: log-pvc
---
apiVersion: v1
kind: Service
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

## Мониторинг и логирование

### Система мониторинга

```python
import logging
import time
from datetime import datetime
import psutil
import requests
from typing import Dict, Any

class ProductionMonitor:
    """Мониторинг продакшен системы"""
    
    def __init__(self, log_file='production.log'):
        self.log_file = log_file
        self.setup_logging()
        self.metrics = {}
    
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def log_prediction(self, input_data: Dict, prediction: Any, 
                      processing_time: float, model_info: Dict):
        """Логирование предсказания"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_data': input_data,
            'prediction': prediction,
            'processing_time': processing_time,
            'model_info': model_info
        }
        self.logger.info(f"Prediction: {log_entry}")
    
    def log_error(self, error: Exception, context: Dict):
        """Логирование ошибок"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        self.logger.error(f"Error: {error_entry}")
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Получение системных метрик"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'timestamp': datetime.now().isoformat()
        }
    
    def check_model_health(self, model) -> Dict[str, Any]:
        """Проверка здоровья модели"""
        try:
            # Тестовое предсказание
            test_data = pd.DataFrame({'feature1': [1.0], 'feature2': [2.0]})
            start_time = time.time()
            prediction = model.predict(test_data)
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

### Алерты и уведомления

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class AlertSystem:
    """Система алертов для продакшена"""
    
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def send_email_alert(self, subject: str, message: str, recipients: list):
        """Отправка email алерта"""
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
        """Отправка Slack алерта"""
        try:
            payload = {
                "text": message,
                "username": "AutoML Gluon Monitor",
                "icon_emoji": ":robot_face:"
            }
            
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            
            print("Slack alert sent successfully")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
    
    def check_performance_thresholds(self, metrics: Dict[str, float], 
                                   thresholds: Dict[str, float]):
        """Проверка пороговых значений производительности"""
        alerts = []
        
        for metric, threshold in thresholds.items():
            if metric in metrics and metrics[metric] < threshold:
                alerts.append(f"{metric} is below threshold: {metrics[metric]} < {threshold}")
        
        return alerts
```

## Масштабирование

### Горизонтальное масштабирование

```python
# Настройка для горизонтального масштабирования
import asyncio
from concurrent.futures import ThreadPoolExecutor
import queue
import threading

class ScalablePredictionService:
    """Масштабируемый сервис предсказаний"""
    
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
    async def process_prediction(self, data: Dict) -> Dict:
        """Асинхронная обработка предсказания"""
        loop = asyncio.get_event_loop()
        
        # Выполнение предсказания в отдельном потоке
        result = await loop.run_in_executor(
            self.executor, 
            self._predict_sync, 
            data
        )
        
        return result
    
    def _predict_sync(self, data: Dict) -> Dict:
        """Синхронное предсказание"""
        # Ваша логика предсказания
        pass
    
    def batch_predict(self, batch_data: List[Dict]) -> List[Dict]:
        """Пакетная обработка предсказаний"""
        results = []
        
        # Разделение на батчи
        batch_size = 100
        for i in range(0, len(batch_data), batch_size):
            batch = batch_data[i:i+batch_size]
            
            # Параллельная обработка батча
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = [executor.submit(self._predict_sync, data) for data in batch]
                batch_results = [future.result() for future in futures]
                results.extend(batch_results)
        
        return results
```

### Кэширование

```python
import redis
import json
import hashlib
from typing import Any, Optional

class PredictionCache:
    """Кэш для предсказаний"""
    
    def __init__(self, redis_host='localhost', redis_port=6379, ttl=3600):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.ttl = ttl
    
    def _generate_cache_key(self, data: Dict) -> str:
        """Генерация ключа кэша"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()
    
    def get_prediction(self, data: Dict) -> Optional[Dict]:
        """Получение предсказания из кэша"""
        cache_key = self._generate_cache_key(data)
        cached_result = self.redis_client.get(cache_key)
        
        if cached_result:
            return json.loads(cached_result)
        
        return None
    
    def set_prediction(self, data: Dict, prediction: Dict):
        """Сохранение предсказания в кэш"""
        cache_key = self._generate_cache_key(data)
        self.redis_client.setex(
            cache_key, 
            self.ttl, 
            json.dumps(prediction)
        )
    
    def invalidate_cache(self, pattern: str = "*"):
        """Очистка кэша"""
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)
```

## Безопасность

### Аутентификация и авторизация

```python
from functools import wraps
import jwt
from datetime import datetime, timedelta
import secrets

class SecurityManager:
    """Менеджер безопасности"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.api_keys = {}
    
    def generate_api_key(self, user_id: str) -> str:
        """Генерация API ключа"""
        api_key = secrets.token_urlsafe(32)
        self.api_keys[api_key] = {
            'user_id': user_id,
            'created_at': datetime.now(),
            'permissions': ['predict', 'model_info']
        }
        return api_key
    
    def validate_api_key(self, api_key: str) -> bool:
        """Валидация API ключа"""
        return api_key in self.api_keys
    
    def get_user_permissions(self, api_key: str) -> list:
        """Получение разрешений пользователя"""
        if api_key in self.api_keys:
            return self.api_keys[api_key]['permissions']
        return []
    
    def require_auth(self, permissions: list = None):
        """Декоратор для проверки аутентификации"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Проверка API ключа
                api_key = request.headers.get('X-API-Key')
                if not api_key or not self.validate_api_key(api_key):
                    return jsonify({'error': 'Invalid API key'}), 401
                
                # Проверка разрешений
                if permissions:
                    user_permissions = self.get_user_permissions(api_key)
                    if not any(perm in user_permissions for perm in permissions):
                        return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

### Валидация входных данных

```python
from pydantic import BaseModel, validator
from typing import List, Dict, Any, Union
import numpy as np

class InputValidator:
    """Валидатор входных данных"""
    
    def __init__(self, feature_schema: Dict[str, Any]):
        self.feature_schema = feature_schema
    
    def validate_input(self, data: List[Dict[str, Any]]) -> bool:
        """Валидация входных данных"""
        try:
            for record in data:
                # Проверка наличия всех обязательных признаков
                for feature, schema in self.feature_schema.items():
                    if feature not in record:
                        raise ValueError(f"Missing required feature: {feature}")
                    
                    # Проверка типа данных
                    if not isinstance(record[feature], schema['type']):
                        raise ValueError(f"Invalid type for feature {feature}")
                    
                    # Проверка диапазона значений
                    if 'min' in schema and record[feature] < schema['min']:
                        raise ValueError(f"Value too small for feature {feature}")
                    
                    if 'max' in schema and record[feature] > schema['max']:
                        raise ValueError(f"Value too large for feature {feature}")
            
            return True
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def sanitize_input(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Очистка входных данных"""
        sanitized_data = []
        
        for record in data:
            sanitized_record = {}
            for feature, value in record.items():
                # Очистка от потенциально опасных символов
                if isinstance(value, str):
                    sanitized_record[feature] = value.strip()
                else:
                    sanitized_record[feature] = value
            
            sanitized_data.append(sanitized_record)
        
        return sanitized_data
```

## Тестирование продакшен системы

### Нагрузочное тестирование

```python
import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import statistics

class LoadTester:
    """Нагрузочное тестирование API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []
    
    async def single_request(self, session: aiohttp.ClientSession, 
                           data: Dict[str, Any]) -> Dict[str, Any]:
        """Одиночный запрос"""
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
    
    async def load_test(self, concurrent_users: int, 
                       requests_per_user: int, 
                       test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Нагрузочное тестирование"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    data = test_data[request % len(test_data)]
                    task = self.single_request(session, data)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks)
        
        # Анализ результатов
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

## Следующие шаги

После освоения продакшен деплоя переходите к:
- [Переобучению моделей](./07_retraining.md)
- [Лучшим практикам](./08_best_practices.md)
- [Примерам использования](./09_examples.md)
