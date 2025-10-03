# 05. 🤖 Обучение моделей

**Цель:** Научиться обучать эффективные ML-модели для финансовых данных.

## Выбор алгоритмов для торговли

**Теория:** Выбор алгоритмов для финансовых данных критически важен для успеха ML-систем. Финансовые данные имеют уникальные характеристики, которые требуют специальных подходов к обучению моделей.

### Почему не все алгоритмы подходят?

**Теория:** Финансовые данные имеют специфические характеристики, которые делают многие стандартные ML-алгоритмы неэффективными или даже опасными. Понимание этих особенностей критично для выбора правильных алгоритмов.

**Финансовые данные имеют особенности:**

**1. Нестационарность**
- **Теория:** Распределения данных меняются во времени из-за изменения рыночных условий
- **Почему проблематично:** Стандартные алгоритмы предполагают стационарность
- **Последствия:** Модели быстро устаревают, снижается производительность
- **Плюсы:** Возможность адаптации к изменениям
- **Минусы:** Сложность обучения, необходимость регулярного обновления

**2. Высокая волатильность**
- **Теория:** Финансовые данные содержат много шума и случайных колебаний
- **Почему проблематично:** Шум может переобучить модель на случайных паттернах
- **Последствия:** Ложные сигналы, переобучение, нестабильность
- **Плюсы:** Возможность выявления реальных паттернов
- **Минусы:** Сложность фильтрации шума, риск переобучения

**3. Неравномерность**
- **Теория:** Редкие, но важные события (кризисы, крахи) имеют непропорционально большое влияние
- **Почему проблематично:** Стандартные алгоритмы могут игнорировать редкие события
- **Последствия:** Модели могут не учитывать критические события
- **Плюсы:** Возможность выявления аномалий
- **Минусы:** Сложность балансировки классов, риск игнорирования важных событий

**4. Корреляции**
- **Теория:** Признаки часто сильно коррелированы, что может привести к мультиколлинеарности
- **Почему проблематично:** Коррелированные признаки могут искажать результаты
- **Последствия:** Нестабильность модели, сложность интерпретации
- **Плюсы:** Возможность выявления зависимостей
- **Минусы:** Сложность обработки, риск переобучения

### Лучшие алгоритмы для финансов

**Теория:** Выбор алгоритмов для финансовых данных должен основываться на их способности работать с нестационарными, зашумленными и коррелированными данными. Некоторые алгоритмы показали особую эффективность в финансовой сфере.

**1. Ансамблевые методы**
- **Почему эффективны:** Комбинируют множество моделей, снижая риск переобучения
- **Плюсы:** Высокая точность, устойчивость к выбросам, интерпретируемость
- **Минусы:** Высокие вычислительные затраты, сложность настройки
- **Применение:** Random Forest, XGBoost, LightGBM для классификации и регрессии

**2. Нейронные сети**
- **Почему эффективны:** Могут моделировать сложные нелинейные зависимости
- **Плюсы:** Высокая гибкость, способность к обучению сложным паттернам
- **Минусы:** Требуют много данных, сложность интерпретации, риск переобучения
- **Применение:** LSTM, GRU для временных рядов, Transformer для последовательностей

**3. SVM (Support Vector Machine)**
- **Почему эффективны:** Хорошо работают с нелинейными зависимостями
- **Плюсы:** Эффективны на малых данных, устойчивы к выбросам
- **Минусы:** Медленное обучение на больших данных, сложность настройки
- **Применение:** Классификация направлений движения цен

**4. Logistic Regression**
- **Почему эффективны:** Простые, интерпретируемые, быстрые
- **Плюсы:** Легкая интерпретация, быстрая работа, стабильность
- **Минусы:** Ограниченная способность к моделированию сложных зависимостей
- **Применение:** Базовые модели, интерпретируемые системы

**Дополнительные соображения:**
- **Регуляризация:** Важна для предотвращения переобучения
- **Кросс-валидация:** Критична для временных рядов
- **Гиперпараметрическая оптимизация:** Может значительно улучшить производительность
- **Ансамблирование:** Комбинация алгоритмов часто превосходит отдельные модели

## Ансамблевые методы

**Теория:** Ансамблевые методы комбинируют множество моделей для улучшения производительности. Они особенно эффективны для финансовых данных, так как снижают риск переобучения и повышают стабильность предсказаний.

**Почему ансамблевые методы эффективны для финансов:**
- **Снижение риска:** Комбинация моделей снижает риск ошибок
- **Устойчивость к выбросам:** Разные модели по-разному реагируют на выбросы
- **Стабильность:** Ансамбли более стабильны, чем отдельные модели
- **Интерпретируемость:** Можно анализировать важность признаков

### 1. Random Forest

**Теория:** Random Forest - это ансамбль решающих деревьев, который использует бутстрап агрегацию (bagging) для создания множества моделей. Каждое дерево обучается на случайной подвыборке данных и признаков.

**Детальная теория Random Forest:**

**Принцип работы:**
1. **Bootstrap Sampling:** Каждое дерево обучается на случайной выборке с возвращением (обычно 63% данных)
2. **Feature Randomness:** На каждом узле дерева выбирается случайное подмножество признаков
3. **Voting/Averaging:** Финальное предсказание - это среднее (регрессия) или голосование (классификация) всех деревьев

**Почему Random Forest эффективен для финансов:**
- **Устойчивость к переобучению:** Множество деревьев снижают риск переобучения на шуме
- **Обработка выбросов:** Деревья по-разному реагируют на выбросы, снижая их влияние
- **Интерпретируемость:** Можно анализировать важность признаков через feature importance
- **Быстрота:** Параллельное обучение деревьев позволяет обрабатывать большие объемы данных
- **Устойчивость к мультиколлинеарности:** Случайный выбор признаков снижает влияние корреляций

**Математическая основа:**
- **Bootstrap:** Для каждого дерева t, обучаем на выборке D_t, полученной из D с возвращением
- **Feature Selection:** На каждом узле выбираем √p признаков из p доступных
- **Prediction:** ŷ = (1/T) * Σ(t=1 to T) f_t(x), где T - количество деревьев

**Плюсы Random Forest:**
- Высокая точность на большинстве задач
- Устойчивость к переобучению
- Интерпретируемость через feature importance
- Быстрота обучения и предсказания
- Работает с пропущенными значениями
- Не требует масштабирования признаков

**Минусы Random Forest:**
- Могут быть менее точными на очень сложных данных
- Требуют настройки параметров (n_estimators, max_depth, etc.)
- Могут быть избыточными для простых задач
- Плохо работают с очень разреженными данными
- Могут переобучиться на очень маленьких датасетах
**Практическая реализация Random Forest:**

**Что делает этот код:**
1. **Разделение данных:** Создает обучающую и тестовую выборки с сохранением пропорций классов
2. **Создание модели:** Настраивает параметры Random Forest для финансовых данных
3. **Обучение:** Обучает модель на обучающих данных
4. **Оценка:** Проверяет производительность на обучающей и тестовой выборках

**Объяснение параметров:**
- `n_estimators=100`: Количество деревьев в лесу (больше = лучше, но медленнее)
- `max_depth=10`: Максимальная глубина дерева (предотвращает переобучение)
- `min_samples_split=5`: Минимум образцов для разделения узла
- `min_samples_leaf=2`: Минимум образцов в листе
- `n_jobs=-1`: Использует все доступные ядра процессора

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train_random_forest(X, y, test_size=0.2, random_state=42):
    """
    Обучение Random Forest для финансовых данных
    
    Args:
        X (array-like): Матрица признаков (samples, features)
        y (array-like): Целевые переменные (samples,)
        test_size (float): Доля тестовых данных (0.0-1.0)
        random_state (int): Seed для воспроизводимости
    
    Returns:
        tuple: (обученная модель, метрики, важность признаков)
    """
    
    print("=== Обучение Random Forest ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Разделение данных с сохранением пропорций классов
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Создание модели с оптимизированными параметрами для финансов
    rf = RandomForestClassifier(
        n_estimators=100,        # Количество деревьев
        max_depth=10,            # Максимальная глубина (предотвращает переобучение)
        min_samples_split=5,     # Минимум для разделения узла
        min_samples_leaf=2,      # Минимум в листе
        max_features='sqrt',     # Количество признаков для разделения
        bootstrap=True,          # Bootstrap sampling
        oob_score=True,          # Out-of-bag оценка
        random_state=random_state,
        n_jobs=-1,               # Параллельное обучение
        verbose=0
    )
    
    print("\nПараметры модели:")
    print(f"n_estimators: {rf.n_estimators}")
    print(f"max_depth: {rf.max_depth}")
    print(f"max_features: {rf.max_features}")
    
    # Обучение модели
    print("\nОбучение модели...")
    rf.fit(X_train, y_train)
    
    # Предсказания
    y_train_pred = rf.predict(X_train)
    y_test_pred = rf.predict(X_test)
    
    # Оценка производительности
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    oob_score = rf.oob_score_
    
    print(f"\n=== Результаты ===")
    print(f"Train accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    print(f"OOB score: {oob_score:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Test) ===")
    print(classification_report(y_test, y_test_pred))
    
    # Важность признаков
    feature_importance = rf.feature_importances_
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # Создание DataFrame с важностью признаков
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\n=== Топ-10 важных признаков ===")
    print(importance_df.head(10))
    
    # Метрики для возврата
    metrics = {
        'train_accuracy': train_score,
        'test_accuracy': test_score,
        'oob_score': oob_score,
        'feature_importance': importance_df,
        'confusion_matrix': confusion_matrix(y_test, y_test_pred)
    }
    
    return rf, metrics, importance_df

def plot_feature_importance(importance_df, top_n=15):
    """Визуализация важности признаков"""
    
    plt.figure(figsize=(10, 8))
    top_features = importance_df.head(top_n)
    
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title(f'Важность признаков (Top {top_n})')
    plt.xlabel('Важность')
    plt.ylabel('Признаки')
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_random_forest_usage():
    """Пример использования Random Forest"""
    
    # Создание синтетических данных для демонстрации
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с некоторой логикой
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1  # Класс 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2  # Класс 2
        else:
            y[i] = 0  # Класс 0
    
    print("=== Пример использования Random Forest ===")
    
    # Обучение модели
    model, metrics, importance_df = train_random_forest(X, y)
    
    # Визуализация важности признаков
    plot_feature_importance(importance_df)
    
    return model, metrics

# Запуск примера (раскомментируйте для тестирования)
# model, metrics = example_random_forest_usage()
```

### 2. XGBoost

**Теория:** XGBoost (eXtreme Gradient Boosting) - это продвинутая реализация градиентного бустинга, которая особенно эффективна для финансовых данных благодаря своей способности обрабатывать нелинейные зависимости и выбросы.

**Детальная теория XGBoost:**

**Принцип работы:**
1. **Gradient Boosting:** Последовательно добавляет деревья, каждое из которых исправляет ошибки предыдущих
2. **Regularization:** Использует L1 и L2 регуляризацию для предотвращения переобучения
3. **Parallel Processing:** Оптимизирован для параллельных вычислений
4. **Missing Value Handling:** Автоматически обрабатывает пропущенные значения

**Почему XGBoost эффективен для финансов:**
- **Высокая точность:** Часто показывает лучшие результаты на табличных данных
- **Обработка выбросов:** Устойчив к аномальным значениям
- **Feature Importance:** Позволяет анализировать важность признаков
- **Быстрота:** Оптимизирован для скорости
- **Регуляризация:** Встроенная защита от переобучения

**Математическая основа:**
- **Objective Function:** L(φ) = Σ l(yi, ŷi) + Σ Ω(fk)
- **Gradient Boosting:** F_m(x) = F_{m-1}(x) + γ_m * h_m(x)
- **Regularization:** Ω(f) = γT + (1/2)λ||w||²

**Ключевые параметры:**
- `learning_rate`: Скорость обучения (0.01-0.3)
- `max_depth`: Глубина деревьев (3-10)
- `n_estimators`: Количество бустеров (50-1000)
- `subsample`: Доля образцов для каждого дерева (0.6-1.0)
- `colsample_bytree`: Доля признаков для каждого дерева (0.6-1.0)

**Практическая реализация XGBoost:**

**Что делает этот код:**
1. **Настройка параметров:** Оптимизирует параметры для финансовых данных
2. **Early Stopping:** Предотвращает переобучение через валидацию
3. **Оценка производительности:** Использует метрики, подходящие для финансов
4. **Feature Importance:** Анализирует важность признаков

```python
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def train_xgboost(X, y, test_size=0.2, random_state=42, early_stopping_rounds=10):
    """
    Обучение XGBoost для финансовых данных
    
    Args:
        X (array-like): Матрица признаков (samples, features)
        y (array-like): Целевые переменные (samples,)
        test_size (float): Доля тестовых данных (0.0-1.0)
        random_state (int): Seed для воспроизводимости
        early_stopping_rounds (int): Количество раундов для early stopping
    
    Returns:
        tuple: (обученная модель, метрики, важность признаков)
    """
    
    print("=== Обучение XGBoost ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Оптимизированные параметры для финансовых данных
    params = {
        'objective': 'multi:softprob',    # Многоклассовая классификация с вероятностями
        'num_class': len(np.unique(y)),   # Количество классов
        'max_depth': 6,                   # Глубина деревьев (предотвращает переобучение)
        'learning_rate': 0.1,             # Скорость обучения
        'n_estimators': 100,              # Количество бустеров
        'subsample': 0.8,                 # Доля образцов для каждого дерева
        'colsample_bytree': 0.8,          # Доля признаков для каждого дерева
        'reg_alpha': 0.1,                 # L1 регуляризация
        'reg_lambda': 1.0,                # L2 регуляризация
        'random_state': random_state,
        'n_jobs': -1,                     # Параллельное обучение
        'verbosity': 0                    # Отключить вывод
    }
    
    print("\nПараметры XGBoost:")
    for key, value in params.items():
        print(f"{key}: {value}")
    
    # Создание модели
    xgb_model = xgb.XGBClassifier(**params)
    
    # Обучение с early stopping
    print("\nОбучение модели...")
    xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=early_stopping_rounds,
        verbose=False
    )
    
    # Предсказания
    y_train_pred = xgb_model.predict(X_train)
    y_test_pred = xgb_model.predict(X_test)
    y_test_proba = xgb_model.predict_proba(X_test)
    
    # Оценка производительности
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    print(f"\n=== Результаты ===")
    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Best iteration: {xgb_model.best_iteration}")
    print(f"Best score: {xgb_model.best_score:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Test) ===")
    print(classification_report(y_test, y_test_pred))
    
    # Важность признаков
    feature_importance = xgb_model.feature_importances_
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # Создание DataFrame с важностью признаков
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\n=== Топ-10 важных признаков ===")
    print(importance_df.head(10))
    
    # Метрики для возврата
    metrics = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'best_iteration': xgb_model.best_iteration,
        'best_score': xgb_model.best_score,
        'feature_importance': importance_df,
        'confusion_matrix': confusion_matrix(y_test, y_test_pred),
        'predictions': y_test_pred,
        'probabilities': y_test_proba
    }
    
    return xgb_model, metrics, importance_df

def plot_xgboost_importance(importance_df, top_n=15):
    """Визуализация важности признаков XGBoost"""
    
    plt.figure(figsize=(12, 8))
    top_features = importance_df.head(top_n)
    
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title(f'Важность признаков XGBoost (Top {top_n})')
    plt.xlabel('Важность')
    plt.ylabel('Признаки')
    plt.tight_layout()
    plt.show()

def plot_learning_curve(model, X_train, y_train, X_test, y_test):
    """Визуализация кривой обучения"""
    
    # Получение результатов обучения
    results = model.evals_result()
    
    plt.figure(figsize=(12, 4))
    
    # График ошибки
    plt.subplot(1, 2, 1)
    plt.plot(results['validation_0']['mlogloss'], label='Train')
    plt.plot(results['validation_1']['mlogloss'], label='Test')
    plt.title('Learning Curve - Log Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Log Loss')
    plt.legend()
    plt.grid(True)
    
    # График точности
    plt.subplot(1, 2, 2)
    train_acc = [1 - x for x in results['validation_0']['mlogloss']]
    test_acc = [1 - x for x in results['validation_1']['mlogloss']]
    plt.plot(train_acc, label='Train')
    plt.plot(test_acc, label='Test')
    plt.title('Learning Curve - Accuracy')
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_xgboost_usage():
    """Пример использования XGBoost"""
    
    # Создание синтетических данных для демонстрации
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков с некоторой структурой
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с нелинейными зависимостями
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Сложная нелинейная зависимость
        score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] + 
                np.sin(X[i, 3]) + X[i, 4] * X[i, 5])
        
        if score > 2.0:
            y[i] = 2  # Класс 2
        elif score > 0.5:
            y[i] = 1  # Класс 1
        else:
            y[i] = 0  # Класс 0
    
    print("=== Пример использования XGBoost ===")
    
    # Обучение модели
    model, metrics, importance_df = train_xgboost(X, y)
    
    # Визуализация важности признаков
    plot_xgboost_importance(importance_df)
    
    return model, metrics

