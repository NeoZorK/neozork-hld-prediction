# Testing Examples

Примеры тестирования и анализа покрытия кода.

## 🧪 Быстрый старт тестирования

### Запуск всех тестов
```bash
# Все тесты
python -m pytest tests/

# С подробным выводом
python -m pytest tests/ -v

# С максимальной подробностью
python -m pytest tests/ -vvv

# С выводом print statements
python -m pytest tests/ -s
```

### Запуск конкретных категорий тестов
```bash
# Тесты расчетов
python -m pytest tests/calculation/ -v

# Тесты CLI
python -m pytest tests/cli/ -v

# Тесты данных
python -m pytest tests/data/ -v

# Тесты EDA
python -m pytest tests/eda/ -v

# Тесты экспорта
python -m pytest tests/export/ -v

# Тесты MCP серверов
python -m pytest tests/mcp/ -v

# Тесты скриптов
python -m pytest tests/scripts/ -v
```

## 📊 Анализ покрытия

### Базовый анализ покрытия
```bash
# Анализ покрытия с HTML отчетом
python -m pytest tests/ --cov=src --cov-report=html

# Анализ покрытия с терминальным отчетом
python -m pytest tests/ --cov=src --cov-report=term

# Анализ покрытия с пропущенными строками
python -m pytest tests/ --cov=src --cov-report=term-missing

# Анализ покрытия с ветками
python -m pytest tests/ --cov=src --cov-report=html --cov-branch
```

### Детальный анализ покрытия
```bash
# Анализ покрытия конкретных модулей
python -m pytest tests/ --cov=src.calculation --cov=src.cli --cov-report=html

# Анализ покрытия с исключениями
python -m pytest tests/ --cov=src --cov-report=html --cov-omit="*/tests/*,*/__pycache__/*"

# Анализ покрытия с минимальным порогом
python -m pytest tests/ --cov=src --cov-report=html --cov-fail-under=80
```

### Автоматический анализ покрытия
```bash
# Запуск анализа покрытия
python tests/zzz_analyze_test_coverage.py

# Анализ с подробным отчетом
python tests/zzz_analyze_test_coverage.py --verbose

# Анализ с экспортом в файл
python tests/zzz_analyze_test_coverage.py --output coverage_report.txt
```

## 🎯 Конкретные тесты

### Тест MCP сервера stdio режима
```bash
# Тест stdio режима
python tests/test_stdio.py

# Тест с подробным выводом
python tests/test_stdio.py -v

# Тест с отладкой
python tests/test_stdio.py --debug
```

### Тест CLI функциональности
```bash
# Тест примеров CLI
python -m pytest tests/cli/test_cli_examples.py -v

# Тест поиска индикаторов
python -m pytest tests/cli/test_indicators_search.py -v

# Тест интерактивного режима
python -m pytest tests/cli/test_interactive_mode.py -v

# Тест show режима
python -m pytest tests/cli/test_cli_show_mode.py -v
```

### Тест расчетов индикаторов
```bash
# Тест всех индикаторов
python -m pytest tests/calculation/indicators/ -v

# Тест конкретных категорий индикаторов
python -m pytest tests/calculation/indicators/oscillators/ -v
python -m pytest tests/calculation/indicators/trend/ -v
python -m pytest tests/calculation/indicators/momentum/ -v
python -m pytest tests/calculation/indicators/volatility/ -v
python -m pytest tests/calculation/indicators/volume/ -v

# Тест граничных случаев
python -m pytest tests/calculation/indicators/edge_cases/ -v

# Тест производительности
python -m pytest tests/calculation/indicators/performance/ -v

# Тест интеграции
python -m pytest tests/calculation/indicators/integration/ -v
```

### Тест загрузчиков данных
```bash
# Тест загрузчиков данных
python -m pytest tests/data/fetchers/ -v

# Тест конкретных загрузчиков
python -m pytest tests/data/fetchers/test_binance_fetcher.py -v
python -m pytest tests/data/fetchers/test_csv_fetcher.py -v
python -m pytest tests/data/fetchers/test_yfinance_fetcher.py -v
python -m pytest tests/data/fetchers/test_exrate_fetcher.py -v
```

### Тест экспорта
```bash
# Тест функциональности экспорта
python -m pytest tests/export/test_export_functionality.py -v
```

## 🔍 Отладка тестов

### Отладка с pdb
```bash
# Запуск теста с отладчиком
python -m pytest tests/test_stdio.py::test_stdio_mode -s --pdb

# Запуск теста с отладчиком при ошибке
python -m pytest tests/test_stdio.py -s --pdb

# Запуск теста с отладчиком при любом результате
python -m pytest tests/test_stdio.py -s --pdbcls=IPython.terminal.debugger:Pdb
```

### Отладка с подробным выводом
```bash
# Максимальная подробность
python -m pytest tests/ -vvv -s

# Показать локальные переменные при ошибке
python -m pytest tests/ -l

# Показать трассировку
python -m pytest tests/ --tb=long

# Показать короткую трассировку
python -m pytest tests/ --tb=short

# Показать только строку с ошибкой
python -m pytest tests/ --tb=line
```

### Отладка конкретных тестов
```bash
# Запуск конкретного теста
python -m pytest tests/test_stdio.py::test_stdio_mode -v

# Запуск тестов по паттерну
python -m pytest tests/ -k "test_stdio" -v

# Запуск тестов исключая паттерн
python -m pytest tests/ -k "not slow" -v
```

