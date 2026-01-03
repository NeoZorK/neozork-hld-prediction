# Run and Test Guides / Run and Test Guides

## 📁 Structure / Structure

```
docs/run-and-test-guides/
├── index.md # main page / main page
├── project-Structure.md # Project Structure / Project Structure
├── Troubleshooting.md # Troubleshooting / Troubleshooting
├── faq.md # Frequently Asked Questions / FAQ
├── russian/ # Russian Version / Russian Version
│ ├── complete-manual-ru.md # Complete guide / Complete manual
│ ├── quick-start-ru.md # Quick start / Quick start
│ ├── testing-guide-ru.md # guide on testing / testing guide
│ └── deployment-guide-ru.md # guide on deployment / deployment guide
└── english/ # English Version / English Version
 ├── complete-manual-en.md # Complete manual
 ├── quick-start-en.md # Quick start
 ├── testing-guide-en.md # testing guide
 └── deployment-guide-en.md # deployment guide
```

## 🚀 Быстрый доступ / Quick Access

### Russian Version / Russian Version
- [Complete guide](russian/complete-manual-ru.md) - Detailed guide on all components
- [Quick start](russian/quick-start-ru.md) - Launch за 5 minutes
- [guide on testing](russian/testing-guide-ru.md) - Все о тестировании
- [guide on deployment](russian/deployment-guide-ru.md) - Развертывание in продакшне

### English Version
- [Complete Manual](english/complete-manual-en.md) - Comprehensive guide for all components
- [Quick start](english/quick-start-en.md) - Get running in 5 minutes
- [testing Guide](english/testing-guide-en.md) - Everything about testing
- [deployment Guide](english/deployment-guide-en.md) - Production deployment

## 📋 components системы / system components

### Основные components / main components
1. **Основной анализ** (`run_Analysis.py`) - Ручное построение графиков / Manual charting
2. **Интерактивная система** (`interactive/`) - ML торговые стратегии / ML trading strategies
3. **SaaS platform** (`src/saas/`) - Облачная platform / Cloud platform
4. **Pocket Hedge fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
5. **mobile application** (`src/mobile_app/`) - React Native application / React Native app
6. **Админ панель** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel
7. **Monitoring** (`src/Monitoring/`) - Система Monitoringа / Monitoring system

### Тестирование / testing
- **Многопоточное тестирование** / Multithreaded testing
- **Автоматическое определение окружения** / Automatic environment detection
- **Покрытие кода** / Code coverage
- **Специализированные тесты** / Specialized tests

### Развертывание / deployment
- **Локальное развертывание** / Local deployment
- **Docker контейнеры** / Docker containers
- **Apple Silicon нативные контейнеры** / Apple Silicon native containers
- **Kubernetes кластеры** / Kubernetes clusters
- **Продакшн развертывание** / Production deployment

## 🛠️ Полезные team / Useful Commands

### Launch / Launch
```bash
# Основной анализ / main Analysis
uv run run_Analysis.py demo --rule PHLD

# Интерактивная система / Interactive system
uv run python interactive/neozork.py

# SaaS platform / SaaS platform
uv run python run_saas.py

# Pocket Hedge fund
uv run python run_pocket_hedge_fund.py
```

### Тестирование / testing
```bash
# Все тесты / all tests
uv run pytest tests -n auto

# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with coverage / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Docker / Docker
```bash
# Launch сервисов / Launch Services
docker-compose up -d

# Остановка / Stop
docker-compose down

# Тесты in Docker / Tests in Docker
docker-compose exec neozork-hld uv run pytest tests/ -n auto
```

## 🆘 Поддержка / Support

### Troubleshooting / Troubleshooting
- [Troubleshooting](Troubleshooting.md) - Common Issues and решения
- [FAQ](faq.md) - Frequently Asked Questions

### Дополнительные ресурсы / Additional Resources
- [Project Structure](project-Structure.md) - Подробная Project Structure
- [Основная documentation](../index.md) - main page документации

---

**Версия / Version**: 1.0.0
**Последнее update / Last Updated**: $(date)
**Автор / Author**: NeoZork Development team
