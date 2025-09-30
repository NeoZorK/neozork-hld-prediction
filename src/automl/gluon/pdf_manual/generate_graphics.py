#!/usr/bin/env python3
"""
Скрипт для создания графиков и диаграмм для учебника AutoML Gluon
Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd
from pathlib import Path
import os

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_installation_flowchart():
    """Создание блок-схемы установки"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 9.5, 'Установка AutoML Gluon', fontsize=16, fontweight='bold', ha='center')
    
    # Блоки
    blocks = [
        (5, 8.5, 2, 0.5, 'Проверка Python 3.7+'),
        (5, 7.5, 2, 0.5, 'Установка pip/conda'),
        (5, 6.5, 2, 0.5, 'pip install autogluon'),
        (5, 5.5, 2, 0.5, 'Проверка установки'),
        (5, 4.5, 2, 0.5, 'Настройка окружения'),
        (5, 3.5, 2, 0.5, 'Тест импорта'),
        (5, 2.5, 2, 0.5, 'Готово!')
    ]
    
    # Рисование блоков
    for x, y, w, h, text in blocks:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='blue', facecolor='lightblue', alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Стрелки
    for i in range(len(blocks)-1):
        ax.arrow(5, blocks[i][1] - 0.3, 0, -0.4, head_width=0.1, head_length=0.1, 
                fc='red', ec='red')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/installation_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_architecture_diagram():
    """Создание диаграммы архитектуры AutoML Gluon"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(6, 9.5, 'Архитектура AutoML Gluon', fontsize=16, fontweight='bold', ha='center')
    
    # Основные компоненты
    components = [
        (2, 8, 2, 1, 'TabularPredictor', 'lightgreen'),
        (6, 8, 2, 1, 'TimeSeriesPredictor', 'lightblue'),
        (10, 8, 2, 1, 'ImagePredictor', 'lightcoral'),
        (2, 6, 2, 1, 'Feature Engineering', 'lightyellow'),
        (6, 6, 2, 1, 'Model Selection', 'lightpink'),
        (10, 6, 2, 1, 'Ensemble', 'lightgray'),
        (2, 4, 2, 1, 'GBM', 'orange'),
        (4, 4, 2, 1, 'XGBoost', 'cyan'),
        (6, 4, 2, 1, 'CatBoost', 'magenta'),
        (8, 4, 2, 1, 'Random Forest', 'yellow'),
        (10, 4, 2, 1, 'Neural Networks', 'purple'),
        (6, 2, 2, 1, 'Validation', 'lightsteelblue'),
        (6, 0.5, 2, 1, 'Predictions', 'lightgreen')
    ]
    
    # Рисование компонентов
    for x, y, w, h, text, color in components:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Соединения
    connections = [
        (2, 7.5, 6, 7.5),  # TabularPredictor -> TimeSeriesPredictor
        (6, 7.5, 10, 7.5), # TimeSeriesPredictor -> ImagePredictor
        (2, 6.5, 2, 5.5),  # TabularPredictor -> Feature Engineering
        (6, 6.5, 6, 5.5),  # TimeSeriesPredictor -> Model Selection
        (10, 6.5, 10, 5.5), # ImagePredictor -> Ensemble
    ]
    
    for x1, y1, x2, y2 in connections:
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_metrics_comparison():
    """Создание графика сравнения метрик"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Метрики для классификации
    classification_metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    classification_values = [0.85, 0.82, 0.88, 0.85, 0.91]
    
    bars1 = ax1.bar(classification_metrics, classification_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax1.set_title('Метрики классификации', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Значение', fontsize=12)
    ax1.set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars1, classification_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Метрики для регрессии
    regression_metrics = ['RMSE', 'MAE', 'R²', 'MAPE', 'SMAPE']
    regression_values = [0.12, 0.08, 0.89, 0.15, 0.13]
    
    bars2 = ax2.bar(regression_metrics, regression_values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax2.set_title('Метрики регрессии', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Значение', fontsize=12)
    ax2.set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars2, regression_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_validation_methods():
    """Создание диаграммы методов валидации"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 9.5, 'Методы валидации в AutoML Gluon', fontsize=16, fontweight='bold', ha='center')
    
    # Методы валидации
    methods = [
        (2, 8, 1.5, 1, 'Holdout\nValidation', 'lightblue'),
        (5, 8, 1.5, 1, 'K-Fold\nCV', 'lightgreen'),
        (8, 8, 1.5, 1, 'Stratified\nCV', 'lightcoral'),
        (2, 6, 1.5, 1, 'Time Series\nSplit', 'lightyellow'),
        (5, 6, 1.5, 1, 'Walk-Forward\nValidation', 'lightpink'),
        (8, 6, 1.5, 1, 'Monte Carlo\nValidation', 'lightgray'),
        (2, 4, 1.5, 1, 'Bootstrap\nValidation', 'orange'),
        (5, 4, 1.5, 1, 'Cross-Validation\nwith Groups', 'cyan'),
        (8, 4, 1.5, 1, 'Nested\nCV', 'magenta'),
        (5, 2, 1.5, 1, 'Backtest\nValidation', 'yellow')
    ]
    
    # Рисование методов
    for x, y, w, h, text, color in methods:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Соединения
    center_connections = [
        (5, 7.5, 5, 6.5),  # K-Fold -> Walk-Forward
        (5, 5.5, 5, 4.5),  # Walk-Forward -> Cross-Validation with Groups
        (5, 3.5, 5, 2.5),  # Cross-Validation with Groups -> Backtest
    ]
    
    for x1, y1, x2, y2 in center_connections:
        ax.arrow(x1, y1, 0, -0.4, head_width=0.1, head_length=0.1, 
                fc='red', ec='red')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/validation_methods.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_production_architecture():
    """Создание диаграммы продакшен архитектуры"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(6, 9.5, 'Продакшен архитектура AutoML Gluon', fontsize=16, fontweight='bold', ha='center')
    
    # Компоненты системы
    components = [
        (2, 8, 2, 1, 'Data\nSources', 'lightblue'),
        (6, 8, 2, 1, 'Data\nPipeline', 'lightgreen'),
        (10, 8, 2, 1, 'Feature\nStore', 'lightcoral'),
        (2, 6, 2, 1, 'Model\nTraining', 'lightyellow'),
        (6, 6, 2, 1, 'Model\nRegistry', 'lightpink'),
        (10, 6, 2, 1, 'Model\nServing', 'lightgray'),
        (2, 4, 2, 1, 'API\nGateway', 'orange'),
        (6, 4, 2, 1, 'Load\nBalancer', 'cyan'),
        (10, 4, 2, 1, 'Monitoring', 'magenta'),
        (2, 2, 2, 1, 'Docker\nContainers', 'yellow'),
        (6, 2, 2, 1, 'Kubernetes\nCluster', 'purple'),
        (10, 2, 2, 1, 'CI/CD\nPipeline', 'lightsteelblue')
    ]
    
    # Рисование компонентов
    for x, y, w, h, text, color in components:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Соединения
    connections = [
        (2, 7.5, 6, 7.5),  # Data Sources -> Data Pipeline
        (6, 7.5, 10, 7.5), # Data Pipeline -> Feature Store
        (2, 6.5, 2, 5.5),  # Data Sources -> Model Training
        (6, 6.5, 6, 5.5),  # Data Pipeline -> Model Registry
        (10, 6.5, 10, 5.5), # Feature Store -> Model Serving
        (2, 4.5, 2, 3.5),  # Model Training -> API Gateway
        (6, 4.5, 6, 3.5),  # Model Registry -> Load Balancer
        (10, 4.5, 10, 3.5), # Model Serving -> Monitoring
        (2, 2.5, 2, 1.5),  # API Gateway -> Docker Containers
        (6, 2.5, 6, 1.5),  # Load Balancer -> Kubernetes Cluster
        (10, 2.5, 10, 1.5), # Monitoring -> CI/CD Pipeline
    ]
    
    for x1, y1, x2, y2 in connections:
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
        # Добавление стрелок
        ax.arrow(x1, y1, 0, -0.4, head_width=0.1, head_length=0.1, 
                fc='red', ec='red')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/production_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_retraining_workflow():
    """Создание диаграммы процесса переобучения"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 9.5, 'Процесс переобучения моделей', fontsize=16, fontweight='bold', ha='center')
    
    # Этапы переобучения
    stages = [
        (2, 8, 1.5, 0.8, 'Мониторинг\nпроизводительности', 'lightblue'),
        (4, 8, 1.5, 0.8, 'Обнаружение\nдрейфа данных', 'lightgreen'),
        (6, 8, 1.5, 0.8, 'Триггер\nпереобучения', 'lightcoral'),
        (8, 8, 1.5, 0.8, 'Загрузка\nновых данных', 'lightyellow'),
        (2, 6, 1.5, 0.8, 'Подготовка\nданных', 'lightpink'),
        (4, 6, 1.5, 0.8, 'Обучение\nновой модели', 'lightgray'),
        (6, 6, 1.5, 0.8, 'Валидация\nмодели', 'orange'),
        (8, 6, 1.5, 0.8, 'A/B тестирование', 'cyan'),
        (2, 4, 1.5, 0.8, 'Деплой\nмодели', 'magenta'),
        (4, 4, 1.5, 0.8, 'Мониторинг\nв продакшене', 'yellow'),
        (6, 4, 1.5, 0.8, 'Откат при\nпроблемах', 'purple'),
        (8, 4, 1.5, 0.8, 'Обновление\nметаданных', 'lightsteelblue')
    ]
    
    # Рисование этапов
    for x, y, w, h, text, color in stages:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=7, fontweight='bold')
    
    # Стрелки процесса
    arrows = [
        (2, 7.6, 4, 7.6),  # Мониторинг -> Обнаружение дрейфа
        (4, 7.6, 6, 7.6),  # Обнаружение дрейфа -> Триггер
        (6, 7.6, 8, 7.6),  # Триггер -> Загрузка данных
        (8, 7.6, 2, 6.4),  # Загрузка данных -> Подготовка данных
        (2, 5.6, 4, 5.6),  # Подготовка -> Обучение
        (4, 5.6, 6, 5.6),  # Обучение -> Валидация
        (6, 5.6, 8, 5.6),  # Валидация -> A/B тестирование
        (8, 5.6, 2, 4.4),  # A/B тестирование -> Деплой
        (2, 3.6, 4, 3.6),  # Деплой -> Мониторинг
        (4, 3.6, 6, 3.6),  # Мониторинг -> Откат
        (6, 3.6, 8, 3.6),  # Откат -> Обновление метаданных
    ]
    
    for x1, y1, x2, y2 in arrows:
        ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.1, head_length=0.1, 
                fc='red', ec='red')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/retraining_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_apple_silicon_optimization():
    """Создание диаграммы оптимизации для Apple Silicon"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 9.5, 'Оптимизация для Apple Silicon (M1/M2/M3)', fontsize=16, fontweight='bold', ha='center')
    
    # Компоненты оптимизации
    components = [
        (2, 8, 1.5, 1, 'MLX\nFramework', 'lightblue'),
        (4, 8, 1.5, 1, 'Ray\nDistributed', 'lightgreen'),
        (6, 8, 1.5, 1, 'OpenMP\nParallel', 'lightcoral'),
        (8, 8, 1.5, 1, 'MPS\nAcceleration', 'lightyellow'),
        (2, 6, 1.5, 1, 'CUDA\nDisabled', 'lightpink'),
        (4, 6, 1.5, 1, 'Memory\nOptimization', 'lightgray'),
        (6, 6, 1.5, 1, 'CPU\nThreading', 'orange'),
        (8, 6, 1.5, 1, 'GPU\nUtilization', 'cyan'),
        (2, 4, 1.5, 1, 'Data\nPreprocessing', 'magenta'),
        (4, 4, 1.5, 1, 'Model\nTraining', 'yellow'),
        (6, 4, 1.5, 1, 'Inference\nSpeed', 'purple'),
        (8, 4, 1.5, 1, 'Performance\nMonitoring', 'lightsteelblue'),
        (5, 2, 1.5, 1, 'Apple Silicon\nOptimized Pipeline', 'red')
    ]
    
    # Рисование компонентов
    for x, y, w, h, text, color in components:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=7, fontweight='bold')
    
    # Соединения к центральному компоненту
    center_x, center_y = 5, 2
    for x, y, w, h, text, color in components[:-1]:  # Все кроме центрального
        ax.plot([x, center_x], [y-h/2, center_y+h/2], 'k-', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/apple_silicon_optimization.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_comparison():
    """Создание графика сравнения производительности"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Сравнение времени обучения
    models = ['GBM', 'XGBoost', 'CatBoost', 'Random Forest', 'Neural Network']
    training_time = [120, 180, 200, 90, 300]
    inference_time = [5, 8, 10, 15, 20]
    
    x = np.arange(len(models))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, training_time, width, label='Время обучения (сек)', color='lightblue')
    bars2 = ax1.bar(x + width/2, inference_time, width, label='Время предсказания (мс)', color='lightcoral')
    
    ax1.set_xlabel('Модели')
    ax1.set_ylabel('Время')
    ax1.set_title('Сравнение производительности моделей')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=45)
    ax1.legend()
    
    # Добавление значений на столбцы
    for bar, value in zip(bars1, training_time):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                f'{value}s', ha='center', va='bottom', fontsize=8)
    
    for bar, value in zip(bars2, inference_time):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{value}ms', ha='center', va='bottom', fontsize=8)
    
    # Сравнение точности
    accuracy_scores = [0.85, 0.87, 0.89, 0.82, 0.91]
    
    bars3 = ax2.bar(models, accuracy_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax2.set_xlabel('Модели')
    ax2.set_ylabel('Точность')
    ax2.set_title('Сравнение точности моделей')
    ax2.set_xticklabels(models, rotation=45)
    ax2.set_ylim(0, 1)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars3, accuracy_scores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_troubleshooting_flowchart():
    """Создание блок-схемы troubleshooting"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 11.5, 'Troubleshooting AutoML Gluon', fontsize=16, fontweight='bold', ha='center')
    
    # Блоки troubleshooting
    blocks = [
        (5, 10.5, 2, 0.8, 'Проблема с AutoML Gluon', 'lightcoral'),
        (2, 9, 1.5, 0.8, 'Ошибка\nустановки', 'lightblue'),
        (5, 9, 1.5, 0.8, 'Ошибка\nобучения', 'lightgreen'),
        (8, 9, 1.5, 0.8, 'Ошибка\nпредсказания', 'lightyellow'),
        (2, 7, 1.5, 0.8, 'Проверить\nзависимости', 'lightpink'),
        (5, 7, 1.5, 0.8, 'Проверить\nданные', 'lightgray'),
        (8, 7, 1.5, 0.8, 'Проверить\nмодель', 'orange'),
        (2, 5, 1.5, 0.8, 'Переустановить\nпакеты', 'cyan'),
        (5, 5, 1.5, 0.8, 'Очистить\nданные', 'magenta'),
        (8, 5, 1.5, 0.8, 'Переобучить\nмодель', 'yellow'),
        (5, 3, 2, 0.8, 'Проблема решена?', 'lightsteelblue'),
        (2, 1.5, 1.5, 0.8, 'Да', 'lightgreen'),
        (8, 1.5, 1.5, 0.8, 'Нет\nОбратиться\nк документации', 'lightcoral')
    ]
    
    # Рисование блоков
    for x, y, w, h, text, color in blocks:
        rect = patches.Rectangle((x-w/2, y-h/2), w, h, linewidth=2, 
                                edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Стрелки
    arrows = [
        (5, 10.1, 2, 9.4),  # Проблема -> Ошибка установки
        (5, 10.1, 5, 9.4),  # Проблема -> Ошибка обучения
        (5, 10.1, 8, 9.4),  # Проблема -> Ошибка предсказания
        (2, 8.6, 2, 7.4),   # Ошибка установки -> Проверить зависимости
        (5, 8.6, 5, 7.4),   # Ошибка обучения -> Проверить данные
        (8, 8.6, 8, 7.4),   # Ошибка предсказания -> Проверить модель
        (2, 6.6, 2, 5.4),   # Проверить зависимости -> Переустановить пакеты
        (5, 6.6, 5, 5.4),   # Проверить данные -> Очистить данные
        (8, 6.6, 8, 5.4),   # Проверить модель -> Переобучить модель
        (2, 4.6, 3, 3.4),   # Переустановить пакеты -> Проблема решена?
        (5, 4.6, 5, 3.4),   # Очистить данные -> Проблема решена?
        (8, 4.6, 7, 3.4),   # Переобучить модель -> Проблема решена?
        (4, 2.6, 2, 1.9),   # Проблема решена? -> Да
        (6, 2.6, 8, 1.9),   # Проблема решена? -> Нет
    ]
    
    for x1, y1, x2, y2 in arrows:
        ax.arrow(x1, y1, x2-x1, y2-y1, head_width=0.1, head_length=0.1, 
                fc='red', ec='red')
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/troubleshooting_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Основная функция для создания всех графиков"""
    
    print("=== Создание графиков для учебника AutoML Gluon ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    # Создание директории для изображений
    images_dir = Path('docs/automl/gluon/images')
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Создание всех графиков
    graphics_functions = [
        create_installation_flowchart,
        create_architecture_diagram,
        create_metrics_comparison,
        create_validation_methods,
        create_production_architecture,
        create_retraining_workflow,
        create_apple_silicon_optimization,
        create_performance_comparison,
        create_troubleshooting_flowchart
    ]
    
    for i, func in enumerate(graphics_functions, 1):
        print(f"Создание графика {i}/{len(graphics_functions)}: {func.__name__}")
        try:
            func()
            print(f"✓ График {func.__name__} создан успешно")
        except Exception as e:
            print(f"✗ Ошибка создания графика {func.__name__}: {e}")
    
    print(f"\n🎉 Все графики созданы в директории: {images_dir.absolute()}")
    print("Графики готовы для использования в учебнике!")

if __name__ == "__main__":
    main()
