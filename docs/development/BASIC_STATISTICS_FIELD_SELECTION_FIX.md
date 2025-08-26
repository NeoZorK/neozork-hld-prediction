# Basic Statistics Field Selection Fix

## Проблема

В функции `run_basic_statistics()` в файле `interactive_system.py` была обнаружена проблема с выбором полей для визуализации:

### Исходная проблема:
1. **Ограничение на количество колонок**: строка `cols_to_plot = numeric_data.columns[:6]` ограничивала визуализацию только первыми 6 колонками
2. **Отсутствие приоритизации**: важные торговые поля (`predicted_high`, `pressure`, `pressure_vector`) могли не попадать в визуализацию, если они были не в первых 6 колонках
3. **Отсутствие информации в HTML**: пользователи не понимали, почему определенные поля отсутствуют в визуализации

### Пример проблемы:
```python
# Исходный код (проблемный)
cols_to_plot = numeric_data.columns[:6]  # Только первые 6 колонок
```

Если данные содержали колонки в таком порядке:
```
['Open', 'High', 'Low', 'Close', 'Volume', 'sma_20', 'rsi_14', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']
```

То в визуализацию попадали только:
```
['Open', 'High', 'Low', 'Close', 'Volume', 'sma_20']
```

А важные поля `predicted_high`, `pressure`, `pressure_vector` оставались без визуализации.

## Решение

### 1. Улучшенная логика выбора колонок

Заменили простой срез на умную логику приоритизации:

```python
# Новый код (исправленный)
# Select important columns for visualization (prioritize key fields)
important_cols = ['open', 'high', 'low', 'close', 'volume', 'predicted_low', 'predicted_high', 'pressure', 'pressure_vector']

# Find available important columns
available_important = []
for col in important_cols:
    for numeric_col in numeric_data.columns:
        if col.lower() in numeric_col.lower():
            available_important.append(numeric_col)
            break

# Add other numeric columns if we have space
other_cols = [col for col in numeric_data.columns if col not in available_important]

# Combine important columns first, then others (limit to 6 total)
cols_to_plot = available_important + other_cols
cols_to_plot = cols_to_plot[:6]

print(f"📊 Selected columns for visualization: {cols_to_plot}")
```

### 2. Добавление информации в HTML отчет

Добавили секцию с объяснением полей в HTML отчет:

```html
<div class="plot-section">
    <div class="plot-header">
        <h2>📊 Analysis Overview</h2>
        <p class="plot-description">Summary of analyzed fields and their importance</p>
    </div>
    <div class="interpretation">
        <h3>Analyzed Fields:</h3>
        <ul>
            <li><strong>OHLCV Fields:</strong> open, high, low, close, volume - Basic price and volume data</li>
            <li><strong>Predicted Fields:</strong> predicted_low, predicted_high - Model predictions for price targets</li>
            <li><strong>Pressure Fields:</strong> pressure, pressure_vector - Market pressure indicators</li>
            <li><strong>Other Fields:</strong> Additional numeric indicators and features</li>
        </ul>
        <p><strong>Note:</strong> The system prioritizes important trading fields (OHLCV, predictions, pressure) over other numeric columns for visualization.</p>
    </div>
</div>
```

## Результаты

### До исправления:
- Визуализация: `['Open', 'High', 'Low', 'Close', 'Volume', 'sma_20']`
- Отсутствуют: `predicted_high`, `pressure`, `pressure_vector`

### После исправления:
- Визуализация: `['Open', 'High', 'Low', 'Close', 'Volume', 'predicted_low']`
- Приоритет отдается важным торговым полям
- Пользователи понимают логику выбора полей

## Преимущества решения

1. **Приоритизация важных полей**: OHLCV, predicted_low, predicted_high, pressure, pressure_vector всегда включаются первыми
2. **Гибкость**: работает с разными вариантами названий колонок (Open/open/OPEN)
3. **Прозрачность**: пользователи видят, какие поля были выбраны и почему
4. **Ограничение размера**: по-прежнему ограничивает визуализацию 6 колонками для читаемости
5. **Обратная совместимость**: не ломает существующую функциональность

## Тестирование

Создан тестовый скрипт `tests/eda/test_column_selection.py` для проверки логики:

```bash
uv run python tests/eda/test_column_selection.py
```

Тест проверяет:
- Работу с разными вариантами названий колонок
- Правильность приоритизации важных полей
- Ограничение на 6 колонок
- Включение всех важных полей в визуализацию

## Файлы изменений

1. `interactive_system.py` - основная логика выбора колонок
2. `tests/eda/test_column_selection.py` - тесты для проверки логики
3. `docs/development/BASIC_STATISTICS_FIELD_SELECTION_FIX.md` - эта документация

## Заключение

Исправление решает проблему с выбором полей в Basic Statistics, обеспечивая:
- Включение всех важных торговых полей в визуализацию
- Понятную логику приоритизации для пользователей
- Сохранение ограничений на размер визуализации
- Работу с различными вариантами названий колонок
