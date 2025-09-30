# Метрики и оценка качества в AutoML Gluon

## Введение в метрики

Метрики в AutoML Gluon используются для:
- Оценки качества моделей
- Сравнения различных алгоритмов
- Выбора лучшей модели
- Мониторинга производительности

## Метрики для классификации

### Базовые метрики

#### Accuracy (Точность)
```python
# Процент правильных предсказаний
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy:.4f}")
```

#### Precision (Точность)
```python
# Доля правильно предсказанных положительных случаев
from sklearn.metrics import precision_score

precision = precision_score(y_true, y_pred, average='binary')
print(f"Precision: {precision:.4f}")

# Для многоклассовой классификации
precision_macro = precision_score(y_true, y_pred, average='macro')
precision_micro = precision_score(y_true, y_pred, average='micro')
```

#### Recall (Полнота)
```python
# Доля положительных случаев, которые были правильно предсказаны
from sklearn.metrics import recall_score

recall = recall_score(y_true, y_pred, average='binary')
print(f"Recall: {recall:.4f}")

# Для многоклассовой классификации
recall_macro = recall_score(y_true, y_pred, average='macro')
recall_micro = recall_score(y_true, y_pred, average='micro')
```

#### F1-Score
```python
# Гармоническое среднее precision и recall
from sklearn.metrics import f1_score

f1 = f1_score(y_true, y_pred, average='binary')
print(f"F1-Score: {f1:.4f}")

# Для многоклассовой классификации
f1_macro = f1_score(y_true, y_pred, average='macro')
f1_micro = f1_score(y_true, y_pred, average='micro')
```

### Продвинутые метрики

#### ROC AUC
```python
# Площадь под ROC кривой
from sklearn.metrics import roc_auc_score

# Для бинарной классификации
roc_auc = roc_auc_score(y_true, y_prob)
print(f"ROC AUC: {roc_auc:.4f}")

# Для многоклассовой классификации
roc_auc_ovo = roc_auc_score(y_true, y_prob, multi_class='ovo')
roc_auc_ovr = roc_auc_score(y_true, y_prob, multi_class='ovr')
```

#### PR AUC
```python
# Площадь под Precision-Recall кривой
from sklearn.metrics import average_precision_score

pr_auc = average_precision_score(y_true, y_prob)
print(f"PR AUC: {pr_auc:.4f}")
```

#### Log Loss
```python
# Логарифмическая функция потерь
from sklearn.metrics import log_loss

log_loss_score = log_loss(y_true, y_prob)
print(f"Log Loss: {log_loss_score:.4f}")
```

#### Balanced Accuracy
```python
# Сбалансированная точность для несбалансированных данных
from sklearn.metrics import balanced_accuracy_score

balanced_acc = balanced_accuracy_score(y_true, y_pred)
print(f"Balanced Accuracy: {balanced_acc:.4f}")
```

### Метрики для несбалансированных данных

#### Matthews Correlation Coefficient (MCC)
```python
from sklearn.metrics import matthews_corrcoef

mcc = matthews_corrcoef(y_true, y_pred)
print(f"MCC: {mcc:.4f}")
```

#### Cohen's Kappa
```python
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(y_true, y_pred)
print(f"Cohen's Kappa: {kappa:.4f}")
```

## Метрики для регрессии

### Базовые метрики

#### Mean Absolute Error (MAE)
```python
from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_true, y_pred)
print(f"MAE: {mae:.4f}")
```

#### Mean Squared Error (MSE)
```python
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_true, y_pred)
print(f"MSE: {mse:.4f}")
```

#### Root Mean Squared Error (RMSE)
```python
import numpy as np

rmse = np.sqrt(mean_squared_error(y_true, y_pred))
print(f"RMSE: {rmse:.4f}")
```

#### R² Score
```python
from sklearn.metrics import r2_score

r2 = r2_score(y_true, y_pred)
print(f"R² Score: {r2:.4f}")
```

### Продвинутые метрики

#### Mean Absolute Percentage Error (MAPE)
```python
def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

mape_score = mape(y_true, y_pred)
print(f"MAPE: {mape_score:.4f}%")
```

