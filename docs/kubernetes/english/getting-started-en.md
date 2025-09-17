# Getting Started with Kubernetes - English

This guide will help you get started with deploying the Neozork HLD Prediction project on Kubernetes.

## Prerequisites

### System Requirements
- Kubernetes cluster (version 1.20 or higher)
- kubectl command-line tool configured
- Docker images built and available in a container registry
- Minimum 4 CPU cores and 8GB RAM for the cluster

### Required Tools
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

### Cluster Access
Ensure your kubectl is configured to access your Kubernetes cluster:
```bash
# Check cluster connection
kubectl cluster-info

# Verify you can list nodes
kubectl get nodes
```

## Quick Start

### 1. Build and Push Docker Images

First, build the Docker images for your platform:

```bash
# For Apple Silicon (ARM64)
docker build -f Dockerfile.apple -t neozork-interactive:apple-latest .

# For x86 (AMD64)
docker build -f Dockerfile -t neozork-interactive:latest .

# Push to your registry (replace with your registry)
docker tag neozork-interactive:apple-latest your-registry/neozork-interactive:apple-latest
docker tag neozork-interactive:latest your-registry/neozork-interactive:latest

docker push your-registry/neozork-interactive:apple-latest
docker push your-registry/neozork-interactive:latest
```

### 2. Deploy to Kubernetes

Apply the Kubernetes manifests:

```bash
# Deploy the application
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods -l app=neozork-interactive
kubectl get services
```

### 3. Verify Deployment

Check that all components are running:

```bash
# Check pod status
kubectl get pods -l app=neozork-interactive

# Check service endpoints
kubectl get endpoints

# View pod logs
kubectl logs -l app=neozork-interactive --tail=50
```

### 4. Access the Application

Port forward to access the application locally:

```bash
# Forward port 8080 to the service
kubectl port-forward service/neozork-interactive-service 8080:80

# Access the application
curl http://localhost:8080/health
```

## Configuration

### Environment Variables

The deployment uses several environment variables that can be customized:

- `PYTHONPATH`: Set to "/app" for proper Python module resolution
- `APPLE_SILICON`: Set to "true" for Apple Silicon optimizations
- `MLX_ENABLED`: Enable MLX framework for Apple Silicon

### Resource Requirements

The deployment includes resource requests and limits:

**Apple Silicon:**
- CPU: 1000m request, 2000m limit
- Memory: 2Gi request, 4Gi limit

**x86:**
- CPU: 500m request, 1000m limit
- Memory: 1Gi request, 2Gi limit

### Persistent Volumes

The deployment creates four persistent volume claims:

1. **Data Volume** (10Gi): Application data storage
2. **Logs Volume** (5Gi): Application logs
3. **Plots Volume** (5Gi): Generated plots and charts
4. **Results Volume** (10Gi): Analysis results

## Health Checks

The deployment includes comprehensive health checks:

### Liveness Probe
- **Path**: `/health`
- **Port**: 8080
- **Initial Delay**: 30 seconds
- **Period**: 10 seconds

### Readiness Probe
- **Path**: `/ready`
- **Port**: 8080
- **Initial Delay**: 5 seconds
- **Period**: 5 seconds

## Service Configuration

The deployment creates a LoadBalancer service that:
- Exposes the application on port 80
- Routes traffic to container port 8080
- Provides external access to the application

## Next Steps

After successful deployment:

1. **Configure Monitoring**: Set up Prometheus and Grafana for observability
2. **Set up Ingress**: Configure external access with SSL/TLS
3. **Scale the Application**: Adjust replica count based on load
4. **Backup Strategy**: Implement data backup for persistent volumes

## Troubleshooting

### Common Issues

**Pods not starting:**
```bash
# Check pod events
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>
```

**Service not accessible:**
```bash
# Check service endpoints
kubectl get endpoints

# Check service configuration
kubectl describe service neozork-interactive-service
```

**Persistent volume issues:**
```bash
# Check PVC status
kubectl get pvc

# Check PV status
kubectl get pv
```

### Getting Help

- Check the [Troubleshooting Guide](./troubleshooting-en.md) for detailed solutions
- Review the [Configuration Reference](./configuration-reference-en.md) for all options
- Open an issue in the project repository for support
