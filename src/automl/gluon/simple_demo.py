#!/usr/bin/env python3
"""
SCHR Levels AutoML - Simple Demo

Demonstrates CLI capabilities and web visualizations without Flask dependency.
"""

import os
import sys
import webbrowser
import time
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))


def show_cli_help():
    """Show CLI help and capabilities"""
    print("🚀 SCHR Levels AutoML - CLI Demo")
    print("=" * 50)
    
    print("""
SCHR Levels AutoML - Flexible Financial Analysis Tool

Usage: schr_gluon_cli.py [OPTIONS] COMMAND [ARGS]...

Commands:
  train      Train ML models
  predict    Make predictions  
  backtest   Run backtesting
  validate   Run validation
  web        Launch web dashboard

Global Options:
  --verbose, -v              Enable verbose logging
  --quiet, -q                Suppress output except errors
  --config, -c PATH          Path to configuration file
  --output-dir, -o PATH      Output directory for results
  --log-level LEVEL          Logging level (DEBUG, INFO, WARNING, ERROR)
  
Data Options:
  --data-path PATH           Path to data directory
  --symbol SYMBOL            Trading symbol (BTCUSD, ETHUSD, EURUSD, etc.)
  --timeframe TIMEFRAME      Timeframe (MN1, W1, D1, H4, H1, M15, M5, M1)
  
Model Options:
  --tasks TASK [TASK ...]    ML tasks to run
  --time-limit SECONDS       Training time limit in seconds
  --presets PRESET           AutoGluon presets
  --exclude-models MODEL     Models to exclude
  
Validation Options:
  --test-size FLOAT          Test set size (0.0-1.0)
  --cv-folds INT             Cross-validation folds
  --random-state INT         Random state for reproducibility
  
Web Options:
  --web                      Enable web visualization
  --browser                  Open browser automatically
  --port INT                 Web server port
  --host HOST                Web server host
  --theme THEME              Dashboard theme (dark, light)
  
Backtest Options:
  --start-date DATE          Backtest start date (YYYY-MM-DD)
  --end-date DATE            Backtest end date (YYYY-MM-DD)
  --initial-capital FLOAT    Initial capital for backtesting
  --commission FLOAT         Trading commission rate
  
Performance Options:
  --n-jobs INT               Number of parallel jobs (-1 for all cores)
  --memory-limit STRING      Memory limit for training
  --gpu                      Enable GPU acceleration
    """)
    
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


