# Indicator Examples

Примеры использования технических индикаторов в проекте.

## 🎯 Быстрый обзор индикаторов

### Просмотр доступных индикаторов
```bash
# Все индикаторы
python run_analysis.py --indicators

# По категориям
python run_analysis.py --indicators oscillators
python run_analysis.py --indicators trend
python run_analysis.py --indicators momentum
python run_analysis.py --indicators volatility
python run_analysis.py --indicators volume
python run_analysis.py --indicators predictive
python run_analysis.py --indicators probability
python run_analysis.py --indicators sentiment
python run_analysis.py --indicators suportresist

# Детальная информация
python run_analysis.py --indicators oscillators rsi
python run_analysis.py --indicators momentum macd
python run_analysis.py --indicators trend ema
```

## 📊 Oscillators (Осцилляторы)

### RSI (Relative Strength Index)
```bash
# Демо с RSI
python run_analysis.py demo --rule RSI

# Yahoo Finance с RSI
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# Binance с RSI
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule RSI

# CSV с RSI
python run_analysis.py csv --csv-file data.csv --point 0.01 --rule RSI
```

### Stochastic Oscillator
```bash
# Демо с Stochastic
python run_analysis.py demo --rule STOCH

# Реальные данные с Stochastic
python run_analysis.py yf -t EURUSD=X --period 3mo --point 0.00001 --rule STOCH
```

### CCI (Commodity Channel Index)
```bash
# Демо с CCI
python run_analysis.py demo --rule CCI

# Криптовалюты с CCI
python run_analysis.py binance -t ETHUSDT --interval H1 --point 0.001 --rule CCI
```

## 📈 Trend Indicators (Трендовые индикаторы)

### EMA (Exponential Moving Average)
```bash
# Демо с EMA
python run_analysis.py demo --rule EMA

# Акции с EMA
python run_analysis.py yf -t MSFT --period 6mo --point 0.01 --rule EMA

# Форекс с EMA
python run_analysis.py exrate -t GBPUSD --interval D1 --point 0.00001 --rule EMA
```

### ADX (Average Directional Index)
```bash
# Демо с ADX
python run_analysis.py demo --rule ADX

# Реальные данные с ADX
python run_analysis.py yf -t GOOGL --period 1y --point 0.01 --rule ADX
```

### SAR (Parabolic SAR)
```bash
# Демо с SAR
python run_analysis.py demo --rule SAR

# Криптовалюты с SAR
python run_analysis.py binance -t ADAUSDT --interval D1 --point 0.001 --rule SAR
```

## ⚡ Momentum Indicators (Моментум индикаторы)

### MACD (Moving Average Convergence Divergence)
```bash
# Демо с MACD
python run_analysis.py demo --rule MACD

# Акции с MACD
python run_analysis.py yf -t TSLA --period 3mo --point 0.01 --rule MACD

# Форекс с MACD
python run_analysis.py exrate -t USDJPY --interval D1 --point 0.01 --rule MACD
```

### Stochastic Oscillator (Momentum)
```bash
# Демо с Stochastic
python run_analysis.py demo --rule STOCH

# Реальные данные с Stochastic
python run_analysis.py yf -t BTC-USD --period 1y --point 0.01 --rule STOCH
```

## 📊 Volatility Indicators (Волатильность)

### ATR (Average True Range)
```bash
# Демо с ATR
python run_analysis.py demo --rule ATR

# Акции с ATR
python run_analysis.py yf -t NVDA --period 6mo --point 0.01 --rule ATR

# Криптовалюты с ATR
python run_analysis.py binance -t SOLUSDT --interval H4 --point 0.001 --rule ATR
```

### Bollinger Bands
```bash
# Демо с Bollinger Bands
python run_analysis.py demo --rule BB

# Форекс с Bollinger Bands
python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule BB

# Акции с Bollinger Bands
python run_analysis.py yf -t AMZN --period 1mo --point 0.01 --rule BB
```

