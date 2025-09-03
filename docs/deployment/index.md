# Deployment Documentation

This section covers production deployment configurations and best practices for the NeoZork HLD Prediction project.

> **📖 Complete Deployment Guide**: For comprehensive deployment documentation, see [DEPLOYMENT.md](DEPLOYMENT.md)

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## 🚀 Quick Start

### Production Deployment
```bash
# Production environment setup
./scripts/production/setup.sh

# Start production services
./scripts/production/start.sh

# Monitor services
./scripts/production/monitor.sh
```

### Local Development
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run application
python run_analysis.py
```

## 📚 Deployment Guides

### [Container Documentation](../containers/index.md) ⭐ **NEW**
Comprehensive container documentation including native and Docker containers.

**Key Features:**
- **Native Container**: Apple Silicon optimized with 30-50% performance improvement (limited to v0.5.2 and earlier versions)
- **Docker Container**: Cross-platform solution for all operating systems (limited to v0.5.2 and earlier versions)
- **Container Comparison**: Performance and feature analysis
- **Smart Container Logic**: Intelligent container state management

### [Production Deployment](production.md)
Production-ready deployment configurations and best practices.

### [Monitoring](monitoring.md)
System monitoring, logging, and health check configurations.

## 🔧 Configuration

### Production Environment Variables
```bash
# Production environment
NODE_ENV=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
API_KEY=your_api_key
```

### Environment Variables
```bash
# Production environment
NODE_ENV=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port
API_KEY=your_api_key

# Local environment
export NODE_ENV=development
export LOG_LEVEL=DEBUG
export DATABASE_URL=postgresql://localhost:5432/dev_db
```

## 🧪 Testing Deployment

### Production Testing
```bash
# Test production setup
pytest tests/production/test_deployment.py -v

# Test production configuration
pytest tests/production/ -v

# Run integration tests
./scripts/production/test.sh
```

### Local Environment
> **Note**: Docker testing is limited to v0.5.2 and earlier versions.

```bash
# Test adaptive functionality
pytest tests/docker/test_uv_simple.py -v

# Check UV status
python scripts/check_uv_mode.py --verbose
```

## 📊 Performance Metrics

### Production Performance
- **Response Time**: < 100ms average
- **Throughput**: 1000+ requests/second
- **Memory Usage**: Optimized for production
- **CPU Usage**: Efficient resource utilization
- **Database Performance**: Optimized queries and indexing

### Monitoring
- **Application Metrics**: Response times, error rates
- **System Metrics**: CPU, memory, disk usage
- **Database Metrics**: Query performance, connection pools
- **Network Metrics**: Bandwidth, latency

## 🔒 Security Considerations

### Production Security
- **HTTPS Only**: All communications encrypted
- **API Key Management**: Secure key storage and rotation
- **Database Security**: Encrypted connections and access control
- **Network Security**: Firewall and access controls
- **Input Validation**: Comprehensive input sanitization

### Security Best Practices
- **Non-root Execution**: Secure service operation
- **Package Verification**: Security checks for dependencies
- **Environment Isolation**: Proper environment separation
- **Regular Updates**: Security patches and updates

## 🚨 Troubleshooting

### Production Issues

#### Service Failures
```bash
# Check service status
./scripts/production/status.sh

# View service logs
./scripts/production/logs.sh

# Restart services
./scripts/production/restart.sh
```

#### Performance Issues
```bash
# Monitor system resources
./scripts/production/monitor.sh

# Check database performance
./scripts/production/db-status.sh

# Analyze logs
./scripts/production/analyze-logs.sh
```

### Common Issues

#### Database Connection Problems
```bash
# Check database connectivity
./scripts/production/test-db.sh

# Verify connection string
echo $DATABASE_URL

# Test database queries
./scripts/production/db-test.sh
```

#### API Key Issues
```bash
# Verify API key
./scripts/production/verify-api.sh

# Check API key permissions
./scripts/production/check-permissions.sh

# Rotate API key if needed
./scripts/production/rotate-api-key.sh
```

## 📈 Monitoring & Logging

### Production Monitoring
```bash
# Check service status
./scripts/production/status.sh

# View service logs
./scripts/production/logs.sh --follow

# Monitor system resources
./scripts/production/monitor.sh
```

### Health Checks
```bash
# Check service health
./scripts/production/health.sh

# View service logs
./scripts/production/logs.sh -f

# Monitor resource usage
./scripts/production/stats.sh
```

### Log Management
```bash
# View application logs
tail -f logs/app.log

# Check error logs
tail -f logs/error.log

# Monitor system logs
tail -f logs/system.log
```

## 🎯 Deployment Recommendations

### Production Environment
- **Use dedicated servers** for production workloads
- **Implement load balancing** for high availability
- **Set up monitoring** and alerting systems
- **Configure backup** and disaster recovery
- **Use CDN** for static content delivery

### Security Best Practices
- **Regular security audits** and penetration testing
- **Implement rate limiting** and DDoS protection
- **Use secure communication** protocols (HTTPS, WSS)
- **Monitor for security** incidents and anomalies

### Performance Optimization
- **Database optimization** with proper indexing
- **Caching strategies** for frequently accessed data
- **CDN integration** for static assets
- **Load balancing** for distributed workloads

## 🔄 Updates & Maintenance

### Updating Production
```bash
# Backup current deployment
./scripts/production/backup.sh

# Deploy new version
./scripts/production/deploy.sh

# Verify deployment
./scripts/production/verify.sh

# Rollback if needed
./scripts/production/rollback.sh
```

### System Updates
```bash
# Update system packages
./scripts/production/update-system.sh

# Update application dependencies
./scripts/production/update-deps.sh

# Restart services
./scripts/production/restart.sh
```

## 📚 Additional Resources

- [Production Best Practices](https://docs.example.com/production)
- [Monitoring Guide](https://docs.example.com/monitoring)
- [Security Guidelines](https://docs.example.com/security)
- [Project Issues](https://github.com/username/neozork-hld-prediction/issues)

---

**Last Updated**: 2024
**Version**: 2.0.0 (Production Ready) 