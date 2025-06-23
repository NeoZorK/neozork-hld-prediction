# EDA Examples

Примеры использования Exploratory Data Analysis (EDA) в проекте.

## 🔍 Быстрый старт EDA

### Запуск EDA скрипта
```bash
# Базовый запуск EDA
bash eda

# EDA с помощью
bash eda -h

# EDA с подробным выводом
bash eda --verbose

# EDA с экспортом результатов
bash eda --export-results
```

### EDA с UV
```bash
# Запуск EDA через UV
uv run ./eda

# EDA с параметрами
uv run ./eda --verbose --export-results
```

## 📊 Анализ данных

### Базовый статистический анализ
```bash
# Запуск базовой статистики
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# Анализ конкретного файла
python -c "from src.eda.basic_stats import analyze_file; analyze_file('data/test.csv')"

# Анализ с экспортом
python -c "from src.eda.basic_stats import analyze_data; analyze_data(export=True)"
```

### Корреляционный анализ
```bash
# Корреляционный анализ
python -c "from src.eda.correlation_analysis import analyze_correlations; analyze_correlations()"

# Анализ с визуализацией
python -c "from src.eda.correlation_analysis import plot_correlation_matrix; plot_correlation_matrix()"

# Анализ конкретных колонок
python -c "from src.eda.correlation_analysis import analyze_columns; analyze_columns(['close', 'volume'])"
```

### Анализ временных рядов
```bash
# Анализ временных рядов
python -c "from src.eda.time_series_analysis import analyze_time_series; analyze_time_series()"

# Анализ трендов
python -c "from src.eda.time_series_analysis import analyze_trends; analyze_trends()"

# Анализ сезонности
python -c "from src.eda.time_series_analysis import analyze_seasonality; analyze_seasonality()"
```

## 📈 Визуализация данных

### Базовые графики
```bash
# Создание базовых графиков
python -c "from src.eda.visualization import create_basic_plots; create_basic_plots()"

# График распределения
python -c "from src.eda.visualization import plot_distribution; plot_distribution('close')"

# График временного ряда
python -c "from src.eda.visualization import plot_time_series; plot_time_series('close')"
```

### Специализированные графики
```bash
# График свечей
python -c "from src.eda.visualization import plot_candlestick; plot_candlestick()"

# График объема
python -c "from src.eda.visualization import plot_volume; plot_volume()"

# График волатильности
python -c "from src.eda.visualization import plot_volatility; plot_volatility()"
```

### Интерактивные графики
```bash
# Интерактивный график с Plotly
python -c "from src.eda.visualization import create_interactive_plot; create_interactive_plot()"

# Интерактивная карта корреляций
python -c "from src.eda.visualization import plot_interactive_correlation; plot_interactive_correlation()"
```

## 🔍 Анализ качества данных

### Проверка качества данных
```bash
# Анализ качества данных
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# Проверка пропущенных значений
python -c "from src.eda.data_quality import check_missing_values; check_missing_values()"

# Проверка дубликатов
python -c "from src.eda.data_quality import check_duplicates; check_duplicates()"
```

### Обработка выбросов
```bash
# Анализ выбросов
python -c "from src.eda.outlier_analysis import analyze_outliers; analyze_outliers()"

# Визуализация выбросов
python -c "from src.eda.outlier_analysis import plot_outliers; plot_outliers()"

# Обработка выбросов
python -c "from src.eda.outlier_analysis import handle_outliers; handle_outliers()"
```

### Нормализация данных
```bash
# Анализ распределения
python -c "from src.eda.data_normalization import analyze_distribution; analyze_distribution()"

# Нормализация данных
python -c "from src.eda.data_normalization import normalize_data; normalize_data()"

# Стандартизация данных
python -c "from src.eda.data_normalization import standardize_data; standardize_data()"
```

## 📊 Анализ индикаторов

### Анализ технических индикаторов
```bash
# Анализ всех индикаторов
python -c "from src.eda.indicator_analysis import analyze_all_indicators; analyze_all_indicators()"

# Анализ конкретного индикатора
python -c "from src.eda.indicator_analysis import analyze_indicator; analyze_indicator('RSI')"

# Сравнение индикаторов
python -c "from src.eda.indicator_analysis import compare_indicators; compare_indicators(['RSI', 'MACD'])"
```

