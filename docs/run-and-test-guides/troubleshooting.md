# Troubleshooting / Troubleshooting

## 🆘 Common Issues / Common Issues

### Installation Issues / Installation Issues

#### UV not installed / UV not installed
```bash
# Installation UV / Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# check установки / Check installation
uv --version
```

#### зависимостей / Dependency errors Errors
```bash
# clean cache UV / Clean UV cache
uv cache clean

# reinstall зависимостей / Reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
```

#### with Node.js / Node.js issues Issues
```bash
# clean cache npm / Clean npm cache
npm cache clean --force

# reinstall зависимостей / Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Launch Issues / Launch Issues

#### импорта / Import Errors Errors
```bash
# check PYTHONPATH / Check PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# check package installation / Check package installation
uv pip list | grep neozork
```

#### with портами / Port Issues Issues
```bash
# check occupied ports / Check occupied ports
lsof -i :8080
lsof -i :3000
lsof -i :9090

# Free ports / Free ports
kill -9 $(lsof -t -i:8080)
```

#### with database / Database issues Issues
```bash
# check PostgreSQL connection / Check PostgreSQL connection
psql -h localhost -U neozork_user -d neozork_fund

# Restart PostgreSQL / Restart PostgreSQL
sudo systemctl restart postgresql
```

### Проблемы with testing / Testing Issues

#### Тесты not start / Tests don't run
```bash
# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# Запуск with отладкой / Run with debugging
uv run pytest tests/ -v -s

# Запуск specific test / Run specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

#### with coverage / Coverage issues Issues
```bash
# clean coverage cache / Clean coverage cache
rm -rf .coverage htmlcov/

# Запуск with coverage / Run with coverage
uv run pytest tests/ --cov=src --cov-report=html -n auto
```

#### Медленные тесты / Slow tests
```bash
# Запуск with таймаутом / Run with timeout
./scripts/run_tests_with_timeout.sh

# Запуск with ограниченными потоками / Run with limited threads
uv run pytest tests/ -n 2
```

### Проблемы with Docker / Docker Issues

#### Контейнеры not start / Containers don't start
```bash
# Rebuild containers / Rebuild containers
docker-compose build --no-cache

# clean Docker / Clean Docker
docker system prune -a

# Restart Docker / Restart Docker
sudo systemctl restart docker
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

#### with network / Network issues Issues
```bash
# Просмотр сетей / View networks
docker network ls

# clean сетей / Clean networks
docker network prune

# create сети / Create network
docker network create neozork_network
```

### Проблемы with Kubernetes / Kubernetes Issues

#### Pods not start / Pods don't start
```bash
# Просмотр событий / View events
kubectl get events

# description pod / Describe pod
kubectl describe pod <pod-name>

# Логи pod / Pod logs
kubectl logs <pod-name>
```

#### with сервисами / Service issues Issues
```bash
# Просмотр сервисов / View services
kubectl get services

# description сервиса / Describe service
kubectl describe service <service-name>

# check endpoints / Check endpoints
kubectl get endpoints
```

#### with развертыванием / Deployment issues Issues
```bash
# Просмотр развертываний / View deployments
kubectl get deployments

# description развертывания / Describe deployment
kubectl describe deployment <deployment-name>

# Откат развертывания / Rollback deployment
kubectl rollout undo deployment/<deployment-name>
```

## 🔧 Отладочные команды / Debug Commands

### check статуса системы / System Status Check
```bash
# check UV / Check UV
python scripts/utilities/check_uv_mode.py --verbose

# check MCP / Check MCP
python scripts/check_mcp_status.py

# check Docker / Check Docker
docker-compose ps
docker images
docker volume ls
```

### Анализ логов / Log Analysis
```bash
# Просмотр всех логов / View all logs
find logs/ -name "*.log" -exec tail -f {} \;

# Поиск ошибок / Search for errors
grep -r "ERROR" logs/

# Поиск предупреждений / Search for warnings
grep -r "WARNING" logs/

# Анализ производительности / Performance analysis
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

## 🛠️ Восстановление системы / System Recovery

### Полное восстановление / Full Recovery
```bash
# Остановка всех сервисов / Stop all services
docker-compose down
./scripts/native-container/stop.sh

# clean системы / Clean system
uv cache clean
docker system prune -a
./scripts/native-container/cleanup.sh --all --force

# reinstall зависимостей / Reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
cd src/mobile_app && npm install && cd ../..
cd src/admin_panel && npm install && cd ../..

# Запуск сервисов / Start services
docker-compose up -d
```

### Восстановление данных / Data Recovery
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
- [Полное guide / Complete Manual](russian/complete-manual-ru.md)
- [guide on тестированию / Testing Guide](russian/testing-guide-ru.md)
- [guide on развертыванию / Deployment Guide](russian/deployment-guide-ru.md)
