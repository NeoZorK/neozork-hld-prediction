#!/usr/bin/env python3
"""
SCHR Levels AutoML - Demo Script

Demonstrates all web visualizations and CLI capabilities.
"""

import os
import sys
import webbrowser
import time
import threading
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from automl.gluon.cli.main import SCHRCLI
from automl.gluon.web.dashboard import SCHRWebDashboard
from automl.gluon.analysis.pipeline import SCHRLevelsAutoMLPipeline


def demo_cli_help():
    """Show CLI help and capabilities"""
    print("🚀 SCHR Levels AutoML - CLI Demo")
    print("=" * 50)
    
    cli = SCHRCLI()
    cli.parser.print_help()
    
    print("\n📋 Example Commands:")
    print("  # Train all models with web visualization")
    print("  python schr_gluon_cli.py train --symbol BTCUSD --timeframe MN1 --web --browser")
    print()
    print("  # Quick prediction")
    print("  python schr_gluon_cli.py predict --symbol BTCUSD --timeframe MN1 --web")
    print()
    print("  # Comprehensive backtest")
    print("  python schr_gluon_cli.py backtest --symbol BTCUSD --timeframe MN1 --web --browser")
    print()
    print("  # Walk-forward validation")
    print("  python schr_gluon_cli.py validate --type walk-forward --symbol BTCUSD --web")
    print()
    print("  # Monte Carlo validation")
    print("  python schr_gluon_cli.py validate --type monte-carlo --symbol BTCUSD --web")
    print()
    print("  # Launch web dashboard")
    print("  python schr_gluon_cli.py web --port 8080 --browser")


