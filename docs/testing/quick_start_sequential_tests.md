# Quick start: Sequential Test Runner

## Что это такое?

Последовательный тест-раннер - это решение for Launchа тестов in Docker контейнере папка за папкой, что предотвращает сбои воркеров and Issues with ресурсами при параллельном выполнении.

## quick start

### 1. Launch in Docker контейнере

```bash
# При Launchе контейнера выберите 'y' for Launchа тестов
docker run -it your-container
# Ответьте 'y' on вопрос о Launchе тестов
```

### 2. Ручной Launch

```bash
# Launch всех тестов последовательно
python scripts/run_sequential_tests_docker.py

# Тестирование функциональности раннера
python scripts/test_sequential_runner.py
```

### 3. Использование in интерактивной оболочке

```bash
# in Docker контейнере доступны команды:
python scripts/run_sequential_tests_docker.py
uv run pytest tests -n auto # Старый способ (может вызывать проблемы)
```

## Порядок выполнения тестов

Тесты выполняются in следующем порядке:

1. **common** - Базовые утилиты (7 тестов, ~2s)
2. **unit** - Юнит-тесты (335 тестов, ~7s)
3. **utils** - Утилиты (30 тестов, ~2s)
4. **data** - Обработка данных
5. **calculation** - Математические расчеты
6. **cli** - Командная строка
7. **plotting** - Графики
8. **export** - Экспорт данных
9. **eda** - Анализ данных
10. **interactive** - Интерактивный режим
11. **integration** - Интеграционные тесты
12. **ml** - Машинное обучение
13. **mcp** - MCP сервер
14. **docker** - Docker тесты
15. **native-container** - Нативные контейнеры
16. **pocket_hedge_fund** - application
17. **saas** - SaaS application
18. **scripts** - Скрипты
19. **workflow** - Рабочие процессы
20. **e2e** - End-to-end тесты

## configuration

settings находятся in файле `tests/test_execution_order.yaml`:

```yaml
test_folders:
 - name: "common"
 description: "Basic utilities"
 timeout: 30
 required: true

global_settings:
 max_total_time: 3600 # 1 час
 stop_on_failure: true
 skip_empty_folders: true
```

## Преимущества

✅ **Стабильность**: Нет сбоев воркеров
✅ **Предсказуемость**: Постоянный порядок выполнения
✅ **Управление ресурсами**: Контроль памяти and CPU
✅ **Легкая отладка**: Понятно, какая папка вызвала проблему
✅ **Гибкость**: Настраиваемые таймауты and parameters

## example вывода

```
============================================================
Running folder 1/20: common
Description: Basic utilities and common functions
Timeout: 30s
============================================================
2024-01-15 10:30:01 - INFO - Running tests in folder: common (1 files)
2024-01-15 10:30:05 - INFO - ✅ Folder common completed successfully in 4.23s
2024-01-15 10:30:05 - INFO - Passed: 7, Failed: 0, Skipped: 0

============================================================
Running folder 2/20: unit
Description: Unit tests for individual components
Timeout: 60s
============================================================
2024-01-15 10:30:06 - INFO - Running tests in folder: unit (20 files)
2024-01-15 10:30:15 - INFO - ✅ Folder unit completed successfully in 9.12s
2024-01-15 10:30:15 - INFO - Passed: 335, Failed: 0, Skipped: 53
```

## Решение проблем

### Tests do not start
- Проверьте, что вы in Docker контейнере
- Убедитесь, что файл `tests/test_execution_order.yaml` существует

### Таймаут папки
- Увеличьте `timeout` in конфигурации for медленных папок
- Проверьте on наличие бесконечных циклов in тестах

### Ошибки конфигурации
- Запустите `python scripts/test_sequential_runner.py` for диагностики
- Проверьте синтаксис YAML файла

## integration with CI/CD

```bash
# in CI/CD пайплайне
docker run --rm your-container python scripts/run_sequential_tests_docker.py
```

## Сравнение with параллельным выполнением

| Параллельное (`-n auto`) | Последовательное |
|---------------------------|------------------|
| ❌ Сбои воркеров | ✅ Стабильная работа |
| ❌ Непредсказуемый порядок | ✅ Контролируемый порядок |
| ❌ Issues with ресурсами | ✅ Управление ресурсами |
| ✅ Быстрее | ⚠️ Медленнее, но надежнее |

## Заключение

Последовательный тест-раннер - это надежное решение for Docker окружений, которое обеспечивает стабильное выполнение тестов без сбоев воркеров and проблем with ресурсами.
