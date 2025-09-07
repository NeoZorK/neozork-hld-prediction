#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Setup Script for NeoZork SaaS Platform

This script sets up the production environment for the SaaS platform including:
- Database configuration
- Environment variables
- SSL certificates
- Monitoring setup
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductionSetup:
    """Production setup manager for NeoZork SaaS Platform."""
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.deploy_dir = self.project_root / "deploy"
        
    def setup_environment(self):
        """Setup production environment variables."""
        logger.info("Setting up production environment...")
        
        env_vars = {
            "ENVIRONMENT": "production",
            "SAAS_HOST": "0.0.0.0",
            "SAAS_PORT": "8080",
            "DATABASE_URL": "postgresql://neozork:password@localhost:5432/neozork_saas",
            "REDIS_URL": "redis://localhost:6379/0",
            "STRIPE_SECRET_KEY": "sk_live_...",
            "STRIPE_PUBLISHABLE_KEY": "pk_live_...",
            "JWT_SECRET": "your-jwt-secret-key",
            "ENCRYPTION_KEY": "your-encryption-key",
            "SENTRY_DSN": "your-sentry-dsn",
            "LOG_LEVEL": "INFO"
        }
        
        env_file = self.project_root / ".env.production"
        with open(env_file, "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        logger.info(f"Environment variables written to {env_file}")
    
    def setup_database(self):
        """Setup production database."""
        logger.info("Setting up production database...")
        
        # Create database migration script
        migration_script = self.deploy_dir / "migrate_database.py"
        with open(migration_script, "w") as f:
            f.write("""
import asyncio
import asyncpg
from src.saas.models import *

async def create_tables():
    conn = await asyncpg.connect("postgresql://neozork:password@localhost:5432/neozork_saas")
    
    # Create tables for all SaaS models
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS tenants (
            tenant_id VARCHAR PRIMARY KEY,
            tenant_slug VARCHAR UNIQUE NOT NULL,
            name VARCHAR NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            tenant_type VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    ''')
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id VARCHAR PRIMARY KEY,
            tenant_id VARCHAR REFERENCES tenants(tenant_id),
            plan_id VARCHAR NOT NULL,
            tier VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            monthly_price DECIMAL(10,2),
            annual_price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    ''')
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR PRIMARY KEY,
            tenant_id VARCHAR REFERENCES tenants(tenant_id),
            user_id VARCHAR UNIQUE NOT NULL,
            first_name VARCHAR NOT NULL,
            last_name VARCHAR NOT NULL,
            email VARCHAR UNIQUE NOT NULL,
            customer_type VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
    ''')
    
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS usage_records (
            usage_id VARCHAR PRIMARY KEY,
            tenant_id VARCHAR REFERENCES tenants(tenant_id),
            customer_id VARCHAR REFERENCES customers(customer_id),
            usage_type VARCHAR NOT NULL,
            amount DECIMAL(15,2) NOT NULL,
            cost_per_unit DECIMAL(10,4),
            total_cost DECIMAL(15,2),
            timestamp TIMESTAMP DEFAULT NOW()
        );
    ''')
    
    await conn.close()
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
""")
        
        logger.info("Database migration script created")
    
    def setup_nginx(self):
        """Setup Nginx configuration."""
        logger.info("Setting up Nginx configuration...")
        
        nginx_config = self.deploy_dir / "nginx.conf"
        with open(nginx_config, "w") as f:
            f.write("""
upstream neozork_saas {
    server 127.0.0.1:8080;
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}

server {
    listen 80;
    server_name neozork-saas.com *.neozork-saas.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name neozork-saas.com *.neozork-saas.com;
    
    ssl_certificate /etc/ssl/certs/neozork-saas.crt;
    ssl_certificate_key /etc/ssl/private/neozork-saas.key;
    
    location / {
        proxy_pass http://neozork_saas;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /health {
        proxy_pass http://neozork_saas/health;
        access_log off;
    }
}
""")
        
        logger.info("Nginx configuration created")
    
    def setup_monitoring(self):
        """Setup monitoring configuration."""
        logger.info("Setting up monitoring configuration...")
        
        # Prometheus configuration
        prometheus_config = self.deploy_dir / "prometheus.yml"
        with open(prometheus_config, "w") as f:
            f.write("""
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'neozork-saas'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/metrics'
    scrape_interval: 5s
""")
        
        # Grafana dashboard configuration
        grafana_dashboard = self.deploy_dir / "grafana-dashboard.json"
        with open(grafana_dashboard, "w") as f:
            f.write("""
{
  "dashboard": {
    "title": "NeoZork SaaS Platform",
    "panels": [
      {
        "title": "API Requests",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Active Tenants",
        "type": "stat",
        "targets": [
          {
            "expr": "saas_active_tenants",
            "legendFormat": "Active Tenants"
          }
        ]
      },
      {
        "title": "Subscription Revenue",
        "type": "graph",
        "targets": [
          {
            "expr": "saas_monthly_revenue",
            "legendFormat": "Monthly Revenue"
          }
        ]
      }
    ]
  }
}
""")
        
        logger.info("Monitoring configuration created")
    
    def setup_docker(self):
        """Setup Docker configuration for production."""
        logger.info("Setting up Docker configuration...")
        
        dockerfile = self.deploy_dir / "Dockerfile.production"
        with open(dockerfile, "w") as f:
            f.write("""
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY run_saas.py .

# Create non-root user
RUN useradd -m -u 1000 neozork && chown -R neozork:neozork /app
USER neozork

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

# Start the application
CMD ["python", "run_saas.py"]
""")
        
        # Docker Compose for production
        docker_compose = self.deploy_dir / "docker-compose.production.yml"
        with open(docker_compose, "w") as f:
            f.write("""
version: '3.8'

services:
  neozork-saas:
    build:
      context: ..
      dockerfile: deploy/Dockerfile.production
    ports:
      - "8080:8080"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://neozork:password@postgres:5432/neozork_saas
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=neozork_saas
      - POSTGRES_USER=neozork
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - neozork-saas
    restart: unless-stopped
    
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped
    
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  grafana_data:
""")
        
        logger.info("Docker configuration created")
    
    def run_setup(self):
        """Run the complete production setup."""
        logger.info("Starting production setup...")
        
        # Create deploy directory
        self.deploy_dir.mkdir(exist_ok=True)
        
        # Run all setup steps
        self.setup_environment()
        self.setup_database()
        self.setup_nginx()
        self.setup_monitoring()
        self.setup_docker()
        
        logger.info("Production setup completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Review and update environment variables in .env.production")
        logger.info("2. Run database migration: python deploy/migrate_database.py")
        logger.info("3. Start services: docker-compose -f deploy/docker-compose.production.yml up -d")
        logger.info("4. Setup SSL certificates")
        logger.info("5. Configure domain and DNS")


if __name__ == "__main__":
    setup = ProductionSetup()
    setup.run_setup()
