# Deployment Guide

## Overview

This guide covers deploying the Neozork HLD Prediction system in various environments, from local development to production.

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows (10+)
- **Python**: 3.9+ (3.11+ recommended)
- **Memory**: 4GB+ RAM (8GB+ for production)
- **Storage**: 10GB+ free space
- **Network**: Internet access for package installation

### Software Dependencies
- **UV**: Python package manager
- **Git**: Version control
- **Docker**: Container deployment (optional)
- **System packages**: build-essential, python3-dev

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/neozork-hld-prediction.git
cd neozork-hld-prediction
```

### 2. Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Install Dependencies
```bash
# Install all dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

### 4. Verify Installation
```bash
# Run tests
uv run pytest tests/ -v

# Test CLI
uv run python -m src.cli.core.cli --help

# Check imports
uv run python -c "import src; print('Import successful')"
```

## Production Deployment

### 1. Server Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv build-essential python3-dev

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Application Deployment
```bash
# Create application directory
sudo mkdir -p /opt/neozork
sudo chown $USER:$USER /opt/neozork

# Clone repository
cd /opt/neozork
git clone https://github.com/your-org/neozork-hld-prediction.git .

# Install dependencies
uv sync --frozen-lockfile

# Create production configuration
cp config.json config.production.json
# Edit config.production.json for production settings
```

### 3. System Service Setup
```bash
# Create systemd service file
sudo tee /etc/systemd/system/neozork.service > /dev/null <<EOF
[Unit]
Description=Neozork HLD Prediction System
After=network.target

[Service]
Type=simple
User=neozork
WorkingDirectory=/opt/neozork
Environment=PATH=/opt/neozork/.venv/bin
Environment=NEOZORK_ENV=production
ExecStart=/opt/neozork/.venv/bin/python -m src.cli.core.cli
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create system user
sudo useradd -r -s /bin/false neozork
sudo chown -R neozork:neozork /opt/neozork

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable neozork
sudo systemctl start neozork
sudo systemctl status neozork
```

### 4. Nginx Configuration (Optional)
```bash
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/neozork > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/neozork /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Docker Deployment

### 1. Build Image
```bash
# Build Docker image
docker build -t neozork:latest .

# Tag for registry
docker tag neozork:latest your-registry.com/neozork:latest
```

### 2. Docker Compose
```bash
# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'
services:
  neozork:
    image: neozork:latest
    container_name: neozork-app
    environment:
      - NEOZORK_ENV=production
      - NEOZORK_CONFIG_PATH=/app/config.json
    volumes:
      - ./config.json:/app/config.json:ro
      - ./data:/app/data
      - ./logs:/app/logs
      - ./models:/app/models
    ports:
      - "8000:8000"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import src; print('OK')"]
      interval: 30s
      timeout: 10s
      retries: 3

  neozork-worker:
    image: neozork:latest
    container_name: neozork-worker
    environment:
      - NEOZORK_ENV=production
      - NEOZORK_WORKER_MODE=true
    volumes:
      - ./config.json:/app/config.json:ro
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    depends_on:
      - neozork
EOF

# Start services
docker-compose up -d
```

### 3. Kubernetes Deployment
```yaml
# neozork-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork
  labels:
    app: neozork
spec:
  replicas: 3
  selector:
    matchLabels:
      app: neozork
  template:
    metadata:
      labels:
        app: neozork
    spec:
      containers:
      - name: neozork
        image: your-registry.com/neozork:latest
        ports:
        - containerPort: 8000
        env:
        - name: NEOZORK_ENV
          value: "production"
        - name: NEOZORK_CONFIG_PATH
          value: "/app/config.json"
        volumeMounts:
        - name: config
          mountPath: /app/config.json
          subPath: config.json
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
        - name: models
          mountPath: /app/models
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
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
      - name: models
        persistentVolumeClaim:
          claimName: neozork-models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: neozork-service
