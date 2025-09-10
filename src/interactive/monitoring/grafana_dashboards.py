# -*- coding: utf-8 -*-
"""
Grafana Dashboards for NeoZork Interactive ML Trading Strategy Development.

This module provides Grafana dashboard creation and management capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
from typing import Dict, Any, Optional, List, Tuple
import warnings

class GrafanaDashboards:
    """
    Grafana dashboards system for visualization.
    
    Features:
    - Dashboard Creation
    - Panel Management
    - Data Source Integration
    - Alert Configuration
    - Dashboard Sharing
    - Template Management
    """
    
    def __init__(self):
        """Initialize the Grafana Dashboards system."""
        self.dashboards = {}
        self.panels = {}
        self.data_sources = {}
        self.alert_configs = {}
        self.templates = {}
    
    def create_dashboard(self, dashboard_name: str, title: str, 
                        description: str = "", tags: List[str] = None) -> Dict[str, Any]:
        """
        Create a new Grafana dashboard.
        
        Args:
            dashboard_name: Name of the dashboard
            title: Title of the dashboard
            description: Description of the dashboard
            tags: Tags for the dashboard
            
        Returns:
            Dashboard creation result
        """
        try:
            # Generate dashboard ID
            dashboard_id = f"dashboard_{int(time.time())}"
            
            # Create dashboard
            dashboard = {
                "id": dashboard_id,
                "name": dashboard_name,
                "title": title,
                "description": description,
                "tags": tags or [],
                "panels": [],
                "time_range": {
                    "from": "now-1h",
                    "to": "now"
                },
                "refresh": "5s",
                "created_time": time.time(),
                "last_updated": time.time(),
                "version": 1
            }
            
            # Store dashboard
            self.dashboards[dashboard_id] = dashboard
            
            result = {
                "status": "success",
                "dashboard_id": dashboard_id,
                "dashboard_name": dashboard_name,
                "title": title,
                "description": description,
                "tags": tags or [],
                "message": "Dashboard created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create dashboard: {str(e)}"}
    
    def add_panel(self, dashboard_id: str, panel_type: str, title: str,
                  query: str, data_source: str, position: Dict[str, int] = None) -> Dict[str, Any]:
        """
        Add a panel to dashboard.
        
        Args:
            dashboard_id: Dashboard ID
            panel_type: Type of panel (graph, table, stat, gauge, etc.)
            title: Title of the panel
            query: Query for the panel
            data_source: Data source for the panel
            position: Position of the panel (x, y, w, h)
            
        Returns:
            Panel addition result
        """
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            # Generate panel ID
            panel_id = f"panel_{int(time.time())}"
            
            # Default position
            if position is None:
                position = {"x": 0, "y": 0, "w": 12, "h": 8}
            
            # Create panel
            panel = {
                "id": panel_id,
                "type": panel_type,
                "title": title,
                "query": query,
                "data_source": data_source,
                "position": position,
                "options": {},
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Add panel to dashboard
            self.dashboards[dashboard_id]["panels"].append(panel)
            self.dashboards[dashboard_id]["last_updated"] = time.time()
            self.dashboards[dashboard_id]["version"] += 1
            
            # Store panel separately
            self.panels[panel_id] = panel
            
            result = {
                "status": "success",
                "panel_id": panel_id,
                "dashboard_id": dashboard_id,
                "panel_type": panel_type,
                "title": title,
                "query": query,
                "data_source": data_source,
                "position": position,
                "message": "Panel added successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to add panel: {str(e)}"}
    
    def update_panel(self, panel_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a panel.
        
        Args:
            panel_id: Panel ID
            updates: Updates to apply
            
        Returns:
            Panel update result
        """
        try:
            if panel_id not in self.panels:
                return {"status": "error", "message": f"Panel {panel_id} not found"}
            
            # Update panel
            panel = self.panels[panel_id]
            for key, value in updates.items():
                if key in panel:
                    panel[key] = value
            
            panel["last_updated"] = time.time()
            
            # Update dashboard version
            for dashboard_id, dashboard in self.dashboards.items():
                for panel in dashboard["panels"]:
                    if panel["id"] == panel_id:
                        dashboard["last_updated"] = time.time()
                        dashboard["version"] += 1
                        break
            
            result = {
                "status": "success",
                "panel_id": panel_id,
                "updates": updates,
                "message": "Panel updated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to update panel: {str(e)}"}
    
    def remove_panel(self, panel_id: str) -> Dict[str, Any]:
        """
        Remove a panel from dashboard.
        
        Args:
            panel_id: Panel ID to remove
            
        Returns:
            Panel removal result
        """
        try:
            if panel_id not in self.panels:
                return {"status": "error", "message": f"Panel {panel_id} not found"}
            
            # Remove panel from dashboards
            for dashboard_id, dashboard in self.dashboards.items():
                dashboard["panels"] = [p for p in dashboard["panels"] if p["id"] != panel_id]
                if len(dashboard["panels"]) < len([p for p in dashboard["panels"] if p["id"] != panel_id]):
                    dashboard["last_updated"] = time.time()
                    dashboard["version"] += 1
            
            # Remove panel
            del self.panels[panel_id]
            
            result = {
                "status": "success",
                "panel_id": panel_id,
                "message": "Panel removed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to remove panel: {str(e)}"}
    
    def create_data_source(self, name: str, source_type: str, 
                          url: str, access: str = "proxy") -> Dict[str, Any]:
        """
        Create a data source.
        
        Args:
            name: Name of the data source
            source_type: Type of data source (prometheus, influxdb, etc.)
            url: URL of the data source
            access: Access mode (proxy, direct)
            
        Returns:
            Data source creation result
        """
        try:
            # Generate data source ID
            data_source_id = f"ds_{int(time.time())}"
            
            # Create data source
            data_source = {
                "id": data_source_id,
                "name": name,
                "type": source_type,
                "url": url,
                "access": access,
                "is_default": False,
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Store data source
            self.data_sources[data_source_id] = data_source
            
            result = {
                "status": "success",
                "data_source_id": data_source_id,
                "name": name,
                "type": source_type,
                "url": url,
                "access": access,
                "message": "Data source created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create data source: {str(e)}"}
    
    def configure_alert(self, panel_id: str, alert_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure alert for a panel.
        
        Args:
            panel_id: Panel ID
            alert_config: Alert configuration
            
        Returns:
            Alert configuration result
        """
        try:
            if panel_id not in self.panels:
                return {"status": "error", "message": f"Panel {panel_id} not found"}
            
            # Generate alert ID
            alert_id = f"alert_{int(time.time())}"
            
            # Create alert configuration
            alert = {
                "id": alert_id,
                "panel_id": panel_id,
                "name": alert_config.get("name", f"Alert for {panel_id}"),
                "message": alert_config.get("message", ""),
                "frequency": alert_config.get("frequency", "10s"),
                "conditions": alert_config.get("conditions", []),
                "notifications": alert_config.get("notifications", []),
                "enabled": alert_config.get("enabled", True),
                "created_time": time.time(),
                "last_updated": time.time()
            }
            
            # Store alert configuration
            self.alert_configs[alert_id] = alert
            
            result = {
                "status": "success",
                "alert_id": alert_id,
                "panel_id": panel_id,
                "alert_config": alert,
                "message": "Alert configured successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to configure alert: {str(e)}"}
    
    def create_template(self, template_name: str, template_type: str,
                       content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a dashboard template.
        
        Args:
            template_name: Name of the template
            template_type: Type of template (trading, performance, system)
            content: Template content
            
        Returns:
            Template creation result
        """
        try:
            # Generate template ID
            template_id = f"template_{int(time.time())}"
            
            # Create template
            template = {
                "id": template_id,
                "name": template_name,
                "type": template_type,
                "content": content,
                "created_time": time.time(),
                "last_updated": time.time(),
                "version": 1
            }
            
            # Store template
            self.templates[template_id] = template
            
            result = {
                "status": "success",
                "template_id": template_id,
                "template_name": template_name,
                "template_type": template_type,
                "content": content,
                "message": "Template created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create template: {str(e)}"}
    
    def apply_template(self, dashboard_id: str, template_id: str) -> Dict[str, Any]:
        """
        Apply a template to a dashboard.
        
        Args:
            dashboard_id: Dashboard ID
            template_id: Template ID
            
        Returns:
            Template application result
        """
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            if template_id not in self.templates:
                return {"status": "error", "message": f"Template {template_id} not found"}
            
            # Get template
            template = self.templates[template_id]
            template_content = template["content"]
            
            # Apply template to dashboard
            dashboard = self.dashboards[dashboard_id]
            
            # Add panels from template
            if "panels" in template_content:
                for panel_template in template_content["panels"]:
                    panel_result = self.add_panel(
                        dashboard_id,
                        panel_template.get("type", "graph"),
                        panel_template.get("title", "Panel"),
                        panel_template.get("query", ""),
                        panel_template.get("data_source", "prometheus"),
                        panel_template.get("position", {"x": 0, "y": 0, "w": 12, "h": 8})
                    )
                    
                    if panel_result["status"] != "success":
                        return panel_result
            
            # Update dashboard settings
            if "time_range" in template_content:
                dashboard["time_range"] = template_content["time_range"]
            
            if "refresh" in template_content:
                dashboard["refresh"] = template_content["refresh"]
            
            dashboard["last_updated"] = time.time()
            dashboard["version"] += 1
            
            result = {
                "status": "success",
                "dashboard_id": dashboard_id,
                "template_id": template_id,
                "template_name": template["name"],
                "message": "Template applied successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to apply template: {str(e)}"}
    
    def get_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """
        Get dashboard information.
        
        Args:
            dashboard_id: Dashboard ID
            
        Returns:
            Dashboard information
        """
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            dashboard = self.dashboards[dashboard_id]
            
            result = {
                "status": "success",
                "dashboard": dashboard
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get dashboard: {str(e)}"}
    
    def list_dashboards(self) -> Dict[str, Any]:
        """
        List all dashboards.
        
        Returns:
            List of dashboards
        """
        try:
            dashboard_list = []
            
            for dashboard_id, dashboard in self.dashboards.items():
                dashboard_list.append({
                    "id": dashboard_id,
                    "name": dashboard["name"],
                    "title": dashboard["title"],
                    "description": dashboard["description"],
                    "tags": dashboard["tags"],
                    "n_panels": len(dashboard["panels"]),
                    "created_time": dashboard["created_time"],
                    "last_updated": dashboard["last_updated"],
                    "version": dashboard["version"]
                })
            
            result = {
                "status": "success",
                "dashboards": dashboard_list,
                "n_dashboards": len(dashboard_list)
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to list dashboards: {str(e)}"}
    
    def export_dashboard(self, dashboard_id: str, format: str = "json") -> Dict[str, Any]:
        """
        Export dashboard.
        
        Args:
            dashboard_id: Dashboard ID
            format: Export format (json, grafana)
            
        Returns:
            Export result
        """
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            dashboard = self.dashboards[dashboard_id]
            
            if format == "json":
                # Export as JSON
                export_data = {
                    "dashboard": dashboard,
                    "export_time": time.time()
                }
                
                result = {
                    "status": "success",
                    "format": "json",
                    "data": export_data,
                    "size": len(json.dumps(export_data))
                }
                
            elif format == "grafana":
                # Export as Grafana format
                grafana_data = {
                    "dashboard": {
                        "id": None,
                        "title": dashboard["title"],
                        "description": dashboard["description"],
                        "tags": dashboard["tags"],
                        "timezone": "browser",
                        "panels": [],
                        "time": dashboard["time_range"],
                        "refresh": dashboard["refresh"],
                        "version": dashboard["version"]
                    },
                    "overwrite": True
                }
                
                # Add panels
                for panel in dashboard["panels"]:
                    grafana_panel = {
                        "id": None,
                        "title": panel["title"],
                        "type": panel["type"],
                        "targets": [
                            {
                                "expr": panel["query"],
                                "datasource": panel["data_source"]
                            }
                        ],
                        "gridPos": panel["position"],
                        "options": panel["options"]
                    }
                    grafana_data["dashboard"]["panels"].append(grafana_panel)
                
                result = {
                    "status": "success",
                    "format": "grafana",
                    "data": grafana_data,
                    "size": len(json.dumps(grafana_data))
                }
                
            else:
                return {"status": "error", "message": f"Unsupported format: {format}"}
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to export dashboard: {str(e)}"}
    
    def delete_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """
        Delete a dashboard.
        
        Args:
            dashboard_id: Dashboard ID
            
        Returns:
            Deletion result
        """
        try:
            if dashboard_id not in self.dashboards:
                return {"status": "error", "message": f"Dashboard {dashboard_id} not found"}
            
            # Remove panels
            dashboard = self.dashboards[dashboard_id]
            for panel in dashboard["panels"]:
                if panel["id"] in self.panels:
                    del self.panels[panel["id"]]
            
            # Remove dashboard
            del self.dashboards[dashboard_id]
            
            result = {
                "status": "success",
                "dashboard_id": dashboard_id,
                "message": "Dashboard deleted successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete dashboard: {str(e)}"}
