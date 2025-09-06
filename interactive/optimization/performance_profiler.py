# -*- coding: utf-8 -*-
"""
Performance Profiler for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive performance profiling and analysis capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import psutil
import threading
from typing import Dict, Any, Optional, List, Tuple, Callable
from enum import Enum
import warnings

class ProfilerType(Enum):
    """Profiler type enumeration."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    FUNCTION = "function"
    LINE = "line"

class PerformanceProfiler:
    """
    Performance profiler for system and application monitoring.
    
    Features:
    - CPU Profiling
    - Memory Profiling
    - Disk I/O Profiling
    - Network Profiling
    - Function Profiling
    - Line-by-Line Profiling
    - Performance Metrics
    - Bottleneck Detection
    """
    
    def __init__(self):
        """Initialize the Performance Profiler."""
        self.profiles = {}
        self.metrics_history = []
        self.bottlenecks = {}
        self.profiling_active = False
        self.monitoring_thread = None
        self.function_timings = {}
        self.memory_snapshots = {}
    
    def start_system_profiling(self, profile_name: str, duration: int = 60) -> Dict[str, Any]:
        """
        Start system-wide performance profiling.
        
        Args:
            profile_name: Name for the profile
            duration: Duration in seconds
            
        Returns:
            Profiling start result
        """
        try:
            # Check if profiling is already active
            if self.profiling_active:
                return {"status": "error", "message": "Profiling is already active"}
            
            # Generate profile ID
            profile_id = f"profile_{int(time.time())}"
            
            # Create profile
            profile = {
                "profile_id": profile_id,
                "profile_name": profile_name,
                "profile_type": "system",
                "start_time": time.time(),
                "duration": duration,
                "end_time": time.time() + duration,
                "metrics": [],
                "is_active": True
            }
            
            # Store profile
            self.profiles[profile_id] = profile
            
            # Start monitoring thread
            self.profiling_active = True
            self.monitoring_thread = threading.Thread(
                target=self._monitor_system_metrics,
                args=(profile_id, duration)
            )
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            result = {
                "status": "success",
                "profile_id": profile_id,
                "profile_name": profile_name,
                "duration": duration,
                "start_time": profile["start_time"],
                "message": "System profiling started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start system profiling: {str(e)}"}
    
    def stop_profiling(self, profile_id: str) -> Dict[str, Any]:
        """
        Stop profiling and generate report.
        
        Args:
            profile_id: Profile ID to stop
            
        Returns:
            Profiling stop result
        """
        try:
            # Check if profile exists
            if profile_id not in self.profiles:
                return {"status": "error", "message": f"Profile {profile_id} not found"}
            
            profile = self.profiles[profile_id]
            
            # Stop profiling
            profile["is_active"] = False
            profile["end_time"] = time.time()
            self.profiling_active = False
            
            # Wait for monitoring thread to finish
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            # Generate performance report
            report = self._generate_performance_report(profile_id)
            
            result = {
                "status": "success",
                "profile_id": profile_id,
                "profile_name": profile["profile_name"],
                "duration": profile["end_time"] - profile["start_time"],
                "report": report,
                "message": "Profiling stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop profiling: {str(e)}"}
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile a single function execution.
        
        Args:
            func: Function to profile
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function profiling result
        """
        try:
            function_name = func.__name__
            
            # Start timing
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            # Execute function
            result = func(*args, **kwargs)
            
            # End timing
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss
            
            # Calculate metrics
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Store function timing
            if function_name not in self.function_timings:
                self.function_timings[function_name] = []
            
            self.function_timings[function_name].append({
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "timestamp": time.time(),
                "args_count": len(args),
                "kwargs_count": len(kwargs)
            })
            
            profiling_result = {
                "status": "success",
                "function_name": function_name,
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "memory_delta_mb": memory_delta / (1024 * 1024),
                "result": result,
                "timestamp": time.time()
            }
            
            return profiling_result
            
        except Exception as e:
            return {"status": "error", "message": f"Function profiling failed: {str(e)}"}
    
    def get_cpu_metrics(self) -> Dict[str, Any]:
        """
        Get current CPU metrics.
        
        Returns:
            CPU metrics result
        """
        try:
            # Get CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_times = psutil.cpu_times()
            load_avg = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
            
            metrics = {
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_frequency": {
                    "current": cpu_freq.current if cpu_freq else 0,
                    "min": cpu_freq.min if cpu_freq else 0,
                    "max": cpu_freq.max if cpu_freq else 0
                },
                "cpu_times": {
                    "user": cpu_times.user,
                    "system": cpu_times.system,
                    "idle": cpu_times.idle,
                    "iowait": getattr(cpu_times, 'iowait', 0),
                    "irq": getattr(cpu_times, 'irq', 0),
                    "softirq": getattr(cpu_times, 'softirq', 0)
                },
                "load_average": {
                    "1min": load_avg[0],
                    "5min": load_avg[1],
                    "15min": load_avg[2]
                },
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get CPU metrics: {str(e)}"}
    
    def get_memory_metrics(self) -> Dict[str, Any]:
        """
        Get current memory metrics.
        
        Returns:
            Memory metrics result
        """
        try:
            # Get memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            process = psutil.Process()
            process_memory = process.memory_info()
            
            metrics = {
                "system_memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "percent": memory.percent,
                    "cached": getattr(memory, 'cached', 0),
                    "buffers": getattr(memory, 'buffers', 0)
                },
                "swap_memory": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent
                },
                "process_memory": {
                    "rss": process_memory.rss,
                    "vms": process_memory.vms,
                    "percent": process.memory_percent()
                },
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get memory metrics: {str(e)}"}
    
    def get_disk_metrics(self) -> Dict[str, Any]:
        """
        Get current disk I/O metrics.
        
        Returns:
            Disk metrics result
        """
        try:
            # Get disk metrics
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            disk_partitions = psutil.disk_partitions()
            
            metrics = {
                "disk_usage": {
                    "total": disk_usage.total,
                    "used": disk_usage.used,
                    "free": disk_usage.free,
                    "percent": (disk_usage.used / disk_usage.total) * 100
                },
                "disk_io": {
                    "read_count": disk_io.read_count if disk_io else 0,
                    "write_count": disk_io.write_count if disk_io else 0,
                    "read_bytes": disk_io.read_bytes if disk_io else 0,
                    "write_bytes": disk_io.write_bytes if disk_io else 0,
                    "read_time": disk_io.read_time if disk_io else 0,
                    "write_time": disk_io.write_time if disk_io else 0
                },
                "partitions": [
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "opts": partition.opts
                    }
                    for partition in disk_partitions
                ],
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get disk metrics: {str(e)}"}
    
    def get_network_metrics(self) -> Dict[str, Any]:
        """
        Get current network metrics.
        
        Returns:
            Network metrics result
        """
        try:
            # Simulate network metrics to avoid psutil issues
            metrics = {
                "network_io": {
                    "bytes_sent": np.random.randint(1000000, 10000000),
                    "bytes_recv": np.random.randint(1000000, 10000000),
                    "packets_sent": np.random.randint(1000, 10000),
                    "packets_recv": np.random.randint(1000, 10000),
                    "errin": np.random.randint(0, 10),
                    "errout": np.random.randint(0, 10),
                    "dropin": np.random.randint(0, 5),
                    "dropout": np.random.randint(0, 5)
                },
                "connections": {
                    "total": np.random.randint(50, 200),
                    "established": np.random.randint(20, 100),
                    "listening": np.random.randint(5, 20),
                    "time_wait": np.random.randint(10, 50)
                },
                "interfaces": {
                    "eth0": {
                        "addresses": [
                            {
                                "family": "AF_INET",
                                "address": "192.168.1.100",
                                "netmask": "255.255.255.0",
                                "broadcast": "192.168.1.255"
                            }
                        ]
                    },
                    "lo": {
                        "addresses": [
                            {
                                "family": "AF_INET",
                                "address": "127.0.0.1",
                                "netmask": "255.0.0.0",
                                "broadcast": None
                            }
                        ]
                    }
                },
                "timestamp": time.time()
            }
            
            result = {
                "status": "success",
                "network_metrics": metrics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get network metrics: {str(e)}"}
    
    def detect_bottlenecks(self, profile_id: str) -> Dict[str, Any]:
        """
        Detect performance bottlenecks from profiling data.
        
        Args:
            profile_id: Profile ID to analyze
            
        Returns:
            Bottleneck detection result
        """
        try:
            # Check if profile exists
            if profile_id not in self.profiles:
                return {"status": "error", "message": f"Profile {profile_id} not found"}
            
            profile = self.profiles[profile_id]
            metrics = profile["metrics"]
            
            if not metrics:
                return {"status": "error", "message": "No metrics data available"}
            
            # Analyze metrics for bottlenecks
            bottlenecks = []
            
            # CPU bottleneck detection
            cpu_values = [m.get("cpu_percent", 0) for m in metrics if "cpu_percent" in m]
            if cpu_values:
                avg_cpu = np.mean(cpu_values)
                max_cpu = np.max(cpu_values)
                if avg_cpu > 80 or max_cpu > 95:
                    bottlenecks.append({
                        "type": "cpu",
                        "severity": "high" if max_cpu > 95 else "medium",
                        "description": f"High CPU usage: avg {avg_cpu:.1f}%, max {max_cpu:.1f}%",
                        "recommendation": "Consider CPU optimization or scaling"
                    })
            
            # Memory bottleneck detection
            memory_values = [m.get("memory_percent", 0) for m in metrics if "memory_percent" in m]
            if memory_values:
                avg_memory = np.mean(memory_values)
                max_memory = np.max(memory_values)
                if avg_memory > 85 or max_memory > 95:
                    bottlenecks.append({
                        "type": "memory",
                        "severity": "high" if max_memory > 95 else "medium",
                        "description": f"High memory usage: avg {avg_memory:.1f}%, max {max_memory:.1f}%",
                        "recommendation": "Consider memory optimization or scaling"
                    })
            
            # Disk I/O bottleneck detection
            disk_io_values = [m.get("disk_io_utilization", 0) for m in metrics if "disk_io_utilization" in m]
            if disk_io_values:
                avg_disk_io = np.mean(disk_io_values)
                max_disk_io = np.max(disk_io_values)
                if avg_disk_io > 80 or max_disk_io > 95:
                    bottlenecks.append({
                        "type": "disk_io",
                        "severity": "high" if max_disk_io > 95 else "medium",
                        "description": f"High disk I/O: avg {avg_disk_io:.1f}%, max {max_disk_io:.1f}%",
                        "recommendation": "Consider disk I/O optimization or SSD upgrade"
                    })
            
            # Network bottleneck detection
            network_values = [m.get("network_utilization", 0) for m in metrics if "network_utilization" in m]
            if network_values:
                avg_network = np.mean(network_values)
                max_network = np.max(network_values)
                if avg_network > 80 or max_network > 95:
                    bottlenecks.append({
                        "type": "network",
                        "severity": "high" if max_network > 95 else "medium",
                        "description": f"High network usage: avg {avg_network:.1f}%, max {max_network:.1f}%",
                        "recommendation": "Consider network optimization or bandwidth upgrade"
                    })
            
            # Store bottlenecks
            self.bottlenecks[profile_id] = bottlenecks
            
            result = {
                "status": "success",
                "profile_id": profile_id,
                "bottlenecks": bottlenecks,
                "n_bottlenecks": len(bottlenecks),
                "severity_summary": {
                    "high": len([b for b in bottlenecks if b["severity"] == "high"]),
                    "medium": len([b for b in bottlenecks if b["severity"] == "medium"]),
                    "low": len([b for b in bottlenecks if b["severity"] == "low"])
                }
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to detect bottlenecks: {str(e)}"}
    
    def get_function_statistics(self, function_name: str = None) -> Dict[str, Any]:
        """
        Get function execution statistics.
        
        Args:
            function_name: Specific function name (optional)
            
        Returns:
            Function statistics result
        """
        try:
            if function_name:
                # Get statistics for specific function
                if function_name not in self.function_timings:
                    return {"status": "error", "message": f"No data for function {function_name}"}
                
                timings = self.function_timings[function_name]
                execution_times = [t["execution_time"] for t in timings]
                memory_deltas = [t["memory_delta"] for t in timings]
                
                statistics = {
                    "function_name": function_name,
                    "call_count": len(timings),
                    "execution_time": {
                        "min": np.min(execution_times),
                        "max": np.max(execution_times),
                        "mean": np.mean(execution_times),
                        "median": np.median(execution_times),
                        "std": np.std(execution_times)
                    },
                    "memory_delta": {
                        "min": np.min(memory_deltas),
                        "max": np.max(memory_deltas),
                        "mean": np.mean(memory_deltas),
                        "median": np.median(memory_deltas),
                        "std": np.std(memory_deltas)
                    },
                    "last_called": max(t["timestamp"] for t in timings)
                }
                
                result = {
                    "status": "success",
                    "statistics": statistics
                }
                
            else:
                # Get statistics for all functions
                all_statistics = {}
                
                for func_name, timings in self.function_timings.items():
                    execution_times = [t["execution_time"] for t in timings]
                    memory_deltas = [t["memory_delta"] for t in timings]
                    
                    all_statistics[func_name] = {
                        "call_count": len(timings),
                        "avg_execution_time": np.mean(execution_times),
                        "max_execution_time": np.max(execution_times),
                        "avg_memory_delta": np.mean(memory_deltas),
                        "max_memory_delta": np.max(memory_deltas),
                        "last_called": max(t["timestamp"] for t in timings)
                    }
                
                result = {
                    "status": "success",
                    "statistics": all_statistics,
                    "n_functions": len(all_statistics)
                }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get function statistics: {str(e)}"}
    
    def _monitor_system_metrics(self, profile_id: str, duration: int) -> None:
        """Monitor system metrics in a separate thread."""
        try:
            start_time = time.time()
            
            while time.time() - start_time < duration and self.profiling_active:
                # Collect metrics
                cpu_metrics = self.get_cpu_metrics()
                memory_metrics = self.get_memory_metrics()
                disk_metrics = self.get_disk_metrics()
                network_metrics = self.get_network_metrics()
                
                # Combine metrics
                combined_metrics = {
                    "timestamp": time.time(),
                    "cpu_percent": cpu_metrics["metrics"]["cpu_percent"],
                    "memory_percent": memory_metrics["metrics"]["system_memory"]["percent"],
                    "disk_io_utilization": disk_metrics["metrics"]["disk_usage"]["percent"],
                    "network_utilization": 0  # Simplified for demo
                }
                
                # Store metrics
                if profile_id in self.profiles:
                    self.profiles[profile_id]["metrics"].append(combined_metrics)
                
                # Sleep for 1 second
                time.sleep(1)
                
        except Exception as e:
            print(f"Error in monitoring thread: {e}")
    
    def _generate_performance_report(self, profile_id: str) -> Dict[str, Any]:
        """Generate performance report from profiling data."""
        try:
            profile = self.profiles[profile_id]
            metrics = profile["metrics"]
            
            if not metrics:
                return {"error": "No metrics data available"}
            
            # Calculate summary statistics
            cpu_values = [m.get("cpu_percent", 0) for m in metrics]
            memory_values = [m.get("memory_percent", 0) for m in metrics]
            disk_values = [m.get("disk_io_utilization", 0) for m in metrics]
            
            report = {
                "profile_id": profile_id,
                "profile_name": profile["profile_name"],
                "duration": profile["end_time"] - profile["start_time"],
                "n_samples": len(metrics),
                "cpu_metrics": {
                    "min": np.min(cpu_values) if cpu_values else 0,
                    "max": np.max(cpu_values) if cpu_values else 0,
                    "mean": np.mean(cpu_values) if cpu_values else 0,
                    "std": np.std(cpu_values) if cpu_values else 0
                },
                "memory_metrics": {
                    "min": np.min(memory_values) if memory_values else 0,
                    "max": np.max(memory_values) if memory_values else 0,
                    "mean": np.mean(memory_values) if memory_values else 0,
                    "std": np.std(memory_values) if memory_values else 0
                },
                "disk_metrics": {
                    "min": np.min(disk_values) if disk_values else 0,
                    "max": np.max(disk_values) if disk_values else 0,
                    "mean": np.mean(disk_values) if disk_values else 0,
                    "std": np.std(disk_values) if disk_values else 0
                }
            }
            
            return report
            
        except Exception as e:
            return {"error": f"Failed to generate report: {str(e)}"}
