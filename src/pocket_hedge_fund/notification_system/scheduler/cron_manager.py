"""
Cron Manager for notification system.

This module provides cron job management functionality for scheduled notifications.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
import asyncio
import logging
import re

logger = logging.getLogger(__name__)


class CronManager:
    """Manages cron jobs for scheduled notifications."""
    
    def __init__(self):
        """Initialize cron manager."""
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.running = False
        self.logger = logger
        self._task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the cron manager."""
        if self.running:
            return
        
        self.running = True
        self._task = asyncio.create_task(self._run_scheduler())
        self.logger.info("Cron manager started")
    
    async def stop(self):
        """Stop the cron manager."""
        if not self.running:
            return
        
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self.logger.info("Cron manager stopped")
    
    def add_job(self, job_id: str, cron_expression: str, callback: Callable, **kwargs) -> bool:
        """Add a cron job."""
        try:
            if not self._validate_cron_expression(cron_expression):
                self.logger.error(f"Invalid cron expression: {cron_expression}")
                return False
            
            self.jobs[job_id] = {
                'cron_expression': cron_expression,
                'callback': callback,
                'kwargs': kwargs,
                'next_run': self._calculate_next_run(cron_expression),
                'created_at': datetime.now()
            }
            
            self.logger.info(f"Cron job {job_id} added successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add cron job {job_id}: {e}")
            return False
    
    def remove_job(self, job_id: str) -> bool:
        """Remove a cron job."""
        try:
            if job_id in self.jobs:
                del self.jobs[job_id]
                self.logger.info(f"Cron job {job_id} removed successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove cron job {job_id}: {e}")
            return False
    
    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a cron job by ID."""
        return self.jobs.get(job_id)
    
    def list_jobs(self) -> Dict[str, Dict[str, Any]]:
        """List all cron jobs."""
        return self.jobs.copy()
    
    def _validate_cron_expression(self, cron_expression: str) -> bool:
        """Validate cron expression format."""
        # Simple validation - check if it has 5 parts
        parts = cron_expression.strip().split()
        if len(parts) != 5:
            return False
        
        # Basic format validation
        cron_pattern = r'^(\*|[0-5]?\d) (\*|[01]?\d|2[0-3]) (\*|[012]?\d|3[01]) (\*|[01]?\d) (\*|[0-6])$'
        return bool(re.match(cron_pattern, cron_expression))
    
    def _calculate_next_run(self, cron_expression: str) -> datetime:
        """Calculate next run time for cron expression."""
        # Simplified implementation - just return current time + 1 minute
        # In a real implementation, this would parse the cron expression
        return datetime.now() + timedelta(minutes=1)
    
    async def _run_scheduler(self):
        """Run the cron scheduler."""
        while self.running:
            try:
                current_time = datetime.now()
                
                for job_id, job_data in self.jobs.items():
                    if current_time >= job_data['next_run']:
                        try:
                            # Execute the job
                            if asyncio.iscoroutinefunction(job_data['callback']):
                                await job_data['callback'](**job_data['kwargs'])
                            else:
                                job_data['callback'](**job_data['kwargs'])
                            
                            # Update next run time
                            job_data['next_run'] = self._calculate_next_run(job_data['cron_expression'])
                            
                            self.logger.info(f"Cron job {job_id} executed successfully")
                        except Exception as e:
                            self.logger.error(f"Failed to execute cron job {job_id}: {e}")
                
                # Sleep for 1 minute before next check
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cron scheduler: {e}")
                await asyncio.sleep(60)
