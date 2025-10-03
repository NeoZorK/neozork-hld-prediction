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

**Почему Random Forest эффективен для финансов:**
- **Устойчивость к переобучению:** Множество деревьев снижают риск переобучения
- **Обработка выбросов:** Деревья по-разному реагируют на выбросы
- **Интерпретируемость:** Можно анализировать важность признаков
- **Быстрота:** Параллельное обучение деревьев

**Плюсы Random Forest:**
- Высокая точность
- Устойчивость к переобучению
- Интерпретируемость
- Быстрота обучения

**Минусы Random Forest:**
- Могут быть менее точными на очень сложных данных
- Требуют настройки параметров
- Могут быть избыточными для простых задач
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_random_forest(X, y):
    """Обучение Random Forest"""
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Создание модели
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    # Обучение
    rf.fit(X_train, y_train)
    
    # Оценка
    train_score = rf.score(X_train, y_train)
    test_score = rf.score(X_test, y_test)
    
    print(f"Train accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    return rf
```

### 2. XGBoost
```python
import xgboost as xgb
from sklearn.metrics import classification_report

def train_xgboost(X, y):
    """Обучение XGBoost"""
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Параметры XGBoost
    params = {
        'objective': 'multi:softprob',
        'num_class': 3,
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42
    }
    
    # Создание модели
    xgb_model = xgb.XGBClassifier(**params)
    
    # Обучение
    xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=10,
        verbose=False
    )
    
    # Предсказания
    y_pred = xgb_model.predict(X_test)
    
    # Отчет
    print(classification_report(y_test, y_pred))
    
    return xgb_model
```

### 3. LightGBM
```python
import lightgbm as lgb

def train_lightgbm(X, y):
    """Обучение LightGBM"""
    
    # Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Параметры LightGBM
    params = {
        'objective': 'multiclass',
        'num_class': 3,
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1
    }
    
    # Создание датасетов
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    # Обучение
    model = lgb.train(
        params,
        train_data,
        valid_sets=[test_data],
        num_boost_round=100,
        callbacks=[lgb.early_stopping(10)]
    )
    
    return model
```

## Нейронные сети

### 1. Простая нейронная сеть
```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

class TradingNN(nn.Module):
    def __init__(self, input_size, hidden_size=128, num_classes=3):
        super(TradingNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, hidden_size)
        self.fc4 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.dropout(x)
        x = self.fc4(x)
        return x

def train_neural_network(X, y, epochs=100):
    """Обучение нейронной сети"""
    
    # Преобразование в тензоры
    X_tensor = torch.FloatTensor(X)
    y_tensor = torch.LongTensor(y)
    
    # Создание датасета
    dataset = TensorDataset(X_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Создание модели
    model = TradingNN(X.shape[1])
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Обучение
    for epoch in range(epochs):
        for batch_X, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
        
        if epoch % 10 == 0:
            print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
    
    return model
```

### 2. LSTM для временных рядов
```python
class LSTMTradingModel(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=3):
        super(LSTMTradingModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        # Инициализация скрытого состояния
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        # LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Берем последний выход
        out = self.dropout(out[:, -1, :])
        out = self.fc(out)
        
        return out

def train_lstm_model(X, y, sequence_length=10):
    """Обучение LSTM модели"""
    
    # Создание последовательностей
    X_seq, y_seq = create_sequences(X, y, sequence_length)
    
    # Преобразование в тензоры
    X_tensor = torch.FloatTensor(X_seq)
    y_tensor = torch.LongTensor(y_seq)
    
    # Создание модели
    model = LSTMTradingModel(X.shape[1])
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Обучение
    for epoch in range(100):
        optimizer.zero_grad()
        outputs = model(X_tensor)
        loss = criterion(outputs, y_tensor)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            print(f'Epoch {epoch}, Loss: {loss.item():.4f}')
    
    return model

def create_sequences(X, y, sequence_length):
    """Создание последовательностей для LSTM"""
    X_seq, y_seq = [], []
    
    for i in range(sequence_length, len(X)):
        X_seq.append(X[i-sequence_length:i])
        y_seq.append(y[i])
    
    return np.array(X_seq), np.array(y_seq)
```

## Валидация моделей

### 1. Time Series Cross Validation
```python
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def time_series_cv(model, X, y, n_splits=5):
    """Кросс-валидация для временных рядов"""
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    scores = []
    
    for train_idx, test_idx in tscv.split(X):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        # Обучение
        model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = model.predict(X_test)
        
        # Метрики
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        scores.append({
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        })
    
    return scores
```

### 2. Walk-Forward Validation
```python
def walk_forward_validation(model, X, y, train_size=1000, step_size=100):
    """Walk-Forward валидация"""
    
    results = []
    
    for i in range(train_size, len(X), step_size):
        # Обучающая выборка
        X_train = X[i-train_size:i]
        y_train = y[i-train_size:i]
        
        # Тестовая выборка
        X_test = X[i:i+step_size]
        y_test = y[i:i+step_size]
        
        # Обучение
        model.fit(X_train, y_train)
        
        # Предсказания
        y_pred = model.predict(X_test)
        
        # Метрики
        accuracy = accuracy_score(y_test, y_pred)
        results.append(accuracy)
    
    return results
```

## Гиперпараметрическая оптимизация

### 1. Grid Search
```python
from sklearn.model_selection import GridSearchCV

def optimize_random_forest(X, y):
    """Оптимизация Random Forest"""
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, 15],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestClassifier(random_state=42)
    
    grid_search = GridSearchCV(
        rf, param_grid, cv=5, 
        scoring='accuracy', n_jobs=-1
    )
    
    grid_search.fit(X, y)
    
    return grid_search.best_estimator_, grid_search.best_params_
```

### 2. Optuna оптимизация
```python
import optuna

def optimize_xgboost_optuna(X, y):
    """Оптимизация XGBoost с Optuna"""
    
    def objective(trial):
        params = {
            'objective': 'multi:softprob',
            'num_class': 3,
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0)
        }
        
        model = xgb.XGBClassifier(**params)
        scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        return scores.mean()
    
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=100)
    
    return study.best_params_