### Standard Deviation
```bash
# Демо с Standard Deviation
python run_analysis.py demo --rule STDEV

# Реальные данные с Standard Deviation
python run_analysis.py yf -t META --period 3mo --point 0.01 --rule STDEV
```

## 📊 Volume Indicators (Объемные индикаторы)

### OBV (On-Balance Volume)
```bash
# Демо с OBV
python run_analysis.py demo --rule OBV

# Акции с OBV
python run_analysis.py yf -t NFLX --period 1mo --point 0.01 --rule OBV
```

### VWAP (Volume Weighted Average Price)
```bash
# Демо с VWAP
python run_analysis.py demo --rule VWAP

# Криптовалюты с VWAP
python run_analysis.py binance -t ETHUSDT --interval H1 --point 0.001 --rule VWAP

# Акции с VWAP
python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule VWAP
```

## 🎯 Support/Resistance (Поддержка/Сопротивление)

### Donchian Channels
```bash
# Демо с Donchian Channels
python run_analysis.py demo --rule DONCHIAN

# Форекс с Donchian Channels
python run_analysis.py exrate -t GBPJPY --interval D1 --point 0.01 --rule DONCHIAN
```

### Fibonacci Retracements
```bash
# Демо с Fibonacci Retracements
python run_analysis.py demo --rule FIBO

# Криптовалюты с Fibonacci Retracements
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule FIBO
```

### Pivot Points
```bash
# Демо с Pivot Points
python run_analysis.py demo --rule PIVOT

# Форекс с Pivot Points
python run_analysis.py exrate -t USDCAD --interval D1 --point 0.00001 --rule PIVOT
```

## 🔮 Predictive Indicators (Предиктивные индикаторы)

### HMA (Hull Moving Average)
```bash
# Демо с HMA
python run_analysis.py demo --rule HMA

# Реальные данные с HMA
python run_analysis.py yf -t SPY --period 3mo --point 0.01 --rule HMA
```

### Time Series Forecast
```bash
# Демо с Time Series Forecast
python run_analysis.py demo --rule TSFORECAST

# Акции с Time Series Forecast
python run_analysis.py yf -t QQQ --period 6mo --point 0.01 --rule TSFORECAST
```

## 🎲 Probability Indicators (Вероятностные индикаторы)

### Kelly Criterion
```bash
# Демо с Kelly Criterion
python run_analysis.py demo --rule KELLY

# Реальные данные с Kelly Criterion
python run_analysis.py yf -t IWM --period 1y --point 0.01 --rule KELLY
```

### Monte Carlo Simulation
```bash
# Демо с Monte Carlo
python run_analysis.py demo --rule MONTECARLO

# Криптовалюты с Monte Carlo
python run_analysis.py binance -t DOTUSDT --interval D1 --point 0.001 --rule MONTECARLO
```

## 😊 Sentiment Indicators (Сентимент индикаторы)

### Commitment of Traders
```bash
# Демо с COT
python run_analysis.py demo --rule COT

# Форекс с COT
python run_analysis.py exrate -t AUDUSD --interval D1 --point 0.00001 --rule COT
```

### Fear & Greed Index
```bash
# Демо с Fear & Greed
python run_analysis.py demo --rule FEARGREED

# Криптовалюты с Fear & Greed
python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule FEARGREED
```

### Social Sentiment
```bash
# Демо с Social Sentiment
python run_analysis.py demo --rule SOCIALSENTIMENT

# Акции с Social Sentiment
python run_analysis.py yf -t GME --period 1mo --point 0.01 --rule SOCIALSENTIMENT
```

## 🔄 Комбинирование индикаторов

### Множественные индикаторы в одном анализе
```bash
# Анализ с несколькими индикаторами
python run_analysis.py demo --rule RSI --export-parquet
python run_analysis.py demo --rule MACD --export-parquet
python run_analysis.py demo --rule EMA --export-parquet

# Просмотр результатов
python run_analysis.py show ind parquet
```

