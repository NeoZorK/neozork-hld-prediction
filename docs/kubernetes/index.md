# Kubernetes Documentation

This section contains comprehensive documentation for deploying and managing the Neozork HLD Prediction project using Kubernetes.

## Table of Contents

### English Documentation
- [Getting Started with Kubernetes](./english/getting-started-en.md) - Basic setup and deployment
- [Deployment Guide](./english/deployment-guide-en.md) - Complete deployment instructions
- [Configuration Reference](./english/configuration-reference-en.md) - All configuration options
- [Monitoring and Logging](./english/monitoring-logging-en.md) - Observability setup
- [Troubleshooting](./english/troubleshooting-en.md) - Common issues and solutions
- [Advanced Topics](./english/advanced-topics-en.md) - Scaling, security, and optimization

### Russian Documentation (Русская документация)
- [Начало работы с Kubernetes](./russian/getting-started-ru.md) - Базовая настройка и развертывание
- [Руководство по развертыванию](./russian/deployment-guide-ru.md) - Полные инструкции по развертыванию
- [Справочник конфигурации](./russian/configuration-reference-ru.md) - Все параметры конфигурации
- [Мониторинг и логирование](./russian/monitoring-logging-ru.md) - Настройка наблюдаемости
- [Устранение неполадок](./russian/troubleshooting-ru.md) - Частые проблемы и решения
- [Продвинутые темы](./russian/advanced-topics-ru.md) - Масштабирование, безопасность и оптимизация

## Quick Start

### Prerequisites
- Kubernetes cluster (v1.20+)
- kubectl configured
- Docker images built and pushed to registry

### Basic Deployment
```bash
# Apply the basic deployment
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Check deployment status
kubectl get pods -l app=neozork-interactive

# Access the service
kubectl port-forward service/neozork-interactive-service 8080:80
```

## Architecture Overview

The project supports multiple deployment strategies:

1. **Apple Silicon Deployment** - Optimized for ARM64 architecture
2. **x86 Deployment** - Standard AMD64 architecture
3. **Multi-platform Deployment** - Hybrid approach

## Key Features

- **Multi-platform Support**: ARM64 and AMD64 architectures
- **Persistent Storage**: Data, logs, plots, and results volumes
- **Health Checks**: Liveness and readiness probes
- **Resource Management**: CPU and memory limits/requests
- **Service Discovery**: LoadBalancer and ClusterIP services
- **Monitoring Integration**: Prometheus and Grafana support

## Support

For issues and questions:
- Check the troubleshooting guides
- Review the configuration reference
- Open an issue in the project repository
