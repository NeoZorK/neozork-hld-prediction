"""
Scalable Infrastructure System
Microservices, load balancing, auto-scaling, distributed systems
"""

import asyncio
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    """Service status enumeration"""
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    SCALING = "scaling"

class LoadBalancerType(Enum):
    """Load balancer type enumeration"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    LEAST_RESPONSE_TIME = "least_response_time"

class ScalingPolicy(Enum):
    """Scaling policy enumeration"""
    CPU_BASED = "cpu_based"
    MEMORY_BASED = "memory_based"
    REQUEST_BASED = "request_based"
    CUSTOM_METRIC = "custom_metric"
    SCHEDULED = "scheduled"

@dataclass
class ServiceInstance:
    """Service instance definition"""
    instance_id: str
    service_name: str
    host: str
    port: int
    status: ServiceStatus
    cpu_usage: float
    memory_usage: float
    request_count: int
    response_time: float
    last_health_check: datetime
    created_at: datetime
    metadata: Dict[str, Any]

@dataclass
class ServiceDefinition:
    """Service definition"""
    service_name: str
    version: str
    replicas: int
    min_replicas: int
    max_replicas: int
    cpu_limit: float
    memory_limit: float
    scaling_policy: ScalingPolicy
    health_check_endpoint: str
    dependencies: List[str]
    environment_variables: Dict[str, str]
    created_at: datetime

@dataclass
class LoadBalancerConfig:
    """Load balancer configuration"""
    lb_type: LoadBalancerType
    health_check_interval: int
    health_check_timeout: int
    max_retries: int
    sticky_sessions: bool
    session_timeout: int

class HealthChecker:
    """Health check manager"""
    
    def __init__(self):
        self.health_checks = {}
        self.health_history = {}
        
    async def register_health_check(self, service_name: str, endpoint: str, 
                                  interval: int = 30, timeout: int = 5) -> bool:
        """Register health check for service"""
        self.health_checks[service_name] = {
            "endpoint": endpoint,
            "interval": interval,
            "timeout": timeout,
            "last_check": None,
            "status": "unknown"
        }
        
        logger.info(f"Registered health check for {service_name}")
        return True
    
    async def perform_health_check(self, service_name: str) -> Dict[str, Any]:
        """Perform health check for service"""
        if service_name not in self.health_checks:
            return {"status": "error", "message": "Service not registered"}
        
        health_config = self.health_checks[service_name]
        start_time = time.time()
        
        try:
            # Simulate health check (in real implementation, this would make HTTP request)
            await asyncio.sleep(0.1)  # Simulate network delay
            
            # Simulate health check result
            is_healthy = True  # In real implementation, this would check actual endpoint
            
            response_time = time.time() - start_time
            
            result = {
                "service_name": service_name,
                "status": "healthy" if is_healthy else "unhealthy",
                "response_time": response_time,
                "timestamp": datetime.now(),
                "endpoint": health_config["endpoint"]
            }
            
            # Update health history
            if service_name not in self.health_history:
                self.health_history[service_name] = []
            
            self.health_history[service_name].append(result)
            
            # Keep only last 100 health checks
            if len(self.health_history[service_name]) > 100:
                self.health_history[service_name] = self.health_history[service_name][-100:]
            
            return result
            
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {e}")
            return {
                "service_name": service_name,
                "status": "error",
                "response_time": time.time() - start_time,
                "timestamp": datetime.now(),
                "error": str(e)
            }
    
    async def run_continuous_health_checks(self):
        """Run continuous health checks for all registered services"""
        while True:
            tasks = []
            for service_name in self.health_checks.keys():
                task = self.perform_health_check(service_name)
                tasks.append(task)
            
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, dict) and result.get("status") == "error":
                        logger.warning(f"Health check error: {result}")
            
            # Wait for next check cycle
            await asyncio.sleep(30)  # Check every 30 seconds

class LoadBalancer:
    """Load balancer implementation"""
    
    def __init__(self, config: LoadBalancerConfig):
        self.config = config
        self.service_instances = {}
        self.current_index = {}
        self.connection_counts = {}
        self.response_times = {}
        
    async def add_service_instance(self, service_name: str, instance: ServiceInstance) -> bool:
        """Add service instance to load balancer"""
        if service_name not in self.service_instances:
            self.service_instances[service_name] = []
            self.current_index[service_name] = 0
            self.connection_counts[service_name] = {}
            self.response_times[service_name] = {}
        
        self.service_instances[service_name].append(instance)
        self.connection_counts[service_name][instance.instance_id] = 0
        self.response_times[service_name][instance.instance_id] = 0.0
        
        logger.info(f"Added instance {instance.instance_id} to service {service_name}")
        return True
    
    async def remove_service_instance(self, service_name: str, instance_id: str) -> bool:
        """Remove service instance from load balancer"""
        if service_name not in self.service_instances:
            return False
        
        # Remove instance from list
        self.service_instances[service_name] = [
            inst for inst in self.service_instances[service_name]
            if inst.instance_id != instance_id
        ]
        
        # Clean up tracking data
        if instance_id in self.connection_counts[service_name]:
            del self.connection_counts[service_name][instance_id]
        if instance_id in self.response_times[service_name]:
            del self.response_times[service_name][instance_id]
        
        logger.info(f"Removed instance {instance_id} from service {service_name}")
        return True
    
    async def select_instance(self, service_name: str, client_ip: str = None) -> Optional[ServiceInstance]:
        """Select service instance based on load balancing algorithm"""
        if service_name not in self.service_instances or not self.service_instances[service_name]:
            return None
        
        instances = self.service_instances[service_name]
        
        # Filter healthy instances
        healthy_instances = [
            inst for inst in instances
            if inst.status == ServiceStatus.RUNNING
        ]
        
        if not healthy_instances:
            return None
        
        # Apply load balancing algorithm
        if self.config.lb_type == LoadBalancerType.ROUND_ROBIN:
            return self._round_robin_selection(service_name, healthy_instances)
        elif self.config.lb_type == LoadBalancerType.LEAST_CONNECTIONS:
            return self._least_connections_selection(service_name, healthy_instances)
        elif self.config.lb_type == LoadBalancerType.LEAST_RESPONSE_TIME:
            return self._least_response_time_selection(service_name, healthy_instances)
        elif self.config.lb_type == LoadBalancerType.IP_HASH:
            return self._ip_hash_selection(service_name, healthy_instances, client_ip)
        else:
            return healthy_instances[0]  # Default to first instance
    
    def _round_robin_selection(self, service_name: str, instances: List[ServiceInstance]) -> ServiceInstance:
        """Round robin selection"""
        if service_name not in self.current_index:
            self.current_index[service_name] = 0
        
        selected = instances[self.current_index[service_name] % len(instances)]
        self.current_index[service_name] = (self.current_index[service_name] + 1) % len(instances)
        
        return selected
    
    def _least_connections_selection(self, service_name: str, instances: List[ServiceInstance]) -> ServiceInstance:
        """Least connections selection"""
        min_connections = float('inf')
        selected_instance = None
        
        for instance in instances:
            connections = self.connection_counts[service_name].get(instance.instance_id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_instance = instance
        
        return selected_instance
    
    def _least_response_time_selection(self, service_name: str, instances: List[ServiceInstance]) -> ServiceInstance:
        """Least response time selection"""
        min_response_time = float('inf')
        selected_instance = None
        
        for instance in instances:
            response_time = self.response_times[service_name].get(instance.instance_id, 0.0)
            if response_time < min_response_time:
                min_response_time = response_time
                selected_instance = instance
        
        return selected_instance
    
    def _ip_hash_selection(self, service_name: str, instances: List[ServiceInstance], client_ip: str) -> ServiceInstance:
        """IP hash selection for sticky sessions"""
        if not client_ip:
            return instances[0]
        
        hash_value = hash(client_ip) % len(instances)
        return instances[hash_value]
    
    async def route_request(self, service_name: str, request_data: Dict[str, Any], 
                          client_ip: str = None) -> Dict[str, Any]:
        """Route request to selected instance"""
        instance = await self.select_instance(service_name, client_ip)
        
        if not instance:
            return {
                "status": "error",
                "message": "No healthy instances available",
                "service_name": service_name
            }
        
        # Update connection count
        self.connection_counts[service_name][instance.instance_id] += 1
        
        # Simulate request processing
        start_time = time.time()
        try:
            # In real implementation, this would make actual HTTP request
            await asyncio.sleep(0.1)  # Simulate processing time
            
            response_time = time.time() - start_time
            self.response_times[service_name][instance.instance_id] = response_time
            
            return {
                "status": "success",
                "instance_id": instance.instance_id,
                "service_name": service_name,
                "response_time": response_time,
                "response_data": {"message": "Request processed successfully"}
            }
            
        except Exception as e:
            logger.error(f"Request failed for instance {instance.instance_id}: {e}")
            return {
                "status": "error",
                "instance_id": instance.instance_id,
                "service_name": service_name,
                "error": str(e)
            }
        finally:
            # Decrease connection count
            self.connection_counts[service_name][instance.instance_id] -= 1

class AutoScaler:
    """Auto-scaling manager"""
    
    def __init__(self):
        self.scaling_policies = {}
        self.scaling_history = {}
        self.metrics_collector = {}
        
    async def set_scaling_policy(self, service_name: str, policy: ScalingPolicy, 
                               config: Dict[str, Any]) -> bool:
        """Set scaling policy for service"""
        self.scaling_policies[service_name] = {
            "policy": policy,
            "config": config,
            "last_scaling": None
        }
        
        logger.info(f"Set scaling policy for {service_name}: {policy.value}")
        return True
    
    async def collect_metrics(self, service_name: str) -> Dict[str, Any]:
        """Collect metrics for service"""
        # Simulate metrics collection
        metrics = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "request_count": 100,  # Simulated
            "response_time": 0.5,  # Simulated
            "active_connections": 50,  # Simulated
            "timestamp": datetime.now()
        }
        
        self.metrics_collector[service_name] = metrics
        return metrics
    
    async def evaluate_scaling_decision(self, service_name: str) -> Dict[str, Any]:
        """Evaluate if service needs scaling"""
        if service_name not in self.scaling_policies:
            return {"action": "none", "reason": "No scaling policy set"}
        
        policy_config = self.scaling_policies[service_name]
        metrics = await self.collect_metrics(service_name)
        
        action = "none"
        reason = ""
        target_replicas = None
        
        if policy_config["policy"] == ScalingPolicy.CPU_BASED:
            cpu_threshold = policy_config["config"].get("cpu_threshold", 70.0)
            if metrics["cpu_usage"] > cpu_threshold:
                action = "scale_up"
                reason = f"CPU usage {metrics['cpu_usage']:.1f}% exceeds threshold {cpu_threshold}%"
            elif metrics["cpu_usage"] < cpu_threshold * 0.5:
                action = "scale_down"
                reason = f"CPU usage {metrics['cpu_usage']:.1f}% below threshold {cpu_threshold * 0.5}%"
        
        elif policy_config["policy"] == ScalingPolicy.MEMORY_BASED:
            memory_threshold = policy_config["config"].get("memory_threshold", 80.0)
            if metrics["memory_usage"] > memory_threshold:
                action = "scale_up"
                reason = f"Memory usage {metrics['memory_usage']:.1f}% exceeds threshold {memory_threshold}%"
            elif metrics["memory_usage"] < memory_threshold * 0.6:
                action = "scale_down"
                reason = f"Memory usage {metrics['memory_usage']:.1f}% below threshold {memory_threshold * 0.6}%"
        
        elif policy_config["policy"] == ScalingPolicy.REQUEST_BASED:
            request_threshold = policy_config["config"].get("request_threshold", 1000)
            if metrics["request_count"] > request_threshold:
                action = "scale_up"
                reason = f"Request count {metrics['request_count']} exceeds threshold {request_threshold}"
            elif metrics["request_count"] < request_threshold * 0.3:
                action = "scale_down"
                reason = f"Request count {metrics['request_count']} below threshold {request_threshold * 0.3}"
        
        # Calculate target replicas
        if action != "none":
            current_replicas = policy_config["config"].get("current_replicas", 1)
            min_replicas = policy_config["config"].get("min_replicas", 1)
            max_replicas = policy_config["config"].get("max_replicas", 10)
            
            if action == "scale_up":
                target_replicas = min(current_replicas + 1, max_replicas)
            elif action == "scale_down":
                target_replicas = max(current_replicas - 1, min_replicas)
        
        decision = {
            "service_name": service_name,
            "action": action,
            "reason": reason,
            "current_replicas": policy_config["config"].get("current_replicas", 1),
            "target_replicas": target_replicas,
            "metrics": metrics,
            "timestamp": datetime.now()
        }
        
        # Store scaling history
        if service_name not in self.scaling_history:
            self.scaling_history[service_name] = []
        
        self.scaling_history[service_name].append(decision)
        
        # Keep only last 50 scaling decisions
        if len(self.scaling_history[service_name]) > 50:
            self.scaling_history[service_name] = self.scaling_history[service_name][-50:]
        
        return decision
    
    async def execute_scaling(self, service_name: str, target_replicas: int) -> bool:
        """Execute scaling action"""
        logger.info(f"Scaling {service_name} to {target_replicas} replicas")
        
        # In real implementation, this would interact with container orchestration
        # For now, just simulate the scaling
        await asyncio.sleep(1)  # Simulate scaling time
        
        # Update current replicas in policy config
        if service_name in self.scaling_policies:
            self.scaling_policies[service_name]["config"]["current_replicas"] = target_replicas
            self.scaling_policies[service_name]["last_scaling"] = datetime.now()
        
        return True

class ServiceRegistry:
    """Service registry for service discovery"""
    
    def __init__(self):
        self.services = {}
        self.instances = {}
        self.service_dependencies = {}
        
    async def register_service(self, service: ServiceDefinition) -> bool:
        """Register service definition"""
        self.services[service.service_name] = service
        self.instances[service.service_name] = []
        
        logger.info(f"Registered service: {service.service_name}")
        return True
    
    async def register_instance(self, service_name: str, instance: ServiceInstance) -> bool:
        """Register service instance"""
        if service_name not in self.instances:
            self.instances[service_name] = []
        
        self.instances[service_name].append(instance)
        
        logger.info(f"Registered instance {instance.instance_id} for service {service_name}")
        return True
    
    async def discover_service(self, service_name: str) -> List[ServiceInstance]:
        """Discover service instances"""
        return self.instances.get(service_name, [])
    
    async def get_service_definition(self, service_name: str) -> Optional[ServiceDefinition]:
        """Get service definition"""
        return self.services.get(service_name)
    
    async def update_instance_status(self, instance_id: str, status: ServiceStatus) -> bool:
        """Update instance status"""
        for service_name, instances in self.instances.items():
            for instance in instances:
                if instance.instance_id == instance_id:
                    instance.status = status
                    instance.last_health_check = datetime.now()
                    logger.info(f"Updated status for instance {instance_id}: {status.value}")
                    return True
        
        return False

class DistributedSystemManager:
    """Main distributed system manager"""
    
    def __init__(self):
        self.service_registry = ServiceRegistry()
        self.load_balancer = LoadBalancer(LoadBalancerConfig(
            lb_type=LoadBalancerType.ROUND_ROBIN,
            health_check_interval=30,
            health_check_timeout=5,
            max_retries=3,
            sticky_sessions=False,
            session_timeout=300
        ))
        self.auto_scaler = AutoScaler()
        self.health_checker = HealthChecker()
        self.monitoring_data = {}
        
    async def initialize_system(self):
        """Initialize distributed system"""
        # Start health checker
        asyncio.create_task(self.health_checker.run_continuous_health_checks())
        
        # Start auto-scaling evaluation
        asyncio.create_task(self._run_auto_scaling_evaluation())
        
        logger.info("Distributed system initialized")
    
    async def deploy_service(self, service: ServiceDefinition) -> bool:
        """Deploy service to distributed system"""
        # Register service
        await self.service_registry.register_service(service)
        
        # Set up scaling policy
        scaling_config = {
            "current_replicas": service.replicas,
            "min_replicas": service.min_replicas,
            "max_replicas": service.max_replicas,
            "cpu_threshold": 70.0,
            "memory_threshold": 80.0
        }
        
        await self.auto_scaler.set_scaling_policy(service.service_name, service.scaling_policy, scaling_config)
        
        # Register health check
        await self.health_checker.register_health_check(service.service_name, service.health_check_endpoint)
        
        # Create initial instances
        for i in range(service.replicas):
            instance = ServiceInstance(
                instance_id=f"{service.service_name}-{i}",
                service_name=service.service_name,
                host="localhost",
                port=8000 + i,
                status=ServiceStatus.RUNNING,
                cpu_usage=0.0,
                memory_usage=0.0,
                request_count=0,
                response_time=0.0,
                last_health_check=datetime.now(),
                created_at=datetime.now(),
                metadata={}
            )
            
            await self.service_registry.register_instance(service.service_name, instance)
            await self.load_balancer.add_service_instance(service.service_name, instance)
        
        logger.info(f"Deployed service {service.service_name} with {service.replicas} replicas")
        return True
    
    async def route_request(self, service_name: str, request_data: Dict[str, Any], 
                          client_ip: str = None) -> Dict[str, Any]:
        """Route request through load balancer"""
        return await self.load_balancer.route_request(service_name, request_data, client_ip)
    
    async def _run_auto_scaling_evaluation(self):
        """Run continuous auto-scaling evaluation"""
        while True:
            try:
                for service_name in self.auto_scaler.scaling_policies.keys():
                    decision = await self.auto_scaler.evaluate_scaling_decision(service_name)
                    
                    if decision["action"] != "none" and decision["target_replicas"]:
                        await self.auto_scaler.execute_scaling(service_name, decision["target_replicas"])
                        logger.info(f"Auto-scaling decision for {service_name}: {decision['action']} to {decision['target_replicas']} replicas")
                
                await asyncio.sleep(60)  # Evaluate every minute
                
            except Exception as e:
                logger.error(f"Auto-scaling evaluation error: {e}")
                await asyncio.sleep(60)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        services_status = {}
        
        for service_name, instances in self.service_registry.instances.items():
            healthy_instances = [inst for inst in instances if inst.status == ServiceStatus.RUNNING]
            
            services_status[service_name] = {
                "total_instances": len(instances),
                "healthy_instances": len(healthy_instances),
                "status": "healthy" if len(healthy_instances) > 0 else "unhealthy",
                "avg_cpu_usage": sum(inst.cpu_usage for inst in instances) / len(instances) if instances else 0,
                "avg_memory_usage": sum(inst.memory_usage for inst in instances) / len(instances) if instances else 0
            }
        
        return {
            "timestamp": datetime.now(),
            "total_services": len(self.service_registry.services),
            "total_instances": sum(len(instances) for instances in self.service_registry.instances.values()),
            "services_status": services_status,
            "load_balancer_type": self.load_balancer.config.lb_type.value,
            "auto_scaling_policies": len(self.auto_scaler.scaling_policies)
        }
    
    async def get_service_metrics(self, service_name: str) -> Dict[str, Any]:
        """Get detailed metrics for service"""
        if service_name not in self.service_registry.instances:
            return {"error": "Service not found"}
        
        instances = self.service_registry.instances[service_name]
        service_def = await self.service_registry.get_service_definition(service_name)
        
        # Get health check history
        health_history = self.health_checker.health_history.get(service_name, [])
        
        # Get scaling history
        scaling_history = self.auto_scaler.scaling_history.get(service_name, [])
        
        # Get current metrics
        current_metrics = await self.auto_scaler.collect_metrics(service_name)
        
        return {
            "service_name": service_name,
            "service_definition": asdict(service_def) if service_def else None,
            "instances": [asdict(inst) for inst in instances],
            "current_metrics": current_metrics,
            "health_history": health_history[-10:],  # Last 10 health checks
            "scaling_history": scaling_history[-5:],  # Last 5 scaling decisions
            "timestamp": datetime.now()
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get system summary"""
        return {
            "total_services": len(self.service_registry.services),
            "total_instances": sum(len(instances) for instances in self.service_registry.instances.values()),
            "scaling_policies": len(self.auto_scaler.scaling_policies),
            "health_checks": len(self.health_checker.health_checks),
            "last_update": datetime.now()
        }

