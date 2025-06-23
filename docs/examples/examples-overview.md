# Examples Overview

Обзор всех примеров использования проекта Neozork HLD Prediction.

## 📚 Каталог примеров

### 🚀 Быстрый старт
- **[Quick Examples](quick-examples.md)** - Быстрые примеры для начала работы
  - Установка и настройка
  - Первые шаги
  - Базовый анализ данных
  - Интерактивный режим

### 📊 Основные примеры
- **[Usage Examples](usage-examples.md)** - Полные примеры использования
  - Комплексные рабочие процессы
  - Продвинутые сценарии
  - Интеграция компонентов
  - Оптимизация производительности

### 🎯 Специализированные примеры
- **[Indicator Examples](indicator-examples.md)** - Примеры использования индикаторов
  - Все категории индикаторов
  - Комбинирование индикаторов
  - Экспорт результатов
  - Различные бэкенды для графиков

- **[MCP Examples](mcp-examples.md)** - Примеры использования MCP серверов
  - Автозапуск MCP серверов
  - Интеграция с GitHub Copilot
  - Паттерны использования
  - Отладка и мониторинг

- **[Testing Examples](testing-examples.md)** - Примеры тестирования
  - Запуск тестов
  - Анализ покрытия
  - Отладка тестов
  - Непрерывная интеграция

- **[Script Examples](script-examples.md)** - Примеры использования скриптов
  - Утилитарные скрипты
  - Отладочные скрипты
  - Автоматизация
  - Рабочие процессы

- **[Docker Examples](docker-examples.md)** - Примеры использования Docker
  - Развертывание в контейнерах
  - Разработка в Docker
  - Масштабирование
  - Отладка контейнеров

- **[EDA Examples](eda-examples.md)** - Примеры Exploratory Data Analysis
  - Базовый статистический анализ
  - Корреляционный анализ
  - Визуализация данных
  - Анализ качества данных

## 🎯 Рекомендации по использованию

### Для новичков
1. Начните с **[Quick Examples](quick-examples.md)**
2. Изучите **[Getting Started](getting-started.md)**
3. Попробуйте интерактивный режим
4. Изучите **[Indicator Examples](indicator-examples.md)**

### Для разработчиков
1. Изучите **[Testing Examples](testing-examples.md)**
2. Настройте **[MCP Examples](mcp-examples.md)**
3. Используйте **[Script Examples](script-examples.md)**
4. Рассмотрите **[Docker Examples](docker-examples.md)**

### Для аналитиков
1. Изучите **[Usage Examples](usage-examples.md)**
2. Освойте **[Indicator Examples](indicator-examples.md)**
3. Используйте **[EDA Examples](eda-examples.md)**
4. Настройте автоматизацию через скрипты
5. Рассмотрите Docker для воспроизводимости

### Для DevOps
1. Изучите **[Docker Examples](docker-examples.md)**
2. Настройте **[Testing Examples](testing-examples.md)**
3. Автоматизируйте через **[Script Examples](script-examples.md)**
4. Интегрируйте MCP серверы

### Для исследователей данных
1. Изучите **[EDA Examples](eda-examples.md)**
2. Освойте **[Indicator Examples](indicator-examples.md)**
3. Используйте **[Usage Examples](usage-examples.md)**
4. Рассмотрите **[Docker Examples](docker-examples.md)** для воспроизводимости

## 🔄 Рабочие процессы

### Полный пайплайн анализа
```bash
# 1. Быстрый старт
python run_analysis.py demo --rule RSI

# 2. Загрузка реальных данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 3. EDA анализ
bash eda
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# 4. Анализ с индикаторами
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet

# 5. Просмотр результатов
python run_analysis.py show ind parquet

# 6. Тестирование
python -m pytest tests/ --cov=src --cov-report=html

# 7. Анализ покрытия
python tests/zzz_analyze_test_coverage.py
```

### Разработка с MCP
```bash
# 1. Запуск MCP серверов
python scripts/auto_start_mcp.py

# 2. Тестирование MCP
python tests/test_stdio.py

# 3. Разработка с AI помощью
# Используйте GitHub Copilot в IDE

# 4. Исправление импортов
python scripts/fix_imports.py

# 5. Запуск тестов
python -m pytest tests/ -v
```

### EDA пайплайн
```bash
# 1. Загрузка данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Базовый EDA
bash eda
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# 3. Анализ качества данных
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# 4. Корреляционный анализ
python -c "from src.eda.correlation_analysis import analyze_correlations; analyze_correlations()"

# 5. Визуализация
python -c "from src.eda.visualization import create_comprehensive_plots; create_comprehensive_plots()"

# 6. Экспорт результатов
python -c "from src.eda.export import export_to_csv; export_to_csv('eda_results.csv')"
```

