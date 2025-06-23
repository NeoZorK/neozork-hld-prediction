# Quick Examples

Быстрые примеры использования для начала работы с проектом.

## 🚀 Быстрый старт

### Установка и настройка
```bash
# Клонирование и установка
git clone <repository>
cd neozork-hld-prediction
pip install uv && uv sync

# Проверка установки
python run_analysis.py --version
```

### Первые шаги
```bash
# Демо-режим
python run_analysis.py demo

# Интерактивный режим
python run_analysis.py interactive

# Просмотр всех примеров
python run_analysis.py --examples
```

## 📊 Анализ данных

### Демо-данные
```bash
# Базовый демо
python run_analysis.py demo

# С конкретным индикатором
python run_analysis.py demo --rule RSI
python run_analysis.py demo --rule MACD
python run_analysis.py demo --rule EMA

# С разными бэкендами для графиков
python run_analysis.py demo -d plotly
python run_analysis.py demo -d seaborn
python run_analysis.py demo -d term
```

### Реальные данные
```bash
# Yahoo Finance
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# Binance (криптовалюты)
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule MACD

# CSV файлы
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule EMA

# Exchange Rate API (форекс)
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule BB
```

## 🔍 Исследование индикаторов

### Просмотр доступных индикаторов
```bash
# Все индикаторы
python run_analysis.py --indicators

# По категориям
python run_analysis.py --indicators oscillators
python run_analysis.py --indicators trend
python run_analysis.py --indicators momentum

# Детальная информация
python run_analysis.py --indicators oscillators rsi
python run_analysis.py --indicators momentum macd
```

### Использование индикаторов
```bash
# RSI (Relative Strength Index)
python run_analysis.py demo --rule RSI

# MACD (Moving Average Convergence Divergence)
python run_analysis.py demo --rule MACD

# EMA (Exponential Moving Average)
python run_analysis.py demo --rule EMA

# Bollinger Bands
python run_analysis.py demo --rule BB

# ATR (Average True Range)
python run_analysis.py demo --rule ATR

# Stochastic Oscillator
python run_analysis.py demo --rule STOCH

# VWAP (Volume Weighted Average Price)
python run_analysis.py demo --rule VWAP
```

## 📁 Управление данными

### Просмотр кэшированных данных
```bash
# Все данные
python run_analysis.py show

# По источникам
python run_analysis.py show yf
python run_analysis.py show binance
python run_analysis.py show csv
python run_analysis.py show exrate

# Фильтрация по ключевым словам
python run_analysis.py show yf aapl
python run_analysis.py show binance btc
```

### Экспорт результатов
```bash
# Экспорт в разных форматах
python run_analysis.py demo --rule RSI --export-parquet
python run_analysis.py demo --rule RSI --export-csv
python run_analysis.py demo --rule RSI --export-json

# Все форматы сразу
python run_analysis.py demo --rule RSI --export-parquet --export-csv --export-json
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python -m pytest tests/

# Конкретные категории
python -m pytest tests/calculation/ -v
python -m pytest tests/cli/ -v
python -m pytest tests/data/ -v

# С покрытием
python -m pytest tests/ --cov=src --cov-report=html
```

### Анализ покрытия
```bash
# Анализ покрытия тестами
python tests/zzz_analyze_test_coverage.py
```

## 🔧 MCP серверы

### Автозапуск MCP серверов
```bash
# Запуск
python scripts/auto_start_mcp.py

# Статус
python scripts/auto_start_mcp.py --status

# Остановка
python scripts/auto_start_mcp.py --stop
```

### Тестирование MCP
```bash
# Тест stdio режима
python tests/test_stdio.py

# Тест MCP функциональности
python -m pytest tests/mcp/ -v
```

## 🐳 Docker

### Использование Docker
```bash
# Запуск в контейнере
docker compose run --rm neozork-hld python run_analysis.py demo

# Интерактивная сессия
docker compose run --rm neozork-hld bash

# С UV
uv run ./nz demo
```

## 🔍 Отладка

### Утилиты отладки
```bash
# Отладка Binance соединения
python scripts/debug_scripts/debug_binance_connection.py

# Проверка parquet файлов
python scripts/debug_scripts/debug_check_parquet.py

# Отладка индикаторов
python scripts/debug_scripts/debug_indicators.py

# Отладка CLI
python scripts/debug_scripts/debug_cli.py
```

### Решение проблем
```bash
# Проблемы с зависимостями
pip install --upgrade -r requirements.txt
# или
uv sync

# Проблемы с кэшем
rm -rf data/cache/*
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --force-refresh

# Проблемы с правами
chmod +x scripts/*.sh
chmod +x nz
chmod +x eda

# Проблемы с Docker
docker compose down
docker compose build --no-cache
```

## 📈 Рабочие процессы

### Полный пайплайн анализа
```bash
# 1. Загрузка данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Анализ с разными индикаторами
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet
python run_analysis.py show yf AAPL --rule EMA --export-parquet

# 3. Просмотр результатов
python run_analysis.py show ind parquet
```

### Пакетная обработка
```bash
# Множественные символы
for symbol in AAPL MSFT GOOGL; do
    python run_analysis.py yf -t $symbol --period 1mo --point 0.01 --rule RSI
done

# Множественные таймфреймы
for timeframe in D1 H1 M15; do
    python run_analysis.py binance -t BTCUSDT --interval $timeframe --point 0.01 --rule MACD
done
```

## 🎯 Оптимизация производительности

### Быстрые бэкенды
```bash
# Самый быстрый бэкенд
python run_analysis.py demo -d fastest

# Терминальный бэкенд (для SSH/Docker)
python run_analysis.py demo -d term

# Эффективные правила
python run_analysis.py demo --rule OHLCV  # Только свечи
python run_analysis.py demo --rule AUTO   # Автоопределение
```

## 📚 Дополнительные ресурсы

- **[Полные примеры использования](usage-examples.md)** - Подробные примеры и рабочие процессы
- **[Руководство по началу работы](getting-started.md)** - Установка и базовая настройка
- **[Руководство по тестированию](testing.md)** - Запуск тестов и анализ покрытия
- **[Настройка MCP серверов](mcp-servers/SETUP.md)** - Интеграция с GitHub Copilot
- **[Документация по скриптам](scripts.md)** - Утилиты и скрипты отладки

---

💡 **Совет**: Используйте `python run_analysis.py --help` для получения справки по командам и `python run_analysis.py --examples` для просмотра всех примеров. 