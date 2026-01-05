# Troubleshooting / Troubleshooting

## 🆘 Common Issues / Common Issues

### installation Issues / installation Issues

#### UV not installed / UV not installed
```bash
# installation UV / install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# installation check / installation check
uv --version
```

#### dependencies / Dependency errors Errors
```bash
# clean cache UV / clean UV cache
uv cache clean

# reinstall dependencies / reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
```

#### with Node.js / Node.js issues Issues
```bash
# clean cache npm / clean npm cache
npm cache clean --force

# reinstall dependencies / reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Launch Issues / Launch Issues

#### import / import Errors Errors
```bash
# check PYTHONPATH / check PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# check package installation / check package installation
uv pip List | grep neozork
```

#### with ports / Port Issues Issues
```bash
# check occupied ports / check occupied ports
lsof -i :8080
lsof -i :3000
lsof -i :9090

# Free ports / Free ports
kill -9 $(lsof -t -i:8080)
```

#### with database / database issues Issues
```bash
# check PostgreSQL connection / check PostgreSQL connection
psql -h localhost -U neozork_User -d neozork_fund

# Restart PostgreSQL / Restart PostgreSQL
sudo systemctl Restart PostgreSQL
```

### Issues with testing / testing Issues

#### tests do not start / tests don't run
```bash
# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# Launch with debugging / Run with debugging
uv run pytest tests/ -v -s

# Launch specific test / Run specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

#### with coverage / coverage issues Issues
```bash
# clean coverage cache / clean coverage cache
rm -rf .coverage htmlcov/

# Launch with coverage / Run with coverage
uv run pytest tests/ --cov=src --cov-Report=html -n auto
```

#### Slow tests / Slow tests
```bash
# Launch with timeout / Run with timeout
./scripts/run_tests_with_timeout.sh

# Launch with limited threads / Run with limited threads
uv run pytest tests/ -n 2
```

### Issues with Docker / Docker Issues

#### Containers do not start / Containers don't start
```bash
# Rebuild containers / Rebuild containers
docker-compose build --no-cache

# clean Docker / clean Docker
docker system prune -a

# Restart Docker / Restart Docker
sudo systemctl Restart Docker
```

#### with volumes / Volume issues Issues
```bash
# View volumes / View volumes
docker volume ls

# clean volumes / clean volumes
docker volume prune

# create volumes / Create volumes
docker volume create neozork_data
```

#### with network / network issues Issues
```bash
# View networks / View networks
docker network ls

# clean networks / clean networks
docker network prune

# create network / create network
docker network create neozork_network
```

### Issues with Kubernetes / Kubernetes Issues

#### pods not start / pods don't start
```bash
# View events / View events
kubectl get events

# describe pod / describe pod
kubectl describe pod <pod-name>

# pod Logs / pod Logs
kubectl Logs <pod-name>
```

#### with services / service issues Issues
```bash
# View services / View services
kubectl get services

# describe service / describe service
kubectl describe service <service-name>

# check endpoints / check endpoints
kubectl get endpoints
```

#### with deployment / deployment issues Issues
```bash
# View deployments / View deployments
kubectl get deployments

# describe deployment / describe deployment
kubectl describe deployment <deployment-name>

# Rollback deployment / Rollback deployment
kubectl rollout undo deployment/<deployment-name>
```

## ♪ Debug Commands

### check system status / system Status check
```bash
# check UV / check UV
python scripts/utilities/check_uv_mode.py --verbose

# check MCP / check MCP
python scripts/check_mcp_status.py

# check Docker / check Docker
docker-compose ps
docker images
docker volume ls
```

### Laundry analysis / Log Analysis
```bash
# View all logs
find Logs/ -name "*.log" -exec tail -f {} \;

# Searching for Errors
grep -r "ERROR" Logs/

# Searching for Warnings / Search for Warnings
grep -r "WARNING" Logs/

# Performance analysis / Performance Analysis
grep -r "performance" Logs/
```

### Debug Scripts
```bash
# Data debug data
python scripts/debug/debug_yfinance.py
python scripts/debug/debug_binance.py
python scripts/debug/debug_polygon.py

# Debug indicators
python scripts/debug/debug_rsi_signals.py
python scripts/debug/debug_wave_indicator.py

# Debug system debug system
python scripts/debug_docker_processes.py
python scripts/mcp/debug_mcp_detection.py
```

## ♪ Recovery system / system Recovery

### Full recovery / Full Recovery
```bash
# Stopping all services
docker-compose down
./scripts/native-container/stop.sh

# Clear System / Clear System
uv cache clean
docker system prune -a
./scripts/native-container/cleanup.sh --all --force

# reinstall dependencies / reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
cd src/mobile_app && npm install && cd ../..
cd src/admin_panel && npm install && cd ../..

# Launch services / start services
docker-compose up -d
```

### Data recovery / data Recovery
```bash
# Backup / Backup
docker-compose exec neozork-hld pg_dump -U neozork_User neozork_fund > backup.sql

# Recovery / Restore
docker-compose exec neozork-hld psql -U neozork_User neozork_fund < backup.sql
```

### Reconfiguring configuration / Configuring Recovery
```bash
# Backup configration backup
tar -czf config-backup.tar.gz .env docker-compose.yml k8s/

# Restore configuration / Restore conference
tar -xzf config-backup.tar.gz
```

## * Get help / Getting Help

### Logs and diagnostics / Logs and Diagnostics
```bash
# Collection of diagnostic information / Collection Diagnostic information
./scripts/utilities/collect_diagnostics.sh

# Sending logs / Sand Logs
./scripts/utilities/send_Logs.sh
```

### Community / Community
- **GitHub Issues**: https://github.com/Username/neozork-hld-Prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

### documentation / Documentation
- [Complete guide / Complete Manual](russian/complete-manual-ru.md)
- [guide on testing / testing Guide](russian/testing-guide-ru.md)
- [guide on deployment / deployment Guide](russian/deployment-guide-ru.md)
