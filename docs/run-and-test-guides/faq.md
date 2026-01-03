# Frequently Asked Questions / Frequently Asked Questions

## 🚀 General questions / General questions

### Q: How to quickly Launch the system? / How to quickly Launch the system?
**A:** Use Quick start:
```bash
# installation dependencies / install dependencies
uv pip install -r requirements.txt

# Launch main Analysis / Launch main Analysis
uv run run_Analysis.py demo --rule PHLD

# Run all tests / Run all tests
uv run pytest tests -n auto
```

### Q: What components are included in the system? / What components are included in the system?
**A:** Система включает:
- **Основной анализ** (`run_Analysis.py`) - Ручное построение графиков / Manual charting
- **Интерактивная система** (`interactive/`) - ML торговые стратегии / ML trading strategies
- **SaaS platform** (`src/saas/`) - Облачная platform / Cloud platform
- **Pocket Hedge fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
- **mobile application** (`src/mobile_app/`) - React Native application / React Native app
- **Админ панель** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel
- **Monitoring** (`src/Monitoring/`) - Система Monitoringа / Monitoring system

### Q: What требования к системе? / What are the system requirements?
**A:** Минимальные требования:
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 20.10+ (опционально / optional)
- **UV**: Последняя версия / Latest version
- **Память / Memory**: 4GB RAM
- **Диск / Disk**: 10GB свободного места / free space

## 🧪 Вопросы on testing / testing Questions

### Q: Как запустить все тесты? / How to Run all tests?
**A:** Use многопоточное тестирование:
```bash
# Все тесты / all tests
uv run pytest tests -n auto

# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with coverage / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Q: Как запустить тесты конкретного компонента? / How to run tests for specific component?
**A:** Запустите тесты on категориям:
```bash
# Тесты расчетов / Calculation tests
uv run pytest tests/calculation/ -n auto

# Тесты SaaS / SaaS tests
uv run pytest tests/saas/ -n auto

# Тесты Pocket Hedge fund / Pocket Hedge fund tests
uv run pytest tests/pocket_hedge_fund/ -n auto
```

### Q: Что делать, если tests do not start? / What to do if tests don't run?
**A:** Попробуйте Safe mode:
```bash
# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with debugging / with debugging
uv run pytest tests/ -v -s

# Конкретный тест / specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

## 🐳 Вопросы on Docker / Docker Questions

### Q: Как Launch the system in Docker? / How to run system in Docker?
**A:** Use Docker Compose:
```bash
# Launch all services / Launch all services
docker-compose up -d

# Launch with Logsрованием / Launch with logging
docker-compose up

# Остановка / Stop
docker-compose down
```

### Q: Как запустить тесты in Docker? / How to run tests in Docker?
**A:** execute team in контейнере:
```bash
# Тесты in контейнере / tests in container
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Конкретные тесты / specific tests
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v
```

### Q: Что делать, если Docker not Launchается? / What to do if Docker doesn't start?
**A:** Попробуйте пересборку:
```bash
# Rebuild containers / Rebuild containers
docker-compose build --no-cache

# clean Docker / clean Docker
docker system prune -a

# Restart Docker / Restart Docker
sudo systemctl Restart Docker
```

## 🍎 Вопросы on Apple Silicon / Apple Silicon Questions

### Q: Как запустить нативный контейнер? / How to run native container?
**A:** Use скрипты нативного контейнера:
```bash
# Интерактивный Launch / Interactive Launch
./scripts/native-container/native-container.sh

# Быстрый Launch / Quick Launch
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# check статуса / check status
./scripts/native-container/run.sh --status
```

### Q: Как управлять нативным контейнером? / How to manage native container?
**A:** Use team управления:
```bash
# Остановка / Stop
./scripts/native-container/stop.sh

# ПереLaunch / Restart
./scripts/native-container/force_restart.sh

# clean / cleanup
./scripts/native-container/cleanup.sh --all --force
```

## 🚀 Вопросы on deployment / deployment Questions

### Q: Как развернуть system in продакшне? / How to deploy system in production?
**A:** Use продакшн конфигурацию:
```bash
# configuration продакшна / Setup production
python deploy/production_setup.py

# Launch продакшн services / Launch production services
docker-compose -f docker-compose.prod.yml up -d
```

### Q: Как развернуть in Kubernetes? / How to deploy in Kubernetes?
**A:** Примените манифесты:
```bash
# Применение манифестов / Apply manifests
kubectl apply -f k8s/

# check статуса / check status
kubectl get pods
kubectl get services
```

## 🔧 Вопросы on настройке / Configuration Questions

### Q: Как настроить переменные окружения? / How to configure environment variables?
**A:** Отредактируйте файл .env:
```bash
# Копирование примера / Copy example
cp env.example .env

# Редактирование / Edit
nano .env
```

### Q: Как настроить базу данных? / How to configure database?
**A:** install PostgreSQL and настройте переменные:
```bash
# installation PostgreSQL / install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# create базы данных / Create database
createdb neozork_fund

# configuration User / Configure User
createUser neozork_User
```

## 📊 Вопросы on Monitoringу / Monitoring Questions

### Q: Как Viewеть Logs? / How to View Logs?
**A:** Use team Viewа логов:
```bash
# Logs приложения / application Logs
tail -f Logs/pocket_hedge_fund.log

# Docker Logs / Docker Logs
docker-compose Logs -f neozork-hld

# Все Logs / all Logs
tail -f Logs/*.log
```

### Q: Как проверить статус системы? / How to check system status?
**A:** Use team проверки:
```bash
# health check / health check
curl http://localhost:8080/health

# Prometheus metrics / Prometheus metrics
curl http://localhost:9090/metrics

# Статус Docker / Docker status
docker-compose ps
```

## 🆘 Вопросы on устранению неполадок / Troubleshooting Questions

### Q: Что делать, если возникают import Errors? / What to do if import Errors occur?
**A:** Проверьте PYTHONPATH:
```bash
# installation PYTHONPATH / Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# installation check / installation check
uv pip List | grep neozork
```

### Q: Что делать, если тесты медленно Workingют? / What to do if tests run slowly?
**A:** Use оптимизированные team:
```bash
# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# Ограниченные потоки / Limited threads
uv run pytest tests/ -n 2

# Конкретные тесты / specific tests
uv run pytest tests/calculation/ -v
```

### Q: Как получить помощь? / How to get help?
**A:** Use доступные ресурсы:
- **documentation / Documentation**: [docs/run-and-test-guides/](.)
- **GitHub Issues**: https://github.com/Username/neozork-hld-Prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

## 📚 Дополнительные ресурсы / Additional Resources

- [Complete guide / Complete Manual](russian/complete-manual-ru.md)
- [Quick start / Quick start](russian/quick-start-ru.md)
- [guide on testing / testing Guide](russian/testing-guide-ru.md)
- [guide on deployment / deployment Guide](russian/deployment-guide-ru.md)
- [Troubleshooting / Troubleshooting](Troubleshooting.md)