# Запуск примера (раскомментируйте для тестирования)
# model, metrics = example_xgboost_usage()
```

### 3. LightGBM

**Теория:** LightGBM (Light Gradient Boosting Machine) - это быстрая и эффективная реализация градиентного бустинга, разработанная Microsoft. Особенно эффективна для больших датасетов и финансовых данных благодаря оптимизированному алгоритму построения деревьев.

**Детальная теория LightGBM:**

**Принцип работы:**
1. **Leaf-wise Growth:** Строит деревья по листьям, а не по уровням (как XGBoost)
2. **Gradient-based One-Side Sampling (GOSS):** Использует только образцы с большими градиентами
3. **Exclusive Feature Bundling (EFB):** Группирует взаимно исключающие признаки
4. **Categorical Feature Support:** Автоматически обрабатывает категориальные признаки

**Почему LightGBM эффективен для финансов:**
- **Скорость:** В 10-100 раз быстрее XGBoost на больших данных
- **Память:** Использует меньше памяти благодаря оптимизациям
- **Точность:** Часто показывает лучшие результаты
- **Категориальные признаки:** Отлично работает с финансовыми категориями
- **Регуляризация:** Встроенная защита от переобучения

**Математическая основа:**
- **Leaf-wise Growth:** Выбирает лист с максимальным приростом информации
- **GOSS:** Использует топ-a% образцов с большими градиентами + случайные b% остальных
- **EFB:** Группирует признаки с низкой корреляцией

**Ключевые параметры:**
- `num_leaves`: Количество листьев (31-255)
- `learning_rate`: Скорость обучения (0.01-0.3)
- `feature_fraction`: Доля признаков (0.6-1.0)
- `bagging_fraction`: Доля образцов (0.6-1.0)
- `min_data_in_leaf`: Минимум данных в листе (20-100)

**Практическая реализация LightGBM:**

**Что делает этот код:**
1. **Оптимизированные параметры:** Настройка для финансовых данных
2. **Early Stopping:** Предотвращение переобучения
3. **Валидация:** Мониторинг производительности
4. **Feature Importance:** Анализ важности признаков

```python
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

def train_lightgbm(X, y, test_size=0.2, random_state=42, early_stopping_rounds=10):
    """
    Обучение LightGBM для финансовых данных
    
    Args:
        X (array-like): Матрица признаков (samples, features)
        y (array-like): Целевые переменные (samples,)
        test_size (float): Доля тестовых данных (0.0-1.0)
        random_state (int): Seed для воспроизводимости
        early_stopping_rounds (int): Количество раундов для early stopping
    
    Returns:
        tuple: (обученная модель, метрики, важность признаков)
    """
    
    print("=== Обучение LightGBM ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Оптимизированные параметры для финансовых данных
    params = {
        'objective': 'multiclass',           # Многоклассовая классификация
        'num_class': len(np.unique(y)),      # Количество классов
        'boosting_type': 'gbdt',             # Тип бустинга (Gradient Boosting Decision Tree)
        'num_leaves': 31,                    # Количество листьев (2^max_depth - 1)
        'learning_rate': 0.05,               # Скорость обучения
        'feature_fraction': 0.9,             # Доля признаков для каждого дерева
        'bagging_fraction': 0.8,             # Доля образцов для каждого дерева
        'bagging_freq': 5,                   # Частота применения bagging
        'min_data_in_leaf': 20,              # Минимум данных в листе
        'min_sum_hessian_in_leaf': 1e-3,     # Минимум суммы гессианов в листе
        'lambda_l1': 0.1,                    # L1 регуляризация
        'lambda_l2': 1.0,                    # L2 регуляризация
        'min_gain_to_split': 0.0,            # Минимальный прирост для разделения
        'max_depth': -1,                     # Максимальная глубина (-1 = неограниченно)
        'save_binary': True,                 # Сохранение бинарных файлов
        'seed': random_state,                # Seed для воспроизводимости
        'feature_fraction_seed': random_state,
        'bagging_seed': random_state,
        'drop_seed': random_state,
        'data_random_seed': random_state,
        'verbose': -1,                       # Отключить вывод
        'n_jobs': -1                         # Параллельное обучение
    }
    
    print("\nПараметры LightGBM:")
    for key, value in params.items():
        print(f"{key}: {value}")
    
    # Создание датасетов LightGBM
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    # Обучение модели
    print("\nОбучение модели...")
    model = lgb.train(
        params,
        train_data,
        valid_sets=[test_data],
        num_boost_round=100,
        callbacks=[
            lgb.early_stopping(early_stopping_rounds),
            lgb.log_evaluation(0)  # Отключить вывод прогресса
        ]
    )
    
    # Предсказания
    y_train_pred = model.predict(X_train, num_iteration=model.best_iteration)
    y_test_pred = model.predict(X_test, num_iteration=model.best_iteration)
    
    # Преобразование вероятностей в классы
    y_train_pred_class = np.argmax(y_train_pred, axis=1)
    y_test_pred_class = np.argmax(y_test_pred, axis=1)
    
    # Оценка производительности
    train_accuracy = accuracy_score(y_train, y_train_pred_class)
    test_accuracy = accuracy_score(y_test, y_test_pred_class)
    
    print(f"\n=== Результаты ===")
    print(f"Train accuracy: {train_accuracy:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Best iteration: {model.best_iteration}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Test) ===")
    print(classification_report(y_test, y_test_pred_class))
    
    # Важность признаков
    feature_importance = model.feature_importance(importance_type='gain')
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    
    # Создание DataFrame с важностью признаков
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\n=== Топ-10 важных признаков ===")
    print(importance_df.head(10))
    
    # Метрики для возврата
    metrics = {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'best_iteration': model.best_iteration,
        'feature_importance': importance_df,
        'confusion_matrix': confusion_matrix(y_test, y_test_pred_class),
        'predictions': y_test_pred_class,
        'probabilities': y_test_pred
    }
    
    return model, metrics, importance_df

def plot_lightgbm_importance(importance_df, top_n=15):
    """Визуализация важности признаков LightGBM"""
    
    plt.figure(figsize=(12, 8))
    top_features = importance_df.head(top_n)
    
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title(f'Важность признаков LightGBM (Top {top_n})')
    plt.xlabel('Важность')
    plt.ylabel('Признаки')
    plt.tight_layout()
    plt.show()

def plot_lightgbm_learning_curve(model):
    """Визуализация кривой обучения LightGBM"""
    
    # Получение истории обучения
    history = model.evals_result_
    
    plt.figure(figsize=(12, 4))
    
    # График ошибки
    plt.subplot(1, 2, 1)
    train_loss = history['training']['multi_logloss']
    valid_loss = history['valid_0']['multi_logloss']
    
    plt.plot(train_loss, label='Train')
    plt.plot(valid_loss, label='Validation')
    plt.title('Learning Curve - Multi Log Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Multi Log Loss')
    plt.legend()
    plt.grid(True)
    
    # График точности
    plt.subplot(1, 2, 2)
    train_acc = [1 - x for x in train_loss]
    valid_acc = [1 - x for x in valid_loss]
    
    plt.plot(train_acc, label='Train')
    plt.plot(valid_acc, label='Validation')
    plt.title('Learning Curve - Accuracy')
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_lightgbm_usage():
    """Пример использования LightGBM"""
    
    # Создание синтетических данных для демонстрации
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков с некоторой структурой
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с нелинейными зависимостями
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Сложная нелинейная зависимость
        score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] + 
                np.sin(X[i, 3]) + X[i, 4] * X[i, 5])
        
        if score > 2.0:
            y[i] = 2  # Класс 2
        elif score > 0.5:
            y[i] = 1  # Класс 1
        else:
            y[i] = 0  # Класс 0
    
    print("=== Пример использования LightGBM ===")
    
    # Обучение модели
    model, metrics, importance_df = train_lightgbm(X, y)
    
    # Визуализация важности признаков
    plot_lightgbm_importance(importance_df)
    
    # Визуализация кривой обучения
    plot_lightgbm_learning_curve(model)
    
    return model, metrics

# Запуск примера (раскомментируйте для тестирования)
# model, metrics = example_lightgbm_usage()
```

## Нейронные сети

**Теория:** Нейронные сети - это мощный инструмент для моделирования сложных нелинейных зависимостей в финансовых данных. Они особенно эффективны для выявления скрытых паттернов и взаимодействий между признаками.

**Почему нейронные сети эффективны для финансов:**
- **Нелинейность:** Могут моделировать сложные нелинейные зависимости
- **Взаимодействия:** Автоматически выявляют взаимодействия между признаками
- **Адаптивность:** Могут адаптироваться к изменяющимся рыночным условиям
- **Масштабируемость:** Хорошо работают с большими объемами данных

### 1. Простая нейронная сеть

**Теория:** Полносвязная нейронная сеть (Multi-Layer Perceptron) состоит из нескольких слоев нейронов, соединенных весами. Каждый нейрон применяет нелинейную функцию активации к взвешенной сумме входов.

**Архитектура сети:**
- **Входной слой:** Количество нейронов = количество признаков
- **Скрытые слои:** 2-3 слоя с 64-256 нейронами каждый
- **Выходной слой:** Количество нейронов = количество классов
- **Dropout:** Регуляризация для предотвращения переобучения
- **Активация:** ReLU для скрытых слоев, Softmax для выходного

**Практическая реализация:**

**Что делает этот код:**
1. **Создание архитектуры:** Определяет структуру нейронной сети
2. **Обучение:** Использует backpropagation для оптимизации весов
3. **Регуляризация:** Применяет dropout для предотвращения переобучения
4. **Валидация:** Мониторит производительность в процессе обучения

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

class TradingNN(nn.Module):
    """
    Нейронная сеть для торговых предсказаний
    
    Архитектура:
    - Входной слой: input_size нейронов
    - 3 скрытых слоя: hidden_size нейронов каждый
    - Выходной слой: num_classes нейронов
    - Dropout: 0.2 для регуляризации
    - Активация: ReLU для скрытых слоев
    """
    
    def __init__(self, input_size, hidden_size=128, num_classes=3, dropout_rate=0.2):
        super(TradingNN, self).__init__()
        
        # Определение слоев
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc4 = nn.Linear(hidden_size, num_classes)
        
        # Регуляризация
        self.dropout = nn.Dropout(dropout_rate)
        
        # Функция активации
        self.relu = nn.ReLU()
        
        # Инициализация весов
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Инициализация весов для лучшей сходимости"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        """Прямой проход через сеть"""
        # Первый скрытый слой
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        
        # Второй скрытый слой
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        
        # Третий скрытый слой
        x = self.relu(self.fc3(x))
        x = self.dropout(x)
        
        # Выходной слой (без активации - будет применен в loss function)
        x = self.fc4(x)
        
        return x

def train_neural_network(X, y, epochs=100, batch_size=32, learning_rate=0.001, 
                        test_size=0.2, random_state=42):
    """
    Обучение нейронной сети для торговых предсказаний
    
    Args:
        X (array-like): Матрица признаков
        y (array-like): Целевые переменные
        epochs (int): Количество эпох обучения
        batch_size (int): Размер батча
        learning_rate (float): Скорость обучения
        test_size (float): Доля тестовых данных
        random_state (int): Seed для воспроизводимости
    
    Returns:
        tuple: (обученная модель, метрики, история обучения)
    """
    
    print("=== Обучение нейронной сети ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Преобразование в тензоры PyTorch
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.LongTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.LongTensor(y_test)
    
    # Создание датасета и DataLoader
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Создание модели
    model = TradingNN(X.shape[1], num_classes=len(np.unique(y)))
    
    # Функция потерь и оптимизатор
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # История обучения
    train_losses = []
    train_accuracies = []
    test_accuracies = []
    
    print(f"\nПараметры обучения:")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Learning rate: {learning_rate}")
    print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")
    
    # Обучение
    print("\nНачало обучения...")
    model.train()
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        correct = 0
        total = 0
        
        for batch_X, batch_y in train_dataloader:
            # Обнуление градиентов
            optimizer.zero_grad()
            
            # Прямой проход
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            # Обратный проход
            loss.backward()
            optimizer.step()
            
            # Статистика
            epoch_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
        
        # Вычисление метрик
        avg_loss = epoch_loss / len(train_dataloader)
        train_accuracy = correct / total
        
        train_losses.append(avg_loss)
        train_accuracies.append(train_accuracy)
        
        # Оценка на тестовых данных
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test_tensor)
            _, test_predicted = torch.max(test_outputs.data, 1)
            test_accuracy = accuracy_score(y_test, test_predicted.numpy())
            test_accuracies.append(test_accuracy)
        model.train()
        
        # Вывод прогресса
        if epoch % 10 == 0 or epoch == epochs - 1:
            print(f'Epoch {epoch:3d}/{epochs}: '
                  f'Loss: {avg_loss:.4f}, '
                  f'Train Acc: {train_accuracy:.4f}, '
                  f'Test Acc: {test_accuracy:.4f}')
    
    # Финальная оценка
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        _, test_predicted = torch.max(test_outputs.data, 1)
        test_predictions = test_predicted.numpy()
        test_probabilities = torch.softmax(test_outputs, dim=1).numpy()
    
    # Метрики
    final_accuracy = accuracy_score(y_test, test_predictions)
    
    print(f"\n=== Финальные результаты ===")
    print(f"Test accuracy: {final_accuracy:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report ===")
    print(classification_report(y_test, test_predictions))
    
    # История обучения
    history = {
        'train_losses': train_losses,
        'train_accuracies': train_accuracies,
        'test_accuracies': test_accuracies
    }
    
    # Метрики для возврата
    metrics = {
        'test_accuracy': final_accuracy,
        'confusion_matrix': confusion_matrix(y_test, test_predictions),
        'predictions': test_predictions,
        'probabilities': test_probabilities,
        'history': history
    }
    
    return model, metrics, history

def plot_training_history(history):
    """Визуализация истории обучения"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # График потерь
    ax1.plot(history['train_losses'], label='Train Loss')
    ax1.set_title('Training Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # График точности
    ax2.plot(history['train_accuracies'], label='Train Accuracy')
    ax2.plot(history['test_accuracies'], label='Test Accuracy')
    ax2.set_title('Training and Test Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_neural_network_usage():
    """Пример использования нейронной сети"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с нелинейными зависимостями
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Сложная нелинейная зависимость
        score = (X[i, 0] ** 2 + X[i, 1] * X[i, 2] + 
                np.sin(X[i, 3]) + X[i, 4] * X[i, 5])
        
        if score > 2.0:
            y[i] = 2  # Класс 2
        elif score > 0.5:
            y[i] = 1  # Класс 1
        else:
            y[i] = 0  # Класс 0
    
    print("=== Пример использования нейронной сети ===")
    
    # Обучение модели
    model, metrics, history = train_neural_network(X, y, epochs=50)
    
    # Визуализация истории обучения
    plot_training_history(history)
    
    return model, metrics

# Запуск примера (раскомментируйте для тестирования)
# model, metrics = example_neural_network_usage()
```

### 2. LSTM для временных рядов

**Теория:** LSTM (Long Short-Term Memory) - это специальный тип рекуррентной нейронной сети, разработанный для работы с временными последовательностями. LSTM особенно эффективен для финансовых данных, так как может запоминать долгосрочные зависимости и паттерны.

**Детальная теория LSTM:**

**Принцип работы:**
1. **Забывающий гейт (Forget Gate):** Решает, какую информацию забыть из предыдущего состояния
2. **Входной гейт (Input Gate):** Решает, какую новую информацию сохранить
3. **Гейт обновления (Update Gate):** Обновляет состояние ячейки
4. **Выходной гейт (Output Gate):** Решает, какую информацию вывести

**Почему LSTM эффективен для финансов:**
- **Временные зависимости:** Может запоминать паттерны на длинных временных интервалах
- **Устойчивость к градиентному исчезновению:** Решает проблему RNN
- **Обработка последовательностей:** Идеально подходит для временных рядов
- **Контекстная информация:** Учитывает историю для принятия решений

**Математическая основа:**
- **Forget Gate:** f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
- **Input Gate:** i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
- **Cell State:** C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
- **Update:** C_t = f_t * C_{t-1} + i_t * C̃_t
- **Output Gate:** o_t = σ(W_o · [h_{t-1}, x_t] + b_o)
- **Hidden State:** h_t = o_t * tanh(C_t)

