# Продвинутые темы - Русский

Это руководство охватывает продвинутые темы Kubernetes для проекта Neozork HLD Prediction, включая масштабирование, безопасность, оптимизацию и производственные соображения.

## Содержание

1. [Стратегии автомасштабирования](#стратегии-автомасштабирования)
2. [Усиление безопасности](#усиление-безопасности)
3. [Оптимизация производительности](#оптимизация-производительности)
4. [Развертывание в нескольких кластерах](#развертывание-в-нескольких-кластерах)
5. [Восстановление после сбоев](#восстановление-после-сбоев)
6. [Оптимизация затрат](#оптимизация-затрат)
7. [Продвинутые сети](#продвинутые-сети)
8. [Пользовательские операторы](#пользовательские-операторы)
9. [Интеграция GitOps](#интеграция-gitops)
10. [Готовность к продакшену](#готовность-к-продакшену)

## Стратегии автомасштабирования

### Горизонтальный автомасштабировщик подов (HPA)

```yaml
# hpa-config.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: neozork-hpa
  namespace: neozork
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: neozork-interactive-apple
  minReplicas: 2
  maxReplicas: 20
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
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max
```

### Вертикальный автомасштабировщик подов (VPA)

```yaml
# vpa-config.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: neozork-vpa
  namespace: neozork
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: neozork-interactive-apple
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: neozork-interactive
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 4000m
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

### Автомасштабировщик кластера

```yaml
# cluster-autoscaler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cluster-autoscaler
  template:
    metadata:
      labels:
        app: cluster-autoscaler
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
        name: cluster-autoscaler
        resources:
          limits:
            cpu: 100m
            memory: 300Mi
          requests:
            cpu: 100m
            memory: 300Mi
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/neozork-cluster
        - --balance-similar-node-groups
        - --scale-down-enabled=true
        - --scale-down-delay-after-add=10m
        - --scale-down-unneeded-time=10m
```

## Усиление безопасности

### Стандарты безопасности подов

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
  readOnlyRootFilesystem: true
  hostNetwork: false
  hostIPC: false
  hostPID: false
```

### Сетевые политики

```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: neozork-network-policy
  namespace: neozork
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
    - podSelector:
        matchLabels:
          app: neozork-interactive
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
  - to: []
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```

### Конфигурация RBAC

```yaml
# rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: neozork-sa
  namespace: neozork
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: neozork
  name: neozork-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: neozork-rolebinding
  namespace: neozork
subjects:
- kind: ServiceAccount
  name: neozork-sa
  namespace: neozork
roleRef:
  kind: Role
  name: neozork-role
  apiGroup: rbac.authorization.k8s.io
```

### Контекст безопасности

```yaml
# security-context.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-secure
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
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: var-cache
          mountPath: /var/cache
        - name: var-log
          mountPath: /var/log
      volumes:
      - name: tmp
        emptyDir: {}
      - name: var-cache
        emptyDir: {}
      - name: var-log
        emptyDir: {}
```

## Оптимизация производительности

### Оптимизация ресурсов

```yaml
# resource-optimization.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-optimized
spec:
  template:
    spec:
      containers:
      - name: neozork-interactive
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
            ephemeral-storage: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
            ephemeral-storage: 2Gi
        env:
        - name: OMP_NUM_THREADS
          value: "4"
        - name: MKL_NUM_THREADS
          value: "4"
        - name: OPENBLAS_NUM_THREADS
          value: "4"
        - name: NUMEXPR_NUM_THREADS
          value: "4"
        - name: VECLIB_MAXIMUM_THREADS
          value: "4"
        - name: NUMBA_NUM_THREADS
          value: "4"
```

### Сродство узлов и анти-сродство

```yaml
# affinity.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-affinity
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: kubernetes.io/arch
                operator: In
                values:
                - arm64
              - key: node-type
                operator: In
                values:
                - compute-optimized
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - neozork-interactive
              topologyKey: kubernetes.io/hostname
```

### Оптимизация CPU и памяти

```yaml
# cpu-memory-optimization.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: neozork-optimization-config
data:
  optimization.conf: |
    # Оптимизация CPU
    cpu_cores: 4
    thread_pool_size: 8
    batch_size: 32
    
    # Оптимизация памяти
    memory_limit: 4Gi
    cache_size: 1Gi
    buffer_size: 256Mi
    
    # Оптимизация GPU (если доступно)
    gpu_memory_fraction: 0.8
    gpu_allow_growth: true
```

## Развертывание в нескольких кластерах

### Федерация кластеров

```yaml
# federated-deployment.yaml
apiVersion: types.kubefed.io/v1beta1
kind: FederatedDeployment
metadata:
  name: neozork-interactive
  namespace: neozork
spec:
  template:
    metadata:
      labels:
        app: neozork-interactive
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: neozork-interactive
      template:
        metadata:
          labels:
            app: neozork-interactive
        spec:
          containers:
          - name: neozork-interactive
            image: neozork-interactive:latest
            ports:
            - containerPort: 8080
  placement:
    clusters:
    - name: cluster-us-east-1
    - name: cluster-eu-west-1
  overrides:
  - clusterName: cluster-us-east-1
    clusterOverrides:
    - path: spec.replicas
      value: 3
  - clusterName: cluster-eu-west-1
    clusterOverrides:
    - path: spec.replicas
      value: 2
```

### Обнаружение сервисов между кластерами

```yaml
# cross-cluster-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: neozork-interactive-cross-cluster
  namespace: neozork
  annotations:
    service.alpha.kubernetes.io/tolerate-unready-endpoints: "true"
spec:
  type: ExternalName
  externalName: neozork-interactive.other-cluster.svc.cluster.local
  ports:
  - port: 8080
    targetPort: 8080
```

## Восстановление после сбоев

### Стратегия резервного копирования

```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: neozork-backup
  namespace: neozork
spec:
  schedule: "0 2 * * *"  # Ежедневно в 2:00
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command:
            - /bin/bash
            - -c
            - |
              # Резервное копирование базы данных
              pg_dump -h postgres-service -U neozork neozork > /backup/db-backup-$(date +%Y%m%d).sql
              
              # Резервное копирование данных приложения
              tar czf /backup/app-data-backup-$(date +%Y%m%d).tar.gz /app/data
              
              # Загрузка в S3
              aws s3 cp /backup/ s3://neozork-backups/$(date +%Y%m%d)/ --recursive
              
              # Очистка старых резервных копий
              find /backup -name "*.sql" -mtime +7 -delete
              find /backup -name "*.tar.gz" -mtime +7 -delete
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-password
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: access-key-id
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: aws-credentials
                  key: secret-access-key
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

### Стратегия восстановления

```yaml
# restore-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: neozork-restore
  namespace: neozork
spec:
  template:
    spec:
      containers:
      - name: restore
        image: postgres:15
        command:
        - /bin/bash
        - -c
        - |
          # Загрузка из S3
          aws s3 cp s3://neozork-backups/20240101/ /restore/ --recursive
          
          # Восстановление базы данных
          psql -h postgres-service -U neozork neozork < /restore/db-backup-20240101.sql
          
          # Восстановление данных приложения
          tar xzf /restore/app-data-backup-20240101.tar.gz -C /
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-password
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: access-key-id
        - name: AWS_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: secret-access-key
        volumeMounts:
        - name: restore-storage
          mountPath: /restore
      volumes:
      - name: restore-storage
        persistentVolumeClaim:
          claimName: restore-pvc
      restartPolicy: Never
```

## Оптимизация затрат

### Конфигурация спот-инстансов

```yaml
# spot-instance-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-spot
spec:
  template:
    spec:
      nodeSelector:
        node.kubernetes.io/instance-type: spot
      tolerations:
      - key: "spot-instance"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"
      containers:
      - name: neozork-interactive
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 2Gi
```

### Квоты ресурсов

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: neozork-quota
  namespace: neozork
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    persistentvolumeclaims: "10"
    pods: "20"
    services: "5"
    secrets: "10"
    configmaps: "10"
```

## Продвинутые сети

### Сервисная сетка (Istio)

```yaml
# istio-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: neozork-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - neozork.local
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: neozork-tls
    hosts:
    - neozork.local
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: neozork-virtual-service
spec:
  hosts:
  - neozork.local
  gateways:
  - neozork-gateway
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: neozork-interactive-service
        port:
          number: 8080
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
```

### Сетевые политики с Calico

```yaml
# calico-network-policy.yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: neozork-calico-policy
  namespace: neozork
spec:
  selector: app == "neozork-interactive"
  types:
  - Ingress
  - Egress
  ingress:
  - action: Allow
    protocol: TCP
    source:
      selector: app == "ingress-nginx"
    destination:
      ports:
      - 8080
  egress:
  - action: Allow
    protocol: TCP
    destination:
      selector: app == "postgres"
      ports:
      - 5432
  - action: Allow
    protocol: TCP
    destination:
      selector: app == "redis"
      ports:
      - 6379
  - action: Allow
    protocol: UDP
    destination:
      ports:
      - 53
```

## Пользовательские операторы

### Оператор Neozork

```go
// neozork-operator.go
package main

import (
    "context"
    "fmt"
    "time"

    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller"
    "sigs.k8s.io/controller-runtime/pkg/handler"
    "sigs.k8s.io/controller-runtime/pkg/manager"
    "sigs.k8s.io/controller-runtime/pkg/reconcile"
    "sigs.k8s.io/controller-runtime/pkg/source"
)

type NeozorkReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

func (r *NeozorkReconciler) Reconcile(ctx context.Context, req reconcile.Request) (reconcile.Result, error) {
    // Пользовательская логика согласования
    fmt.Printf("Согласование ресурса Neozork: %s\n", req.NamespacedName)
    
    // Реализуйте вашу пользовательскую логику здесь
    // - Масштабирование развертываний на основе торгового объема
    // - Обновление конфигураций на основе рыночных условий
    // - Управление пользовательскими ресурсами
    
    return reconcile.Result{RequeueAfter: time.Minute * 5}, nil
}

func main() {
    // Настройка менеджера и контроллера
    mgr, err := manager.New(cfg, manager.Options{})
    if err != nil {
        panic(err)
    }

    // Создание контроллера
    c, err := controller.New("neozork-controller", mgr, controller.Options{
        Reconciler: &NeozorkReconciler{
            Client: mgr.GetClient(),
            Scheme: mgr.GetScheme(),
        },
    })
    if err != nil {
        panic(err)
    }

    // Наблюдение за ресурсами Neozork
    err = c.Watch(&source.Kind{Type: &neozorkv1.NeozorkTrading{}}, &handler.EnqueueRequestForObject{})
    if err != nil {
        panic(err)
    }

    // Запуск менеджера
    if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
        panic(err)
    }
}
```

## Интеграция GitOps

### Приложение ArgoCD

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: neozork-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/neozork-k8s-manifests
    targetRevision: HEAD
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: neozork
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
```

### Конфигурация Flux

```yaml
# flux-config.yaml
apiVersion: source.toolkit.fluxcd.io/v1beta1
kind: GitRepository
metadata:
  name: neozork-repo
  namespace: flux-system
spec:
  interval: 1m
  ref:
    branch: main
  url: https://github.com/your-org/neozork-k8s-manifests
---
apiVersion: kustomize.toolkit.fluxcd.io/v1beta1
kind: Kustomization
metadata:
  name: neozork-kustomization
  namespace: flux-system
spec:
  interval: 5m
  sourceRef:
    kind: GitRepository
    name: neozork-repo
  path: "./overlays/production"
  prune: true
  validation: client
```

## Готовность к продакшену

### Чек-лист продакшена

```yaml
# production-readiness.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: production-checklist
data:
  checklist.md: |
    # Чек-лист готовности к продакшену
    
    ## Безопасность
    - [ ] RBAC настроен
    - [ ] Сетевые политики реализованы
    - [ ] Политики безопасности подов включены
    - [ ] Управление секретами настроено
    - [ ] TLS/SSL сертификаты установлены
    
    ## Мониторинг
    - [ ] Метрики Prometheus настроены
    - [ ] Дашборды Grafana созданы
    - [ ] Правила оповещений определены
    - [ ] Агрегация логов настроена
    - [ ] Проверки здоровья реализованы
    
    ## Высокая доступность
    - [ ] Несколько реплик настроены
    - [ ] Правила анти-сродства установлены
    - [ ] Балансировка нагрузки настроена
    - [ ] Стратегия резервного копирования реализована
    - [ ] План восстановления после сбоев готов
    
    ## Производительность
    - [ ] Лимиты ресурсов установлены
    - [ ] Автомасштабирование настроено
    - [ ] Тестирование производительности завершено
    - [ ] Оптимизация применена
    - [ ] Планирование мощности выполнено
    
    ## Операции
    - [ ] CI/CD пайплайн настроен
    - [ ] GitOps рабочий процесс настроен
    - [ ] Документация завершена
    - [ ] Руководства созданы
    - [ ] Обучение команды завершено
```

### Развертывание в продакшене

```yaml
# production-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-prod
  namespace: neozork
  labels:
    app: neozork-interactive
    environment: production
    version: v1.0.0
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: neozork-interactive
      environment: production
  template:
    metadata:
      labels:
        app: neozork-interactive
        environment: production
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: neozork-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
      containers:
      - name: neozork-interactive
        image: neozork-interactive:v1.0.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: config
        configMap:
          name: neozork-config
      - name: data
        persistentVolumeClaim:
          claimName: neozork-data-pvc
      - name: logs
        persistentVolumeClaim:
          claimName: neozork-logs-pvc
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - neozork-interactive
              topologyKey: kubernetes.io/hostname
```

Это руководство по продвинутым темам предоставляет комплексное покрытие стратегий развертывания Kubernetes, готовых к продакшену, для проекта Neozork HLD Prediction. Реализуйте эти паттерны на основе ваших конкретных требований и ограничений инфраструктуры.
