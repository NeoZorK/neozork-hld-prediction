#!/usr/bin/env python3
"""
Генерация визуализаций для главы 14 - Продвинутая ML-система
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Arrow
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import pandas as pd
import os

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_advanced_architecture_visualization():
    """Создание схемы продвинутой архитектуры системы"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 9.5, 'Продвинутая ML-система для DEX торговли', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Слой данных
    data_layer = FancyBboxPatch((0.5, 8), 9, 0.8, 
                               boxstyle="round,pad=0.1", 
                               facecolor='lightblue', alpha=0.7)
    ax.add_patch(data_layer)
    ax.text(5, 8.4, 'Слой данных', fontsize=14, fontweight='bold', ha='center')
    
    # Источники данных
    sources = ['Binance API', 'Coinbase API', 'Kraken API', 'News API', 'Social Media']
    for i, source in enumerate(sources):
        x = 1 + i * 1.6
        rect = Rectangle((x, 7.5), 1.2, 0.3, facecolor='lightcyan', edgecolor='navy')
        ax.add_patch(rect)
        ax.text(x + 0.6, 7.65, source, fontsize=8, ha='center')
    
    # Слой обработки данных
    processing_layer = FancyBboxPatch((0.5, 6.5), 9, 0.8, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='lightgreen', alpha=0.7)
    ax.add_patch(processing_layer)
    ax.text(5, 6.9, 'Слой обработки данных', fontsize=14, fontweight='bold', ha='center')
    
    # Компоненты обработки
    components = ['Data Collector', 'Feature Engineering', 'Data Validation', 'Preprocessing']
    for i, component in enumerate(components):
        x = 1.5 + i * 1.5
        rect = Rectangle((x, 6), 1, 0.3, facecolor='lightseagreen', edgecolor='darkgreen')
        ax.add_patch(rect)
        ax.text(x + 0.5, 6.15, component, fontsize=8, ha='center')
    
    # Слой моделей
    model_layer = FancyBboxPatch((0.5, 4.5), 9, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor='lightyellow', alpha=0.7)
    ax.add_patch(model_layer)
    ax.text(5, 5.7, 'Слой моделей', fontsize=14, fontweight='bold', ha='center')
    
    # Модели
    models = ['Price Direction', 'Volatility', 'Volume', 'Sentiment', 'Macro']
    for i, model in enumerate(models):
        x = 1 + i * 1.6
        rect = Rectangle((x, 4.8), 1.2, 0.4, facecolor='gold', edgecolor='orange')
        ax.add_patch(rect)
        ax.text(x + 0.6, 5, model, fontsize=8, ha='center')
    
    # Ансамбль
    ensemble = Circle((5, 4.2), 0.3, facecolor='red', edgecolor='darkred')
    ax.add_patch(ensemble)
    ax.text(5, 4.2, 'Ensemble', fontsize=8, ha='center', color='white', fontweight='bold')
    
    # Слой риск-менеджмента
    risk_layer = FancyBboxPatch((0.5, 3), 9, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor='lightcoral', alpha=0.7)
    ax.add_patch(risk_layer)
    ax.text(5, 3.4, 'Слой риск-менеджмента', fontsize=14, fontweight='bold', ha='center')
    
    # Компоненты риск-менеджмента
    risk_components = ['Position Sizing', 'Stop Loss', 'Portfolio Optimization', 'VaR Calculation']
    for i, component in enumerate(risk_components):
        x = 1.5 + i * 1.5
        rect = Rectangle((x, 2.5), 1, 0.3, facecolor='salmon', edgecolor='darkred')
        ax.add_patch(rect)
        ax.text(x + 0.5, 2.65, component, fontsize=8, ha='center')
    
    # Слой мониторинга
    monitoring_layer = FancyBboxPatch((0.5, 1), 9, 1, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='lightpink', alpha=0.7)
    ax.add_patch(monitoring_layer)
    ax.text(5, 1.4, 'Слой мониторинга', fontsize=14, fontweight='bold', ha='center')
    
    # Компоненты мониторинга
    monitoring_components = ['Performance Tracking', 'Alert System', 'Auto Retrain', 'Health Check']
    for i, component in enumerate(monitoring_components):
        x = 1.5 + i * 1.5
        rect = Rectangle((x, 0.5), 1, 0.3, facecolor='pink', edgecolor='purple')
        ax.add_patch(rect)
        ax.text(x + 0.5, 0.65, component, fontsize=8, ha='center')
    
    # Стрелки между слоями
    for i in range(4):
        y_start = 8 - i * 1.5
        y_end = y_start - 0.5
        arrow = Arrow(5, y_start, 0, -0.3, width=0.1, facecolor='black')
        ax.add_patch(arrow)
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/advanced_production_flow.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_multi_model_system_visualization():
    """Создание диаграммы системы множественных моделей"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(6, 9.5, 'Система множественных моделей', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Входные данные
    input_data = Circle((1, 8), 0.5, facecolor='lightblue', edgecolor='navy')
    ax.add_patch(input_data)
    ax.text(1, 8, 'Data', fontsize=10, ha='center', fontweight='bold')
    
    # Модели
    models = [
        ('Price Direction', 3, 7, 'lightgreen'),
        ('Volatility', 6, 7, 'lightyellow'),
        ('Volume', 9, 7, 'lightcoral'),
        ('Sentiment', 3, 5, 'lightpink'),
        ('Macro', 6, 5, 'lightgray'),
        ('Technical', 9, 5, 'lightcyan')
    ]
    
    for name, x, y, color in models:
        # Модель
        model_rect = Rectangle((x-0.8, y-0.4), 1.6, 0.8, 
                              facecolor=color, edgecolor='black')
        ax.add_patch(model_rect)
        ax.text(x, y, name, fontsize=9, ha='center', fontweight='bold')
        
        # Стрелка от данных к модели
        arrow = Arrow(1.5, 8, x-1.3, y-7.6, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Ансамбль
    ensemble = Circle((6, 3), 0.8, facecolor='red', edgecolor='darkred')
    ax.add_patch(ensemble)
    ax.text(6, 3, 'Ensemble\nModel', fontsize=10, ha='center', 
            color='white', fontweight='bold')
    
    # Стрелки от моделей к ансамблю
    for name, x, y, color in models:
        arrow = Arrow(x, y-0.4, 6-x, 3.8-y, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Финальное предсказание
    prediction = Rectangle((5, 1), 2, 0.8, facecolor='gold', edgecolor='orange')
    ax.add_patch(prediction)
    ax.text(6, 1.4, 'Final\nPrediction', fontsize=10, ha='center', fontweight='bold')
    
    # Стрелка от ансамбля к предсказанию
    arrow = Arrow(6, 2.2, 0, -0.2, width=0.1, facecolor='black')
    ax.add_patch(arrow)
    
    # Метрики производительности
    metrics_text = """
    Модели показывают разную производительность:
    • Price Direction: 75% точность
    • Volatility: 68% точность  
    • Volume: 72% точность
    • Sentiment: 65% точность
    • Macro: 70% точность
    • Technical: 78% точность
    
    Ensemble: 82% точность
    """
    
    ax.text(0.5, 4, metrics_text, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/multi_model_system.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_ensemble_visualization():
    """Создание визуализации ансамблевой модели"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Заголовок
    ax.text(5, 7.5, 'Ансамблевая модель - объединение предсказаний', 
            fontsize=16, fontweight='bold', ha='center')
    
    # Входные модели
    models = [
        ('Model A\n(75%)', 1, 6, 'lightblue'),
        ('Model B\n(68%)', 3, 6, 'lightgreen'),
        ('Model C\n(72%)', 5, 6, 'lightyellow'),
        ('Model D\n(65%)', 7, 6, 'lightcoral'),
        ('Model E\n(70%)', 9, 6, 'lightpink')
    ]
    
    for name, x, y, color in models:
        # Модель
        model_circle = Circle((x, y), 0.6, facecolor=color, edgecolor='black')
        ax.add_patch(model_circle)
        ax.text(x, y, name, fontsize=8, ha='center', fontweight='bold')
        
        # Предсказание
        pred_rect = Rectangle((x-0.4, y-1.5), 0.8, 0.6, 
                             facecolor=color, alpha=0.7, edgecolor='black')
        ax.add_patch(pred_rect)
        ax.text(x, y-1.2, 'Pred', fontsize=7, ha='center')
    
    # Ансамбль
    ensemble = Circle((5, 3), 1, facecolor='red', edgecolor='darkred')
    ax.add_patch(ensemble)
    ax.text(5, 3, 'Ensemble\nModel', fontsize=10, ha='center', 
            color='white', fontweight='bold')
    
    # Стрелки от моделей к ансамблю
    for name, x, y, color in models:
        arrow = Arrow(x, y-0.6, 5-x, 4-y, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Финальное предсказание
    final_pred = Rectangle((4, 1), 2, 0.8, facecolor='gold', edgecolor='orange')
    ax.add_patch(final_pred)
    ax.text(5, 1.4, 'Final\nPrediction\n(82%)', fontsize=10, ha='center', fontweight='bold')
    
    # Стрелка от ансамбля к финальному предсказанию
    arrow = Arrow(5, 2, 0, -0.2, width=0.1, facecolor='black')
    ax.add_patch(arrow)
    
    # Объяснение
    explanation = """
    Ансамбль объединяет предсказания:
    
    1. Взвешенное голосование
    2. Мета-обучение
    3. Бутстрап агрегация
    4. Стекинг
    
    Результат: более точные предсказания
    """
    
    ax.text(0.5, 2, explanation, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/ensemble_model_visualization.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_risk_management_visualization():
    """Создание схемы продвинутого риск-менеджмента"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(6, 9.5, 'Продвинутый риск-менеджмент', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Входные данные
    input_data = Rectangle((1, 8), 2, 0.8, facecolor='lightblue', edgecolor='navy')
    ax.add_patch(input_data)
    ax.text(2, 8.4, 'Market Data', fontsize=10, ha='center', fontweight='bold')
    
    # Компоненты риск-менеджмента
    risk_components = [
        ('Position Sizing\n(Kelly Criterion)', 3, 6.5, 'lightgreen'),
        ('Stop Loss\n(Dynamic)', 6, 6.5, 'lightyellow'),
        ('Portfolio\nOptimization', 9, 6.5, 'lightcoral'),
        ('VaR Calculation\n(95% confidence)', 3, 4.5, 'lightpink'),
        ('Correlation\nAnalysis', 6, 4.5, 'lightgray'),
        ('Stress Testing', 9, 4.5, 'lightcyan')
    ]
    
    for name, x, y, color in risk_components:
        # Компонент
        comp_rect = Rectangle((x-1, y-0.6), 2, 1.2, 
                             facecolor=color, edgecolor='black')
        ax.add_patch(comp_rect)
        ax.text(x, y, name, fontsize=9, ha='center', fontweight='bold')
        
        # Стрелка от данных к компоненту
        arrow = Arrow(2.5, 8, x-2, y-7.5, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Риск-менеджер
    risk_manager = Circle((6, 2.5), 1, facecolor='red', edgecolor='darkred')
    ax.add_patch(risk_manager)
    ax.text(6, 2.5, 'Risk\nManager', fontsize=10, ha='center', 
            color='white', fontweight='bold')
    
    # Стрелки от компонентов к риск-менеджеру
    for name, x, y, color in risk_components:
        arrow = Arrow(x, y-0.6, 6-x, 3.1-y, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Финальные решения
    decisions = Rectangle((4, 0.5), 4, 1, facecolor='gold', edgecolor='orange')
    ax.add_patch(decisions)
    ax.text(6, 1, 'Risk-Adjusted\nDecisions', fontsize=12, ha='center', fontweight='bold')
    
    # Стрелка от риск-менеджера к решениям
    arrow = Arrow(6, 1.5, 0, -0.2, width=0.1, facecolor='black')
    ax.add_patch(arrow)
    
    # Метрики риска
    risk_metrics = """
    Ключевые метрики риска:
    
    • Максимальная просадка: 5.8%
    • VaR (95%): 2.3%
    • Коэффициент Шарпа: 2.1
    • Корреляция портфеля: <0.3
    • Ликвидность: >$1M
    """
    
    ax.text(0.5, 3, risk_metrics, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/advanced_risk_management.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_microservices_architecture():
    """Создание диаграммы микросервисной архитектуры"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(7, 9.5, 'Микросервисная архитектура ML-системы', 
            fontsize=18, fontweight='bold', ha='center')
    
    # API Gateway
    gateway = Rectangle((6, 8), 2, 0.8, facecolor='lightblue', edgecolor='navy')
    ax.add_patch(gateway)
    ax.text(7, 8.4, 'API Gateway', fontsize=12, ha='center', fontweight='bold')
    
    # Микросервисы
    services = [
        ('Data Service', 1, 6, 'lightgreen'),
        ('Model Service', 4, 6, 'lightyellow'),
        ('Risk Service', 7, 6, 'lightcoral'),
        ('Trading Service', 10, 6, 'lightpink'),
        ('Monitoring Service', 13, 6, 'lightgray')
    ]
    
    for name, x, y, color in services:
        # Сервис
        service_rect = Rectangle((x-0.8, y-0.6), 1.6, 1.2, 
                                facecolor=color, edgecolor='black')
        ax.add_patch(service_rect)
        ax.text(x, y, name, fontsize=9, ha='center', fontweight='bold')
        
        # Стрелка от Gateway к сервису
        arrow = Arrow(7, 8, x-6, y-7.4, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # База данных
    database = Rectangle((6, 3), 2, 0.8, facecolor='lightcyan', edgecolor='teal')
    ax.add_patch(database)
    ax.text(7, 3.4, 'Database', fontsize=12, ha='center', fontweight='bold')
    
    # Стрелки от сервисов к базе данных
    for name, x, y, color in services:
        arrow = Arrow(x, y-0.6, 7-x, 3.8-y, width=0.05, facecolor='black')
        ax.add_patch(arrow)
    
    # Мониторинг
    monitoring = Rectangle((2, 1), 10, 1, facecolor='lightyellow', edgecolor='orange')
    ax.add_patch(monitoring)
    ax.text(7, 1.5, 'Monitoring & Logging', fontsize=12, ha='center', fontweight='bold')
    
    # Преимущества
    advantages = """
    Преимущества микросервисов:
    
    • Независимое масштабирование
    • Изоляция отказов
    • Технологическое разнообразие
    • Независимое развертывание
    • Легкость тестирования
    """
    
    ax.text(0.5, 4, advantages, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/microservices_architecture.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_kubernetes_deployment():
    """Создание схемы Kubernetes деплоя"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Заголовок
    ax.text(6, 9.5, 'Kubernetes Deployment', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Namespace
    namespace = Rectangle((1, 8), 10, 1, facecolor='lightblue', alpha=0.3, edgecolor='navy')
    ax.add_patch(namespace)
    ax.text(6, 8.5, 'ML-System Namespace', fontsize=14, ha='center', fontweight='bold')
    
    # Pods
    pods = [
        ('API Gateway\nPod', 2, 6.5, 'lightgreen'),
        ('Data Service\nPod', 4, 6.5, 'lightyellow'),
        ('Model Service\nPod', 6, 6.5, 'lightcoral'),
        ('Risk Service\nPod', 8, 6.5, 'lightpink'),
        ('Trading Service\nPod', 10, 6.5, 'lightgray')
    ]
    
    for name, x, y, color in pods:
        # Pod
        pod_rect = Rectangle((x-0.6, y-0.4), 1.2, 0.8, 
                           facecolor=color, edgecolor='black')
        ax.add_patch(pod_rect)
        ax.text(x, y, name, fontsize=8, ha='center', fontweight='bold')
    
    # Services
    services = [
        ('API Service', 2, 4.5, 'lightcyan'),
        ('Data Service', 4, 4.5, 'lightcyan'),
        ('Model Service', 6, 4.5, 'lightcyan'),
        ('Risk Service', 8, 4.5, 'lightcyan'),
        ('Trading Service', 10, 4.5, 'lightcyan')
    ]
    
    for name, x, y, color in services:
        # Service
        service_rect = Rectangle((x-0.6, y-0.3), 1.2, 0.6, 
                               facecolor=color, edgecolor='blue')
        ax.add_patch(service_rect)
        ax.text(x, y, name, fontsize=8, ha='center')
    
    # Ingress
    ingress = Rectangle((4, 2.5), 4, 0.8, facecolor='gold', edgecolor='orange')
    ax.add_patch(ingress)
    ax.text(6, 2.9, 'Ingress Controller', fontsize=12, ha='center', fontweight='bold')
    
    # ConfigMap и Secrets
    config = Rectangle((1, 1), 2, 0.8, facecolor='lightgreen', edgecolor='green')
    ax.add_patch(config)
    ax.text(2, 1.4, 'ConfigMap', fontsize=10, ha='center', fontweight='bold')
    
    secrets = Rectangle((9, 1), 2, 0.8, facecolor='lightcoral', edgecolor='red')
    ax.add_patch(secrets)
    ax.text(10, 1.4, 'Secrets', fontsize=10, ha='center', fontweight='bold')
    
    # Характеристики
    characteristics = """
    Kubernetes особенности:
    
    • Автоматическое масштабирование
    • Self-healing
    • Rolling updates
    • Resource limits
    • Health checks
    • Load balancing
    """
    
    ax.text(0.5, 3.5, characteristics, fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
    
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/kubernetes_deployment.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_advanced_monitoring_dashboard():
    """Создание дашборда продвинутого мониторинга"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # График 1: Производительность моделей
    models = ['Price Direction', 'Volatility', 'Volume', 'Sentiment', 'Macro', 'Ensemble']
    accuracy = [0.75, 0.68, 0.72, 0.65, 0.70, 0.82]
    
    bars1 = ax1.bar(models, accuracy, color=['lightblue', 'lightgreen', 'lightyellow', 
                                           'lightcoral', 'lightpink', 'red'])
    ax1.set_title('Производительность моделей', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Точность')
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='x', rotation=45)
    
    # Добавление значений на столбцы
    for bar, acc in zip(bars1, accuracy):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{acc:.2f}', ha='center', fontweight='bold')
    
    # График 2: Метрики риска
    risk_metrics = ['Max Drawdown', 'VaR (95%)', 'Sharpe Ratio', 'Win Rate']
    values = [0.058, 0.023, 2.1, 0.684]
    colors = ['red', 'orange', 'green', 'blue']
    
    bars2 = ax2.bar(risk_metrics, values, color=colors)
    ax2.set_title('Метрики риска', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Значение')
    ax2.tick_params(axis='x', rotation=45)
    
    # Добавление значений на столбцы
    for bar, val in zip(bars2, values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{val:.3f}', ha='center', fontweight='bold')
    
    # График 3: Временной ряд доходности
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    returns = np.cumsum(np.random.normal(0.001, 0.02, 100))
    
    ax3.plot(dates, returns, linewidth=2, color='blue')
    ax3.set_title('Кумулятивная доходность', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Доходность')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # График 4: Статус системы
    components = ['API Gateway', 'Data Service', 'Model Service', 'Risk Service', 'Trading Service']
    status = ['Healthy', 'Healthy', 'Warning', 'Healthy', 'Healthy']
    colors = ['green', 'green', 'orange', 'green', 'green']
    
    bars4 = ax4.barh(components, [1]*len(components), color=colors)
    ax4.set_title('Статус компонентов системы', fontsize=14, fontweight='bold')
    ax4.set_xlabel('Статус')
    
    # Добавление статуса на столбцы
    for bar, stat in zip(bars4, status):
        ax4.text(0.5, bar.get_y() + bar.get_height()/2, stat, 
                ha='center', va='center', fontweight='bold')
    
    plt.suptitle('Продвинутый мониторинг ML-системы', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/advanced_monitoring_dashboard.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_comparison():
    """Создание сравнения простой vs продвинутой системы"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Простая система
    simple_metrics = ['Accuracy', 'Sharpe Ratio', 'Max Drawdown', 'Win Rate']
    simple_values = [0.65, 1.2, 0.12, 0.58]
    
    bars1 = ax1.bar(simple_metrics, simple_values, color='lightblue')
    ax1.set_title('Простая ML-система', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Значение')
    ax1.set_ylim(0, max(simple_values) * 1.2)
    
    # Добавление значений на столбцы
    for bar, val in zip(bars1, simple_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{val:.2f}', ha='center', fontweight='bold')
    
    # Продвинутая система
    advanced_metrics = ['Accuracy', 'Sharpe Ratio', 'Max Drawdown', 'Win Rate']
    advanced_values = [0.82, 2.1, 0.058, 0.684]
    
    bars2 = ax2.bar(advanced_metrics, advanced_values, color='lightgreen')
    ax2.set_title('Продвинутая ML-система', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Значение')
    ax2.set_ylim(0, max(advanced_values) * 1.2)
    
    # Добавление значений на столбцы
    for bar, val in zip(bars2, advanced_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{val:.3f}', ha='center', fontweight='bold')
    
    plt.suptitle('Сравнение простой и продвинутой ML-систем', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('docs/automl/gluon/images/optimized/performance_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Основная функция для создания всех визуализаций"""
    
    print("Создание визуализаций для главы 14...")
    
    # Создание директории для изображений
    os.makedirs('docs/automl/gluon/images/optimized', exist_ok=True)
    
    # Создание визуализаций
    print("1. Создание схемы продвинутой архитектуры...")
    create_advanced_architecture_visualization()
    
    print("2. Создание диаграммы системы множественных моделей...")
    create_multi_model_system_visualization()
    
    print("3. Создание визуализации ансамблевой модели...")
    create_ensemble_visualization()
    
    print("4. Создание схемы продвинутого риск-менеджмента...")
    create_risk_management_visualization()
    
    print("5. Создание диаграммы микросервисной архитектуры...")
    create_microservices_architecture()
    
    print("6. Создание схемы Kubernetes деплоя...")
    create_kubernetes_deployment()
    
    print("7. Создание дашборда продвинутого мониторинга...")
    create_advanced_monitoring_dashboard()
    
    print("8. Создание сравнения простой vs продвинутой системы...")
    create_performance_comparison()
    
    print("\n✅ Все визуализации для главы 14 созданы успешно!")
    print("📁 Изображения сохранены в: docs/automl/gluon/images/optimized/")

if __name__ == "__main__":
    main()