**Практическая реализация LSTM:**

**Что делает этот код:**
1. **Создание последовательностей:** Преобразует данные в формат временных рядов
2. **Архитектура LSTM:** Определяет структуру рекуррентной сети
3. **Обучение:** Использует backpropagation through time (BPTT)
4. **Валидация:** Оценивает производительность на временных данных

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

class LSTMTradingModel(nn.Module):
    """
    LSTM модель для торговых предсказаний на временных рядах
    
    Архитектура:
    - LSTM слои: для обработки временных последовательностей
    - Dropout: для регуляризации
    - Полносвязный слой: для финальной классификации
    """
    
    def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=3, dropout_rate=0.2):
        super(LSTMTradingModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM слои
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0,
            bidirectional=False
        )
        
        # Полносвязный слой для классификации
        self.fc = nn.Linear(hidden_size, num_classes)
        
        # Dropout для регуляризации
        self.dropout = nn.Dropout(dropout_rate)
        
        # Инициализация весов
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Инициализация весов LSTM"""
        for name, param in self.named_parameters():
            if 'weight_ih' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'weight_hh' in name:
                nn.init.orthogonal_(param.data)
            elif 'bias' in name:
                param.data.fill_(0)
                # Установка forget gate bias в 1 для лучшей инициализации
                n = param.size(0)
                param.data[(n//4):(n//2)].fill_(1)
    
    def forward(self, x):
        """
        Прямой проход через LSTM
        
        Args:
            x: Входные данные формы (batch_size, sequence_length, input_size)
        
        Returns:
            Выходные данные формы (batch_size, num_classes)
        """
        batch_size = x.size(0)
        
        # Инициализация скрытого состояния
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=x.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_size, device=x.device)
        
        # LSTM forward pass
        lstm_out, (hn, cn) = self.lstm(x, (h0, c0))
        
        # Берем последний выход из последовательности
        last_output = lstm_out[:, -1, :]  # (batch_size, hidden_size)
        
        # Применяем dropout
        last_output = self.dropout(last_output)
        
        # Финальная классификация
        output = self.fc(last_output)
        
        return output

def create_sequences(X, y, sequence_length):
    """
    Создание последовательностей для LSTM
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        sequence_length: Длина последовательности
    
    Returns:
        X_seq: Последовательности признаков (samples-seq_len+1, seq_len, features)
        y_seq: Целевые переменные для последовательностей (samples-seq_len+1,)
    """
    X_seq, y_seq = [], []
    
    for i in range(sequence_length, len(X)):
        X_seq.append(X[i-sequence_length:i])
        y_seq.append(y[i])
    
    return np.array(X_seq), np.array(y_seq)

def train_lstm_model(X, y, sequence_length=10, epochs=100, batch_size=32, 
                    learning_rate=0.001, test_size=0.2, random_state=42):
    """
    Обучение LSTM модели для торговых предсказаний
    
    Args:
        X: Матрица признаков
        y: Целевые переменные
        sequence_length: Длина временной последовательности
        epochs: Количество эпох обучения
        batch_size: Размер батча
        learning_rate: Скорость обучения
        test_size: Доля тестовых данных
        random_state: Seed для воспроизводимости
    
    Returns:
        tuple: (обученная модель, метрики, история обучения)
    """
    
    print("=== Обучение LSTM модели ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    print(f"Длина последовательности: {sequence_length}")
    
    # Создание последовательностей
    X_seq, y_seq = create_sequences(X, y, sequence_length)
    print(f"Размер последовательностей: {X_seq.shape}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X_seq, y_seq, test_size=test_size, random_state=random_state, stratify=y_seq
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} последовательностей")
    print(f"Тестовая выборка: {X_test.shape[0]} последовательностей")
    
    # Преобразование в тензоры PyTorch
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.LongTensor(y_train)
    X_test_tensor = torch.FloatTensor(X_test)
    y_test_tensor = torch.LongTensor(y_test)
    
    # Создание датасета и DataLoader
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Создание модели
    model = LSTMTradingModel(
        input_size=X.shape[1], 
        num_classes=len(np.unique(y)),
        hidden_size=64,
        num_layers=2
    )
    
    # Функция потерь и оптимизатор
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # История обучения
    train_losses = []
    train_accuracies = []
    test_accuracies = []
    
    print(f"\nПараметры обучения:")
    print(f"Epochs: {epochs}")
    print(f"Batch size: {batch_size}")
    print(f"Learning rate: {learning_rate}")
    print(f"Sequence length: {sequence_length}")
    print(f"Model parameters: {sum(p.numel() for p in model.parameters())}")
    
    # Обучение
    print("\nНачало обучения...")
    model.train()
    
    for epoch in range(epochs):
        epoch_loss = 0.0
        correct = 0
        total = 0
        
        for batch_X, batch_y in train_dataloader:
            # Обнуление градиентов
            optimizer.zero_grad()
            
            # Прямой проход
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            # Обратный проход
            loss.backward()
            
            # Обрезка градиентов для стабильности
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            
            optimizer.step()
            
            # Статистика
            epoch_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
        
        # Вычисление метрик
        avg_loss = epoch_loss / len(train_dataloader)
        train_accuracy = correct / total
        
        train_losses.append(avg_loss)
        train_accuracies.append(train_accuracy)
        
        # Оценка на тестовых данных
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test_tensor)
            _, test_predicted = torch.max(test_outputs.data, 1)
            test_accuracy = accuracy_score(y_test, test_predicted.numpy())
            test_accuracies.append(test_accuracy)
        model.train()
        
        # Вывод прогресса
        if epoch % 10 == 0 or epoch == epochs - 1:
            print(f'Epoch {epoch:3d}/{epochs}: '
                  f'Loss: {avg_loss:.4f}, '
                  f'Train Acc: {train_accuracy:.4f}, '
                  f'Test Acc: {test_accuracy:.4f}')
    
    # Финальная оценка
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        _, test_predicted = torch.max(test_outputs.data, 1)
        test_predictions = test_predicted.numpy()
        test_probabilities = torch.softmax(test_outputs, dim=1).numpy()
    
    # Метрики
    final_accuracy = accuracy_score(y_test, test_predictions)
    
    print(f"\n=== Финальные результаты ===")
    print(f"Test accuracy: {final_accuracy:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report ===")
    print(classification_report(y_test, test_predictions))
    
    # История обучения
    history = {
        'train_losses': train_losses,
        'train_accuracies': train_accuracies,
        'test_accuracies': test_accuracies
    }
    
    # Метрики для возврата
    metrics = {
        'test_accuracy': final_accuracy,
        'confusion_matrix': confusion_matrix(y_test, test_predictions),
        'predictions': test_predictions,
        'probabilities': test_probabilities,
        'history': history
    }
    
    return model, metrics, history

def plot_lstm_training_history(history):
    """Визуализация истории обучения LSTM"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # График потерь
    ax1.plot(history['train_losses'], label='Train Loss')
    ax1.set_title('LSTM Training Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # График точности
    ax2.plot(history['train_accuracies'], label='Train Accuracy')
    ax2.plot(history['test_accuracies'], label='Test Accuracy')
    ax2.set_title('LSTM Training and Test Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_lstm_usage():
    """Пример использования LSTM"""
    
    # Создание синтетических временных данных
    np.random.seed(42)
    n_samples, n_features = 1000, 10
    sequence_length = 10
    
    # Генерация признаков с временной структурой
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с временными зависимостями
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Временная зависимость: текущее значение зависит от предыдущих
        if i < sequence_length:
            y[i] = 0  # Начальные значения
        else:
            # Сложная временная зависимость
            recent_sum = np.sum(X[i-sequence_length:i, 0])
            recent_volatility = np.std(X[i-sequence_length:i, 1])
            
            if recent_sum > 2.0 and recent_volatility < 1.0:
                y[i] = 2  # Класс 2
            elif recent_sum > 0.5 or recent_volatility > 1.5:
                y[i] = 1  # Класс 1
            else:
                y[i] = 0  # Класс 0
    
    print("=== Пример использования LSTM ===")
    
    # Обучение модели
    model, metrics, history = train_lstm_model(
        X, y, 
        sequence_length=sequence_length, 
        epochs=50
    )
    
    # Визуализация истории обучения
    plot_lstm_training_history(history)
    
    return model, metrics

# Запуск примера (раскомментируйте для тестирования)
# model, metrics = example_lstm_usage()
```

## Валидация моделей

**Теория:** Валидация моделей для финансовых данных критически важна, так как стандартные методы кросс-валидации могут привести к data leakage (утечке данных) из-за временной природы финансовых данных.

**Почему стандартная кросс-валидация не подходит:**
- **Data Leakage:** Будущие данные могут "протекать" в обучающую выборку
- **Временная зависимость:** Финансовые данные имеют временную структуру
- **Нестационарность:** Распределения меняются во времени
- **Реалистичность:** Нужно имитировать реальные торговые условия

### 1. Time Series Cross Validation

**Теория:** Time Series Cross Validation (TSCV) - это специальный метод валидации для временных рядов, который предотвращает data leakage, используя только прошлые данные для предсказания будущих.

**Принцип работы TSCV:**
1. **Временное разделение:** Данные разделяются по времени, а не случайно
2. **Строгая последовательность:** Каждая следующая выборка включает предыдущие
3. **Реалистичность:** Имитирует реальные условия торговли
4. **Предотвращение leakage:** Будущие данные никогда не используются для обучения

**Практическая реализация TSCV:**

**Что делает этот код:**
1. **Временное разделение:** Создает временные фолды без пересечений
2. **Обучение на истории:** Каждая модель обучается только на прошлых данных
3. **Тестирование на будущем:** Предсказания делаются на будущих данных
4. **Метрики:** Вычисляет различные метрики для каждого фолда

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix, classification_report)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def time_series_cv(model, X, y, n_splits=5, test_size=None, random_state=42):
    """
    Кросс-валидация для временных рядов
    
    Args:
        model: Модель для валидации (должна иметь методы fit и predict)
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        n_splits: Количество фолдов
        test_size: Размер тестового фолда (если None, вычисляется автоматически)
        random_state: Seed для воспроизводимости
    
    Returns:
        dict: Результаты валидации с метриками для каждого фолда
    """
    
    print("=== Time Series Cross Validation ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Количество фолдов: {n_splits}")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Создание TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)
    
    # Списки для хранения результатов
    fold_scores = []
    fold_predictions = []
    fold_confusion_matrices = []
    
    print(f"\nНачало валидации...")
    
    for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
        print(f"\n--- Fold {fold + 1}/{n_splits} ---")
        
        # Разделение данных
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        print(f"Train size: {len(train_idx)} ({len(train_idx)/len(X)*100:.1f}%)")
        print(f"Test size: {len(test_idx)} ({len(test_idx)/len(X)*100:.1f}%)")
        print(f"Train period: {train_idx[0]} - {train_idx[-1]}")
        print(f"Test period: {test_idx[0]} - {test_idx[-1]}")
        
        # Создание копии модели для каждого фолда
        fold_model = type(model)(**model.get_params())
        
        # Обучение модели
        print("Обучение модели...")
        fold_model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = fold_model.predict(X_test)
        y_pred_proba = fold_model.predict_proba(X_test) if hasattr(fold_model, 'predict_proba') else None
        
        # Вычисление метрик
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Матрица ошибок
        cm = confusion_matrix(y_test, y_pred)
        
        # Сохранение результатов
        fold_score = {
            'fold': fold + 1,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'train_size': len(train_idx),
            'test_size': len(test_idx)
        }
        
        fold_scores.append(fold_score)
        fold_predictions.append({
            'y_true': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        })
        fold_confusion_matrices.append(cm)
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1: {f1:.4f}")
    
    # Агрегированные результаты
    results = {
        'fold_scores': fold_scores,
        'fold_predictions': fold_predictions,
        'fold_confusion_matrices': fold_confusion_matrices,
        'mean_accuracy': np.mean([s['accuracy'] for s in fold_scores]),
        'std_accuracy': np.std([s['accuracy'] for s in fold_scores]),
        'mean_precision': np.mean([s['precision'] for s in fold_scores]),
        'mean_recall': np.mean([s['recall'] for s in fold_scores]),
        'mean_f1': np.mean([s['f1'] for s in fold_scores])
    }
    
    # Вывод итоговых результатов
    print(f"\n=== Итоговые результаты TSCV ===")
    print(f"Mean Accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
    print(f"Mean Precision: {results['mean_precision']:.4f}")
    print(f"Mean Recall: {results['mean_recall']:.4f}")
    print(f"Mean F1: {results['mean_f1']:.4f}")
    
    return results

def plot_tscv_results(results, figsize=(15, 10)):
    """Визуализация результатов Time Series Cross Validation"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Извлечение данных
    fold_scores = results['fold_scores']
    folds = [s['fold'] for s in fold_scores]
    accuracies = [s['accuracy'] for s in fold_scores]
    precisions = [s['precision'] for s in fold_scores]
    recalls = [s['recall'] for s in fold_scores]
    f1_scores = [s['f1'] for s in fold_scores]
    
    # График точности по фолдам
    axes[0, 0].plot(folds, accuracies, 'o-', label='Accuracy')
    axes[0, 0].axhline(y=results['mean_accuracy'], color='r', linestyle='--', 
                      label=f'Mean: {results["mean_accuracy"]:.3f}')
    axes[0, 0].set_title('Accuracy by Fold')
    axes[0, 0].set_xlabel('Fold')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # График метрик по фолдам
    axes[0, 1].plot(folds, accuracies, 'o-', label='Accuracy')
    axes[0, 1].plot(folds, precisions, 's-', label='Precision')
    axes[0, 1].plot(folds, recalls, '^-', label='Recall')
    axes[0, 1].plot(folds, f1_scores, 'd-', label='F1')
    axes[0, 1].set_title('Metrics by Fold')
    axes[0, 1].set_xlabel('Fold')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Box plot метрик
    metrics_data = [accuracies, precisions, recalls, f1_scores]
    metrics_labels = ['Accuracy', 'Precision', 'Recall', 'F1']
    axes[1, 0].boxplot(metrics_data, labels=metrics_labels)
    axes[1, 0].set_title('Distribution of Metrics')
    axes[1, 0].set_ylabel('Score')
    axes[1, 0].grid(True)
    
    # Агрегированная матрица ошибок
    if results['fold_confusion_matrices']:
        # Суммируем все матрицы ошибок
        total_cm = np.sum(results['fold_confusion_matrices'], axis=0)
        
        # Нормализуем для процентов
        total_cm_norm = total_cm.astype('float') / total_cm.sum(axis=1)[:, np.newaxis]
        
        sns.heatmap(total_cm_norm, annot=True, fmt='.2f', cmap='Blues', ax=axes[1, 1])
        axes[1, 1].set_title('Aggregated Confusion Matrix')
        axes[1, 1].set_xlabel('Predicted')
        axes[1, 1].set_ylabel('True')
    
    plt.tight_layout()
    plt.show()

def analyze_tscv_stability(results):
    """Анализ стабильности результатов TSCV"""
    
    fold_scores = results['fold_scores']
    accuracies = [s['accuracy'] for s in fold_scores]
    
    print("=== Анализ стабильности TSCV ===")
    print(f"Accuracy - Min: {min(accuracies):.4f}, Max: {max(accuracies):.4f}")
    print(f"Accuracy - Range: {max(accuracies) - min(accuracies):.4f}")
    print(f"Accuracy - Std: {np.std(accuracies):.4f}")
    print(f"Accuracy - CV: {np.std(accuracies) / np.mean(accuracies):.4f}")
    
    # Анализ тренда
    if len(accuracies) >= 3:
        # Проверяем, есть ли тренд (улучшение/ухудшение со временем)
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(accuracies)), accuracies)
        
        print(f"\nТренд точности:")
        print(f"Slope: {slope:.6f} (положительный = улучшение)")
        print(f"R-squared: {r_value**2:.4f}")
        print(f"P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            if slope > 0:
                print("Статистически значимое улучшение со временем")
            else:
                print("Статистически значимое ухудшение со временем")
        else:
            print("Нет статистически значимого тренда")

# Пример использования:
def example_tscv_usage():
    """Пример использования Time Series Cross Validation"""
    
    from sklearn.ensemble import RandomForestClassifier
    
    # Создание синтетических временных данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков с временной структурой
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с временными зависимостями
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Временная зависимость
        if i < 100:
            y[i] = 0
        elif i < 500:
            y[i] = 1 if X[i, 0] > 0 else 0
        else:
            y[i] = 2 if X[i, 0] > 0.5 else (1 if X[i, 0] > -0.5 else 0)
    
    print("=== Пример Time Series Cross Validation ===")
    
    # Создание модели
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    
    # Выполнение TSCV
    results = time_series_cv(model, X, y, n_splits=5)
    
    # Визуализация результатов
    plot_tscv_results(results)
    
    # Анализ стабильности
    analyze_tscv_stability(results)
    
    return results

# Запуск примера (раскомментируйте для тестирования)
# results = example_tscv_usage()
```

### 2. Walk-Forward Validation

**Теория:** Walk-Forward Validation (WFV) - это метод валидации, который имитирует реальные торговые условия, где модель постоянно переобучается на новых данных и делает предсказания на следующий период.

**Принцип работы WFV:**
1. **Скользящее окно:** Обучающая выборка имеет фиксированный размер
2. **Пошаговое продвижение:** Окно сдвигается на фиксированный шаг
3. **Реалистичность:** Имитирует реальные торговые условия
4. **Адаптивность:** Модель адаптируется к новым данным

**Почему WFV эффективен для финансов:**
- **Реалистичность:** Точно имитирует реальные торговые условия
- **Адаптивность:** Модель постоянно обновляется
- **Стабильность:** Показывает, как модель работает в долгосрочной перспективе
- **Дрейф данных:** Помогает выявить, когда модель устаревает

**Практическая реализация WFV:**

**Что делает этот код:**
1. **Скользящее окно:** Создает обучающие выборки фиксированного размера
2. **Пошаговое тестирование:** Тестирует модель на следующих данных
3. **Переобучение:** Модель переобучается на каждом шаге
4. **Метрики:** Отслеживает производительность во времени

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def walk_forward_validation(model, X, y, train_size=1000, step_size=100, 
                          min_test_size=50, random_state=42):
    """
    Walk-Forward валидация для временных рядов
    
    Args:
        model: Модель для валидации (должна иметь методы fit и predict)
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        train_size: Размер обучающего окна
        step_size: Размер шага для продвижения окна
        min_test_size: Минимальный размер тестовой выборки
        random_state: Seed для воспроизводимости
    
    Returns:
        dict: Результаты walk-forward валидации
    """
    
    print("=== Walk-Forward Validation ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Размер обучающего окна: {train_size}")
    print(f"Размер шага: {step_size}")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Вычисление количества итераций
    n_iterations = (len(X) - train_size) // step_size
    print(f"Количество итераций: {n_iterations}")
    
    # Списки для хранения результатов
    iteration_results = []
    all_predictions = []
    all_true_labels = []
    
    print(f"\nНачало walk-forward валидации...")
    
    for i in range(n_iterations):
        start_idx = i * step_size
        train_end_idx = start_idx + train_size
        test_start_idx = train_end_idx
        test_end_idx = min(test_start_idx + step_size, len(X))
        
        # Проверка минимального размера тестовой выборки
        if test_end_idx - test_start_idx < min_test_size:
            print(f"Итерация {i+1}: Недостаточно данных для тестирования, пропускаем")
            continue
        
        print(f"\n--- Итерация {i+1}/{n_iterations} ---")
        print(f"Обучающий период: {start_idx} - {train_end_idx-1}")
        print(f"Тестовый период: {test_start_idx} - {test_end_idx-1}")
        
        # Разделение данных
        X_train = X[start_idx:train_end_idx]
        y_train = y[start_idx:train_end_idx]
        X_test = X[test_start_idx:test_end_idx]
        y_test = y[test_start_idx:test_end_idx]
        
        print(f"Train size: {len(X_train)}")
        print(f"Test size: {len(X_test)}")
        
        # Создание копии модели для каждой итерации
        fold_model = type(model)(**model.get_params())
        
        # Обучение модели
        print("Обучение модели...")
        fold_model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = fold_model.predict(X_test)
        y_pred_proba = fold_model.predict_proba(X_test) if hasattr(fold_model, 'predict_proba') else None
        
        # Вычисление метрик
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # Матрица ошибок
        cm = confusion_matrix(y_test, y_pred)
        
        # Сохранение результатов
        iteration_result = {
            'iteration': i + 1,
            'train_start': start_idx,
            'train_end': train_end_idx - 1,
            'test_start': test_start_idx,
            'test_end': test_end_idx - 1,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'train_size': len(X_train),
            'test_size': len(X_test),
            'confusion_matrix': cm
        }
        
        iteration_results.append(iteration_result)
        all_predictions.extend(y_pred)
        all_true_labels.extend(y_test)
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1: {f1:.4f}")
    
    # Агрегированные результаты
    if iteration_results:
        accuracies = [r['accuracy'] for r in iteration_results]
        precisions = [r['precision'] for r in iteration_results]
        recalls = [r['recall'] for r in iteration_results]
        f1_scores = [r['f1'] for r in iteration_results]
        
        results = {
            'iteration_results': iteration_results,
            'all_predictions': np.array(all_predictions),
            'all_true_labels': np.array(all_true_labels),
            'mean_accuracy': np.mean(accuracies),
            'std_accuracy': np.std(accuracies),
            'mean_precision': np.mean(precisions),
            'mean_recall': np.mean(recalls),
            'mean_f1': np.mean(f1_scores),
            'n_iterations': len(iteration_results)
        }
        
        # Вывод итоговых результатов
        print(f"\n=== Итоговые результаты Walk-Forward ===")
        print(f"Количество итераций: {results['n_iterations']}")
        print(f"Mean Accuracy: {results['mean_accuracy']:.4f} ± {results['std_accuracy']:.4f}")
        print(f"Mean Precision: {results['mean_precision']:.4f}")
        print(f"Mean Recall: {results['mean_recall']:.4f}")
        print(f"Mean F1: {results['mean_f1']:.4f}")
        
        # Общая точность по всем предсказаниям
        overall_accuracy = accuracy_score(all_true_labels, all_predictions)
        print(f"Overall Accuracy: {overall_accuracy:.4f}")
        
    else:
        print("Нет результатов для анализа")
        results = None
    
    return results

def plot_walk_forward_results(results, figsize=(15, 12)):
    """Визуализация результатов Walk-Forward валидации"""
    
    if results is None:
        print("Нет данных для визуализации")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Извлечение данных
    iteration_results = results['iteration_results']
    iterations = [r['iteration'] for r in iteration_results]
    accuracies = [r['accuracy'] for r in iteration_results]
    precisions = [r['precision'] for r in iteration_results]
    recalls = [r['recall'] for r in iteration_results]
    f1_scores = [r['f1'] for r in iteration_results]
    
    # График точности по итерациям
    axes[0, 0].plot(iterations, accuracies, 'o-', label='Accuracy')
    axes[0, 0].axhline(y=results['mean_accuracy'], color='r', linestyle='--', 
                      label=f'Mean: {results["mean_accuracy"]:.3f}')
    axes[0, 0].set_title('Accuracy by Iteration')
    axes[0, 0].set_xlabel('Iteration')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # График всех метрик по итерациям
    axes[0, 1].plot(iterations, accuracies, 'o-', label='Accuracy')
    axes[0, 1].plot(iterations, precisions, 's-', label='Precision')
    axes[0, 1].plot(iterations, recalls, '^-', label='Recall')
    axes[0, 1].plot(iterations, f1_scores, 'd-', label='F1')
    axes[0, 1].set_title('Metrics by Iteration')
    axes[0, 1].set_xlabel('Iteration')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Скользящее среднее точности
    window_size = max(1, len(accuracies) // 5)  # 20% от общего количества итераций
    if window_size > 1:
        rolling_accuracy = pd.Series(accuracies).rolling(window=window_size).mean()
        axes[1, 0].plot(iterations, accuracies, 'o-', alpha=0.3, label='Raw Accuracy')
        axes[1, 0].plot(iterations, rolling_accuracy, 'r-', linewidth=2, 
                       label=f'Rolling Mean (window={window_size})')
        axes[1, 0].set_title('Accuracy with Rolling Mean')
        axes[1, 0].set_xlabel('Iteration')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
    else:
        axes[1, 0].plot(iterations, accuracies, 'o-')
        axes[1, 0].set_title('Accuracy by Iteration')
        axes[1, 0].set_xlabel('Iteration')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].grid(True)
    
    # Общая матрица ошибок
    if len(results['all_true_labels']) > 0:
        overall_cm = confusion_matrix(results['all_true_labels'], results['all_predictions'])
        overall_cm_norm = overall_cm.astype('float') / overall_cm.sum(axis=1)[:, np.newaxis]
        
        sns.heatmap(overall_cm_norm, annot=True, fmt='.2f', cmap='Blues', ax=axes[1, 1])
        axes[1, 1].set_title('Overall Confusion Matrix')
        axes[1, 1].set_xlabel('Predicted')
        axes[1, 1].set_ylabel('True')
    
    plt.tight_layout()
    plt.show()

def analyze_walk_forward_stability(results):
    """Анализ стабильности результатов Walk-Forward валидации"""
    
    if results is None:
        print("Нет данных для анализа")
        return
    
    iteration_results = results['iteration_results']
    accuracies = [r['accuracy'] for r in iteration_results]
    
    print("=== Анализ стабильности Walk-Forward ===")
    print(f"Accuracy - Min: {min(accuracies):.4f}, Max: {max(accuracies):.4f}")
    print(f"Accuracy - Range: {max(accuracies) - min(accuracies):.4f}")
    print(f"Accuracy - Std: {np.std(accuracies):.4f}")
    print(f"Accuracy - CV: {np.std(accuracies) / np.mean(accuracies):.4f}")
    
    # Анализ тренда
    if len(accuracies) >= 3:
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(accuracies)), accuracies)
        
        print(f"\nТренд точности:")
        print(f"Slope: {slope:.6f} (положительный = улучшение)")
        print(f"R-squared: {r_value**2:.4f}")
        print(f"P-value: {p_value:.4f}")
        
        if p_value < 0.05:
            if slope > 0:
                print("Статистически значимое улучшение со временем")
            else:
                print("Статистически значимое ухудшение со временем")
        else:
            print("Нет статистически значимого тренда")
    
    # Анализ стабильности (скользящее окно)
    if len(accuracies) >= 10:
        window_size = max(3, len(accuracies) // 5)
        rolling_std = pd.Series(accuracies).rolling(window=window_size).std()
        
        print(f"\nСтабильность (скользящее стандартное отклонение, окно={window_size}):")
        print(f"Mean Rolling Std: {rolling_std.mean():.4f}")
        print(f"Max Rolling Std: {rolling_std.max():.4f}")
        
        # Проверка на деградацию производительности
        recent_acc = np.mean(accuracies[-window_size:])
        early_acc = np.mean(accuracies[:window_size])
        degradation = early_acc - recent_acc
        
        print(f"\nДеградация производительности:")
        print(f"Early accuracy: {early_acc:.4f}")
        print(f"Recent accuracy: {recent_acc:.4f}")
        print(f"Degradation: {degradation:.4f}")
        
        if degradation > 0.05:  # 5% деградация
            print("⚠️  ВНИМАНИЕ: Значительная деградация производительности!")
        elif degradation > 0.02:  # 2% деградация
            print("⚠️  Предупреждение: Умеренная деградация производительности")
        else:
            print("✅ Производительность стабильна")

# Пример использования:
def example_walk_forward_usage():
    """Пример использования Walk-Forward валидации"""
    
    from sklearn.ensemble import RandomForestClassifier
    
    # Создание синтетических временных данных
    np.random.seed(42)
    n_samples, n_features = 2000, 20
    
    # Генерация признаков с временной структурой
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной с временными зависимостями и дрейфом
    y = np.zeros(n_samples)
    for i in range(n_samples):
        # Дрейф: паттерны меняются со временем
        if i < 500:
            # Ранний период: простые паттерны
            y[i] = 1 if X[i, 0] > 0 else 0
        elif i < 1000:
            # Средний период: более сложные паттерны
            y[i] = 2 if X[i, 0] > 0.5 else (1 if X[i, 0] > -0.5 else 0)
        else:
            # Поздний период: паттерны снова меняются
            y[i] = 1 if X[i, 0] > -0.2 else (2 if X[i, 0] > 0.8 else 0)
    
    print("=== Пример Walk-Forward валидации ===")
    
    # Создание модели
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    
    # Выполнение Walk-Forward валидации
    results = walk_forward_validation(
        model, X, y, 
        train_size=500, 
        step_size=100
    )
    
    # Визуализация результатов
    plot_walk_forward_results(results)
    
    # Анализ стабильности
    analyze_walk_forward_stability(results)
    
    return results

# Запуск примера (раскомментируйте для тестирования)
# results = example_walk_forward_usage()
```

## Гиперпараметрическая оптимизация

**Теория:** Гиперпараметрическая оптимизация - это процесс поиска наилучших параметров модели для достижения максимальной производительности. Для финансовых данных это критически важно, так как неправильные параметры могут привести к переобучению или недообучению.

**Почему оптимизация важна для финансов:**
- **Переобучение:** Финансовые данные склонны к переобучению
- **Стабильность:** Правильные параметры обеспечивают стабильность
- **Производительность:** Оптимальные параметры улучшают точность
- **Риск-доходность:** Баланс между точностью и стабильностью

**Методы оптимизации:**
1. **Grid Search:** Полный перебор всех комбинаций параметров
2. **Random Search:** Случайный поиск в пространстве параметров
3. **Bayesian Optimization:** Умный поиск с использованием предыдущих результатов
4. **Optuna:** Современная библиотека для оптимизации

### 1. Grid Search

**Теория:** Grid Search - это метод полного перебора, который тестирует все возможные комбинации параметров из заданной сетки. Хотя он может быть вычислительно дорогим, он гарантирует нахождение оптимальных параметров в заданном пространстве.

**Принцип работы Grid Search:**
1. **Определение сетки:** Задается диапазон значений для каждого параметра
2. **Полный перебор:** Тестируются все комбинации параметров
3. **Кросс-валидация:** Каждая комбинация оценивается с помощью CV
4. **Выбор лучших:** Выбирается комбинация с лучшей производительностью

**Плюсы Grid Search:**
- Гарантирует нахождение оптимальных параметров в сетке
- Простой в понимании и реализации
- Хорошо работает с небольшими пространствами параметров

**Минусы Grid Search:**
- Вычислительно дорогой
- Не масштабируется на большие пространства параметров
- Может быть неэффективным для непрерывных параметров

**Практическая реализация Grid Search:**

**Что делает этот код:**
1. **Определение сетки:** Создает сетку параметров для Random Forest
2. **Кросс-валидация:** Использует Time Series CV для финансовых данных
3. **Поиск:** Тестирует все комбинации параметров
4. **Оценка:** Возвращает лучшую модель и параметры

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple

def optimize_random_forest(X, y, param_grid=None, cv_folds=5, 
                          scoring='accuracy', n_jobs=-1, random_state=42):
    """
    Оптимизация Random Forest с помощью Grid Search
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        param_grid: Сетка параметров для поиска
        cv_folds: Количество фолдов для кросс-валидации
        scoring: Метрика для оценки
        n_jobs: Количество параллельных процессов
        random_state: Seed для воспроизводимости
    
    Returns:
        tuple: (лучшая модель, лучшие параметры, результаты поиска)
    """
    
    print("=== Grid Search для Random Forest ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # Сетка параметров по умолчанию
    if param_grid is None:
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None]
        }
    
    print(f"\nСетка параметров:")
    for param, values in param_grid.items():
        print(f"{param}: {values}")
    
    # Подсчет общего количества комбинаций
    total_combinations = 1
    for values in param_grid.values():
        total_combinations *= len(values)
    print(f"Всего комбинаций: {total_combinations}")
    print(f"Всего тестов: {total_combinations * cv_folds}")
    
    # Создание базовой модели
    rf = RandomForestClassifier(random_state=random_state, n_jobs=1)
    
    # Создание Time Series CV для финансовых данных
    tscv = TimeSeriesSplit(n_splits=cv_folds)
    
    # Grid Search
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=tscv,
        scoring=scoring,
        n_jobs=n_jobs,
        verbose=1,
        return_train_score=True
    )
    
    print(f"\nНачало Grid Search...")
    grid_search.fit(X, y)
    
    # Результаты
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_
    
    print(f"\n=== Результаты Grid Search ===")
    print(f"Лучшая точность: {best_score:.4f}")
    print(f"Лучшие параметры:")
    for param, value in best_params.items():
        print(f"  {param}: {value}")
    
    # Анализ результатов
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    # Топ-5 комбинаций
    top_results = results_df.nlargest(5, 'mean_test_score')[
        ['params', 'mean_test_score', 'std_test_score']
    ]
    
    print(f"\nТоп-5 комбинаций:")
    for i, (_, row) in enumerate(top_results.iterrows(), 1):
        print(f"{i}. Score: {row['mean_test_score']:.4f} ± {row['std_test_score']:.4f}")
        print(f"   Params: {row['params']}")
    
    return best_model, best_params, grid_search

def plot_grid_search_results(grid_search, param_name, figsize=(12, 8)):
    """Визуализация результатов Grid Search для одного параметра"""
    
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    # Фильтрация по параметру
    param_results = results_df[results_df['param_' + param_name].notna()]
    
    if param_results.empty:
        print(f"Нет данных для параметра {param_name}")
        return
    
    # Группировка по значениям параметра
    param_values = param_results['param_' + param_name].unique()
    mean_scores = []
    std_scores = []
    
    for value in param_values:
        value_results = param_results[param_results['param_' + param_name] == value]
        mean_scores.append(value_results['mean_test_score'].mean())
        std_scores.append(value_results['std_test_score'].mean())
    
    # Создание графика
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # График средних значений
    ax1.errorbar(param_values, mean_scores, yerr=std_scores, 
                marker='o', capsize=5, capthick=2)
    ax1.set_title(f'Grid Search Results: {param_name}')
    ax1.set_xlabel(param_name)
    ax1.set_ylabel('Mean Test Score')
    ax1.grid(True, alpha=0.3)
    
    # График стандартных отклонений
    ax2.bar(param_values, std_scores, alpha=0.7)
    ax2.set_title(f'Score Variability: {param_name}')
    ax2.set_xlabel(param_name)
    ax2.set_ylabel('Std Test Score')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_grid_search_stability(grid_search):
    """Анализ стабильности результатов Grid Search"""
    
    results_df = pd.DataFrame(grid_search.cv_results_)
    
    print("=== Анализ стабильности Grid Search ===")
    
    # Лучшие результаты
    best_score = grid_search.best_score_
    best_std = results_df.loc[grid_search.best_index_, 'std_test_score']
    
    print(f"Лучший результат:")
    print(f"  Score: {best_score:.4f} ± {best_std:.4f}")
    print(f"  CV: {best_std / best_score:.4f}")
    
    # Анализ стабильности
    all_scores = results_df['mean_test_score']
    all_stds = results_df['std_test_score']
    
    print(f"\nОбщая статистика:")
    print(f"  Score range: {all_scores.min():.4f} - {all_scores.max():.4f}")
    print(f"  Mean std: {all_stds.mean():.4f}")
    print(f"  Max std: {all_stds.max():.4f}")
    
    # Топ-10 результатов
    top_10 = results_df.nlargest(10, 'mean_test_score')
    
    print(f"\nТоп-10 результатов:")
    for i, (_, row) in enumerate(top_10.iterrows(), 1):
        print(f"{i:2d}. {row['mean_test_score']:.4f} ± {row['std_test_score']:.4f} - {row['params']}")

# Пример использования:
def example_grid_search_usage():
    """Пример использования Grid Search"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2
        else:
            y[i] = 0
    
    print("=== Пример Grid Search ===")
    
    # Простая сетка для демонстрации
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [5, 10],
        'min_samples_split': [2, 5]
    }
    
    # Выполнение Grid Search
    best_model, best_params, grid_search = optimize_random_forest(
        X, y, param_grid=param_grid, cv_folds=3
    )
    
    # Анализ результатов
    analyze_grid_search_stability(grid_search)
    
    # Визуализация (если есть данные)
    if 'n_estimators' in best_params:
        plot_grid_search_results(grid_search, 'n_estimators')
    
    return best_model, best_params, grid_search

# Запуск примера (раскомментируйте для тестирования)
# best_model, best_params, grid_search = example_grid_search_usage()
```

### 2. Optuna оптимизация

**Теория:** Optuna - это современная библиотека для гиперпараметрической оптимизации, которая использует Bayesian Optimization и другие продвинутые методы для эффективного поиска оптимальных параметров.

**Принцип работы Optuna:**
1. **Bayesian Optimization:** Использует предыдущие результаты для выбора следующих параметров
2. **Tree-structured Parzen Estimator (TPE):** Эффективный алгоритм для оптимизации
3. **Pruning:** Прекращает неперспективные испытания раньше
4. **Параллелизация:** Поддерживает параллельное выполнение испытаний

**Почему Optuna эффективен для финансов:**
- **Эффективность:** Находит хорошие параметры быстрее Grid Search
- **Масштабируемость:** Работает с большими пространствами параметров
- **Pruning:** Экономит вычислительные ресурсы
- **Гибкость:** Легко настраивается под конкретные задачи

**Практическая реализация Optuna:**

**Что делает этот код:**
1. **Определение пространства:** Создает пространство поиска параметров
2. **Objective функция:** Определяет функцию для оптимизации
3. **Испытания:** Выполняет множество испытаний с разными параметрами
4. **Pruning:** Прекращает неперспективные испытания

```python
import numpy as np
import pandas as pd
import optuna
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

def optimize_xgboost_optuna(X, y, n_trials=100, cv_folds=5, 
                           timeout=None, n_jobs=1, random_state=42):
    """
    Оптимизация XGBoost с помощью Optuna
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        n_trials: Количество испытаний
        cv_folds: Количество фолдов для кросс-валидации
        timeout: Максимальное время оптимизации в секундах
        n_jobs: Количество параллельных процессов
        random_state: Seed для воспроизводимости
    
    Returns:
        tuple: (лучшие параметры, объект study, лучшая модель)
    """
    
    print("=== Optuna оптимизация XGBoost ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    print(f"Количество испытаний: {n_trials}")
    
    # Создание Time Series CV для финансовых данных
    tscv = TimeSeriesSplit(n_splits=cv_folds)
    
    def objective(trial):
        """Objective функция для Optuna"""
        
        # Определение пространства параметров
        params = {
            'objective': 'multi:softprob',
            'num_class': len(np.unique(y)),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
            'n_estimators': trial.suggest_int('n_estimators', 50, 500),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
            'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'gamma': trial.suggest_float('gamma', 0.0, 5.0),
            'random_state': random_state,
            'n_jobs': 1,
            'verbosity': 0
        }
        
        # Создание модели
        model = xgb.XGBClassifier(**params)
        
        # Кросс-валидация
        try:
            scores = cross_val_score(
                model, X, y, 
                cv=tscv, 
                scoring='accuracy',
                n_jobs=1
            )
            return scores.mean()
        except Exception as e:
            # Возвращаем плохой результат при ошибке
            return 0.0
    
    # Создание study
    study = optuna.create_study(
        direction='maximize',
        sampler=optuna.samplers.TPESampler(seed=random_state),
        pruner=optuna.pruners.MedianPruner(
            n_startup_trials=10,
            n_warmup_steps=5,
            interval_steps=1
        )
    )
    
    # Оптимизация
    print(f"\nНачало оптимизации...")
    study.optimize(
        objective, 
        n_trials=n_trials,
        timeout=timeout,
        n_jobs=n_jobs,
        show_progress_bar=True
    )
    
    # Результаты
    best_params = study.best_params_
    best_score = study.best_value
    
    print(f"\n=== Результаты Optuna ===")
    print(f"Лучшая точность: {best_score:.4f}")
    print(f"Лучшие параметры:")
    for param, value in best_params.items():
        print(f"  {param}: {value}")
    
    # Создание лучшей модели
    best_model = xgb.XGBClassifier(**best_params)
    best_model.fit(X, y)
    
    # Анализ результатов
    print(f"\n=== Анализ оптимизации ===")
    print(f"Количество завершенных испытаний: {len(study.trials)}")
    print(f"Количество прерванных испытаний: {len([t for t in study.trials if t.state == optuna.trial.TrialState.PRUNED])}")
    
    return best_params, study, best_model

def plot_optuna_results(study, figsize=(15, 10)):
    """Визуализация результатов Optuna"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # График истории оптимизации
    trials = study.trials
    trial_numbers = [t.number for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
    values = [t.value for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
    
    axes[0, 0].plot(trial_numbers, values, 'o-', alpha=0.7)
    axes[0, 0].set_title('Optimization History')
    axes[0, 0].set_xlabel('Trial Number')
    axes[0, 0].set_ylabel('Objective Value')
    axes[0, 0].grid(True, alpha=0.3)
    
    # График важности параметров
    try:
        importance = optuna.importance.get_param_importances(study)
        params = list(importance.keys())
        importances = list(importance.values())
        
        axes[0, 1].barh(params, importances)
        axes[0, 1].set_title('Parameter Importance')
        axes[0, 1].set_xlabel('Importance')
        axes[0, 1].grid(True, alpha=0.3)
    except Exception as e:
        axes[0, 1].text(0.5, 0.5, f'Importance not available:\n{str(e)}', 
                       ha='center', va='center', transform=axes[0, 1].transAxes)
        axes[0, 1].set_title('Parameter Importance')
    
    # График распределения значений
    if len(values) > 0:
        axes[1, 0].hist(values, bins=20, alpha=0.7, edgecolor='black')
        axes[1, 0].axvline(np.mean(values), color='red', linestyle='--', 
                          label=f'Mean: {np.mean(values):.4f}')
        axes[1, 0].axvline(np.max(values), color='green', linestyle='--', 
                          label=f'Best: {np.max(values):.4f}')
        axes[1, 0].set_title('Value Distribution')
        axes[1, 0].set_xlabel('Objective Value')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
    
    # График сходимости
    if len(values) > 1:
        best_values = np.maximum.accumulate(values)
        axes[1, 1].plot(trial_numbers, best_values, 'g-', linewidth=2, label='Best Value')
        axes[1, 1].plot(trial_numbers, values, 'o-', alpha=0.3, label='All Values')
        axes[1, 1].set_title('Convergence')
        axes[1, 1].set_xlabel('Trial Number')
        axes[1, 1].set_ylabel('Best Objective Value')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_optuna_study(study):
    """Анализ результатов Optuna study"""
    
    print("=== Анализ Optuna Study ===")
    
    # Основная статистика
    trials = study.trials
    completed_trials = [t for t in trials if t.state == optuna.trial.TrialState.COMPLETE]
    pruned_trials = [t for t in trials if t.state == optuna.trial.TrialState.PRUNED]
    
    print(f"Всего испытаний: {len(trials)}")
    print(f"Завершенных: {len(completed_trials)}")
    print(f"Прерванных: {len(pruned_trials)}")
    
    if completed_trials:
        values = [t.value for t in completed_trials]
        print(f"\nСтатистика значений:")
        print(f"  Лучшее: {max(values):.4f}")
        print(f"  Худшее: {min(values):.4f}")
        print(f"  Среднее: {np.mean(values):.4f}")
        print(f"  Стандартное отклонение: {np.std(values):.4f}")
        
        # Анализ сходимости
        best_values = np.maximum.accumulate(values)
        improvement = best_values[-1] - best_values[0]
        print(f"\nУлучшение: {improvement:.4f}")
        
        # Анализ стабильности
        recent_trials = min(10, len(values))
        recent_values = values[-recent_trials:]
        recent_std = np.std(recent_values)
        print(f"Стабильность (последние {recent_trials} испытаний): {recent_std:.4f}")
    
    # Анализ параметров
    if completed_trials:
        print(f"\nАнализ параметров:")
        param_names = list(completed_trials[0].params.keys())
        
        for param_name in param_names:
            param_values = [t.params[param_name] for t in completed_trials]
            if isinstance(param_values[0], (int, float)):
                print(f"  {param_name}: {min(param_values):.4f} - {max(param_values):.4f}")
            else:
                unique_values = list(set(param_values))
                print(f"  {param_name}: {unique_values}")

# Пример использования:
def example_optuna_usage():
    """Пример использования Optuna"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2
        else:
            y[i] = 0
    
    print("=== Пример Optuna оптимизации ===")
    
    # Выполнение оптимизации
    best_params, study, best_model = optimize_xgboost_optuna(
        X, y, n_trials=50, cv_folds=3
    )
    
    # Визуализация результатов
    plot_optuna_results(study)
    
    # Анализ результатов
    analyze_optuna_study(study)
    
    return best_params, study, best_model

# Запуск примера (раскомментируйте для тестирования)
# best_params, study, best_model = example_optuna_usage()
```

## Реализация ансамблевых методов

**Теория:** Ансамблевые методы комбинируют несколько моделей для улучшения производительности. В финансовой сфере это особенно важно, так как разные модели могут выявлять разные паттерны в данных.

**Почему ансамбли эффективны для финансов:**
- **Снижение риска:** Комбинация моделей снижает риск ошибок
- **Разнообразие:** Разные модели выявляют разные паттерны
- **Стабильность:** Ансамбли более стабильны, чем отдельные модели
- **Робастность:** Устойчивы к выбросам и шуму

**Типы ансамблей:**
1. **Voting:** Простое голосование моделей
2. **Stacking:** Мета-модель обучается на предсказаниях базовых моделей
3. **Blending:** Взвешенная комбинация предсказаний
4. **Bagging:** Обучение на разных подвыборках данных

### 1. Voting Classifier

**Теория:** Voting Classifier - это простой метод ансамблирования, который комбинирует предсказания нескольких моделей через голосование. Может быть hard voting (голосование по классам) или soft voting (голосование по вероятностям).

**Принцип работы Voting:**
1. **Hard Voting:** Каждая модель голосует за класс, выбирается класс с большинством голосов
2. **Soft Voting:** Каждая модель возвращает вероятности, вычисляется среднее и выбирается класс с максимальной вероятностью

**Плюсы Voting:**
- Простота реализации
- Хорошо работает с разнообразными моделями
- Легко интерпретировать

**Минусы Voting:**
- Не учитывает качество отдельных моделей
- Может быть неэффективным при плохих моделях

**Практическая реализация Voting Classifier:**

**Что делает этот код:**
1. **Создание моделей:** Определяет базовые модели для ансамбля
2. **Voting:** Настраивает тип голосования (hard/soft)
3. **Обучение:** Обучает весь ансамбль
4. **Оценка:** Проверяет производительность ансамбля

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def create_ensemble_model(X, y, voting='soft', test_size=0.2, random_state=42):
    """
    Создание ансамблевой модели с Voting Classifier
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        voting: Тип голосования ('hard' или 'soft')
        test_size: Доля тестовых данных
        random_state: Seed для воспроизводимости
    
    Returns:
        tuple: (ансамблевая модель, метрики, индивидуальные модели)
    """
    
    print("=== Создание Voting Ensemble ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    print(f"Тип голосования: {voting}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Создание индивидуальных моделей
    models = {
        'rf': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        ),
        'xgb': xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=random_state,
            n_jobs=-1,
            verbosity=0
        ),
        'lgb': lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=random_state,
            n_jobs=-1,
            verbose=-1
        )
    }
    
    print(f"\nИндивидуальные модели:")
    for name, model in models.items():
        print(f"  {name}: {type(model).__name__}")
    
    # Создание Voting Classifier
    ensemble = VotingClassifier(
        estimators=list(models.items()),
        voting=voting,
        n_jobs=-1
    )
    
    # Обучение ансамбля
    print(f"\nОбучение ансамбля...")
    ensemble.fit(X_train, y_train)
    
    # Предсказания ансамбля
    y_pred_ensemble = ensemble.predict(X_test)
    y_pred_proba_ensemble = ensemble.predict_proba(X_test)
    
    # Оценка ансамбля
    ensemble_accuracy = accuracy_score(y_test, y_pred_ensemble)
    
    print(f"\n=== Результаты ансамбля ===")
    print(f"Ensemble accuracy: {ensemble_accuracy:.4f}")
    
    # Оценка индивидуальных моделей
    individual_scores = {}
    individual_predictions = {}
    
    print(f"\n=== Результаты индивидуальных моделей ===")
    for name, model in models.items():
        # Обучение индивидуальной модели
        model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Оценка
        accuracy = accuracy_score(y_test, y_pred)
        individual_scores[name] = accuracy
        individual_predictions[name] = y_pred
        
        print(f"{name}: {accuracy:.4f}")
    
    # Сравнение результатов
    print(f"\n=== Сравнение результатов ===")
    best_individual = max(individual_scores, key=individual_scores.get)
    best_individual_score = individual_scores[best_individual]
    
    print(f"Лучшая индивидуальная модель: {best_individual} ({best_individual_score:.4f})")
    print(f"Ансамбль: {ensemble_accuracy:.4f}")
    print(f"Улучшение: {ensemble_accuracy - best_individual_score:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Ensemble) ===")
    print(classification_report(y_test, y_pred_ensemble))
    
    # Метрики для возврата
    metrics = {
        'ensemble_accuracy': ensemble_accuracy,
        'individual_scores': individual_scores,
        'best_individual': best_individual,
        'improvement': ensemble_accuracy - best_individual_score,
        'confusion_matrix': confusion_matrix(y_test, y_pred_ensemble),
        'predictions': y_pred_ensemble,
        'probabilities': y_pred_proba_ensemble
    }
    
    return ensemble, metrics, models

