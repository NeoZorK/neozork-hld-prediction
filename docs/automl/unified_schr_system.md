# Unified SCHR Levels AutoML System
# Единая система SCHR Levels AutoML

## 🎯 Описание

Unified SCHR System - это единая система для создания robust profitable ML-моделей на основе SCHR Levels индикаторов. Система объединяет лучшие части из `schr-levels-gluon.py` и `src/automl/gluon/` в единую рабочую систему.

## 🚀 Основные возможности

### 1. **4 задачи ML:**
- **pressure_vector_sign** - предсказание знака PRESSURE_VECTOR (+ или -)
- **price_direction_1period** - предсказание направления цены (вверх/вниз/hold)
- **level_breakout** - предсказание пробития уровней (пробитие вверх/вниз/между уровнями)
- **trading_signal** - комплексный торговый сигнал (buy/sell/hold)

### 2. **Robust валидация:**
- **Walk Forward Analysis** - проверка стабильности на временных рядах
- **Monte Carlo Simulation** - оценка робастности модели
- **Backtesting** - тестирование на исторических данных

### 3. **Enhanced Features:**
- Технические индикаторы (SMA, RSI, MACD, ATR)
- SCHR Levels признаки (расстояние до уровней, позиция)
- Pressure features (лаги, скользящие средние)
- Временные признаки (час, день недели, месяц)

## 📁 Структура файлов

```
src/automl/
├── unified_schr_system.py    # Основная система
└── run_unified_schr.py       # CLI для запуска

docs/automl/
└── unified_schr_system.md    # Документация
```

## 🛠 Установка и запуск

### 1. Установка зависимостей:
```bash
pip install autogluon pandas numpy scikit-learn rich matplotlib seaborn
```

### 2. Запуск системы:
```bash
# Анализ по умолчанию (BTCUSD MN1)
python run_unified_schr.py

# Анализ конкретного символа
python run_unified_schr.py -s EURUSD -t D1

# Анализ конкретного файла
python run_unified_schr.py -f data/GBPUSD.parquet

# Указать путь к данным
python run_unified_schr.py --data-path data/cache/csv_converted/
```

## 📊 Результаты

Система создает:

1. **Обученные модели** в папке `models/unified_schr_production/`
2. **Детальный отчет** с метриками качества
3. **Результаты валидации** (Walk Forward, Monte Carlo, Backtest)
4. **Рекомендации** по деплою

## 🎯 Для торгового бота

Система готова для интеграции с торговым ботом:

```python
from automl.unified_schr_system import UnifiedSCHRSystem

# Загрузить обученную систему
system = UnifiedSCHRSystem()
system.load_models("models/unified_schr_production/")

# Получить предсказания для новых данных
new_data = load_latest_data()
predictions = system.predict_for_trading(new_data, "trading_signal")

# Использовать для торговли
for i, prediction in enumerate(predictions['predictions']):
    if prediction == 2:  # Strong buy
        execute_buy_order()
    elif prediction == 0:  # Strong sell
        execute_sell_order()
    # else: hold
```

## 🔧 Конфигурация

### Настройки задач:
```python
task_configs = {
    'pressure_vector_sign': {
        'problem_type': 'binary',
        'eval_metric': 'roc_auc',
        'time_limit': 1800
    },
    'price_direction_1period': {
        'problem_type': 'multiclass', 
        'eval_metric': 'accuracy',
        'time_limit': 1800
    },
    'level_breakout': {
        'problem_type': 'multiclass',
        'eval_metric': 'accuracy', 
        'time_limit': 2400
    },
    'trading_signal': {
        'problem_type': 'multiclass',
        'eval_metric': 'accuracy',
        'time_limit': 2000
    }
}
```

### Настройки валидации:
- **Walk Forward**: 5 folds
- **Monte Carlo**: 100 итераций
- **Backtesting**: автоматический расчет метрик

## 📈 Метрики качества

### Основные метрики:
- **Accuracy** - общая точность
- **Precision** - точность по классам
- **Recall** - полнота по классам
- **F1-Score** - гармоническое среднее

### Торговые метрики:
- **Total Return** - общая доходность
- **Sharpe Ratio** - коэффициент Шарпа
- **Max Drawdown** - максимальная просадка
- **Stability Score** - оценка стабильности

## 🚀 Деплой

### 1. **Подготовка к продакшену:**
```bash
# Обучить модели
python run_unified_schr.py -s BTCUSD -t H1

# Проверить качество
# Accuracy > 0.6, Stability > 0.7, Sharpe > 1.0
```

### 2. **Интеграция с ботом:**
```python
# Загрузить систему
system = UnifiedSCHRSystem()
system.load_models("models/unified_schr_production/")

# Получить предсказания
def get_trading_signal(data):
    result = system.predict_for_trading(data, "trading_signal")
    return result['predictions'][-1]  # Последний сигнал
```

### 3. **Мониторинг:**
- Отслеживание качества предсказаний
- Автоматическое переобучение при дрифте
- Алерты при снижении производительности

## 🔄 Обновления

### Автоматическое переобучение:
```python
# Проверить дрифт данных
drift_results = system.monitor_drift(new_data)

# Переобучить при необходимости
if drift_results['drift_detected']:
    system.retrain_models(new_data, target_column)
```

## 📝 Логи

Все операции логируются в:
- `logs/unified_schr_system.log` - основной лог
- `logs/schr_levels_automl.log` - детальные логи AutoGluon

## 🎯 Рекомендации

### Для максимальной прибыльности:
1. **Используйте multiple timeframes** - комбинируйте H1, H4, D1
2. **Регулярно переобучайте** - каждую неделю/месяц
3. **Мониторьте качество** - отслеживайте метрики в реальном времени
4. **Тестируйте на демо** - перед использованием реальных денег

### Для робастности:
1. **Walk Forward валидация** - обязательна для временных рядов
2. **Monte Carlo** - проверка стабильности
3. **Backtesting** - тестирование торговой стратегии
4. **Risk management** - управление рисками

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи в `logs/`
2. Убедитесь в наличии данных в `data/cache/csv_converted/`
3. Проверьте установку AutoGluon
4. Обратитесь к документации AutoGluon

---

**Создано:** NeoZork HLDP  
**Версия:** 1.0  
**Дата:** 2024
