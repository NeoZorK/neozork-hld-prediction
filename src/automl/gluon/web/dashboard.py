"""
Main Web Dashboard for SCHR Levels AutoML

Provides comprehensive web interface for all analysis components.
"""

import os
import webbrowser
import threading
import time
from typing import Dict, Any, Optional
from flask import Flask, render_template, jsonify, request
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json


class SCHRWebDashboard:
    """Main web dashboard for SCHR Levels AutoML"""
    
    def __init__(self, port: int = 8080, host: str = '127.0.0.1', 
                 theme: str = 'dark', auto_refresh: int = 30):
        self.port = port
        self.host = host
        self.theme = theme
        self.auto_refresh = auto_refresh
        self.app = Flask(__name__)
        self.data = {}
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('index.html', theme=self.theme)
        
        @self.app.route('/api/data')
        def get_data():
            return jsonify(self.data)
        
        @self.app.route('/api/backtest')
        def get_backtest():
            return jsonify(self.data.get('backtest', {}))
        
        @self.app.route('/api/forecast')
        def get_forecast():
            return jsonify(self.data.get('forecast', {}))
        
        @self.app.route('/api/walkforward')
        def get_walkforward():
            return jsonify(self.data.get('walkforward', {}))
        
        @self.app.route('/api/montecarlo')
        def get_montecarlo():
            return jsonify(self.data.get('montecarlo', {}))
        
        @self.app.route('/api/accuracy')
        def get_accuracy():
            return jsonify(self.data.get('accuracy', {}))
        
        @self.app.route('/api/probabilities')
        def get_probabilities():
            return jsonify(self.data.get('probabilities', {}))
    
    def show_training_results(self, results: Dict[str, Any]):
        """Show training results in web interface"""
        self.data['training'] = results
        self._launch_dashboard("Training Results")
    
    def show_predictions(self, predictions: Dict[str, Any]):
        """Show predictions in web interface"""
        self.data['forecast'] = predictions
        self._launch_dashboard("Predictions")
    
    def show_backtest_results(self, results: Dict[str, Any]):
        """Show backtest results in web interface"""
        self.data['backtest'] = results
        self._launch_dashboard("Backtest Results")
    
    def show_validation_results(self, results: Dict[str, Any], validation_type: str):
        """Show validation results in web interface"""
        if validation_type == 'walk-forward':
            self.data['walkforward'] = results
            self._launch_dashboard("Walk-Forward Validation")
        elif validation_type == 'monte-carlo':
            self.data['montecarlo'] = results
            self._launch_dashboard("Monte Carlo Validation")
    
    def show_accuracy_stability(self, results: Dict[str, Any]):
        """Show accuracy and stability analysis"""
        self.data['accuracy'] = results
        self._launch_dashboard("Accuracy & Stability Analysis")
    
    def show_probabilities_analysis(self, results: Dict[str, Any]):
        """Show probabilities analysis"""
        self.data['probabilities'] = results
        self._launch_dashboard("Probabilities Analysis")
    
    def _launch_dashboard(self, title: str):
        """Launch dashboard with specific title"""
        # Start Flask app in separate thread
        def run_app():
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        
        thread = threading.Thread(target=run_app)
        thread.daemon = True
        thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Open browser
        url = f"http://{self.host}:{self.port}"
        webbrowser.open(url)
        
        print(f"🌐 {title} dashboard launched at {url}")
        print("Press Ctrl+C to stop the server")
    
    def launch(self):
        """Launch main dashboard"""
        self._launch_dashboard("SCHR Levels AutoML Dashboard")