### Анализ сигналов
```bash
# Анализ сигналов индикаторов
python -c "from src.eda.signal_analysis import analyze_signals; analyze_signals()"

# Визуализация сигналов
python -c "from src.eda.signal_analysis import plot_signals; plot_signals()"

# Анализ точности сигналов
python -c "from src.eda.signal_analysis import analyze_signal_accuracy; analyze_signal_accuracy()"
```

## 🎯 Специализированный анализ

### Анализ трендов
```bash
# Анализ трендов
python -c "from src.eda.trend_analysis import analyze_trends; analyze_trends()"

# Определение трендов
python -c "from src.eda.trend_analysis import identify_trends; identify_trends()"

# Визуализация трендов
python -c "from src.eda.trend_analysis import plot_trends; plot_trends()"
```

### Анализ волатильности
```bash
# Анализ волатильности
python -c "from src.eda.volatility_analysis import analyze_volatility; analyze_volatility()"

# Расчет волатильности
python -c "from src.eda.volatility_analysis import calculate_volatility; calculate_volatility()"

# Визуализация волатильности
python -c "from src.eda.volatility_analysis import plot_volatility; plot_volatility()"
```

### Анализ объема
```bash
# Анализ объема
python -c "from src.eda.volume_analysis import analyze_volume; analyze_volume()"

# Анализ паттернов объема
python -c "from src.eda.volume_analysis import analyze_volume_patterns; analyze_volume_patterns()"

# Визуализация объема
python -c "from src.eda.volume_analysis import plot_volume_analysis; plot_volume_analysis()"
```

## 🔄 Рабочие процессы EDA

### Полный EDA пайплайн
```bash
# 1. Загрузка данных
python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Базовый анализ
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# 3. Анализ качества
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# 4. Корреляционный анализ
python -c "from src.eda.correlation_analysis import analyze_correlations; analyze_correlations()"

# 5. Временной анализ
python -c "from src.eda.time_series_analysis import analyze_time_series; analyze_time_series()"

# 6. Визуализация
python -c "from src.eda.visualization import create_comprehensive_plots; create_comprehensive_plots()"
```

### EDA для индикаторов
```bash
# 1. Расчет индикаторов
python run_analysis.py show yf AAPL --rule RSI --export-parquet
python run_analysis.py show yf AAPL --rule MACD --export-parquet

# 2. Анализ индикаторов
python -c "from src.eda.indicator_analysis import analyze_all_indicators; analyze_all_indicators()"

# 3. Анализ сигналов
python -c "from src.eda.signal_analysis import analyze_signals; analyze_signals()"

# 4. Визуализация результатов
python -c "from src.eda.visualization import plot_indicator_analysis; plot_indicator_analysis()"
```

### EDA для сравнения активов
```bash
# 1. Загрузка данных нескольких активов
python run_analysis.py yf -t AAPL --period 1y --point 0.01
python run_analysis.py yf -t MSFT --period 1y --point 0.01
python run_analysis.py yf -t GOOGL --period 1y --point 0.01

# 2. Сравнительный анализ
python -c "from src.eda.comparative_analysis import compare_assets; compare_assets(['AAPL', 'MSFT', 'GOOGL'])"

# 3. Анализ корреляций между активами
python -c "from src.eda.correlation_analysis import analyze_asset_correlations; analyze_asset_correlations()"
```

## 📊 Экспорт результатов

### Экспорт в разные форматы
```bash
# Экспорт в CSV
python -c "from src.eda.export import export_to_csv; export_to_csv('eda_results.csv')"

# Экспорт в JSON
python -c "from src.eda.export import export_to_json; export_to_json('eda_results.json')"

# Экспорт в Excel
python -c "from src.eda.export import export_to_excel; export_to_excel('eda_results.xlsx')"

# Экспорт графиков
python -c "from src.eda.export import export_plots; export_plots('plots/')"
```

### Генерация отчетов
```bash
# Генерация HTML отчета
python -c "from src.eda.reporting import generate_html_report; generate_html_report()"

# Генерация PDF отчета
python -c "from src.eda.reporting import generate_pdf_report; generate_pdf_report()"

# Генерация Markdown отчета
python -c "from src.eda.reporting import generate_markdown_report; generate_markdown_report()"
```

