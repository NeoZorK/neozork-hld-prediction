#!/usr/bin/env python3
"""
Генерация дополнительных графиков для учебника AutoML Gluon
- Графики метрик
- Графики робастности
- Графики Monte Carlo
- Графики walk-forward

Автор: Shcherbyna Rostyslav
Дата: 2024
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from pathlib import Path
from scipy import stats
from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Настройка стиля
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_metrics_visualization(output_path):
    """Создание графиков для метрик"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Метрики машинного обучения - Визуализация и интерпретация', fontsize=16, fontweight='bold')
    
    # 1. ROC Curve
    ax1 = axes[0, 0]
    np.random.seed(42)
    y_true = np.random.binomial(1, 0.7, 1000)
    y_scores = np.random.beta(2, 1, 1000)
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    ax1.plot(fpr, tpr, 'b-', linewidth=2, label='ROC Curve')
    ax1.plot([0, 1], [0, 1], 'r--', linewidth=2, label='Random Classifier')
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title('ROC Curve\n(Receiver Operating Characteristic)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Precision-Recall Curve
    ax2 = axes[0, 1]
    precision, recall, _ = precision_recall_curve(y_true, y_scores)
    ax2.plot(recall, precision, 'g-', linewidth=2, label='PR Curve')
    ax2.axhline(y=0.5, color='r', linestyle='--', label='Random Classifier')
    ax2.set_xlabel('Recall')
    ax2.set_ylabel('Precision')
    ax2.set_title('Precision-Recall Curve')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Confusion Matrix
    ax3 = axes[0, 2]
    y_pred = (y_scores > 0.5).astype(int)
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax3)
    ax3.set_title('Confusion Matrix')
    ax3.set_xlabel('Predicted')
    ax3.set_ylabel('Actual')
    
    # 4. Accuracy vs Threshold
    ax4 = axes[1, 0]
    thresholds = np.linspace(0, 1, 100)
    accuracies = []
    for thresh in thresholds:
        y_pred_thresh = (y_scores > thresh).astype(int)
        acc = np.mean(y_pred_thresh == y_true)
        accuracies.append(acc)
    ax4.plot(thresholds, accuracies, 'purple', linewidth=2)
    ax4.set_xlabel('Threshold')
    ax4.set_ylabel('Accuracy')
    ax4.set_title('Accuracy vs Threshold')
    ax4.grid(True, alpha=0.3)
    
    # 5. F1 Score vs Threshold
    ax5 = axes[1, 1]
    f1_scores = []
    for thresh in thresholds:
        y_pred_thresh = (y_scores > thresh).astype(int)
        tp = np.sum((y_pred_thresh == 1) & (y_true == 1))
        fp = np.sum((y_pred_thresh == 1) & (y_true == 0))
        fn = np.sum((y_pred_thresh == 0) & (y_true == 1))
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        f1_scores.append(f1)
    ax5.plot(thresholds, f1_scores, 'orange', linewidth=2)
    ax5.set_xlabel('Threshold')
    ax5.set_ylabel('F1 Score')
    ax5.set_title('F1 Score vs Threshold')
    ax5.grid(True, alpha=0.3)
    
    # 6. Metrics Comparison
    ax6 = axes[1, 2]
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    values = [0.85, 0.82, 0.88, 0.85, 0.91]
    bars = ax6.bar(metrics, values, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
    ax6.set_ylabel('Score')
    ax6.set_title('Метрики модели')
    ax6.set_ylim(0, 1)
    for i, v in enumerate(values):
        ax6.text(i, v + 0.01, f'{v:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_robustness_visualization(output_path):
    """Создание графиков для робастности"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Робастность ML-систем - Определение и примеры', fontsize=16, fontweight='bold')
    
    # 1. Robust vs Overfitted Model
    ax1 = axes[0, 0]
    x = np.linspace(0, 10, 100)
    y_true = 2 * x + 3 + np.sin(x) * 0.5
    
    # Robust model
    y_robust = 2 * x + 3 + np.random.normal(0, 0.3, len(x))
    
    # Overfitted model
    y_overfit = 2 * x + 3 + np.sin(x) * 0.5 + np.random.normal(0, 0.1, len(x))
    
    ax1.plot(x, y_true, 'k-', linewidth=2, label='True Function', alpha=0.7)
    ax1.scatter(x[::10], y_robust[::10], color='blue', alpha=0.6, s=30, label='Robust Model')
    ax1.scatter(x[::10], y_overfit[::10], color='red', alpha=0.6, s=30, label='Overfitted Model')
    ax1.set_xlabel('Input Feature')
    ax1.set_ylabel('Target')
    ax1.set_title('Робастная vs Переобученная модель')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Performance Stability
    ax2 = axes[0, 1]
    time_periods = np.arange(1, 21)
    robust_performance = 0.85 + np.random.normal(0, 0.02, 20)
    overfit_performance = 0.95 - np.exp(-time_periods/5) * 0.3 + np.random.normal(0, 0.05, 20)
    
    ax2.plot(time_periods, robust_performance, 'b-', linewidth=2, label='Robust System', marker='o')
    ax2.plot(time_periods, overfit_performance, 'r-', linewidth=2, label='Overfitted System', marker='s')
    ax2.set_xlabel('Time Period')
    ax2.set_ylabel('Performance Score')
    ax2.set_title('Стабильность производительности')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Cross-Validation Scores
    ax3 = axes[1, 0]
    cv_folds = np.arange(1, 11)
    robust_cv = 0.85 + np.random.normal(0, 0.03, 10)
    overfit_cv = 0.95 + np.random.normal(0, 0.01, 10)
    
    ax3.boxplot([robust_cv, overfit_cv], labels=['Robust Model', 'Overfitted Model'])
    ax3.set_ylabel('CV Score')
    ax3.set_title('Cross-Validation стабильность')
    ax3.grid(True, alpha=0.3)
    
    # 4. Feature Importance Stability
    ax4 = axes[1, 1]
    features = ['Feature A', 'Feature B', 'Feature C', 'Feature D', 'Feature E']
    robust_importance = [0.4, 0.3, 0.15, 0.1, 0.05]
    overfit_importance = [0.6, 0.2, 0.1, 0.05, 0.05]
    
    x_pos = np.arange(len(features))
    width = 0.35
    
    ax4.bar(x_pos - width/2, robust_importance, width, label='Robust Model', alpha=0.8)
    ax4.bar(x_pos + width/2, overfit_importance, width, label='Overfitted Model', alpha=0.8)
    ax4.set_xlabel('Features')
    ax4.set_ylabel('Importance')
    ax4.set_title('Стабильность важности признаков')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(features, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_monte_carlo_visualization(output_path):
    """Создание графиков для Monte Carlo"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Monte Carlo анализ - Робастные vs Переобученные системы', fontsize=16, fontweight='bold')
    
    # 1. Profit Distribution
    ax1 = axes[0, 0]
    np.random.seed(42)
    robust_profits = np.random.normal(0.15, 0.05, 1000)  # Стабильная прибыль
    overfit_profits = np.random.normal(0.25, 0.15, 1000)  # Высокая, но нестабильная прибыль
    
    ax1.hist(robust_profits, bins=50, alpha=0.7, label='Robust System', color='blue', density=True)
    ax1.hist(overfit_profits, bins=50, alpha=0.7, label='Overfitted System', color='red', density=True)
    ax1.axvline(np.mean(robust_profits), color='blue', linestyle='--', linewidth=2, label='Robust Mean')
    ax1.axvline(np.mean(overfit_profits), color='red', linestyle='--', linewidth=2, label='Overfit Mean')
    ax1.set_xlabel('Profit Rate')
    ax1.set_ylabel('Density')
    ax1.set_title('Распределение прибыли')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Risk-Return Scatter
    ax2 = axes[0, 1]
    robust_returns = np.random.normal(0.15, 0.05, 1000)
    robust_risks = np.random.normal(0.08, 0.02, 1000)
    
    overfit_returns = np.random.normal(0.25, 0.15, 1000)
    overfit_risks = np.random.normal(0.20, 0.05, 1000)
    
    ax2.scatter(robust_risks, robust_returns, alpha=0.6, label='Robust System', color='blue', s=20)
    ax2.scatter(overfit_risks, overfit_returns, alpha=0.6, label='Overfitted System', color='red', s=20)
    ax2.set_xlabel('Risk (Volatility)')
    ax2.set_ylabel('Return')
    ax2.set_title('Risk-Return профиль')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Cumulative Returns
    ax3 = axes[1, 0]
    time_periods = np.arange(1, 101)
    
    # Robust system - стабильный рост
    robust_cumulative = np.cumsum(np.random.normal(0.001, 0.01, 100))
    
    # Overfitted system - нестабильный рост
    overfit_cumulative = np.cumsum(np.random.normal(0.002, 0.05, 100))
    
    ax3.plot(time_periods, robust_cumulative, 'b-', linewidth=2, label='Robust System')
    ax3.plot(time_periods, overfit_cumulative, 'r-', linewidth=2, label='Overfitted System')
    ax3.set_xlabel('Time Period')
    ax3.set_ylabel('Cumulative Return')
    ax3.set_title('Кумулятивная доходность')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Drawdown Analysis
    ax4 = axes[1, 1]
    robust_drawdowns = np.random.exponential(0.02, 1000)
    overfit_drawdowns = np.random.exponential(0.08, 1000)
    
    ax4.hist(robust_drawdowns, bins=50, alpha=0.7, label='Robust System', color='blue', density=True)
    ax4.hist(overfit_drawdowns, bins=50, alpha=0.7, label='Overfitted System', color='red', density=True)
    ax4.set_xlabel('Drawdown')
    ax4.set_ylabel('Density')
    ax4.set_title('Распределение просадок')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_walk_forward_visualization(output_path):
    """Создание графиков для walk-forward валидации"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Walk-Forward валидация - Правильная реализация и выбор параметров', fontsize=16, fontweight='bold')
    
    # 1. Walk-Forward схема
    ax1 = axes[0, 0]
    total_periods = 24
    train_size = 12
    test_size = 3
    
    # Создаем схему walk-forward
    for i in range(0, total_periods - train_size - test_size + 1, test_size):
        train_start = i
        train_end = i + train_size
        test_start = train_end
        test_end = test_start + test_size
        
        # Training period
        ax1.barh(0, train_size, left=train_start, height=0.3, color='blue', alpha=0.7, label='Training' if i == 0 else "")
        ax1.text(train_start + train_size/2, 0, f'Train {i+1}', ha='center', va='center', fontsize=8)
        
        # Test period
        ax1.barh(0.5, test_size, left=test_start, height=0.3, color='red', alpha=0.7, label='Test' if i == 0 else "")
        ax1.text(test_start + test_size/2, 0.5, f'Test {i+1}', ha='center', va='center', fontsize=8)
    
    ax1.set_xlabel('Time Periods')
    ax1.set_ylabel('')
    ax1.set_title('Walk-Forward схема')
    ax1.set_yticks([0, 0.5])
    ax1.set_yticklabels(['Training', 'Testing'])
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Performance over time
    ax2 = axes[0, 1]
    periods = np.arange(1, 13)
    performance = 0.8 + 0.1 * np.sin(periods * 0.5) + np.random.normal(0, 0.02, 12)
    
    ax2.plot(periods, performance, 'b-o', linewidth=2, markersize=6)
    ax2.axhline(y=0.8, color='r', linestyle='--', alpha=0.7, label='Baseline')
    ax2.fill_between(periods, performance - 0.05, performance + 0.05, alpha=0.3, color='blue')
    ax2.set_xlabel('Walk-Forward Iteration')
    ax2.set_ylabel('Performance Score')
    ax2.set_title('Производительность по итерациям')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Training vs Test Performance
    ax3 = axes[1, 0]
    iterations = np.arange(1, 11)
    train_perf = 0.9 + np.random.normal(0, 0.02, 10)
    test_perf = 0.8 + np.random.normal(0, 0.05, 10)
    
    ax3.plot(iterations, train_perf, 'g-o', linewidth=2, label='Training Performance', markersize=6)
    ax3.plot(iterations, test_perf, 'r-s', linewidth=2, label='Test Performance', markersize=6)
    ax3.set_xlabel('Walk-Forward Iteration')
    ax3.set_ylabel('Performance Score')
    ax3.set_title('Training vs Test Performance')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Parameter Selection
    ax4 = axes[1, 1]
    param_values = np.linspace(0.1, 2.0, 20)
    train_scores = 0.9 - 0.1 * np.exp(-param_values) + np.random.normal(0, 0.01, 20)
    test_scores = 0.8 - 0.2 * np.exp(-param_values) + np.random.normal(0, 0.02, 20)
    
    ax4.plot(param_values, train_scores, 'g-', linewidth=2, label='Training Score')
    ax4.plot(param_values, test_scores, 'r-', linewidth=2, label='Test Score')
    ax4.axvline(x=param_values[np.argmax(test_scores)], color='orange', linestyle='--', 
                label=f'Best Parameter: {param_values[np.argmax(test_scores)]:.2f}')
    ax4.set_xlabel('Parameter Value')
    ax4.set_ylabel('Score')
    ax4.set_title('Выбор оптимальных параметров')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("=== Создание дополнительных графиков для учебника AutoML Gluon ===")
    print("Автор: Shcherbyna Rostyslav")
    print("Дата: 2024")
    
    output_dir = Path(__file__).parent.parent.parent.parent.parent / "docs" / "automl" / "gluon" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    graphics_to_create = [
        (create_metrics_visualization, "metrics_detailed.png"),
        (create_robustness_visualization, "robustness_analysis.png"),
        (create_monte_carlo_visualization, "monte_carlo_analysis.png"),
        (create_walk_forward_visualization, "walk_forward_analysis.png"),
    ]
    
    for i, (func, filename) in enumerate(graphics_to_create):
        print(f"Создание графика {i+1}/{len(graphics_to_create)}: {func.__name__}")
        try:
            func(output_dir / filename)
            print(f"✓ График {func.__name__} создан успешно")
        except Exception as e:
            print(f"✗ Ошибка при создании графика {func.__name__}: {e}")
    
    print(f"\n🎉 Все дополнительные графики созданы в директории: {output_dir}")
    print("Графики готовы для использования в учебнике!")

if __name__ == "__main__":
    main()
