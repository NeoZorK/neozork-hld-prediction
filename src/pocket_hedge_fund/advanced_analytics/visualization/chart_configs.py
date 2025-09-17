"""
Chart Configurations for advanced analytics visualization.

This module provides chart configuration functionality for analytics visualizations.
"""

from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ChartConfigs:
    """Chart configurations for analytics visualization."""
    
    def __init__(self):
        """Initialize chart configurations."""
        self.configs: Dict[str, Dict[str, Any]] = {}
        self.default_configs: Dict[str, Dict[str, Any]] = {
            'line': {
                'type': 'line',
                'options': {
                    'responsive': True,
                    'interaction': {
                        'intersect': False,
                        'mode': 'index'
                    },
                    'scales': {
                        'x': {
                            'display': True,
                            'title': {
                                'display': True,
                                'text': 'Time'
                            }
                        },
                        'y': {
                            'display': True,
                            'title': {
                                'display': True,
                                'text': 'Value'
                            }
                        }
                    }
                }
            },
            'bar': {
                'type': 'bar',
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'position': 'top'
                        }
                    },
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            },
            'scatter': {
                'type': 'scatter',
                'options': {
                    'responsive': True,
                    'scales': {
                        'x': {
                            'type': 'linear',
                            'position': 'bottom'
                        }
                    }
                }
            },
            'heatmap': {
                'type': 'heatmap',
                'options': {
                    'responsive': True,
                    'plugins': {
                        'legend': {
                            'display': True
                        }
                    }
                }
            }
        }
        self.logger = logger
    
    def get_config(self, chart_type: str) -> Dict[str, Any]:
        """Get configuration for a specific chart type."""
        try:
            if chart_type in self.configs:
                return self.configs[chart_type].copy()
            elif chart_type in self.default_configs:
                return self.default_configs[chart_type].copy()
            else:
                self.logger.warning(f"No configuration found for chart type: {chart_type}")
                return {}
        except Exception as e:
            self.logger.error(f"Error getting config for {chart_type}: {e}")
            return {}
    
    def set_config(self, chart_type: str, config: Dict[str, Any]) -> bool:
        """Set configuration for a specific chart type."""
        try:
            self.configs[chart_type] = config.copy()
            self.logger.info(f"Configuration set for chart type: {chart_type}")
            return True
        except Exception as e:
            self.logger.error(f"Error setting config for {chart_type}: {e}")
            return False
    
    def update_config(self, chart_type: str, updates: Dict[str, Any]) -> bool:
        """Update configuration for a specific chart type."""
        try:
            if chart_type not in self.configs:
                self.configs[chart_type] = self.get_config(chart_type)
            
            # Deep update
            self._deep_update(self.configs[chart_type], updates)
            self.logger.info(f"Configuration updated for chart type: {chart_type}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating config for {chart_type}: {e}")
            return False
    
    def _deep_update(self, base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
        """Deep update a dictionary."""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """Get all configurations."""
        all_configs = {}
        all_configs.update(self.default_configs)
        all_configs.update(self.configs)
        return all_configs
    
    def list_chart_types(self) -> List[str]:
        """List all available chart types."""
        chart_types = set(self.default_configs.keys())
        chart_types.update(self.configs.keys())
        return list(chart_types)
    
    def export_config(self, chart_type: str, filepath: str) -> bool:
        """Export configuration to a file."""
        try:
            config = self.get_config(chart_type)
            if not config:
                self.logger.warning(f"No configuration to export for {chart_type}")
                return False
            
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            self.logger.info(f"Configuration exported to {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting config: {e}")
            return False
    
    def import_config(self, chart_type: str, filepath: str) -> bool:
        """Import configuration from a file."""
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            
            self.set_config(chart_type, config)
            self.logger.info(f"Configuration imported from {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Error importing config: {e}")
            return False
    
    def reset_config(self, chart_type: str) -> bool:
        """Reset configuration to default."""
        try:
            if chart_type in self.configs:
                del self.configs[chart_type]
            self.logger.info(f"Configuration reset for chart type: {chart_type}")
            return True
        except Exception as e:
            self.logger.error(f"Error resetting config for {chart_type}: {e}")
            return False
    
    def clear_all_configs(self) -> None:
        """Clear all custom configurations."""
        self.configs.clear()
        self.logger.info("All custom configurations cleared")
