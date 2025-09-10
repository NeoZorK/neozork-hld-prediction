# -*- coding: utf-8 -*-
"""
Load Balancer for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive load balancing capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import threading
import random
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import warnings

class LoadBalancingAlgorithm(Enum):
    """Load balancing algorithm enumeration."""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    LEAST_RESPONSE_TIME = "least_response_time"
    IP_HASH = "ip_hash"
    RANDOM = "random"

class HealthCheckType(Enum):
    """Health check type enumeration."""
    HTTP = "http"
    HTTPS = "https"
    TCP = "tcp"
    CUSTOM = "custom"

class LoadBalancer:
    """
    Load balancer for distributing traffic across multiple instances.
    
    Features:
    - Multiple Load Balancing Algorithms
    - Health Checks
    - Session Persistence
    - SSL Termination
    - Traffic Monitoring
    - Failover Management
    """
    
    def __init__(self, algorithm: str = LoadBalancingAlgorithm.ROUND_ROBIN.value):
        """
        Initialize the Load Balancer.
        
        Args:
            algorithm: Load balancing algorithm to use
        """
        self.algorithm = algorithm
        self.backend_servers = {}
        self.health_checks = {}
        self.traffic_stats = {}
        self.session_persistence = {}
        self.ssl_certificates = {}
        self.is_running = False
        self.health_check_thread = None
        self.current_server_index = 0
        self.server_weights = {}
        self.server_connections = {}
        self.server_response_times = {}
    
    def add_backend_server(self, server_id: str, host: str, port: int, 
                          weight: int = 1, health_check_path: str = "/health") -> Dict[str, Any]:
        """
        Add a backend server to the load balancer.
        
        Args:
            server_id: Unique server identifier
            host: Server hostname or IP
            port: Server port
            weight: Server weight for weighted algorithms
            health_check_path: Health check endpoint path
            
        Returns:
            Server addition result
        """
        try:
            # Create server configuration
            server_config = {
                "server_id": server_id,
                "host": host,
                "port": port,
                "weight": weight,
                "health_check_path": health_check_path,
                "is_healthy": True,
                "is_enabled": True,
                "added_time": time.time(),
                "last_health_check": None,
                "response_time": 0.0,
                "active_connections": 0,
                "total_requests": 0,
                "failed_requests": 0
            }
            
            # Add server
            self.backend_servers[server_id] = server_config
            self.server_weights[server_id] = weight
            self.server_connections[server_id] = 0
            self.server_response_times[server_id] = []
            
            # Initialize traffic stats
            self.traffic_stats[server_id] = {
                "requests_per_second": 0,
                "bytes_sent": 0,
                "bytes_received": 0,
                "error_rate": 0.0,
                "avg_response_time": 0.0
            }
            
            result = {
                "status": "success",
                "server_id": server_id,
                "host": host,
                "port": port,
                "weight": weight,
                "health_check_path": health_check_path,
                "message": "Backend server added successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to add backend server: {str(e)}"}
    
    def remove_backend_server(self, server_id: str) -> Dict[str, Any]:
        """
        Remove a backend server from the load balancer.
        
        Args:
            server_id: Server ID to remove
            
        Returns:
            Server removal result
        """
        try:
            # Check if server exists
            if server_id not in self.backend_servers:
                return {"status": "error", "message": f"Server {server_id} not found"}
            
            # Remove server
            del self.backend_servers[server_id]
            del self.server_weights[server_id]
            del self.server_connections[server_id]
            del self.server_response_times[server_id]
            del self.traffic_stats[server_id]
            
            result = {
                "status": "success",
                "server_id": server_id,
                "message": "Backend server removed successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to remove backend server: {str(e)}"}
    
    def update_server_weight(self, server_id: str, weight: int) -> Dict[str, Any]:
        """
        Update server weight.
        
        Args:
            server_id: Server ID
            weight: New weight
            
        Returns:
            Weight update result
        """
        try:
            # Check if server exists
            if server_id not in self.backend_servers:
                return {"status": "error", "message": f"Server {server_id} not found"}
            
            # Update weight
            self.backend_servers[server_id]["weight"] = weight
            self.server_weights[server_id] = weight
            
            result = {
                "status": "success",
                "server_id": server_id,
                "old_weight": self.backend_servers[server_id]["weight"],
                "new_weight": weight,
                "message": "Server weight updated successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to update server weight: {str(e)}"}
    
    def get_next_server(self, client_ip: str = None, session_id: str = None) -> Dict[str, Any]:
        """
        Get the next server based on the load balancing algorithm.
        
        Args:
            client_ip: Client IP address
            session_id: Session ID for persistence
            
        Returns:
            Next server selection result
        """
        try:
            # Get healthy and enabled servers
            available_servers = [
                server_id for server_id, server in self.backend_servers.items()
                if server["is_healthy"] and server["is_enabled"]
            ]
            
            if not available_servers:
                return {"status": "error", "message": "No healthy servers available"}
            
            # Check session persistence
            if session_id and session_id in self.session_persistence:
                server_id = self.session_persistence[session_id]
                if server_id in available_servers:
                    return {
                        "status": "success",
                        "server_id": server_id,
                        "host": self.backend_servers[server_id]["host"],
                        "port": self.backend_servers[server_id]["port"],
                        "algorithm": self.algorithm,
                        "reason": "session_persistence"
                    }
            
            # Select server based on algorithm
            if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN.value:
                server_id = self._round_robin_selection(available_servers)
            elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS.value:
                server_id = self._least_connections_selection(available_servers)
            elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN.value:
                server_id = self._weighted_round_robin_selection(available_servers)
            elif self.algorithm == LoadBalancingAlgorithm.LEAST_RESPONSE_TIME.value:
                server_id = self._least_response_time_selection(available_servers)
            elif self.algorithm == LoadBalancingAlgorithm.IP_HASH.value:
                server_id = self._ip_hash_selection(available_servers, client_ip)
            elif self.algorithm == LoadBalancingAlgorithm.RANDOM.value:
                server_id = self._random_selection(available_servers)
            else:
                server_id = self._round_robin_selection(available_servers)
            
            # Update server statistics
            self.backend_servers[server_id]["total_requests"] += 1
            self.server_connections[server_id] += 1
            
            # Set session persistence if session_id provided
            if session_id:
                self.session_persistence[session_id] = server_id
            
            result = {
                "status": "success",
                "server_id": server_id,
                "host": self.backend_servers[server_id]["host"],
                "port": self.backend_servers[server_id]["port"],
                "algorithm": self.algorithm,
                "reason": "algorithm_selection"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get next server: {str(e)}"}
    
    def start_health_checks(self, interval: int = 30) -> Dict[str, Any]:
        """
        Start health checks for backend servers.
        
        Args:
            interval: Health check interval in seconds
            
        Returns:
            Health check start result
        """
        try:
            if self.is_running:
                return {"status": "error", "message": "Health checks already running"}
            
            self.is_running = True
            self.health_check_thread = threading.Thread(
                target=self._health_check_loop,
                args=(interval,)
            )
            self.health_check_thread.daemon = True
            self.health_check_thread.start()
            
            result = {
                "status": "success",
                "interval": interval,
                "message": "Health checks started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start health checks: {str(e)}"}
    
    def stop_health_checks(self) -> Dict[str, Any]:
        """
        Stop health checks.
        
        Returns:
            Health check stop result
        """
        try:
            self.is_running = False
            
            if self.health_check_thread and self.health_check_thread.is_alive():
                self.health_check_thread.join(timeout=5)
            
            result = {
                "status": "success",
                "message": "Health checks stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop health checks: {str(e)}"}
    
    def get_load_balancer_status(self) -> Dict[str, Any]:
        """
        Get load balancer status.
        
        Returns:
            Load balancer status result
        """
        try:
            # Calculate statistics
            total_servers = len(self.backend_servers)
            healthy_servers = len([s for s in self.backend_servers.values() if s["is_healthy"]])
            enabled_servers = len([s for s in self.backend_servers.values() if s["is_enabled"]])
            total_requests = sum(s["total_requests"] for s in self.backend_servers.values())
            total_connections = sum(self.server_connections.values())
            
            # Calculate average response time
            all_response_times = []
            for server_id, response_times in self.server_response_times.items():
                all_response_times.extend(response_times)
            avg_response_time = np.mean(all_response_times) if all_response_times else 0.0
            
            status = {
                "algorithm": self.algorithm,
                "total_servers": total_servers,
                "healthy_servers": healthy_servers,
                "enabled_servers": enabled_servers,
                "total_requests": total_requests,
                "total_connections": total_connections,
                "avg_response_time": avg_response_time,
                "is_health_checks_running": self.is_running,
                "session_persistence_sessions": len(self.session_persistence)
            }
            
            result = {
                "status": "success",
                "status": status
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get load balancer status: {str(e)}"}
    
    def get_server_statistics(self, server_id: str = None) -> Dict[str, Any]:
        """
        Get server statistics.
        
        Args:
            server_id: Specific server ID (optional)
            
        Returns:
            Server statistics result
        """
        try:
            if server_id:
                # Get statistics for specific server
                if server_id not in self.backend_servers:
                    return {"status": "error", "message": f"Server {server_id} not found"}
                
                server = self.backend_servers[server_id]
                traffic_stats = self.traffic_stats[server_id]
                
                statistics = {
                    "server_id": server_id,
                    "host": server["host"],
                    "port": server["port"],
                    "weight": server["weight"],
                    "is_healthy": server["is_healthy"],
                    "is_enabled": server["is_enabled"],
                    "total_requests": server["total_requests"],
                    "failed_requests": server["failed_requests"],
                    "active_connections": server["active_connections"],
                    "response_time": server["response_time"],
                    "traffic_stats": traffic_stats,
                    "added_time": server["added_time"],
                    "last_health_check": server["last_health_check"]
                }
                
                result = {
                    "status": "success",
                    "statistics": statistics
                }
                
            else:
                # Get statistics for all servers
                all_statistics = {}
                
                for server_id, server in self.backend_servers.items():
                    traffic_stats = self.traffic_stats[server_id]
                    
                    all_statistics[server_id] = {
                        "host": server["host"],
                        "port": server["port"],
                        "weight": server["weight"],
                        "is_healthy": server["is_healthy"],
                        "is_enabled": server["is_enabled"],
                        "total_requests": server["total_requests"],
                        "failed_requests": server["failed_requests"],
                        "active_connections": server["active_connections"],
                        "response_time": server["response_time"],
                        "traffic_stats": traffic_stats
                    }
                
                result = {
                    "status": "success",
                    "statistics": all_statistics,
                    "n_servers": len(all_statistics)
                }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get server statistics: {str(e)}"}
    
    def _round_robin_selection(self, available_servers: List[str]) -> str:
        """Round robin server selection."""
        if not available_servers:
            return None
        
        server_id = available_servers[self.current_server_index % len(available_servers)]
        self.current_server_index += 1
        return server_id
    
    def _least_connections_selection(self, available_servers: List[str]) -> str:
        """Least connections server selection."""
        if not available_servers:
            return None
        
        return min(available_servers, key=lambda s: self.server_connections[s])
    
    def _weighted_round_robin_selection(self, available_servers: List[str]) -> str:
        """Weighted round robin server selection."""
        if not available_servers:
            return None
        
        # Simple weighted selection based on weights
        total_weight = sum(self.server_weights[s] for s in available_servers)
        if total_weight == 0:
            return available_servers[0]
        
        # Select server based on weight
        random_value = random.random() * total_weight
        current_weight = 0
        
        for server_id in available_servers:
            current_weight += self.server_weights[server_id]
            if random_value <= current_weight:
                return server_id
        
        return available_servers[0]
    
    def _least_response_time_selection(self, available_servers: List[str]) -> str:
        """Least response time server selection."""
        if not available_servers:
            return None
        
        return min(available_servers, key=lambda s: self.backend_servers[s]["response_time"])
    
    def _ip_hash_selection(self, available_servers: List[str], client_ip: str) -> str:
        """IP hash server selection."""
        if not available_servers or not client_ip:
            return available_servers[0] if available_servers else None
        
        # Simple hash-based selection
        hash_value = hash(client_ip) % len(available_servers)
        return available_servers[hash_value]
    
    def _random_selection(self, available_servers: List[str]) -> str:
        """Random server selection."""
        if not available_servers:
            return None
        
        return random.choice(available_servers)
    
    def _health_check_loop(self, interval: int) -> None:
        """Health check loop for monitoring server health."""
        try:
            while self.is_running:
                for server_id, server in self.backend_servers.items():
                    self._perform_health_check(server_id, server)
                
                time.sleep(interval)
                
        except Exception as e:
            print(f"Error in health check loop: {e}")
    
    def _perform_health_check(self, server_id: str, server: Dict[str, Any]) -> None:
        """Perform health check for a server."""
        try:
            # Simulate health check
            start_time = time.time()
            
            # Simulate response time
            response_time = random.uniform(0.01, 0.1)
            time.sleep(response_time)
            
            # Simulate health check result (90% success rate)
            is_healthy = random.random() > 0.1
            
            # Update server status
            server["is_healthy"] = is_healthy
            server["last_health_check"] = time.time()
            server["response_time"] = response_time
            
            # Update response time history
            self.server_response_times[server_id].append(response_time)
            if len(self.server_response_times[server_id]) > 100:
                self.server_response_times[server_id].pop(0)
            
            # Update traffic stats
            if not is_healthy:
                server["failed_requests"] += 1
            
        except Exception as e:
            print(f"Error in health check for server {server_id}: {e}")
