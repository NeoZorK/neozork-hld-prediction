# Примеры использования AutoML Gluon

**Автор:** Shcherbyna Rostyslav  
**Дата:** 2024  

## Почему примеры критически важны

**Почему 90% разработчиков начинают с примеров, а не с документации?** Потому что примеры показывают, как теория работает на практике. Это как обучение вождению - сначала смотришь, как ездят другие.

### Проблемы без практических примеров
- **Долгое изучение**: Месяцы на понимание базовых концепций
- **Ошибки в реализации**: Неправильное использование API
- **Неэффективные решения**: Изобретение велосипеда
- **Разочарование**: Сложность отпугивает новичков

### Преимущества хороших примеров
- **Быстрое старт**: От идеи до работающего кода за часы
- **Правильные паттерны**: Изучение лучших практик на примерах
- **Уверенность**: Понимание того, как все работает
- **Вдохновение**: Идеи для собственных проектов

## Введение в примеры

<img src="images/optimized/monte_carlo_analysis.png" alt="Monte Carlo анализ" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 8.1: Monte Carlo анализ - робастные vs переобученные системы, распределение прибыли, risk-return профиль*

**Почему примеры - это язык машинного обучения?** Потому что они переводят сложные алгоритмы в понятные числа. Это как переводчик между техническими деталями и бизнес-результатами.

**Типы примеров в AutoML Gluon:**
- **Базовые примеры**: Простые задачи для понимания основ
- **Продвинутые примеры**: Сложные сценарии для опытных пользователей
- **Реальные проекты**: Полные решения реальных бизнес-задач
- **Специализированные примеры**: Для конкретных доменов (медицина, финансы)

В этом разделе представлены практические примеры использования AutoML Gluon для различных задач машинного обучения. Каждый пример включает полный код, объяснения и лучшие практики.

## Пример 1: Классификация клиентов банка

**Почему начинаем с банковской задачи?** Потому что это классический пример ML в финансах - понятный, важный и с четкими бизнес-метриками.

### Задача
**Почему предсказание дефолта так важно?** Потому что неправильное решение может стоить банку миллионы долларов. Это как медицинская диагностика, но для денег.

Предсказание вероятности дефолта клиента банка на основе финансовых показателей.

**Бизнес-контекст:**
- **Цель**: Минимизировать потери от плохих кредитов
- **Метрика**: ROC-AUC (важнее точность для положительных случаев)
- **Стоимость ошибки**: Ложный отрицательный результат дороже ложного положительного
- **Объем данных**: Обычно 100K-1M записей

### Данные
**Почему используем синтетические данные?** Потому что реальные банковские данные конфиденциальны, но структура и паттерны остаются теми же.

```python
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

# Создание синтетических данных для банковской задачи
def create_bank_data(n_samples=10000):
    """Создание синтетических банковских данных - имитация реальных банковских данных"""
    
    # Генерация данных с реалистичными параметрами
    X, y = make_classification(
        n_samples=n_samples,        # Размер выборки
        n_features=20,             # Количество признаков
        n_informative=15,          # Информативные признаки (важные для предсказания)
        n_redundant=5,             # Избыточные признаки (коррелированные)
        n_classes=2,               # Бинарная классификация (дефолт/не дефолт)
        random_state=42            # Воспроизводимость результатов
    )
    
    # Создание DataFrame с осмысленными названиями
    feature_names = [
        'age', 'income', 'credit_score', 'debt_ratio', 'employment_years',
        'loan_amount', 'interest_rate', 'payment_history', 'savings_balance',
        'investment_value', 'credit_cards', 'late_payments', 'bankruptcies',
        'foreclosures', 'collections', 'inquiries', 'credit_utilization',
        'account_age', 'payment_frequency', 'credit_mix'
    ]
    
    data = pd.DataFrame(X, columns=feature_names)
    data['default_risk'] = y
    
    # Добавление категориальных переменных
    data['employment_status'] = np.random.choice(['employed', 'unemployed', 'self_employed'], n_samples)
    data['education'] = np.random.choice(['high_school', 'bachelor', 'master', 'phd'], n_samples)
    data['marital_status'] = np.random.choice(['single', 'married', 'divorced'], n_samples)
    
    # Добавление временных переменных
    data['application_date'] = pd.date_range('2020-01-01', periods=n_samples, freq='D')
    
    return data

# Создание данных
bank_data = create_bank_data(10000)
print("Bank data shape:", bank_data.shape)
print("Default rate:", bank_data['default_risk'].mean())
```