def create_html_dashboard(title: str, content: str, port: int) -> str:
    """Create HTML dashboard"""
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #1a1a1a;
            color: #ffffff;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .content {{
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .chart-container {{
            background: #2a2a2a;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        
        .chart-title {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #00ff88;
            font-weight: 500;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: #2a2a2a;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #00ff88;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            color: #cccccc;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 {title}</h1>
        <p>SCHR Levels AutoML - Advanced Financial Analysis Platform</p>
    </div>
    
    <div class="content">
        {content}
    </div>
    
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
    """
    
    # Save HTML file
    filename = f"dashboard_{port}.html"
    with open(filename, 'w') as f:
        f.write(html_content)
    
    return os.path.abspath(filename)


def demo_backtest_visualization():
    """Demo backtest visualization in browser"""
    print("📈 Launching Backtest Visualization...")
    
    # Create sample backtest data
    backtest_data = {
        'equity_curve': [10000, 10200, 10150, 10300, 10200, 10400, 10350, 10500, 10450, 10600],
        'drawdown': [0, 0, 0.05, 0, 0.03, 0, 0.02, 0, 0.01, 0],
        'returns': [0, 0.02, -0.005, 0.015, -0.01, 0.02, -0.005, 0.015, -0.005, 0.015],
        'metrics': {
            'total_return': 0.06,
            'sharpe_ratio': 1.25,
            'max_drawdown': 0.05,
            'win_rate': 0.75,
            'profit_factor': 2.5,
            'total_trades': 4
        }
    }
    
    # Create HTML content
    content = f"""
    <div class="chart-title">📊 Portfolio Performance</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">6.0%</div>
            <div class="metric-label">Total Return</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">1.25</div>
            <div class="metric-label">Sharpe Ratio</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">5.0%</div>
            <div class="metric-label">Max Drawdown</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">75%</div>
            <div class="metric-label">Win Rate</div>
        </div>
    </div>
    
    <div class="chart-title">📈 Equity Curve</div>
    <div id="equity-chart" style="height: 400px;"></div>
    
    <div class="chart-title">📊 Returns Distribution</div>
    <div id="returns-chart" style="height: 400px;"></div>
    
    <script>
        // Equity curve
        const equityData = {json.dumps(backtest_data['equity_curve'])};
        const dates = Array.from({{length: equityData.length}}, (_, i) => new Date(Date.now() - (equityData.length - i) * 24 * 60 * 60 * 1000));
        
        Plotly.newPlot('equity-chart', [{{
            x: dates,
            y: equityData,
            type: 'scatter',
            mode: 'lines',
            name: 'Portfolio Value',
            line: {{ color: '#00ff88', width: 2 }}
        }}], {{
            title: 'Portfolio Equity Curve',
            xaxis: {{ title: 'Date' }},
            yaxis: {{ title: 'Value' }},
            template: 'plotly_dark'
        }});
        
        // Returns distribution
        const returnsData = {json.dumps(backtest_data['returns'])};
        Plotly.newPlot('returns-chart', [{{
            x: returnsData,
            type: 'histogram',
            name: 'Returns Distribution',
            marker: {{ color: '#667eea' }}
        }}], {{
            title: 'Returns Distribution',
            xaxis: {{ title: 'Returns' }},
            yaxis: {{ title: 'Frequency' }},
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Backtest Analysis", content, 8081)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Backtest dashboard opened in browser")
    print("   - Portfolio equity curve")
    print("   - Returns distribution")
    print("   - Performance metrics")
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
    
    # Create HTML content
    content = f"""
    <div class="chart-title">🔮 Model Predictions</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">3</div>
            <div class="metric-label">Active Models</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">85%</div>
            <div class="metric-label">Avg Confidence</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">10</div>
            <div class="metric-label">Predictions</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">Real-time</div>
            <div class="metric-label">Update Mode</div>
        </div>
    </div>
    
    <div class="chart-title">📈 Prediction Timeline</div>
    <div id="forecast-chart" style="height: 400px;"></div>
    
    <div class="chart-title">🎯 Probability Heatmap</div>
    <div id="probability-heatmap" style="height: 400px;"></div>
    
    <script>
        // Forecast chart
        const tasks = {json.dumps(list(forecast_data.keys()))};
        const traces = [];
        
        tasks.forEach((task, index) => {{
            const predictions = forecast_data[task].predictions;
            traces.push({{
                x: Array.from({{length: predictions.length}}, (_, i) => i),
                y: predictions,
                type: 'scatter',
                mode: 'lines+markers',
                name: task,
                line: {{ color: index === 0 ? '#00ff88' : index === 1 ? '#ff4444' : '#667eea' }}
            }});
        }});
        
        Plotly.newPlot('forecast-chart', traces, {{
            title: 'Model Predictions Over Time',
            xaxis: {{ title: 'Time' }},
            yaxis: {{ title: 'Prediction' }},
            template: 'plotly_dark'
        }});
        
        // Probability heatmap
        const probMatrix = tasks.map(task => {{
            const probs = forecast_data[task].probabilities;
            return Object.values(probs).map(arr => arr[0]); // First prediction
        }});
        
        Plotly.newPlot('probability-heatmap', [{{
            z: probMatrix,
            x: ['Down', 'Hold', 'Up'],
            y: tasks,
            type: 'heatmap',
            colorscale: 'RdYlBu_r'
        }}], {{
            title: 'Prediction Probabilities Heatmap',
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Forecast Predictions", content, 8082)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Forecast dashboard opened in browser")
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
    
    # Create HTML content
    content = f"""
    <div class="chart-title">🔄 Walk-Forward Validation Results</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">69%</div>
            <div class="metric-label">Avg Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">5</div>
            <div class="metric-label">Folds</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">±2.5%</div>
            <div class="metric-label">Std Deviation</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">Stable</div>
            <div class="metric-label">Status</div>
        </div>
    </div>
    
    <div class="chart-title">📊 Fold-by-Fold Accuracy</div>
    <div id="walkforward-chart" style="height: 400px;"></div>
    
    <div class="chart-title">📈 Model Stability Analysis</div>
    <div id="stability-chart" style="height: 400px;"></div>
    
    <script>
        // Walk-forward chart
        const tasks = {json.dumps(list(walkforward_data.keys()))};
        const traces = [];
        
        tasks.forEach((task, index) => {{
            const accuracies = walkforward_data[task].accuracies;
            const foldNames = accuracies.map((_, i) => `Fold ${{i+1}}`);
            
            traces.push({{
                x: foldNames,
                y: accuracies,
                type: 'scatter',
                mode: 'lines+markers',
                name: task,
                line: {{ color: index === 0 ? '#00ff88' : index === 1 ? '#ff4444' : '#667eea' }}
            }});
        }});
        
        Plotly.newPlot('walkforward-chart', traces, {{
            title: 'Walk-Forward Validation Results',
            xaxis: {{ title: 'Fold' }},
            yaxis: {{ title: 'Accuracy' }},
            template: 'plotly_dark'
        }});
        
        // Stability chart
        const meanAccuracies = tasks.map(task => walkforward_data[task].mean_accuracy);
        const stdAccuracies = tasks.map(task => walkforward_data[task].std_accuracy);
        
        Plotly.newPlot('stability-chart', [{{
            x: tasks,
            y: meanAccuracies,
            error_y: {{ type: 'data', array: stdAccuracies }},
            type: 'bar',
            name: 'Mean Accuracy ± Std',
            marker: {{ color: '#0066cc' }}
        }}], {{
            title: 'Model Stability Analysis',
            xaxis: {{ title: 'Task' }},
            yaxis: {{ title: 'Accuracy' }},
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Walk-Forward Validation", content, 8083)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Walk-Forward dashboard opened in browser")
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
    
    # Create HTML content
    content = f"""
    <div class="chart-title">🎲 Monte Carlo Validation Analysis</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">20</div>
            <div class="metric-label">Iterations</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">57%</div>
            <div class="metric-label">Avg Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">±1.8%</div>
            <div class="metric-label">Std Deviation</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">Robust</div>
            <div class="metric-label">Status</div>
        </div>
    </div>
    
    <div class="chart-title">📊 Accuracy Distribution</div>
    <div id="montecarlo-chart" style="height: 400px;"></div>
    
    <div class="chart-title">📈 Model Stability Comparison</div>
    <div id="stability-comparison" style="height: 400px;"></div>
    
    <script>
        // Monte Carlo chart
        const tasks = {json.dumps(list(montecarlo_data.keys()))};
        const traces = [];
        
        tasks.forEach((task, index) => {{
            const accuracies = montecarlo_data[task].accuracies;
            
            traces.push({{
                x: accuracies,
                type: 'histogram',
                name: task,
                opacity: 0.7,
                marker: {{ color: index === 0 ? '#00ff88' : index === 1 ? '#ff4444' : '#667eea' }}
            }});
        }});
        
        Plotly.newPlot('montecarlo-chart', traces, {{
            title: 'Monte Carlo Validation Distribution',
            xaxis: {{ title: 'Accuracy' }},
            yaxis: {{ title: 'Frequency' }},
            barmode: 'overlay',
            template: 'plotly_dark'
        }});
        
        // Stability comparison
        const meanAccuracies = tasks.map(task => montecarlo_data[task].mean_accuracy);
        const stdAccuracies = tasks.map(task => montecarlo_data[task].std_accuracy);
        
        Plotly.newPlot('stability-comparison', [{{
            x: tasks,
            y: meanAccuracies,
            error_y: {{ type: 'data', array: stdAccuracies }},
            type: 'bar',
            name: 'Mean Accuracy ± Std',
            marker: {{ color: '#0066cc' }}
        }}], {{
            title: 'Model Stability Comparison',
            xaxis: {{ title: 'Task' }},
            yaxis: {{ title: 'Accuracy' }},
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Monte Carlo Validation", content, 8084)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Monte Carlo dashboard opened in browser")
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
    
    # Create HTML content
    content = f"""
    <div class="chart-title">🎯 Model Performance Analysis</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">57%</div>
            <div class="metric-label">Avg Accuracy</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">82%</div>
            <div class="metric-label">Avg Stability</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">3</div>
            <div class="metric-label">Models</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">Good</div>
            <div class="metric-label">Overall</div>
        </div>
    </div>
    
    <div class="chart-title">📊 Model Accuracy Comparison</div>
    <div id="accuracy-chart" style="height: 400px;"></div>
    
    <div class="chart-title">📈 Stability Radar Chart</div>
    <div id="stability-radar" style="height: 400px;"></div>
    
    <script>
        // Accuracy comparison
        const tasks = {json.dumps(list(accuracy_data.keys()))};
        const accuracies = tasks.map(task => accuracy_data[task].accuracy);
        
        Plotly.newPlot('accuracy-chart', [{{
            x: tasks,
            y: accuracies,
            type: 'bar',
            name: 'Accuracy',
            marker: {{ color: '#00ff88' }}
        }}], {{
            title: 'Model Accuracy Comparison',
            xaxis: {{ title: 'Task' }},
            yaxis: {{ title: 'Accuracy' }},
            template: 'plotly_dark'
        }});
        
        // Stability radar chart
        const radarData = tasks.map(task => ({{
            r: [
                accuracy_data[task].accuracy,
                accuracy_data[task].precision,
                accuracy_data[task].recall,
                accuracy_data[task].f1_score,
                accuracy_data[task].stability
            ],
            theta: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Stability'],
            fill: 'toself',
            name: task
        }}));
        
        Plotly.newPlot('stability-radar', radarData, {{
            polar: {{
                radialaxis: {{
                    visible: true,
                    range: [0, 1]
                }}
            }},
            title: 'Model Stability Radar Chart',
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Accuracy & Stability Analysis", content, 8085)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Accuracy & Stability dashboard opened in browser")
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
    
    # Create HTML content
    content = f"""
    <div class="chart-title">📊 Probability Analysis Dashboard</div>
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-value">85%</div>
            <div class="metric-label">Avg Confidence</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">3</div>
            <div class="metric-label">Models</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">30</div>
            <div class="metric-label">Predictions</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">High</div>
            <div class="metric-label">Signal Quality</div>
        </div>
    </div>
    
    <div class="chart-title">📈 Probability Distribution</div>
    <div id="probability-distribution" style="height: 400px;"></div>
    
    <div class="chart-title">🎯 Confidence Analysis</div>
    <div id="confidence-analysis" style="height: 400px;"></div>
    
    <script>
        // Probability distribution
        const tasks = {json.dumps(list(probabilities_data.keys()))};
        const traces = [];
        
        tasks.forEach((task, index) => {{
            const probs = probabilities_data[task].probabilities;
            const allProbs = Object.values(probs).flat();
            
            traces.push({{
                x: allProbs,
                type: 'histogram',
                name: task,
                opacity: 0.7,
                marker: {{ color: index === 0 ? '#00ff88' : index === 1 ? '#ff4444' : '#667eea' }}
            }});
        }});
        
        Plotly.newPlot('probability-distribution', traces, {{
            title: 'Probability Distribution by Task',
            xaxis: {{ title: 'Probability' }},
            yaxis: {{ title: 'Frequency' }},
            barmode: 'overlay',
            template: 'plotly_dark'
        }});
        
        // Confidence analysis
        const maxProbs = tasks.map(task => {{
            const probs = probabilities_data[task].probabilities;
            return Math.max(...Object.values(probs).flat());
        }});
        const meanProbs = tasks.map(task => {{
            const probs = probabilities_data[task].probabilities;
            const allProbs = Object.values(probs).flat();
            return allProbs.reduce((a, b) => a + b, 0) / allProbs.length;
        }});
        
        Plotly.newPlot('confidence-analysis', [{{
            x: tasks,
            y: maxProbs,
            type: 'bar',
            name: 'Max Probability',
            marker: {{ color: '#ff4444' }}
        }}, {{
            x: tasks,
            y: meanProbs,
            type: 'bar',
            name: 'Mean Probability',
            marker: {{ color: '#00ff88' }}
        }}], {{
            title: 'Prediction Confidence Analysis',
            xaxis: {{ title: 'Task' }},
            yaxis: {{ title: 'Probability' }},
            barmode: 'group',
            template: 'plotly_dark'
        }});
    </script>
    """
    
    # Create and open HTML file
    html_file = create_html_dashboard("Probabilities Analysis", content, 8086)
    webbrowser.open(f"file://{html_file}")
    
    print("🌐 Probabilities dashboard opened in browser")
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
    show_cli_help()
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
    print("📋 Dashboard Files Created:")
    print("   - Backtest: dashboard_8081.html")
    print("   - Forecast: dashboard_8082.html")
    print("   - Walk-Forward: dashboard_8083.html")
    print("   - Monte Carlo: dashboard_8084.html")
    print("   - Accuracy: dashboard_8085.html")
    print("   - Probabilities: dashboard_8086.html")
    print()
    print("💡 All HTML files are saved locally and can be opened anytime")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
