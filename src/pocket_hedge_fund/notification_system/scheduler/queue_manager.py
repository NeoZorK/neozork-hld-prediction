"""
Queue Manager for notification system.

This module provides queue management functionality for notification processing.
"""

from typing import Dict, Any, List, Optional
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class QueueManager:
    """Manages notification queues."""
    
    def __init__(self, max_size: int = 10000):
        """Initialize queue manager."""
        self.max_size = max_size
        self.queues: Dict[str, asyncio.Queue] = {}
        self.logger = logger
        self.stats = {
            'total_processed': 0,
            'total_failed': 0,
            'queue_sizes': {}
        }
    
    def create_queue(self, queue_name: str) -> bool:
        """Create a new queue."""
        try:
            if queue_name not in self.queues:
                self.queues[queue_name] = asyncio.Queue(maxsize=self.max_size)
                self.stats['queue_sizes'][queue_name] = 0
                self.logger.info(f"Queue {queue_name} created successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to create queue {queue_name}: {e}")
            return False
    
    def get_queue(self, queue_name: str) -> Optional[asyncio.Queue]:
        """Get a queue by name."""
        return self.queues.get(queue_name)
    
    async def enqueue(self, queue_name: str, item: Any) -> bool:
        """Add an item to a queue."""
        try:
            if queue_name not in self.queues:
                self.create_queue(queue_name)
            
            queue = self.queues[queue_name]
            await queue.put(item)
            self.stats['queue_sizes'][queue_name] = queue.qsize()
            self.logger.debug(f"Item enqueued to {queue_name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enqueue item to {queue_name}: {e}")
            return False
    
    async def dequeue(self, queue_name: str) -> Optional[Any]:
        """Remove an item from a queue."""
        try:
            if queue_name not in self.queues:
                return None
            
            queue = self.queues[queue_name]
            item = await queue.get()
            self.stats['queue_sizes'][queue_name] = queue.qsize()
            self.logger.debug(f"Item dequeued from {queue_name}")
            return item
        except Exception as e:
            self.logger.error(f"Failed to dequeue item from {queue_name}: {e}")
            return None
    
    def get_queue_size(self, queue_name: str) -> int:
        """Get the size of a queue."""
        if queue_name in self.queues:
            return self.queues[queue_name].qsize()
        return 0
    
    def get_all_queue_sizes(self) -> Dict[str, int]:
        """Get sizes of all queues."""
        return {name: queue.qsize() for name, queue in self.queues.items()}
    
    def list_queues(self) -> List[str]:
        """List all queue names."""
        return list(self.queues.keys())
    
    def remove_queue(self, queue_name: str) -> bool:
        """Remove a queue."""
        try:
            if queue_name in self.queues:
                del self.queues[queue_name]
                if queue_name in self.stats['queue_sizes']:
                    del self.stats['queue_sizes'][queue_name]
                self.logger.info(f"Queue {queue_name} removed successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove queue {queue_name}: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get queue manager statistics."""
        return {
            'total_queues': len(self.queues),
            'queue_sizes': self.get_all_queue_sizes(),
            'total_processed': self.stats['total_processed'],
            'total_failed': self.stats['total_failed']
        }
    
    def increment_processed(self):
        """Increment processed counter."""
        self.stats['total_processed'] += 1
    
    def increment_failed(self):
        """Increment failed counter."""
        self.stats['total_failed'] += 1
    
    async def clear_queue(self, queue_name: str) -> bool:
        """Clear all items from a queue."""
        try:
            if queue_name not in self.queues:
                return False
            
            queue = self.queues[queue_name]
            # Clear the queue by getting all items
            while not queue.empty():
                try:
                    await queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
            
            self.stats['queue_sizes'][queue_name] = 0
            self.logger.info(f"Queue {queue_name} cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear queue {queue_name}: {e}")
            return False
