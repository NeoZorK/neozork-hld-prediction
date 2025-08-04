# SuperTrend Hover Tool Fix (Fast Mode Only)

## Проблема

При использовании команды с режимом `-d fast`:
```bash
uv run run_analysis.py show csv gbp -d fast --rule supertrend:10,3,open
```

В hover tool отображались значения "???" для полей:
- Date
- SuperTrend  
- Direction

**Примечание**: Это исправление применяется только для режима `-d fast`. Другие режимы (fastest, plotly, mpl и т.д.) не затронуты.

## Причина проблемы

Проблема была в том, что hover tool для SuperTrend индикатора использовал неправильные колонки данных:

1. **Неправильный режим hover**: Использовался `mode='mouse'` вместо `mode='vline'`
2. **Неправильные колонки данных**: Hover tool всегда использовал `@supertrend`, но данные могли быть в колонках `PPrice1`/`PPrice2`
3. **Отсутствие данных в ColumnDataSource**: Не все необходимые колонки передавались в источник данных

## Решение

### 1. Исправление режима hover

Изменен режим hover с `mouse` на `vline` для лучшей совместимости:

```python
# Было:
mode='mouse'

# Стало:
mode='vline'
```

### 2. Динамический выбор колонок

Добавлена логика для динамического выбора правильных колонок:

```python
elif indicator_name == 'supertrend':
    # Check if we have PPrice1/PPrice2 or direct supertrend column
    has_pprice = 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns
    if has_pprice:
        # Use PPrice1 for hover (support level)
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SuperTrend", "@PPrice1{0.5f}"),
                ("Direction", "@Direction{0.0f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
    else:
        # Use direct supertrend column
        return HoverTool(
            tooltips=[
                ("Date", "@index{%F %H:%M}"),
                ("SuperTrend", "@supertrend{0.5f}"),
                ("Direction", "@Direction{0.0f}")
            ],
            formatters={'@index': 'datetime'},
            mode='vline'
        )
```

### 3. Улучшение передачи данных в ColumnDataSource

Добавлено обеспечение того, что все необходимые колонки передаются в источник данных:

```python
# Add supertrend values to both display_df and source for hover tool
display_df['supertrend'] = supertrend_values
if source is not None:
    source.data['supertrend'] = supertrend_values
    
    # Also ensure PPrice1 and PPrice2 are in source for fallback hover
    source.data['PPrice1'] = p1
    source.data['PPrice2'] = p2
    
    # Ensure Direction is also in the main source for hover tool
    if 'Direction' not in source.data:
        source.data['Direction'] = direction
        
    # Ensure all required columns are in source for proper hover functionality
    source.data['index'] = display_df['index'] if 'index' in display_df.columns else display_df.index
```

## Тестирование

Создан комплексный тест `tests/plotting/test_fast_supertrend_hover_fix.py` который проверяет:

1. **Hover с колонками PPrice1/PPrice2**: Проверяет, что используется `@PPrice1`
2. **Hover с прямой колонкой supertrend**: Проверяет, что используется `@supertrend`
3. **Форматтеры**: Проверяет правильность форматтеров даты
4. **Отсутствие колонок**: Проверяет работу при отсутствии некоторых колонок
5. **Отсутствие Direction**: Проверяет работу без колонки Direction

## Затронутые файлы

- `src/plotting/fast_plot.py` - Основное исправление для режима fast
- `tests/plotting/test_fast_supertrend_hover_fix.py` - Новый тест для режима fast

## Результат

После исправления hover tool для SuperTrend индикатора корректно отображает:

- **Date**: Правильная дата в формате YYYY-MM-DD HH:MM
- **SuperTrend**: Числовое значение SuperTrend с точностью 0.5f
- **Direction**: Числовое значение направления тренда с точностью 0.0f

## Проверка исправления

Для проверки исправления выполните:

```bash
# Тест hover tool для режима fast
uv run pytest tests/plotting/test_fast_supertrend_hover_fix.py -v

# Проверка в браузере (только режим fast)
uv run run_analysis.py show csv gbp -d fast --rule supertrend:10,3,open
```

График откроется в браузере, и при наведении на SuperTrend индикатор будут отображаться корректные значения вместо "???".

**Важно**: Это исправление работает только для режима `-d fast`. Для других режимов (fastest, plotly, mpl) используйте соответствующие команды. 