#!/usr/bin/env python3
"""
Генерация графиков для примеров продакшена
- Простой пример продакшена
- Сложный пример продакшена

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_simple_production_flow(output_path):
    """Создание графика простого примера продакшена"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Простой пример: От идеи до продакшен деплоя', fontsize=16, fontweight='bold')
    
    # 1. Процесс разработки
    ax1 = axes[0, 0]
    steps = ['Идея', 'Данные', 'Модель', 'Валидация', 'API', 'Docker', 'DEX', 'Мониторинг']
    x_pos = np.arange(len(steps))
    colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
    
    bars = ax1.bar(x_pos, [1]*len(steps), color=colors, alpha=0.8)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(steps, rotation=45, ha='right')
    ax1.set_ylabel('Этап')
    ax1.set_title('Процесс разработки')
    ax1.set_ylim(0, 1.2)
    
    # Добавление стрелок
    for i in range(len(steps)-1):
        ax1.annotate('', xy=(i+0.7, 0.5), xytext=(i+0.3, 0.5),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # 2. Архитектура системы
    ax2 = axes[0, 1]
    components = ['ML Model', 'API', 'Database', 'DEX Contract']
    positions = [(0.2, 0.8), (0.8, 0.8), (0.2, 0.2), (0.8, 0.2)]
    
    for i, (comp, pos) in enumerate(zip(components, positions)):
        circle = plt.Circle(pos, 0.15, color=colors[i], alpha=0.7)
        ax2.add_patch(circle)
        ax2.text(pos[0], pos[1], comp, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Соединения
    connections = [(0, 1), (1, 2), (1, 3)]
    for start, end in connections:
        ax2.plot([positions[start][0], positions[end][0]], 
                [positions[start][1], positions[end][1]], 'k-', alpha=0.5, linewidth=2)
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_title('Архитектура системы')
    ax2.axis('off')
    
    # 3. Метрики производительности
    ax3 = axes[1, 0]
    metrics = ['Accuracy', 'Sharpe Ratio', 'Max DD', 'Win Rate']
    values = [0.723, 1.45, 0.082, 0.684]
    colors_metrics = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    
    bars = ax3.bar(metrics, values, color=colors_metrics, alpha=0.8)
    ax3.set_ylabel('Значение')
    ax3.set_title('Метрики производительности')
    ax3.set_ylim(0, max(values) * 1.2)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Временная линия разработки
    ax4 = axes[1, 1]
    timeline = ['Неделя 1', 'Неделя 2', 'Неделя 3', 'Неделя 4']
    tasks = ['Данные', 'Модель', 'API', 'Деплой']
    progress = [0.25, 0.5, 0.75, 1.0]
    
    for i, (week, task, prog) in enumerate(zip(timeline, tasks, progress)):
        ax4.barh(i, prog, color=colors[i], alpha=0.8)
        ax4.text(prog/2, i, f'{task}\n{prog*100:.0f}%', ha='center', va='center', fontweight='bold')
    
    ax4.set_yticks(range(len(timeline)))
    ax4.set_yticklabels(timeline)
    ax4.set_xlabel('Прогресс')
    ax4.set_title('Временная линия разработки')
    ax4.set_xlim(0, 1)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_advanced_production_flow(output_path):
    """Создание графика сложного примера продакшена"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Сложный пример: Продвинутая ML-система для DEX', fontsize=16, fontweight='bold')
    
    # 1. Микросервисная архитектура
    ax1 = axes[0, 0]
    services = ['API Gateway', 'Data Service', 'Model Service', 'Risk Service', 'Trading Service', 'Monitoring']
    positions = [(0.5, 0.9), (0.1, 0.6), (0.3, 0.6), (0.7, 0.6), (0.9, 0.6), (0.5, 0.3)]
    colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']
    
    for i, (service, pos, color) in enumerate(zip(services, positions, colors)):
        # Создание прямоугольника для сервиса
        rect = plt.Rectangle((pos[0]-0.08, pos[1]-0.05), 0.16, 0.1, 
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax1.add_patch(rect)
        ax1.text(pos[0], pos[1], service, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Соединения между сервисами
    connections = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (2, 3), (3, 4)]
    for start, end in connections:
        ax1.plot([positions[start][0], positions[end][0]], 
                [positions[start][1], positions[end][1]], 'k-', alpha=0.3, linewidth=1)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('Микросервисная архитектура')
    ax1.axis('off')
    
    # 2. Множественные модели
    ax2 = axes[0, 1]
    models = ['Price Direction', 'Volatility', 'Volume', 'Sentiment', 'Macro', 'Ensemble']
    accuracies = [0.75, 0.68, 0.72, 0.65, 0.70, 0.785]
    colors_models = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']
    
    bars = ax2.bar(models, accuracies, color=colors_models, alpha=0.8)
    ax2.set_ylabel('Точность')
    ax2.set_title('Производительность моделей')
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis='x', rotation=45)
    
    # Добавление значений
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{acc:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Продвинутые метрики
    ax3 = axes[1, 0]
    metrics = ['Accuracy', 'Sharpe', 'Max DD', 'VaR 95%', 'Win Rate', 'Return']
    values = [0.785, 2.1, 0.058, 0.023, 0.684, 0.342]
    colors_metrics = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
    
    # Создание радиальной диаграммы
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    values_plot = values + values[:1]  # Замыкаем круг
    angles += angles[:1]
    
    ax3 = plt.subplot(2, 2, 3, projection='polar')
    ax3.plot(angles, values_plot, 'o-', linewidth=2, color='#3498db')
    ax3.fill(angles, values_plot, alpha=0.25, color='#3498db')
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(metrics)
    ax3.set_title('Продвинутые метрики', pad=20)
    
    # 4. Сложность системы
    ax4 = axes[1, 1]
    components = ['Данные', 'Модели', 'API', 'Риск', 'Торговля', 'Мониторинг']
    complexity = [3, 5, 4, 5, 4, 3]  # Уровень сложности 1-5
    colors_comp = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']
    
    bars = ax4.bar(components, complexity, color=colors_comp, alpha=0.8)
    ax4.set_ylabel('Уровень сложности')
    ax4.set_title('Сложность компонентов')
    ax4.set_ylim(0, 6)
    ax4.tick_params(axis='x', rotation=45)
    
    # Добавление значений
    for bar, comp in zip(bars, complexity):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{comp}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_production_comparison(output_path):
    """Создание графика сравнения простого и сложного подходов"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Сравнение простого и сложного подходов к продакшену', fontsize=16, fontweight='bold')
    
    # 1. Время разработки
    ax1 = axes[0, 0]
    approaches = ['Простой', 'Сложный']
    time_weeks = [2, 8]
    colors = ['#2ecc71', '#e74c3c']
    
    bars = ax1.bar(approaches, time_weeks, color=colors, alpha=0.8)
    ax1.set_ylabel('Недели разработки')
    ax1.set_title('Время разработки')
    ax1.set_ylim(0, 10)
    
    for bar, time in zip(bars, time_weeks):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{time} недель', ha='center', va='bottom', fontweight='bold')
    
    # 2. Сложность
    ax2 = axes[0, 1]
    complexity_metrics = ['Компоненты', 'API', 'База данных', 'Мониторинг', 'Деплой']
    simple_complexity = [3, 2, 1, 2, 2]
    advanced_complexity = [8, 5, 3, 4, 5]
    
    x = np.arange(len(complexity_metrics))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, simple_complexity, width, label='Простой', color='#2ecc71', alpha=0.8)
    bars2 = ax2.bar(x + width/2, advanced_complexity, width, label='Сложный', color='#e74c3c', alpha=0.8)
    
    ax2.set_ylabel('Уровень сложности')
    ax2.set_title('Сложность компонентов')
    ax2.set_xticks(x)
    ax2.set_xticklabels(complexity_metrics, rotation=45)
    ax2.legend()
    ax2.set_ylim(0, 6)
    
    # 3. Производительность
    ax3 = axes[1, 0]
    performance_metrics = ['Точность', 'Sharpe', 'Доходность', 'Просадка']
    simple_perf = [0.723, 1.45, 0.237, 0.082]
    advanced_perf = [0.785, 2.1, 0.342, 0.058]
    
    x = np.arange(len(performance_metrics))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, simple_perf, width, label='Простой', color='#2ecc71', alpha=0.8)
    bars2 = ax3.bar(x + width/2, advanced_perf, width, label='Сложный', color='#e74c3c', alpha=0.8)
    
    ax3.set_ylabel('Значение')
    ax3.set_title('Производительность')
    ax3.set_xticks(x)
    ax3.set_xticklabels(performance_metrics)
    ax3.legend()
    
    # 4. Ресурсы
    ax4 = axes[1, 1]
    resource_types = ['CPU', 'RAM', 'Storage', 'Network']
    simple_resources = [2, 4, 10, 1]
    advanced_resources = [8, 16, 50, 5]
    
    x = np.arange(len(resource_types))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, simple_resources, width, label='Простой', color='#2ecc71', alpha=0.8)
    bars2 = ax4.bar(x + width/2, advanced_resources, width, label='Сложный', color='#e74c3c', alpha=0.8)
    
    ax4.set_ylabel('Требования')
    ax4.set_title('Требования к ресурсам')
    ax4.set_xticks(x)
    ax4.set_xticklabels(resource_types)
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("=== Создание графиков для примеров продакшена ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    output_dir = Path(__file__).parent.parent.parent.parent.parent / "docs" / "automl" / "gluon" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    graphics_to_create = [
        (create_simple_production_flow, "simple_production_flow.png"),
        (create_advanced_production_flow, "advanced_production_flow.png"),
        (create_production_comparison, "production_comparison.png"),
    ]
    
    for i, (func, filename) in enumerate(graphics_to_create):
        print(f"Создание графика {i+1}/{len(graphics_to_create)}: {func.__name__}")
        try:
            func(output_dir / filename)
            print(f"✓ График {func.__name__} создан успешно")
        except Exception as e:
            print(f"✗ Ошибка при создании графика {func.__name__}: {e}")
    
    print(f"\n🎉 Все графики для примеров продакшена созданы в директории: {output_dir}")
    print("Графики готовы для использования в учебнике!")

if __name__ == "__main__":
    main()