### Docker развертывание
```bash
# 1. Сборка контейнера
docker compose build

# 2. Запуск анализа
docker compose run --rm neozork-hld python run_analysis.py demo

# 3. EDA в контейнере
docker compose run --rm neozork-hld bash eda

# 4. Тестирование в контейнере
docker compose run --rm neozork-hld python -m pytest tests/

# 5. MCP серверы в контейнере
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py
```

## 📊 Категории примеров

### Анализ данных
- **Демо данные**: Быстрое тестирование
- **Yahoo Finance**: Акции и форекс
- **Binance**: Криптовалюты
- **CSV файлы**: Пользовательские данные
- **Exchange Rate API**: Реальные курсы валют

### Технические индикаторы
- **Трендовые**: EMA, ADX, SAR
- **Осцилляторы**: RSI, Stochastic, CCI
- **Моментум**: MACD, Stochastic
- **Волатильность**: ATR, Bollinger Bands, Standard Deviation
- **Объемные**: OBV, VWAP
- **Поддержка/Сопротивление**: Donchian, Fibonacci, Pivot Points
- **Предиктивные**: HMA, Time Series Forecast
- **Вероятностные**: Kelly Criterion, Monte Carlo
- **Сентимент**: COT, Fear & Greed, Social Sentiment

### Экспорт и визуализация
- **Форматы**: Parquet, CSV, JSON
- **Бэкенды**: Plotly, Seaborn, Matplotlib, Terminal
- **Оптимизация**: Fastest, Term для SSH/Docker

### EDA (Exploratory Data Analysis)
- **Базовый анализ**: Статистика, распределения
- **Корреляционный анализ**: Матрицы корреляций
- **Временной анализ**: Тренды, сезонность
- **Качество данных**: Пропущенные значения, выбросы
- **Визуализация**: Графики, диаграммы, интерактивные графики

### Тестирование
- **Модульные тесты**: Отдельные компоненты
- **Интеграционные тесты**: Взаимодействие компонентов
- **Покрытие кода**: Анализ покрытия тестами
- **Производительность**: Бенчмаркинг
- **Граничные случаи**: Обработка ошибок

### MCP серверы
- **Автозапуск**: Автоматическое управление
- **GitHub Copilot**: AI помощь в разработке
- **Тестирование**: Проверка функциональности
- **Мониторинг**: Отслеживание состояния

### Скрипты
- **Утилитарные**: Исправление импортов, анализ зависимостей
- **Отладочные**: Диагностика проблем
- **Автоматизация**: Рабочие процессы
- **Мониторинг**: Логи и метрики

### Docker
- **Развертывание**: Контейнеризация
- **Разработка**: Hot reload, отладка
- **Масштабирование**: Множественные экземпляры
- **Мониторинг**: Логи, метрики, ресурсы

## 🎯 Сценарии использования

### Исследовательский анализ
```bash
# Интерактивный режим для исследования
python run_analysis.py interactive

# EDA анализ
bash eda
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# Быстрое тестирование индикаторов
python run_analysis.py demo --rule RSI -d plotly
python run_analysis.py demo --rule MACD -d plotly
python run_analysis.py demo --rule BB -d plotly
```

### Производственный анализ
```bash
# Загрузка и анализ реальных данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# EDA анализ
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# Анализ с индикаторами
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet
```

### Разработка новых индикаторов
```bash
# Создание тестовых данных
python scripts/create_test_parquet.py

# EDA анализ данных
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# Разработка с MCP помощью
python scripts/auto_start_mcp.py

# Тестирование
python -m pytest tests/calculation/indicators/ -v
```

### CI/CD пайплайн
```bash
# Запуск тестов
python -m pytest tests/ --cov=src --cov-report=xml

# Анализ покрытия
python tests/zzz_analyze_test_coverage.py

# EDA проверка данных
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# Сборка Docker образа
docker compose build
```

## 💡 Советы по использованию

### Выбор примеров
- **Новички**: Начните с Quick Examples
- **Разработчики**: Изучите Testing и MCP Examples
- **Аналитики**: Сосредоточьтесь на Usage, Indicator и EDA Examples
- **DevOps**: Используйте Docker и Script Examples
- **Исследователи данных**: Изучите EDA Examples

### Оптимизация
- Используйте fastest бэкенд для больших данных
- Применяйте term бэкенд для SSH/Docker
- Монтируйте volumes в Docker для данных
- Используйте кэширование для повторных запросов
- Применяйте EDA для понимания данных

### Отладка
- Запускайте отладочные скрипты при проблемах
- Проверяйте логи MCP серверов
- Используйте тесты для валидации
- Анализируйте покрытие кода
- Применяйте EDA для диагностики проблем с данными

---

📚 **Дополнительные ресурсы:**
- **[Полная документация](index.md)** - Обзор всей документации
- **[Руководство по началу работы](getting-started.md)** - Установка и настройка
- **[Структура проекта](project-structure.md)** - Организация кода
- **[Руководство по тестированию](testing.md)** - Подробное руководство по тестированию 