### Подготовка данных
```python
def prepare_bank_data(data):
    """Подготовка банковских данных"""
    
    # Обработка пропущенных значений
    data = data.fillna(data.median())
    
    # Создание новых признаков
    data['debt_to_income'] = data['debt_ratio'] * data['income']
    data['credit_utilization_ratio'] = data['credit_utilization'] / (data['credit_score'] + 1)
    data['payment_stability'] = data['payment_history'] / (data['late_payments'] + 1)
    
    # Обработка выбросов
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'default_risk':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
            data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])
    
    return data

# Подготовка данных
bank_data_processed = prepare_bank_data(bank_data)
```

### Обучение модели
```python
def train_bank_model(data):
    """Обучение модели для банковской задачи"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['default_risk'])
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='default_risk',
        problem_type='binary',
        eval_metric='roc_auc',
        path='./bank_models'
    )
    
    # Настройка гиперпараметров для банковской задачи
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'CAT': [
            {
                'iterations': 200,
                'learning_rate': 0.1,
                'depth': 6,
                'l2_leaf_reg': 3.0
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
bank_predictor, bank_test_data = train_bank_model(bank_data_processed)
```

### Оценка качества
```python
def evaluate_bank_model(predictor, test_data):
    """Оценка качества банковской модели"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    probabilities = predictor.predict_proba(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'probabilities': probabilities
    }

# Оценка модели
bank_results = evaluate_bank_model(bank_predictor, bank_test_data)

print("Bank Model Performance:")
for metric, value in bank_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nTop 10 Feature Importance:")
print(bank_results['feature_importance'].head(10))
```

### Визуализация результатов
```python
def visualize_bank_results(results, test_data):
    """Визуализация результатов банковской модели"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # ROC кривая
    from sklearn.metrics import roc_curve, auc
    fpr, tpr, _ = roc_curve(test_data['default_risk'], results['probabilities'][1])
    roc_auc = auc(fpr, tpr)
    
    axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
    axes[0, 0].plot([0, 1], [0, 1], 'k--')
    axes[0, 0].set_xlabel('False Positive Rate')
    axes[0, 0].set_ylabel('True Positive Rate')
    axes[0, 0].set_title('ROC Curve')
    axes[0, 0].legend()
    
    # Precision-Recall кривая
    from sklearn.metrics import precision_recall_curve
    precision, recall, _ = precision_recall_curve(test_data['default_risk'], results['probabilities'][1])
    
    axes[0, 1].plot(recall, precision)
    axes[0, 1].set_xlabel('Recall')
    axes[0, 1].set_ylabel('Precision')
    axes[0, 1].set_title('Precision-Recall Curve')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Распределение вероятностей
    axes[1, 1].hist(results['probabilities'][1], bins=50, alpha=0.7)
    axes[1, 1].set_xlabel('Default Probability')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of Default Probabilities')
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_bank_results(bank_results, bank_test_data)
```

## Пример 2: Прогнозирование цен на недвижимость

### Задача
Предсказание цены недвижимости на основе характеристик объекта.