spec:
  selector:
    app: neozork
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Environment-Specific Configurations

### Development Environment
```json
{
  "system": {"environment": "development"},
  "logging": {"level": "DEBUG"},
  "development": {"debug_mode": true},
  "performance": {"caching": {"enabled": false}}
}
```

### Staging Environment
```json
{
  "system": {"environment": "staging"},
  "logging": {"level": "INFO"},
  "development": {"debug_mode": false},
  "performance": {"caching": {"enabled": true}},
  "data": {"cache_dir": "/tmp/neozork-staging"}
}
```

### Production Environment
```json
{
  "system": {"environment": "production"},
  "logging": {"level": "WARNING"},
  "development": {"debug_mode": false},
  "performance": {"caching": {"enabled": true}},
  "security": {"strict_mode": true},
  "monitoring": {"health_checks": {"enabled": true}}
}
```

## Monitoring and Health Checks

### 1. Health Check Endpoint
```python
# Add to your CLI or web interface
@app.route('/health')
def health_check():
    try:
        # Check database connectivity
        # Check file system access
        # Check ML model availability
        return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

### 2. Logging Configuration
```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/neozork.log",
    "max_size_mb": 100,
    "backup_count": 10,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
      "console": {"enabled": true, "level": "INFO"},
      "file": {"enabled": true, "level": "DEBUG"},
      "syslog": {"enabled": true, "level": "WARNING"}
    }
  }
}
```

### 3. Metrics Collection
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
requests_total = Counter('neozork_requests_total', 'Total requests')
request_duration = Histogram('neozork_request_duration_seconds', 'Request duration')
active_connections = Gauge('neozork_active_connections', 'Active connections')

# Export metrics endpoint
@app.route('/metrics')
def metrics():
    return generate_latest()
```

## Security Considerations

### 1. Access Control
```bash
# Restrict file permissions
chmod 600 config.json
chown neozork:neozork config.json

# Use dedicated user
sudo useradd -r -s /bin/false neozork
sudo chown -R neozork:neozork /opt/neozork
```

### 2. Network Security
```bash
# Firewall configuration
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Restrict access to application ports
sudo ufw allow from 192.168.1.0/24 to any port 8000
```

### 3. SSL/TLS Configuration
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Backup and Recovery

### 1. Data Backup
```bash
# Create backup script
cat > backup.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/backup/neozork/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup configuration
cp config.json "$BACKUP_DIR/"

# Backup data
tar -czf "$BACKUP_DIR/data.tar.gz" data/

# Backup models
tar -czf "$BACKUP_DIR/models.tar.gz" models/

# Backup logs
tar -czf "$BACKUP_DIR/logs.tar.gz" logs/

# Cleanup old backups (keep last 7 days)
find /backup/neozork -type d -mtime +7 -exec rm -rf {} \;
EOF

chmod +x backup.sh

# Add to crontab
echo "0 2 * * * /opt/neozork/backup.sh" | crontab -
```

### 2. Recovery Procedures
```bash
# Restore from backup
BACKUP_DATE="20241201_143000"
BACKUP_DIR="/backup/neozork/$BACKUP_DATE"

# Stop services
sudo systemctl stop neozork

# Restore data
tar -xzf "$BACKUP_DIR/data.tar.gz" -C /
tar -xzf "$BACKUP_DIR/models.tar.gz" -C /
tar -xzf "$BACKUP_DIR/logs.tar.gz" -C /

# Restore configuration
cp "$BACKUP_DIR/config.json" /opt/neozork/

# Start services
sudo systemctl start neozork
```

## Performance Optimization