#### Symmetric Mean Absolute Percentage Error (SMAPE)
```python
def smape(y_true, y_pred):
    return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100

smape_score = smape(y_true, y_pred)
print(f"SMAPE: {smape_score:.4f}%")
```

#### Mean Absolute Scaled Error (MASE)
```python
def mase(y_true, y_pred, y_train):
    # Наивный прогноз (следующее значение)
    naive_forecast = np.roll(y_train, 1)
    naive_mae = np.mean(np.abs(y_train - naive_forecast))
    
    # MAE модели
    model_mae = np.mean(np.abs(y_true - y_pred))
    
    return model_mae / naive_mae

mase_score = mase(y_true, y_pred, y_train)
print(f"MASE: {mase_score:.4f}")
```

## Использование метрик в AutoGluon

### Настройка метрик для обучения

```python
from autogluon.tabular import TabularPredictor

# Для классификации
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy'  # или 'f1', 'roc_auc', 'log_loss'
)

# Для регрессии
predictor = TabularPredictor(
    label='target',
    problem_type='regression',
    eval_metric='rmse'  # или 'mae', 'r2'
)
```

### Множественные метрики

```python
# Обучение с несколькими метриками
predictor.fit(
    train_data,
    eval_metric=['accuracy', 'f1', 'roc_auc']
)

# Получение всех метрик
performance = predictor.evaluate(test_data)
print(performance)
```

### Кастомные метрики

```python
from autogluon.core import Scorer

# Создание кастомной метрики
def custom_metric(y_true, y_pred):
    """Кастомная метрика для оценки качества"""
    # Ваша логика расчета
    return score

custom_scorer = Scorer(
    name='custom_metric',
    score_func=custom_metric,
    greater_is_better=True
)

predictor.fit(
    train_data,
    eval_metric=custom_scorer
)
```

## Анализ производительности

### Лидерборд моделей

```python
# Получение лидерборда
leaderboard = predictor.leaderboard(test_data)
print(leaderboard)

# Детальный лидерборд
leaderboard_detailed = predictor.leaderboard(
    test_data,
    extra_info=True,
    silent=False
)
```

### Анализ важности признаков

```python
# Важность признаков
feature_importance = predictor.feature_importance()
print(feature_importance)

# Визуализация важности признаков
import matplotlib.pyplot as plt

feature_importance.plot(kind='barh', figsize=(10, 8))
plt.title('Feature Importance')
plt.xlabel('Importance')
plt.show()
```

### Анализ ошибок

```python
# Анализ ошибок для классификации
from sklearn.metrics import classification_report, confusion_matrix

# Отчет по классификации
print(classification_report(y_true, y_pred))

# Матрица ошибок
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)

# Визуализация матрицы ошибок
import seaborn as sns
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.show()
```

## Метрики для временных рядов

### Метрики для прогнозирования

```python
# Mean Absolute Scaled Error (MASE)
def mase_time_series(y_true, y_pred, y_train, seasonal_period=1):
    """MASE для временных рядов"""
    # Наивный прогноз
    naive_forecast = np.roll(y_train, seasonal_period)
    naive_mae = np.mean(np.abs(y_train - naive_forecast))
    
    # MAE модели
    model_mae = np.mean(np.abs(y_true - y_pred))
    
    return model_mae / naive_mae

# Symmetric Mean Absolute Percentage Error (SMAPE)
def smape_time_series(y_true, y_pred):
    """SMAPE для временных рядов"""
    return np.mean(2 * np.abs(y_true - y_pred) / (np.abs(y_true) + np.abs(y_pred))) * 100
```

### Метрики для финансовых данных

```python
# Sharpe Ratio
def sharpe_ratio(returns, risk_free_rate=0.02):
    """Коэффициент Шарпа"""
    excess_returns = returns - risk_free_rate
    return np.mean(excess_returns) / np.std(excess_returns)

# Maximum Drawdown
def max_drawdown(cumulative_returns):
    """Максимальная просадка"""
    peak = np.maximum.accumulate(cumulative_returns)
    drawdown = (cumulative_returns - peak) / peak
    return np.min(drawdown)

# Calmar Ratio
def calmar_ratio(returns, max_dd):
    """Коэффициент Калмара"""
    annual_return = np.mean(returns) * 252
    return annual_return / abs(max_dd)
```

