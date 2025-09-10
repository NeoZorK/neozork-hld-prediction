# Руководства по запуску и тестированию / Run and Test Guides

## 📁 Структура / Structure

```
docs/run-and-test-guides/
├── index.md                           # Главная страница / Main page
├── project-structure.md              # Структура проекта / Project structure
├── troubleshooting.md                # Устранение неполадок / Troubleshooting
├── faq.md                           # Часто задаваемые вопросы / FAQ
├── russian/                         # Русская версия / Russian version
│   ├── complete-manual-ru.md        # Полное руководство / Complete manual
│   ├── quick-start-ru.md            # Быстрый старт / Quick start
│   ├── testing-guide-ru.md          # Руководство по тестированию / Testing guide
│   └── deployment-guide-ru.md       # Руководство по развертыванию / Deployment guide
└── english/                         # Английская версия / English version
    ├── complete-manual-en.md        # Complete manual
    ├── quick-start-en.md            # Quick start
    ├── testing-guide-en.md          # Testing guide
    └── deployment-guide-en.md       # Deployment guide
```

## 🚀 Быстрый доступ / Quick Access

### Русская версия / Russian Version
- [Полное руководство](russian/complete-manual-ru.md) - Подробное руководство по всем компонентам
- [Быстрый старт](russian/quick-start-ru.md) - Запуск за 5 минут
- [Руководство по тестированию](russian/testing-guide-ru.md) - Все о тестировании
- [Руководство по развертыванию](russian/deployment-guide-ru.md) - Развертывание в продакшне

### English Version
- [Complete Manual](english/complete-manual-en.md) - Comprehensive guide for all components
- [Quick Start](english/quick-start-en.md) - Get running in 5 minutes
- [Testing Guide](english/testing-guide-en.md) - Everything about testing
- [Deployment Guide](english/deployment-guide-en.md) - Production deployment

## 📋 Компоненты системы / System Components

### Основные компоненты / Main Components
1. **Основной анализ** (`run_analysis.py`) - Ручное построение графиков / Manual charting
2. **Интерактивная система** (`interactive/`) - ML торговые стратегии / ML trading strategies
3. **SaaS платформа** (`src/saas/`) - Облачная платформа / Cloud platform
4. **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Хедж-фонд / Hedge fund
5. **Мобильное приложение** (`src/mobile_app/`) - React Native приложение / React Native app
6. **Админ панель** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel
7. **Мониторинг** (`src/monitoring/`) - Система мониторинга / Monitoring system

### Тестирование / Testing
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

### Запуск / Launch
```bash
# Основной анализ / Main analysis
uv run run_analysis.py demo --rule PHLD

# Интерактивная система / Interactive system
uv run python interactive/neozork.py

# SaaS платформа / SaaS platform
uv run python run_saas.py

# Pocket Hedge Fund
uv run python run_pocket_hedge_fund.py
```

### Тестирование / Testing
```bash
# Все тесты / All tests
uv run pytest tests -n auto

# Безопасный режим / Safe mode
./scripts/run_tests_safe.sh

# С покрытием / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Docker / Docker
```bash
# Запуск сервисов / Launch services
docker-compose up -d

# Остановка / Stop
docker-compose down

# Тесты в Docker / Tests in Docker
docker-compose exec neozork-hld uv run pytest tests/ -n auto
```

## 🆘 Поддержка / Support

### Устранение неполадок / Troubleshooting
- [Устранение неполадок](troubleshooting.md) - Частые проблемы и решения
- [FAQ](faq.md) - Часто задаваемые вопросы

### Дополнительные ресурсы / Additional Resources
- [Структура проекта](project-structure.md) - Подробная структура проекта
- [Основная документация](../index.md) - Главная страница документации

---

**Версия / Version**: 1.0.0  
**Последнее обновление / Last Updated**: $(date)  
**Автор / Author**: NeoZork Development Team
