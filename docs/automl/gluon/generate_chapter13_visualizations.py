#!/usr/bin/env python3
"""
Генерация визуализаций для главы 13_simple_production_example.md
Создает наглядные картинки для объяснения процесса создания ML-системы
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Arrow
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_ml_workflow_visualization():
    """Создает визуализацию workflow процесса создания ML-системы"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.suptitle('Workflow: От идеи до продакшен деплоя ML-системы', fontsize=16, fontweight='bold')
    
    # Определение этапов
    stages = [
        ("1. Определение задачи", "Идея\nЦель\nМетрики", (1, 8), "lightblue"),
        ("2. Подготовка данных", "Загрузка\nОчистка\nFeature Engineering", (3, 8), "lightgreen"),
        ("3. Создание модели", "AutoML Gluon\nОбучение\nВалидация", (5, 8), "lightcoral"),
        ("4. Валидация", "Backtest\nWalk-Forward\nMonte Carlo", (7, 8), "lightyellow"),
        ("5. API создание", "Flask API\nЭндпоинты\nДокументация", (9, 8), "lightpink"),
        ("6. Контейнеризация", "Docker\nDocker Compose\nОркестрация", (11, 8), "lightgray"),
        ("7. Blockchain деплой", "Smart Contract\nDEX интеграция\nТорговля", (13, 8), "lightcyan"),
        ("8. Мониторинг", "Метрики\nАлерты\nПереобучение", (15, 8), "lightsteelblue")
    ]
    
    # Рисование этапов
    for i, (title, description, (x, y), color) in enumerate(stages):
        # Основной блок
        rect = FancyBboxPatch((x-0.4, y-0.8), 0.8, 1.6, 
                             boxstyle="round,pad=0.1", 
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Заголовок
        ax.text(x, y+0.3, title, ha='center', va='center', fontweight='bold', fontsize=10)
        
        # Описание
        ax.text(x, y-0.3, description, ha='center', va='center', fontsize=8)
        
        # Номер этапа
        circle = Circle((x, y+0.6), 0.15, facecolor='white', edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y+0.6, str(i+1), ha='center', va='center', fontweight='bold', fontsize=12)
    
    # Стрелки между этапами
    for i in range(len(stages)-1):
        x1 = stages[i][2][0] + 0.4
        x2 = stages[i+1][2][0] - 0.4
        y = stages[i][2][1]
        
        arrow = FancyArrowPatch((x1, y), (x2, y),
                               arrowstyle='->', mutation_scale=20, 
                               color='darkblue', linewidth=2)
        ax.add_patch(arrow)
    
    # Временные рамки
    time_frames = [
        ("1-2 дня", (1, 6.5)),
        ("2-3 дня", (3, 6.5)),
        ("1-2 дня", (5, 6.5)),
        ("2-3 дня", (7, 6.5)),
        ("1 день", (9, 6.5)),
        ("1 день", (11, 6.5)),
        ("1-2 дня", (13, 6.5)),
        ("Постоянно", (15, 6.5))
    ]
    
    for time_frame, (x, y) in time_frames:
        ax.text(x, y, time_frame, ha='center', va='center', 
                fontsize=8, style='italic', color='darkred')
    
    # Настройка осей
    ax.set_xlim(0, 16)
    ax.set_ylim(5, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Заголовок временных рамок
    ax.text(8, 7.2, 'Временные рамки для каждого этапа', ha='center', va='center', 
            fontsize=12, fontweight='bold', color='darkred')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/ml_workflow_process.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_validation_methods_visualization():
    """Создает визуализацию методов валидации"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Методы валидации ML-моделей', fontsize=16, fontweight='bold')
    
    # 1. Backtest
    ax1 = axes[0, 0]
    ax1.set_title('Backtest - Простая валидация', fontweight='bold')
    
    # Создание временного ряда для backtest
    np.random.seed(42)
    n_days = 100
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    # Генерация данных
    price = 100 + np.cumsum(np.random.randn(n_days) * 0.02)
    predictions = np.random.choice([0, 1], n_days, p=[0.3, 0.7])
    actual = np.random.choice([0, 1], n_days, p=[0.4, 0.6])
    
    # График цены
    ax1_twin = ax1.twinx()
    ax1_twin.plot(dates, price, 'b-', linewidth=2, label='Цена')
    ax1_twin.set_ylabel('Цена', color='blue')
    ax1_twin.tick_params(axis='y', labelcolor='blue')
    
    # Точки предсказаний
    correct_predictions = predictions == actual
    correct_dates = dates[correct_predictions]
    incorrect_dates = dates[~correct_predictions]
    
    ax1.scatter(correct_dates, predictions[correct_predictions], 
               color='green', s=50, alpha=0.7, label='Правильные предсказания')
    ax1.scatter(incorrect_dates, predictions[~correct_predictions], 
               color='red', s=50, alpha=0.7, label='Неправильные предсказания')
    
    ax1.set_ylabel('Предсказание (0/1)')
    ax1.set_ylim(-0.5, 1.5)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 2. Walk-Forward валидация
    ax2 = axes[0, 1]
    ax2.set_title('Walk-Forward валидация', fontweight='bold')
    
    # Создание схемы walk-forward
    n_periods = 5
    window_size = 20
    step_size = 10
    
    for i in range(n_periods):
        start_idx = i * step_size
        end_idx = start_idx + window_size
        test_start = end_idx
        test_end = test_start + step_size
        
        # Обучающий период
        ax2.barh(i, window_size, left=start_idx, height=0.6, 
                color='lightblue', alpha=0.7, label='Обучающие данные' if i == 0 else "")
        
        # Тестовый период
        ax2.barh(i, step_size, left=test_start, height=0.6, 
                color='lightcoral', alpha=0.7, label='Тестовые данные' if i == 0 else "")
        
        # Точность
        accuracy = np.random.uniform(0.6, 0.8)
        ax2.text(test_start + step_size/2, i, f'{accuracy:.2f}', 
                ha='center', va='center', fontweight='bold')
    
    ax2.set_xlabel('Время')
    ax2.set_ylabel('Период валидации')
    ax2.set_title('Walk-Forward валидация - Скользящее окно')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Monte Carlo валидация
    ax3 = axes[1, 0]
    ax3.set_title('Monte Carlo валидация', fontweight='bold')
    
    # Генерация результатов Monte Carlo
    n_simulations = 100
    mc_results = np.random.normal(0.7, 0.1, n_simulations)
    mc_results = np.clip(mc_results, 0, 1)
    
    # Гистограмма результатов
    ax3.hist(mc_results, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    ax3.axvline(np.mean(mc_results), color='red', linestyle='--', linewidth=2, 
               label=f'Среднее: {np.mean(mc_results):.3f}')
    ax3.axvline(np.mean(mc_results) + np.std(mc_results), color='orange', linestyle='--', 
               label=f'±1σ: {np.std(mc_results):.3f}')
    ax3.axvline(np.mean(mc_results) - np.std(mc_results), color='orange', linestyle='--')
    
    ax3.set_xlabel('Точность')
    ax3.set_ylabel('Частота')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Сравнение методов
    ax4 = axes[1, 1]
    ax4.set_title('Сравнение методов валидации', fontweight='bold')
    
    methods = ['Backtest', 'Walk-Forward', 'Monte Carlo']
    accuracy_mean = [0.72, 0.68, 0.70]
    accuracy_std = [0.05, 0.08, 0.10]
    time_required = [1, 5, 3]  # часы
    
    x = np.arange(len(methods))
    bars = ax4.bar(x, accuracy_mean, yerr=accuracy_std, capsize=5, 
                   color=['lightblue', 'lightcoral', 'lightgreen'], alpha=0.7)
    
    # Добавление значений
    for i, (mean, std) in enumerate(zip(accuracy_mean, accuracy_std)):
        ax4.text(i, mean + std + 0.01, f'{mean:.2f}±{std:.2f}', 
                ha='center', va='bottom', fontweight='bold')
    
    ax4.set_xlabel('Метод валидации')
    ax4.set_ylabel('Точность')
    ax4.set_xticks(x)
    ax4.set_xticklabels(methods)
    ax4.set_ylim(0, 1)
    ax4.grid(True, alpha=0.3)
    
    # Добавление информации о времени
    ax4_twin = ax4.twinx()
    ax4_twin.plot(x, time_required, 'ro-', linewidth=2, markersize=8, label='Время (часы)')
    ax4_twin.set_ylabel('Время выполнения (часы)', color='red')
    ax4_twin.tick_params(axis='y', labelcolor='red')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/validation_methods_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_production_architecture_visualization():
    """Создает визуализацию архитектуры продакшен системы"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.suptitle('Архитектура продакшен ML-системы', fontsize=16, fontweight='bold')
    
    # Определение компонентов системы
    components = {
        'Data Source': (2, 8, 2, 1, 'lightblue'),
        'ML Model': (2, 6, 2, 1, 'lightgreen'),
        'Flask API': (6, 8, 2, 1, 'lightcoral'),
        'Docker Container': (6, 6, 2, 1, 'lightyellow'),
        'Redis Cache': (6, 4, 2, 1, 'lightpink'),
        'Smart Contract': (10, 8, 2, 1, 'lightgray'),
        'DEX Integration': (10, 6, 2, 1, 'lightcyan'),
        'Monitoring': (10, 4, 2, 1, 'lightsteelblue'),
        'Database': (14, 6, 2, 1, 'lightsalmon'),
        'Logging': (14, 4, 2, 1, 'lightgoldenrodyellow')
    }
    
    # Рисование компонентов
    for name, (x, y, w, h, color) in components.items():
        rect = FancyBboxPatch((x, y), w, h, 
                             boxstyle="round,pad=0.1", 
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', 
                fontweight='bold', fontsize=10)
    
    # Стрелки соединений
    connections = [
        ((3, 8), (6, 8)),  # Data Source -> Flask API
        ((3, 6), (6, 6)),  # ML Model -> Docker Container
        ((7, 8), (7, 6)),  # Flask API -> Docker Container
        ((7, 6), (7, 4)),  # Docker Container -> Redis Cache
        ((8, 8), (10, 8)), # Flask API -> Smart Contract
        ((8, 6), (10, 6)), # Docker Container -> DEX Integration
        ((8, 4), (10, 4)), # Redis Cache -> Monitoring
        ((11, 8), (14, 6)), # Smart Contract -> Database
        ((11, 6), (14, 6)), # DEX Integration -> Database
        ((11, 4), (14, 4)), # Monitoring -> Logging
    ]
    
    for (x1, y1), (x2, y2) in connections:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', mutation_scale=15, 
                               color='darkblue', linewidth=2)
        ax.add_patch(arrow)
    
    # Группировка компонентов
    # Data Layer
    ax.text(3, 9.5, 'Data Layer', ha='center', fontsize=12, fontweight='bold')
    ax.plot([1, 5], [9.2, 9.2], 'k-', linewidth=2)
    
    # Processing Layer
    ax.text(7, 9.5, 'Processing Layer', ha='center', fontsize=12, fontweight='bold')
    ax.plot([5.5, 8.5], [9.2, 9.2], 'k-', linewidth=2)
    
    # Blockchain Layer
    ax.text(11, 9.5, 'Blockchain Layer', ha='center', fontsize=12, fontweight='bold')
    ax.plot([9.5, 12.5], [9.2, 9.2], 'k-', linewidth=2)
    
    # Storage Layer
    ax.text(15, 9.5, 'Storage Layer', ha='center', fontsize=12, fontweight='bold')
    ax.plot([13.5, 16.5], [9.2, 9.2], 'k-', linewidth=2)
    
    # Настройка осей
    ax.set_xlim(0, 18)
    ax.set_ylim(2, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Добавление описания потоков данных
    flow_descriptions = [
        ("Исторические данные", (2.5, 7.5)),
        ("ML предсказания", (2.5, 5.5)),
        ("API запросы", (7, 7.5)),
        ("Контейнеризация", (7, 5.5)),
        ("Кэширование", (7, 3.5)),
        ("Торговые сигналы", (11, 7.5)),
        ("DEX операции", (11, 5.5)),
        ("Метрики", (11, 3.5)),
        ("Сохранение", (15, 5.5)),
        ("Логи", (15, 3.5))
    ]
    
    for desc, (x, y) in flow_descriptions:
        ax.text(x, y, desc, ha='center', va='center', fontsize=8, 
                style='italic', color='darkgreen')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/production_architecture_detailed.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_metrics_visualization():
    """Создает визуализацию метрик производительности"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Метрики производительности ML-системы', fontsize=16, fontweight='bold')
    
    # 1. Точность модели по времени
    ax1 = axes[0, 0]
    ax1.set_title('Точность модели по времени', fontweight='bold')
    
    # Генерация данных точности
    np.random.seed(42)
    n_days = 30
    dates = pd.date_range('2023-01-01', periods=n_days, freq='D')
    
    # Точность с трендом и шумом
    base_accuracy = 0.72
    trend = np.linspace(0, 0.05, n_days)
    noise = np.random.normal(0, 0.02, n_days)
    accuracy = base_accuracy + trend + noise
    accuracy = np.clip(accuracy, 0, 1)
    
    ax1.plot(dates, accuracy, 'b-', linewidth=2, marker='o', markersize=4)
    ax1.axhline(y=0.7, color='red', linestyle='--', linewidth=2, label='Целевая точность')
    ax1.axhline(y=0.6, color='orange', linestyle='--', linewidth=2, label='Минимальная точность')
    
    ax1.set_ylabel('Точность')
    ax1.set_ylim(0.5, 1.0)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Доходность стратегии
    ax2 = axes[0, 1]
    ax2.set_title('Доходность торговой стратегии', fontweight='bold')
    
    # Генерация данных доходности
    returns = np.random.normal(0.001, 0.02, n_days)  # Дневная доходность
    cumulative_returns = np.cumprod(1 + returns) - 1
    
    ax2.plot(dates, cumulative_returns * 100, 'g-', linewidth=2, marker='s', markersize=4)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.axhline(y=20, color='green', linestyle='--', linewidth=2, label='Целевая доходность')
    
    ax2.set_ylabel('Кумулятивная доходность (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Коэффициент Шарпа
    ax3 = axes[1, 0]
    ax3.set_title('Коэффициент Шарпа по времени', fontweight='bold')
    
    # Расчет коэффициента Шарпа
    window = 7
    sharpe_ratios = []
    for i in range(window, len(returns)):
        window_returns = returns[i-window:i]
        sharpe = np.mean(window_returns) / np.std(window_returns) * np.sqrt(252)
        sharpe_ratios.append(sharpe)
    
    sharpe_dates = dates[window:]
    ax3.plot(sharpe_dates, sharpe_ratios, 'purple', linewidth=2, marker='^', markersize=4)
    ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='Хороший Sharpe')
    ax3.axhline(y=2.0, color='green', linestyle='--', linewidth=2, label='Отличный Sharpe')
    
    ax3.set_ylabel('Коэффициент Шарпа')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Распределение ошибок
    ax4 = axes[1, 1]
    ax4.set_title('Распределение ошибок предсказаний', fontweight='bold')
    
    # Генерация ошибок
    prediction_errors = np.random.normal(0, 0.1, 1000)
    prediction_errors = np.clip(prediction_errors, -0.5, 0.5)
    
    ax4.hist(prediction_errors, bins=30, alpha=0.7, color='lightcoral', edgecolor='black')
    ax4.axvline(0, color='red', linestyle='--', linewidth=2, label='Идеальное предсказание')
    ax4.axvline(np.mean(prediction_errors), color='blue', linestyle='-', linewidth=2, 
               label=f'Среднее: {np.mean(prediction_errors):.3f}')
    
    ax4.set_xlabel('Ошибка предсказания')
    ax4.set_ylabel('Частота')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/performance_metrics_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_blockchain_integration_visualization():
    """Создает визуализацию интеграции с blockchain"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.suptitle('Интеграция ML-системы с DEX Blockchain', fontsize=16, fontweight='bold')
    
    # Определение компонентов blockchain системы
    components = {
        'ML API': (2, 8, 2, 1, 'lightblue'),
        'Smart Contract': (6, 8, 2, 1, 'lightgreen'),
        'DEX Protocol': (10, 8, 2, 1, 'lightcoral'),
        'Token A': (6, 6, 1.5, 1, 'lightyellow'),
        'Token B': (8.5, 6, 1.5, 1, 'lightpink'),
        'Liquidity Pool': (10, 6, 2, 1, 'lightgray'),
        'User Wallet': (14, 8, 2, 1, 'lightcyan'),
        'Transaction': (14, 6, 2, 1, 'lightsteelblue')
    }
    
    # Рисование компонентов
    for name, (x, y, w, h, color) in components.items():
        rect = FancyBboxPatch((x, y), w, h, 
                             boxstyle="round,pad=0.1", 
                             facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, name, ha='center', va='center', 
                fontweight='bold', fontsize=9)
    
    # Стрелки потока данных
    flows = [
        ((3, 8), (6, 8), 'Prediction', 'darkblue'),
        ((7, 8), (10, 8), 'Trade Signal', 'darkgreen'),
        ((10, 7), (10, 6), 'Swap Request', 'darkred'),
        ((7.5, 6), (8.5, 6), 'Token Exchange', 'darkorange'),
        ((10, 6), (14, 6), 'Execute Trade', 'purple'),
        ((14, 7), (14, 8), 'Update Balance', 'brown')
    ]
    
    for (x1, y1), (x2, y2), label, color in flows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                               arrowstyle='->', mutation_scale=15, 
                               color=color, linewidth=2)
        ax.add_patch(arrow)
        
        # Подпись стрелки
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.2, label, ha='center', va='bottom', 
                fontsize=8, fontweight='bold', color=color)
    
    # Добавление примера торговой операции
    trade_example = """
    Пример торговой операции:
    1. ML API предсказывает рост цены Token A
    2. Smart Contract получает сигнал
    3. DEX Protocol выполняет swap
    4. Token A -> Token B через Liquidity Pool
    5. User Wallet получает обновленный баланс
    """
    
    ax.text(8, 4, trade_example, ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))
    
    # Настройка осей
    ax.set_xlim(0, 16)
    ax.set_ylim(3, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Заголовки секций
    ax.text(4, 9.5, 'ML Prediction Layer', ha='center', fontsize=12, fontweight='bold')
    ax.text(8, 9.5, 'Smart Contract Layer', ha='center', fontsize=12, fontweight='bold')
    ax.text(12, 9.5, 'DEX Integration Layer', ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/blockchain_integration_flow.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def create_monitoring_dashboard_visualization():
    """Создает визуализацию дашборда мониторинга"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Дашборд мониторинга ML-системы', fontsize=16, fontweight='bold')
    
    # 1. Статус системы
    ax1 = axes[0, 0]
    ax1.set_title('Статус компонентов системы', fontweight='bold')
    
    components = ['ML API', 'Database', 'Redis', 'Blockchain', 'Monitoring']
    status = ['Healthy', 'Healthy', 'Warning', 'Healthy', 'Healthy']
    colors = ['green', 'green', 'orange', 'green', 'green']
    
    y_pos = np.arange(len(components))
    bars = ax1.barh(y_pos, [1, 1, 0.7, 1, 1], color=colors, alpha=0.7)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(components)
    ax1.set_xlabel('Статус')
    ax1.set_xlim(0, 1.2)
    
    # Добавление статусов
    for i, (bar, stat) in enumerate(zip(bars, status)):
        ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, 
                stat, va='center', fontweight='bold')
    
    ax1.grid(True, alpha=0.3)
    
    # 2. Метрики в реальном времени
    ax2 = axes[0, 1]
    ax2.set_title('Метрики в реальном времени', fontweight='bold')
    
    # Генерация данных
    np.random.seed(42)
    n_points = 24  # 24 часа
    hours = np.arange(n_points)
    
    accuracy = 0.72 + np.random.normal(0, 0.02, n_points)
    latency = 50 + np.random.normal(0, 10, n_points)
    throughput = 100 + np.random.normal(0, 20, n_points)
    
    # Нормализация для отображения
    accuracy_norm = accuracy
    latency_norm = latency / 100
    throughput_norm = throughput / 200
    
    ax2.plot(hours, accuracy_norm, 'b-', linewidth=2, label='Точность', marker='o')
    ax2.plot(hours, latency_norm, 'r-', linewidth=2, label='Задержка (×100ms)', marker='s')
    ax2.plot(hours, throughput_norm, 'g-', linewidth=2, label='Пропускная способность (×200)', marker='^')
    
    ax2.set_xlabel('Время (часы)')
    ax2.set_ylabel('Нормализованные значения')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Алерты и уведомления
    ax3 = axes[1, 0]
    ax3.set_title('Алерты и уведомления', fontweight='bold')
    
    alerts = [
        ('High Latency', 'Warning', 'orange'),
        ('Low Accuracy', 'Critical', 'red'),
        ('Memory Usage', 'Info', 'blue'),
        ('API Rate Limit', 'Warning', 'orange')
    ]
    
    y_pos = np.arange(len(alerts))
    colors = [alert[2] for alert in alerts]
    
    bars = ax3.barh(y_pos, [1, 1, 1, 1], color=colors, alpha=0.7)
    
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels([alert[0] for alert in alerts])
    ax3.set_xlabel('Уровень важности')
    
    # Добавление уровней
    for i, (bar, alert) in enumerate(zip(bars, alerts)):
        ax3.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, 
                alert[1], va='center', fontweight='bold')
    
    ax3.grid(True, alpha=0.3)
    
    # 4. Производительность по времени
    ax4 = axes[1, 1]
    ax4.set_title('Производительность за последние 7 дней', fontweight='bold')
    
    # Генерация данных за неделю
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    daily_accuracy = [0.72, 0.75, 0.68, 0.71, 0.73, 0.70, 0.69]
    daily_returns = [0.5, 1.2, -0.8, 0.3, 0.9, 0.1, -0.2]
    
    # Двойная ось
    ax4_twin = ax4.twinx()
    
    bars1 = ax4.bar(days, daily_accuracy, alpha=0.7, color='lightblue', label='Точность')
    line1 = ax4_twin.plot(days, daily_returns, 'ro-', linewidth=2, markersize=6, label='Доходность (%)')
    
    ax4.set_ylabel('Точность', color='blue')
    ax4_twin.set_ylabel('Доходность (%)', color='red')
    ax4.set_ylim(0.6, 0.8)
    ax4_twin.set_ylim(-1, 2)
    
    # Объединение легенд
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized/monitoring_dashboard.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Основная функция для генерации всех визуализаций"""
    print("Генерация визуализаций для главы 13_simple_production_example.md...")
    
    # Создание директории для изображений
    import os
    os.makedirs('/Users/rostsh/Documents/DIS/REPO/neozork-hld-prediction/docs/automl/gluon/images/optimized', exist_ok=True)
    
    # Генерация всех визуализаций
    print("1. Создание workflow процесса...")
    create_ml_workflow_visualization()
    
    print("2. Создание визуализации методов валидации...")
    create_validation_methods_visualization()
    
    print("3. Создание архитектуры продакшен системы...")
    create_production_architecture_visualization()
    
    print("4. Создание метрик производительности...")
    create_performance_metrics_visualization()
    
    print("5. Создание интеграции с blockchain...")
    create_blockchain_integration_visualization()
    
    print("6. Создание дашборда мониторинга...")
    create_monitoring_dashboard_visualization()
    
    print("Все визуализации успешно созданы!")

if __name__ == "__main__":
    main()