## Мониторинг метрик

### Отслеживание метрик в реальном времени

```python
import logging
from datetime import datetime

class MetricsLogger:
    def __init__(self, log_file='metrics.log'):
        self.log_file = log_file
        self.metrics_history = []
    
    def log_metrics(self, metrics_dict):
        """Логирование метрик"""
        timestamp = datetime.now()
        metrics_dict['timestamp'] = timestamp
        self.metrics_history.append(metrics_dict)
        
        # Запись в файл
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp}: {metrics_dict}\n")
    
    def get_metrics_trend(self, metric_name):
        """Получение тренда метрики"""
        return [m[metric_name] for m in self.metrics_history if metric_name in m]

# Использование
metrics_logger = MetricsLogger()

# Логирование метрик
metrics = {
    'accuracy': 0.85,
    'f1_score': 0.82,
    'roc_auc': 0.88
}
metrics_logger.log_metrics(metrics)
```

### Алерты по метрикам

```python
class MetricsAlert:
    def __init__(self, threshold=0.8, metric_name='accuracy'):
        self.threshold = threshold
        self.metric_name = metric_name
    
    def check_alert(self, current_metric):
        """Проверка алерта"""
        if current_metric < self.threshold:
            print(f"ALERT: {self.metric_name} = {current_metric} < {self.threshold}")
            return True
        return False

# Использование
alert = MetricsAlert(threshold=0.8, metric_name='accuracy')
if alert.check_alert(0.75):
    # Отправка уведомления
    pass
```

## Примеры использования метрик

### Полный пример оценки модели

```python
from autogluon.tabular import TabularPredictor
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Создание данных
X, y = make_classification(
    n_samples=10000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    n_classes=2,
    random_state=42
)

data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(20)])
data['target'] = y

# Разделение данных
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Создание и обучение модели
predictor = TabularPredictor(
    label='target',
    problem_type='binary',
    eval_metric='accuracy'
)

predictor.fit(train_data, time_limit=300)

# Предсказания
predictions = predictor.predict(test_data)
probabilities = predictor.predict_proba(test_data)

# Оценка качества
performance = predictor.evaluate(test_data)
print("Performance Metrics:")
for metric, value in performance.items():
    print(f"{metric}: {value:.4f}")

# Лидерборд
leaderboard = predictor.leaderboard(test_data)
print("\nLeaderboard:")
print(leaderboard)

# Важность признаков
feature_importance = predictor.feature_importance()
print("\nFeature Importance:")
print(feature_importance.head(10))

# Визуализация
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# ROC кривая
from sklearn.metrics import roc_curve, auc
fpr, tpr, _ = roc_curve(test_data['target'], probabilities[1])
roc_auc = auc(fpr, tpr)
axes[0, 0].plot(fpr, tpr, label=f'ROC AUC = {roc_auc:.3f}')
axes[0, 0].plot([0, 1], [0, 1], 'k--')
axes[0, 0].set_xlabel('False Positive Rate')
axes[0, 0].set_ylabel('True Positive Rate')
axes[0, 0].set_title('ROC Curve')
axes[0, 0].legend()

# Precision-Recall кривая
from sklearn.metrics import precision_recall_curve
precision, recall, _ = precision_recall_curve(test_data['target'], probabilities[1])
axes[0, 1].plot(recall, precision)
axes[0, 1].set_xlabel('Recall')
axes[0, 1].set_ylabel('Precision')
axes[0, 1].set_title('Precision-Recall Curve')

# Матрица ошибок
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(test_data['target'], predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0])
axes[1, 0].set_title('Confusion Matrix')

# Важность признаков
feature_importance.head(10).plot(kind='barh', ax=axes[1, 1])
axes[1, 1].set_title('Top 10 Feature Importance')

plt.tight_layout()
plt.show()
```

## Следующие шаги

После освоения работы с метриками переходите к:
- [Методам валидации](./05_validation.md)
- [Продакшен деплою](./06_production.md)
- [Переобучению моделей](./07_retraining.md)
