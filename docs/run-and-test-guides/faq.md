# Часто задаваемые вопросы / Frequently Asked Questions

## 🚀 Общие вопросы / General Questions

### Q: Как быстро запустить систему? / How to quickly launch the system?
**A:** Используйте быстрый старт:
```bash
# Установка зависимостей / Install dependencies
uv pip install -r requirements.txt

# Запуск основного анализа / Launch main analysis
uv run run_analysis.py demo --rule PHLD

# Запуск всех тестов / Run all tests
uv run pytest tests -n auto
```

### Q: Какие компоненты входят в систему? / What components are included in the system?
**A:** Система включает:
- **Основной анализ** (`run_analysis.py`) - Ручное построение графиков / Manual charting
- **Интерактивная система** (`interactive/`) - ML торговые стратегии / ML trading strategies
- **SaaS платформа** (`src/saas/`) - Облачная платформа / Cloud platform
- **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Хедж-фонд / Hedge fund
- **Мобильное приложение** (`mobile_app/`) - React Native приложение / React Native app
- **Админ панель** (`admin_panel/`) - Vue.js админка / Vue.js admin panel
- **Мониторинг** (`src/monitoring/`) - Система мониторинга / Monitoring system

### Q: Какие требования к системе? / What are the system requirements?
**A:** Минимальные требования:
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 20.10+ (опционально / optional)
- **UV**: Последняя версия / Latest version
- **Память / Memory**: 4GB RAM
- **Диск / Disk**: 10GB свободного места / free space

## 🧪 Вопросы по тестированию / Testing Questions

### Q: Как запустить все тесты? / How to run all tests?
**A:** Используйте многопоточное тестирование:
```bash
# Все тесты / All tests
uv run pytest tests -n auto

# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# С покрытием / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Q: Как запустить тесты конкретного компонента? / How to run tests for specific component?
**A:** Запустите тесты по категориям:
```bash
# Тесты расчетов / Calculation tests
uv run pytest tests/calculation/ -n auto

# Тесты SaaS / SaaS tests
uv run pytest tests/saas/ -n auto

# Тесты Pocket Hedge Fund / Pocket Hedge Fund tests
uv run pytest tests/pocket_hedge_fund/ -n auto
```

### Q: Что делать, если тесты не запускаются? / What to do if tests don't run?
**A:** Попробуйте безопасный режим:
```bash
# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# С отладкой / With debugging
uv run pytest tests/ -v -s

# Конкретный тест / Specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

## 🐳 Вопросы по Docker / Docker Questions

### Q: Как запустить систему в Docker? / How to run system in Docker?
**A:** Используйте Docker Compose:
```bash
# Запуск всех сервисов / Launch all services
docker-compose up -d

# Запуск с логированием / Launch with logging
docker-compose up

# Остановка / Stop
docker-compose down
```

### Q: Как запустить тесты в Docker? / How to run tests in Docker?
**A:** Выполните команды в контейнере:
```bash
# Тесты в контейнере / Tests in container
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Конкретные тесты / Specific tests
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v
```

### Q: Что делать, если Docker не запускается? / What to do if Docker doesn't start?
**A:** Попробуйте пересборку:
```bash
# Пересборка контейнеров / Rebuild containers
docker-compose build --no-cache

# Очистка Docker / Clean Docker
docker system prune -a

# Перезапуск Docker / Restart Docker
sudo systemctl restart docker
```

## 🍎 Вопросы по Apple Silicon / Apple Silicon Questions

### Q: Как запустить нативный контейнер? / How to run native container?
**A:** Используйте скрипты нативного контейнера:
```bash
# Интерактивный запуск / Interactive launch
./scripts/native-container/native-container.sh

# Быстрый запуск / Quick launch
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Проверка статуса / Check status
./scripts/native-container/run.sh --status
```

### Q: Как управлять нативным контейнером? / How to manage native container?
**A:** Используйте команды управления:
```bash
# Остановка / Stop
./scripts/native-container/stop.sh

# Перезапуск / Restart
./scripts/native-container/force_restart.sh

# Очистка / Cleanup
./scripts/native-container/cleanup.sh --all --force
```

## 🚀 Вопросы по развертыванию / Deployment Questions

### Q: Как развернуть систему в продакшне? / How to deploy system in production?
**A:** Используйте продакшн конфигурацию:
```bash
# Настройка продакшна / Setup production
python deploy/production_setup.py

# Запуск продакшн сервисов / Launch production services
docker-compose -f docker-compose.prod.yml up -d
```

### Q: Как развернуть в Kubernetes? / How to deploy in Kubernetes?
**A:** Примените манифесты:
```bash
# Применение манифестов / Apply manifests
kubectl apply -f k8s/

# Проверка статуса / Check status
kubectl get pods
kubectl get services
```

## 🔧 Вопросы по настройке / Configuration Questions

### Q: Как настроить переменные окружения? / How to configure environment variables?
**A:** Отредактируйте файл .env:
```bash
# Копирование примера / Copy example
cp env.example .env

# Редактирование / Edit
nano .env
```

### Q: Как настроить базу данных? / How to configure database?
**A:** Установите PostgreSQL и настройте переменные:
```bash
# Установка PostgreSQL / Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Создание базы данных / Create database
createdb neozork_fund

# Настройка пользователя / Configure user
createuser neozork_user
```

## 📊 Вопросы по мониторингу / Monitoring Questions

### Q: Как просмотреть логи? / How to view logs?
**A:** Используйте команды просмотра логов:
```bash
# Логи приложения / Application logs
tail -f logs/pocket_hedge_fund.log

# Docker логи / Docker logs
docker-compose logs -f neozork-hld

# Все логи / All logs
tail -f logs/*.log
```

### Q: Как проверить статус системы? / How to check system status?
**A:** Используйте команды проверки:
```bash
# Health check / Проверка здоровья
curl http://localhost:8080/health

# Prometheus метрики / Prometheus metrics
curl http://localhost:9090/metrics

# Статус Docker / Docker status
docker-compose ps
```

## 🆘 Вопросы по устранению неполадок / Troubleshooting Questions

### Q: Что делать, если возникают ошибки импорта? / What to do if import errors occur?
**A:** Проверьте PYTHONPATH:
```bash
# Установка PYTHONPATH / Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Проверка установки / Check installation
uv pip list | grep neozork
```

### Q: Что делать, если тесты медленно работают? / What to do if tests run slowly?
**A:** Используйте оптимизированные команды:
```bash
# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# Ограниченные потоки / Limited threads
uv run pytest tests/ -n 2

# Конкретные тесты / Specific tests
uv run pytest tests/calculation/ -v
```

### Q: Как получить помощь? / How to get help?
**A:** Используйте доступные ресурсы:
- **Документация / Documentation**: [docs/run-and-test-guides/](.)
- **GitHub Issues**: https://github.com/username/neozork-hld-prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

## 📚 Дополнительные ресурсы / Additional Resources

- [Полное руководство / Complete Manual](russian/complete-manual-ru.md)
- [Быстрый старт / Quick Start](russian/quick-start-ru.md)
- [Руководство по тестированию / Testing Guide](russian/testing-guide-ru.md)
- [Руководство по развертыванию / Deployment Guide](russian/deployment-guide-ru.md)
- [Устранение неполадок / Troubleshooting](troubleshooting.md)
