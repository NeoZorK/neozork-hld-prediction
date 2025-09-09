# Pocket Hedge Fund - Production Deployment

This directory contains production deployment configuration for the Pocket Hedge Fund application.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- SSL certificates (for HTTPS)
- Domain name configured
- Environment variables configured

### 1. Environment Setup

```bash
# Copy environment template
cp env.prod.example .env.prod

# Edit environment variables
nano .env.prod
```

**Required Environment Variables:**
- `POSTGRES_PASSWORD` - Secure PostgreSQL password
- `REDIS_PASSWORD` - Secure Redis password  
- `JWT_SECRET_KEY` - JWT secret key (minimum 32 characters)
- `GRAFANA_PASSWORD` - Grafana admin password
- `CORS_ORIGINS` - Allowed CORS origins

### 2. SSL Certificates

Place your SSL certificates in the `nginx/ssl/` directory:
- `cert.pem` - SSL certificate
- `key.pem` - SSL private key

### 3. Deploy

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 📊 Services

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| **API** | 8000 | FastAPI application |
| **PostgreSQL** | 5432 | Primary database |
| **Redis** | 6379 | Caching and sessions |
| **Nginx** | 80/443 | Reverse proxy and SSL termination |

### Monitoring Services

| Service | Port | Description |
|---------|------|-------------|
| **Prometheus** | 9090 | Metrics collection |
| **Grafana** | 3000 | Monitoring dashboards |

## 🔧 Configuration

### Database

- **PostgreSQL 15** with Alpine Linux
- Connection pooling enabled
- Health checks configured
- Persistent volume for data

### Security

- **JWT Authentication** with configurable expiration
- **Rate Limiting** per endpoint
- **CORS** protection
- **Security Headers** (HSTS, CSP, XSS protection)
- **SSL/TLS** termination

### Performance

- **Gzip compression** enabled
- **Connection pooling** for database
- **Redis caching** for sessions
- **Nginx load balancing** ready

## 📈 Monitoring

### Prometheus Metrics

- API response times and error rates
- Database connection pool status
- Redis memory usage
- System resource utilization

### Grafana Dashboards

- Application performance metrics
- Database performance
- System health overview
- Custom business metrics

### Health Checks

All services include health check endpoints:
- API: `http://localhost:8000/health`
- Database: PostgreSQL health check
- Redis: Redis ping check
- Nginx: HTTP health check

## 🔄 Maintenance

### Database Backups

```bash
# Create backup
docker exec phf-postgres pg_dump -U phf_user pocket_hedge_fund > backup.sql

# Restore backup
docker exec -i phf-postgres psql -U phf_user pocket_hedge_fund < backup.sql
```

### Log Management

```bash
# View API logs
docker-compose -f docker-compose.prod.yml logs -f api

# View database logs
docker-compose -f docker-compose.prod.yml logs -f postgres

# View nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### Updates

```bash
# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Restart services
docker-compose -f docker-compose.prod.yml up -d

# Zero-downtime deployment (with proper load balancer)
docker-compose -f docker-compose.prod.yml up -d --no-deps api
```

## 🛡️ Security Best Practices

### Environment Security

- Use strong, unique passwords
- Rotate JWT secrets regularly
- Enable SSL/TLS encryption
- Configure proper CORS origins
- Use environment-specific configurations

### Network Security

- Firewall configuration
- VPN access for admin interfaces
- Regular security updates
- Monitor access logs

### Data Protection

- Encrypt sensitive data at rest
- Regular database backups
- Secure file upload handling
- Input validation and sanitization

## 📋 Troubleshooting

### Common Issues

1. **SSL Certificate Errors**
   - Verify certificate files are in correct location
   - Check certificate validity and permissions

2. **Database Connection Issues**
   - Verify PostgreSQL is running and accessible
   - Check database credentials and connection string

3. **API Not Responding**
   - Check API container logs
   - Verify environment variables
   - Check database connectivity

4. **High Memory Usage**
   - Monitor container resource usage
   - Adjust worker processes if needed
   - Check for memory leaks

### Debug Commands

```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View resource usage
docker stats

# Check network connectivity
docker exec phf-api ping postgres
docker exec phf-api ping redis

# Test API endpoints
curl -k https://localhost/health
curl -k https://localhost/api/v1/auth/health
```

## 🔄 Scaling

### Horizontal Scaling

To scale the API service:

```bash
# Scale API to 3 instances
docker-compose -f docker-compose.prod.yml up -d --scale api=3
```

### Load Balancer Configuration

For production, consider using an external load balancer (AWS ALB, CloudFlare, etc.) instead of Nginx for better scalability.

## 📞 Support

For deployment issues:
1. Check service logs
2. Verify environment configuration
3. Test individual service health
4. Review monitoring dashboards

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [PostgreSQL Administration](https://www.postgresql.org/docs/)
- [Prometheus Monitoring](https://prometheus.io/docs/)
- [Grafana Dashboards](https://grafana.com/docs/)
