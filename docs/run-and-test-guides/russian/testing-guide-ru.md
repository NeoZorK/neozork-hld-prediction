# Руководство по тестированию - NeoZork HLD Prediction

## 🧪 Обзор тестирования

Система NeoZork HLD Prediction включает в себя комплексную систему тестирования с поддержкой:
- Многопоточного тестирования
- Автоматического определения окружения
- Покрытия кода
- Специализированных тестов

## 🚀 Быстрый старт тестирования

### Запуск всех тестов
```bash
# Все тесты (многопоточные)
uv run pytest tests -n auto

# Безопасный режим
./scripts/run_tests_safe.sh

# Автоматическое определение окружения
./scripts/run_all_tests.sh
```

### Тестирование с покрытием
```bash
# Покрытие кода
uv run pytest tests/ --cov=src -n auto

# HTML отчет
uv run pytest tests/ --cov=src --cov-report=html -n auto
```

## 📋 Категории тестов

### Основные тесты
```bash
# Тесты расчетов
uv run pytest tests/calculation/ -n auto -v

# Тесты CLI
uv run pytest tests/cli/ -n auto -v

# Тесты данных
uv run pytest tests/data/ -n auto -v

# Тесты EDA
uv run pytest tests/eda/ -n auto -v
```

### Тесты компонентов
```bash
# Тесты SaaS
uv run pytest tests/saas/ -n auto -v

# Тесты Pocket Hedge Fund
uv run pytest tests/pocket_hedge_fund/ -n auto -v

# Тесты интерактивной системы
uv run pytest tests/interactive/ -n auto -v

# Тесты мониторинга
uv run pytest tests/monitoring/ -n auto -v
```

### Тесты развертывания
```bash
# Тесты Docker
uv run pytest tests/docker/ -n auto -v

# Тесты нативного контейнера
uv run pytest tests/native-container/ -n auto -v

# Тесты интеграции
uv run pytest tests/integration/ -n auto -v
```

## 🔧 Специализированное тестирование

### Тесты производительности
```bash
# Тесты производительности
uv run pytest tests/ -m performance -n auto

# Тесты с профилированием
uv run pytest tests/ --profile -n auto
```

### Тесты безопасности
```bash
# Тесты безопасности
uv run pytest tests/ -m security -n auto

# Тесты аутентификации
uv run pytest tests/pocket_hedge_fund/test_auth_system.py -v
```

### Тесты API
```bash
# Тесты API endpoints
uv run pytest tests/pocket_hedge_fund/test_api_endpoints.py -v

# Тесты SaaS API
uv run pytest tests/saas/ -v
```

## 🐳 Тестирование в Docker

### Тесты в Docker контейнере
```bash
# Тесты в основном контейнере
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Тесты конкретной категории
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v

# Тесты с покрытием
docker-compose exec neozork-hld uv run pytest tests/ --cov=src -n auto
```

### Тесты нативного контейнера
```bash
# Вход в контейнер
./scripts/native-container/exec.sh --shell

# Внутри контейнера:
uv run pytest tests/ -n auto
uv run pytest tests/calculation/ -v
uv run pytest tests/ --cov=src -n auto
```

## 📊 Анализ результатов

### Просмотр результатов
```bash
# HTML отчет покрытия
open htmlcov/index.html

# XML отчет
cat coverage.xml

# Текстовый отчет
uv run pytest tests/ --cov=src --cov-report=term-missing -n auto
```

### Анализ производительности
```bash
# Профилирование тестов
uv run pytest tests/ --profile --profile-svg

# Анализ времени выполнения
uv run pytest tests/ --durations=10
```

## 🛠️ Отладка тестов

### Запуск с отладкой
```bash
# Подробный вывод
uv run pytest tests/ -v -s

# Остановка на первой ошибке
uv run pytest tests/ -x

# Запуск конкретного теста
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

### Отладочные скрипты
```bash
# Отладка тестов
python scripts/debug/debug_test_issues.py

# Анализ покрытия
python scripts/analysis/generate_test_coverage.py

# Управление результатами тестов
python scripts/analysis/manage_test_results.py
```

## 📚 Дополнительные ресурсы

- [Полное руководство](complete-manual-ru.md)
- [Быстрый старт](quick-start-ru.md)
- [Руководство по развертыванию](deployment-guide-ru.md)