### Данные
```python
def create_real_estate_data(n_samples=5000):
    """Создание синтетических данных о недвижимости"""
    
    np.random.seed(42)
    
    # Основные характеристики
    data = pd.DataFrame({
        'area': np.random.normal(120, 30, n_samples),
        'bedrooms': np.random.poisson(3, n_samples),
        'bathrooms': np.random.poisson(2, n_samples),
        'age': np.random.exponential(10, n_samples),
        'garage': np.random.binomial(1, 0.7, n_samples),
        'pool': np.random.binomial(1, 0.2, n_samples),
        'garden': np.random.binomial(1, 0.6, n_samples)
    })
    
    # Категориальные переменные
    data['location'] = np.random.choice(['downtown', 'suburbs', 'rural'], n_samples)
    data['property_type'] = np.random.choice(['house', 'apartment', 'townhouse'], n_samples)
    data['condition'] = np.random.choice(['excellent', 'good', 'fair', 'poor'], n_samples)
    
    # Создание целевой переменной (цена)
    base_price = 100000
    price = (base_price + 
             data['area'] * 1000 +
             data['bedrooms'] * 10000 +
             data['bathrooms'] * 5000 +
             data['garage'] * 15000 +
             data['pool'] * 25000 +
             data['garden'] * 10000 -
             data['age'] * 2000)
    
    # Добавление шума
    price += np.random.normal(0, 20000, n_samples)
    data['price'] = np.maximum(price, 50000)  # Минимальная цена
    
    return data

# Создание данных
real_estate_data = create_real_estate_data(5000)
print("Real estate data shape:", real_estate_data.shape)
print("Price statistics:")
print(real_estate_data['price'].describe())
```

### Подготовка данных
```python
def prepare_real_estate_data(data):
    """Подготовка данных о недвижимости"""
    
    # Создание новых признаков
    data['area_per_bedroom'] = data['area'] / (data['bedrooms'] + 1)
    data['total_rooms'] = data['bedrooms'] + data['bathrooms']
    data['age_category'] = pd.cut(data['age'], bins=[0, 5, 15, 30, 100], labels=['new', 'recent', 'old', 'very_old'])
    
    # Обработка выбросов
    data['area'] = np.where(data['area'] > 300, 300, data['area'])
    data['age'] = np.where(data['age'] > 50, 50, data['age'])
    
    return data

# Подготовка данных
real_estate_processed = prepare_real_estate_data(real_estate_data)
```

### Обучение модели
```python
def train_real_estate_model(data):
    """Обучение модели для недвижимости"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='price',
        problem_type='regression',
        eval_metric='rmse',
        path='./real_estate_models'
    )
    
    # Настройка гиперпараметров для регрессии
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 300,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 300,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'RF': [
            {
                'n_estimators': 200,
                'max_depth': 15,
                'min_samples_split': 5,
                'min_samples_leaf': 2
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
real_estate_predictor, real_estate_test_data = train_real_estate_model(real_estate_processed)
```

### Оценка качества
```python
def evaluate_real_estate_model(predictor, test_data):
    """Оценка качества модели недвижимости"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    # Анализ ошибок
    errors = test_data['price'] - predictions
    mae = np.mean(np.abs(errors))
    mape = np.mean(np.abs(errors / test_data['price'])) * 100
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'mae': mae,
        'mape': mape,
        'errors': errors
    }

# Оценка модели
real_estate_results = evaluate_real_estate_model(real_estate_predictor, real_estate_test_data)

print("Real Estate Model Performance:")
for metric, value in real_estate_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print(f"\nMAE: {real_estate_results['mae']:.2f}")
print(f"MAPE: {real_estate_results['mape']:.2f}%")
```

### Визуализация результатов
```python
def visualize_real_estate_results(results, test_data):
    """Визуализация результатов модели недвижимости"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Предсказания vs Фактические значения
    axes[0, 0].scatter(test_data['price'], results['predictions'], alpha=0.6)
    axes[0, 0].plot([test_data['price'].min(), test_data['price'].max()], 
                   [test_data['price'].min(), test_data['price'].max()], 'r--')
    axes[0, 0].set_xlabel('Actual Price')
    axes[0, 0].set_ylabel('Predicted Price')
    axes[0, 0].set_title('Predictions vs Actual')
    
    # Распределение ошибок
    axes[0, 1].hist(results['errors'], bins=50, alpha=0.7)
    axes[0, 1].set_xlabel('Prediction Error')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Prediction Errors')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Ошибки по цене
    axes[1, 1].scatter(test_data['price'], results['errors'], alpha=0.6)
    axes[1, 1].set_xlabel('Actual Price')
    axes[1, 1].set_ylabel('Prediction Error')
    axes[1, 1].set_title('Errors by Price Range')
    axes[1, 1].axhline(y=0, color='r', linestyle='--')
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_real_estate_results(real_estate_results, real_estate_test_data)
```

