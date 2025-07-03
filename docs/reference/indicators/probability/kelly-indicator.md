# Kelly Criterion Oscillator (Probability)

## Overview

The Kelly Criterion Oscillator is a probability-based indicator that calculates the optimal position size for trading based on the historical win probability and risk/reward ratio. It is visualized в стиле MACD: основная линия, сигнальная линия (EMA), гистограмма и пороговые уровни.

## How It Works

1. **Calculation**: For each point, the indicator computes the percentage price changes over a rolling window (period, e.g., 20 bars).
2. **Win/Loss Analysis**: It counts the number of positive (win) and negative (loss) returns in the window.
3. **Kelly Formula**: Calculates the Kelly fraction:
   
   \[
   f = \frac{bp - q}{b}
   \]
   where:
   - \(b\) = average win / average loss (odds)
   - \(p\) = win probability
   - \(q = 1 - p\) = loss probability

4. **Signal Line**: Exponential moving average (EMA, span=9) of the Kelly line.
5. **Histogram**: Difference between Kelly and signal line.
6. **Thresholds**: 0.1 (10%) — минимальный уровень для сигнала, 0.25 (25%) — максимальный допустимый Kelly.

## Output Fields

- **kelly**: Основная линия Kelly (оптимальная доля капитала для сделки)
- **kelly_signal**: EMA(9) от Kelly (сигнальная линия)
- **kelly_histogram**: Разница между Kelly и сигнальной линией
- **kelly_threshold_10**: Линия порога 0.1 (10%)
- **kelly_threshold_25**: Линия порога 0.25 (25%)

## Visualization (MACD-style)

- **Blue line**: Kelly fraction (main line)
- **Red line**: Signal line (EMA)
- **Green/Red bars**: Histogram (green — Kelly выше сигнальной, red — ниже)
- **Orange dashed**: 10% threshold
- **Red dashed**: 25% threshold
- **Gray dashed**: Zero line

## Interpretation

- **Kelly > 0.1**: Сигнал к увеличению позиции (BUY), если линия растет
- **Kelly < 0.1**: Сигнал к снижению позиции (SELL), если линия падает
- **Histogram > 0**: Усиление сигнала, Kelly выше сигнальной
- **Histogram < 0**: Ослабление сигнала, Kelly ниже сигнальной
- **Kelly > 0.25**: Не рекомендуется, слишком агрессивно

## Best Practices

- Используйте Kelly только с надежными историческими данными
- Не превышайте 25% Kelly (слишком высокий риск)
- Комбинируйте с фильтрами тренда (например, EMA, MACD)
- Для волатильных рынков уменьшайте период (например, 10-15)
- Для стабильных рынков увеличивайте период (20-30)
- Используйте сигнальную линию для подтверждения

## Example Chart

```mermaid
graph LR
    A[Kelly Line (blue)] -- Above Signal --> B[Histogram (green)]
    A -- Below Signal --> C[Histogram (red)]
    D[Signal Line (red)]
    E[Threshold 0.1 (orange dashed)]
    F[Threshold 0.25 (red dashed)]
    G[Zero Line (gray dashed)]
```

## Integration with Other Indicators

- **MACD**: Используйте Kelly для фильтрации MACD-сигналов (например, только если Kelly > 0.1)
- **RSI**: Не открывайте сделки по Kelly, если RSI в зоне перекупленности/перепроданности
- **ATR**: Используйте ATR для динамического управления размером позиции
- **Bollinger Bands**: Kelly может усиливать сигналы выхода за границы полос

## References
- Kelly, J. L. (1956). "A New Interpretation of Information Rate". Bell System Technical Journal.
- Investopedia: [Kelly Criterion](https://www.investopedia.com/terms/k/kellycriterion.asp)

---

_Документация подготовлена для режима dual chart fastest. Все примеры и рекомендации актуальны только для этого режима._ 