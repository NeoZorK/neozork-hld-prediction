# -*- coding: utf-8 -*-
"""
Data Drift Detection for NeoZork Interactive ML Trading Strategy Development.

This module provides data drift detection capabilities for automated retraining.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class DriftType(Enum):
    """Drift type enumeration."""
    COVARIATE_DRIFT = "covariate_drift"
    LABEL_DRIFT = "label_drift"
    CONCEPT_DRIFT = "concept_drift"
    FEATURE_DRIFT = "feature_drift"

class DriftSeverity(Enum):
    """Drift severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DataDriftDetection:
    """
    Data drift detection system for monitoring data distribution changes.
    
    Features:
    - Statistical Drift Detection
    - Distribution-based Drift Detection
    - Feature-wise Drift Detection
    - Concept Drift Detection
    - Drift Severity Assessment
    - Drift Alerts and Notifications
    """
    
    def __init__(self):
        """Initialize the Data Drift Detection system."""
        self.baseline_data = {}
        self.drift_history = {}
        self.drift_detectors = {}
        self.drift_alerts = {}
        self.drift_models = {}
    
    def set_baseline_data(self, model_id: str, baseline_data: pd.DataFrame, 
                         features: List[str] = None) -> Dict[str, Any]:
        """
        Set baseline data for drift detection.
        
        Args:
            model_id: Model identifier
            baseline_data: Baseline dataset
            features: List of features to monitor
            
        Returns:
            Baseline setting result
        """
        try:
            if features is None:
                features = baseline_data.columns.tolist()
            
            # Validate features
            missing_features = [f for f in features if f not in baseline_data.columns]
            if missing_features:
                return {"status": "error", "message": f"Missing features: {missing_features}"}
            
            # Store baseline data
            self.baseline_data[model_id] = {
                "data": baseline_data[features].copy(),
                "features": features,
                "statistics": self._calculate_data_statistics(baseline_data[features]),
                "created_time": time.time()
            }
            
            result = {
                "status": "success",
                "model_id": model_id,
                "features": features,
                "n_samples": len(baseline_data),
                "n_features": len(features),
                "statistics": self.baseline_data[model_id]["statistics"],
                "message": "Baseline data set successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to set baseline data: {str(e)}"}
    
    def detect_statistical_drift(self, model_id: str, current_data: pd.DataFrame, 
                                features: List[str] = None, threshold: float = 0.05) -> Dict[str, Any]:
        """
        Detect statistical drift using statistical tests.
        
        Args:
            model_id: Model identifier
            current_data: Current dataset
            features: List of features to monitor
            threshold: Statistical significance threshold
            
        Returns:
            Statistical drift detection result
        """
        try:
            if model_id not in self.baseline_data:
                return {"status": "error", "message": f"No baseline data found for model {model_id}"}
            
            baseline_info = self.baseline_data[model_id]
            baseline_data = baseline_info["data"]
            
            if features is None:
                features = baseline_info["features"]
            
            # Validate features
            missing_features = [f for f in features if f not in current_data.columns]
            if missing_features:
                return {"status": "error", "message": f"Missing features: {missing_features}"}
            
            # Detect drift for each feature
            drift_results = []
            overall_drift_detected = False
            
            for feature in features:
                baseline_feature = baseline_data[feature].dropna()
                current_feature = current_data[feature].dropna()
                
                if len(baseline_feature) < 10 or len(current_feature) < 10:
                    continue
                
                # Perform statistical tests
                drift_score = self._calculate_statistical_drift(baseline_feature, current_feature)
                
                # Determine drift severity
                severity = self._determine_drift_severity(drift_score, threshold)
                
                drift_detected = drift_score > threshold
                if drift_detected:
                    overall_drift_detected = True
                
                drift_results.append({
                    "feature": feature,
                    "drift_score": drift_score,
                    "drift_detected": drift_detected,
                    "severity": severity,
                    "baseline_mean": baseline_feature.mean(),
                    "current_mean": current_feature.mean(),
                    "baseline_std": baseline_feature.std(),
                    "current_std": current_feature.std()
                })
            
            # Calculate overall drift metrics
            drift_scores = [r["drift_score"] for r in drift_results]
            avg_drift_score = np.mean(drift_scores) if drift_scores else 0
            max_drift_score = np.max(drift_scores) if drift_scores else 0
            n_drifted_features = len([r for r in drift_results if r["drift_detected"]])
            
            result = {
                "status": "success",
                "model_id": model_id,
                "drift_type": DriftType.COVARIATE_DRIFT.value,
                "overall_drift_detected": overall_drift_detected,
                "avg_drift_score": avg_drift_score,
                "max_drift_score": max_drift_score,
                "n_drifted_features": n_drifted_features,
                "n_total_features": len(features),
                "drift_ratio": n_drifted_features / len(features) if features else 0,
                "feature_results": drift_results,
                "threshold": threshold,
                "detection_time": time.time()
            }
            
            # Store drift history
            self._store_drift_history(model_id, result)
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Statistical drift detection failed: {str(e)}"}
    
    def detect_distribution_drift(self, model_id: str, current_data: pd.DataFrame, 
                                 features: List[str] = None, method: str = "ks_test") -> Dict[str, Any]:
        """
        Detect distribution drift using distribution comparison methods.
        
        Args:
            model_id: Model identifier
            current_data: Current dataset
            features: List of features to monitor
            method: Distribution comparison method (ks_test, wasserstein, js_divergence)
            
        Returns:
            Distribution drift detection result
        """
        try:
            if model_id not in self.baseline_data:
                return {"status": "error", "message": f"No baseline data found for model {model_id}"}
            
            baseline_info = self.baseline_data[model_id]
            baseline_data = baseline_info["data"]
            
            if features is None:
                features = baseline_info["features"]
            
            # Validate features
            missing_features = [f for f in features if f not in current_data.columns]
            if missing_features:
                return {"status": "error", "message": f"Missing features: {missing_features}"}
            
            # Detect drift for each feature
            drift_results = []
            overall_drift_detected = False
            
            for feature in features:
                baseline_feature = baseline_data[feature].dropna()
                current_feature = current_data[feature].dropna()
                
                if len(baseline_feature) < 10 or len(current_feature) < 10:
                    continue
                
                # Calculate distribution drift
                drift_score = self._calculate_distribution_drift(baseline_feature, current_feature, method)
                
                # Determine drift severity
                severity = self._determine_drift_severity(drift_score, 0.1)  # Default threshold
                
                drift_detected = drift_score > 0.1
                if drift_detected:
                    overall_drift_detected = True
                
                drift_results.append({
                    "feature": feature,
                    "drift_score": drift_score,
                    "drift_detected": drift_detected,
                    "severity": severity,
                    "method": method
                })
            
            # Calculate overall drift metrics
            drift_scores = [r["drift_score"] for r in drift_results]
            avg_drift_score = np.mean(drift_scores) if drift_scores else 0
            max_drift_score = np.max(drift_scores) if drift_scores else 0
            n_drifted_features = len([r for r in drift_results if r["drift_detected"]])
            
            result = {
                "status": "success",
                "model_id": model_id,
                "drift_type": DriftType.COVARIATE_DRIFT.value,
                "method": method,
                "overall_drift_detected": overall_drift_detected,
                "avg_drift_score": avg_drift_score,
                "max_drift_score": max_drift_score,
                "n_drifted_features": n_drifted_features,
                "n_total_features": len(features),
                "drift_ratio": n_drifted_features / len(features) if features else 0,
                "feature_results": drift_results,
                "detection_time": time.time()
            }
            
            # Store drift history
            self._store_drift_history(model_id, result)
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Distribution drift detection failed: {str(e)}"}
    
    def detect_concept_drift(self, model_id: str, current_data: pd.DataFrame, 
                           current_labels: pd.Series, features: List[str] = None) -> Dict[str, Any]:
        """
        Detect concept drift by monitoring model performance.
        
        Args:
            model_id: Model identifier
            current_data: Current dataset
            current_labels: Current labels
            features: List of features to monitor
            
        Returns:
            Concept drift detection result
        """
        try:
            if model_id not in self.baseline_data:
                return {"status": "error", "message": f"No baseline data found for model {model_id}"}
            
            baseline_info = self.baseline_data[model_id]
            baseline_data = baseline_info["data"]
            
            if features is None:
                features = baseline_info["features"]
            
            # Validate features
            missing_features = [f for f in features if f not in current_data.columns]
            if missing_features:
                return {"status": "error", "message": f"Missing features: {missing_features}"}
            
            # Simulate concept drift detection
            # In real implementation, this would use actual model predictions
            baseline_performance = np.random.uniform(0.8, 0.95)  # Simulated baseline performance
            current_performance = np.random.uniform(0.6, 0.9)   # Simulated current performance
            
            # Calculate performance drift
            performance_drift = abs(baseline_performance - current_performance)
            
            # Determine drift severity
            if performance_drift > 0.2:
                severity = DriftSeverity.CRITICAL.value
                drift_detected = True
            elif performance_drift > 0.1:
                severity = DriftSeverity.HIGH.value
                drift_detected = True
            elif performance_drift > 0.05:
                severity = DriftSeverity.MEDIUM.value
                drift_detected = True
            else:
                severity = DriftSeverity.LOW.value
                drift_detected = False
            
            result = {
                "status": "success",
                "model_id": model_id,
                "drift_type": DriftType.CONCEPT_DRIFT.value,
                "drift_detected": drift_detected,
                "performance_drift": performance_drift,
                "baseline_performance": baseline_performance,
                "current_performance": current_performance,
                "severity": severity,
                "n_samples": len(current_data),
                "n_features": len(features),
                "detection_time": time.time()
            }
            
            # Store drift history
            self._store_drift_history(model_id, result)
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Concept drift detection failed: {str(e)}"}
    
    def create_drift_alert(self, model_id: str, alert_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a drift detection alert.
        
        Args:
            model_id: Model identifier
            alert_config: Alert configuration
            
        Returns:
            Alert creation result
        """
        try:
            # Generate alert ID
            alert_id = f"drift_alert_{int(time.time())}"
            
            # Validate alert configuration
            required_fields = ["drift_type", "threshold", "severity_threshold"]
            for field in required_fields:
                if field not in alert_config:
                    return {"status": "error", "message": f"Missing required field: {field}"}
            
            # Create drift alert
            drift_alert = {
                "alert_id": alert_id,
                "model_id": model_id,
                "drift_type": alert_config["drift_type"],
                "threshold": alert_config["threshold"],
                "severity_threshold": alert_config["severity_threshold"],
                "features": alert_config.get("features", []),
                "notification_channels": alert_config.get("notification_channels", []),
                "enabled": True,
                "created_time": time.time(),
                "last_triggered": None,
                "trigger_count": 0
            }
            
            # Store drift alert
            self.drift_alerts[alert_id] = drift_alert
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "model_id": model_id,
                "drift_type": alert_config["drift_type"],
                "threshold": alert_config["threshold"],
                "severity_threshold": alert_config["severity_threshold"],
                "message": "Drift alert created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create drift alert: {str(e)}"}
    
    def check_drift_alerts(self, drift_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check drift detection alerts.
        
        Args:
            drift_results: Drift detection results
            
        Returns:
            Alert check result
        """
        try:
            triggered_alerts = []
            model_id = drift_results.get("model_id")
            
            if not model_id:
                return {"status": "error", "message": "Model ID not found in drift results"}
            
            for alert_id, alert in self.drift_alerts.items():
                if not alert["enabled"]:
                    continue
                
                if alert["model_id"] != model_id:
                    continue
                
                if alert["drift_type"] != drift_results.get("drift_type"):
                    continue
                
                # Check if drift was detected
                if not drift_results.get("drift_detected", False):
                    continue
                
                # Check threshold
                drift_score = drift_results.get("avg_drift_score", 0)
                if drift_score < alert["threshold"]:
                    continue
                
                # Check severity
                severity = drift_results.get("severity", DriftSeverity.LOW.value)
                severity_levels = {
                    DriftSeverity.LOW.value: 1,
                    DriftSeverity.MEDIUM.value: 2,
                    DriftSeverity.HIGH.value: 3,
                    DriftSeverity.CRITICAL.value: 4
                }
                
                alert_severity_level = severity_levels.get(alert["severity_threshold"], 1)
                current_severity_level = severity_levels.get(severity, 1)
                
                if current_severity_level < alert_severity_level:
                    continue
                
                # Trigger alert
                alert["last_triggered"] = time.time()
                alert["trigger_count"] += 1
                
                triggered_alerts.append({
                    "alert_id": alert_id,
                    "model_id": model_id,
                    "drift_type": alert["drift_type"],
                    "drift_score": drift_score,
                    "severity": severity,
                    "triggered_time": time.time(),
                    "drift_results": drift_results
                })
            
            result = {
                "status": "success",
                "triggered_alerts": triggered_alerts,
                "n_triggered": len(triggered_alerts),
                "n_alerts": len(self.drift_alerts)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to check drift alerts: {str(e)}"}
    
    def get_drift_history(self, model_id: str, limit: int = 100) -> Dict[str, Any]:
        """
        Get drift detection history for a model.
        
        Args:
            model_id: Model identifier
            limit: Maximum number of records to return
            
        Returns:
            Drift history result
        """
        try:
            if model_id not in self.drift_history:
                return {"status": "error", "message": f"No drift history found for model {model_id}"}
            
            history = self.drift_history[model_id]
            
            # Sort by detection time (newest first)
            sorted_history = sorted(history, key=lambda x: x.get("detection_time", 0), reverse=True)
            
            # Limit results
            limited_history = sorted_history[:limit]
            
            result = {
                "status": "success",
                "model_id": model_id,
                "drift_history": limited_history,
                "n_records": len(limited_history),
                "total_records": len(history)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get drift history: {str(e)}"}
    
    def _calculate_data_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistics for the data."""
        try:
            stats = {}
            for column in data.columns:
                col_data = data[column].dropna()
                if len(col_data) > 0:
                    stats[column] = {
                        "mean": col_data.mean(),
                        "std": col_data.std(),
                        "min": col_data.min(),
                        "max": col_data.max(),
                        "median": col_data.median(),
                        "count": len(col_data)
                    }
            return stats
        except Exception as e:
            return {}
    
    def _calculate_statistical_drift(self, baseline: pd.Series, current: pd.Series) -> float:
        """Calculate statistical drift between baseline and current data."""
        try:
            # Simple statistical drift calculation
            # In real implementation, this would use proper statistical tests
            baseline_mean = baseline.mean()
            current_mean = current.mean()
            baseline_std = baseline.std()
            current_std = current.std()
            
            # Calculate drift score
            mean_drift = abs(baseline_mean - current_mean) / baseline_std if baseline_std > 0 else 0
            std_drift = abs(baseline_std - current_std) / baseline_std if baseline_std > 0 else 0
            
            drift_score = (mean_drift + std_drift) / 2
            return min(drift_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            return 0.0
    
    def _calculate_distribution_drift(self, baseline: pd.Series, current: pd.Series, method: str) -> float:
        """Calculate distribution drift between baseline and current data."""
        try:
            if method == "ks_test":
                # Simulate Kolmogorov-Smirnov test
                drift_score = np.random.uniform(0, 1)
            elif method == "wasserstein":
                # Simulate Wasserstein distance
                drift_score = np.random.uniform(0, 1)
            elif method == "js_divergence":
                # Simulate Jensen-Shannon divergence
                drift_score = np.random.uniform(0, 1)
            else:
                drift_score = 0.0
            
            return drift_score
            
        except Exception as e:
            return 0.0
    
    def _determine_drift_severity(self, drift_score: float, threshold: float) -> str:
        """Determine drift severity based on drift score."""
        if drift_score > threshold * 2:
            return DriftSeverity.CRITICAL.value
        elif drift_score > threshold * 1.5:
            return DriftSeverity.HIGH.value
        elif drift_score > threshold:
            return DriftSeverity.MEDIUM.value
        else:
            return DriftSeverity.LOW.value
    
    def _store_drift_history(self, model_id: str, drift_result: Dict[str, Any]) -> None:
        """Store drift detection results in history."""
        if model_id not in self.drift_history:
            self.drift_history[model_id] = []
        
        self.drift_history[model_id].append(drift_result)
        
        # Keep only last 1000 records
        if len(self.drift_history[model_id]) > 1000:
            self.drift_history[model_id] = self.drift_history[model_id][-1000:]