### Пакетная обработка индикаторов
```bash
# Обработка множественных индикаторов
for indicator in RSI MACD EMA BB ATR; do
    python run_analysis.py demo --rule $indicator --export-parquet
done
```

## 📊 Экспорт результатов

### Экспорт в разных форматах
```bash
# Parquet (рекомендуется для больших данных)
python run_analysis.py demo --rule RSI --export-parquet

# CSV (для Excel/таблиц)
python run_analysis.py demo --rule MACD --export-csv

# JSON (для API/веб-приложений)
python run_analysis.py demo --rule EMA --export-json

# Все форматы сразу
python run_analysis.py demo --rule BB --export-parquet --export-csv --export-json
```

### Просмотр экспортированных данных
```bash
# Просмотр parquet файлов
python run_analysis.py show ind parquet

# Просмотр CSV файлов
python run_analysis.py show ind csv

# Просмотр JSON файлов
python run_analysis.py show ind json
```

## 🎨 Различные бэкенды для графиков

### Интерактивные графики
```bash
# Plotly (интерактивный)
python run_analysis.py demo --rule RSI -d plotly

# Seaborn (красивые статические)
python run_analysis.py demo --rule MACD -d seaborn
```

### Быстрые бэкенды
```bash
# Самый быстрый
python run_analysis.py demo --rule EMA -d fastest

# Терминальный (для SSH/Docker)
python run_analysis.py demo --rule BB -d term
```

## 🔍 Специальные правила

### OHLCV (только свечи)
```bash
# Только график свечей без индикаторов
python run_analysis.py demo --rule OHLCV
```

### AUTO (автоопределение)
```bash
# Автоопределение колонок и индикаторов
python run_analysis.py demo --rule AUTO -d mpl
```

## 📈 Рабочие процессы

### Полный анализ акции
```bash
# 1. Загрузка данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Анализ с трендовыми индикаторами
python run_analysis.py show yf AAPL --rule EMA --export-parquet
python run_analysis.py show yf AAPL --rule ADX --export-parquet

# 3. Анализ с осцилляторами
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet

# 4. Анализ волатильности
python run_analysis.py show yf AAPL --rule BB --export-parquet
python run_analysis.py show yf AAPL --rule ATR --export-parquet

# 5. Просмотр результатов
python run_analysis.py show ind parquet
```

### Анализ криптовалют
```bash
# 1. Загрузка данных
python run_analysis.py binance -t BTCUSDT --interval D1 --start 2024-01-01 --end 2024-12-31 --point 0.01

# 2. Технический анализ
python run_analysis.py show binance BTCUSDT --rule RSI --export-parquet
python run_analysis.py show binance BTCUSDT --rule MACD --export-parquet
python run_analysis.py show binance BTCUSDT --rule BB --export-parquet

# 3. Просмотр результатов
python run_analysis.py show ind parquet
```

## 💡 Советы по использованию

### Выбор индикаторов
- **Трендовые рынки**: EMA, ADX, SAR
- **Боковые рынки**: RSI, Stochastic, Bollinger Bands
- **Волатильные рынки**: ATR, Standard Deviation
- **Объемный анализ**: OBV, VWAP

### Оптимизация производительности
```bash
# Используйте fastest бэкенд для больших данных
python run_analysis.py csv --csv-file large_data.csv --point 0.01 -d fastest

# Используйте term бэкенд для SSH/Docker
python run_analysis.py yf -t EURUSD=X --period 1mo --point 0.00001 -d term
```

### Отладка индикаторов
```bash
# Отладка конкретного индикатора
python scripts/debug_scripts/debug_indicators.py

# Проверка данных
python scripts/debug_scripts/debug_check_parquet.py
```

---

📚 **Дополнительные ресурсы:**
- **[Полные примеры использования](usage-examples.md)** - Подробные примеры и рабочие процессы
- **[Быстрые примеры](quick-examples.md)** - Быстрый старт
- **[Документация индикаторов](indicators/)** - Подробная документация по каждому индикатору 