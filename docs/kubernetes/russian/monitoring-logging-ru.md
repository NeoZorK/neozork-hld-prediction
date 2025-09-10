# Мониторинг и логирование - Русский

Это руководство охватывает комплексную настройку мониторинга и логирования для проекта Neozork HLD Prediction на Kubernetes.

## Содержание

1. [Обзор мониторинга](#обзор-мониторинга)
2. [Настройка Prometheus](#настройка-prometheus)
3. [Конфигурация Grafana](#конфигурация-grafana)
4. [Метрики приложения](#метрики-приложения)
5. [Стратегия логирования](#стратегия-логирования)
6. [Конфигурация оповещений](#конфигурация-оповещений)
7. [Мониторинг производительности](#мониторинг-производительности)
8. [Мониторинг безопасности](#мониторинг-безопасности)
9. [Устранение неполадок мониторинга](#устранение-неполадок-мониторинга)

## Обзор мониторинга

### Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Стек мониторинга                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Grafana   │  │ Prometheus  │  │   Alert     │         │
│  │  Dashboard  │  │   Server    │  │  Manager    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Node       │  │  Service    │  │  Custom     │         │
│  │  Exporter   │  │  Monitor    │  │  Metrics    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### Ключевые метрики

- **Метрики приложения**: Время отклика, частота запросов, частота ошибок
- **Метрики инфраструктуры**: CPU, память, диск, сеть
- **Бизнес-метрики**: Торговые сигналы, точность прогнозов
- **Метрики безопасности**: Неудачные входы, подозрительная активность

## Настройка Prometheus

### Установка

```bash
# Добавление репозитория Prometheus Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Установка стека Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi
```

### Конфигурация

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    rule_files:
      - "neozork_rules.yml"
    
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - action: labelmap
            regex: __meta_kubernetes_pod_label_(.+)
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: kubernetes_pod_name
```

### Монитор сервиса

```yaml
# service-monitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: neozork-metrics
  namespace: monitoring
  labels:
    app: neozork-interactive
spec:
  selector:
    matchLabels:
      app: neozork-interactive
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
```

## Конфигурация Grafana

### Установка

```bash
# Установка Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set persistence.size=10Gi \
  --set adminPassword=admin123
```

### Конфигурация дашборда

```yaml
# grafana-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: neozork-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  neozork-dashboard.json: |
    {
      "dashboard": {
        "id": null,
        "title": "Дашборд Neozork HLD Prediction",
        "tags": ["neozork", "trading", "prediction"],
        "timezone": "browser",
        "panels": [
          {
            "id": 1,
            "title": "Частота запросов",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"neozork-interactive\"}[5m])",
                "legendFormat": "{{method}} {{endpoint}}"
              }
            ]
          },
          {
            "id": 2,
            "title": "Время отклика",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"neozork-interactive\"}[5m]))",
                "legendFormat": "95-й процентиль"
              }
            ]
          },
          {
            "id": 3,
            "title": "Частота ошибок",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"neozork-interactive\",status=~\"5..\"}[5m])",
                "legendFormat": "Ошибки 5xx"
              }
            ]
          },
          {
            "id": 4,
            "title": "Торговые сигналы",
            "type": "graph",
            "targets": [
              {
                "expr": "neozork_trading_signals_total",
                "legendFormat": "{{signal_type}}"
              }
            ]
          },
          {
            "id": 5,
            "title": "Точность прогнозов",
            "type": "singlestat",
            "targets": [
              {
                "expr": "neozork_prediction_accuracy",
                "legendFormat": "Точность %"
              }
            ]
          }
        ],
        "time": {
          "from": "now-1h",
          "to": "now"
        },
        "refresh": "30s"
      }
    }
```

### Источники данных

```yaml
# grafana-datasource.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasource
  namespace: monitoring
data:
  datasource.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus-server:80
        access: proxy
        isDefault: true
```

## Метрики приложения

### Реализация пользовательских метрик

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Метрики запросов
REQUEST_COUNT = Counter('http_requests_total', 'Общее количество HTTP запросов', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Длительность HTTP запросов', ['method', 'endpoint'])

# Бизнес-метрики
TRADING_SIGNALS = Counter('neozork_trading_signals_total', 'Общее количество сгенерированных торговых сигналов', ['signal_type'])
PREDICTION_ACCURACY = Gauge('neozork_prediction_accuracy', 'Процент точности прогнозов')
ACTIVE_CONNECTIONS = Gauge('neozork_active_connections', 'Количество активных подключений')

# Системные метрики
MEMORY_USAGE = Gauge('neozork_memory_usage_bytes', 'Использование памяти в байтах')
CPU_USAGE = Gauge('neozork_cpu_usage_percent', 'Процент использования CPU')

def start_metrics_server(port=8080):
    """Запуск сервера метрик Prometheus."""
    start_http_server(port)
    print(f"Сервер метрик запущен на порту {port}")

def record_request(method, endpoint, status, duration):
    """Запись метрик HTTP запросов."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

def record_trading_signal(signal_type):
    """Запись генерации торгового сигнала."""
    TRADING_SIGNALS.labels(signal_type=signal_type).inc()

def update_prediction_accuracy(accuracy):
    """Обновление метрики точности прогнозов."""
    PREDICTION_ACCURACY.set(accuracy)

def update_system_metrics():
    """Обновление метрик системных ресурсов."""
    import psutil
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    CPU_USAGE.set(psutil.cpu_percent())
```

### Конечная точка метрик

```python
# app.py
from flask import Flask, request, jsonify
import time
from metrics import record_request, record_trading_signal, update_prediction_accuracy

app = Flask(__name__)

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    record_request(
        method=request.method,
        endpoint=request.endpoint,
        status=response.status_code,
        duration=duration
    )
    return response

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/ready')
def ready():
    return jsonify({"status": "ready"})

@app.route('/metrics')
def metrics():
    # Конечная точка метрик Prometheus
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/trading/signal', methods=['POST'])
def generate_trading_signal():
    # Бизнес-логика здесь
    signal_type = "buy"  # или "sell"
    record_trading_signal(signal_type)
    return jsonify({"signal": signal_type})

@app.route('/api/prediction/accuracy', methods=['POST'])
def update_accuracy():
    accuracy = request.json.get('accuracy', 0)
    update_prediction_accuracy(accuracy)
    return jsonify({"status": "updated"})
```

## Стратегия логирования

### Структурированное логирование

```python
# logging_config.py
import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'trading_pair'):
            log_entry['trading_pair'] = record.trading_pair
            
        return json.dumps(log_entry)

def setup_logging():
    """Настройка конфигурации структурированного логирования."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Удаление обработчиков по умолчанию
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Обработчик консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # Обработчик файлов
    file_handler = logging.FileHandler('/app/logs/application.log')
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    return logger
```

### Агрегация логов

```yaml
# fluentd-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
  namespace: monitoring
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/*neozork*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      format json
      time_key time
      time_format %Y-%m-%dT%H:%M:%S.%NZ
    </source>
    
    <filter kubernetes.**>
      @type kubernetes_metadata
    </filter>
    
    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name neozork-logs
      type_name _doc
    </match>
```

### Ротация логов

```yaml
# logrotate-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: logrotate-config
data:
  logrotate.conf: |
    /app/logs/*.log {
        daily
        missingok
        rotate 30
        compress
        delaycompress
        notifempty
        create 644 root root
        postrotate
            /bin/kill -USR1 $(cat /var/run/rsyslogd.pid 2> /dev/null) 2> /dev/null || true
        endscript
    }
```

## Конфигурация оповещений

### Правила Prometheus

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: neozork-alerts
  namespace: monitoring
spec:
  groups:
  - name: neozork.rules
    rules:
    - alert: NeozorkDown
      expr: up{job="neozork-interactive"} == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Сервис Neozork недоступен"
        description: "Сервис Neozork недоступен более 1 минуты"
    
    - alert: HighErrorRate
      expr: rate(http_requests_total{job="neozork-interactive",status=~"5.."}[5m]) > 0.1
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "Обнаружена высокая частота ошибок"
        description: "Частота ошибок составляет {{ $value }} ошибок в секунду"
    
    - alert: HighResponseTime
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="neozork-interactive"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Высокое время отклика"
        description: "95-й процентиль времени отклика составляет {{ $value }} секунд"
    
    - alert: LowPredictionAccuracy
      expr: neozork_prediction_accuracy < 70
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Низкая точность прогнозов"
        description: "Точность прогнозов составляет {{ $value }}%"
    
    - alert: HighMemoryUsage
      expr: (neozork_memory_usage_bytes / (1024*1024*1024)) > 3
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Высокое использование памяти"
        description: "Использование памяти составляет {{ $value }} GB"
```

### Конфигурация Alertmanager

```yaml
# alertmanager-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
  namespace: monitoring
data:
  alertmanager.yml: |
    global:
      smtp_smarthost: 'smtp.gmail.com:587'
      smtp_from: 'alerts@neozork.com'
      smtp_auth_username: 'alerts@neozork.com'
      smtp_auth_password: 'your-password'
    
    route:
      group_by: ['alertname']
      group_wait: 10s
      group_interval: 10s
      repeat_interval: 1h
      receiver: 'web.hook'
      routes:
      - match:
          severity: critical
        receiver: 'critical-alerts'
      - match:
          severity: warning
        receiver: 'warning-alerts'
    
    receivers:
    - name: 'web.hook'
      webhook_configs:
      - url: 'http://webhook-service:5001/webhook'
    
    - name: 'critical-alerts'
      email_configs:
      - to: 'admin@neozork.com'
        subject: 'КРИТИЧНО: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Оповещение: {{ .Annotations.summary }}
          Описание: {{ .Annotations.description }}
          {{ end }}
    
    - name: 'warning-alerts'
      email_configs:
      - to: 'team@neozork.com'
        subject: 'ПРЕДУПРЕЖДЕНИЕ: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Оповещение: {{ .Annotations.summary }}
          Описание: {{ .Annotations.description }}
          {{ end }}
```

## Мониторинг производительности

### Интеграция APM

```python
# apm_config.py
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler

def setup_apm(app):
    """Настройка мониторинга производительности приложений."""
    app.config['ELASTIC_APM'] = {
        'SERVICE_NAME': 'neozork-interactive',
        'SECRET_TOKEN': 'your-secret-token',
        'SERVER_URL': 'http://apm-server:8200',
        'ENVIRONMENT': 'production',
        'ENABLED': True,
        'CAPTURE_BODY': 'all',
        'CAPTURE_HEADERS': True,
        'TRANSACTION_SAMPLE_RATE': 1.0
    }
    
    apm = ElasticAPM(app)
    
    # Настройка логирования APM
    apm_handler = LoggingHandler(client=apm.client)
    apm_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger()
    logger.addHandler(apm_handler)
    
    return apm
```

### Пользовательские метрики производительности

```python
# performance_metrics.py
from prometheus_client import Histogram, Counter, Gauge
import time
import functools

# Метрики производительности
PREDICTION_TIME = Histogram('neozork_prediction_duration_seconds', 'Время, затраченное на прогнозы')
DATA_PROCESSING_TIME = Histogram('neozork_data_processing_duration_seconds', 'Время обработки данных')
MODEL_LOAD_TIME = Histogram('neozork_model_load_duration_seconds', 'Время загрузки моделей')

# Метрики использования ресурсов
GPU_MEMORY_USAGE = Gauge('neozork_gpu_memory_usage_bytes', 'Использование памяти GPU')
GPU_UTILIZATION = Gauge('neozork_gpu_utilization_percent', 'Процент использования GPU')

def measure_time(metric):
    """Декоратор для измерения времени выполнения функции."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                metric.observe(duration)
        return wrapper
    return decorator

@measure_time(PREDICTION_TIME)
def make_prediction(data):
    """Создание торгового прогноза."""
    # Логика прогнозирования здесь
    pass

@measure_time(DATA_PROCESSING_TIME)
def process_market_data(data):
    """Обработка рыночных данных."""
    # Логика обработки данных здесь
    pass
```

## Мониторинг безопасности

### Метрики безопасности

```python
# security_metrics.py
from prometheus_client import Counter, Histogram

# Метрики безопасности
FAILED_LOGINS = Counter('neozork_failed_logins_total', 'Общее количество неудачных попыток входа', ['user', 'ip'])
SUSPICIOUS_REQUESTS = Counter('neozork_suspicious_requests_total', 'Общее количество подозрительных запросов', ['type', 'ip'])
RATE_LIMIT_HITS = Counter('neozork_rate_limit_hits_total', 'Общее количество попаданий в лимит скорости', ['endpoint', 'ip'])
SECURITY_SCAN_TIME = Histogram('neozork_security_scan_duration_seconds', 'Время, затраченное на сканирование безопасности')

def record_failed_login(user, ip):
    """Запись неудачной попытки входа."""
    FAILED_LOGINS.labels(user=user, ip=ip).inc()

def record_suspicious_request(request_type, ip):
    """Запись подозрительного запроса."""
    SUSPICIOUS_REQUESTS.labels(type=request_type, ip=ip).inc()

def record_rate_limit_hit(endpoint, ip):
    """Запись попадания в лимит скорости."""
    RATE_LIMIT_HITS.labels(endpoint=endpoint, ip=ip).inc()
```

### Оповещения безопасности

```yaml
# security-alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: neozork-security-alerts
  namespace: monitoring
spec:
  groups:
  - name: neozork.security
    rules:
    - alert: MultipleFailedLogins
      expr: rate(neozork_failed_logins_total[5m]) > 5
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "Обнаружены множественные неудачные попытки входа"
        description: "Частота неудачных входов составляет {{ $value }} в секунду"
    
    - alert: SuspiciousActivity
      expr: rate(neozork_suspicious_requests_total[5m]) > 1
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "Обнаружена подозрительная активность"
        description: "Частота подозрительных запросов составляет {{ $value }} в секунду"
    
    - alert: RateLimitExceeded
      expr: rate(neozork_rate_limit_hits_total[5m]) > 10
      for: 1m
      labels:
        severity: warning
      annotations:
        summary: "Превышен лимит скорости"
        description: "Частота попаданий в лимит скорости составляет {{ $value }} в секунду"
```

## Устранение неполадок мониторинга

### Частые проблемы

1. **Метрики не появляются**
   ```bash
   # Проверка ServiceMonitor
   kubectl get servicemonitor -n monitoring
   
   # Проверка целей Prometheus
   kubectl port-forward -n monitoring svc/prometheus-server 9090:80
   # Открыть http://localhost:9090/targets
   ```

2. **Проблемы с дашбордом Grafana**
   ```bash
   # Проверка логов Grafana
   kubectl logs -n monitoring deployment/grafana
   
   # Проверка конфигурации источника данных
   kubectl exec -n monitoring deployment/grafana -- cat /etc/grafana/provisioning/datasources/datasource.yaml
   ```

3. **Оповещения не работают**
   ```bash
   # Проверка конфигурации Alertmanager
   kubectl get configmap -n monitoring alertmanager-config -o yaml
   
   # Проверка логов Alertmanager
   kubectl logs -n monitoring deployment/alertmanager
   ```

### Проверки здоровья мониторинга

```bash
# Проверка здоровья Prometheus
kubectl exec -n monitoring deployment/prometheus-server -- curl http://localhost:9090/-/healthy

# Проверка здоровья Grafana
kubectl exec -n monitoring deployment/grafana -- curl http://localhost:3000/api/health

# Проверка конечной точки метрик
kubectl exec deployment/neozork-interactive-apple -- curl http://localhost:8080/metrics
```

Эта комплексная настройка мониторинга и логирования обеспечивает полную наблюдаемость для проекта Neozork HLD Prediction, позволяя проактивно обнаруживать проблемы и оптимизировать производительность.
