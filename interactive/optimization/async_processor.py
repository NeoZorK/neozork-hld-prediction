# -*- coding: utf-8 -*-
"""
Async Processor for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive asynchronous processing capabilities.
"""

import pandas as pd
import numpy as np
import time
import json
import asyncio
import threading
import concurrent.futures
from typing import Dict, Any, Optional, List, Tuple, Callable, Coroutine
from enum import Enum
import warnings

class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AsyncProcessor:
    """
    Async processor for concurrent task execution and optimization.
    
    Features:
    - Asynchronous Task Execution
    - Task Queue Management
    - Priority-based Scheduling
    - Parallel Processing
    - Task Monitoring
    - Resource Management
    - Error Handling
    """
    
    def __init__(self, max_workers: int = 4, max_queue_size: int = 1000):
        """
        Initialize the Async Processor.
        
        Args:
            max_workers: Maximum number of worker threads
            max_queue_size: Maximum queue size
        """
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.task_queue = []
        self.running_tasks = {}
        self.completed_tasks = {}
        self.failed_tasks = {}
        self.task_counter = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self.loop = None
        self.is_running = False
        self.worker_thread = None
        self.task_stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "cancelled_tasks": 0,
            "avg_execution_time": 0
        }
    
    def start_processor(self) -> Dict[str, Any]:
        """
        Start the async processor.
        
        Returns:
            Processor start result
        """
        try:
            if self.is_running:
                return {"status": "error", "message": "Processor is already running"}
            
            # Start worker thread
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._worker_loop)
            self.worker_thread.daemon = True
            self.worker_thread.start()
            
            result = {
                "status": "success",
                "max_workers": self.max_workers,
                "max_queue_size": self.max_queue_size,
                "message": "Async processor started successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to start processor: {str(e)}"}
    
    def stop_processor(self) -> Dict[str, Any]:
        """
        Stop the async processor.
        
        Returns:
            Processor stop result
        """
        try:
            if not self.is_running:
                return {"status": "error", "message": "Processor is not running"}
            
            # Stop processor
            self.is_running = False
            
            # Wait for worker thread to finish
            if self.worker_thread and self.worker_thread.is_alive():
                self.worker_thread.join(timeout=5)
            
            # Shutdown executor
            self.executor.shutdown(wait=True)
            
            result = {
                "status": "success",
                "message": "Async processor stopped successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to stop processor: {str(e)}"}
    
    def submit_task(self, func: Callable, *args, priority: str = TaskPriority.NORMAL.value, 
                   timeout: int = None, **kwargs) -> Dict[str, Any]:
        """
        Submit a task for execution.
        
        Args:
            func: Function to execute
            *args: Function arguments
            priority: Task priority
            timeout: Task timeout in seconds
            **kwargs: Function keyword arguments
            
        Returns:
            Task submission result
        """
        try:
            # Check queue size
            if len(self.task_queue) >= self.max_queue_size:
                return {"status": "error", "message": "Task queue is full"}
            
            # Generate task ID
            self.task_counter += 1
            task_id = f"task_{self.task_counter}"
            
            # Create task
            task = {
                "task_id": task_id,
                "function": func,
                "args": args,
                "kwargs": kwargs,
                "priority": priority,
                "timeout": timeout,
                "status": TaskStatus.PENDING.value,
                "created_time": time.time(),
                "started_time": None,
                "completed_time": None,
                "result": None,
                "error": None
            }
            
            # Add to queue
            self.task_queue.append(task)
            
            # Sort queue by priority
            priority_order = {
                TaskPriority.CRITICAL.value: 0,
                TaskPriority.HIGH.value: 1,
                TaskPriority.NORMAL.value: 2,
                TaskPriority.LOW.value: 3
            }
            self.task_queue.sort(key=lambda t: priority_order.get(t["priority"], 2))
            
            # Update statistics
            self.task_stats["total_tasks"] += 1
            
            result = {
                "status": "success",
                "task_id": task_id,
                "priority": priority,
                "queue_position": len(self.task_queue),
                "message": "Task submitted successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to submit task: {str(e)}"}
    
    def submit_async_task(self, coro: Coroutine, priority: str = TaskPriority.NORMAL.value, 
                         timeout: int = None) -> Dict[str, Any]:
        """
        Submit an async coroutine for execution.
        
        Args:
            coro: Coroutine to execute
            priority: Task priority
            timeout: Task timeout in seconds
            
        Returns:
            Async task submission result
        """
        try:
            # Check queue size
            if len(self.task_queue) >= self.max_queue_size:
                return {"status": "error", "message": "Task queue is full"}
            
            # Generate task ID
            self.task_counter += 1
            task_id = f"async_task_{self.task_counter}"
            
            # Create async task
            task = {
                "task_id": task_id,
                "coroutine": coro,
                "priority": priority,
                "timeout": timeout,
                "status": TaskStatus.PENDING.value,
                "created_time": time.time(),
                "started_time": None,
                "completed_time": None,
                "result": None,
                "error": None,
                "is_async": True
            }
            
            # Add to queue
            self.task_queue.append(task)
            
            # Sort queue by priority
            priority_order = {
                TaskPriority.CRITICAL.value: 0,
                TaskPriority.HIGH.value: 1,
                TaskPriority.NORMAL.value: 2,
                TaskPriority.LOW.value: 3
            }
            self.task_queue.sort(key=lambda t: priority_order.get(t["priority"], 2))
            
            # Update statistics
            self.task_stats["total_tasks"] += 1
            
            result = {
                "status": "success",
                "task_id": task_id,
                "priority": priority,
                "queue_position": len(self.task_queue),
                "message": "Async task submitted successfully"
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to submit async task: {str(e)}"}
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get task status.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task status result
        """
        try:
            # Check running tasks
            if task_id in self.running_tasks:
                task = self.running_tasks[task_id]
                return {
                    "status": "success",
                    "task_id": task_id,
                    "task_status": task["status"],
                    "created_time": task["created_time"],
                    "started_time": task["started_time"],
                    "message": "Task is running"
                }
            
            # Check completed tasks
            if task_id in self.completed_tasks:
                task = self.completed_tasks[task_id]
                return {
                    "status": "success",
                    "task_id": task_id,
                    "task_status": task["status"],
                    "created_time": task["created_time"],
                    "started_time": task["started_time"],
                    "completed_time": task["completed_time"],
                    "execution_time": task["completed_time"] - task["started_time"],
                    "result": task["result"],
                    "message": "Task completed successfully"
                }
            
            # Check failed tasks
            if task_id in self.failed_tasks:
                task = self.failed_tasks[task_id]
                return {
                    "status": "success",
                    "task_id": task_id,
                    "task_status": task["status"],
                    "created_time": task["created_time"],
                    "started_time": task["started_time"],
                    "completed_time": task["completed_time"],
                    "error": task["error"],
                    "message": "Task failed"
                }
            
            # Check pending tasks
            for task in self.task_queue:
                if task["task_id"] == task_id:
                    return {
                        "status": "success",
                        "task_id": task_id,
                        "task_status": task["status"],
                        "created_time": task["created_time"],
                        "queue_position": self.task_queue.index(task) + 1,
                        "message": "Task is pending"
                    }
            
            return {"status": "error", "message": f"Task {task_id} not found"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get task status: {str(e)}"}
    
    def cancel_task(self, task_id: str) -> Dict[str, Any]:
        """
        Cancel a task.
        
        Args:
            task_id: Task ID to cancel
            
        Returns:
            Task cancellation result
        """
        try:
            # Check if task is running
            if task_id in self.running_tasks:
                task = self.running_tasks[task_id]
                task["status"] = TaskStatus.CANCELLED.value
                task["completed_time"] = time.time()
                
                # Move to completed tasks
                self.completed_tasks[task_id] = task
                del self.running_tasks[task_id]
                
                # Update statistics
                self.task_stats["cancelled_tasks"] += 1
                
                return {
                    "status": "success",
                    "task_id": task_id,
                    "message": "Running task cancelled"
                }
            
            # Check if task is pending
            for i, task in enumerate(self.task_queue):
                if task["task_id"] == task_id:
                    task["status"] = TaskStatus.CANCELLED.value
                    task["completed_time"] = time.time()
                    
                    # Move to completed tasks
                    self.completed_tasks[task_id] = task
                    del self.task_queue[i]
                    
                    # Update statistics
                    self.task_stats["cancelled_tasks"] += 1
                    
                    return {
                        "status": "success",
                        "task_id": task_id,
                        "message": "Pending task cancelled"
                    }
            
            return {"status": "error", "message": f"Task {task_id} not found or already completed"}
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to cancel task: {str(e)}"}
    
    def get_processor_statistics(self) -> Dict[str, Any]:
        """
        Get processor statistics.
        
        Returns:
            Processor statistics result
        """
        try:
            # Calculate average execution time
            completed_tasks = list(self.completed_tasks.values())
            if completed_tasks:
                execution_times = [
                    task["completed_time"] - task["started_time"]
                    for task in completed_tasks
                    if task["started_time"] and task["completed_time"]
                ]
                avg_execution_time = np.mean(execution_times) if execution_times else 0
            else:
                avg_execution_time = 0
            
            statistics = {
                "is_running": self.is_running,
                "max_workers": self.max_workers,
                "max_queue_size": self.max_queue_size,
                "queue_size": len(self.task_queue),
                "running_tasks": len(self.running_tasks),
                "completed_tasks": len(self.completed_tasks),
                "failed_tasks": len(self.failed_tasks),
                "total_tasks": self.task_stats["total_tasks"],
                "avg_execution_time": avg_execution_time,
                "queue_utilization": (len(self.task_queue) / self.max_queue_size * 100) if self.max_queue_size > 0 else 0,
                "worker_utilization": (len(self.running_tasks) / self.max_workers * 100) if self.max_workers > 0 else 0
            }
            
            result = {
                "status": "success",
                "statistics": statistics
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to get processor statistics: {str(e)}"}
    
    def parallel_execute(self, functions: List[Callable], max_workers: int = None) -> Dict[str, Any]:
        """
        Execute multiple functions in parallel.
        
        Args:
            functions: List of functions to execute
            max_workers: Maximum number of workers
            
        Returns:
            Parallel execution result
        """
        try:
            if max_workers is None:
                max_workers = min(len(functions), self.max_workers)
            
            # Execute functions in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(func) for func in functions]
                results = []
                
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        results.append({"status": "success", "result": result})
                    except Exception as e:
                        results.append({"status": "error", "error": str(e)})
            
            result = {
                "status": "success",
                "results": results,
                "n_functions": len(functions),
                "n_successful": len([r for r in results if r["status"] == "success"]),
                "n_failed": len([r for r in results if r["status"] == "error"]),
                "max_workers": max_workers
            }
            
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Failed to execute functions in parallel: {str(e)}"}
    
    def _worker_loop(self) -> None:
        """Worker loop for processing tasks."""
        try:
            while self.is_running:
                # Process tasks from queue
                if self.task_queue and len(self.running_tasks) < self.max_workers:
                    task = self.task_queue.pop(0)
                    self._execute_task(task)
                
                # Sleep briefly to prevent busy waiting
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error in worker loop: {e}")
    
    def _execute_task(self, task: Dict[str, Any]) -> None:
        """Execute a single task."""
        try:
            task_id = task["task_id"]
            task["status"] = TaskStatus.RUNNING.value
            task["started_time"] = time.time()
            
            # Add to running tasks
            self.running_tasks[task_id] = task
            
            # Execute task
            if task.get("is_async", False):
                # Async task
                result = asyncio.run(task["coroutine"])
            else:
                # Regular task
                result = task["function"](*task["args"], **task["kwargs"])
            
            # Task completed successfully
            task["status"] = TaskStatus.COMPLETED.value
            task["completed_time"] = time.time()
            task["result"] = result
            
            # Move to completed tasks
            self.completed_tasks[task_id] = task
            del self.running_tasks[task_id]
            
            # Update statistics
            self.task_stats["completed_tasks"] += 1
            
        except Exception as e:
            # Task failed
            task["status"] = TaskStatus.FAILED.value
            task["completed_time"] = time.time()
            task["error"] = str(e)
            
            # Move to failed tasks
            self.failed_tasks[task_id] = task
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            # Update statistics
            self.task_stats["failed_tasks"] += 1
