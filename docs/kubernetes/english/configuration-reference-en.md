# Kubernetes Configuration Reference - English

This document provides a comprehensive reference for all Kubernetes configuration options available in the Neozork HLD Prediction project.

## Table of Contents

1. [Deployment Configuration](#deployment-configuration)
2. [Service Configuration](#service-configuration)
3. [Persistent Volume Configuration](#persistent-volume-configuration)
4. [Resource Configuration](#resource-configuration)
5. [Environment Variables](#environment-variables)
6. [Health Check Configuration](#health-check-configuration)
7. [Security Configuration](#security-configuration)
8. [Monitoring Configuration](#monitoring-configuration)
9. [Network Configuration](#network-configuration)
10. [Platform-Specific Configuration](#platform-specific-configuration)

## Deployment Configuration

### Basic Deployment Settings

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork-interactive-apple
  labels:
    app: neozork-interactive
    platform: apple-silicon
spec:
  replicas: 2                    # Number of pod replicas
  strategy:                      # Deployment strategy
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: neozork-interactive
```

### Platform-Specific Node Selection

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

### Container Configuration

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

## Service Configuration

### LoadBalancer Service

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

### ClusterIP Service (Internal)

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

### NodePort Service

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

## Persistent Volume Configuration

### Data Volume

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

### Logs Volume

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

### Plots Volume

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

### Results Volume

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

### Volume Mounts

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

## Resource Configuration

### Apple Silicon Resources

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

### x86 Resources

```yaml
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### Custom Resource Configuration

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

## Environment Variables

### Core Application Variables

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

### Platform-Specific Variables

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

### Database Configuration

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

### Redis Configuration

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

## Health Check Configuration

### Liveness Probe

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

### Readiness Probe

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

### Startup Probe

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

## Security Configuration

### Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 1000
  fsGroup: 1000
  seccompProfile:
    type: RuntimeDefault
```

### Pod Security Context

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

### Container Security Context

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

## Monitoring Configuration

### Service Monitor

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

### PrometheusRule

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
        summary: "Neozork service is down"
```

## Network Configuration

### Network Policy

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

### Ingress Configuration

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

## Platform-Specific Configuration

### Apple Silicon Optimization

```yaml
# Cursor MCP Configuration
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

### x86 Optimization

```yaml
# Cursor MCP Configuration
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

## Configuration Best Practices

### 1. Resource Management
- Always set both requests and limits
- Use appropriate resource classes for different workloads
- Monitor resource usage and adjust accordingly

### 2. Security
- Run containers as non-root users
- Use read-only root filesystems where possible
- Implement network policies for traffic isolation

### 3. High Availability
- Use multiple replicas for critical services
- Implement proper health checks
- Use anti-affinity rules for pod distribution

### 4. Monitoring
- Enable comprehensive logging
- Set up metrics collection
- Configure alerting for critical events

### 5. Storage
- Use appropriate storage classes for different data types
- Implement backup strategies for persistent data
- Monitor storage usage and plan for growth

This configuration reference provides all the necessary options for customizing your Kubernetes deployment. Choose the configurations that best fit your specific requirements and infrastructure constraints.
