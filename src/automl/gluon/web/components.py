"""
Web Components for SCHR Levels AutoML

Individual visualization components for different analysis types.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional


class BacktestVisualizer:
    """Visualizer for backtesting results"""
    
    def __init__(self):
        self.colors = {
            'profit': '#00ff88',
            'loss': '#ff4444', 
            'neutral': '#888888',
            'equity': '#0066cc',
            'drawdown': '#ff6666'
        }
    
    def create_equity_curve(self, results: Dict[str, Any]) -> go.Figure:
        """Create equity curve visualization"""
        equity_data = results.get('equity_curve', [])
        dates = pd.date_range(start='2020-01-01', periods=len(equity_data), freq='D')
        
        fig = go.Figure()
        
        # Equity curve
        fig.add_trace(go.Scatter(
            x=dates,
            y=equity_data,
            mode='lines',
            name='Portfolio Value',
            line=dict(color=self.colors['equity'], width=2)
        ))
        
        # Drawdown
        drawdown = results.get('drawdown', [])
        fig.add_trace(go.Scatter(
            x=dates,
            y=drawdown,
            mode='lines',
            name='Drawdown',
            line=dict(color=self.colors['drawdown'], width=1),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title='Portfolio Equity Curve & Drawdown',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            template='plotly_dark'
        )
        
        return fig
    
    def create_returns_distribution(self, results: Dict[str, Any]) -> go.Figure:
        """Create returns distribution visualization"""
        returns = results.get('returns', [])
        
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=returns,
            nbinsx=50,
            name='Returns Distribution',
            marker_color=self.colors['neutral']
        ))
        
        # Add mean line
        mean_return = np.mean(returns)
        fig.add_vline(
            x=mean_return,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Mean: {mean_return:.2%}"
        )
        
        fig.update_layout(
            title='Returns Distribution',
            xaxis_title='Returns',
            yaxis_title='Frequency',
            template='plotly_dark'
        )
        
        return fig
    
    def create_metrics_table(self, results: Dict[str, Any]) -> go.Figure:
        """Create metrics summary table"""
        metrics = {
            'Total Return': f"{results.get('total_return', 0):.2%}",
            'Sharpe Ratio': f"{results.get('sharpe_ratio', 0):.2f}",
            'Max Drawdown': f"{results.get('max_drawdown', 0):.2%}",
            'Win Rate': f"{results.get('win_rate', 0):.2%}",
            'Profit Factor': f"{results.get('profit_factor', 0):.2f}",
            'Total Trades': f"{results.get('total_trades', 0)}"
        }
        
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['Metric', 'Value'],
                fill_color='#2E2E2E',
                font=dict(color='white', size=14),
                align='left'
            ),
            cells=dict(
                values=[list(metrics.keys()), list(metrics.values())],
                fill_color='#1E1E1E',
                font=dict(color='white', size=12),
                align='left'
            )
        )])
        
        fig.update_layout(
            title='Backtest Metrics Summary',
            template='plotly_dark'
        )
        
        return fig


class ForecastVisualizer:
    """Visualizer for prediction forecasts"""
    
    def __init__(self):
        self.colors = {
            'actual': '#00ff88',
            'predicted': '#ff4444',
            'confidence': '#0066cc'
        }
    
    def create_forecast_chart(self, data: Dict[str, Any]) -> go.Figure:
        """Create forecast visualization"""
        fig = go.Figure()
        
        # Historical data
        historical = data.get('historical', [])
        dates = pd.date_range(start='2020-01-01', periods=len(historical), freq='D')
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=historical,
            mode='lines',
            name='Historical',
            line=dict(color=self.colors['actual'], width=2)
        ))
        
        # Predictions
        predictions = data.get('predictions', [])
        pred_dates = pd.date_range(start=dates[-1], periods=len(predictions)+1, freq='D')[1:]
        
        fig.add_trace(go.Scatter(
            x=pred_dates,
            y=predictions,
            mode='lines+markers',
            name='Forecast',
            line=dict(color=self.colors['predicted'], width=2)
        ))
        
        # Confidence intervals
        if 'confidence_lower' in data and 'confidence_upper' in data:
            fig.add_trace(go.Scatter(
                x=pred_dates,
                y=data['confidence_upper'],
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=pred_dates,
                y=data['confidence_lower'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor=f'rgba(0, 102, 204, 0.2)',
                name='Confidence Interval',
                hoverinfo='skip'
            ))
        
        fig.update_layout(
            title='Price Forecast with Confidence Intervals',
            xaxis_title='Date',
            yaxis_title='Price',
            hovermode='x unified',
            template='plotly_dark'
        )
        
        return fig
    
    def create_probability_heatmap(self, probabilities: Dict[str, Any]) -> go.Figure:
        """Create probability heatmap"""
        tasks = list(probabilities.keys())
        prob_matrix = np.array([list(probs.values()) for probs in probabilities.values()])
        
        fig = go.Figure(data=go.Heatmap(
            z=prob_matrix,
            x=['Down', 'Hold', 'Up'],
            y=tasks,
            colorscale='RdYlBu_r',
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='Prediction Probabilities Heatmap',
            xaxis_title='Prediction Class',
            yaxis_title='Task',
            template='plotly_dark'
        )
        
        return fig


class WalkForwardVisualizer:
    """Visualizer for walk-forward validation"""
    
    def create_validation_chart(self, results: Dict[str, Any]) -> go.Figure:
        """Create walk-forward validation chart"""
        fig = go.Figure()
        
        for task, data in results.items():
            accuracies = data.get('accuracies', [])
            fold_names = [f'Fold {i+1}' for i in range(len(accuracies))]
            
            fig.add_trace(go.Scatter(
                x=fold_names,
                y=accuracies,
                mode='lines+markers',
                name=f'{task}',
                line=dict(width=2)
            ))
        
        # Add mean line
        all_accuracies = []
        for data in results.values():
            all_accuracies.extend(data.get('accuracies', []))
        
        if all_accuracies:
            mean_acc = np.mean(all_accuracies)
            fig.add_hline(
                y=mean_acc,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Mean: {mean_acc:.2%}"
            )
        
        fig.update_layout(
            title='Walk-Forward Validation Results',
            xaxis_title='Fold',
            yaxis_title='Accuracy',
            hovermode='x unified',
            template='plotly_dark'
        )
        
        return fig


class MonteCarloVisualizer:
    """Visualizer for Monte Carlo validation"""
    
    def create_distribution_chart(self, results: Dict[str, Any]) -> go.Figure:
        """Create Monte Carlo distribution chart"""
        fig = go.Figure()
        
        for task, data in results.items():
            accuracies = data.get('accuracies', [])
            
            fig.add_trace(go.Histogram(
                x=accuracies,
                name=f'{task}',
                opacity=0.7,
                nbinsx=20
            ))
        
        fig.update_layout(
            title='Monte Carlo Validation Distribution',
            xaxis_title='Accuracy',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_dark'
        )
        
        return fig
    
    def create_stability_chart(self, results: Dict[str, Any]) -> go.Figure:
        """Create stability analysis chart"""
        tasks = list(results.keys())
        means = [results[task]['mean_accuracy'] for task in tasks]
        stds = [results[task]['std_accuracy'] for task in tasks]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=tasks,
            y=means,
            error_y=dict(type='data', array=stds),
            name='Mean Accuracy ± Std',
            marker_color='#0066cc'
        ))
        
        fig.update_layout(
            title='Model Stability Analysis',
            xaxis_title='Task',
            yaxis_title='Accuracy',
            template='plotly_dark'
        )
        
        return fig


class AccuracyStabilityVisualizer:
    """Visualizer for accuracy and stability analysis"""
    
    def create_accuracy_comparison(self, results: Dict[str, Any]) -> go.Figure:
        """Create accuracy comparison chart"""
        tasks = list(results.keys())
        accuracies = [results[task]['accuracy'] for task in tasks]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=tasks,
            y=accuracies,
            name='Accuracy',
            marker_color='#00ff88'
        ))
        
        fig.update_layout(
            title='Model Accuracy Comparison',
            xaxis_title='Task',
            yaxis_title='Accuracy',
            template='plotly_dark'
        )
        
        return fig
    
    def create_stability_radar(self, results: Dict[str, Any]) -> go.Figure:
        """Create stability radar chart"""
        tasks = list(results.keys())
        
        # Calculate stability metrics
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'stability']
        
        fig = go.Figure()
        
        for task in tasks:
            values = []
            for metric in metrics:
                if metric == 'stability':
                    values.append(results[task].get('stability', 0))
                else:
                    values.append(results[task].get(metric, 0))
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metrics,
                fill='toself',
                name=task
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Model Stability Radar Chart",
            template='plotly_dark'
        )
        
        return fig


class ProbabilitiesVisualizer:
    """Visualizer for probability analysis"""
    
    def create_probability_distribution(self, probabilities: Dict[str, Any]) -> go.Figure:
        """Create probability distribution chart"""
        fig = go.Figure()
        
        for task, probs in probabilities.items():
            prob_values = list(probs.values())
            
            fig.add_trace(go.Histogram(
                x=prob_values,
                name=task,
                opacity=0.7,
                nbinsx=20
            ))
        
        fig.update_layout(
            title='Probability Distribution by Task',
            xaxis_title='Probability',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_dark'
        )
        
        return fig
    
    def create_confidence_analysis(self, probabilities: Dict[str, Any]) -> go.Figure:
        """Create confidence analysis chart"""
        tasks = list(probabilities.keys())
        max_probs = [max(list(probs.values())) for probs in probabilities.values()]
        mean_probs = [np.mean(list(probs.values())) for probs in probabilities.values()]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=tasks,
            y=max_probs,
            name='Max Probability',
            marker_color='#ff4444'
        ))
        
        fig.add_trace(go.Bar(
            x=tasks,
            y=mean_probs,
            name='Mean Probability',
            marker_color='#00ff88'
        ))
        
        fig.update_layout(
            title='Prediction Confidence Analysis',
            xaxis_title='Task',
            yaxis_title='Probability',
            barmode='group',
            template='plotly_dark'
        )
        
        return fig