## Пример 3: Анализ временных рядов

### Задача
Прогнозирование продаж товаров на основе исторических данных.

### Данные
```python
def create_sales_data(n_days=365, n_products=10):
    """Создание синтетических данных о продажах"""
    
    np.random.seed(42)
    
    # Создание временного ряда
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    data = []
    for product_id in range(n_products):
        # Базовый тренд
        trend = np.linspace(100, 150, n_days)
        
        # Сезонность (еженедельная)
        seasonality = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)
        
        # Случайный шум
        noise = np.random.normal(0, 10, n_days)
        
        # Продажи
        sales = trend + seasonality + noise
        sales = np.maximum(sales, 0)  # Негативные продажи невозможны
        
        # Создание записей
        for i, (date, sale) in enumerate(zip(dates, sales)):
            data.append({
                'date': date,
                'product_id': f'product_{product_id}',
                'sales': sale,
                'day_of_week': date.dayofweek,
                'month': date.month,
                'quarter': date.quarter
            })
    
    return pd.DataFrame(data)

# Создание данных
sales_data = create_sales_data(365, 10)
print("Sales data shape:", sales_data.shape)
print("Sales statistics:")
print(sales_data['sales'].describe())
```

### Подготовка данных для временных рядов
```python
def prepare_sales_data(data):
    """Подготовка данных о продажах для временных рядов"""
    
    # Создание лаговых признаков
    data = data.sort_values(['product_id', 'date'])
    
    for lag in [1, 2, 3, 7, 14, 30]:
        data[f'sales_lag_{lag}'] = data.groupby('product_id')['sales'].shift(lag)
    
    # Скользящие средние
    for window in [7, 14, 30]:
        data[f'sales_ma_{window}'] = data.groupby('product_id')['sales'].rolling(window=window).mean().reset_index(0, drop=True)
    
    # Тренды
    data['sales_trend'] = data.groupby('product_id')['sales'].rolling(window=7).mean().reset_index(0, drop=True)
    
    # Сезонные признаки
    data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)
    data['is_month_start'] = (data['date'].dt.day <= 7).astype(int)
    data['is_month_end'] = (data['date'].dt.day >= 25).astype(int)
    
    return data

# Подготовка данных
sales_processed = prepare_sales_data(sales_data)
```

### Обучение модели временных рядов
```python
def train_sales_model(data):
    """Обучение модели для прогнозирования продаж"""
    
    # Разделение на train/test (последние 30 дней для теста)
    split_date = data['date'].max() - pd.Timedelta(days=30)
    train_data = data[data['date'] <= split_date]
    test_data = data[data['date'] > split_date]
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='sales',
        problem_type='regression',
        eval_metric='rmse',
        path='./sales_models'
    )
    
    # Настройка гиперпараметров для временных рядов
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=3,  # Меньше фолдов для временных рядов
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
sales_predictor, sales_test_data = train_sales_model(sales_processed)
```

