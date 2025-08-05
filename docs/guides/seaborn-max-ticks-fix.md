# Seaborn MAXTICKS Fix

## Проблема

При использовании режима `-d sb` (seaborn) с индикатором MACD возникала ошибка:

```
Locator attempting to generate 1827 ticks ([7977.0, ..., 20759.0]), which exceeds Locator.MAXTICKS (1000).
```

Эта проблема возникала из-за того, что matplotlib пытался создать слишком много тиков для больших датасетов, превышая лимит в 1000 тиков.

## Причина

В файле `src/plotting/dual_chart_seaborn.py` использовался фиксированный интервал для тиков:

```python
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
ax2.xaxis.set_major_locator(mdates.DayLocator(interval=7))
```

Это приводило к попытке создания слишком большого количества тиков для больших датасетов.

## Решение

Исправление было применено в файле `src/plotting/dual_chart_seaborn.py`:

### До исправления:
```python
# Format x-axis for main chart
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
```

### После исправления:
```python
# Format x-axis for main chart
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Calculate appropriate interval based on data length and time range
data_length = len(display_df)
date_range = display_df.index.max() - display_df.index.min()
days_range = date_range.days

# Choose appropriate locator based on time range
if days_range > 365 * 5:  # More than 5 years
    ax1.xaxis.set_major_locator(mdates.YearLocator(2))  # Every 2 years
elif days_range > 365 * 2:  # More than 2 years
    ax1.xaxis.set_major_locator(mdates.YearLocator(1))  # Every year
elif days_range > 365:  # More than 1 year
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Every 3 months
elif days_range > 90:  # More than 3 months
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Every month
else:  # Less than 3 months
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days_range // 10)))

plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
```

## Логика выбора интервала

Исправление использует адаптивную логику выбора интервала тиков на основе временного диапазона данных:

- **Более 5 лет**: тики каждые 2 года (`YearLocator(2)`)
- **Более 2 лет**: тики каждый год (`YearLocator(1)`)
- **Более 1 года**: тики каждые 3 месяца (`MonthLocator(interval=3)`)
- **Более 3 месяцев**: тики каждый месяц (`MonthLocator(interval=1)`)
- **Менее 3 месяцев**: тики с интервалом `max(1, days_range // 10)` дней

## Тестирование

Создан тест `tests/plotting/test_dual_chart_seaborn_fix.py` для проверки исправления:

- `test_large_dataset_ticks_calculation()` - тест больших датасетов
- `test_medium_dataset_ticks_calculation()` - тест средних датасетов  
- `test_small_dataset_ticks_calculation()` - тест маленьких датасетов
- `test_no_max_ticks_error()` - тест отсутствия ошибки MAXTICKS
- `test_ticks_interval_calculation()` - тест правильного расчета интервалов

## Проверка исправления

Команда, которая раньше вызывала ошибку, теперь работает корректно:

```bash
uv run run_analysis.py show csv gbp -d sb --rule macd:12,26,9,close
```

## Совместимость

Исправление полностью совместимо с существующим кодом и не влияет на другие режимы отображения (`mpl`, `fastest`, `fast`, `term`).

## Файлы изменений

- `src/plotting/dual_chart_seaborn.py` - основное исправление
- `tests/plotting/test_dual_chart_seaborn_fix.py` - тесты для проверки исправления
- `docs/guides/seaborn-max-ticks-fix.md` - данная документация 