```

## Ансамблевые методы

### 1. Voting Classifier
```python
from sklearn.ensemble import VotingClassifier

def create_ensemble_model(X, y):
    """Создание ансамблевой модели"""
    
    # Индивидуальные модели
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    xgb_model = xgb.XGBClassifier(n_estimators=100, random_state=42)
    lgb_model = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    
    # Ансамбль
    ensemble = VotingClassifier(
        estimators=[
            ('rf', rf),
            ('xgb', xgb_model),
            ('lgb', lgb_model)
        ],
        voting='soft'
    )
    
    # Обучение
    ensemble.fit(X, y)
    
    return ensemble
```

### 2. Stacking
```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

def create_stacking_model(X, y):
    """Создание Stacking модели"""
    
    # Базовые модели
    base_models = [
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('xgb', xgb.XGBClassifier(n_estimators=100, random_state=42)),
        ('lgb', lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1))
    ]
    
    # Мета-модель
    meta_model = LogisticRegression()
    
    # Stacking
    stacking_model = StackingClassifier(
        estimators=base_models,
        final_estimator=meta_model,
        cv=5
    )
    
    # Обучение
    stacking_model.fit(X, y)
    
    return stacking_model
```

## Оценка производительности

### 1. Метрики классификации
```python
from sklearn.metrics import confusion_matrix, classification_report

def evaluate_model(model, X_test, y_test):
    """Оценка модели"""
    
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    # Метрики
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Матрица ошибок
    cm = confusion_matrix(y_test, y_pred)
    
    # Отчет
    report = classification_report(y_test, y_pred)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'classification_report': report
    }
```

### 2. Торговые метрики
```python
def calculate_trading_metrics(y_true, y_pred, returns):
    """Расчет торговых метрик"""
    
    # Точность предсказаний
    accuracy = accuracy_score(y_true, y_pred)
    
    # Прибыльность
    correct_predictions = (y_true == y_pred)
    total_return = (returns * correct_predictions).sum()
    
    # Sharpe Ratio
    if returns.std() > 0:
        sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252)
    else:
        sharpe_ratio = 0
    
    # Максимальная просадка
    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        'accuracy': accuracy,
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }
```

## Практический пример

```python
def train_complete_trading_model(X, y):
    """Полное обучение торговой модели"""
    
    # 1. Разделение данных
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 2. Обучение ансамбля
    ensemble = create_ensemble_model(X_train, y_train)
    
    # 3. Валидация
    cv_scores = time_series_cv(ensemble, X_train, y_train)
    
    # 4. Оценка на тесте
    test_metrics = evaluate_model(ensemble, X_test, y_test)
    
    # 5. Торговые метрики
    # (предполагаем, что у нас есть returns)
    # trading_metrics = calculate_trading_metrics(y_test, y_pred, returns)
    
    print("=== Результаты обучения ===")
    print(f"CV Accuracy: {np.mean([s['accuracy'] for s in cv_scores]):.4f}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test F1: {test_metrics['f1']:.4f}")
    
    return ensemble, test_metrics
```

## Следующие шаги

После обучения модели переходите к:
- **[06_backtesting.md](06_backtesting.md)** - Бэктестинг
- **[07_walk_forward_analysis.md](07_walk_forward_analysis.md)** - Walk-forward анализ

## Ключевые выводы

1. **Ансамблевые методы** работают лучше для финансов
2. **Валидация** критически важна
3. **Гиперпараметры** сильно влияют на результат
4. **Торговые метрики** важнее точности
5. **Ансамбли** обычно превосходят отдельные модели

---

**Важно:** Не гонитесь за высокой точностью - важнее стабильная прибыльность!