### Оценка качества временных рядов
```python
def evaluate_sales_model(predictor, test_data):
    """Оценка качества модели продаж"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Анализ по продуктам
    product_performance = {}
    for product_id in test_data['product_id'].unique():
        product_data = test_data[test_data['product_id'] == product_id]
        product_predictions = predictions[test_data['product_id'] == product_id]
        
        mae = np.mean(np.abs(product_data['sales'] - product_predictions))
        mape = np.mean(np.abs((product_data['sales'] - product_predictions) / product_data['sales'])) * 100
        
        product_performance[product_id] = {
            'mae': mae,
            'mape': mape
        }
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'product_performance': product_performance,
        'predictions': predictions
    }

# Оценка модели
sales_results = evaluate_sales_model(sales_predictor, sales_test_data)

print("Sales Model Performance:")
for metric, value in sales_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nProduct Performance:")
for product, perf in sales_results['product_performance'].items():
    print(f"{product}: MAE={perf['mae']:.2f}, MAPE={perf['mape']:.2f}%")
```

### Визуализация временных рядов
```python
def visualize_sales_results(results, test_data):
    """Визуализация результатов модели продаж"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Временной ряд для одного продукта
    product_id = test_data['product_id'].iloc[0]
    product_data = test_data[test_data['product_id'] == product_id]
    product_predictions = results['predictions'][test_data['product_id'] == product_id]
    
    axes[0, 0].plot(product_data['date'], product_data['sales'], label='Actual', alpha=0.7)
    axes[0, 0].plot(product_data['date'], product_predictions, label='Predicted', alpha=0.7)
    axes[0, 0].set_title(f'Sales Forecast for {product_id}')
    axes[0, 0].set_xlabel('Date')
    axes[0, 0].set_ylabel('Sales')
    axes[0, 0].legend()
    
    # Распределение ошибок
    errors = test_data['sales'] - results['predictions']
    axes[0, 1].hist(errors, bins=30, alpha=0.7)
    axes[0, 1].set_xlabel('Prediction Error')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Prediction Errors')
    
    # Важность признаков
    results['feature_importance'].head(10).plot(kind='barh', ax=axes[1, 0])
    axes[1, 0].set_title('Top 10 Feature Importance')
    
    # Производительность по продуктам
    products = list(results['product_performance'].keys())
    maes = [results['product_performance'][p]['mae'] for p in products]
    
    axes[1, 1].bar(products, maes)
    axes[1, 1].set_xlabel('Product')
    axes[1, 1].set_ylabel('MAE')
    axes[1, 1].set_title('Performance by Product')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_sales_results(sales_results, sales_test_data)
```

## Пример 4: Многоклассовая классификация

### Задача
Классификация изображений на основе извлеченных признаков.

### Данные
```python
def create_image_data(n_samples=5000, n_features=100):
    """Создание синтетических данных изображений"""
    
    np.random.seed(42)
    
    # Создание признаков изображений
    features = np.random.randn(n_samples, n_features)
    
    # Создание целевых классов
    n_classes = 5
    classes = ['cat', 'dog', 'bird', 'car', 'tree']
    y = np.random.choice(n_classes, n_samples)
    
    # Создание DataFrame
    feature_names = [f'feature_{i}' for i in range(n_features)]
    data = pd.DataFrame(features, columns=feature_names)
    data['class'] = [classes[i] for i in y]
    
    # Добавление метаданных
    data['image_size'] = np.random.choice(['small', 'medium', 'large'], n_samples)
    data['color_channels'] = np.random.choice([1, 3], n_samples)
    data['resolution'] = np.random.choice(['low', 'medium', 'high'], n_samples)
    
    return data

# Создание данных
image_data = create_image_data(5000, 100)
print("Image data shape:", image_data.shape)
print("Class distribution:")
print(image_data['class'].value_counts())
```

### Подготовка данных
```python
def prepare_image_data(data):
    """Подготовка данных изображений"""
    
    # Создание новых признаков
    data['feature_sum'] = data.select_dtypes(include=[np.number]).sum(axis=1)
    data['feature_mean'] = data.select_dtypes(include=[np.number]).mean(axis=1)
    data['feature_std'] = data.select_dtypes(include=[np.number]).std(axis=1)
    
    # Нормализация признаков
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'color_channels':
            data[col] = (data[col] - data[col].mean()) / data[col].std()
    
    return data

# Подготовка данных
image_processed = prepare_image_data(image_data)
```