## ⚡ Параллельное тестирование

### Запуск тестов в параллели
```bash
# Автоматическое определение количества процессов
python -m pytest tests/ -n auto

# Конкретное количество процессов
python -m pytest tests/ -n 4

# Параллельное тестирование с покрытием
python -m pytest tests/ -n auto --cov=src --cov-report=html
```

## 🚨 Обработка ошибок

### Остановка при первой ошибке
```bash
# Остановка при первой ошибке
python -m pytest tests/ -x

# Остановка при первой ошибке с отладчиком
python -m pytest tests/ -x --pdb
```

### Повторный запуск неудачных тестов
```bash
# Повторный запуск неудачных тестов
python -m pytest tests/ --lf

# Повторный запуск с максимальным количеством попыток
python -m pytest tests/ --maxfail=3
```

## 📈 Метрики тестирования

### Время выполнения тестов
```bash
# Измерение времени выполнения
python -m pytest tests/ --durations=10

# Измерение времени с подробностями
python -m pytest tests/ --durations=0
```

### Статистика тестов
```bash
# Статистика тестов
python -m pytest tests/ --tb=no -q

# Статистика с покрытием
python -m pytest tests/ --cov=src --cov-report=term-missing -q
```

## 🔧 Настройка тестов

### Конфигурация pytest
```bash
# Запуск с конфигурацией
python -m pytest tests/ -c pytest.ini

# Запуск с маркерами
python -m pytest tests/ -m "not slow"

# Запуск с фильтрами
python -m pytest tests/ --ignore=tests/slow/
```

### Переменные окружения для тестов
```bash
# Установка переменных окружения
export TEST_MODE=1
export DEBUG=1
python -m pytest tests/

# Запуск с переменными окружения
TEST_MODE=1 DEBUG=1 python -m pytest tests/
```

## 🐳 Тестирование в Docker

### Запуск тестов в контейнере
```bash
# Запуск всех тестов в Docker
docker compose run --rm neozork-hld python -m pytest tests/

# Запуск тестов с покрытием в Docker
docker compose run --rm neozork-hld python -m pytest tests/ --cov=src --cov-report=html

# Запуск конкретных тестов в Docker
docker compose run --rm neozork-hld python -m pytest tests/test_stdio.py -v
```

### Тестирование MCP серверов в Docker
```bash
# Тест stdio режима в Docker
docker compose run --rm neozork-hld python tests/test_stdio.py

# Тест MCP функциональности в Docker
docker compose run --rm neozork-hld python -m pytest tests/mcp/ -v
```

## 📊 Отчеты о тестировании

### Генерация отчетов
```bash
# HTML отчет о покрытии
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# XML отчет для CI/CD
python -m pytest tests/ --cov=src --cov-report=xml

# JSON отчет
python -m pytest tests/ --cov=src --cov-report=json

# Множественные форматы
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term --cov-report=xml
```

### Анализ отчетов
```bash
# Просмотр HTML отчета
open htmlcov/index.html

# Анализ покрытия по модулям
python -c "import coverage; cov = coverage.Coverage(); cov.load(); print(cov.report())"
```

## 🎯 Специализированные тесты

### Тест производительности
```bash
# Тест производительности индикаторов
python -m pytest tests/calculation/indicators/performance/ -v

# Бенчмаркинг
python -m pytest tests/calculation/indicators/performance/test_performance.py -v
```

### Тест граничных случаев
```bash
# Тест граничных случаев
python -m pytest tests/calculation/indicators/edge_cases/ -v

# Тест с пустыми данными
python -m pytest tests/calculation/indicators/edge_cases/test_edge_cases.py::test_empty_data -v
```

### Тест валидации
```bash
# Тест математической валидации
python -m pytest tests/calculation/indicators/validation/ -v

# Тест корректности расчетов
python -m pytest tests/calculation/indicators/validation/test_mathematical_validation.py -v
```

## 🔄 Непрерывная интеграция

### GitHub Actions
```yaml
# Пример .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync
      - name: Run tests
        run: |
          python -m pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Локальная CI
```bash
# Скрипт для локальной CI
#!/bin/bash
set -e

echo "Running tests..."
python -m pytest tests/ --cov=src --cov-report=term-missing

echo "Running coverage analysis..."
python tests/zzz_analyze_test_coverage.py

echo "All tests passed!"
```

## 💡 Советы по тестированию

### Лучшие практики
```bash
# Запускайте тесты перед коммитом
python -m pytest tests/ -x

# Регулярно проверяйте покрытие
python -m pytest tests/ --cov=src --cov-report=html

# Используйте маркеры для категоризации
python -m pytest tests/ -m "unit"  # только unit тесты
python -m pytest tests/ -m "integration"  # только integration тесты

# Тестируйте граничные случаи
python -m pytest tests/calculation/indicators/edge_cases/ -v
```

### Отладка проблем
```bash
# Если тест падает, используйте отладчик
python -m pytest tests/failing_test.py::test_function -s --pdb

# Проверьте зависимости
pip list | grep pytest

# Проверьте версии
python -c "import pytest; print(pytest.__version__)"
```

---

📚 **Дополнительные ресурсы:**
- **[Руководство по тестированию](testing.md)** - Подробное руководство
- **[Полные примеры использования](usage-examples.md)** - Комплексные примеры
- **[Быстрые примеры](quick-examples.md)** - Быстрый старт
- **[Анализ покрытия](tests/zzz_analyze_test_coverage.py)** - Автоматический анализ покрытия 