# -*- coding: utf-8 -*-
"""
Horizontal Scaling for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive horizontal scaling capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import threading
import subprocess
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class ScalingStrategy(Enum):
    """Scaling strategy enumeration."""
    CPU_BASED = "cpu_based"
    MEMORY_BASED = "memory_based"
    LOAD_BASED = "load_based"
    CUSTOM_METRIC = "custom_metric"
    SCHEDULED = "scheduled"

class InstanceStatus(Enum):
    """Instance status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    TERMINATED = "terminated"

class HorizontalScaling:
    """
    Horizontal scaling manager for distributed system deployment.
    
    Features:
    - Auto-scaling Groups
    - Load Balancing
    - Instance Management
    - Health Checks
    - Scaling Policies
    - Resource Monitoring
    """
    
    def __init__(self, max_instances: int = 10, min_instances: int = 1):
        """
        Initialize the Horizontal Scaling manager.
        
        Args:
            max_instances: Maximum number of instances
            min_instances: Minimum number of instances
        """
        self.max_instances = max_instances
        self.min_instances = min_instances
        self.instances = {}
        self.scaling_policies = {}
        self.load_balancer = None
        self.health_checks = {}
        self.metrics_history = []
        self.scaling_events = []
        self.instance_counter = 0
        self.is_scaling_active = False
        self.scaling_thread = None
    
    def create_scaling_group(self, group_name: str, instance_type: str, 
                           scaling_strategy: str = ScalingStrategy.CPU_BASED.value,
                           target_metric: str = "cpu_utilization",
                           target_value: float = 70.0) -> Dict[str, Any]:
        """
        Create an auto-scaling group.
        
        Args:
            group_name: Name of the scaling group
            instance_type: Type of instances to create
            scaling_strategy: Scaling strategy to use
            target_metric: Target metric for scaling
            target_value: Target value for the metric
            
        Returns:
            Scaling group creation result
        """
        try:
            # Generate group ID
            group_id = f"sg_{int(time.time())}"
            
            # Create scaling group
            scaling_group = {
                "group_id": group_id,
                "group_name": group_name,
                "instance_type": instance_type,
                "scaling_strategy": scaling_strategy,
                "target_metric": target_metric,
                "target_value": target_value,
                "min_instances": self.min_instances,
                "max_instances": self.max_instances,
                "current_instances": 0,
                "desired_instances": self.min_instances,
                "created_time": time.time(),
                "instances": [],
                "scaling_history": []
            }
            
            # Store scaling group
            self.scaling_policies[group_id] = scaling_group
            
            result = {
                "status": "success",
                "group_id": group_id,
                "group_name": group_name,
                "instance_type": instance_type,
                "scaling_strategy": scaling_strategy,
                "target_metric": target_metric,
                "target_value": target_value,
                "min_instances": self.min_instances,
                "max_instances": self.max_instances,
                "message": "Scaling group created successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to create scaling group: {str(e)}"}
    
    def launch_instance(self, group_id: str, instance_type: str = None) -> Dict[str, Any]:
        """
        Launch a new instance in the scaling group.
        
        Args:
            group_id: Scaling group ID
            instance_type: Type of instance to launch
            
        Returns:
            Instance launch result
        """
        try:
            # Check if scaling group exists
            if group_id not in self.scaling_policies:
                return {"status": "error", "message": f"Scaling group {group_id} not found"}
            
            scaling_group = self.scaling_policies[group_id]
            
            # Check instance limit
            if scaling_group["current_instances"] >= scaling_group["max_instances"]:
                return {"status": "error", "message": "Maximum instances reached"}
            
            # Use group instance type if not specified
            if instance_type is None:
                instance_type = scaling_group["instance_type"]
            
            # Generate instance ID
            self.instance_counter += 1
            instance_id = f"i-{self.instance_counter:06d}"
            
            # Create instance
            instance = {
                "instance_id": instance_id,
                "group_id": group_id,
                "instance_type": instance_type,
                "status": InstanceStatus.PENDING.value,
                "launch_time": time.time(),
                "private_ip": f"10.0.{self.instance_counter % 256}.{self.instance_counter % 256}",
                "public_ip": f"54.{self.instance_counter % 256}.{self.instance_counter % 256}.{self.instance_counter % 256}",
                "health_status": "initializing",
                "metrics": {
                    "cpu_utilization": 0.0,
                    "memory_utilization": 0.0,
                    "network_in": 0,
                    "network_out": 0,
                    "disk_usage": 0.0
                }
            }
            
            # Store instance
            self.instances[instance_id] = instance
            scaling_group["instances"].append(instance_id)
            scaling_group["current_instances"] += 1
            
            # Simulate instance startup
            threading.Timer(2.0, self._simulate_instance_startup, args=[instance_id]).start()
            
            result = {
                "status": "success",
                "instance_id": instance_id,
                "group_id": group_id,
                "instance_type": instance_type,
                "status": instance["status"],
                "private_ip": instance["private_ip"],
                "public_ip": instance["public_ip"],
                "message": "Instance launched successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to launch instance: {str(e)}"}
    
    def terminate_instance(self, instance_id: str) -> Dict[str, Any]:
        """
        Terminate an instance.
        
        Args:
            instance_id: Instance ID to terminate
            
        Returns:
            Instance termination result
        """
        try:
            # Check if instance exists
            if instance_id not in self.instances:
                return {"status": "error", "message": f"Instance {instance_id} not found"}
            
            instance = self.instances[instance_id]
            group_id = instance["group_id"]
            
            # Check minimum instances
            scaling_group = self.scaling_policies[group_id]
            if scaling_group["current_instances"] <= scaling_group["min_instances"]:
                return {"status": "error", "message": "Cannot terminate instance: minimum instances reached"}
            
            # Update instance status
            instance["status"] = InstanceStatus.STOPPING.value
            
            # Simulate instance termination
            threading.Timer(1.0, self._simulate_instance_termination, args=[instance_id]).start()
            
            result = {
                "status": "success",
                "instance_id": instance_id,
                "group_id": group_id,
                "status": instance["status"],
                "message": "Instance termination initiated"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to terminate instance: {str(e)}"}
    
    def update_scaling_policy(self, group_id: str, target_metric: str = None,
                            target_value: float = None, min_instances: int = None,
                            max_instances: int = None) -> Dict[str, Any]:
        """
        Update scaling policy for a group.
        
        Args:
            group_id: Scaling group ID
            target_metric: New target metric
            target_value: New target value
            min_instances: New minimum instances
            max_instances: New maximum instances
            
        Returns:
            Policy update result
        """
        try:
            # Check if scaling group exists
            if group_id not in self.scaling_policies:
                return {"status": "error", "message": f"Scaling group {group_id} not found"}
            
            scaling_group = self.scaling_policies[group_id]
            
            # Update policy parameters
            if target_metric is not None:
                scaling_group["target_metric"] = target_metric
            if target_value is not None:
                scaling_group["target_value"] = target_value
            if min_instances is not None:
                scaling_group["min_instances"] = min_instances
            if max_instances is not None:
                scaling_group["max_instances"] = max_instances
            
            # Validate policy
            if scaling_group["min_instances"] > scaling_group["max_instances"]:
                return {"status": "error", "message": "Minimum instances cannot be greater than maximum instances"}
            
            result = {
                "status": "success",
                "group_id": group_id,
                "target_metric": scaling_group["target_metric"],
                "target_value": scaling_group["target_value"],
                "min_instances": scaling_group["min_instances"],
                "max_instances": scaling_group["max_instances"],
                "message": "Scaling policy updated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to update scaling policy: {str(e)}"}
    
    def get_scaling_group_status(self, group_id: str) -> Dict[str, Any]:
        """
        Get scaling group status.
        
        Args:
            group_id: Scaling group ID
            
        Returns:
            Scaling group status result
        """
        try:
            # Check if scaling group exists
            if group_id not in self.scaling_policies:
                return {"status": "error", "message": f"Scaling group {group_id} not found"}
            
            scaling_group = self.scaling_policies[group_id]
            
            # Get instance statuses
            instance_statuses = {}
            for instance_id in scaling_group["instances"]:
                if instance_id in self.instances:
                    instance = self.instances[instance_id]
                    instance_statuses[instance_id] = {
                        "status": instance["status"],
                        "health_status": instance["health_status"],
                        "launch_time": instance["launch_time"],
                        "private_ip": instance["private_ip"],
                        "public_ip": instance["public_ip"]
                    }
            
            # Calculate group metrics
            running_instances = len([i for i in instance_statuses.values() if i["status"] == "running"])
            healthy_instances = len([i for i in instance_statuses.values() if i["health_status"] == "healthy"])
            
            status = {
                "group_id": group_id,
                "group_name": scaling_group["group_name"],
                "instance_type": scaling_group["instance_type"],
                "scaling_strategy": scaling_group["scaling_strategy"],
                "target_metric": scaling_group["target_metric"],
                "target_value": scaling_group["target_value"],
                "min_instances": scaling_group["min_instances"],
                "max_instances": scaling_group["max_instances"],
                "current_instances": scaling_group["current_instances"],
                "desired_instances": scaling_group["desired_instances"],
                "running_instances": running_instances,
                "healthy_instances": healthy_instances,
                "instance_statuses": instance_statuses,
                "created_time": scaling_group["created_time"]
            }
            
            result = {
                "status": "success",
                "status": status
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get scaling group status: {str(e)}"}
    
    def start_auto_scaling(self, group_id: str) -> Dict[str, Any]:
        """
        Start auto-scaling for a group.
        
        Args:
            group_id: Scaling group ID
            
        Returns:
            Auto-scaling start result
        """
        try:
            # Check if scaling group exists
            if group_id not in self.scaling_policies:
                return {"status": "error", "message": f"Scaling group {group_id} not found"}
            
            # Start scaling thread if not already running
            if not self.is_scaling_active:
                self.is_scaling_active = True
                self.scaling_thread = threading.Thread(target=self._auto_scaling_loop)
                self.scaling_thread.daemon = True
                self.scaling_thread.start()
            
            result = {
                "status": "success",
                "group_id": group_id,
                "message": "Auto-scaling started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start auto-scaling: {str(e)}"}
    
    def stop_auto_scaling(self, group_id: str) -> Dict[str, Any]:
        """
        Stop auto-scaling for a group.
        
        Args:
            group_id: Scaling group ID
            
        Returns:
            Auto-scaling stop result
        """
        try:
            # Stop scaling thread
            self.is_scaling_active = False
            
            if self.scaling_thread and self.scaling_thread.is_alive():
                self.scaling_thread.join(timeout=5)
            
            result = {
                "status": "success",
                "group_id": group_id,
                "message": "Auto-scaling stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop auto-scaling: {str(e)}"}
    
    def get_scaling_statistics(self) -> Dict[str, Any]:
        """
        Get scaling statistics.
        
        Returns:
            Scaling statistics result
        """
        try:
            # Calculate statistics
            total_instances = len(self.instances)
            running_instances = len([i for i in self.instances.values() if i["status"] == "running"])
            pending_instances = len([i for i in self.instances.values() if i["status"] == "pending"])
            stopped_instances = len([i for i in self.instances.values() if i["status"] == "stopped"])
            failed_instances = len([i for i in self.instances.values() if i["status"] == "failed"])
            
            # Calculate average metrics
            if running_instances > 0:
                avg_cpu = np.mean([i["metrics"]["cpu_utilization"] for i in self.instances.values() if i["status"] == "running"])
                avg_memory = np.mean([i["metrics"]["memory_utilization"] for i in self.instances.values() if i["status"] == "running"])
            else:
                avg_cpu = 0.0
                avg_memory = 0.0
            
            statistics = {
                "total_instances": total_instances,
                "running_instances": running_instances,
                "pending_instances": pending_instances,
                "stopped_instances": stopped_instances,
                "failed_instances": failed_instances,
                "scaling_groups": len(self.scaling_policies),
                "avg_cpu_utilization": avg_cpu,
                "avg_memory_utilization": avg_memory,
                "is_scaling_active": self.is_scaling_active,
                "scaling_events": len(self.scaling_events)
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get scaling statistics: {str(e)}"}
    
    def _simulate_instance_startup(self, instance_id: str) -> None:
        """Simulate instance startup process."""
        try:
            if instance_id in self.instances:
                instance = self.instances[instance_id]
                instance["status"] = InstanceStatus.RUNNING.value
                instance["health_status"] = "healthy"
                
                # Record scaling event
                self.scaling_events.append({
                    "event_type": "instance_started",
                    "instance_id": instance_id,
                    "group_id": instance["group_id"],
                    "timestamp": time.time()
                })
                
        except Exception as e:
            print(f"Error in instance startup simulation: {e}")
    
    def _simulate_instance_termination(self, instance_id: str) -> None:
        """Simulate instance termination process."""
        try:
            if instance_id in self.instances:
                instance = self.instances[instance_id]
                group_id = instance["group_id"]
                
                # Update instance status
                instance["status"] = InstanceStatus.TERMINATED.value
                
                # Remove from scaling group
                if group_id in self.scaling_policies:
                    scaling_group = self.scaling_policies[group_id]
                    if instance_id in scaling_group["instances"]:
                        scaling_group["instances"].remove(instance_id)
                        scaling_group["current_instances"] -= 1
                
                # Record scaling event
                self.scaling_events.append({
                    "event_type": "instance_terminated",
                    "instance_id": instance_id,
                    "group_id": group_id,
                    "timestamp": time.time()
                })
                
        except Exception as e:
            print(f"Error in instance termination simulation: {e}")
    
    def _auto_scaling_loop(self) -> None:
        """Auto-scaling loop for monitoring and scaling decisions."""
        try:
            while self.is_scaling_active:
                for group_id, scaling_group in self.scaling_policies.items():
                    self._evaluate_scaling_decision(group_id, scaling_group)
                
                # Sleep for 30 seconds
                time.sleep(30)
                
        except Exception as e:
            print(f"Error in auto-scaling loop: {e}")
    
    def _evaluate_scaling_decision(self, group_id: str, scaling_group: Dict[str, Any]) -> None:
        """Evaluate scaling decision for a group."""
        try:
            # Get current metrics
            running_instances = [i for i in scaling_group["instances"] if i in self.instances and self.instances[i]["status"] == "running"]
            
            if not running_instances:
                return
            
            # Calculate average metric
            target_metric = scaling_group["target_metric"]
            target_value = scaling_group["target_value"]
            
            if target_metric == "cpu_utilization":
                avg_metric = np.mean([self.instances[i]["metrics"]["cpu_utilization"] for i in running_instances])
            elif target_metric == "memory_utilization":
                avg_metric = np.mean([self.instances[i]["metrics"]["memory_utilization"] for i in running_instances])
            else:
                avg_metric = 0.0
            
            # Make scaling decision
            current_instances = scaling_group["current_instances"]
            desired_instances = scaling_group["desired_instances"]
            
            if avg_metric > target_value and current_instances < scaling_group["max_instances"]:
                # Scale out
                new_instances = min(2, scaling_group["max_instances"] - current_instances)
                for _ in range(new_instances):
                    self.launch_instance(group_id)
                
                # Record scaling event
                self.scaling_events.append({
                    "event_type": "scale_out",
                    "group_id": group_id,
                    "reason": f"{target_metric} > {target_value}",
                    "current_instances": current_instances,
                    "new_instances": new_instances,
                    "timestamp": time.time()
                })
                
            elif avg_metric < target_value * 0.5 and current_instances > scaling_group["min_instances"]:
                # Scale in
                instances_to_terminate = min(1, current_instances - scaling_group["min_instances"])
                for instance_id in running_instances[:instances_to_terminate]:
                    self.terminate_instance(instance_id)
                
                # Record scaling event
                self.scaling_events.append({
                    "event_type": "scale_in",
                    "group_id": group_id,
                    "reason": f"{target_metric} < {target_value * 0.5}",
                    "current_instances": current_instances,
                    "instances_to_terminate": instances_to_terminate,
                    "timestamp": time.time()
                })
                
        except Exception as e:
            print(f"Error in scaling decision evaluation: {e}")
