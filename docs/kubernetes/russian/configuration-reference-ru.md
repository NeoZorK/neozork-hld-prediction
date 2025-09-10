# Справочник конфигурации Kubernetes - Русский

Этот документ предоставляет комплексный справочник по всем опциям конфигурации Kubernetes, доступным в проекте Neozork HLD Prediction.

## Содержание

1. [Конфигурация развертывания](#конфигурация-развертывания)
2. [Конфигурация сервиса](#конфигурация-сервиса)
3. [Конфигурация постоянных томов](#конфигурация-постоянных-томов)
4. [Конфигурация ресурсов](#конфигурация-ресурсов)
5. [Переменные окружения](#переменные-окружения)
6. [Конфигурация проверок здоровья](#конфигурация-проверок-здоровья)
7. [Конфигурация безопасности](#конфигурация-безопасности)
8. [Конфигурация мониторинга](#конфигурация-мониторинга)
9. [Сетевая конфигурация](#сетевая-конфигурация)
10. [Платформо-специфичная конфигурация](#платформо-специфичная-конфигурация)

## Конфигурация развертывания

### Основные настройки развертывания

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-apple
  labels:
    app: neozork-interactive
    platform: apple-silicon
spec:
  replicas: 2                    # Количество реплик подов
  strategy:                      # Стратегия развертывания
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: neozork-interactive
```

### Платформо-специфичный выбор узлов

```yaml
# Apple Silicon (ARM64)
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/arch: arm64

# x86 (AMD64)
spec:
  template:
    spec:
      nodeSelector:
        kubernetes.io/arch: amd64
```

### Конфигурация контейнера

```yaml
spec:
  template:
    spec:
      containers:
      - name: neozork-interactive
        image: neozork-interactive:apple-latest
        ports:
        - containerPort: 8080
          protocol: TCP
        env:
        - name: PYTHONPATH
          value: "/app"
        - name: APPLE_SILICON
          value: "true"
        - name: MLX_ENABLED
          value: "true"
```

## Конфигурация сервиса

### Сервис LoadBalancer

```yaml
apiVersion: v1
kind: Service
metadata:
  name: neozork-interactive-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: neozork-interactive
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Сервис ClusterIP (внутренний)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: neozork-interactive-internal
spec:
  type: ClusterIP
  selector:
    app: neozork-interactive
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
```

### Сервис NodePort

```yaml
apiVersion: v1
kind: Service
metadata:
  name: neozork-interactive-nodeport
spec:
  type: NodePort
  selector:
    app: neozork-interactive
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
```

## Конфигурация постоянных томов

### Том данных

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neozork-data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### Том логов

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neozork-logs-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### Том графиков

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neozork-plots-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### Том результатов

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: neozork-results-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: fast-ssd
```

### Монтирование томов

```yaml
spec:
  template:
    spec:
      containers:
      - name: neozork-interactive
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: logs-volume
          mountPath: /app/logs
        - name: plots-volume
          mountPath: /app/plots
        - name: results-volume
          mountPath: /app/results
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: neozork-data-pvc
      - name: logs-volume
        persistentVolumeClaim:
          claimName: neozork-logs-pvc
      - name: plots-volume
        persistentVolumeClaim:
          claimName: neozork-plots-pvc
      - name: results-volume
        persistentVolumeClaim:
          claimName: neozork-results-pvc
```

## Конфигурация ресурсов

### Ресурсы Apple Silicon

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### Ресурсы x86

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### Пользовательская конфигурация ресурсов

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
    ephemeral-storage: "1Gi"
  limits:
    memory: "1Gi"
    cpu: "500m"
    ephemeral-storage: "2Gi"
```

## Переменные окружения

### Основные переменные приложения

```yaml
env:
- name: PYTHONPATH
  value: "/app"
- name: ENVIRONMENT
  value: "production"
- name: LOG_LEVEL
  value: "INFO"
- name: API_HOST
  value: "0.0.0.0"
- name: API_PORT
  value: "8080"
```

### Платформо-специфичные переменные

```yaml
# Apple Silicon
env:
- name: APPLE_SILICON
  value: "true"
- name: MLX_ENABLED
  value: "true"
- name: MPS_ENABLED
  value: "true"

# x86
env:
- name: CUDA_ENABLED
  value: "true"
- name: OPENCL_ENABLED
  value: "true"
```

### Конфигурация базы данных

```yaml
env:
- name: DATABASE_HOST
  value: "postgres-service"
- name: DATABASE_PORT
  value: "5432"
- name: DATABASE_NAME
  value: "neozork"
- name: DATABASE_USER
  value: "neozork"
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: database-password
```

### Конфигурация Redis

```yaml
env:
- name: REDIS_HOST
  value: "redis-service"
- name: REDIS_PORT
  value: "6379"
- name: REDIS_PASSWORD
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: redis-password
```

## Конфигурация проверок здоровья

### Проверка жизнеспособности

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
    scheme: HTTP
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
```

### Проверка готовности

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
    scheme: HTTP
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

### Проверка запуска

```yaml
startupProbe:
  httpGet:
    path: /startup
    port: 8080
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 30
```

## Конфигурация безопасности

### Контекст безопасности

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
```

### Контекст безопасности пода

```yaml
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
```

### Контекст безопасности контейнера

```yaml
containers:
- name: neozork-interactive
  securityContext:
    allowPrivilegeEscalation: false
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 1000
    capabilities:
      drop:
      - ALL
```

## Конфигурация мониторинга

### Монитор сервиса

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: neozork-metrics
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

### Правило Prometheus

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: neozork-alerts
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
```

## Сетевая конфигурация

### Сетевая политика

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: neozork-network-policy
spec:
  podSelector:
    matchLabels:
      app: neozork-interactive
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

### Конфигурация Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: neozork-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - neozork.local
    secretName: neozork-tls
  rules:
  - host: neozork.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: neozork-interactive-service
            port:
              number: 80
```

## Платформо-специфичная конфигурация

### Оптимизация Apple Silicon

```yaml
# Конфигурация Cursor MCP
{
  "kubernetes": {
    "enabled": true,
    "namespace": "neozork",
    "deployment": {
      "replicas": 2,
      "strategy": "RollingUpdate",
      "maxSurge": 1,
      "maxUnavailable": 0,
      "platforms": {
        "apple-silicon": {
          "nodeSelector": {
            "kubernetes.io/arch": "arm64"
          },
          "image": "neozork-interactive:apple-latest",
          "resources": {
            "requests": {
              "memory": "2Gi",
              "cpu": "1000m"
            },
            "limits": {
              "memory": "4Gi",
              "cpu": "2000m"
            }
          }
        }
      }
    }
  }
}
```

### Оптимизация x86

```yaml
# Конфигурация Cursor MCP
{
  "kubernetes": {
    "platforms": {
      "x86": {
        "nodeSelector": {
          "kubernetes.io/arch": "amd64"
        },
        "image": "neozork-interactive:latest",
        "resources": {
          "requests": {
            "memory": "1Gi",
            "cpu": "500m"
          },
          "limits": {
            "memory": "2Gi",
            "cpu": "1000m"
          }
        }
      }
    }
  }
}
```

## Лучшие практики конфигурации

### 1. Управление ресурсами
- Всегда устанавливайте как запросы, так и лимиты
- Используйте подходящие классы ресурсов для разных рабочих нагрузок
- Мониторьте использование ресурсов и корректируйте соответственно

### 2. Безопасность
- Запускайте контейнеры от имени непривилегированных пользователей
- Используйте файловые системы только для чтения где возможно
- Реализуйте сетевые политики для изоляции трафика

### 3. Высокая доступность
- Используйте несколько реплик для критических сервисов
- Реализуйте правильные проверки здоровья
- Используйте правила анти-сродства для распределения подов

### 4. Мониторинг
- Включите комплексное логирование
- Настройте сбор метрик
- Настройте оповещения для критических событий

### 5. Хранилище
- Используйте подходящие классы хранилища для разных типов данных
- Реализуйте стратегии резервного копирования для постоянных данных
- Мониторьте использование хранилища и планируйте рост

Этот справочник конфигурации предоставляет все необходимые опции для настройки вашего развертывания Kubernetes. Выберите конфигурации, которые лучше всего подходят для ваших конкретных требований и ограничений инфраструктуры.
