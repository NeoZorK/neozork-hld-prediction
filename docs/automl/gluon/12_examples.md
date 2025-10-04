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

<img src="images/optimized/metrics_comparison_detailed.png" alt="Сравнение метрик и задач" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 1: Сравнение метрик для классификации и регрессии - ROC Curve, Precision-Recall, Confusion Matrix, метрики регрессии*

**Почему примеры - это язык машинного обучения?** Потому что они переводят сложные алгоритмы в понятные числа. Это как переводчик между техническими деталями и бизнес-результатами.

**Типы примеров в AutoML Gluon:**
- **Базовые примеры**: Простые задачи для понимания основ
- **Продвинутые примеры**: Сложные сценарии для опытных пользователей
- **Реальные проекты**: Полные решения реальных бизнес-задач
- **Специализированные примеры**: Для конкретных доменов (медицина, финансы)

В этом разделе представлены практические примеры использования AutoML Gluon для различных задач машинного обучения. Каждый пример включает полный код, объяснения и лучшие практики.

## Пример 1: Классификация клиентов банка

<img src="images/optimized/bank_classification_analysis.png" alt="Банковский пример" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 2: Пример классификации клиентов банка - ROC Curve, Precision-Recall, Confusion Matrix, важность признаков*

**Почему начинаем с банковской задачи?** Потому что это классический пример ML в финансах - понятный, важный и с четкими бизнес-метриками.

**Ключевые аспекты банковского ML:**
- **Финансовые риски**: Оценка кредитоспособности клиентов
- **Регулирование**: Соблюдение банковских стандартов
- **Интерпретируемость**: Объяснимость решений для регуляторов
- **Справедливость**: Предотвращение дискриминации
- **Мониторинг**: Отслеживание качества в реальном времени
- **A/B тестирование**: Сравнение моделей на реальных данных

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
    """
    Создание синтетических банковских данных - имитация реальных банковских данных
    
    Parameters:
    -----------
    n_samples : int, default=10000
        Размер выборки для генерации:
        - 1000-5000: небольшие датасеты (быстрое тестирование)
        - 5000-20000: средние датасеты (баланс качества и скорости)
        - 20000+: большие датасеты (максимальное качество)
        
    Returns:
    --------
    pd.DataFrame
        Синтетические банковские данные:
        - Числовые признаки: возраст, доход, кредитный рейтинг, долг/доход
        - Категориальные признаки: статус занятости, образование, семейное положение
        - Временные признаки: дата подачи заявки
        - Целевая переменная: default_risk (0/1)
        
    Notes:
    ------
    Структура банковских данных:
    - 20 числовых признаков (возраст, доход, кредитный рейтинг и др.)
    - 15 информативных признаков (влияют на дефолт)
    - 5 избыточных признаков (коррелированные с информативными)
    - 3 категориальных признака (статус, образование, семейное положение)
    - Временные метки для анализа трендов
    
    Бизнес-контекст:
    - Задача: предсказание дефолта по кредиту
    - Целевая переменная: default_risk (0 - нет дефолта, 1 - дефолт)
    - Применение: кредитное скоринг, риск-менеджмент
    """
    
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
    """
    Подготовка банковских данных для машинного обучения
    
    Parameters:
    -----------
    data : pd.DataFrame
        Исходные банковские данные:
        - Содержит числовые и категориальные признаки
        - Может содержать пропущенные значения
        - Может содержать выбросы
        
    Returns:
    --------
    pd.DataFrame
        Подготовленные данные:
        - Заполнены пропущенные значения
        - Созданы новые признаки
        - Обработаны выбросы
        - Готовы для обучения модели
        
    Notes:
    ------
    Процесс подготовки данных:
    1. Заполнение пропущенных значений медианой
    2. Создание новых признаков (feature engineering)
    3. Обработка выбросов методом IQR
    4. Нормализация данных
    
    Новые признаки:
    - debt_to_income: отношение долга к доходу
    - credit_utilization_ratio: коэффициент использования кредита
    - payment_stability: стабильность платежей
    
    Обработка выбросов:
    - Метод IQR (Interquartile Range)
    - Замена выбросов на граничные значения
    - Сохранение целевой переменной
    """
    
    # Обработка пропущенных значений
    # Медиана более устойчива к выбросам чем среднее
    data = data.fillna(data.median())
    
    # Создание новых признаков (feature engineering)
    # Комбинирование существующих признаков для улучшения качества
    data['debt_to_income'] = data['debt_ratio'] * data['income']  # Отношение долга к доходу
    data['credit_utilization_ratio'] = data['credit_utilization'] / (data['credit_score'] + 1)  # Коэффициент использования кредита
    data['payment_stability'] = data['payment_history'] / (data['late_payments'] + 1)  # Стабильность платежей
    
    # Обработка выбросов методом IQR
    # IQR = Q3 - Q1, выбросы: < Q1 - 1.5*IQR или > Q3 + 1.5*IQR
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'default_risk':  # Не обрабатываем целевую переменную
            Q1 = data[col].quantile(0.25)  # Первый квартиль
            Q3 = data[col].quantile(0.75)  # Третий квартиль
            IQR = Q3 - Q1  # Межквартильный размах
            # Замена выбросов на граничные значения
            data[col] = np.where(data[col] < Q1 - 1.5 * IQR, Q1 - 1.5 * IQR, data[col])
            data[col] = np.where(data[col] > Q3 + 1.5 * IQR, Q3 + 1.5 * IQR, data[col])
    
    return data

