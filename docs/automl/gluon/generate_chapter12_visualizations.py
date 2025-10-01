#!/usr/bin/env python3
"""
Генерация визуализаций для главы 12_examples.md
Создает наглядные картинки для объяснения метрик и задач
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, confusion_matrix,
    classification_report, mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_metrics_comparison_visualization():
    """Создает визуализацию сравнения метрик для классификации и регрессии"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Сравнение метрик для классификации и регрессии', fontsize=16, fontweight='bold')
    
    # Генерация данных для классификации
    X_clf, y_clf = make_classification(n_samples=1000, n_features=2, n_redundant=0, 
                                     n_informative=2, n_clusters_per_class=1, random_state=42)
    X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X_clf, y_clf, test_size=0.3, random_state=42)
    
    # Обучение модели классификации
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_clf, y_train_clf)
    y_pred_clf = clf.predict(X_test_clf)
    y_prob_clf = clf.predict_proba(X_test_clf)[:, 1]
    
    # ROC кривая
    fpr, tpr, _ = roc_curve(y_test_clf, y_prob_clf)
    roc_auc = auc(fpr, tpr)
    axes[0, 0].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC AUC = {roc_auc:.3f}')
    axes[0, 0].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    axes[0, 0].set_xlim([0.0, 1.0])
    axes[0, 0].set_ylim([0.0, 1.05])
    axes[0, 0].set_xlabel('False Positive Rate')
    axes[0, 0].set_ylabel('True Positive Rate')
    axes[0, 0].set_title('ROC Curve (Классификация)')
    axes[0, 0].legend(loc="lower right")
    axes[0, 0].grid(True, alpha=0.3)
    
    # Precision-Recall кривая
    precision, recall, _ = precision_recall_curve(y_test_clf, y_prob_clf)
    axes[0, 1].plot(recall, precision, color='darkorange', lw=2)
    axes[0, 1].set_xlabel('Recall')
    axes[0, 1].set_ylabel('Precision')
    axes[0, 1].set_title('Precision-Recall Curve')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test_clf, y_pred_clf)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 2])
    axes[0, 2].set_title('Confusion Matrix')
    axes[0, 2].set_xlabel('Predicted')
    axes[0, 2].set_ylabel('Actual')
    
    # Генерация данных для регрессии
    X_reg, y_reg = make_regression(n_samples=1000, n_features=1, noise=20, random_state=42)
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_reg, y_reg, test_size=0.3, random_state=42)
    
    # Обучение модели регрессии
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train_reg, y_train_reg)
    y_pred_reg = reg.predict(X_test_reg)
    
    # Предсказания vs Фактические значения
    axes[1, 0].scatter(y_test_reg, y_pred_reg, alpha=0.6, color='darkorange')
    axes[1, 0].plot([y_test_reg.min(), y_test_reg.max()], [y_test_reg.min(), y_test_reg.max()], 'r--', lw=2)
    axes[1, 0].set_xlabel('Actual Values')
    axes[1, 0].set_ylabel('Predicted Values')
    axes[1, 0].set_title('Predictions vs Actual (Регрессия)')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Распределение ошибок
    errors = y_test_reg - y_pred_reg
    axes[1, 1].hist(errors, bins=30, alpha=0.7, color='darkorange')
    axes[1, 1].set_xlabel('Prediction Error')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of Prediction Errors')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Метрики качества
    mae = mean_absolute_error(y_test_reg, y_pred_reg)
    mse = mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)
    
    metrics_text = f'MAE: {mae:.3f}\nMSE: {mse:.3f}\nR²: {r2:.3f}'
    axes[1, 2].text(0.1, 0.5, metrics_text, transform=axes[1, 2].transAxes, 
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    axes[1, 2].set_title('Regression Metrics')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/metrics_comparison_detailed.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_bank_classification_visualization():
    """Создает визуализацию для банковской задачи классификации"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Банковская задача: Предсказание дефолта клиентов', fontsize=16, fontweight='bold')
    
    # Генерация банковских данных
    np.random.seed(42)
    n_samples = 1000
    
    # Создание реалистичных банковских данных
    data = {
        'age': np.random.normal(35, 10, n_samples),
        'income': np.random.normal(50000, 20000, n_samples),
        'credit_score': np.random.normal(650, 100, n_samples),
        'debt_ratio': np.random.beta(2, 5, n_samples),
        'employment_years': np.random.exponential(5, n_samples),
        'loan_amount': np.random.lognormal(10, 1, n_samples)
    }
    
    # Создание целевой переменной на основе логики
    default_prob = (
        0.1 * (data['debt_ratio'] > 0.4) +
        0.2 * (data['credit_score'] < 600) +
        0.15 * (data['age'] < 25) +
        0.1 * (data['employment_years'] < 2) +
        0.05 * (data['income'] < 30000) +
        np.random.normal(0, 0.05, n_samples)
    )
    data['default_risk'] = (default_prob > 0.3).astype(int)
    
    df = pd.DataFrame(data)
    
    # Разделение данных
    X = df.drop('default_risk', axis=1)
    y = df['default_risk']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Обучение модели
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    
    # ROC кривая
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    axes[0, 0].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC AUC = {roc_auc:.3f}')
    axes[0, 0].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    axes[0, 0].set_xlabel('False Positive Rate')
    axes[0, 0].set_ylabel('True Positive Rate')
    axes[0, 0].set_title('ROC Curve - Качество разделения классов')
    axes[0, 0].legend(loc="lower right")
    axes[0, 0].grid(True, alpha=0.3)
    
    # Precision-Recall кривая
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    axes[0, 1].plot(recall, precision, color='darkorange', lw=2)
    axes[0, 1].set_xlabel('Recall (Полнота)')
    axes[0, 1].set_ylabel('Precision (Точность)')
    axes[0, 1].set_title('Precision-Recall Curve - Баланс точности и полноты')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0],
                xticklabels=['Нет дефолта', 'Дефолт'],
                yticklabels=['Нет дефолта', 'Дефолт'])
    axes[1, 0].set_title('Confusion Matrix - Анализ ошибок')
    axes[1, 0].set_xlabel('Предсказанный класс')
    axes[1, 0].set_ylabel('Истинный класс')
    
    # Важность признаков
    feature_importance = pd.Series(clf.feature_importances_, index=X.columns)
    feature_importance.sort_values(ascending=True).plot(kind='barh', ax=axes[1, 1], color='darkorange')
    axes[1, 1].set_title('Важность признаков - Какие факторы важны')
    axes[1, 1].set_xlabel('Важность')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/bank_classification_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_real_estate_regression_visualization():
    """Создает визуализацию для задачи регрессии недвижимости"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Задача регрессии: Прогнозирование цен на недвижимость', fontsize=16, fontweight='bold')
    
    # Генерация данных о недвижимости
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'area': np.random.normal(120, 30, n_samples),
        'bedrooms': np.random.poisson(3, n_samples),
        'bathrooms': np.random.poisson(2, n_samples),
        'age': np.random.exponential(10, n_samples),
        'garage': np.random.binomial(1, 0.7, n_samples),
        'pool': np.random.binomial(1, 0.2, n_samples),
        'location_score': np.random.uniform(1, 10, n_samples)
    }
    
    # Создание целевой переменной (цена)
    base_price = 100000
    price = (base_price + 
             data['area'] * 1000 +
             data['bedrooms'] * 10000 +
             data['bathrooms'] * 5000 +
             data['garage'] * 15000 +
             data['pool'] * 25000 -
             data['age'] * 2000 +
             data['location_score'] * 5000 +
             np.random.normal(0, 20000, n_samples))
    
    data['price'] = np.maximum(price, 50000)
    
    df = pd.DataFrame(data)
    
    # Разделение данных
    X = df.drop('price', axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Обучение модели
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    
    # Предсказания vs Фактические значения
    axes[0, 0].scatter(y_test, y_pred, alpha=0.6, color='darkorange')
    axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0, 0].set_xlabel('Фактическая цена')
    axes[0, 0].set_ylabel('Предсказанная цена')
    axes[0, 0].set_title('Предсказания vs Фактические значения')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Распределение ошибок
    errors = y_test - y_pred
    axes[0, 1].hist(errors, bins=30, alpha=0.7, color='darkorange')
    axes[0, 1].set_xlabel('Ошибка предсказания')
    axes[0, 1].set_ylabel('Частота')
    axes[0, 1].set_title('Распределение ошибок предсказания')
    axes[0, 1].axvline(x=0, color='red', linestyle='--')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Важность признаков
    feature_importance = pd.Series(reg.feature_importances_, index=X.columns)
    feature_importance.sort_values(ascending=True).plot(kind='barh', ax=axes[1, 0], color='darkorange')
    axes[1, 0].set_title('Важность признаков')
    axes[1, 0].set_xlabel('Важность')
    
    # Метрики качества
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    metrics_text = f'MAE: {mae:.0f} руб.\nRMSE: {rmse:.0f} руб.\nR²: {r2:.3f}\nMAPE: {mape:.1f}%'
    axes[1, 1].text(0.1, 0.5, metrics_text, transform=axes[1, 1].transAxes, 
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    axes[1, 1].set_title('Метрики качества регрессии')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/real_estate_regression_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_time_series_visualization():
    """Создает визуализацию для задачи временных рядов"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Задача временных рядов: Прогнозирование продаж', fontsize=16, fontweight='bold')
    
    # Генерация временного ряда
    np.random.seed(42)
    n_days = 365
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    # Создание временного ряда с трендом и сезонностью
    trend = np.linspace(100, 150, n_days)
    seasonality = 20 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Еженедельная сезонность
    noise = np.random.normal(0, 10, n_days)
    sales = trend + seasonality + noise
    sales = np.maximum(sales, 0)  # Негативные продажи невозможны
    
    # Разделение на train/test
    split_idx = int(0.8 * n_days)
    train_sales = sales[:split_idx]
    test_sales = sales[split_idx:]
    train_dates = dates[:split_idx]
    test_dates = dates[split_idx:]
    
    # Простое предсказание (скользящее среднее)
    window = 7
    predictions = []
    for i in range(len(test_sales)):
        if i < window:
            pred = np.mean(train_sales[-window:])
        else:
            pred = np.mean(test_sales[i-window:i])
        predictions.append(pred)
    
    predictions = np.array(predictions)
    
    # Временной ряд
    axes[0, 0].plot(train_dates, train_sales, label='Обучающие данные', color='blue', alpha=0.7)
    axes[0, 0].plot(test_dates, test_sales, label='Фактические значения', color='green', linewidth=2)
    axes[0, 0].plot(test_dates, predictions, label='Предсказания', color='red', linewidth=2)
    axes[0, 0].set_title('Временной ряд продаж с прогнозом')
    axes[0, 0].set_xlabel('Дата')
    axes[0, 0].set_ylabel('Продажи')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Ошибки прогноза
    errors = test_sales - predictions
    axes[0, 1].plot(test_dates, errors, color='red', alpha=0.7)
    axes[0, 1].axhline(y=0, color='black', linestyle='--')
    axes[0, 1].set_title('Ошибки прогноза по времени')
    axes[0, 1].set_xlabel('Дата')
    axes[0, 1].set_ylabel('Ошибка')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Распределение ошибок
    axes[1, 0].hist(errors, bins=20, alpha=0.7, color='darkorange')
    axes[1, 0].set_title('Распределение ошибок прогноза')
    axes[1, 0].set_xlabel('Ошибка')
    axes[1, 0].set_ylabel('Частота')
    axes[1, 0].axvline(x=0, color='red', linestyle='--')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Метрики качества
    mae = np.mean(np.abs(errors))
    mse = np.mean(errors**2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs(errors / test_sales)) * 100
    
    # MASE (Mean Absolute Scaled Error)
    naive_errors = np.abs(train_sales[1:] - train_sales[:-1])
    naive_mae = np.mean(naive_errors)
    mase = mae / naive_mae
    
    metrics_text = f'MAE: {mae:.2f}\nRMSE: {rmse:.2f}\nMAPE: {mape:.1f}%\nMASE: {mase:.3f}'
    axes[1, 1].text(0.1, 0.5, metrics_text, transform=axes[1, 1].transAxes, 
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    axes[1, 1].set_title('Метрики качества временных рядов')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/time_series_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_multiclass_classification_visualization():
    """Создает визуализацию для многоклассовой классификации"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Многоклассовая классификация: Классификация изображений', fontsize=16, fontweight='bold')
    
    # Генерация данных для многоклассовой классификации
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, 
                             n_redundant=5, n_classes=5, n_clusters_per_class=1, random_state=42)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Обучение модели
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Confusion Matrix - Многоклассовая классификация')
    axes[0, 0].set_xlabel('Предсказанный класс')
    axes[0, 0].set_ylabel('Истинный класс')
    
    # Точность по классам
    class_names = [f'Класс {i}' for i in range(5)]
    class_accuracy = []
    for i in range(5):
        class_mask = y_test == i
        if np.sum(class_mask) > 0:
            accuracy = (y_pred[class_mask] == y_test[class_mask]).mean()
            class_accuracy.append(accuracy)
        else:
            class_accuracy.append(0)
    
    bars = axes[0, 1].bar(class_names, class_accuracy, color='darkorange')
    axes[0, 1].set_title('Точность по классам')
    axes[0, 1].set_ylabel('Точность')
    axes[0, 1].set_ylim(0, 1)
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Добавление значений на столбцы
    for bar, acc in zip(bars, class_accuracy):
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{acc:.3f}', ha='center', va='bottom')
    
    # Распределение предсказаний
    pred_counts = pd.Series(y_pred).value_counts().sort_index()
    pred_counts.plot(kind='bar', ax=axes[1, 0], color='darkorange')
    axes[1, 0].set_title('Распределение предсказаний по классам')
    axes[1, 0].set_xlabel('Класс')
    axes[1, 0].set_ylabel('Количество')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Метрики качества
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    accuracy = accuracy_score(y_test, y_pred)
    precision_macro = precision_score(y_test, y_pred, average='macro')
    recall_macro = recall_score(y_test, y_pred, average='macro')
    f1_macro = f1_score(y_test, y_pred, average='macro')
    
    metrics_text = f'Accuracy: {accuracy:.3f}\nPrecision (macro): {precision_macro:.3f}\nRecall (macro): {recall_macro:.3f}\nF1-score (macro): {f1_macro:.3f}'
    axes[1, 1].text(0.1, 0.5, metrics_text, transform=axes[1, 1].transAxes, 
                    fontsize=12, verticalalignment='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    axes[1, 1].set_title('Метрики качества многоклассовой классификации')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/multiclass_classification_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_advanced_metrics_visualization():
    """Создает визуализацию для продвинутых метрик"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Продвинутые метрики для глубокого анализа качества', fontsize=16, fontweight='bold')
    
    # Генерация данных
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, 
                             n_redundant=5, n_classes=2, n_clusters_per_class=1, 
                             weights=[0.8, 0.2], random_state=42)  # Несбалансированные данные
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Обучение модели
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    
    # ROC кривая с разными порогами
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    axes[0, 0].plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC AUC = {roc_auc:.3f}')
    axes[0, 0].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    
    # Отметка оптимального порога
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]
    axes[0, 0].plot(fpr[optimal_idx], tpr[optimal_idx], 'ro', markersize=8, 
                   label=f'Оптимальный порог = {optimal_threshold:.3f}')
    
    axes[0, 0].set_xlabel('False Positive Rate')
    axes[0, 0].set_ylabel('True Positive Rate')
    axes[0, 0].set_title('ROC Curve с оптимальным порогом')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Precision-Recall кривая
    precision, recall, pr_thresholds = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(recall, precision)
    
    axes[0, 1].plot(recall, precision, color='darkorange', lw=2, label=f'PR AUC = {pr_auc:.3f}')
    axes[0, 1].set_xlabel('Recall')
    axes[0, 1].set_ylabel('Precision')
    axes[0, 1].set_title('Precision-Recall Curve')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Сравнение метрик
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        balanced_accuracy_score, matthews_corrcoef, cohen_kappa_score
    )
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    mcc = matthews_corrcoef(y_test, y_pred)
    kappa = cohen_kappa_score(y_test, y_pred)
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Balanced Acc', 'MCC', 'Kappa']
    values = [accuracy, precision, recall, f1, balanced_acc, mcc, kappa]
    
    bars = axes[1, 0].bar(metrics, values, color='darkorange')
    axes[1, 0].set_title('Сравнение различных метрик')
    axes[1, 0].set_ylabel('Значение метрики')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, values):
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.01,
                       f'{value:.3f}', ha='center', va='bottom')
    
    # Анализ порогов
    thresholds = np.linspace(0, 1, 100)
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []
    
    for threshold in thresholds:
        y_pred_thresh = (y_prob >= threshold).astype(int)
        if len(np.unique(y_pred_thresh)) > 1:  # Избегаем деления на ноль
            accuracies.append(accuracy_score(y_test, y_pred_thresh))
            precisions.append(precision_score(y_test, y_pred_thresh, zero_division=0))
            recalls.append(recall_score(y_test, y_pred_thresh, zero_division=0))
            f1_scores.append(f1_score(y_test, y_pred_thresh, zero_division=0))
        else:
            accuracies.append(0)
            precisions.append(0)
            recalls.append(0)
            f1_scores.append(0)
    
    axes[1, 1].plot(thresholds, accuracies, label='Accuracy', linewidth=2)
    axes[1, 1].plot(thresholds, precisions, label='Precision', linewidth=2)
    axes[1, 1].plot(thresholds, recalls, label='Recall', linewidth=2)
    axes[1, 1].plot(thresholds, f1_scores, label='F1-Score', linewidth=2)
    axes[1, 1].set_xlabel('Порог классификации')
    axes[1, 1].set_ylabel('Значение метрики')
    axes[1, 1].set_title('Влияние порога на метрики')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/advanced_metrics_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_production_system_visualization():
    """Создает визуализацию архитектуры продакшен системы"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.suptitle('Архитектура продакшен системы AutoML Gluon', fontsize=16, fontweight='bold')
    
    # Создание блоков системы
    components = {
        'Data Input': (2, 8, 2, 1),
        'Data Preprocessing': (2, 6, 2, 1),
        'Model Training': (2, 4, 2, 1),
        'Model Validation': (2, 2, 2, 1),
        'Model Registry': (6, 8, 2, 1),
        'API Gateway': (6, 6, 2, 1),
        'Prediction Service': (6, 4, 2, 1),
        'Monitoring': (6, 2, 2, 1),
        'Database': (10, 6, 2, 1),
        'Logging': (10, 4, 2, 1),
        'Alerting': (10, 2, 2, 1)
    }
    
    # Цвета для разных типов компонентов
    colors = {
        'Data Input': 'lightblue',
        'Data Preprocessing': 'lightgreen',
        'Model Training': 'lightcoral',
        'Model Validation': 'lightyellow',
        'Model Registry': 'lightpink',
        'API Gateway': 'lightgray',
        'Prediction Service': 'lightcyan',
        'Monitoring': 'lightsteelblue',
        'Database': 'lightsalmon',
        'Logging': 'lightgoldenrodyellow',
        'Alerting': 'lightcoral'
    }
    
    # Рисование компонентов
    for name, (x, y, w, h) in components.items():
        rect = plt.Rectangle((x, y), w, h, facecolor=colors[name], edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Стрелки для соединений
    arrows = [
        ((3, 8), (3, 7)),  # Data Input -> Data Preprocessing
        ((3, 6), (3, 5)),  # Data Preprocessing -> Model Training
        ((3, 4), (3, 3)),  # Model Training -> Model Validation
        ((4, 3), (6, 3)),  # Model Validation -> Model Registry
        ((7, 8), (7, 7)),  # Model Registry -> API Gateway
        ((7, 6), (7, 5)),  # API Gateway -> Prediction Service
        ((7, 4), (7, 3)),  # Prediction Service -> Monitoring
        ((8, 5), (10, 5)), # Prediction Service -> Database
        ((8, 4), (10, 4)), # Prediction Service -> Logging
        ((8, 3), (10, 3)), # Monitoring -> Alerting
    ]
    
    for (x1, y1), (x2, y2) in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='darkblue'))
    
    # Настройка осей
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Добавление заголовков секций
    ax.text(3, 9.5, 'Обучение и валидация', ha='center', fontsize=12, fontweight='bold')
    ax.text(7, 9.5, 'Продакшен сервисы', ha='center', fontsize=12, fontweight='bold')
    ax.text(11, 9.5, 'Инфраструктура', ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/production_system_architecture.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Основная функция для генерации всех визуализаций"""
    print("Генерация визуализаций для главы 12_examples.md...")
    
    # Создание директории для изображений
    import os
    os.makedirs('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized', exist_ok=True)
    
    # Генерация всех визуализаций
    print("1. Создание сравнения метрик...")
    create_metrics_comparison_visualization()
    
    print("2. Создание визуализации банковской задачи...")
    create_bank_classification_visualization()
    
    print("3. Создание визуализации задачи недвижимости...")
    create_real_estate_regression_visualization()
    
    print("4. Создание визуализации временных рядов...")
    create_time_series_visualization()
    
    print("5. Создание визуализации многоклассовой классификации...")
    create_multiclass_classification_visualization()
    
    print("6. Создание визуализации продвинутых метрик...")
    create_advanced_metrics_visualization()
    
    print("7. Создание визуализации продакшен системы...")
    create_production_system_visualization()
    
    print("Все визуализации успешно созданы!")

if __name__ == "__main__":
    main()
