# Быстрый старт - NeoZork HLD Prediction

## 🚀 Запуск за 5 минут

### 1. Установка зависимостей
```bash
# Установка UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Установка Python зависимостей
uv pip install -r requirements.txt

# Установка Node.js зависимостей
cd src/mobile_app && npm install && cd ..
cd src/admin_panel && npm install && cd ../..
```

### 2. Запуск основных компонентов

#### Основной анализ
```bash
# Демо анализ
uv run run_analysis.py demo --rule PHLD

# Анализ с реальными данными
uv run run_analysis.py yfinance AAPL --rule RSI
```

#### Интерактивная система
```bash
# Запуск интерактивной системы
uv run python src/interactive/neozork.py
```

#### SaaS платформа
```bash
# Запуск SaaS
uv run python run_saas.py
# Доступ: http://localhost:8080
```

#### Pocket Hedge Fund
```bash
# Запуск хедж-фонда
uv run python run_pocket_hedge_fund.py
# Доступ: http://localhost:8080
```

#### Мобильное приложение
```bash
cd src/mobile_app
npm start
```

#### Админ панель
```bash
cd src/admin_panel
npm run dev
# Доступ: http://localhost:3000
```

### 3. Тестирование
```bash
# Все тесты
uv run pytest tests -n auto

# Безопасный режим
./scripts/run_tests_safe.sh
```

### 4. Docker (опционально)
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down
```

## 🔧 Полезные команды

### Проверка статуса
```bash
# Проверка UV
python scripts/utilities/check_uv_mode.py --verbose

# Проверка MCP
python scripts/check_mcp_status.py

# Проверка Docker
docker-compose ps
```

### Очистка
```bash
# Очистка кэша UV
uv cache clean

# Очистка Docker
docker system prune -a
```

## 🆘 Решение проблем

### Частые проблемы
1. **Ошибки импорта**: `export PYTHONPATH="${PWD}:${PYTHONPATH}"`
2. **Проблемы с UV**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **Проблемы с Docker**: `docker-compose build --no-cache`
4. **Проблемы с тестами**: `./scripts/run_tests_safe.sh`

### Получение помощи
```bash
# Справка по основному скрипту
./nz --help

# Справка по анализу
uv run run_analysis.py --help
```

---

**Полное руководство**: [complete-manual-ru.md](complete-manual-ru.md)
