# Run and Test Guides / Run and Test Guides

## 📁 Структура / Structure

```
docs/run-and-test-guides/
├── index.md # Main page / Main page
├── project-structure.md # Project Structure / Project Structure
├── Troubleshooting.md # Troubleshooting / Troubleshooting
├── faq.md # Frequently Asked Questions / FAQ
├── russian/ # Russian Version / Russian Version
│ ├── complete-manual-ru.md # Complete guide / Complete manual
│ ├── quick-start-ru.md # quick start / Quick start
│ ├── testing-guide-ru.md # guide on testing / testing guide
│ └── deployment-guide-ru.md # guide on deployment / Deployment guide
└── english/ # English Version / English Version
 ├── complete-manual-en.md # Complete manual
 ├── quick-start-en.md # Quick start
 ├── testing-guide-en.md # testing guide
 └── deployment-guide-en.md # Deployment guide
```

## 🚀 Быстрый доступ / Quick Access

### Russian Version / Russian Version
- [Complete guide](russian/complete-manual-ru.md) - Подробное guide on всем компонентам
- [quick start](russian/quick-start-ru.md) - Launch за 5 minutes
- [guide on testing](russian/testing-guide-ru.md) - Все о тестировании
- [guide on deployment](russian/deployment-guide-ru.md) - Развертывание in продакшне

### English Version
- [Complete Manual](english/complete-manual-en.md) - Comprehensive guide for all components
- [Quick start](english/quick-start-en.md) - Get running in 5 minutes
- [testing Guide](english/testing-guide-en.md) - Everything about testing
- [Deployment Guide](english/deployment-guide-en.md) - Production deployment

## 📋 Компоненты системы / System Components

### Основные компоненты / Main Components
1. **Основной анализ** (`run_analysis.py`) - Ручное построение графиков / Manual charting
2. **Интерактивная система** (`interactive/`) - ML торговые стратегии / ML trading strategies
3. **SaaS platform** (`src/saas/`) - Облачная platform / Cloud platform
4. **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
5. **Mobile application** (`src/mobile_app/`) - React Native application / React Native app
6. **Админ панель** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel
7. **Monitoring** (`src/monitoring/`) - Система Monitoringа / Monitoring system

### Тестирование / testing
- **Многопоточное тестирование** / Multithreaded testing
- **Автоматическое определение окружения** / Automatic environment detection
- **Покрытие кода** / Code coverage
- **Специализированные тесты** / Specialized tests

### Развертывание / Deployment
- **Локальное развертывание** / Local deployment
- **Docker контейнеры** / Docker containers
- **Apple Silicon нативные контейнеры** / Apple Silicon native containers
- **Kubernetes кластеры** / Kubernetes clusters
- **Продакшн развертывание** / Production deployment

## 🛠️ Полезные команды / Useful Commands

### Launch / Launch
```bash
# Основной анализ / Main analysis
uv run run_analysis.py demo --rule PHLD

# Интерактивная система / Interactive system
uv run python interactive/neozork.py

# SaaS platform / SaaS platform
uv run python run_saas.py

# Pocket Hedge Fund
uv run python run_pocket_hedge_fund.py
```

### Тестирование / testing
```bash
# Все тесты / All tests
uv run pytest tests -n auto

# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with coverage / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Docker / Docker
```bash
# Launch сервисов / Launch services
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
- [Project Structure](project-structure.md) - Подробная Project Structure
- [Основная documentation](../index.md) - Main page документации

---

**Версия / Version**: 1.0.0
**Последнее update / Last Updated**: $(date)
**Автор / Author**: NeoZork Development Team