def plot_ensemble_comparison(metrics, figsize=(12, 8)):
    """Визуализация сравнения ансамбля и индивидуальных моделей"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # График точности
    models = list(metrics['individual_scores'].keys()) + ['Ensemble']
    scores = list(metrics['individual_scores'].values()) + [metrics['ensemble_accuracy']]
    colors = ['lightblue'] * len(metrics['individual_scores']) + ['red']
    
    bars = ax1.bar(models, scores, color=colors, alpha=0.7)
    ax1.set_title('Model Performance Comparison')
    ax1.set_ylabel('Accuracy')
    ax1.set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{score:.3f}', ha='center', va='bottom')
    
    ax1.grid(True, alpha=0.3)
    
    # График улучшения
    individual_scores = list(metrics['individual_scores'].values())
    ensemble_score = metrics['ensemble_accuracy']
    improvements = [ensemble_score - score for score in individual_scores]
    
    ax2.bar(metrics['individual_scores'].keys(), improvements, 
           color='green', alpha=0.7)
    ax2.set_title('Improvement over Individual Models')
    ax2.set_ylabel('Improvement')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_ensemble_diversity(individual_predictions, y_test):
    """Анализ разнообразия ансамбля"""
    
    print("=== Анализ разнообразия ансамбля ===")
    
    # Вычисление согласованности между моделями
    model_names = list(individual_predictions.keys())
    n_models = len(model_names)
    
    # Матрица согласованности
    agreement_matrix = np.zeros((n_models, n_models))
    
    for i, model1 in enumerate(model_names):
        for j, model2 in enumerate(model_names):
            if i != j:
                agreement = np.mean(individual_predictions[model1] == individual_predictions[model2])
                agreement_matrix[i, j] = agreement
    
    print(f"Матрица согласованности:")
    print(f"Средняя согласованность: {np.mean(agreement_matrix):.4f}")
    print(f"Минимальная согласованность: {np.min(agreement_matrix):.4f}")
    print(f"Максимальная согласованность: {np.max(agreement_matrix):.4f}")
    
    # Анализ ошибок
    correct_predictions = {}
    for name, pred in individual_predictions.items():
        correct_predictions[name] = (pred == y_test)
    
    # Случаи, где все модели ошиблись
    all_wrong = np.all([~correct_predictions[name] for name in model_names], axis=0)
    all_wrong_count = np.sum(all_wrong)
    
    # Случаи, где все модели были правы
    all_correct = np.all([correct_predictions[name] for name in model_names], axis=0)
    all_correct_count = np.sum(all_correct)
    
    print(f"\nАнализ ошибок:")
    print(f"Все модели правы: {all_correct_count} ({all_correct_count/len(y_test)*100:.1f}%)")
    print(f"Все модели ошиблись: {all_wrong_count} ({all_wrong_count/len(y_test)*100:.1f}%)")
    
    # Случаи, где мнения разделились
    mixed_cases = len(y_test) - all_correct_count - all_wrong_count
    print(f"Смешанные случаи: {mixed_cases} ({mixed_cases/len(y_test)*100:.1f}%)")

# Пример использования:
def example_voting_ensemble_usage():
    """Пример использования Voting Ensemble"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2
        else:
            y[i] = 0
    
    print("=== Пример Voting Ensemble ===")
    
    # Создание ансамбля
    ensemble, metrics, models = create_ensemble_model(X, y, voting='soft')
    
    # Визуализация результатов
    plot_ensemble_comparison(metrics)
    
    # Анализ разнообразия
    individual_predictions = {}
    for name, model in models.items():
        individual_predictions[name] = model.predict(X)
    
    analyze_ensemble_diversity(individual_predictions, y)
    
    return ensemble, metrics, models