# Example usage and testing
async def main():
    """Example usage of DistributedSystemManager"""
    manager = DistributedSystemManager()
    
    # Initialize system
    await manager.initialize_system()
    
    # Deploy services
    trading_service = ServiceDefinition(
        service_name="trading-service",
        version="1.0.0",
        replicas=3,
        min_replicas=2,
        max_replicas=10,
        cpu_limit=1.0,
        memory_limit=512,
        scaling_policy=ScalingPolicy.CPU_BASED,
        health_check_endpoint="/health",
        dependencies=[],
        environment_variables={"ENV": "production"},
        created_at=datetime.now()
    )
    
    data_service = ServiceDefinition(
        service_name="data-service",
        version="1.0.0",
        replicas=2,
        min_replicas=1,
        max_replicas=5,
        cpu_limit=0.5,
        memory_limit=256,
        scaling_policy=ScalingPolicy.MEMORY_BASED,
        health_check_endpoint="/health",
        dependencies=[],
        environment_variables={"ENV": "production"},
        created_at=datetime.now()
    )
    
    await manager.deploy_service(trading_service)
    await manager.deploy_service(data_service)
    
    # Route some requests
    for i in range(5):
        request_data = {"request_id": f"req-{i}", "data": f"test-data-{i}"}
        response = await manager.route_request("trading-service", request_data, f"192.168.1.{i}")
        print(f"Request {i}: {response['status']} - Instance: {response.get('instance_id', 'N/A')}")
    
    # Get system status
    status = await manager.get_system_status()
    print(f"System Status: {status['total_services']} services, {status['total_instances']} instances")
    
    # Get service metrics
    metrics = await manager.get_service_metrics("trading-service")
    print(f"Trading Service Metrics: {len(metrics['instances'])} instances")
    
    # System summary
    summary = manager.get_summary()
    print(f"System Summary: {summary}")

if __name__ == "__main__":
    asyncio.run(main())