## 🐳 EDA в Docker

### Запуск EDA в контейнере
```bash
# Запуск EDA скрипта в Docker
docker compose run --rm neozork-hld bash eda

# EDA с UV в Docker
docker compose run --rm neozork-hld uv run ./eda

# Интерактивная EDA сессия
docker compose run --rm -it neozork-hld bash
```

### Анализ данных в контейнере
```bash
# Базовый анализ в контейнере
docker compose run --rm neozork-hld python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# Визуализация в контейнере
docker compose run --rm neozork-hld python -c "from src.eda.visualization import create_basic_plots; create_basic_plots()"

# Экспорт результатов из контейнера
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld python -c "from src.eda.export import export_to_csv; export_to_csv('results/eda_results.csv')"
```

## 🔍 Отладка EDA

### Отладочные команды
```bash
# Проверка данных для EDA
python -c "from src.eda.debug import check_data_for_eda; check_data_for_eda()"

# Проверка зависимостей EDA
python -c "from src.eda.debug import check_eda_dependencies; check_eda_dependencies()"

# Тестирование EDA функций
python -c "from src.eda.debug import test_eda_functions; test_eda_functions()"
```

### Логирование EDA
```bash
# Включение логирования EDA
python -c "from src.eda.logging import setup_eda_logging; setup_eda_logging()"

# Логирование с уровнем DEBUG
python -c "from src.eda.logging import setup_eda_logging; setup_eda_logging(level='DEBUG')"

# Экспорт логов EDA
python -c "from src.eda.logging import export_eda_logs; export_eda_logs('logs/eda.log')"
```

## 🎯 Специализированные сценарии

### EDA для машинного обучения
```bash
# Подготовка данных для ML
python -c "from src.eda.ml_preparation import prepare_data_for_ml; prepare_data_for_ml()"

# Анализ признаков
python -c "from src.eda.feature_analysis import analyze_features; analyze_features()"

# Выбор признаков
python -c "from src.eda.feature_selection import select_features; select_features()"
```

### EDA для бэктестинга
```bash
# Анализ данных для бэктестинга
python -c "from src.eda.backtest_preparation import prepare_backtest_data; prepare_backtest_data()"

# Анализ результатов бэктестинга
python -c "from src.eda.backtest_analysis import analyze_backtest_results; analyze_backtest_results()"

# Визуализация результатов бэктестинга
python -c "from src.eda.backtest_visualization import plot_backtest_results; plot_backtest_results()"
```

### EDA для риск-менеджмента
```bash
# Анализ рисков
python -c "from src.eda.risk_analysis import analyze_risks; analyze_risks()"

# Расчет Value at Risk (VaR)
python -c "from src.eda.risk_analysis import calculate_var; calculate_var()"

# Анализ максимальных просадок
python -c "from src.eda.risk_analysis import analyze_drawdowns; analyze_drawdowns()"
```

## 💡 Советы по использованию

### Лучшие практики
```bash
# Всегда начинайте с базового анализа
python -c "from src.eda.basic_stats import analyze_data; analyze_data()"

# Проверяйте качество данных
python -c "from src.eda.data_quality import analyze_data_quality; analyze_data_quality()"

# Визуализируйте результаты
python -c "from src.eda.visualization import create_basic_plots; create_basic_plots()"

# Экспортируйте результаты
python -c "from src.eda.export import export_to_csv; export_to_csv('eda_results.csv')"
```

### Оптимизация производительности
```bash
# Используйте выборку для больших данных
python -c "from src.eda.optimization import analyze_sample; analyze_sample(sample_size=10000)"

# Кэширование результатов
python -c "from src.eda.optimization import cache_eda_results; cache_eda_results()"

# Параллельная обработка
python -c "from src.eda.optimization import parallel_eda; parallel_eda()"
```

---

📚 **Дополнительные ресурсы:**
- **[Анализ EDA](analysis-eda.md)** - Подробная документация по EDA
- **[Полные примеры использования](usage-examples.md)** - Комплексные примеры
- **[Быстрые примеры](quick-examples.md)** - Быстрый старт
- **[Примеры индикаторов](indicator-examples.md)** - Анализ технических индикаторов 