### Обучение модели
```python
def train_image_model(data):
    """Обучение модели для классификации изображений"""
    
    # Разделение на train/test
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42, stratify=data['class'])
    
    # Создание предиктора
    predictor = TabularPredictor(
        label='class',
        problem_type='multiclass',
        eval_metric='accuracy',
        path='./image_models'
    )
    
    # Настройка гиперпараметров для многоклассовой классификации
    hyperparameters = {
        'GBM': [
            {
                'num_boost_round': 200,
                'learning_rate': 0.1,
                'num_leaves': 31,
                'feature_fraction': 0.9,
                'bagging_fraction': 0.8,
                'min_data_in_leaf': 20
            }
        ],
        'XGB': [
            {
                'n_estimators': 200,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8,
                'colsample_bytree': 0.8
            }
        ],
        'RF': [
            {
                'n_estimators': 200,
                'max_depth': 15,
                'min_samples_split': 5,
                'min_samples_leaf': 2
            }
        ]
    }
    
    # Обучение модели
    predictor.fit(
        train_data,
        hyperparameters=hyperparameters,
        time_limit=1800,  # 30 минут
        presets='high_quality',
        num_bag_folds=5,
        num_bag_sets=1
    )
    
    return predictor, test_data

# Обучение модели
image_predictor, image_test_data = train_image_model(image_processed)
```

### Оценка качества
```python
def evaluate_image_model(predictor, test_data):
    """Оценка качества модели классификации изображений"""
    
    # Предсказания
    predictions = predictor.predict(test_data)
    probabilities = predictor.predict_proba(test_data)
    
    # Оценка качества
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    leaderboard = predictor.leaderboard(test_data)
    
    # Анализ по классам
    from sklearn.metrics import classification_report, confusion_matrix
    
    class_report = classification_report(test_data['class'], predictions, output_dict=True)
    conf_matrix = confusion_matrix(test_data['class'], predictions)
    
    return {
        'performance': performance,
        'feature_importance': feature_importance,
        'leaderboard': leaderboard,
        'predictions': predictions,
        'probabilities': probabilities,
        'classification_report': class_report,
        'confusion_matrix': conf_matrix
    }

# Оценка модели
image_results = evaluate_image_model(image_predictor, image_test_data)

print("Image Model Performance:")
for metric, value in image_results['performance'].items():
    print(f"{metric}: {value:.4f}")

print("\nClassification Report:")
for class_name, metrics in image_results['classification_report'].items():
    if isinstance(metrics, dict):
        print(f"{class_name}: {metrics}")
```

### Визуализация результатов
```python
def visualize_image_results(results, test_data):
    """Визуализация результатов модели классификации изображений"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Матрица ошибок
    import seaborn as sns
    sns.heatmap(results['confusion_matrix'], annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Confusion Matrix')
    axes[0, 0].set_xlabel('Predicted')
    axes[0, 0].set_ylabel('Actual')
    
    # Важность признаков
    results['feature_importance'].head(15).plot(kind='barh', ax=axes[0, 1])
    axes[0, 1].set_title('Top 15 Feature Importance')
    
    # Распределение предсказаний
    prediction_counts = pd.Series(results['predictions']).value_counts()
    prediction_counts.plot(kind='bar', ax=axes[1, 0])
    axes[1, 0].set_title('Distribution of Predictions')
    axes[1, 0].set_xlabel('Class')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Точность по классам
    class_accuracy = []
    for class_name in test_data['class'].unique():
        class_data = test_data[test_data['class'] == class_name]
        class_predictions = results['predictions'][test_data['class'] == class_name]
        accuracy = (class_data['class'] == class_predictions).mean()
        class_accuracy.append(accuracy)
    
    axes[1, 1].bar(test_data['class'].unique(), class_accuracy)
    axes[1, 1].set_title('Accuracy by Class')
    axes[1, 1].set_xlabel('Class')
    axes[1, 1].set_ylabel('Accuracy')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# Визуализация
visualize_image_results(image_results, image_test_data)
```