# Запуск примера (раскомментируйте для тестирования)
# ensemble, metrics, models = example_voting_ensemble_usage()
```

### 2. Stacking

**Теория:** Stacking (Stacked Generalization) - это продвинутый метод ансамблирования, который использует мета-модель для комбинирования предсказаний базовых моделей. Мета-модель обучается на предсказаниях базовых моделей, что позволяет ей находить оптимальные способы их комбинирования.

**Принцип работы Stacking:**
1. **Базовые модели:** Обучаются на исходных данных
2. **Предсказания:** Базовые модели делают предсказания на валидационных данных
3. **Мета-модель:** Обучается на предсказаниях базовых моделей
4. **Финальное предсказание:** Мета-модель комбинирует предсказания базовых моделей

**Плюсы Stacking:**
- Более сложные комбинации моделей
- Мета-модель может выучить нелинейные зависимости
- Часто показывает лучшие результаты, чем Voting

**Минусы Stacking:**
- Более сложная реализация
- Требует больше вычислительных ресурсов
- Может переобучиться при неправильной настройке

**Практическая реализация Stacking:**

**Что делает этот код:**
1. **Базовые модели:** Определяет набор разнообразных моделей
2. **Мета-модель:** Выбирает модель для комбинирования предсказаний
3. **Кросс-валидация:** Использует CV для предотвращения переобучения
4. **Обучение:** Обучает весь стек моделей

```python
import numpy as np
import pandas as pd
from sklearn.ensemble import StackingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Tuple

