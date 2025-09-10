# Kubernetes Deployment Guide - English

This comprehensive guide covers all aspects of deploying the Neozork HLD Prediction project on Kubernetes, from basic setup to production deployment.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Infrastructure Setup](#infrastructure-setup)
4. [Application Deployment](#application-deployment)
5. [Configuration Management](#configuration-management)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Security Configuration](#security-configuration)
8. [Scaling and Performance](#scaling-and-performance)
9. [Backup and Recovery](#backup-and-recovery)
10. [Production Considerations](#production-considerations)

## Architecture Overview

The Neozork HLD Prediction project is designed as a microservices architecture with the following components:

### Core Components

1. **Interactive Application**: Main application service
2. **API Gateway**: Nginx-based load balancer and reverse proxy
3. **Database**: PostgreSQL for data persistence
4. **Cache**: Redis for session and data caching
5. **Monitoring**: Prometheus and Grafana for observability

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                       │
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

## Prerequisites

### Cluster Requirements

**Minimum Requirements:**
- 3 worker nodes
- 4 CPU cores per node
- 8GB RAM per node
- 100GB storage per node

**Recommended for Production:**
- 5+ worker nodes
- 8 CPU cores per node
- 16GB RAM per node
- 500GB SSD storage per node

### Software Requirements

```bash
# Required tools
kubectl >= 1.20
helm >= 3.0
docker >= 20.10
```

### Network Requirements

- Ingress controller (nginx, traefik, or cloud-specific)
- LoadBalancer support (or NodePort for testing)
- DNS resolution for service discovery

## Infrastructure Setup

### 1. Create Namespace

```bash
# Create dedicated namespace
kubectl create namespace neozork

# Set as default namespace
kubectl config set-context --current --namespace=neozork
```

### 2. Set up Storage Classes

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

### 3. Configure Secrets

```bash
# Create application secrets
kubectl create secret generic app-secrets \
  --from-literal=database-password=your-secure-password \
  --from-literal=secret-key=your-secret-key \
  --from-literal=jwt-secret=your-jwt-secret

# Create TLS secret (if using HTTPS)
kubectl create secret tls neozork-tls \
  --cert=path/to/cert.pem \
  --key=path/to/key.pem
```

## Application Deployment

### 1. Deploy Core Services

```bash
# Deploy the main application
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Verify deployment
kubectl get all -l app=neozork-interactive
```

### 2. Deploy Supporting Services

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

### 3. Deploy Redis

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

## Configuration Management

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

### 2. Environment-specific Configurations

```bash
# Development
kubectl create configmap app-config-dev \
  --from-literal=ENVIRONMENT=development \
  --from-literal=LOG_LEVEL=DEBUG

# Production
kubectl create configmap app-config-prod \
  --from-literal=ENVIRONMENT=production \
  --from-literal=LOG_LEVEL=INFO
```

## Monitoring and Logging

### 1. Deploy Prometheus

```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

### 2. Deploy Grafana

```bash
# Install Grafana
helm install grafana grafana/grafana \
  --namespace monitoring \
  --set persistence.enabled=true \
  --set persistence.size=10Gi
```

### 3. Configure Application Metrics

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

## Security Configuration

### 1. Network Policies

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

### 2. Pod Security Policies

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

## Scaling and Performance

### 1. Horizontal Pod Autoscaler

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

### 2. Vertical Pod Autoscaler

```bash
# Install VPA
kubectl apply -f https://github.com/kubernetes/autoscaler/releases/latest/download/vertical-pod-autoscaler.yaml

# Create VPA for the application
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

## Backup and Recovery

### 1. Database Backup

```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
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

### 2. Application Data Backup

```bash
# Create backup script
cat > backup-script.sh << 'EOF'
#!/bin/bash
kubectl exec -it deployment/neozork-interactive-apple -- tar czf /tmp/app-data-backup.tar.gz /app/data
kubectl cp neozork-interactive-apple-xxx:/tmp/app-data-backup.tar.gz ./app-data-backup-$(date +%Y%m%d).tar.gz
EOF

chmod +x backup-script.sh
```

## Production Considerations

### 1. Resource Optimization

- Use node affinity to place pods on appropriate nodes
- Implement resource quotas and limits
- Monitor resource usage and adjust accordingly

### 2. High Availability

- Deploy across multiple availability zones
- Use anti-affinity rules for pod distribution
- Implement health checks and automatic failover

### 3. Security

- Enable RBAC (Role-Based Access Control)
- Use network policies for traffic isolation
- Implement pod security policies
- Regular security scanning and updates

### 4. Monitoring

- Set up comprehensive logging
- Implement distributed tracing
- Configure alerting for critical metrics
- Regular performance testing

## Troubleshooting

### Common Deployment Issues

1. **Pod Startup Failures**
   - Check resource constraints
   - Verify image availability
   - Review environment variables

2. **Service Connectivity**
   - Verify service selectors
   - Check network policies
   - Test DNS resolution

3. **Storage Issues**
   - Verify storage class availability
   - Check persistent volume claims
   - Review storage quotas

### Useful Commands

```bash
# Check cluster status
kubectl get nodes
kubectl get pods --all-namespaces

# Debug pod issues
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# Check service connectivity
kubectl get endpoints
kubectl port-forward service/<service-name> 8080:80

# Monitor resources
kubectl top nodes
kubectl top pods
```

This deployment guide provides a comprehensive foundation for running the Neozork HLD Prediction project in a production Kubernetes environment. Adjust configurations based on your specific requirements and infrastructure constraints.