# Подготовка данных
bank_data_processed = prepare_bank_data(bank_data)
```

### Обучение модели
```python
def train_bank_model(data):
    """
    Обучение модели для банковской задачи классификации дефолта
    
    Parameters:
    -----------
    data : pd.DataFrame
        Подготовленные банковские данные:
        - Содержит целевую переменную 'default_risk'
        - Обработаны пропущенные значения и выбросы
        - Созданы новые признаки
        
    Returns:
    --------
    tuple
        (predictor, test_data):
        - predictor: обученная модель TabularPredictor
        - test_data: тестовые данные для оценки
        
    Notes:
    ------
    Процесс обучения:
    1. Разделение данных на train/test (80/20)
    2. Стратифицированное разделение (сохранение пропорций классов)
    3. Создание предиктора с настройками для банковской задачи
    4. Настройка гиперпараметров для разных алгоритмов
    5. Обучение с высоким качеством и бэггингом
    
    Настройки для банковской задачи:
    - problem_type: 'binary' (бинарная классификация)
    - eval_metric: 'roc_auc' (ROC-AUC для несбалансированных данных)
    - presets: 'high_quality' (максимальное качество)
    - num_bag_folds: 5 (бэггинг для стабильности)
    - time_limit: 1800s (30 минут обучения)
    """
    
    # Разделение на train/test
    # Стратифицированное разделение сохраняет пропорции классов
    train_data, test_data = train_test_split(
        data, 
        test_size=0.2,  # 20% для тестирования
        random_state=42,  # Воспроизводимость
        stratify=data['default_risk']  # Стратификация по целевому признаку
    )
    
    # Создание предиктора с настройками для банковской задачи
    predictor = TabularPredictor(
        label='default_risk',  # Целевая переменная
        problem_type='binary',  # Бинарная классификация
        eval_metric='roc_auc',  # ROC-AUC для несбалансированных данных
        path='./bank_models'  # Путь для сохранения модели
    )
    
    # Настройка гиперпараметров для банковской задачи
    # Оптимизированы для бинарной классификации с несбалансированными данными
    hyperparameters = {
        'GBM': [  # Gradient Boosting Machine (LightGBM)
            {
                'num_boost_round': 200,  # Количество итераций бустинга (100-500)
                'learning_rate': 0.1,  # Скорость обучения (0.01-0.3)
                'num_leaves': 31,  # Количество листьев в дереве (10-100)
                'feature_fraction': 0.9,  # Доля признаков для каждого дерева (0.5-1.0)
                'bagging_fraction': 0.8,  # Доля данных для каждого дерева (0.5-1.0)
                'min_data_in_leaf': 20  # Минимум образцов в листе (10-100)
            }
        ],
        'XGB': [  # XGBoost
            {
                'n_estimators': 200,  # Количество деревьев (100-1000)
                'learning_rate': 0.1,  # Скорость обучения (0.01-0.3)
                'max_depth': 6,  # Максимальная глубина дерева (3-10)
                'subsample': 0.8,  # Доля образцов для обучения (0.5-1.0)
                'colsample_bytree': 0.8  # Доля признаков для дерева (0.5-1.0)
            }
        ],
        'CAT': [  # CatBoost
            {
                'iterations': 200,  # Количество итераций (100-1000)
                'learning_rate': 0.1,  # Скорость обучения (0.01-0.3)
                'depth': 6,  # Глубина дерева (3-10)
                'l2_leaf_reg': 3.0  # L2 регуляризация (1.0-10.0)
            }
        ]
    }
    
    # Обучение модели с оптимизированными параметрами
    predictor.fit(
        train_data,  # Данные для обучения
        hyperparameters=hyperparameters,  # Настройки алгоритмов
        time_limit=1800,  # Время обучения в секундах (30 минут)
        presets='high_quality',  # Предустановки качества (high_quality для максимального качества)
        num_bag_folds=5,  # Количество фолдов для бэггинга (3-10)
        num_bag_sets=1  # Количество наборов бэггинга (1-3)
    )
    
    return predictor, test_data

