# Deployment Guide - NeoZork HLD Prediction

## 🚀 Deployment Overview

The NeoZork HLD Prediction system supports various deployment options:
- Local deployment
- Docker containers
- Apple Silicon native containers
- Kubernetes clusters
- Production deployment

## 🏠 Local Deployment

### Installation and Setup
```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install dependencies
uv pip install -r requirements.txt

# Setup environment
cp env.example .env
nano .env
```

### Launch Services
```bash
# SaaS platform
uv run python run_saas.py

# Pocket Hedge Fund
uv run python run_pocket_hedge_fund.py

# Monitoring
uv run python -m src.monitoring.system_monitor
```

## 🐳 Docker Deployment

### Docker Compose
```bash
# Launch all services
docker-compose up -d

# Launch with logging
docker-compose up

# Stop
docker-compose down
```

### Service Management
```bash
# Restart services
docker-compose restart

# View logs
docker-compose logs -f neozork-hld

# Execute commands in container
docker-compose exec neozork-hld bash
```

### Production Docker
```bash
# Launch production services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

## 🍎 Apple Silicon Native Containers

### Native Container Setup
```bash
# Interactive launch
./scripts/native-container/native-container.sh

# Quick launch
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Check status
./scripts/native-container/run.sh --status
```

### Native Container Management
```bash
# Stop
./scripts/native-container/stop.sh

# Force restart
./scripts/native-container/force_restart.sh

# Cleanup
./scripts/native-container/cleanup.sh --all --force

# View logs
./scripts/native-container/logs.sh
```

## ☸️ Kubernetes Deployment

### Apply Manifests
```bash
# Apply all manifests
kubectl apply -f k8s/

# Apply specific manifest
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Check status
kubectl get pods
kubectl get services
kubectl get deployments
```

### Deployment Management
```bash
# Scaling
kubectl scale deployment neozork-app --replicas=3

# Update image
kubectl set image deployment/neozork-app neozork-app=neozork:latest

# Rollback
kubectl rollout undo deployment/neozork-app

# View status
kubectl rollout status deployment/neozork-app
```

## 🏭 Production Deployment

### Production Environment Setup
```bash
# Setup production configuration
python deploy/production_setup.py

# Validate configuration
python deploy/production_setup.py --validate

# Create production environment
python deploy/production_setup.py --create
```

### Production Containers
```bash
# Launch production services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Production Monitoring
```bash
# Health check
curl http://localhost:8080/health

# Prometheus metrics
curl http://localhost:9090/metrics

# Service status
kubectl get pods -o wide
```

## 🔧 Configuration

### Environment Variables
```bash
# Main settings
export HOST=0.0.0.0
export PORT=8080
export DEBUG=false

# Database settings
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=neozork_fund
export DB_USER=neozork_user
export DB_PASSWORD=neozork_password

# JWT settings
export JWT_SECRET=your-secret-key-change-in-production
```

### Configuration Files
```bash
# Docker configuration
docker-compose.yml
docker-compose.prod.yml
docker-compose.apple.yml

# Kubernetes manifests
k8s/neozork-apple-deployment.yaml

# Production settings
deploy/production_setup.py
```

## 📊 Monitoring and Logs

### View Logs
```bash
# Application logs
tail -f logs/pocket_hedge_fund.log
tail -f logs/saas_platform.log

# Docker logs
docker-compose logs -f neozork-hld

# Kubernetes logs
kubectl logs -f deployment/neozork-app
```

### System Monitoring
```bash
# Prometheus metrics
curl http://localhost:9090/metrics

# Health check
curl http://localhost:8080/health

# Service status
kubectl get pods
kubectl get services
```

## 🛠️ Maintenance

### System Updates
```bash
# Update code
git pull origin main

# Update dependencies
uv pip install --upgrade -r requirements.txt

# Rebuild containers
docker-compose build --no-cache

# Restart services
docker-compose restart
```

### Backup
```bash
# Backup data
docker-compose exec neozork-hld pg_dump -U neozork_user neozork_fund > backup.sql

# Backup configuration
tar -czf config-backup.tar.gz .env docker-compose.yml k8s/
```

### Restore
```bash
# Restore data
docker-compose exec neozork-hld psql -U neozork_user neozork_fund < backup.sql

# Restore configuration
tar -xzf config-backup.tar.gz
```

## 🆘 Troubleshooting

### Common Issues
1. **Port issues**: Check that ports 8080, 3000, 9090 are free
2. **Docker issues**: `docker system prune -a`
3. **Kubernetes issues**: `kubectl get events`
4. **Database issues**: Check PostgreSQL connection

### Debug Commands
```bash
# Check Docker status
docker-compose ps
docker images
docker volume ls

# Check Kubernetes status
kubectl get pods
kubectl get services
kubectl describe pod <pod-name>

# Check logs
docker-compose logs neozork-hld
kubectl logs <pod-name>
```

## 📚 Additional Resources

- [Complete Manual](complete-manual-en.md)
- [Quick Start](quick-start-en.md)
- [Testing Guide](testing-guide-en.md)