def create_stacking_model(X, y, test_size=0.2, cv_folds=5, random_state=42):
    """
    Создание Stacking модели
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        test_size: Доля тестовых данных
        cv_folds: Количество фолдов для кросс-валидации
        random_state: Seed для воспроизводимости
    
    Returns:
        tuple: (stacking модель, метрики, базовые модели)
    """
    
    print("=== Создание Stacking модели ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    print(f"Количество фолдов CV: {cv_folds}")
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"Обучающая выборка: {X_train.shape[0]} образцов")
    print(f"Тестовая выборка: {X_test.shape[0]} образцов")
    
    # Создание базовых моделей
    base_models = [
        ('rf', RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            n_jobs=-1
        )),
        ('xgb', xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=random_state,
            n_jobs=-1,
            verbosity=0
        )),
        ('lgb', lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=random_state,
            n_jobs=-1,
            verbose=-1
        )),
        ('svm', SVC(
            probability=True,
            random_state=random_state
        )),
        ('mlp', MLPClassifier(
            hidden_layer_sizes=(100, 50),
            max_iter=500,
            random_state=random_state
        ))
    ]
    
    print(f"\nБазовые модели:")
    for name, model in base_models:
        print(f"  {name}: {type(model).__name__}")
    
    # Создание мета-модели
    meta_models = {
        'logistic': LogisticRegression(random_state=random_state, max_iter=1000),
        'rf_meta': RandomForestClassifier(n_estimators=50, random_state=random_state),
        'xgb_meta': xgb.XGBClassifier(n_estimators=50, random_state=random_state, verbosity=0)
    }
    
    print(f"\nМета-модели:")
    for name, model in meta_models.items():
        print(f"  {name}: {type(model).__name__}")
    
    # Тестирование разных мета-моделей
    best_meta_model = None
    best_score = 0
    meta_scores = {}
    
    print(f"\nТестирование мета-моделей...")
    
    for meta_name, meta_model in meta_models.items():
        # Создание Stacking модели
        stacking_model = StackingClassifier(
            estimators=base_models,
            final_estimator=meta_model,
            cv=cv_folds,
            n_jobs=-1
        )
        
        # Кросс-валидация
        scores = cross_val_score(
            stacking_model, X_train, y_train, 
            cv=cv_folds, scoring='accuracy'
        )
        
        mean_score = scores.mean()
        meta_scores[meta_name] = mean_score
        
        print(f"  {meta_name}: {mean_score:.4f} ± {scores.std():.4f}")
        
        if mean_score > best_score:
            best_score = mean_score
            best_meta_model = meta_model
    
    print(f"\nЛучшая мета-модель: {max(meta_scores, key=meta_scores.get)}")
    
    # Создание финальной Stacking модели
    final_stacking_model = StackingClassifier(
        estimators=base_models,
        final_estimator=best_meta_model,
        cv=cv_folds,
        n_jobs=-1
    )
    
    # Обучение
    print(f"\nОбучение Stacking модели...")
    final_stacking_model.fit(X_train, y_train)
    
    # Предсказания
    y_pred_stacking = final_stacking_model.predict(X_test)
    y_pred_proba_stacking = final_stacking_model.predict_proba(X_test)
    
    # Оценка Stacking модели
    stacking_accuracy = accuracy_score(y_test, y_pred_stacking)
    
    print(f"\n=== Результаты Stacking модели ===")
    print(f"Stacking accuracy: {stacking_accuracy:.4f}")
    
    # Оценка базовых моделей
    base_scores = {}
    base_predictions = {}
    
    print(f"\n=== Результаты базовых моделей ===")
    for name, model in base_models:
        # Обучение базовой модели
        model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Оценка
        accuracy = accuracy_score(y_test, y_pred)
        base_scores[name] = accuracy
        base_predictions[name] = y_pred
        
        print(f"{name}: {accuracy:.4f}")
    
    # Сравнение результатов
    print(f"\n=== Сравнение результатов ===")
    best_base = max(base_scores, key=base_scores.get)
    best_base_score = base_scores[best_base]
    
    print(f"Лучшая базовая модель: {best_base} ({best_base_score:.4f})")
    print(f"Stacking модель: {stacking_accuracy:.4f}")
    print(f"Улучшение: {stacking_accuracy - best_base_score:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Stacking) ===")
    print(classification_report(y_test, y_pred_stacking))
    
    # Метрики для возврата
    metrics = {
        'stacking_accuracy': stacking_accuracy,
        'base_scores': base_scores,
        'meta_scores': meta_scores,
        'best_base': best_base,
        'best_meta': max(meta_scores, key=meta_scores.get),
        'improvement': stacking_accuracy - best_base_score,
        'confusion_matrix': confusion_matrix(y_test, y_pred_stacking),
        'predictions': y_pred_stacking,
        'probabilities': y_pred_proba_stacking
    }
    
    return final_stacking_model, metrics, base_models

def plot_stacking_results(metrics, figsize=(15, 10)):
    """Визуализация результатов Stacking"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # График сравнения базовых моделей и Stacking
    models = list(metrics['base_scores'].keys()) + ['Stacking']
    scores = list(metrics['base_scores'].values()) + [metrics['stacking_accuracy']]
    colors = ['lightblue'] * len(metrics['base_scores']) + ['red']
    
    bars = axes[0, 0].bar(models, scores, color=colors, alpha=0.7)
    axes[0, 0].set_title('Base Models vs Stacking')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{score:.3f}', ha='center', va='bottom')
    
    axes[0, 0].grid(True, alpha=0.3)
    
    # График мета-моделей
    meta_models = list(metrics['meta_scores'].keys())
    meta_scores = list(metrics['meta_scores'].values())
    
    bars = axes[0, 1].bar(meta_models, meta_scores, color='green', alpha=0.7)
    axes[0, 1].set_title('Meta-Model Performance')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, score in zip(bars, meta_scores):
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{score:.3f}', ha='center', va='bottom')
    
    axes[0, 1].grid(True, alpha=0.3)
    
    # График улучшения
    base_scores = list(metrics['base_scores'].values())
    stacking_score = metrics['stacking_accuracy']
    improvements = [stacking_score - score for score in base_scores]
    
    axes[1, 0].bar(metrics['base_scores'].keys(), improvements, 
                  color='orange', alpha=0.7)
    axes[1, 0].set_title('Stacking Improvement over Base Models')
    axes[1, 0].set_ylabel('Improvement')
    axes[1, 0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Матрица ошибок
    cm = metrics['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1])
    axes[1, 1].set_title('Confusion Matrix (Stacking)')
    axes[1, 1].set_xlabel('Predicted')
    axes[1, 1].set_ylabel('True')
    
    plt.tight_layout()
    plt.show()

def analyze_stacking_contribution(stacking_model, X_test, y_test):
    """Анализ вклада базовых моделей в Stacking"""
    
    print("=== Анализ вклада базовых моделей ===")
    
    # Получение предсказаний базовых моделей
    base_predictions = stacking_model.transform(X_test)
    
    # Получение весов мета-модели
    if hasattr(stacking_model.final_estimator_, 'coef_'):
        # Для линейных моделей
        weights = stacking_model.final_estimator_.coef_[0]
        print(f"Веса мета-модели: {weights}")
        
        # Анализ важности базовых моделей
        base_names = [name for name, _ in stacking_model.estimators]
        for name, weight in zip(base_names, weights):
            print(f"  {name}: {weight:.4f}")
    
    # Анализ корреляций между базовыми моделями
    base_predictions_df = pd.DataFrame(
        base_predictions, 
        columns=[name for name, _ in stacking_model.estimators]
    )
    
    correlation_matrix = base_predictions_df.corr()
    
    print(f"\nКорреляционная матрица базовых моделей:")
    print(correlation_matrix.round(3))
    
    # Анализ разнообразия
    mean_correlation = correlation_matrix.values[np.triu_indices_from(correlation_matrix.values, k=1)].mean()
    print(f"\nСредняя корреляция: {mean_correlation:.4f}")
    
    if mean_correlation < 0.5:
        print("✅ Хорошее разнообразие базовых моделей")
    elif mean_correlation < 0.7:
        print("⚠️  Умеренное разнообразие базовых моделей")
    else:
        print("❌ Низкое разнообразие базовых моделей")

# Пример использования:
def example_stacking_usage():
    """Пример использования Stacking"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 1000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2
        else:
            y[i] = 0
    
    print("=== Пример Stacking ===")
    
    # Создание Stacking модели
    stacking_model, metrics, base_models = create_stacking_model(X, y)
    
    # Визуализация результатов
    plot_stacking_results(metrics)
    
    # Анализ вклада базовых моделей
    analyze_stacking_contribution(stacking_model, X, y)
    
    return stacking_model, metrics, base_models

