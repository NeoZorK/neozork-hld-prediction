# SuperTrend MPL Display Fix

## Проблема

Индикатор SuperTrend не отображался в режиме `mpl` при использовании команды:
```bash
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:10,3,open
```

## Причина

В файле `src/plotting/dual_chart_mpl.py` отсутствовала обработка индикатора SuperTrend. В то время как другие режимы отображения (fastest, fast) имели полную поддержку SuperTrend, mpl режим не содержал соответствующего кода.

## Решение

Добавлена обработка SuperTrend индикатора в файл `src/plotting/dual_chart_mpl.py`:

### Добавленный код

```python
elif indicator_name == 'supertrend':
    y_axis_label = 'Price'
    
    # Check for SuperTrend columns
    has_supertrend = 'SuperTrend' in display_df.columns
    has_direction = 'SuperTrend_Direction' in display_df.columns
    has_signal = 'SuperTrend_Signal' in display_df.columns
    
    if has_supertrend:
        # Plot SuperTrend line
        supertrend_values = display_df['SuperTrend']
        ax2.plot(display_df.index, supertrend_values, 
                color='blue', linewidth=3, label='SuperTrend')
        
        # Plot price series for reference
        if 'Open' in display_df.columns:
            ax2.plot(display_df.index, display_df['Open'], 
                    color='gray', linewidth=1, alpha=0.7, label='Price')
        
        # Add trend direction visualization
        if has_direction:
            trend_direction = display_df['SuperTrend_Direction']
            
            # Color segments based on trend direction
            uptrend_mask = trend_direction == 1
            downtrend_mask = trend_direction == -1
            
            if uptrend_mask.any():
                ax2.plot(display_df.index[uptrend_mask], supertrend_values[uptrend_mask], 
                        color='green', linewidth=4, alpha=0.8, label='Uptrend')
            
            if downtrend_mask.any():
                ax2.plot(display_df.index[downtrend_mask], supertrend_values[downtrend_mask], 
                        color='red', linewidth=4, alpha=0.8, label='Downtrend')
        
        # Add signal points
        if has_signal:
            buy_signals = display_df['SuperTrend_Signal'] == 1  # BUY
            sell_signals = display_df['SuperTrend_Signal'] == 2  # SELL
            
            if buy_signals.any():
                ax2.scatter(display_df.index[buy_signals], supertrend_values[buy_signals], 
                          color='green', s=50, marker='^', label='Buy Signal')
            
            if sell_signals.any():
                ax2.scatter(display_df.index[sell_signals], supertrend_values[sell_signals], 
                          color='red', s=50, marker='v', label='Sell Signal')
    
    # Fallback: use PPrice1/PPrice2 if SuperTrend column not available
    elif 'PPrice1' in display_df.columns and 'PPrice2' in display_df.columns:
        # Create SuperTrend values from PPrice1/PPrice2
        p1 = display_df['PPrice1']
        p2 = display_df['PPrice2']
        direction = display_df.get('Direction', pd.Series(0, index=display_df.index))
        
        # Use PPrice1 as SuperTrend (support level)
        supertrend_values = p1
        ax2.plot(display_df.index, supertrend_values, 
                color='blue', linewidth=3, label='SuperTrend (Support)')
        
        # Also plot resistance level
        ax2.plot(display_df.index, p2, 
                color='orange', linewidth=2, linestyle='--', label='Resistance')
        
        # Add signal points if available
        if 'Direction' in display_df.columns:
            buy_signals = direction == 1  # BUY
            sell_signals = direction == 2  # SELL
            
            if buy_signals.any():
                ax2.scatter(display_df.index[buy_signals], supertrend_values[buy_signals], 
                          color='green', s=50, marker='^', label='Buy Signal')
            
            if sell_signals.any():
                ax2.scatter(display_df.index[sell_signals], supertrend_values[sell_signals], 
                          color='red', s=50, marker='v', label='Sell Signal')
```

## Функциональность

### Основные возможности

1. **Отображение линии SuperTrend**: Основная линия индикатора отображается синим цветом
2. **Визуализация направления тренда**: 
   - Зеленый цвет для восходящего тренда
   - Красный цвет для нисходящего тренда
3. **Сигнальные точки**:
   - Зеленые треугольники вверх для сигналов покупки
   - Красные треугольники вниз для сигналов продажи
4. **Резервный режим**: Если колонки SuperTrend недоступны, используется PPrice1/PPrice2

### Поддерживаемые параметры

- `period`: Период ATR (по умолчанию: 10)
- `multiplier`: Множитель ATR (по умолчанию: 3.0)
- `price_type`: Тип цены (`open` или `close`)

### Примеры использования

```bash
# Базовое использование
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:10,3,open

# С другими параметрами
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:14,2.5,close

# Короткий период, низкий множитель (более чувствительный)
uv run run_analysis.py show csv gbp -d mpl --rule supertrend:5,2.0,open
```

## Тестирование

Создан комплексный набор тестов в `tests/plotting/test_dual_chart_mpl_supertrend.py`:

- ✅ Тест с колонками SuperTrend
- ✅ Тест с резервными колонками PPrice1/PPrice2
- ✅ Тест сигнальных точек
- ✅ Тест направления тренда
- ✅ Тест парсинга параметров
- ✅ Тест обработки ошибок

Все тесты проходят успешно.

## Результат

Теперь SuperTrend индикатор корректно отображается в режиме `mpl` со всеми функциями:

- ✅ Основная линия SuperTrend
- ✅ Цветовое кодирование тренда
- ✅ Сигнальные точки
- ✅ Поддержка различных параметров
- ✅ Резервный режим работы
- ✅ Полное покрытие тестами

## Совместимость

Исправление полностью совместимо с существующим кодом и не влияет на другие индикаторы или режимы отображения. 