def demo_backtest_visualization():
    """Demo backtest visualization in browser"""
    print("📈 Launching Backtest Visualization...")
    
    # Create sample backtest data
    backtest_data = {
        'equity_curve': [10000, 10200, 10150, 10300, 10200, 10400, 10350, 10500, 10450, 10600],
        'drawdown': [0, 0, 0.05, 0, 0.03, 0, 0.02, 0, 0.01, 0],
        'returns': [0, 0.02, -0.005, 0.015, -0.01, 0.02, -0.005, 0.015, -0.005, 0.015],
        'trades': [
            {'date': '2024-01-01', 'type': 'open_long', 'price': 50000, 'pnl': 0},
            {'date': '2024-01-02', 'type': 'close_long', 'price': 51000, 'pnl': 1000},
            {'date': '2024-01-03', 'type': 'open_short', 'price': 51000, 'pnl': 0},
            {'date': '2024-01-04', 'type': 'close_short', 'price': 50000, 'pnl': 1000}
        ],
        'metrics': {
            'total_return': 0.06,
            'sharpe_ratio': 1.25,
            'max_drawdown': 0.05,
            'win_rate': 0.75,
            'profit_factor': 2.5,
            'total_trades': 4
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8081, host='127.0.0.1')
    dashboard.show_backtest_results(backtest_data)
    
    print("🌐 Backtest dashboard opened in browser at http://127.0.0.1:8081")
    print("   - Portfolio equity curve")
    print("   - Returns distribution")
    print("   - Performance metrics table")
    print("   - Trading statistics")


def demo_forecast_visualization():
    """Demo forecast visualization in browser"""
    print("🔮 Launching Forecast Visualization...")
    
    # Create sample forecast data
    forecast_data = {
        'pressure_vector_sign': {
            'predictions': [1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
            'probabilities': {
                'negative': [0.3, 0.2, 0.7, 0.4, 0.6, 0.3, 0.2, 0.8, 0.3, 0.2],
                'positive': [0.7, 0.8, 0.3, 0.6, 0.4, 0.7, 0.8, 0.2, 0.7, 0.8]
            }
        },
        'price_direction_1period': {
            'predictions': [2, 0, 1, 2, 0, 2, 1, 0, 2, 1],
            'probabilities': {
                'down': [0.2, 0.6, 0.3, 0.1, 0.7, 0.2, 0.4, 0.8, 0.1, 0.3],
                'hold': [0.1, 0.2, 0.4, 0.1, 0.1, 0.1, 0.5, 0.1, 0.1, 0.4],
                'up': [0.7, 0.2, 0.3, 0.8, 0.2, 0.7, 0.1, 0.1, 0.8, 0.3]
            }
        },
        'level_breakout': {
            'predictions': [1, 2, 0, 1, 2, 1, 0, 2, 1, 0],
            'probabilities': {
                'below_low': [0.1, 0.1, 0.6, 0.2, 0.1, 0.2, 0.7, 0.1, 0.2, 0.8],
                'between': [0.7, 0.2, 0.2, 0.6, 0.2, 0.6, 0.2, 0.2, 0.6, 0.1],
                'above_high': [0.2, 0.7, 0.2, 0.2, 0.7, 0.2, 0.1, 0.7, 0.2, 0.1]
            }
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8082, host='127.0.0.1')
    dashboard.show_predictions(forecast_data)
    
    print("🌐 Forecast dashboard opened in browser at http://127.0.0.1:8082")
    print("   - Price forecast with confidence intervals")
    print("   - Probability heatmap")
    print("   - Model predictions comparison")
    print("   - Trading signals visualization")


def demo_walkforward_visualization():
    """Demo walk-forward validation visualization in browser"""
    print("🔄 Launching Walk-Forward Validation Visualization...")
    
    # Create sample walk-forward data
    walkforward_data = {
        'pressure_vector_sign': {
            'accuracies': [0.65, 0.68, 0.72, 0.69, 0.71],
            'mean_accuracy': 0.69,
            'std_accuracy': 0.025
        },
        'price_direction_1period': {
            'accuracies': [0.42, 0.45, 0.38, 0.44, 0.41],
            'mean_accuracy': 0.42,
            'std_accuracy': 0.025
        },
        'level_breakout': {
            'accuracies': [0.58, 0.62, 0.59, 0.61, 0.60],
            'mean_accuracy': 0.60,
            'std_accuracy': 0.015
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8083, host='127.0.0.1')
    dashboard.show_validation_results(walkforward_data, 'walk-forward')
    
    print("🌐 Walk-Forward dashboard opened in browser at http://127.0.0.1:8083")
    print("   - Fold-by-fold accuracy progression")
    print("   - Model stability analysis")
    print("   - Performance consistency metrics")
    print("   - Validation recommendations")


def demo_montecarlo_visualization():
    """Demo Monte Carlo validation visualization in browser"""
    print("🎲 Launching Monte Carlo Validation Visualization...")
    
    # Create sample Monte Carlo data
    montecarlo_data = {
        'pressure_vector_sign': {
            'accuracies': [0.65, 0.68, 0.72, 0.69, 0.71, 0.66, 0.70, 0.67, 0.69, 0.68,
                          0.72, 0.66, 0.68, 0.71, 0.69, 0.67, 0.70, 0.68, 0.72, 0.69],
            'mean_accuracy': 0.69,
            'std_accuracy': 0.018
        },
        'price_direction_1period': {
            'accuracies': [0.42, 0.45, 0.38, 0.44, 0.41, 0.43, 0.40, 0.46, 0.39, 0.42,
                          0.44, 0.41, 0.38, 0.43, 0.40, 0.45, 0.39, 0.42, 0.44, 0.41],
            'mean_accuracy': 0.42,
            'std_accuracy': 0.022
        },
        'level_breakout': {
            'accuracies': [0.58, 0.62, 0.59, 0.61, 0.60, 0.59, 0.61, 0.58, 0.62, 0.60,
                          0.61, 0.59, 0.58, 0.62, 0.60, 0.59, 0.61, 0.58, 0.62, 0.60],
            'mean_accuracy': 0.60,
            'std_accuracy': 0.013
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8084, host='127.0.0.1')
    dashboard.show_validation_results(montecarlo_data, 'monte-carlo')
    
    print("🌐 Monte Carlo dashboard opened in browser at http://127.0.0.1:8084")
    print("   - Accuracy distribution histograms")
    print("   - Model stability analysis")
    print("   - Confidence intervals")
    print("   - Robustness assessment")


def demo_accuracy_stability_visualization():
    """Demo accuracy and stability visualization in browser"""
    print("🎯 Launching Accuracy & Stability Visualization...")
    
    # Create sample accuracy data
    accuracy_data = {
        'pressure_vector_sign': {
            'accuracy': 0.69,
            'precision': 0.72,
            'recall': 0.69,
            'f1_score': 0.70,
            'stability': 0.85
        },
        'price_direction_1period': {
            'accuracy': 0.42,
            'precision': 0.45,
            'recall': 0.42,
            'f1_score': 0.43,
            'stability': 0.78
        },
        'level_breakout': {
            'accuracy': 0.60,
            'precision': 0.62,
            'recall': 0.60,
            'f1_score': 0.61,
            'stability': 0.82
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8085, host='127.0.0.1')
    dashboard.show_accuracy_stability(accuracy_data)
    
    print("🌐 Accuracy & Stability dashboard opened in browser at http://127.0.0.1:8085")
    print("   - Model accuracy comparison")
    print("   - Stability radar chart")
    print("   - Performance recommendations")
    print("   - Model selection guidance")


def demo_probabilities_visualization():
    """Demo probabilities visualization in browser"""
    print("📊 Launching Probabilities Visualization...")
    
    # Create sample probabilities data
    probabilities_data = {
        'pressure_vector_sign': {
            'probabilities': {
                'negative': [0.3, 0.2, 0.7, 0.4, 0.6, 0.3, 0.2, 0.8, 0.3, 0.2],
                'positive': [0.7, 0.8, 0.3, 0.6, 0.4, 0.7, 0.8, 0.2, 0.7, 0.8]
            }
        },
        'price_direction_1period': {
            'probabilities': {
                'down': [0.2, 0.6, 0.3, 0.1, 0.7, 0.2, 0.4, 0.8, 0.1, 0.3],
                'hold': [0.1, 0.2, 0.4, 0.1, 0.1, 0.1, 0.5, 0.1, 0.1, 0.4],
                'up': [0.7, 0.2, 0.3, 0.8, 0.2, 0.7, 0.1, 0.1, 0.8, 0.3]
            }
        },
        'level_breakout': {
            'probabilities': {
                'below_low': [0.1, 0.1, 0.6, 0.2, 0.1, 0.2, 0.7, 0.1, 0.2, 0.8],
                'between': [0.7, 0.2, 0.2, 0.6, 0.2, 0.6, 0.2, 0.2, 0.6, 0.1],
                'above_high': [0.2, 0.7, 0.2, 0.2, 0.7, 0.2, 0.1, 0.7, 0.2, 0.1]
            }
        }
    }
    
    # Launch dashboard
    dashboard = SCHRWebDashboard(port=8086, host='127.0.0.1')
    dashboard.show_probabilities_analysis(probabilities_data)
    
    print("🌐 Probabilities dashboard opened in browser at http://127.0.0.1:8086")
    print("   - Probability distribution analysis")
    print("   - Confidence level assessment")
    print("   - Trading signal strength")
    print("   - Risk management insights")


def main():
    """Main demo function"""
    print("🚀 SCHR Levels AutoML - Complete Demo")
    print("=" * 60)
    print()
    
    # Show CLI help
    demo_cli_help()
    print("\n" + "=" * 60)
    
    # Launch all visualizations
    print("🌐 Launching all web visualizations...")
    print("   Each visualization will open in a new browser window")
    print()
    
    # Launch each demo with delay
    demos = [
        ("Backtest Analysis", demo_backtest_visualization),
        ("Forecast Predictions", demo_forecast_visualization),
        ("Walk-Forward Validation", demo_walkforward_visualization),
        ("Monte Carlo Analysis", demo_montecarlo_visualization),
        ("Accuracy & Stability", demo_accuracy_stability_visualization),
        ("Probabilities Analysis", demo_probabilities_visualization)
    ]
    
    for name, demo_func in demos:
        print(f"📊 {name}...")
        demo_func()
        time.sleep(2)  # Small delay between launches
        print()
    
    print("🎉 All visualizations launched!")
    print("   Check your browser for the interactive dashboards")
    print("   Each dashboard shows different aspects of the analysis")
    print()
    print("📋 Dashboard URLs:")
    print("   - Backtest: http://127.0.0.1:8081")
    print("   - Forecast: http://127.0.0.1:8082")
    print("   - Walk-Forward: http://127.0.0.1:8083")
    print("   - Monte Carlo: http://127.0.0.1:8084")
    print("   - Accuracy: http://127.0.0.1:8085")
    print("   - Probabilities: http://127.0.0.1:8086")
    print()
    print("💡 Use Ctrl+C to stop all servers when done")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