# Запуск примера (раскомментируйте для тестирования)
# stacking_model, metrics, base_models = example_stacking_usage()
```

## Оценка производительности

**Теория:** Оценка производительности моделей для финансовых данных требует особого подхода, так как стандартные метрики могут не отражать реальную эффективность торговой стратегии.

**Почему стандартные метрики недостаточны:**
- **Точность не равна прибыльности:** Высокая точность может не означать прибыльность
- **Классовый дисбаланс:** Финансовые данные часто имеют дисбаланс классов
- **Временная зависимость:** Важна последовательность предсказаний
- **Риск-доходность:** Нужно учитывать риск, а не только доходность

**Типы метрик:**
1. **Классификационные метрики:** Accuracy, Precision, Recall, F1
2. **Торговые метрики:** Sharpe Ratio, Maximum Drawdown, Win Rate
3. **Временные метрики:** Стабильность во времени
4. **Рисковые метрики:** VaR, CVaR, Volatility

### 1. Метрики классификации

**Теория:** Классификационные метрики измеряют качество предсказаний модели на основе правильности классификации образцов по классам.

**Основные метрики:**
- **Accuracy:** Доля правильно классифицированных образцов
- **Precision:** Доля истинно положительных среди предсказанных положительных
- **Recall:** Доля истинно положительных среди всех положительных
- **F1-Score:** Гармоническое среднее Precision и Recall

**Практическая реализация метрик классификации:**

**Что делает этот код:**
1. **Предсказания:** Получает предсказания модели
2. **Вычисление метрик:** Рассчитывает различные метрики качества
3. **Визуализация:** Создает графики для анализа
4. **Анализ:** Интерпретирует результаты

```python
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, confusion_matrix, classification_report,
                           roc_auc_score, roc_curve, precision_recall_curve)
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """
    Комплексная оценка модели
    
    Args:
        model: Обученная модель
        X_test: Тестовые признаки
        y_test: Тестовые метки
        model_name: Название модели для отчетов
    
    Returns:
        dict: Словарь с метриками и результатами
    """
    
    print(f"=== Оценка модели: {model_name} ===")
    print(f"Размер тестовой выборки: {len(y_test)} образцов")
    print(f"Классы: {np.unique(y_test, return_counts=True)}")
    
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
    
    # Основные метрики
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Метрики по классам
    precision_per_class = precision_score(y_test, y_pred, average=None, zero_division=0)
    recall_per_class = recall_score(y_test, y_pred, average=None, zero_division=0)
    f1_per_class = f1_score(y_test, y_pred, average=None, zero_division=0)
    
    # Матрица ошибок
    cm = confusion_matrix(y_test, y_pred)
    
    # ROC AUC (для бинарной классификации)
    roc_auc = None
    if len(np.unique(y_test)) == 2 and y_pred_proba is not None:
        roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
    
    # Результаты
    results = {
        'model_name': model_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'precision_per_class': precision_per_class,
        'recall_per_class': recall_per_class,
        'f1_per_class': f1_per_class,
        'confusion_matrix': cm,
        'roc_auc': roc_auc,
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }
    
    # Вывод результатов
    print(f"\n=== Результаты ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    if roc_auc is not None:
        print(f"ROC AUC: {roc_auc:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report ===")
    print(classification_report(y_test, y_pred))
    
    return results

def plot_classification_metrics(results, figsize=(15, 10)):
    """Визуализация метрик классификации"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Матрица ошибок
    cm = results['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Confusion Matrix')
    axes[0, 0].set_xlabel('Predicted')
    axes[0, 0].set_ylabel('True')
    
    # Метрики по классам
    classes = range(len(results['precision_per_class']))
    x = np.arange(len(classes))
    width = 0.25
    
    axes[0, 1].bar(x - width, results['precision_per_class'], width, label='Precision', alpha=0.8)
    axes[0, 1].bar(x, results['recall_per_class'], width, label='Recall', alpha=0.8)
    axes[0, 1].bar(x + width, results['f1_per_class'], width, label='F1-Score', alpha=0.8)
    
    axes[0, 1].set_title('Metrics per Class')
    axes[0, 1].set_xlabel('Class')
    axes[0, 1].set_ylabel('Score')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(classes)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Общие метрики
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [results['accuracy'], results['precision'], results['recall'], results['f1']]
    
    bars = axes[1, 0].bar(metrics, values, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
    axes[1, 0].set_title('Overall Metrics')
    axes[1, 0].set_ylabel('Score')
    axes[1, 0].set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, values):
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.3f}', ha='center', va='bottom')
    
    axes[1, 0].grid(True, alpha=0.3)
    
    # ROC кривая (если доступна)
    if results['roc_auc'] is not None:
        fpr, tpr, _ = roc_curve(results['y_test'], results['probabilities'][:, 1])
        axes[1, 1].plot(fpr, tpr, color='darkorange', lw=2, 
                       label=f'ROC curve (AUC = {results["roc_auc"]:.2f})')
        axes[1, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        axes[1, 1].set_xlim([0.0, 1.0])
        axes[1, 1].set_ylim([0.0, 1.05])
        axes[1, 1].set_xlabel('False Positive Rate')
        axes[1, 1].set_ylabel('True Positive Rate')
        axes[1, 1].set_title('ROC Curve')
        axes[1, 1].legend(loc="lower right")
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 1].text(0.5, 0.5, 'ROC Curve not available\nfor multiclass problem', 
                       ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('ROC Curve')
    
    plt.tight_layout()
    plt.show()

def analyze_class_balance(y_test, y_pred):
    """Анализ баланса классов"""
    
    print("=== Анализ баланса классов ===")
    
    # Распределение классов
    unique_classes, counts = np.unique(y_test, return_counts=True)
    total_samples = len(y_test)
    
    print(f"Распределение классов в тестовой выборке:")
    for class_label, count in zip(unique_classes, counts):
        percentage = count / total_samples * 100
        print(f"  Класс {class_label}: {count} ({percentage:.1f}%)")
    
    # Анализ предсказаний
    pred_unique, pred_counts = np.unique(y_pred, return_counts=True)
    
    print(f"\nРаспределение предсказаний:")
    for class_label, count in zip(pred_unique, pred_counts):
        percentage = count / total_samples * 100
        print(f"  Класс {class_label}: {count} ({percentage:.1f}%)")
    
    # Анализ дисбаланса
    max_count = max(counts)
    min_count = min(counts)
    imbalance_ratio = max_count / min_count
    
    print(f"\nАнализ дисбаланса:")
    print(f"  Соотношение классов: {imbalance_ratio:.2f}:1")
    
    if imbalance_ratio > 10:
        print("  ⚠️  Сильный дисбаланс классов")
    elif imbalance_ratio > 3:
        print("  ⚠️  Умеренный дисбаланс классов")
    else:
        print("  ✅ Сбалансированные классы")

# Пример использования:
def example_classification_metrics_usage():
    """Пример использования метрик классификации"""
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    
    # Создание синтетических данных
    X, y = make_classification(
        n_samples=1000, n_features=20, n_classes=3, 
        n_informative=15, n_redundant=5, random_state=42
    )
    
    # Разделение данных
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Обучение модели
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("=== Пример метрик классификации ===")
    
    # Оценка модели
    results = evaluate_model(model, X_test, y_test, "Random Forest")
    
    # Визуализация результатов
    plot_classification_metrics(results)
    
    # Анализ баланса классов
    analyze_class_balance(y_test, results['predictions'])
    
    return results

# Запуск примера (раскомментируйте для тестирования)
# results = example_classification_metrics_usage()
```

### 2. Торговые метрики

**Теория:** Торговые метрики измеряют реальную эффективность торговой стратегии, учитывая не только точность предсказаний, но и финансовые результаты.

**Основные торговые метрики:**
- **Sharpe Ratio:** Отношение доходности к риску
- **Maximum Drawdown:** Максимальная потеря от пика
- **Win Rate:** Доля прибыльных сделок
- **Profit Factor:** Отношение прибыли к убыткам
- **Calmar Ratio:** Отношение доходности к максимальной просадке

**Практическая реализация торговых метрик:**

**Что делает этот код:**
1. **Расчет доходности:** Вычисляет прибыльность стратегии
2. **Рисковые метрики:** Оценивает риск стратегии
3. **Торговые показатели:** Анализирует качество торговли
4. **Визуализация:** Создает графики для анализа

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List
from sklearn.metrics import accuracy_score

def calculate_trading_metrics(y_true, y_pred, returns, transaction_costs=0.001):
    """
    Расчет торговых метрик для финансовой стратегии
    
    Args:
        y_true: Истинные классы (0: продажа, 1: удержание, 2: покупка)
        y_pred: Предсказанные классы
        returns: Доходность активов
        transaction_costs: Транзакционные издержки (доля от сделки)
    
    Returns:
        dict: Словарь с торговыми метриками
    """
    
    print("=== Расчет торговых метрик ===")
    print(f"Количество сделок: {len(y_true)}")
    print(f"Транзакционные издержки: {transaction_costs*100:.2f}%")
    
    # Базовые метрики
    accuracy = accuracy_score(y_true, y_pred)
    
    # Создание торговых сигналов
    # 0: продажа (-1), 1: удержание (0), 2: покупка (1)
    signal_mapping = {0: -1, 1: 0, 2: 1}
    y_true_signals = np.array([signal_mapping[label] for label in y_true])
    y_pred_signals = np.array([signal_mapping[label] for label in y_pred])
    
    # Расчет доходности стратегии
    strategy_returns = returns * y_pred_signals
    
    # Учет транзакционных издержек
    position_changes = np.diff(y_pred_signals, prepend=y_pred_signals[0])
    transaction_costs_total = np.abs(position_changes) * transaction_costs
    strategy_returns_net = strategy_returns - transaction_costs_total
    
    # Основные торговые метрики
    total_return = np.sum(strategy_returns_net)
    annualized_return = np.mean(strategy_returns_net) * 252
    
    # Волатильность
    volatility = np.std(strategy_returns_net) * np.sqrt(252)
    
    # Sharpe Ratio
    if volatility > 0:
        sharpe_ratio = annualized_return / volatility
    else:
        sharpe_ratio = 0
    
    # Максимальная просадка
    cumulative_returns = np.cumprod(1 + strategy_returns_net)
    running_max = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = np.min(drawdown)
    
    # Calmar Ratio
    if abs(max_drawdown) > 0:
        calmar_ratio = annualized_return / abs(max_drawdown)
    else:
        calmar_ratio = np.inf
    
    # Win Rate
    profitable_trades = strategy_returns_net > 0
    win_rate = np.mean(profitable_trades) if len(profitable_trades) > 0 else 0
    
    # Profit Factor
    gross_profit = np.sum(strategy_returns_net[strategy_returns_net > 0])
    gross_loss = abs(np.sum(strategy_returns_net[strategy_returns_net < 0]))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf
    
    # Количество сделок
    num_trades = np.sum(np.abs(position_changes))
    
    # Средняя прибыль/убыток
    avg_profit = np.mean(strategy_returns_net[strategy_returns_net > 0]) if np.any(strategy_returns_net > 0) else 0
    avg_loss = np.mean(strategy_returns_net[strategy_returns_net < 0]) if np.any(strategy_returns_net < 0) else 0
    
    # Результаты
    metrics = {
        'accuracy': accuracy,
        'total_return': total_return,
        'annualized_return': annualized_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'calmar_ratio': calmar_ratio,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'num_trades': num_trades,
        'avg_profit': avg_profit,
        'avg_loss': avg_loss,
        'strategy_returns': strategy_returns_net,
        'cumulative_returns': cumulative_returns,
        'drawdown': drawdown
    }
    
    # Вывод результатов
    print(f"\n=== Торговые метрики ===")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Total Return: {total_return:.4f}")
    print(f"Annualized Return: {annualized_return:.4f}")
    print(f"Volatility: {volatility:.4f}")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Max Drawdown: {max_drawdown:.4f}")
    print(f"Calmar Ratio: {calmar_ratio:.4f}")
    print(f"Win Rate: {win_rate:.4f}")
    print(f"Profit Factor: {profit_factor:.4f}")
    print(f"Number of Trades: {num_trades}")
    
    return metrics

def plot_trading_metrics(metrics, figsize=(15, 12)):
    """Визуализация торговых метрик"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Кумулятивная доходность
    cumulative_returns = metrics['cumulative_returns']
    axes[0, 0].plot(cumulative_returns, label='Strategy', linewidth=2)
    axes[0, 0].axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Break-even')
    axes[0, 0].set_title('Cumulative Returns')
    axes[0, 0].set_xlabel('Time')
    axes[0, 0].set_ylabel('Cumulative Return')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Просадка
    drawdown = metrics['drawdown']
    axes[0, 1].fill_between(range(len(drawdown)), drawdown, 0, 
                           color='red', alpha=0.3, label='Drawdown')
    axes[0, 1].plot(drawdown, color='red', linewidth=1)
    axes[0, 1].set_title('Drawdown')
    axes[0, 1].set_xlabel('Time')
    axes[0, 1].set_ylabel('Drawdown')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Распределение доходности
    strategy_returns = metrics['strategy_returns']
    axes[1, 0].hist(strategy_returns, bins=50, alpha=0.7, edgecolor='black')
    axes[1, 0].axvline(x=0, color='red', linestyle='--', alpha=0.7)
    axes[1, 0].set_title('Return Distribution')
    axes[1, 0].set_xlabel('Return')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Основные метрики
    metric_names = ['Sharpe Ratio', 'Calmar Ratio', 'Win Rate', 'Profit Factor']
    metric_values = [
        metrics['sharpe_ratio'],
        metrics['calmar_ratio'],
        metrics['win_rate'],
        metrics['profit_factor']
    ]
    
    # Ограничиваем значения для визуализации
    metric_values_limited = [min(val, 10) if val != np.inf else 10 for val in metric_values]
    
    bars = axes[1, 1].bar(metric_names, metric_values_limited, 
                         color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
    axes[1, 1].set_title('Key Trading Metrics')
    axes[1, 1].set_ylabel('Value')
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, metric_values):
        height = bar.get_height()
        if value == np.inf:
            label = '∞'
        else:
            label = f'{value:.3f}'
        axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       label, ha='center', va='bottom')
    
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_trading_performance(metrics):
    """Анализ торговой производительности"""
    
    print("=== Анализ торговой производительности ===")
    
    # Оценка качества стратегии
    sharpe = metrics['sharpe_ratio']
    calmar = metrics['calmar_ratio']
    win_rate = metrics['win_rate']
    profit_factor = metrics['profit_factor']
    
    print(f"\nОценка качества стратегии:")
    
    # Sharpe Ratio
    if sharpe > 2:
        print(f"✅ Отличный Sharpe Ratio: {sharpe:.3f}")
    elif sharpe > 1:
        print(f"✅ Хороший Sharpe Ratio: {sharpe:.3f}")
    elif sharpe > 0.5:
        print(f"⚠️  Умеренный Sharpe Ratio: {sharpe:.3f}")
    else:
        print(f"❌ Плохой Sharpe Ratio: {sharpe:.3f}")
    
    # Calmar Ratio
    if calmar > 3:
        print(f"✅ Отличный Calmar Ratio: {calmar:.3f}")
    elif calmar > 1:
        print(f"✅ Хороший Calmar Ratio: {calmar:.3f}")
    elif calmar > 0.5:
        print(f"⚠️  Умеренный Calmar Ratio: {calmar:.3f}")
    else:
        print(f"❌ Плохой Calmar Ratio: {calmar:.3f}")
    
    # Win Rate
    if win_rate > 0.6:
        print(f"✅ Высокий Win Rate: {win_rate:.3f}")
    elif win_rate > 0.5:
        print(f"✅ Хороший Win Rate: {win_rate:.3f}")
    elif win_rate > 0.4:
        print(f"⚠️  Умеренный Win Rate: {win_rate:.3f}")
    else:
        print(f"❌ Низкий Win Rate: {win_rate:.3f}")
    
    # Profit Factor
    if profit_factor > 2:
        print(f"✅ Отличный Profit Factor: {profit_factor:.3f}")
    elif profit_factor > 1.5:
        print(f"✅ Хороший Profit Factor: {profit_factor:.3f}")
    elif profit_factor > 1:
        print(f"⚠️  Умеренный Profit Factor: {profit_factor:.3f}")
    else:
        print(f"❌ Плохой Profit Factor: {profit_factor:.3f}")
    
    # Общая оценка
    print(f"\nОбщая оценка:")
    if sharpe > 1 and calmar > 1 and win_rate > 0.5 and profit_factor > 1.5:
        print("🟢 Стратегия показывает отличные результаты")
    elif sharpe > 0.5 and calmar > 0.5 and win_rate > 0.4 and profit_factor > 1:
        print("🟡 Стратегия показывает умеренные результаты")
    else:
        print("🔴 Стратегия требует улучшения")

