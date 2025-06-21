#!/bin/bash

# -*- coding: utf-8 -*-
# scripts/init_dirs.sh

# Always run from the root of the repository, regardless of the current directory
cd "$(dirname "$0")/.." || exit 1

# Create main data directories
mkdir -p data/cache/csv_converted
mkdir -p data/raw_parquet
mkdir -p data/processed

# Create indicator export directories
mkdir -p data/indicators/parquet
mkdir -p data/indicators/csv
mkdir -p data/indicators/json

# Log and results directories
mkdir -p logs
mkdir -p results

# Source and script directories
mkdir -p src/eda
mkdir -p scripts/debug_scripts
mkdir -p scripts/log_analysis
mkdir -p scripts/data_processing

# Create directories for notebooks, source, tests, and MQL5 feed
mkdir -p notebooks
mkdir -p src
mkdir -p tests
mkdir -p mql5_feed

# Create .env file with default fields if it does not exist
if [ ! -f .env ]; then
cat > .env <<EOL
# Polygon.io API key
POLYGON_API_KEY=your_polygon_api_key_here

# Binance API keys
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Exchange Rate API Key from exchangerate-api.com
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key_here

# Add other environment variables as needed
EOL
    echo ".env file created with default fields."
else
    echo ".env file already exists, not overwritten."
fi

# === Индикаторы: новая структура ===
INDICATOR_BASE="src/calculation/indicators"
CATEGORIES=(
  "trend" "momentum" "volatility" "volume" "suportresist" \
  "oscillators" "sentiment" "predictive" "probability"
)
# Список индикаторов по категориям
TREND=("ema_ind.py" "adx_ind.py" "sar_ind.py" "supertrend_ind.py")
MOMENTUM=("rsi_ind.py" "macd_ind.py" "stochoscillator_ind.py")
VOLATILITY=("bb_ind.py" "atr_ind.py" "stdev_ind.py")
VOLUME=("obv_ind.py" "vwap_ind.py")
SUPORTRESIST=("pivot_ind.py" "fiboretr_ind.py" "donchain_ind.py")
OSCILLATORS=("rsi_ind.py" "stoch_ind.py" "cci_ind.py")
SENTIMENT=("putcallratio_ind.py" "cot_ind.py" "feargreed_ind.py")
PREDICTIVE=("hma_ind.py" "tsforecast_ind.py")
PROBABILITY=("montecarlo_ind.py" "kelly_ind.py")

# Создание папок и файлов
mkdir -p "$INDICATOR_BASE"
for cat in "${CATEGORIES[@]}"; do
  mkdir -p "$INDICATOR_BASE/$cat"
  touch "$INDICATOR_BASE/$cat/__init__.py"
done
# Файлы по категориям
for f in "${TREND[@]}"; do touch "$INDICATOR_BASE/trend/$f"; done
for f in "${MOMENTUM[@]}"; do touch "$INDICATOR_BASE/momentum/$f"; done
for f in "${VOLATILITY[@]}"; do touch "$INDICATOR_BASE/volatility/$f"; done
for f in "${VOLUME[@]}"; do touch "$INDICATOR_BASE/volume/$f"; done
for f in "${SUPORTRESIST[@]}"; do touch "$INDICATOR_BASE/suportresist/$f"; done
for f in "${OSCILLATORS[@]}"; do touch "$INDICATOR_BASE/oscillators/$f"; done
for f in "${SENTIMENT[@]}"; do touch "$INDICATOR_BASE/sentiment/$f"; done
for f in "${PREDICTIVE[@]}"; do touch "$INDICATOR_BASE/predictive/$f"; done
for f in "${PROBABILITY[@]}"; do touch "$INDICATOR_BASE/probability/$f"; done

echo "All required directories have been created."