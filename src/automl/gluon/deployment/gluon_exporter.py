# -*- coding: utf-8 -*-
"""
AutoGluon model exporter.

This module provides model export capabilities for deployment.
"""

import os
import shutil
import pickle
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
import logging
import warnings

# AutoGluon imports
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    AUTOGLUON_AVAILABLE = False
    TabularPredictor = None

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class GluonExporter:
    """AutoGluon model exporter."""
    
    def __init__(self):
        """Initialize Gluon exporter."""
        if not AUTOGLUON_AVAILABLE:
            raise ImportError("AutoGluon is not available")
    
    def export(self, predictor: TabularPredictor, export_path: str, 
               formats: List[str] = None) -> Dict[str, str]:
        """
        Export trained models in specified formats.
        
        Args:
            predictor: Trained TabularPredictor
            export_path: Export directory path
            formats: Export formats (pickle, onnx, etc.)
            
        Returns:
            Dictionary of export paths
        """
        if formats is None:
            formats = ['pickle']
        
        export_path = Path(export_path)
        export_path.mkdir(parents=True, exist_ok=True)
        
        export_paths = {}
        
        for format_type in formats:
            try:
                if format_type == 'pickle':
                    path = self._export_pickle(predictor, export_path)
                elif format_type == 'onnx':
                    path = self._export_onnx(predictor, export_path)
                elif format_type == 'json':
                    path = self._export_json(predictor, export_path)
                else:
                    logger.warning(f"Unsupported export format: {format_type}")
                    continue
                
                export_paths[format_type] = str(path)
                logger.info(f"Exported model in {format_type} format to {path}")
                
            except Exception as e:
                logger.error(f"Failed to export in {format_type} format: {e}")
        
        return export_paths
    
    def _export_pickle(self, predictor: TabularPredictor, export_path: Path) -> Path:
        """Export model as pickle file."""
        pickle_path = export_path / "model.pkl"
        
        with open(pickle_path, 'wb') as f:
            pickle.dump(predictor, f)
        
        return pickle_path
    
    def _export_onnx(self, predictor: TabularPredictor, export_path: Path) -> Path:
        """Export model in ONNX format."""
        onnx_path = export_path / "model.onnx"
        
        try:
            # Try to export to ONNX (if supported)
            predictor.export_to_onnx(str(onnx_path))
        except Exception as e:
            logger.warning(f"ONNX export not supported: {e}")
            # Fallback to pickle
            return self._export_pickle(predictor, export_path)
        
        return onnx_path
    
    def _export_json(self, predictor: TabularPredictor, export_path: Path) -> Path:
        """Export model metadata as JSON."""
        json_path = export_path / "model_info.json"
        
        # Get model information
        model_info = {
            'model_type': 'TabularPredictor',
            'problem_type': predictor.problem_type,
            'eval_metric': predictor.eval_metric,
            'feature_importance': predictor.feature_importance().to_dict(),
            'leaderboard': predictor.leaderboard().to_dict()
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, default=str)
        
        return json_path
    
    def export_for_walk_forward(self, predictor: TabularPredictor, 
                               export_path: str) -> Dict[str, str]:
        """
        Export model for walk forward analysis.
        
        Args:
            predictor: Trained TabularPredictor
            export_path: Export directory path
            
        Returns:
            Export paths dictionary
        """
        export_path = Path(export_path) / "walk_forward"
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Export model
        model_paths = self.export(predictor, str(export_path), ['pickle', 'json'])
        
        # Create walk forward specific files
        wf_config = {
            'model_type': 'autogluon',
            'export_timestamp': str(pd.Timestamp.now()),
            'model_path': model_paths.get('pickle', ''),
            'metadata_path': model_paths.get('json', ''),
            'compatible_with': ['walk_forward', 'monte_carlo']
        }
        
        config_path = export_path / "walk_forward_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(wf_config, f, indent=2)
        
        model_paths['config'] = str(config_path)
        
        logger.info("Model exported for walk forward analysis")
        return model_paths
    
    def export_for_monte_carlo(self, predictor: TabularPredictor, 
                             export_path: str) -> Dict[str, str]:
        """
        Export model for Monte Carlo analysis.
        
        Args:
            predictor: Trained TabularPredictor
            export_path: Export directory path
            
        Returns:
            Export paths dictionary
        """
        export_path = Path(export_path) / "monte_carlo"
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Export model
        model_paths = self.export(predictor, str(export_path), ['pickle', 'json'])
        
        # Create Monte Carlo specific files
        mc_config = {
            'model_type': 'autogluon',
            'export_timestamp': str(pd.Timestamp.now()),
            'model_path': model_paths.get('pickle', ''),
            'metadata_path': model_paths.get('json', ''),
            'compatible_with': ['monte_carlo', 'walk_forward'],
            'supports_probability': True
        }
        
        config_path = export_path / "monte_carlo_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(mc_config, f, indent=2)
        
        model_paths['config'] = str(config_path)
        
        logger.info("Model exported for Monte Carlo analysis")
        return model_paths
    
    def create_deployment_package(self, predictor: TabularPredictor, 
                                export_path: str) -> Dict[str, str]:
        """
        Create complete deployment package.
        
        Args:
            predictor: Trained TabularPredictor
            export_path: Export directory path
            
        Returns:
            Deployment package paths
        """
        export_path = Path(export_path) / "deployment"
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Export models
        model_paths = self.export(predictor, str(export_path), ['pickle', 'json'])
        
        # Create deployment configuration
        deployment_config = {
            'model_type': 'autogluon',
            'version': '1.0.0',
            'export_timestamp': str(pd.Timestamp.now()),
            'model_path': model_paths.get('pickle', ''),
            'metadata_path': model_paths.get('json', ''),
            'requirements': [
                'autogluon.tabular',
                'pandas',
                'numpy',
                'scikit-learn'
            ],
            'supported_formats': ['pickle', 'json'],
            'compatible_with': ['walk_forward', 'monte_carlo', 'production']
        }
        
        config_path = export_path / "deployment_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(deployment_config, f, indent=2)
        
        # Create requirements.txt
        requirements_path = export_path / "requirements.txt"
        with open(requirements_path, 'w') as f:
            for req in deployment_config['requirements']:
                f.write(f"{req}\n")
        
        # Create README
        readme_path = export_path / "README.md"
        readme_content = self._create_deployment_readme(predictor)
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        model_paths.update({
            'config': str(config_path),
            'requirements': str(requirements_path),
            'readme': str(readme_path)
        })
        
        logger.info("Deployment package created successfully")
        return model_paths
    
    def _create_deployment_readme(self, predictor: TabularPredictor) -> str:
        """Create deployment README."""
        return f"""# AutoGluon Model Deployment Package

## Model Information
- Model Type: TabularPredictor
- Problem Type: {predictor.problem_type}
- Evaluation Metric: {predictor.eval_metric}

## Files
- `model.pkl`: Trained model (pickle format)
- `model_info.json`: Model metadata
- `deployment_config.json`: Deployment configuration
- `requirements.txt`: Python dependencies

## Usage
```python
import pickle
import pandas as pd

# Load model
with open('model.pkl', 'rb') as f:
    predictor = pickle.load(f)

# Make predictions
predictions = predictor.predict(new_data)
```

## Compatibility
- Walk Forward Analysis: ✅
- Monte Carlo Simulation: ✅
- Production Deployment: ✅

## Requirements
- Python 3.7+
- AutoGluon
- Pandas
- NumPy
- Scikit-learn
"""