## Пример 5: Продакшен система

### Полная продакшен система
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from autogluon.tabular import TabularPredictor
import logging
from datetime import datetime
from typing import Dict, List, Any
import asyncio
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(title="AutoML Gluon Production API", version="1.0.0")

# Глобальные переменные
models = {}
model_metadata = {}

class PredictionRequest(BaseModel):
    model_name: str
    data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class ModelInfo(BaseModel):
    model_name: str
    model_type: str
    performance: Dict[str, float]
    features: List[str]
    created_at: str

@app.on_event("startup")
async def load_models():
    """Загрузка моделей при запуске"""
    global models, model_metadata
    
    # Загрузка банковской модели
    try:
        models['bank_default'] = TabularPredictor.load('./bank_models')
        model_metadata['bank_default'] = {
            'model_type': 'binary_classification',
            'target': 'default_risk',
            'features': ['age', 'income', 'credit_score', 'debt_ratio', 'employment_years']
        }
        logger.info("Bank model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load bank model: {e}")
    
    # Загрузка модели недвижимости
    try:
        models['real_estate'] = TabularPredictor.load('./real_estate_models')
        model_metadata['real_estate'] = {
            'model_type': 'regression',
            'target': 'price',
            'features': ['area', 'bedrooms', 'bathrooms', 'age', 'location']
        }
        logger.info("Real estate model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load real estate model: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    loaded_models = list(models.keys())
    return {
        "status": "healthy" if loaded_models else "unhealthy",
        "loaded_models": loaded_models,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Endpoint для предсказаний"""
    
    if request.model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")
    
    try:
        model = models[request.model_name]
        metadata = model_metadata[request.model_name]
        
        # Преобразование данных
        df = pd.DataFrame(request.data)
        
        # Предсказания
        predictions = model.predict(df)
        
        # Вероятности (если доступны)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities,
            model_info={
                "model_name": request.model_name,
                "model_type": metadata['model_type'],
                "target": metadata['target'],
                "features": metadata['features']
            },
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """Список доступных моделей"""
    return {
        "models": list(models.keys()),
        "metadata": model_metadata
    }

@app.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """Информация о модели"""
    if model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
    
    model = models[model_name]
    metadata = model_metadata[model_name]
    
    return {
        "model_name": model_name,
        "model_type": metadata['model_type'],
        "target": metadata['target'],
        "features": metadata['features'],
        "performance": model.evaluate(pd.DataFrame([{f: 0 for f in metadata['features']}]))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Клиент для тестирования
```python
import requests
import json

def test_production_api():
    """Тестирование продакшен API"""
    
    base_url = "http://localhost:8000"
    
    # Health check
    response = requests.get(f"{base_url}/health")
    print("Health check:", response.json())
    
    # Список моделей
    response = requests.get(f"{base_url}/models")
    print("Available models:", response.json())
    
    # Тест банковской модели
    bank_data = {
        "model_name": "bank_default",
        "data": [
            {
                "age": 35,
                "income": 50000,
                "credit_score": 750,
                "debt_ratio": 0.3,
                "employment_years": 5
            }
        ]
    }
    
    response = requests.post(f"{base_url}/predict", json=bank_data)
    print("Bank prediction:", response.json())
    
    # Тест модели недвижимости
    real_estate_data = {
        "model_name": "real_estate",
        "data": [
            {
                "area": 120,
                "bedrooms": 3,
                "bathrooms": 2,
                "age": 10,
                "location": "downtown"
            }
        ]
    }
    
    response = requests.post(f"{base_url}/predict", json=real_estate_data)
    print("Real estate prediction:", response.json())

# Запуск тестов
if __name__ == "__main__":
    test_production_api()
```

## Следующие шаги

После изучения примеров переходите к:
- [Troubleshooting](./10_troubleshooting.md)
- [Лучшим практикам](./08_best_practices.md)
