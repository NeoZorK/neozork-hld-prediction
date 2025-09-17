# Monitoring and Logging - English

This guide covers comprehensive monitoring and logging setup for the Neozork HLD Prediction project on Kubernetes.

## Table of Contents

1. [Monitoring Overview](#monitoring-overview)
2. [Prometheus Setup](#prometheus-setup)
3. [Grafana Configuration](#grafana-configuration)
4. [Application Metrics](#application-metrics)
5. [Logging Strategy](#logging-strategy)
6. [Alerting Configuration](#alerting-configuration)
7. [Performance Monitoring](#performance-monitoring)
8. [Security Monitoring](#security-monitoring)
9. [Troubleshooting Monitoring](#troubleshooting-monitoring)

## Monitoring Overview

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Monitoring Stack                        │
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

### Key Metrics

- **Application Metrics**: Response time, request rate, error rate
- **Infrastructure Metrics**: CPU, memory, disk, network
- **Business Metrics**: Trading signals, prediction accuracy
- **Security Metrics**: Failed logins, suspicious activities

## Prometheus Setup

### Installation

```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus Stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=50Gi
```

### Configuration

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

### Service Monitor

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

## Grafana Configuration

### Installation

```bash
# Install Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set persistence.size=10Gi \
  --set adminPassword=admin123
```

### Dashboard Configuration

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
        "title": "Neozork HLD Prediction Dashboard",
        "tags": ["neozork", "trading", "prediction"],
        "timezone": "browser",
        "panels": [
          {
            "id": 1,
            "title": "Request Rate",
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
            "title": "Response Time",
            "type": "graph",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job=\"neozork-interactive\"}[5m]))",
                "legendFormat": "95th percentile"
              }
            ]
          },
          {
            "id": 3,
            "title": "Error Rate",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(http_requests_total{job=\"neozork-interactive\",status=~\"5..\"}[5m])",
                "legendFormat": "5xx errors"
              }
            ]
          },
          {
            "id": 4,
            "title": "Trading Signals",
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
            "title": "Prediction Accuracy",
            "type": "singlestat",
            "targets": [
              {
                "expr": "neozork_prediction_accuracy",
                "legendFormat": "Accuracy %"
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

### Data Sources

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

## Application Metrics

### Custom Metrics Implementation

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'endpoint'])

# Business metrics
TRADING_SIGNALS = Counter('neozork_trading_signals_total', 'Total trading signals generated', ['signal_type'])
PREDICTION_ACCURACY = Gauge('neozork_prediction_accuracy', 'Prediction accuracy percentage')
ACTIVE_CONNECTIONS = Gauge('neozork_active_connections', 'Number of active connections')

# System metrics
MEMORY_USAGE = Gauge('neozork_memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('neozork_cpu_usage_percent', 'CPU usage percentage')

def start_metrics_server(port=8080):
    """Start Prometheus metrics server."""
    start_http_server(port)
    print(f"Metrics server started on port {port}")

def record_request(method, endpoint, status, duration):
    """Record HTTP request metrics."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)

def record_trading_signal(signal_type):
    """Record trading signal generation."""
    TRADING_SIGNALS.labels(signal_type=signal_type).inc()

def update_prediction_accuracy(accuracy):
    """Update prediction accuracy metric."""
    PREDICTION_ACCURACY.set(accuracy)

def update_system_metrics():
    """Update system resource metrics."""
    import psutil
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    CPU_USAGE.set(psutil.cpu_percent())
```

### Metrics Endpoint

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
    # Prometheus metrics endpoint
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/trading/signal', methods=['POST'])
def generate_trading_signal():
    # Business logic here
    signal_type = "buy"  # or "sell"
    record_trading_signal(signal_type)
    return jsonify({"signal": signal_type})

@app.route('/api/prediction/accuracy', methods=['POST'])
def update_accuracy():
    accuracy = request.json.get('accuracy', 0)
    update_prediction_accuracy(accuracy)
    return jsonify({"status": "updated"})
```

## Logging Strategy

### Structured Logging

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
    """Setup structured logging configuration."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove default handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler('/app/logs/application.log')
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    return logger
```

### Log Aggregation

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

### Log Rotation

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

## Alerting Configuration

### Prometheus Rules

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
        summary: "Neozork service is down"
        description: "Neozork service has been down for more than 1 minute"
    
    - alert: HighErrorRate
      expr: rate(http_requests_total{job="neozork-interactive",status=~"5.."}[5m]) > 0.1
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected"
        description: "Error rate is {{ $value }} errors per second"
    
    - alert: HighResponseTime
      expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{job="neozork-interactive"}[5m])) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High response time"
        description: "95th percentile response time is {{ $value }} seconds"
    
    - alert: LowPredictionAccuracy
      expr: neozork_prediction_accuracy < 70
      for: 10m
      labels:
        severity: warning
      annotations:
        summary: "Low prediction accuracy"
        description: "Prediction accuracy is {{ $value }}%"
    
    - alert: HighMemoryUsage
      expr: (neozork_memory_usage_bytes / (1024*1024*1024)) > 3
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High memory usage"
        description: "Memory usage is {{ $value }} GB"
```

### Alertmanager Configuration

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
        subject: 'CRITICAL: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
    
    - name: 'warning-alerts'
      email_configs:
      - to: 'team@neozork.com'
        subject: 'WARNING: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}
```

## Performance Monitoring

### APM Integration

```python
# apm_config.py
from elasticapm.contrib.flask import ElasticAPM
from elasticapm.handlers.logging import LoggingHandler

def setup_apm(app):
    """Setup Application Performance Monitoring."""
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
    
    # Setup APM logging
    apm_handler = LoggingHandler(client=apm.client)
    apm_handler.setLevel(logging.INFO)
    
    logger = logging.getLogger()
    logger.addHandler(apm_handler)
    
    return apm
```

### Custom Performance Metrics

```python
# performance_metrics.py
from prometheus_client import Histogram, Counter, Gauge
import time
import functools

# Performance metrics
PREDICTION_TIME = Histogram('neozork_prediction_duration_seconds', 'Time spent on predictions')
DATA_PROCESSING_TIME = Histogram('neozork_data_processing_duration_seconds', 'Time spent processing data')
MODEL_LOAD_TIME = Histogram('neozork_model_load_duration_seconds', 'Time spent loading models')

# Resource usage metrics
GPU_MEMORY_USAGE = Gauge('neozork_gpu_memory_usage_bytes', 'GPU memory usage')
GPU_UTILIZATION = Gauge('neozork_gpu_utilization_percent', 'GPU utilization percentage')

def measure_time(metric):
    """Decorator to measure function execution time."""
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
    """Make trading prediction."""
    # Prediction logic here
    pass

@measure_time(DATA_PROCESSING_TIME)
def process_market_data(data):
    """Process market data."""
    # Data processing logic here
    pass
```

## Security Monitoring

### Security Metrics

```python
# security_metrics.py
from prometheus_client import Counter, Histogram

# Security metrics
FAILED_LOGINS = Counter('neozork_failed_logins_total', 'Total failed login attempts', ['user', 'ip'])
SUSPICIOUS_REQUESTS = Counter('neozork_suspicious_requests_total', 'Total suspicious requests', ['type', 'ip'])
RATE_LIMIT_HITS = Counter('neozork_rate_limit_hits_total', 'Total rate limit hits', ['endpoint', 'ip'])
SECURITY_SCAN_TIME = Histogram('neozork_security_scan_duration_seconds', 'Time spent on security scans')

def record_failed_login(user, ip):
    """Record failed login attempt."""
    FAILED_LOGINS.labels(user=user, ip=ip).inc()

def record_suspicious_request(request_type, ip):
    """Record suspicious request."""
    SUSPICIOUS_REQUESTS.labels(type=request_type, ip=ip).inc()

def record_rate_limit_hit(endpoint, ip):
    """Record rate limit hit."""
    RATE_LIMIT_HITS.labels(endpoint=endpoint, ip=ip).inc()
```

### Security Alerts

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
        summary: "Multiple failed login attempts detected"
        description: "Rate of failed logins is {{ $value }} per second"
    
    - alert: SuspiciousActivity
      expr: rate(neozork_suspicious_requests_total[5m]) > 1
      for: 2m
      labels:
        severity: warning
      annotations:
        summary: "Suspicious activity detected"
        description: "Rate of suspicious requests is {{ $value }} per second"
    
    - alert: RateLimitExceeded
      expr: rate(neozork_rate_limit_hits_total[5m]) > 10
      for: 1m
      labels:
        severity: warning
      annotations:
        summary: "Rate limit exceeded"
        description: "Rate of rate limit hits is {{ $value }} per second"
```

## Troubleshooting Monitoring

### Common Issues

1. **Metrics Not Appearing**
   ```bash
   # Check ServiceMonitor
   kubectl get servicemonitor -n monitoring
   
   # Check Prometheus targets
   kubectl port-forward -n monitoring svc/prometheus-server 9090:80
   # Open http://localhost:9090/targets
   ```

2. **Grafana Dashboard Issues**
   ```bash
   # Check Grafana logs
   kubectl logs -n monitoring deployment/grafana
   
   # Check data source configuration
   kubectl exec -n monitoring deployment/grafana -- cat /etc/grafana/provisioning/datasources/datasource.yaml
   ```

3. **Alerting Not Working**
   ```bash
   # Check Alertmanager configuration
   kubectl get configmap -n monitoring alertmanager-config -o yaml
   
   # Check Alertmanager logs
   kubectl logs -n monitoring deployment/alertmanager
   ```

### Monitoring Health Checks

```bash
# Check Prometheus health
kubectl exec -n monitoring deployment/prometheus-server -- curl http://localhost:9090/-/healthy

# Check Grafana health
kubectl exec -n monitoring deployment/grafana -- curl http://localhost:3000/api/health

# Check metrics endpoint
kubectl exec deployment/neozork-interactive-apple -- curl http://localhost:8080/metrics
```

This comprehensive monitoring and logging setup provides full observability for the Neozork HLD Prediction project, enabling proactive issue detection and performance optimization.
