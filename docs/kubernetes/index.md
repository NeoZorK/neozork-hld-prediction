# Kubernetes Documentation

This section contains comprehensive documentation for deploying and managing the Neozork HLD Prediction project Using Kubernetes.

## Table of Contents

### English Documentation
- [Getting started with Kubernetes](./english/getting-started-en.md) - Basic setup and deployment
- [deployment Guide](./english/deployment-guide-en.md) - Complete deployment instructions
- [Configuration Reference](./english/configuration-reference-en.md) - all configuration options
- [Monitoring and Logging](./english/Monitoring-logging-en.md) - Observability setup
- [Troubleshooting](./english/Troubleshooting-en.md) - Common Issues and solutions
- [Advanced Topics](./english/advanced-topics-en.md) - Scaling, security, and optimization

### Russian Documentation (Русская documentation)
- [Начало работы with Kubernetes](./russian/getting-started-ru.md) - Базовая configuration and развертывание
- [guide on deployment](./russian/deployment-guide-ru.md) - Полные instructions on deployment
- [Справочник конфигурации](./russian/configuration-reference-ru.md) - Все parameters конфигурации
- [Monitoring and логирование](./russian/Monitoring-logging-ru.md) - configuration наблюдаемости
- [Troubleshooting](./russian/Troubleshooting-ru.md) - Common Issues and решения
- [Продвинутые темы](./russian/advanced-topics-ru.md) - Масштабирование, безопасность and оптимизация

## Quick start

### Prerequisites
- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker images built and Pushed to registry

### Basic deployment
```bash
# Apply the basic deployment
kubectl apply -f k8s/neozork-apple-deployment.yaml

# check deployment status
kubectl get pods -l app=neozork-interactive

# Access the service
kubectl port-forward service/neozork-interactive-service 8080:80
```

## Architecture OverView

The project supports multiple deployment strategies:

1. **Apple Silicon deployment** - Optimized for ARM64 architecture
2. **x86 deployment** - Standard AMD64 architecture
3. **Multi-platform deployment** - Hybrid approach

## Key Features

- **Multi-platform Support**: ARM64 and AMD64 architectures
- **Persistent Storage**: data, logs, plots, and results volumes
- **health checks**: Liveness and readiness probes
- **Resource Management**: CPU and memory limits/requests
- **Service Discovery**: LoadBalancer and ClusterIP Services
- **Monitoring integration**: Prometheus and Grafana support

## Support

For issues and questions:
- check the Troubleshooting guides
- ReView the configuration reference
- Open an issue in the project repository