# Пример использования:
def example_trading_metrics_usage():
    """Пример использования торговых метрик"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples = 1000
    
    # Генерация доходности
    returns = np.random.normal(0.001, 0.02, n_samples)  # 0.1% средняя доходность, 2% волатильность
    
    # Создание истинных классов (стратегия)
    y_true = np.random.choice([0, 1, 2], n_samples, p=[0.3, 0.4, 0.3])
    
    # Создание предсказаний (с некоторой точностью)
    y_pred = y_true.copy()
    # Добавляем ошибки
    error_indices = np.random.choice(n_samples, size=int(n_samples * 0.3), replace=False)
    y_pred[error_indices] = np.random.choice([0, 1, 2], len(error_indices))
    
    print("=== Пример торговых метрик ===")
    
    # Расчет метрик
    metrics = calculate_trading_metrics(y_true, y_pred, returns)
    
    # Визуализация
    plot_trading_metrics(metrics)
    
    # Анализ производительности
    analyze_trading_performance(metrics)
    
    return metrics

# Запуск примера (раскомментируйте для тестирования)
# metrics = example_trading_metrics_usage()
```

## Практический пример

**Теория:** Полный процесс обучения торговой модели включает в себя все этапы: от подготовки данных до оценки производительности. Этот пример демонстрирует комплексный подход к созданию ML-модели для финансовых данных.

**Этапы полного процесса:**
1. **Подготовка данных:** Загрузка и предобработка
2. **Разделение данных:** Train/Validation/Test
3. **Обучение моделей:** Различные алгоритмы
4. **Валидация:** Time Series CV
5. **Оптимизация:** Hyperparameter tuning
6. **Ансамблирование:** Комбинирование моделей
7. **Оценка:** Классификационные и торговые метрики

**Практическая реализация полного процесса:**

**Что делает этот код:**
1. **Полный pipeline:** От данных до готовой модели
2. **Множественные алгоритмы:** Тестирует разные подходы
3. **Валидация:** Использует правильные методы для временных рядов
4. **Оптимизация:** Находит лучшие параметры
5. **Ансамблирование:** Комбинирует лучшие модели
6. **Оценка:** Анализирует производительность

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Tuple, List
import warnings
warnings.filterwarnings('ignore')

def train_complete_trading_model(X, y, returns=None, test_size=0.2, 
                               validation_size=0.2, random_state=42):
    """
    Полное обучение торговой модели
    
    Args:
        X: Матрица признаков (samples, features)
        y: Целевые переменные (samples,)
        returns: Доходность активов (samples,)
        test_size: Доля тестовых данных
        validation_size: Доля валидационных данных
        random_state: Seed для воспроизводимости
    
    Returns:
        dict: Результаты обучения и метрики
    """
    
    print("=== Полное обучение торговой модели ===")
    print(f"Размер данных: {X.shape[0]} образцов, {X.shape[1]} признаков")
    print(f"Классы: {np.unique(y, return_counts=True)}")
    
    # 1. Разделение данных
    print(f"\n1. Разделение данных...")
    
    # Сначала отделяем тестовые данные
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Затем разделяем оставшиеся данные на train и validation
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=validation_size/(1-test_size), 
        random_state=random_state, stratify=y_temp
    )
    
    print(f"  Train: {X_train.shape[0]} образцов")
    print(f"  Validation: {X_val.shape[0]} образцов")
    print(f"  Test: {X_test.shape[0]} образцов")
    
    # 2. Обучение базовых моделей
    print(f"\n2. Обучение базовых моделей...")
    
    models = {}
    model_scores = {}
    
    # Random Forest
    print("  Обучение Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=random_state)
    rf.fit(X_train, y_train)
    rf_score = rf.score(X_val, y_val)
    models['rf'] = rf
    model_scores['rf'] = rf_score
    print(f"    Validation accuracy: {rf_score:.4f}")
    
    # XGBoost
    print("  Обучение XGBoost...")
    xgb_model = xgb.XGBClassifier(n_estimators=100, max_depth=6, random_state=random_state, verbosity=0)
    xgb_model.fit(X_train, y_train)
    xgb_score = xgb_model.score(X_val, y_val)
    models['xgb'] = xgb_model
    model_scores['xgb'] = xgb_score
    print(f"    Validation accuracy: {xgb_score:.4f}")
    
    # LightGBM
    print("  Обучение LightGBM...")
    lgb_model = lgb.LGBMClassifier(n_estimators=100, max_depth=6, random_state=random_state, verbose=-1)
    lgb_model.fit(X_train, y_train)
    lgb_score = lgb_model.score(X_val, y_val)
    models['lgb'] = lgb_model
    model_scores['lgb'] = lgb_score
    print(f"    Validation accuracy: {lgb_score:.4f}")
    
    # 3. Time Series Cross Validation
    print(f"\n3. Time Series Cross Validation...")
    
    # Объединяем train и validation для CV
    X_cv = np.vstack([X_train, X_val])
    y_cv = np.hstack([y_train, y_val])
    
    # Выбираем лучшую модель для CV
    best_model_name = max(model_scores, key=model_scores.get)
    best_model = models[best_model_name]
    
    print(f"  Лучшая модель: {best_model_name} ({model_scores[best_model_name]:.4f})")
    
    # Выполняем TSCV
    tscv = TimeSeriesSplit(n_splits=5)
    cv_scores = []
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X_cv)):
        X_fold_train, X_fold_val = X_cv[train_idx], X_cv[val_idx]
        y_fold_train, y_fold_val = y_cv[train_idx], y_cv[val_idx]
        
        # Создаем копию модели
        fold_model = type(best_model)(**best_model.get_params())
        fold_model.fit(X_fold_train, y_fold_train)
        
        fold_score = fold_model.score(X_fold_val, y_fold_val)
        cv_scores.append(fold_score)
        
        print(f"    Fold {fold+1}: {fold_score:.4f}")
    
    cv_mean = np.mean(cv_scores)
    cv_std = np.std(cv_scores)
    print(f"  CV Mean: {cv_mean:.4f} ± {cv_std:.4f}")
    
    # 4. Создание ансамбля
    print(f"\n4. Создание ансамбля...")
    
    # Выбираем топ-3 модели
    top_models = sorted(model_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    ensemble_models = []
    for name, score in top_models:
        ensemble_models.append((name, models[name]))
        print(f"  {name}: {score:.4f}")
    
    # Создаем Voting Classifier
    ensemble = VotingClassifier(
        estimators=ensemble_models,
        voting='soft',
        n_jobs=-1
    )
    
    # Обучение ансамбля
    ensemble.fit(X_train, y_train)
    ensemble_score = ensemble.score(X_val, y_val)
    print(f"  Ensemble validation accuracy: {ensemble_score:.4f}")
    
    # 5. Оценка на тестовых данных
    print(f"\n5. Оценка на тестовых данных...")
    
    # Предсказания всех моделей
    test_predictions = {}
    test_scores = {}
    
    for name, model in models.items():
        pred = model.predict(X_test)
        score = accuracy_score(y_test, pred)
        test_predictions[name] = pred
        test_scores[name] = score
        print(f"  {name}: {score:.4f}")
    
    # Ансамбль
    ensemble_pred = ensemble.predict(X_test)
    ensemble_score = accuracy_score(y_test, ensemble_pred)
    test_predictions['ensemble'] = ensemble_pred
    test_scores['ensemble'] = ensemble_score
    print(f"  Ensemble: {ensemble_score:.4f}")
    
    # 6. Торговые метрики (если доступны)
    trading_metrics = None
    if returns is not None:
        print(f"\n6. Расчет торговых метрик...")
        
        # Используем только тестовые данные для торговых метрик
        test_returns = returns[-len(y_test):]
        
        # Рассчитываем метрики для ансамбля
        trading_metrics = calculate_trading_metrics(
            y_test, ensemble_pred, test_returns
        )
    
    # 7. Результаты
    print(f"\n=== Итоговые результаты ===")
    print(f"Лучшая индивидуальная модель: {max(test_scores, key=test_scores.get)}")
    print(f"Лучший индивидуальный score: {max(test_scores.values()):.4f}")
    print(f"Ensemble score: {ensemble_score:.4f}")
    print(f"CV score: {cv_mean:.4f} ± {cv_std:.4f}")
    
    if trading_metrics:
        print(f"Sharpe Ratio: {trading_metrics['sharpe_ratio']:.4f}")
        print(f"Max Drawdown: {trading_metrics['max_drawdown']:.4f}")
        print(f"Win Rate: {trading_metrics['win_rate']:.4f}")
    
    # Детальный отчет
    print(f"\n=== Classification Report (Ensemble) ===")
    print(classification_report(y_test, ensemble_pred))
    
    # Результаты для возврата
    results = {
        'models': models,
        'ensemble': ensemble,
        'model_scores': model_scores,
        'test_scores': test_scores,
        'cv_scores': cv_scores,
        'cv_mean': cv_mean,
        'cv_std': cv_std,
        'test_predictions': test_predictions,
        'trading_metrics': trading_metrics,
        'best_model': best_model_name,
        'ensemble_score': ensemble_score
    }
    
    return results

def plot_complete_results(results, figsize=(15, 12)):
    """Визуализация результатов полного обучения"""
    
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Сравнение моделей
    models = list(results['test_scores'].keys())
    scores = list(results['test_scores'].values())
    
    bars = axes[0, 0].bar(models, scores, color='skyblue', alpha=0.8)
    axes[0, 0].set_title('Model Performance Comparison')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Добавление значений на столбцы
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{score:.3f}', ha='center', va='bottom')
    
    axes[0, 0].grid(True, alpha=0.3)
    
    # CV результаты
    cv_scores = results['cv_scores']
    axes[0, 1].plot(range(1, len(cv_scores)+1), cv_scores, 'o-', linewidth=2, markersize=8)
    axes[0, 1].axhline(y=results['cv_mean'], color='red', linestyle='--', 
                      label=f'Mean: {results["cv_mean"]:.3f}')
    axes[0, 1].set_title('Cross-Validation Scores')
    axes[0, 1].set_xlabel('Fold')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Торговые метрики (если доступны)
    if results['trading_metrics']:
        trading_metrics = results['trading_metrics']
        
        # Кумулятивная доходность
        cumulative_returns = trading_metrics['cumulative_returns']
        axes[1, 0].plot(cumulative_returns, linewidth=2)
        axes[1, 0].axhline(y=1, color='black', linestyle='--', alpha=0.5)
        axes[1, 0].set_title('Cumulative Returns')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Cumulative Return')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Основные торговые метрики
        metric_names = ['Sharpe', 'Calmar', 'Win Rate', 'Profit Factor']
        metric_values = [
            trading_metrics['sharpe_ratio'],
            trading_metrics['calmar_ratio'],
            trading_metrics['win_rate'],
            trading_metrics['profit_factor']
        ]
        
        # Ограничиваем значения для визуализации
        metric_values_limited = [min(val, 10) if val != np.inf else 10 for val in metric_values]
        
        bars = axes[1, 1].bar(metric_names, metric_values_limited, 
                             color=['skyblue', 'lightgreen', 'lightcoral', 'gold'], alpha=0.8)
        axes[1, 1].set_title('Trading Metrics')
        axes[1, 1].set_ylabel('Value')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # Добавление значений на столбцы
        for bar, value in zip(bars, metric_values):
            height = bar.get_height()
            if value == np.inf:
                label = '∞'
            else:
                label = f'{value:.3f}'
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           label, ha='center', va='bottom')
        
        axes[1, 1].grid(True, alpha=0.3)
    else:
        axes[1, 0].text(0.5, 0.5, 'Trading metrics\nnot available', 
                       ha='center', va='center', transform=axes[1, 0].transAxes)
        axes[1, 0].set_title('Trading Metrics')
        
        axes[1, 1].text(0.5, 0.5, 'Trading metrics\nnot available', 
                       ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Trading Metrics')
    
    plt.tight_layout()
    plt.show()

# Пример использования:
def example_complete_training_usage():
    """Пример полного обучения торговой модели"""
    
    # Создание синтетических данных
    np.random.seed(42)
    n_samples, n_features = 2000, 20
    
    # Генерация признаков
    X = np.random.randn(n_samples, n_features)
    
    # Создание целевой переменной
    y = np.zeros(n_samples)
    for i in range(n_samples):
        if X[i, 0] > 0.5 and X[i, 1] < -0.3:
            y[i] = 1
        elif X[i, 2] > 1.0 or X[i, 3] < -1.0:
            y[i] = 2
        else:
            y[i] = 0
    
    # Генерация доходности
    returns = np.random.normal(0.001, 0.02, n_samples)
    
    print("=== Пример полного обучения торговой модели ===")
    
    # Полное обучение
    results = train_complete_trading_model(X, y, returns)
    
    # Визуализация результатов
    plot_complete_results(results)
    
    return results

# Запуск примера (раскомментируйте для тестирования)
# results = example_complete_training_usage()
```

## Следующие шаги

**Теория:** После успешного обучения модели наступает этап валидации и тестирования. Следующие шаги критически важны для обеспечения надежности торговой стратегии.

**Почему важен каждый этап:**

1. **Бэктестинг** - Проверка модели на исторических данных
   - **Цель:** Убедиться, что модель работает на данных, которые она не видела
   - **Методы:** Walk-forward analysis, Monte Carlo simulation
   - **Критерии:** Стабильность результатов, отсутствие переобучения

2. **Валидация на out-of-sample данных** - Тестирование на новых данных
   - **Цель:** Проверить обобщающую способность модели
   - **Период:** Обычно 20-30% от общего объема данных
   - **Критерии:** Сравнение с бенчмарком, статистическая значимость

3. **Оптимизация параметров** - Тонкая настройка модели
   - **Цель:** Максимизировать производительность при минимизации риска
   - **Методы:** Grid search, Bayesian optimization, Genetic algorithms
   - **Критерии:** Устойчивость к изменениям параметров

4. **Мониторинг производительности** - Отслеживание в реальном времени
   - **Цель:** Своевременно выявлять деградацию модели
   - **Метрики:** Accuracy, Sharpe ratio, Drawdown, Win rate
   - **Действия:** Переобучение, остановка торговли, корректировка параметров

**Практические рекомендации:**

- **Начните с бэктестинга** - это основа для всех дальнейших решений
- **Используйте walk-forward анализ** - он наиболее реалистичен для финансовых данных
- **Тестируйте на разных рыночных условиях** - бычий/медвежий рынок, волатильность
- **Проверяйте стабильность результатов** - избегайте переобучения
- **Документируйте все эксперименты** - это поможет в будущих итерациях

**Структура следующих этапов:**

```
Обучение модели → Бэктестинг → Валидация → Оптимизация → Мониторинг
     ↓              ↓           ↓           ↓           ↓
  Точность      Историческая   Out-of-    Параметры   Реальное
  на train      производительность sample   модели     время
```

После обучения модели переходите к:
- **[06_backtesting.md](06_backtesting.md)** - Бэктестинг торговых стратегий
- **[07_validation.md](07_validation.md)** - Валидация моделей
- **[08_optimization.md](08_optimization.md)** - Оптимизация параметров
- **[09_monitoring.md](09_monitoring.md)** - Мониторинг производительности
- **[07_walk_forward_analysis.md](07_walk_forward_analysis.md)** - Walk-forward анализ

## Ключевые выводы

**Теория:** Обучение ML-моделей для финансовых данных имеет свои особенности и требует специального подхода. Понимание этих принципов критически важно для создания успешных торговых стратегий.

**Основные принципы успешного обучения:**

### 1. **Ансамблевые методы превосходят одиночные модели**
- **Почему:** Финансовые данные сложны и нестабильны
- **Преимущества:** Снижение переобучения, повышение стабильности
- **Рекомендации:** Используйте Voting, Stacking, Bagging
- **Практика:** Комбинируйте 3-5 различных алгоритмов

### 2. **Временные ряды требуют специальной валидации**
- **Проблема:** Стандартная CV нарушает временную структуру
- **Решение:** Time Series CV, Walk-Forward Validation
- **Критерии:** Временная последовательность, отсутствие data leakage
- **Практика:** Всегда используйте временные методы валидации

### 3. **Оптимизация гиперпараметров критически важна**
- **Цель:** Найти оптимальный баланс bias-variance
- **Методы:** Grid Search, Random Search, Bayesian optimization
- **Критерии:** Стабильность, производительность, скорость
- **Практика:** Начните с простых методов, переходите к сложным

### 4. **Торговые метрики важнее классификационных**
- **Причина:** Accuracy не отражает реальную прибыльность
- **Ключевые метрики:** Sharpe Ratio, Max Drawdown, Win Rate
- **Анализ:** Рассматривайте метрики в комплексе
- **Практика:** Оптимизируйте по торговым метрикам, а не по accuracy

### 5. **Качество данных определяет успех**
- **Влияние:** Плохие данные = плохая модель
- **Требования:** Очистка, нормализация, feature engineering
- **Проверка:** Анализ распределений, корреляций, выбросов
- **Практика:** Инвестируйте время в подготовку данных

### 6. **Регуляризация предотвращает переобучение**
- **Проблема:** Финансовые данные склонны к переобучению
- **Методы:** L1/L2 regularization, dropout, early stopping
- **Баланс:** Сложность модели vs. обобщающая способность
- **Практика:** Начинайте с простых моделей, усложняйте постепенно

### 7. **Мониторинг и адаптация необходимы**
- **Реальность:** Рынки постоянно меняются
- **Действия:** Регулярное переобучение, мониторинг метрик
- **Критерии:** Деградация производительности, изменение рынка
- **Практика:** Автоматизируйте процесс мониторинга

**Практические рекомендации:**

1. **Начните с простого** - Random Forest, затем переходите к сложному
2. **Используйте правильную валидацию** - Time Series CV для временных рядов
3. **Оптимизируйте по торговым метрикам** - не по accuracy
4. **Тестируйте на разных периодах** - бычий/медвежий рынок
5. **Документируйте все эксперименты** - это поможет в будущем
6. **Планируйте мониторинг** - модель нужно поддерживать

**Типичные ошибки:**

- ❌ Использование стандартной CV для временных рядов
- ❌ Оптимизация только по accuracy
- ❌ Игнорирование торговых метрик
- ❌ Отсутствие мониторинга производительности
- ❌ Переобучение на исторических данных

**Успешная стратегия:**

- ✅ Правильная валидация (Time Series CV)
- ✅ Ансамблевые методы
- ✅ Оптимизация по торговым метрикам
- ✅ Регулярный мониторинг
- ✅ Адаптация к изменениям рынка

**Заключение:**

Обучение ML-моделей для финансов - это итеративный процесс, требующий глубокого понимания как машинного обучения, так и финансовых рынков. Успех приходит к тем, кто правильно валидирует модели, использует подходящие метрики и постоянно адаптируется к изменениям рынка.

---

**Важно:** Не гонитесь за высокой точностью - важнее стабильная прибыльность!
