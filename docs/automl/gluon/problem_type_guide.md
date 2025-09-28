# Problem Type Guide / Руководство по типам задач
# AutoGluon Trading Strategy Pipeline

## 🎯 **Problem Types / Типы задач**

### **1. Regression (Регрессия)**
- **Цель**: Предсказать непрерывное числовое значение
- **Примеры**: Цена акции, процентное изменение, волатильность
- **Выход**: Число (например, 0.023, -0.015, 0.045)
- **Метрики**: MSE, MAE, R²
- **Использование**: `--problem-type regression`

```bash
# Пример использования
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type regression \
    --quick
```

### **2. Binary Classification (Бинарная классификация)**
- **Цель**: Предсказать направление движения цены
- **Примеры**: Вверх/вниз, покупка/продажа
- **Выход**: 0 или 1 (0=вниз, 1=вверх)
- **Метрики**: Accuracy, Precision, Recall, F1
- **Использование**: `--problem-type binary`

```bash
# Пример использования
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type binary \
    --quick
```

### **3. Multiclass Classification (Многоклассовая классификация)**
- **Цель**: Предсказать категорию движения
- **Примеры**: Вниз/боковик/вверх, сильный/слабый/нейтральный
- **Выход**: 0, 1, 2 (0=вниз, 1=боковик, 2=вверх)
- **Метрики**: Accuracy, Precision, Recall, F1
- **Использование**: `--problem-type multiclass`

```bash
# Пример использования
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type multiclass \
    --quick
```

## 🔧 **Target Variable Creation / Создание целевой переменной**

### **Regression (Регрессия)**
```python
# Целевая переменная: процентное изменение цены
target = data['Close'].pct_change()
# Результат: [-0.023, 0.015, 0.045, ...]
```

### **Binary Classification (Бинарная классификация)**
```python
# Целевая переменная: направление движения
target = (data['Close'].diff() > 0).astype(int)
# Результат: [0, 1, 0, 1, ...] (0=вниз, 1=вверх)
```

### **Multiclass Classification (Многоклассовая классификация)**
```python
# Целевая переменная: категория движения
price_change = data['Close'].pct_change()
target = pd.cut(price_change, 
               bins=[-np.inf, -0.01, 0.01, np.inf], 
               labels=[0, 1, 2]).astype(int)
# Результат: [0, 1, 2, ...] (0=вниз, 1=боковик, 2=вверх)
```

## 📊 **Model Performance / Производительность модели**

### **Regression Metrics**
- **MSE (Mean Squared Error)**: Среднеквадратичная ошибка
- **MAE (Mean Absolute Error)**: Средняя абсолютная ошибка
- **R² (R-squared)**: Коэффициент детерминации

### **Classification Metrics**
- **Accuracy**: Точность классификации
- **Precision**: Точность (доля правильных положительных предсказаний)
- **Recall**: Полнота (доля найденных положительных случаев)
- **F1-Score**: Гармоническое среднее точности и полноты

## 🚀 **Quick Start Examples / Быстрые примеры**

### **1. Price Direction Prediction (Предсказание направления цены)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type binary \
    --quick
```

### **2. Price Change Prediction (Предсказание изменения цены)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type regression \
    --quick
```

### **3. Market Movement Categories (Категории движения рынка)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type multiclass \
    --quick
```

## 🔍 **Advanced Usage / Продвинутое использование**

### **Multiple Timeframes (Несколько таймфреймов)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes ALL \
    --problem-type binary \
    --quick
```

### **Specific Indicator (Конкретный индикатор)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --indicator WAVE2 \
    --timeframes D1 \
    --problem-type binary \
    --quick
```

### **Auto Feature Generation (Автоматическая генерация признаков)**
```bash
uv run python examples/automl/gluon/improved_demo.py \
    --symbol BTCUSD \
    --timeframes D1 \
    --problem-type regression \
    --quick
```

## 📈 **Results Interpretation / Интерпретация результатов**

### **Regression Results**
- **MSE < 0.01**: Отличная точность
- **R² > 0.8**: Хорошая объясняющая способность
- **MAE < 0.005**: Низкая средняя ошибка

### **Classification Results**
- **Accuracy > 0.6**: Хорошая точность для финансовых данных
- **F1-Score > 0.7**: Сбалансированная производительность
- **Precision > 0.6**: Низкий уровень ложных срабатываний

## ⚠️ **Important Notes / Важные замечания**

1. **Data Quality**: Убедитесь в качестве данных
2. **Feature Engineering**: Используйте релевантные признаки
3. **Time Series Split**: Правильно разделяйте данные по времени
4. **Model Validation**: Валидируйте на невидимых данных
5. **Risk Management**: Учитывайте риски в торговых стратегиях

## 🎯 **Best Practices / Лучшие практики**

1. **Start with Binary**: Начните с бинарной классификации
2. **Use Multiple Timeframes**: Используйте несколько таймфреймов
3. **Feature Engineering**: Создавайте качественные признаки
4. **Backtesting**: Тестируйте на исторических данных
5. **Risk Management**: Управляйте рисками

## 📚 **Further Reading / Дополнительное чтение**

- [AutoGluon Documentation](https://auto.gluon.ai/)
- [Time Series Forecasting](https://auto.gluon.ai/tutorials/timeseries/)
- [Tabular Prediction](https://auto.gluon.ai/tutorials/tabular_prediction/)
- [Model Selection](https://auto.gluon.ai/tutorials/model_selection/)
