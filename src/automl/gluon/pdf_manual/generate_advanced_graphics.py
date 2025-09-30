#!/usr/bin/env python3
"""
Генерация графиков для продвинутых разделов учебника
- Теория и основы
- Интерпретируемость
- Продвинутые темы
- Этика и ответственный AI
- Кейс-стади

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

def create_automl_theory_diagram(output_path):
    """Создание диаграммы теории AutoML"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Теоретические основы AutoML', fontsize=16, fontweight='bold')
    
    # 1. Neural Architecture Search
    ax1 = axes[0, 0]
    nas_components = ['Search Space', 'Search Strategy', 'Performance Estimation', 'Architecture']
    nas_flow = ['Data', 'Search Space', 'Search Strategy', 'Architecture', 'Performance', 'Optimization']
    
    # Создание блок-схемы NAS
    positions = [(0.1, 0.8), (0.3, 0.8), (0.5, 0.8), (0.7, 0.8), (0.9, 0.8), (0.5, 0.6)]
    colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']
    
    for i, (comp, pos, color) in enumerate(zip(nas_flow, positions, colors)):
        rect = plt.Rectangle((pos[0]-0.08, pos[1]-0.05), 0.16, 0.1, 
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax1.add_patch(rect)
        ax1.text(pos[0], pos[1], comp, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Соединения
    for i in range(len(positions)-1):
        ax1.plot([positions[i][0], positions[i+1][0]], 
                [positions[i][1], positions[i+1][1]], 'k-', alpha=0.5, linewidth=2)
    
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_title('Neural Architecture Search (NAS)')
    ax1.axis('off')
    
    # 2. Hyperparameter Optimization
    ax2 = axes[0, 1]
    methods = ['Grid Search', 'Random Search', 'Bayesian Optimization', 'Evolutionary']
    efficiency = [0.3, 0.6, 0.9, 0.7]
    colors_hp = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax2.bar(methods, efficiency, color=colors_hp, alpha=0.8)
    ax2.set_ylabel('Эффективность')
    ax2.set_title('Методы оптимизации гиперпараметров')
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, eff in zip(bars, efficiency):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{eff:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Ensemble Methods
    ax3 = axes[1, 0]
    ensemble_types = ['Bagging', 'Boosting', 'Stacking', 'Voting']
    accuracy = [0.85, 0.88, 0.91, 0.87]
    colors_ens = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax3.bar(ensemble_types, accuracy, color=colors_ens, alpha=0.8)
    ax3.set_ylabel('Точность')
    ax3.set_title('Методы ансамблирования')
    ax3.set_ylim(0, 1)
    
    for bar, acc in zip(bars, accuracy):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{acc:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Meta-Learning
    ax4 = axes[1, 1]
    meta_components = ['Meta-Features', 'Algorithm Selection', 'Hyperparameter Transfer', 'Few-Shot Learning']
    importance = [0.8, 0.9, 0.7, 0.85]
    colors_meta = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax4.bar(meta_components, importance, color=colors_meta, alpha=0.8)
    ax4.set_ylabel('Важность')
    ax4.set_title('Компоненты мета-обучения')
    ax4.set_ylim(0, 1)
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, imp in zip(bars, importance):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{imp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_interpretability_overview(output_path):
    """Создание обзора интерпретируемости"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Интерпретируемость и объяснимость ML-моделей', fontsize=16, fontweight='bold')
    
    # 1. Типы интерпретируемости
    ax1 = axes[0, 0]
    interpretability_types = ['Intrinsic', 'Post-hoc', 'Global', 'Local']
    complexity = [0.2, 0.6, 0.4, 0.8]
    colors_int = ['#2ecc71', '#f39c12', '#3498db', '#e74c3c']
    
    bars = ax1.bar(interpretability_types, complexity, color=colors_int, alpha=0.8)
    ax1.set_ylabel('Сложность реализации')
    ax1.set_title('Типы интерпретируемости')
    ax1.set_ylim(0, 1)
    
    for bar, comp in zip(bars, complexity):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{comp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Методы объяснения
    ax2 = axes[0, 1]
    methods = ['SHAP', 'LIME', 'PDP', 'ICE', 'Feature Importance']
    popularity = [0.9, 0.8, 0.7, 0.5, 0.6]
    colors_methods = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax2.bar(methods, popularity, color=colors_methods, alpha=0.8)
    ax2.set_ylabel('Популярность')
    ax2.set_title('Методы объяснения')
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, pop in zip(bars, popularity):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{pop:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Применение по отраслям
    ax3 = axes[1, 0]
    industries = ['Finance', 'Healthcare', 'E-commerce', 'Manufacturing', 'Transport']
    interpretability_need = [0.95, 0.9, 0.7, 0.8, 0.75]
    colors_ind = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax3.bar(industries, interpretability_need, color=colors_ind, alpha=0.8)
    ax3.set_ylabel('Потребность в интерпретируемости')
    ax3.set_title('Применение по отраслям')
    ax3.set_ylim(0, 1)
    ax3.tick_params(axis='x', rotation=45)
    
    for bar, need in zip(bars, interpretability_need):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{need:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Метрики качества объяснений
    ax4 = axes[1, 1]
    metrics = ['Fidelity', 'Consistency', 'Stability', 'Completeness']
    importance = [0.9, 0.8, 0.7, 0.6]
    colors_metrics = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax4.bar(metrics, importance, color=colors_metrics, alpha=0.8)
    ax4.set_ylabel('Важность')
    ax4.set_title('Метрики качества объяснений')
    ax4.set_ylim(0, 1)
    
    for bar, imp in zip(bars, importance):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{imp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_advanced_topics_overview(output_path):
    """Создание обзора продвинутых тем"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Продвинутые темы AutoML', fontsize=16, fontweight='bold')
    
    # 1. Neural Architecture Search
    ax1 = axes[0, 0]
    nas_methods = ['DARTS', 'ENAS', 'Progressive NAS', 'Efficient NAS']
    performance = [0.85, 0.88, 0.82, 0.90]
    efficiency = [0.7, 0.9, 0.8, 0.95]
    
    x = np.arange(len(nas_methods))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, performance, width, label='Performance', color='#2ecc71', alpha=0.8)
    bars2 = ax1.bar(x + width/2, efficiency, width, label='Efficiency', color='#3498db', alpha=0.8)
    
    ax1.set_ylabel('Score')
    ax1.set_title('Neural Architecture Search Methods')
    ax1.set_xticks(x)
    ax1.set_xticklabels(nas_methods)
    ax1.legend()
    ax1.set_ylim(0, 1)
    
    # 2. Meta-Learning
    ax2 = axes[0, 1]
    meta_methods = ['MAML', 'Prototypical', 'Matching Networks', 'Relation Networks']
    few_shot_performance = [0.75, 0.80, 0.78, 0.82]
    colors_meta = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax2.bar(meta_methods, few_shot_performance, color=colors_meta, alpha=0.8)
    ax2.set_ylabel('Few-Shot Performance')
    ax2.set_title('Meta-Learning Methods')
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, perf in zip(bars, few_shot_performance):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{perf:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Multi-Modal Learning
    ax3 = axes[1, 0]
    modalities = ['Vision', 'Language', 'Audio', 'Multimodal']
    accuracy = [0.85, 0.80, 0.75, 0.92]
    colors_mod = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax3.bar(modalities, accuracy, color=colors_mod, alpha=0.8)
    ax3.set_ylabel('Accuracy')
    ax3.set_title('Multi-Modal Learning Performance')
    ax3.set_ylim(0, 1)
    
    for bar, acc in zip(bars, accuracy):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{acc:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Federated Learning
    ax4 = axes[1, 1]
    fl_components = ['Privacy', 'Communication', 'Aggregation', 'Personalization']
    importance = [0.95, 0.7, 0.8, 0.6]
    colors_fl = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax4.bar(fl_components, importance, color=colors_fl, alpha=0.8)
    ax4.set_ylabel('Importance')
    ax4.set_title('Federated Learning Components')
    ax4.set_ylim(0, 1)
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, imp in zip(bars, importance):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{imp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_ai_ethics_overview(output_path):
    """Создание обзора этики AI"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Этика и ответственный AI', fontsize=16, fontweight='bold')
    
    # 1. Принципы этичного AI
    ax1 = axes[0, 0]
    principles = ['Fairness', 'Transparency', 'Privacy', 'Accountability', 'Safety']
    importance = [0.95, 0.90, 0.85, 0.88, 0.92]
    colors_principles = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax1.bar(principles, importance, color=colors_principles, alpha=0.8)
    ax1.set_ylabel('Важность')
    ax1.set_title('Принципы этичного AI')
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='x', rotation=45)
    
    for bar, imp in zip(bars, importance):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{imp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Правовые требования
    ax2 = axes[0, 1]
    regulations = ['GDPR', 'AI Act', 'CCPA', 'PIPEDA', 'LGPD']
    compliance_level = [0.9, 0.8, 0.7, 0.6, 0.5]
    colors_reg = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax2.bar(regulations, compliance_level, color=colors_reg, alpha=0.8)
    ax2.set_ylabel('Уровень соответствия')
    ax2.set_title('Правовые требования')
    ax2.set_ylim(0, 1)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, level in zip(bars, compliance_level):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{level:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Методы обнаружения смещений
    ax3 = axes[1, 0]
    bias_methods = ['Statistical Parity', 'Equalized Odds', 'Demographic Parity', 'Calibration']
    effectiveness = [0.8, 0.85, 0.75, 0.70]
    colors_bias = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax3.bar(bias_methods, effectiveness, color=colors_bias, alpha=0.8)
    ax3.set_ylabel('Эффективность')
    ax3.set_title('Методы обнаружения смещений')
    ax3.set_ylim(0, 1)
    ax3.tick_params(axis='x', rotation=45)
    
    for bar, eff in zip(bars, effectiveness):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{eff:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Отрасли по уровню риска
    ax4 = axes[1, 1]
    industries = ['Healthcare', 'Finance', 'Transport', 'Education', 'Entertainment']
    risk_level = [0.9, 0.8, 0.7, 0.6, 0.3]
    colors_risk = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax4.bar(industries, risk_level, color=colors_risk, alpha=0.8)
    ax4.set_ylabel('Уровень риска')
    ax4.set_title('Отрасли по уровню риска')
    ax4.set_ylim(0, 1)
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, risk in zip(bars, risk_level):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{risk:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_case_studies_overview(output_path):
    """Создание обзора кейс-стади"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Кейс-стади: Реальные проекты с AutoML Gluon', fontsize=16, fontweight='bold')
    
    # 1. Отрасли применения
    ax1 = axes[0, 0]
    industries = ['Finance', 'Healthcare', 'E-commerce', 'Manufacturing', 'Transport']
    adoption_rate = [0.85, 0.75, 0.90, 0.70, 0.65]
    colors_ind = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6']
    
    bars = ax1.bar(industries, adoption_rate, color=colors_ind, alpha=0.8)
    ax1.set_ylabel('Уровень внедрения')
    ax1.set_title('Применение по отраслям')
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='x', rotation=45)
    
    for bar, rate in zip(bars, adoption_rate):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{rate:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Метрики производительности
    ax2 = axes[0, 1]
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    finance_scores = [0.87, 0.85, 0.89, 0.87, 0.92]
    healthcare_scores = [0.91, 0.88, 0.90, 0.89, 0.94]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    bars1 = ax2.bar(x - width/2, finance_scores, width, label='Finance', color='#e74c3c', alpha=0.8)
    bars2 = ax2.bar(x + width/2, healthcare_scores, width, label='Healthcare', color='#2ecc71', alpha=0.8)
    
    ax2.set_ylabel('Score')
    ax2.set_title('Метрики производительности')
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics)
    ax2.legend()
    ax2.set_ylim(0, 1)
    
    # 3. Бизнес-эффект
    ax3 = axes[1, 0]
    effects = ['Cost Reduction', 'Revenue Increase', 'Efficiency Gain', 'Risk Reduction']
    impact = [0.32, 0.25, 0.45, 0.38]
    colors_eff = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax3.bar(effects, impact, color=colors_eff, alpha=0.8)
    ax3.set_ylabel('Влияние (%)')
    ax3.set_title('Бизнес-эффект')
    ax3.set_ylim(0, 0.5)
    ax3.tick_params(axis='x', rotation=45)
    
    for bar, imp in zip(bars, impact):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{imp:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. Сложность проектов
    ax4 = axes[1, 1]
    projects = ['Credit Scoring', 'Medical Diagnosis', 'Recommendations', 'Predictive Maintenance']
    complexity = [0.6, 0.8, 0.7, 0.9]
    colors_proj = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    bars = ax4.bar(projects, complexity, color=colors_proj, alpha=0.8)
    ax4.set_ylabel('Сложность')
    ax4.set_title('Сложность проектов')
    ax4.set_ylim(0, 1)
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, comp in zip(bars, complexity):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{comp:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("=== Создание графиков для продвинутых разделов учебника ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    output_dir = Path(__file__).parent.parent.parent.parent.parent / "docs" / "automl" / "gluon" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    graphics_to_create = [
        (create_automl_theory_diagram, "automl_theory.png"),
        (create_interpretability_overview, "interpretability_overview.png"),
        (create_advanced_topics_overview, "advanced_topics_overview.png"),
        (create_ai_ethics_overview, "ai_ethics_overview.png"),
        (create_case_studies_overview, "case_studies_overview.png"),
    ]
    
    for i, (func, filename) in enumerate(graphics_to_create):
        print(f"Создание графика {i+1}/{len(graphics_to_create)}: {func.__name__}")
        try:
            func(output_dir / filename)
            print(f"✓ График {func.__name__} создан успешно")
        except Exception as e:
            print(f"✗ Ошибка при создании графика {func.__name__}: {e}")
    
    print(f"\n🎉 Все графики для продвинутых разделов созданы в директории: {output_dir}")
    print("Графики готовы для использования в учебнике!")

if __name__ == "__main__":
    main()
