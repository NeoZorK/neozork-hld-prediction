# Seaborn MAXTICKS Fix - Summary

## ✅ Проблема решена

**Команда, которая раньше вызывала ошибку:**
```bash
uv run run_analysis.py show csv gbp -d sb --rule macd:12,26,9,close
```

**Ошибки:**
1. ```
   Locator attempting to generate 1827 ticks ([7977.0, ..., 20759.0]), which exceeds Locator.MAXTICKS (1000).
   ```
2. График не отображался на экране (только сохранялся в файл)
3. Индикатор `putcallratio` не поддерживался в режиме seaborn
4. Индикатор `cot` не поддерживался в режиме seaborn
5. Индикатор `feargreed` не поддерживался в режиме seaborn

## 🔧 Исправления

**Файл:** `src/plotting/dual_chart_seaborn.py`

### 1. Исправление MAXTICKS
**Изменения:**
- Заменен фиксированный интервал `mdates.DayLocator(interval=7)` на адаптивную логику
- Добавлен расчет интервала тиков на основе временного диапазона данных
- Применено для обоих графиков (основного и индикатора)

**Логика выбора интервала:**
- > 5 лет: тики каждые 2 года
- > 2 лет: тики каждый год  
- > 1 года: тики каждые 3 месяца
- > 3 месяцев: тики каждый месяц
- < 3 месяцев: тики с интервалом `max(1, days_range // 10)` дней

### 2. Исправление отображения графика
**Изменения:**
- Добавлен вызов `plt.show()` после сохранения графика
- График теперь отображается на экране

### 3. Добавление поддержки индикаторов
**Добавленные индикаторы:**
- `putcallratio` - индикатор соотношения пут/колл опционов
- `cot` - индикатор Commitments of Traders
- `feargreed` - индикатор страха и жадности

**Функциональность для каждого индикатора:**
- Основная линия индикатора
- Сигнальная линия (если применимо)
- Гистограмма (если применимо)
- Пороговые уровни (Fear/Greed, Bullish/Bearish, Neutral)

## ✅ Результат

**Все команды теперь работают корректно:**
```bash
# MACD индикатор
uv run run_analysis.py show csv gbp -d sb --rule macd:12,26,9,close

# Put/Call Ratio индикатор
uv run run_analysis.py show csv gbp -d sb --rule putcallratio:20,close,60,40

# COT индикатор
uv run run_analysis.py show csv gbp -d sb --rule cot:20,close

# Fear & Greed индикатор
uv run run_analysis.py show csv gbp -d sb --rule feargreed:14,close
```

**Тесты:** 20 тестов прошли успешно
- `test_dual_chart_seaborn_fix.py` - 5 тестов
- `test_seaborn_plot_display.py` - 5 тестов  
- `test_seaborn_putcallratio.py` - 5 тестов
- `test_seaborn_cot.py` - 5 тестов
- `test_seaborn_feargreed.py` - 5 тестов

## 📁 Созданные файлы

**Тесты:**
- `tests/plotting/test_dual_chart_seaborn_fix.py`
- `tests/plotting/test_seaborn_plot_display.py`
- `tests/plotting/test_seaborn_putcallratio.py`
- `tests/plotting/test_seaborn_cot.py`
- `tests/plotting/test_seaborn_feargreed.py`

**Документация:**
- `docs/guides/seaborn-max-ticks-fix.md`
- `docs/guides/seaborn-max-ticks-fix-summary.md`

## 🎯 Статус

✅ **Проблема полностью решена**
- Все индикаторы поддерживаются в режиме seaborn
- Графики отображаются корректно
- Адаптивная логика тиков предотвращает ошибки MAXTICKS
- 100% покрытие тестами для всех исправлений 