### 1. System Tuning
```bash
# Increase file descriptor limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize kernel parameters
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "vm.dirty_ratio=15" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. Application Optimization
```json
{
  "performance": {
    "parallel_processing": {
      "enabled": true,
      "max_workers": 8,
      "chunk_size": 1000
    },
    "caching": {
      "enabled": true,
      "max_size_mb": 500,
      "ttl_seconds": 7200
    },
    "memory": {
      "max_usage_mb": 2048,
      "cleanup_threshold": 0.8
    }
  }
}
```

## Troubleshooting

### 1. Common Issues

#### Service Won't Start
```bash
# Check service status
sudo systemctl status neozork

# Check logs
sudo journalctl -u neozork -f

# Check configuration
python -m json.tool config.json
```

#### Permission Denied
```bash
# Fix file permissions
sudo chown -R neozork:neozork /opt/neozork
sudo chmod 755 /opt/neozork
sudo chmod 600 /opt/neozork/config.json
```

#### Out of Memory
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head

# Adjust memory limits in configuration
# Increase swap space if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 2. Debug Mode
```bash
# Enable debug logging
export NEOZORK_LOG_LEVEL=DEBUG

# Run with verbose output
uv run python -m src.cli.core.cli --verbose --debug

# Check configuration loading
uv run python -c "
from src.core.config import config
print('Config loaded:', config._config)
print('Config path:', config.config_path)
"
```

## CI/CD Pipeline

### 1. GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install UV
      run: |
        curl -LsSf https://astral.sh/uv/install.sh | sh
        echo "$HOME/.cargo/bin" >> $GITHUB_PATH
    
    - name: Install dependencies
      run: uv sync --frozen-lockfile
    
    - name: Run tests
      run: uv run pytest tests/ --cov=src
    
    - name: Build Docker image
      run: docker build -t neozork:${{ github.sha }} .
    
    - name: Deploy to server
      run: |
        # Deploy to your production server
        # This could be via SSH, Kubernetes, etc.
```

### 2. Pre-deployment Checks
```bash
#!/bin/bash
# pre-deploy.sh

echo "Running pre-deployment checks..."

# Run tests
uv run pytest tests/ -v --tb=short

# Check code quality
uv run black --check src/
uv run isort --check-only src/
uv run mypy src/

# Security scan
uv run bandit -r src/

# Dependency check
uv run safety check

echo "Pre-deployment checks completed."
```

## Maintenance

### 1. Regular Updates
```bash
# Update dependencies
uv sync --upgrade

# Update application
git pull origin main
uv sync

# Restart services
sudo systemctl restart neozork
```

### 2. Log Rotation
```bash
# Configure logrotate
sudo tee /etc/logrotate.d/neozork > /dev/null <<EOF
/opt/neozork/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 neozork neozork
    postrotate
        systemctl reload neozork
    endscript
}
EOF
```

### 3. Health Monitoring
```bash
# Create monitoring script
cat > monitor.sh <<'EOF'
#!/bin/bash
# Check service status
if ! systemctl is-active --quiet neozork; then
    echo "Neozork service is down!" | mail -s "Service Alert" admin@example.com
    systemctl restart neozork
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "Disk usage is ${DISK_USAGE}%" | mail -s "Disk Alert" admin@example.com
fi
EOF

chmod +x monitor.sh

# Add to crontab
echo "*/5 * * * * /opt/neozork/monitor.sh" | crontab -
```

## Support and Documentation

### 1. Getting Help
- **Documentation**: Check `docs/` directory
- **Issues**: GitHub Issues repository
- **Discussions**: GitHub Discussions
- **Wiki**: Project wiki for common problems

### 2. Contributing to Deployment
- **Documentation**: Update deployment guides
- **Scripts**: Improve automation scripts
- **Testing**: Test deployment procedures
- **Monitoring**: Enhance monitoring and alerting

### 3. Emergency Procedures
```bash
# Emergency restart
sudo systemctl stop neozork
sudo systemctl start neozork

# Rollback to previous version
git checkout HEAD~1
uv sync
sudo systemctl restart neozork

# Emergency configuration
cp config.emergency.json config.json
sudo systemctl restart neozork
```
