# Production Deployment Guide - English

## Overview

This comprehensive guide covers production deployment for the NeoZork HLD Prediction system, including multiple deployment strategies, monitoring, and best practices.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Configuration Management](#configuration-management)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Security Configuration](#security-configuration)
8. [Backup and Recovery](#backup-and-recovery)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Prerequisites

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+), macOS (Apple Silicon), or Windows with WSL2
- **Memory**: Minimum 4GB RAM, Recommended 8GB+ RAM
- **Storage**: Minimum 20GB free space
- **CPU**: 2+ cores recommended

### Software Dependencies

- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Kubernetes**: Version 1.20+ (for K8s deployment)
- **Python**: Version 3.11+ (for native deployment)
- **UV Package Manager**: Latest version
- **PostgreSQL**: Version 15+ (if not using containerized version)
- **Redis**: Version 7+ (if not using containerized version)

### Network Requirements

- **Ports**: 80, 443, 8000, 5432, 6379, 9090, 3000
- **SSL Certificates**: Valid SSL certificates for HTTPS
- **Domain**: Configured domain name for production access

## Deployment Options

### 1. Docker Compose Deployment (Recommended for Small-Medium Scale)

#### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd neozork-hld-prediction

# Copy environment configuration
cp deployment/pocket_hedge_fund/env.prod.example .env.prod

# Edit environment variables
nano .env.prod

# Start production services
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml up -d
```

#### Services Included

| Service | Port | Description |
|---------|------|-------------|
| **API** | 8000 | FastAPI application |
| **PostgreSQL** | 5432 | Primary database |
| **Redis** | 6379 | Caching and sessions |
| **Nginx** | 80/443 | Reverse proxy and SSL termination |
| **Prometheus** | 9090 | Metrics collection |
| **Grafana** | 3000 | Monitoring dashboards |

### 2. Kubernetes Deployment (Recommended for Large Scale)

#### Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured
- Helm (optional, for package management)

#### Deployment Steps

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Check deployment status
kubectl get pods -l app=neozork-interactive

# Access services
kubectl port-forward service/neozork-interactive-service 8080:80
```

#### Features

- **Auto-scaling**: Horizontal Pod Autoscaler (HPA)
- **Load Balancing**: Kubernetes Service with LoadBalancer
- **Persistent Storage**: PVC for data, logs, and results
- **Health Checks**: Liveness and readiness probes
- **Resource Management**: CPU and memory limits

### 3. Apple Silicon Native Container (macOS Only)

#### Prerequisites

- Apple Silicon Mac (M1/M2/M3)
- Container runtime installed
- UV package manager

#### Deployment

```bash
# Run deployment script
./scripts/deploy_apple_container.sh

# Access application
open http://localhost:8080
```

#### Performance Benefits

- **30-50% faster** than Docker on Apple Silicon
- **Native MLX support** for machine learning acceleration
- **Optimized memory usage** for Apple Silicon architecture

## Configuration Management

### Environment Variables

#### Required Variables

```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password_here
DATABASE_URL=postgresql://phf_user:password@postgres:5432/pocket_hedge_fund

# Redis Configuration
REDIS_PASSWORD=your_secure_redis_password_here
REDIS_URL=redis://:password@redis:6379/0

# JWT Security
JWT_SECRET_KEY=your_very_secure_jwt_secret_key_here_minimum_32_characters

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Optional Variables

```bash
# CORS Configuration
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Monitoring
GRAFANA_PASSWORD=your_secure_grafana_password_here

# SSL Configuration
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
```

### Configuration Files

#### Production Config (`deployment/production/config.yaml`)

```yaml
# System Configuration
system:
  id: "neozork-pocket-hedge-fund"
  version: "1.0.0"
  environment: "production"
  debug_mode: false
  log_level: "INFO"
  max_workers: 8

# Database Configuration
database:
  type: "postgresql"
  host: "postgres"
  port: 5432
  database: "neozork_hld_prediction"
  username: "neozork"
  password: "${POSTGRES_PASSWORD}"
  pool_size: 20
  max_overflow: 30

# Security Configuration
security:
  ssl:
    enabled: true
    cert_path: "/etc/ssl/certs/neozork.crt"
    key_path: "/etc/ssl/private/neozork.key"
  firewall:
    enabled: true
    allowed_ports: [80, 443, 8000]
```

## Monitoring and Logging

### Prometheus Metrics

#### Key Metrics

- **Application Metrics**: Request rate, response time, error rate
- **Database Metrics**: Connection pool, query performance
- **System Metrics**: CPU, memory, disk usage
- **Business Metrics**: Trading signals, prediction accuracy

#### Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'neozork-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### Grafana Dashboards

#### Pre-configured Dashboards

1. **System Overview**: CPU, memory, disk usage
2. **Application Performance**: Request metrics, response times
3. **Database Performance**: Connection pools, query times
4. **Business Metrics**: Trading signals, predictions

#### Access

- **URL**: http://localhost:3000
- **Username**: admin
- **Password**: Set via `GRAFANA_PASSWORD` environment variable

### Logging Configuration

#### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations
- **CRITICAL**: Critical errors that may cause application failure

#### Log Formats

```python
# JSON format for production
LOG_FORMAT = "json"

# Structured logging example
{
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "INFO",
    "service": "neozork-api",
    "message": "Request processed",
    "request_id": "req-123",
    "duration_ms": 150
}
```

## Security Configuration

### SSL/TLS Configuration

#### Nginx SSL Setup

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Authentication and Authorization

#### JWT Configuration

```python
# JWT settings
JWT_SECRET_KEY = "your-very-secure-secret-key"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
```

#### Rate Limiting

```python
# Rate limiting configuration
RATE_LIMIT_REQUESTS = 100  # requests per minute
RATE_LIMIT_WINDOW = 60     # time window in seconds
```

### Security Headers

```python
# Security headers
SECURE_HEADERS = True
HSTS_MAX_AGE = 31536000  # 1 year
CONTENT_SECURITY_POLICY = "default-src 'self'"
```

## Backup and Recovery

### Database Backup

#### Automated Backup Script

```bash
#!/bin/bash
# Database backup script

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="neozork_backup_${DATE}.sql"

# Create backup
docker exec neozork-postgres pg_dump -U neozork neozork_hld_prediction > "${BACKUP_DIR}/${BACKUP_FILE}"

# Compress backup
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

# Remove old backups (keep 30 days)
find "${BACKUP_DIR}" -name "neozork_backup_*.sql.gz" -mtime +30 -delete
```

#### Backup Schedule

```bash
# Add to crontab for daily backups at 2 AM
0 2 * * * /path/to/backup_script.sh
```

### Application Data Backup

#### Backup Strategy

1. **Database**: Daily automated backups
2. **Application Logs**: Weekly rotation and archival
3. **Configuration**: Version controlled in Git
4. **User Data**: Real-time replication to secondary storage

### Recovery Procedures

#### Database Recovery

```bash
# Restore from backup
gunzip -c backup_file.sql.gz | docker exec -i neozork-postgres psql -U neozork neozork_hld_prediction
```

#### Application Recovery

```bash
# Restart services
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml restart

# Check service health
docker-compose -f deployment/pocket_hedge_fund/docker-compose.prod.yml ps
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Issues

**Symptoms**: Application fails to start, database connection errors

**Solutions**:
```bash
# Check database status
docker-compose logs postgres

# Verify database connectivity
docker exec -it neozork-postgres psql -U neozork -d neozork_hld_prediction

# Restart database service
docker-compose restart postgres
```

#### 2. Memory Issues

**Symptoms**: Application crashes, out of memory errors

**Solutions**:
```bash
# Check memory usage
docker stats

# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

#### 3. SSL Certificate Issues

**Symptoms**: HTTPS not working, certificate errors

**Solutions**:
```bash
# Verify certificate files
ls -la /etc/nginx/ssl/

# Check certificate validity
openssl x509 -in cert.pem -text -noout

# Restart nginx
docker-compose restart nginx
```

### Health Checks

#### Application Health Check

```bash
# Check application health
curl -f http://localhost:8000/health

# Check all services
docker-compose ps
```

#### Database Health Check

```bash
# Check database health
docker exec neozork-postgres pg_isready -U neozork -d neozork_hld_prediction
```

### Log Analysis

#### View Application Logs

```bash
# View recent logs
docker-compose logs --tail=100 api

# Follow logs in real-time
docker-compose logs -f api

# View specific service logs
docker-compose logs postgres
```

#### Log Analysis Commands

```bash
# Search for errors
docker-compose logs api | grep -i error

# Count error occurrences
docker-compose logs api | grep -c "ERROR"

# View logs by time range
docker-compose logs --since="2024-01-15T10:00:00" api
```

## Best Practices

### Performance Optimization

#### 1. Resource Allocation

```yaml
# Optimal resource allocation
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 1G
      cpus: '0.5'
```

#### 2. Database Optimization

```sql
-- Database optimization queries
CREATE INDEX CONCURRENTLY idx_trades_timestamp ON trades(timestamp);
CREATE INDEX CONCURRENTLY idx_predictions_symbol ON predictions(symbol);
VACUUM ANALYZE;
```

#### 3. Caching Strategy

```python
# Redis caching configuration
CACHE_TTL = 3600  # 1 hour
SESSION_TIMEOUT = 1800  # 30 minutes
MAX_CONNECTIONS = 1000
```

### Security Best Practices

#### 1. Environment Variables

- Use strong, unique passwords
- Rotate secrets regularly
- Never commit secrets to version control
- Use environment-specific configurations

#### 2. Network Security

- Use HTTPS everywhere
- Implement proper firewall rules
- Use VPN for administrative access
- Regular security updates

#### 3. Application Security

- Regular dependency updates
- Security scanning in CI/CD
- Input validation and sanitization
- Proper error handling

### Monitoring Best Practices

#### 1. Metrics Collection

- Collect business metrics alongside technical metrics
- Set up proper alerting thresholds
- Use structured logging
- Monitor external dependencies

#### 2. Alerting

```yaml
# Alert rules example
groups:
  - name: neozork-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
```

#### 3. Capacity Planning

- Monitor resource usage trends
- Plan for traffic spikes
- Regular performance testing
- Document scaling procedures

### Deployment Best Practices

#### 1. Blue-Green Deployment

```bash
# Blue-green deployment example
# Deploy to green environment
docker-compose -f docker-compose.green.yml up -d

# Test green environment
curl -f http://green.yourdomain.com/health

# Switch traffic to green
# Update load balancer configuration

# Decommission blue environment
docker-compose -f docker-compose.blue.yml down
```

#### 2. Rolling Updates

```bash
# Rolling update with zero downtime
docker-compose up -d --scale api=3
docker-compose up -d --no-deps api
```

#### 3. Health Checks

```yaml
# Comprehensive health checks
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Maintenance Procedures

#### 1. Regular Updates

- Weekly security updates
- Monthly dependency updates
- Quarterly major version updates
- Annual infrastructure review

#### 2. Backup Verification

- Weekly backup restoration tests
- Monthly disaster recovery drills
- Quarterly backup strategy review

#### 3. Performance Monitoring

- Daily performance metrics review
- Weekly capacity planning review
- Monthly optimization opportunities

## Support and Resources

### Documentation

- [API Documentation](http://localhost:8000/docs)
- [Configuration Reference](docs/configuration/)
- [Troubleshooting Guide](docs/troubleshooting/)

### Community

- GitHub Issues: Report bugs and feature requests
- Documentation: Contribute to documentation
- Discussions: Community support and discussions

### Professional Support

For enterprise support and consulting services, contact the development team.

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Maintainer**: NeoZork Development Team
