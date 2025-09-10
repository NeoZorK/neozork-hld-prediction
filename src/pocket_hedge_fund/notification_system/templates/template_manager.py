"""
Template Manager for notification system.

This module provides template management functionality for notifications.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TemplateManager:
    """Manages notification templates."""
    
    def __init__(self):
        """Initialize template manager."""
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.logger = logger
    
    def register_template(self, template_id: str, template_data: Dict[str, Any]) -> bool:
        """Register a new template."""
        try:
            self.templates[template_id] = template_data
            self.logger.info(f"Template {template_id} registered successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register template {template_id}: {e}")
            return False
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get a template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self) -> Dict[str, Dict[str, Any]]:
        """List all registered templates."""
        return self.templates.copy()
    
    def remove_template(self, template_id: str) -> bool:
        """Remove a template."""
        try:
            if template_id in self.templates:
                del self.templates[template_id]
                self.logger.info(f"Template {template_id} removed successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove template {template_id}: {e}")
            return False
    
    def render_template(self, template_id: str, context: Dict[str, Any]) -> Optional[str]:
        """Render a template with context."""
        template = self.get_template(template_id)
        if not template:
            self.logger.warning(f"Template {template_id} not found")
            return None
        
        try:
            # Simple template rendering - replace placeholders
            content = template.get('content', '')
            for key, value in context.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))
            return content
        except Exception as e:
            self.logger.error(f"Failed to render template {template_id}: {e}")
            return None
