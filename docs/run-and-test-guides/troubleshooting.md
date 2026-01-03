# Troubleshooting / Troubleshooting

## 🆘 Common Issues / Common Issues

### installation Issues / installation Issues

#### UV not installed / UV not installed
```bash
# installation UV / install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# check installation / check installation
uv --version
```

#### dependencies / Dependency errors Errors
```bash
# clean cache UV / Clean UV cache
uv cache clean

# reinstall dependencies / reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
```

#### with Node.js / Node.js issues Issues
```bash
# clean cache npm / Clean npm cache
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
psql -h localhost -U neozork_user -d neozork_fund

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
# clean coverage cache / Clean coverage cache
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

# clean Docker / Clean Docker
docker system prune -a

# Restart Docker / Restart Docker
sudo systemctl Restart Docker
```

#### with volumes / Volume issues Issues
```bash
# View volumes / View volumes
docker volume ls

# clean volumes / Clean volumes
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

#### Pods not start / Pods don't start
```bash
# View событий / View events
kubectl get events

# description pod / Describe pod
kubectl describe pod <pod-name>

# Логи pod / Pod logs
kubectl logs <pod-name>
```

#### with сервисами / Service issues Issues
```bash
# View сервисов / View Services
kubectl get Services

# description сервиса / Describe service
kubectl describe service <service-name>

# check endpoints / check endpoints
kubectl get endpoints
```

#### with развертыванием / deployment issues Issues
```bash
# View развертываний / View deployments
kubectl get deployments

# description развертывания / Describe deployment
kubectl describe deployment <deployment-name>

# Откат развертывания / Rollback deployment
kubectl rollout undo deployment/<deployment-name>
```

## 🔧 Отладочные team / Debug Commands

### check статуса системы / system Status check
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

### Анализ логов / Log Analysis
```bash
# View all логов / View all logs
find logs/ -name "*.log" -exec tail -f {} \;

# Поиск ошибок / Search for errors
grep -r "ERROR" logs/

# Поиск предупреждений / Search for warnings
grep -r "WARNING" logs/

# Анализ производительности / Performance Analysis
grep -r "performance" logs/
```

### Отладочные скрипты / Debug Scripts
```bash
# Отладка данных / Debug data
python scripts/debug/debug_yfinance.py
python scripts/debug/debug_binance.py
python scripts/debug/debug_polygon.py

# Отладка indicators / Debug indicators
python scripts/debug/debug_rsi_signals.py
python scripts/debug/debug_wave_indicator.py

# Отладка системы / Debug system
python scripts/debug_docker_processes.py
python scripts/mcp/debug_mcp_detection.py
```

## 🛠️ Восстановление системы / system Recovery

### Полное восстановление / Full Recovery
```bash
# Остановка all сервисов / Stop all Services
docker-compose down
./scripts/native-container/stop.sh

# clean системы / Clean system
uv cache clean
docker system prune -a
./scripts/native-container/cleanup.sh --all --force

# reinstall dependencies / reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
cd src/mobile_app && npm install && cd ../..
cd src/admin_panel && npm install && cd ../..

# Launch сервисов / start Services
docker-compose up -d
```

### Восстановление данных / data Recovery
```bash
# Резервное копирование / Backup
docker-compose exec neozork-hld pg_dump -U neozork_user neozork_fund > backup.sql

# Восстановление / Restore
docker-compose exec neozork-hld psql -U neozork_user neozork_fund < backup.sql
```

### Восстановление конфигурации / Configuration Recovery
```bash
# Резервное копирование конфигурации / Backup configuration
tar -czf config-backup.tar.gz .env docker-compose.yml k8s/

# Восстановление конфигурации / Restore configuration
tar -xzf config-backup.tar.gz
```

## 📞 Получение помощи / Getting Help

### Логи and диагностика / Logs and Diagnostics
```bash
# Сбор диагностической информации / Collect diagnostic information
./scripts/utilities/collect_diagnostics.sh

# Отправка логов / Send logs
./scripts/utilities/send_logs.sh
```

### Сообщество / Community
- **GitHub Issues**: https://github.com/username/neozork-hld-Prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

### documentation / Documentation
- [Complete guide / Complete Manual](russian/complete-manual-ru.md)
- [guide on testing / testing Guide](russian/testing-guide-ru.md)
- [guide on deployment / deployment Guide](russian/deployment-guide-ru.md)
