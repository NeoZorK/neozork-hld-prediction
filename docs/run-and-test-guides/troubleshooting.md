# Устранение неполадок / Troubleshooting

## 🆘 Частые проблемы / Common Issues

### Проблемы с установкой / Installation Issues

#### UV не установлен / UV not installed
```bash
# Установка UV / Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Проверка установки / Check installation
uv --version
```

#### Ошибки зависимостей / Dependency errors
```bash
# Очистка кэша UV / Clean UV cache
uv cache clean

# Переустановка зависимостей / Reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
```

#### Проблемы с Node.js / Node.js issues
```bash
# Очистка кэша npm / Clean npm cache
npm cache clean --force

# Переустановка зависимостей / Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Проблемы с запуском / Launch Issues

#### Ошибки импорта / Import errors
```bash
# Проверка PYTHONPATH / Check PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Проверка установки пакета / Check package installation
uv pip list | grep neozork
```

#### Проблемы с портами / Port issues
```bash
# Проверка занятых портов / Check occupied ports
lsof -i :8080
lsof -i :3000
lsof -i :9090

# Освобождение портов / Free ports
kill -9 $(lsof -t -i:8080)
```

#### Проблемы с базой данных / Database issues
```bash
# Проверка подключения к PostgreSQL / Check PostgreSQL connection
psql -h localhost -U neozork_user -d neozork_fund

# Перезапуск PostgreSQL / Restart PostgreSQL
sudo systemctl restart postgresql
```

### Проблемы с тестированием / Testing Issues

#### Тесты не запускаются / Tests don't run
```bash
# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# Запуск с отладкой / Run with debugging
uv run pytest tests/ -v -s

# Запуск конкретного теста / Run specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

#### Проблемы с покрытием / Coverage issues
```bash
# Очистка кэша покрытия / Clean coverage cache
rm -rf .coverage htmlcov/

# Запуск с покрытием / Run with coverage
uv run pytest tests/ --cov=src --cov-report=html -n auto
```

#### Медленные тесты / Slow tests
```bash
# Запуск с таймаутом / Run with timeout
./scripts/run_tests_with_timeout.sh

# Запуск с ограниченными потоками / Run with limited threads
uv run pytest tests/ -n 2
```

### Проблемы с Docker / Docker Issues

#### Контейнеры не запускаются / Containers don't start
```bash
# Пересборка контейнеров / Rebuild containers
docker-compose build --no-cache

# Очистка Docker / Clean Docker
docker system prune -a

# Перезапуск Docker / Restart Docker
sudo systemctl restart docker
```

#### Проблемы с volumes / Volume issues
```bash
# Просмотр volumes / View volumes
docker volume ls

# Очистка volumes / Clean volumes
docker volume prune

# Создание volumes / Create volumes
docker volume create neozork_data
```

#### Проблемы с сетью / Network issues
```bash
# Просмотр сетей / View networks
docker network ls

# Очистка сетей / Clean networks
docker network prune

# Создание сети / Create network
docker network create neozork_network
```

### Проблемы с Kubernetes / Kubernetes Issues

#### Pods не запускаются / Pods don't start
```bash
# Просмотр событий / View events
kubectl get events

# Описание pod / Describe pod
kubectl describe pod <pod-name>

# Логи pod / Pod logs
kubectl logs <pod-name>
```

#### Проблемы с сервисами / Service issues
```bash
# Просмотр сервисов / View services
kubectl get services

# Описание сервиса / Describe service
kubectl describe service <service-name>

# Проверка endpoints / Check endpoints
kubectl get endpoints
```

#### Проблемы с развертыванием / Deployment issues
```bash
# Просмотр развертываний / View deployments
kubectl get deployments

# Описание развертывания / Describe deployment
kubectl describe deployment <deployment-name>

# Откат развертывания / Rollback deployment
kubectl rollout undo deployment/<deployment-name>
```

## 🔧 Отладочные команды / Debug Commands

### Проверка статуса системы / System Status Check
```bash
# Проверка UV / Check UV
python scripts/utilities/check_uv_mode.py --verbose

# Проверка MCP / Check MCP
python scripts/check_mcp_status.py

# Проверка Docker / Check Docker
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

# Отладка индикаторов / Debug indicators
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

# Очистка системы / Clean system
uv cache clean
docker system prune -a
./scripts/native-container/cleanup.sh --all --force

# Переустановка зависимостей / Reinstall dependencies
uv pip install -r requirements.txt --force-reinstall
cd mobile_app && npm install && cd ..
cd admin_panel && npm install && cd ..

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

### Логи и диагностика / Logs and Diagnostics
```bash
# Сбор диагностической информации / Collect diagnostic information
./scripts/utilities/collect_diagnostics.sh

# Отправка логов / Send logs
./scripts/utilities/send_logs.sh
```

### Сообщество / Community
- **GitHub Issues**: https://github.com/username/neozork-hld-prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

### Документация / Documentation
- [Полное руководство / Complete Manual](russian/complete-manual-ru.md)
- [Руководство по тестированию / Testing Guide](russian/testing-guide-ru.md)
- [Руководство по развертыванию / Deployment Guide](russian/deployment-guide-ru.md)
