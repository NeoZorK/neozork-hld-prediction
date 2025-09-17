# Руководство по развертыванию Kubernetes - Русский

Это комплексное руководство охватывает все аспекты развертывания проекта Neozork HLD Prediction на Kubernetes, от базовой настройки до производственного развертывания.

## Содержание

1. [Обзор архитектуры](#обзор-архитектуры)
2. [Предварительные требования](#предварительные-требования)
3. [Настройка инфраструктуры](#настройка-инфраструктуры)
4. [Развертывание приложения](#развертывание-приложения)
5. [Управление конфигурацией](#управление-конфигурацией)
6. [Мониторинг и логирование](#мониторинг-и-логирование)
7. [Конфигурация безопасности](#конфигурация-безопасности)
8. [Масштабирование и производительность](#масштабирование-и-производительность)
9. [Резервное копирование и восстановление](#резервное-копирование-и-восстановление)
10. [Производственные соображения](#производственные-соображения)

## Обзор архитектуры

Проект Neozork HLD Prediction спроектирован как микросервисная архитектура со следующими компонентами:

### Основные компоненты

1. **Интерактивное приложение**: Основной сервис приложения
2. **API Gateway**: Балансировщик нагрузки и обратный прокси на основе Nginx
3. **База данных**: PostgreSQL для постоянного хранения данных
4. **Кэш**: Redis для кэширования сессий и данных
5. **Мониторинг**: Prometheus и Grafana для наблюдаемости

### Архитектура развертывания

```
┌─────────────────────────────────────────────────────────────┐
│                    Кластер Kubernetes                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Ingress   │  │   Service   │  │  ConfigMap  │         │
│  │             │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Interactive │  │     API     │  │  Database   │         │
│  │   Service   │  │   Service   │  │   Service   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Redis     │  │  Prometheus │  │   Grafana   │         │
│  │   Service   │  │   Service   │  │   Service   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Предварительные требования

### Требования к кластеру

**Минимальные требования:**
- 3 рабочих узла
- 4 ядра CPU на узел
- 8GB RAM на узел
- 100GB хранилища на узел

**Рекомендуемые для продакшена:**
- 5+ рабочих узлов
- 8 ядер CPU на узел
- 16GB RAM на узел
- 500GB SSD хранилища на узел

### Требования к программному обеспечению

```bash
# Необходимые инструменты
kubectl >= 1.20
helm >= 3.0
docker >= 20.10
```

### Сетевые требования

- Контроллер Ingress (nginx, traefik или облачный)
- Поддержка LoadBalancer (или NodePort для тестирования)
- DNS разрешение для обнаружения сервисов

## Настройка инфраструктуры

### 1. Создание пространства имен

```bash
# Создание выделенного пространства имен
kubectl create namespace neozork

# Установка как пространство имен по умолчанию
kubectl config set-context --current --namespace=neozork
```

### 2. Настройка классов хранилища

```yaml
# storage-class.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
  encrypted: "true"
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  fsType: ext4
```

```bash
kubectl apply -f storage-class.yaml
```

### 3. Настройка секретов

```bash
# Создание секретов приложения
kubectl create secret generic app-secrets \
  --from-literal=database-password=your-secure-password \
  --from-literal=secret-key=your-secret-key \
  --from-literal=jwt-secret=your-jwt-secret

# Создание TLS секрета (если используется HTTPS)
kubectl create secret tls neozork-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem
```

## Развертывание приложения

### 1. Развертывание основных сервисов

```bash
# Развертывание основного приложения
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Проверка развертывания
kubectl get all -l app=neozork-interactive
```

### 2. Развертывание вспомогательных сервисов

```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
  labels:
    app: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
        - name: POSTGRES_DB
          value: neozork
        - name: POSTGRES_USER
          value: neozork
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
  storageClassName: fast-ssd
```

```bash
kubectl apply -f postgres-deployment.yaml
```

### 3. Развертывание Redis

```yaml
# redis-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  labels:
    app: redis
spec:
  replicas: 2
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "128Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

```bash
kubectl apply -f redis-deployment.yaml
```

## Управление конфигурацией

### 1. ConfigMaps

```yaml
# app-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  API_HOST: "0.0.0.0"
  API_PORT: "8080"
```

### 2. Конфигурации для разных окружений

```bash
# Разработка
kubectl create configmap app-config-dev \
  --from-literal=ENVIRONMENT=development \
  --from-literal=LOG_LEVEL=DEBUG

# Продакшен
kubectl create configmap app-config-prod \
  --from-literal=ENVIRONMENT=production \
  --from-literal=LOG_LEVEL=INFO
```

## Мониторинг и логирование

### 1. Развертывание Prometheus

```bash
# Добавление репозитория Prometheus Helm
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Установка Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 2. Развертывание Grafana

```bash
# Установка Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set persistence.size=10Gi
```

### 3. Настройка метрик приложения

```yaml
# service-monitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: neozork-metrics
spec:
  selector:
    matchLabels:
      app: neozork-interactive
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
```

## Конфигурация безопасности

### 1. Сетевые политики

```yaml
# network-policy.yaml
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

### 2. Политики безопасности подов

```yaml
# pod-security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: neozork-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

## Масштабирование и производительность

### 1. Горизонтальный автомасштабировщик подов

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: neozork-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: neozork-interactive-apple
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 2. Вертикальный автомасштабировщик подов

```bash
# Установка VPA
kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml

# Создание VPA для приложения
kubectl apply -f - <<EOF
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: neozork-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: neozork-interactive-apple
  updatePolicy:
    updateMode: "Auto"
EOF
```

## Резервное копирование и восстановление

### 1. Резервное копирование базы данных

```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"  # Ежедневно в 2:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15
            command:
            - /bin/bash
            - -c
            - |
              pg_dump -h postgres-service -U neozork neozork > /backup/backup-$(date +%Y%m%d).sql
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-password
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

### 2. Резервное копирование данных приложения

```bash
# Создание скрипта резервного копирования
cat > backup-script.sh << 'EOF'
#!/bin/bash
kubectl exec -it deployment/neozork-interactive-apple -- tar czf /tmp/app-data-backup.tar.gz /app/data
kubectl cp neozork-interactive-apple-xxx:/tmp/app-data-backup.tar.gz ./app-data-backup-$(date +%Y%m%d).tar.gz
EOF

chmod +x backup-script.sh
```

## Производственные соображения

### 1. Оптимизация ресурсов

- Используйте сродство узлов для размещения подов на подходящих узлах
- Реализуйте квоты и ограничения ресурсов
- Мониторьте использование ресурсов и корректируйте соответственно

### 2. Высокая доступность

- Развертывайте в нескольких зонах доступности
- Используйте правила анти-сродства для распределения подов
- Реализуйте проверки здоровья и автоматический отказ

### 3. Безопасность

- Включите RBAC (управление доступом на основе ролей)
- Используйте сетевые политики для изоляции трафика
- Реализуйте политики безопасности подов
- Регулярное сканирование безопасности и обновления

### 4. Мониторинг

- Настройте комплексное логирование
- Реализуйте распределенную трассировку
- Настройте оповещения для критических метрик
- Регулярное тестирование производительности

## Устранение неполадок

### Частые проблемы развертывания

1. **Сбои запуска подов**
   - Проверьте ограничения ресурсов
   - Убедитесь в доступности образа
   - Проверьте переменные окружения

2. **Проблемы подключения к сервису**
   - Проверьте селекторы сервиса
   - Проверьте сетевые политики
   - Тестируйте DNS разрешение

3. **Проблемы с хранилищем**
   - Убедитесь в доступности класса хранилища
   - Проверьте запросы на постоянные тома
   - Проверьте квоты хранилища

### Полезные команды

```bash
# Проверка статуса кластера
kubectl get nodes
kubectl get pods --all-namespaces

# Отладка проблем с подами
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# Проверка подключения к сервису
kubectl get endpoints
kubectl port-forward service/<service-name> 8080:80

# Мониторинг ресурсов
kubectl top nodes
kubectl top pods
```

Это руководство по развертыванию предоставляет комплексную основу для запуска проекта Neozork HLD Prediction в производственной среде Kubernetes. Настройте конфигурации в соответствии с вашими конкретными требованиями и ограничениями инфраструктуры.