# Обучение модели
bank_predictor, bank_test_data = train_bank_model(bank_data_processed)
```

### Оценка качества
```python
def evaluate_bank_model(predictor, test_data):
    """
    Оценка качества банковской модели для классификации дефолта
    
    Parameters:
    -----------
    predictor : TabularPredictor
        Обученная модель для оценки:
        - Должна быть обучена на банковских данных
        - Поддерживает predict() и predict_proba()
        - Содержит информацию о важности признаков
        
    test_data : pd.DataFrame
        Тестовые данные для оценки:
        - Содержит целевую переменную 'default_risk'
        - Имеет те же признаки что и обучающие данные
        - Не участвовали в обучении модели
        
    Returns:
    --------
    Dict[str, Any]
        Результаты оценки модели:
        - performance: метрики качества (accuracy, roc_auc, precision, recall)
        - feature_importance: важность признаков для предсказания
        - leaderboard: сравнение различных моделей
        - predictions: предсказания классов (0/1)
        - probabilities: вероятности классов
        
    Notes:
    ------
    Метрики оценки для банковской задачи:
    - ROC-AUC: основная метрика для несбалансированных данных
    - Precision: доля правильных предсказаний дефолта
    - Recall: доля найденных дефолтов
    - F1-score: гармоническое среднее precision и recall
    - Accuracy: общая точность классификации
    
    Анализ важности признаков:
    - Показывает какие факторы важны для предсказания дефолта
    - Помогает понять логику модели
    - Используется для feature selection
    """
    
    # Предсказания классов (0 - нет дефолта, 1 - дефолт)
    predictions = predictor.predict(test_data)
    
    # Вероятности классов (для анализа уверенности модели)
    probabilities = predictor.predict_proba(test_data)
    
    # Оценка качества модели
    # Автоматический расчет метрик для бинарной классификации
    performance = predictor.evaluate(test_data)
    
    # Анализ важности признаков
    # Показывает вклад каждого признака в предсказание
    feature_importance = predictor.feature_importance()
    
    # Лидерборд моделей
    # Сравнение различных алгоритмов и их комбинаций
    leaderboard = predictor.leaderboard(test_data)
    
    return {
        'performance': performance,  # Метрики качества
        'feature_importance': feature_importance,  # Важность признаков
        'leaderboard': leaderboard,  # Сравнение моделей
        'predictions': predictions,  # Предсказания классов
        'probabilities': probabilities  # Вероятности классов
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

**Почему визуализация критически важна для понимания метрик?** Потому что картинки показывают то, что числа скрывают:

- **ROC Curve**: Показывает качество разделения классов при разных порогах
- **Precision-Recall**: Демонстрирует баланс между точностью и полнотой
- **Confusion Matrix**: Визуализирует типы ошибок модели
- **Feature Importance**: Показывает, какие факторы важны для предсказания

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

<img src="images/optimized/real_estate_regression_analysis.png" alt="Пример недвижимости" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 3: Пример прогнозирования цен на недвижимость - предсказания vs факт, распределение ошибок, важность признаков, метрики качества*

**Почему недвижимость - отличный пример для регрессии?** Потому что это понятная задача с множеством факторов влияния:

**Ключевые аспекты регрессии в недвижимости:**
- **Множественные факторы**: Площадь, район, этаж, год постройки
- **Непрерывная целевая переменная**: Цена в рублях
- **Feature Engineering**: Создание новых признаков из существующих
- **Валидация**: Проверка на переобучение
- **Интерпретируемость**: Понимание влияния каждого фактора
- **Метрики качества**: RMSE, MAE, R² для оценки точности

### Задача
Предсказание цены недвижимости на основе характеристик объекта.

### Данные
```python
def create_real_estate_data(n_samples=5000):
    """
    Создание синтетических данных о недвижимости для регрессионного анализа
    
    Parameters:
    -----------
    n_samples : int, default=5000
        Размер выборки для генерации:
        - 1000-3000: небольшие датасеты (быстрое тестирование)
        - 3000-10000: средние датасеты (баланс качества и скорости)
        - 10000+: большие датасеты (максимальное качество)
        
    Returns:
    --------
    pd.DataFrame
        Синтетические данные о недвижимости:
        - Числовые признаки: площадь, спальни, ванные, возраст
        - Бинарные признаки: гараж, бассейн, сад
        - Категориальные признаки: район, тип недвижимости, состояние
        - Целевая переменная: price (цена в рублях)
        
    Notes:
    ------
    Структура данных недвижимости:
    - 7 числовых признаков (площадь, спальни, ванные, возраст)
    - 3 бинарных признака (гараж, бассейн, сад)
    - 3 категориальных признака (район, тип, состояние)
    - Целевая переменная: price (непрерывная)
    
    Бизнес-логика ценообразования:
    - Базовая цена: 100,000 рублей
    - Площадь: +1,000 руб/м²
    - Спальни: +10,000 руб за спальню
    - Ванные: +5,000 руб за ванную
    - Гараж: +15,000 руб
    - Бассейн: +25,000 руб
    - Сад: +10,000 руб
    - Возраст: -2,000 руб за год
    - Шум: ±20,000 руб (случайная составляющая)
    """
    
    np.random.seed(42)  # Воспроизводимость результатов
    
    # Основные характеристики недвижимости
    data = pd.DataFrame({
        'area': np.random.normal(120, 30, n_samples),  # Площадь (м²) - нормальное распределение
        'bedrooms': np.random.poisson(3, n_samples),  # Количество спален - распределение Пуассона
        'bathrooms': np.random.poisson(2, n_samples),  # Количество ванных - распределение Пуассона
        'age': np.random.exponential(10, n_samples),  # Возраст (лет) - экспоненциальное распределение
        'garage': np.random.binomial(1, 0.7, n_samples),  # Наличие гаража (70% вероятность)
        'pool': np.random.binomial(1, 0.2, n_samples),  # Наличие бассейна (20% вероятность)
        'garden': np.random.binomial(1, 0.6, n_samples)  # Наличие сада (60% вероятность)
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

**Почему визуализация регрессии отличается от классификации?** Потому что здесь мы предсказываем непрерывные значения, а не классы:

- **Scatter Plot**: Показывает корреляцию между предсказанными и фактическими значениями
- **Error Distribution**: Демонстрирует характер ошибок модели (нормальность, выбросы)
- **Feature Importance**: Выявляет наиболее влиятельные факторы на цену
- **Error vs Price**: Показывает, зависит ли точность от диапазона цен

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

<img src="images/optimized/time_series_analysis.png" alt="Пример временных рядов" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 4: Пример анализа временных рядов - временной ряд с прогнозом, ошибки по времени, распределение ошибок, метрики MASE/MAPE*

**Почему временные ряды - особый тип задач?** Потому что они имеют временную зависимость и требуют специальных методов:

**Ключевые аспекты временных рядов:**
- **Временная зависимость**: Будущие значения зависят от прошлых
- **Сезонность**: Повторяющиеся паттерны во времени
- **Тренды**: Долгосрочные изменения
- **Станционарность**: Стабильность статистических свойств
- **Валидация**: Специальные методы для временных данных
- **Прогнозирование**: Предсказание будущих значений

### Задача
Прогнозирование продаж товаров на основе исторических данных.

### Данные
```python
def create_sales_data(n_days=365, n_products=10):
    """
    Создание синтетических данных о продажах для анализа временных рядов
    
    Parameters:
    -----------
    n_days : int, default=365
        Количество дней для генерации:
        - 30-90: краткосрочные тренды (месяц-квартал)
        - 90-365: среднесрочные тренды (квартал-год)
        - 365+: долгосрочные тренды (год+)
        
    n_products : int, default=10
        Количество продуктов для анализа:
        - 1-5: анализ одного продукта
        - 5-20: анализ продуктовой линейки
        - 20+: анализ большого ассортимента
        
    Returns:
    --------
    pd.DataFrame
        Синтетические данные о продажах:
        - date: дата продажи
        - product_id: идентификатор продукта
        - sales: количество продаж
        - day_of_week: день недели (0-6)
        - month: месяц (1-12)
        - quarter: квартал (1-4)
        
    Notes:
    ------
    Структура временного ряда:
    - Тренд: линейный рост продаж во времени
    - Сезонность: еженедельные колебания (выходные vs будни)
    - Шум: случайные колебания (рыночные факторы)
    - Негативные продажи: исключены (продажи ≥ 0)
    
    Временные признаки:
    - day_of_week: день недели для анализа выходных
    - month: месяц для сезонного анализа
    - quarter: квартал для квартального анализа
    """
    
    np.random.seed(42)  # Воспроизводимость результатов
    
    # Создание временного ряда
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    data = []
    for product_id in range(n_products):
        # Базовый тренд (линейный рост продаж)
        trend = np.linspace(100, 150, n_days)  # Рост с 100 до 150 продаж
        
        # Сезонность (еженедельные колебания)
        seasonality = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Амплитуда ±20
        
        # Случайный шум (рыночные факторы)
        noise = np.random.normal(0, 10, n_days)  # Стандартное отклонение 10
        
        # Продажи (комбинация тренда, сезонности и шума)
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
    """
    Подготовка данных о продажах для анализа временных рядов
    
    Parameters:
    -----------
    data : pd.DataFrame
        Исходные данные о продажах:
        - Содержит колонки: date, product_id, sales, day_of_week, month, quarter
        - Отсортированы по product_id и date
        - Могут содержать пропущенные значения
        
    Returns:
    --------
    pd.DataFrame
        Подготовленные данные с временными признаками:
        - Лаговые признаки: sales_lag_1, sales_lag_2, sales_lag_3, sales_lag_7, sales_lag_14, sales_lag_30
        - Скользящие средние: sales_ma_7, sales_ma_14, sales_ma_30
        - Трендовые признаки: sales_trend
        - Сезонные признаки: is_weekend, is_month_start, is_month_end
        
    Notes:
    ------
    Временные признаки для прогнозирования:
    - Лаговые признаки: значения продаж в предыдущие дни
    - Скользящие средние: сглаженные тренды за разные периоды
    - Трендовые признаки: направление изменения продаж
    - Сезонные признаки: календарные эффекты (выходные, начало/конец месяца)
    
    Лаговые признаки:
    - sales_lag_1: продажи вчера (краткосрочная зависимость)
    - sales_lag_7: продажи неделю назад (еженедельная сезонность)
    - sales_lag_30: продажи месяц назад (месячная сезонность)
    
    Скользящие средние:
    - sales_ma_7: средние продажи за неделю
    - sales_ma_14: средние продажи за 2 недели
    - sales_ma_30: средние продажи за месяц
    """
    
    # Создание лаговых признаков
    # Сортировка по продукту и дате для корректного сдвига
    data = data.sort_values(['product_id', 'date'])
    
    # Лаговые признаки (значения продаж в предыдущие дни)
    for lag in [1, 2, 3, 7, 14, 30]:  # Разные лаги для разных временных зависимостей
        data[f'sales_lag_{lag}'] = data.groupby('product_id')['sales'].shift(lag)
    
    # Скользящие средние (сглаженные тренды)
    for window in [7, 14, 30]:  # Разные окна для разных временных масштабов
        data[f'sales_ma_{window}'] = data.groupby('product_id')['sales'].rolling(window=window).mean().reset_index(0, drop=True)
    
    # Трендовые признаки (направление изменения продаж)
    data['sales_trend'] = data.groupby('product_id')['sales'].rolling(window=7).mean().reset_index(0, drop=True)
    
    # Сезонные признаки (календарные эффекты)
    data['is_weekend'] = (data['day_of_week'] >= 5).astype(int)  # Выходные дни
    data['is_month_start'] = (data['date'].dt.day <= 7).astype(int)  # Начало месяца
    data['is_month_end'] = (data['date'].dt.day >= 25).astype(int)  # Конец месяца
    
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

**Почему визуализация временных рядов особенная?** Потому что время - это дополнительное измерение, которое нужно учитывать:

- **Time Series Plot**: Показывает тренды, сезонность и качество прогноза во времени
- **Error Analysis**: Демонстрирует, как ошибки распределены по времени
- **Feature Importance**: Выявляет, какие временные признаки важны
- **Performance by Product**: Сравнивает качество прогноза для разных продуктов

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

<img src="images/optimized/multiclass_classification_analysis.png" alt="Пример многоклассовой классификации" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 5: Пример многоклассовой классификации - Confusion Matrix, точность по классам, распределение предсказаний, метрики качества*

**Почему многоклассовая классификация сложнее бинарной?** Потому что нужно различать множество классов одновременно:

**Ключевые аспекты многоклассовой классификации:**
- **Множественные классы**: Более 2 категорий для классификации
- **Импбаланс классов**: Неравномерное распределение примеров
- **Метрики качества**: Accuracy, Precision, Recall для каждого класса
- **Feature Engineering**: Извлечение признаков из изображений
- **Валидация**: Стратифицированное разделение данных
- **Интерпретируемость**: Понимание решений модели

### Задача
Классификация изображений на основе извлеченных признаков.

### Данные
```python
def create_image_data(n_samples=5000, n_features=100):
    """
    Создание синтетических данных изображений для многоклассовой классификации
    
    Parameters:
    -----------
    n_samples : int, default=5000
        Размер выборки для генерации:
        - 1000-3000: небольшие датасеты (быстрое тестирование)
        - 3000-10000: средние датасеты (баланс качества и скорости)
        - 10000+: большие датасеты (максимальное качество)
        
    n_features : int, default=100
        Количество признаков изображения:
        - 50-100: базовые признаки (цвет, текстура)
        - 100-500: расширенные признаки (формы, объекты)
        - 500+: сложные признаки (глубокие характеристики)
        
    Returns:
    --------
    pd.DataFrame
        Синтетические данные изображений:
        - Числовые признаки: feature_0, feature_1, ..., feature_n
        - Категориальные признаки: class, image_size, resolution
        - Числовые метаданные: color_channels
        
    Notes:
    ------
    Структура данных изображений:
    - n_features числовых признаков (извлеченные характеристики)
    - 5 классов объектов: cat, dog, bird, car, tree
    - 3 размера изображений: small, medium, large
    - 2 типа цветов: grayscale (1), RGB (3)
    - 3 разрешения: low, medium, high
    
    Бизнес-контекст:
    - Задача: классификация объектов на изображениях
    - Применение: компьютерное зрение, автоматическая маркировка
    - Метрики: accuracy, precision, recall для каждого класса
    - Валидация: стратифицированное разделение по классам
    """
    
    np.random.seed(42)  # Воспроизводимость результатов
    
    # Создание признаков изображений (извлеченные характеристики)
    # Нормальное распределение имитирует реальные признаки CNN
    features = np.random.randn(n_samples, n_features)
    
    # Создание целевых классов (5 категорий объектов)
    n_classes = 5
    classes = ['cat', 'dog', 'bird', 'car', 'tree']  # 5 классов объектов
    y = np.random.choice(n_classes, n_samples)  # Случайное распределение классов
    
    # Создание DataFrame с признаками
    feature_names = [f'feature_{i}' for i in range(n_features)]
    data = pd.DataFrame(features, columns=feature_names)
    data['class'] = [classes[i] for i in y]  # Целевая переменная
    
    # Добавление метаданных изображений
    data['image_size'] = np.random.choice(['small', 'medium', 'large'], n_samples)  # Размер изображения
    data['color_channels'] = np.random.choice([1, 3], n_samples)  # Количество цветовых каналов
    data['resolution'] = np.random.choice(['low', 'medium', 'high'], n_samples)  # Разрешение изображения
    
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
    """
    Подготовка данных изображений для многоклассовой классификации
    
    Parameters:
    -----------
    data : pd.DataFrame
        Исходные данные изображений:
        - Содержит числовые признаки (feature_0, feature_1, ...)
        - Содержит категориальные признаки (class, image_size, resolution)
        - Содержит метаданные (color_channels)
        
    Returns:
    --------
    pd.DataFrame
        Подготовленные данные изображений:
        - Созданы агрегированные признаки (feature_sum, feature_mean, feature_std)
        - Нормализованы числовые признаки
        - Готовы для обучения модели
        
    Notes:
    ------
    Процесс подготовки данных:
    1. Создание агрегированных признаков (сумма, среднее, стандартное отклонение)
    2. Нормализация числовых признаков (z-score нормализация)
    3. Сохранение категориальных признаков без изменений
    
    Агрегированные признаки:
    - feature_sum: сумма всех признаков (общая "активность" изображения)
    - feature_mean: среднее значение признаков (средняя "яркость")
    - feature_std: стандартное отклонение признаков (вариативность)
    
    Нормализация:
    - Z-score нормализация: (x - mean) / std
    - Применяется ко всем числовым признакам кроме color_channels
    - Обеспечивает стабильность обучения
    """
    
    # Создание новых признаков (feature engineering)
    # Агрегированные признаки помогают модели понять общие характеристики изображения
    data['feature_sum'] = data.select_dtypes(include=[np.number]).sum(axis=1)  # Сумма всех признаков
    data['feature_mean'] = data.select_dtypes(include=[np.number]).mean(axis=1)  # Среднее значение признаков
    data['feature_std'] = data.select_dtypes(include=[np.number]).std(axis=1)  # Стандартное отклонение признаков
    
    # Нормализация признаков (z-score нормализация)
    # Нормализация улучшает стабильность и скорость обучения
    numeric_columns = data.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if col != 'color_channels':  # Не нормализуем метаданные
            data[col] = (data[col] - data[col].mean()) / data[col].std()  # Z-score нормализация
    
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

**Почему многоклассовая классификация требует особой визуализации?** Потому что нужно анализировать качество по каждому классу отдельно:

- **Confusion Matrix**: Показывает, какие классы путает модель между собой
- **Class Accuracy**: Демонстрирует точность для каждого класса отдельно
- **Prediction Distribution**: Выявляет, не предсказывает ли модель только популярные классы
- **Feature Importance**: Показывает, какие признаки важны для различения классов

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

<img src="images/optimized/production_system_architecture.png" alt="Архитектура продакшен системы" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 7: Архитектура продакшен системы AutoML Gluon - компоненты, потоки данных, мониторинг*

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
    """
    Запрос на предсказание для продакшен API
    
    Parameters:
    -----------
    model_name : str
        Название модели для предсказания:
        - 'bank_default': модель классификации дефолта
        - 'real_estate': модель регрессии цен недвижимости
        - 'sales_forecast': модель прогнозирования продаж
        
    data : List[Dict[str, Any]]
        Данные для предсказания:
        - Список словарей с признаками
        - Каждый словарь - один образец для предсказания
        - Ключи должны соответствовать признакам модели
    """
    model_name: str
    data: List[Dict[str, Any]]

class PredictionResponse(BaseModel):
    """
    Ответ с результатами предсказания
    
    Parameters:
    -----------
    predictions : List[Any]
        Предсказания модели:
        - Для классификации: классы (0/1, 'cat'/'dog' и т.д.)
        - Для регрессии: числовые значения (цены, продажи)
        
    probabilities : List[Dict[str, float]], optional
        Вероятности классов (только для классификации):
        - Словарь с вероятностями для каждого класса
        - None для регрессионных моделей
        
    model_info : Dict[str, Any]
        Информация о модели:
        - model_name: название модели
        - model_type: тип задачи (classification/regression)
        - target: целевая переменная
        - features: список признаков
        
    timestamp : str
        Время выполнения предсказания (ISO формат)
    """
    predictions: List[Any]
    probabilities: List[Dict[str, float]] = None
    model_info: Dict[str, Any]
    timestamp: str

class ModelInfo(BaseModel):
    """
    Информация о модели в продакшен системе
    
    Parameters:
    -----------
    model_name : str
        Название модели в системе
        
    model_type : str
        Тип модели:
        - 'binary_classification': бинарная классификация
        - 'multiclass_classification': многоклассовая классификация
        - 'regression': регрессия
        
    performance : Dict[str, float]
        Метрики производительности модели:
        - accuracy, roc_auc, precision, recall (для классификации)
        - rmse, mae, r2 (для регрессии)
        
    features : List[str]
        Список признаков модели
        
    created_at : str
        Дата создания модели (ISO формат)
    """
    model_name: str
    model_type: str
    performance: Dict[str, float]
    features: List[str]
    created_at: str

@app.on_event("startup")
async def load_models():
    """
    Загрузка моделей при запуске продакшен системы
    
    Notes:
    ------
    Процесс загрузки моделей:
    1. Загрузка банковской модели (классификация дефолта)
    2. Загрузка модели недвижимости (регрессия цен)
    3. Создание метаданных для каждой модели
    4. Логирование результатов загрузки
    
    Метаданные модели:
    - model_type: тип задачи (binary_classification, regression)
    - target: целевая переменная
    - features: список признаков модели
    
    Обработка ошибок:
    - Логирование ошибок загрузки
    - Продолжение работы при частичной загрузке
    - Возврат ошибок через health check
    """
    global models, model_metadata
    
    # Загрузка банковской модели (классификация дефолта)
    try:
        models['bank_default'] = TabularPredictor.load('./bank_models')
        model_metadata['bank_default'] = {
            'model_type': 'binary_classification',  # Бинарная классификация
            'target': 'default_risk',  # Целевая переменная
            'features': ['age', 'income', 'credit_score', 'debt_ratio', 'employment_years']  # Основные признаки
        }
        logger.info("Bank model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load bank model: {e}")
    
    # Загрузка модели недвижимости (регрессия цен)
    try:
        models['real_estate'] = TabularPredictor.load('./real_estate_models')
        model_metadata['real_estate'] = {
            'model_type': 'regression',  # Регрессия
            'target': 'price',  # Целевая переменная
            'features': ['area', 'bedrooms', 'bathrooms', 'age', 'location']  # Основные признаки
        }
        logger.info("Real estate model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load real estate model: {e}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint для мониторинга состояния системы
    
    Returns:
    --------
    Dict[str, Any]
        Статус системы:
        - status: "healthy" если модели загружены, "unhealthy" если нет
        - loaded_models: список загруженных моделей
        - timestamp: время проверки (ISO формат)
        
    Notes:
    ------
    Health check используется для:
    - Мониторинга состояния системы
    - Проверки доступности моделей
    - Автоматического перезапуска при сбоях
    - Load balancer health checks
    """
    loaded_models = list(models.keys())
    return {
        "status": "healthy" if loaded_models else "unhealthy",  # Статус системы
        "loaded_models": loaded_models,  # Список загруженных моделей
        "timestamp": datetime.now().isoformat()  # Время проверки
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Endpoint для предсказаний с использованием обученных моделей
    
    Parameters:
    -----------
    request : PredictionRequest
        Запрос на предсказание:
        - model_name: название модели
        - data: данные для предсказания
        
    Returns:
    --------
    PredictionResponse
        Результаты предсказания:
        - predictions: предсказания модели
        - probabilities: вероятности классов (для классификации)
        - model_info: информация о модели
        - timestamp: время выполнения
        
    Raises:
    -------
    HTTPException
        - 404: модель не найдена
        - 500: ошибка выполнения предсказания
        
    Notes:
    ------
    Процесс предсказания:
    1. Проверка существования модели
    2. Преобразование данных в DataFrame
    3. Выполнение предсказания
    4. Получение вероятностей (для классификации)
    5. Формирование ответа
    
    Обработка ошибок:
    - Логирование ошибок предсказания
    - Возврат HTTP ошибок с описанием
    - Graceful handling исключений
    """
    
    if request.model_name not in models:
        raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")
    
    try:
        model = models[request.model_name]  # Получение модели
        metadata = model_metadata[request.model_name]  # Получение метаданных
        
        # Преобразование данных в DataFrame
        df = pd.DataFrame(request.data)
        
        # Предсказания модели
        predictions = model.predict(df)
        
        # Вероятности классов (только для классификации)
        probabilities = None
        if hasattr(model, 'predict_proba'):  # Проверка поддержки вероятностей
            proba = model.predict_proba(df)
            probabilities = proba.to_dict('records')  # Преобразование в список словарей
        
        return PredictionResponse(
            predictions=predictions.tolist(),  # Преобразование в список
            probabilities=probabilities,  # Вероятности классов
            model_info={
                "model_name": request.model_name,  # Название модели
                "model_type": metadata['model_type'],  # Тип задачи
                "target": metadata['target'],  # Целевая переменная
                "features": metadata['features']  # Список признаков
            },
            timestamp=datetime.now().isoformat()  # Время выполнения
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")  # Логирование ошибки
        raise HTTPException(status_code=500, detail=str(e))  # Возврат HTTP ошибки

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

## Продвинутые примеры

<img src="images/optimized/advanced_metrics_analysis.png" alt="Продвинутые примеры" style="max-width: 100%; height: auto; display: block; margin: 20px auto;">
*Рисунок 6: Продвинутые метрики - ROC с порогами, Precision-Recall, сравнение метрик, влияние порога на качество*

**Почему важны продвинутые примеры?** Потому что они показывают, как решать сложные реальные задачи:

**Типы продвинутых примеров:**
- **Ансамбли моделей**: Комбинирование различных алгоритмов
- **Feature Engineering**: Создание сложных признаков
- **Гиперпараметрическая оптимизация**: Автоматический поиск лучших параметров
- **Несбалансированные данные**: Работа с редкими классами
- **Большие данные**: Обработка датасетов размером в гигабайты
- **Продакшен деплой**: Развертывание моделей в реальных системах

### 🚀 Пример: Ансамбль моделей для финансового прогнозирования

**Почему ансамбли часто работают лучше одиночных моделей?** Потому что они объединяют сильные стороны разных алгоритмов:

- **Разнообразие моделей**: Разные алгоритмы находят разные паттерны
- **Снижение переобучения**: Усреднение снижает риск переобучения
- **Повышение стабильности**: Результат менее зависит от конкретной модели
- **Лучшая обобщающая способность**: Модель работает лучше на новых данных
- **Автоматический выбор**: AutoML сам выбирает лучшие комбинации
- **Интерпретируемость**: Можно понять вклад каждой модели

### 🎯 Пример: Работа с несбалансированными данными

**Почему несбалансированные данные - частая проблема?** Потому что в реальности редкие события встречаются редко:

- **Стратегии балансировки**: SMOTE, undersampling, oversampling
- **Метрики качества**: F1-score, Precision, Recall вместо Accuracy
- **Стоимость ошибок**: Разная цена за разные типы ошибок
- **Валидация**: Стратифицированное разделение данных
- **Ансамбли**: Комбинирование моделей для лучшего качества
- **Мониторинг**: Отслеживание качества на редких классах

## Следующие шаги

После изучения примеров переходите к:
- [Troubleshooting](./10_troubleshooting.md)
- [Лучшим практикам](./08_best_practices.md)
