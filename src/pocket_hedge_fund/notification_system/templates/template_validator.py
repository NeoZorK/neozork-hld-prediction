"""
Template Validator for notification system.

This module provides template validation functionality for notifications.
"""

from typing import Dict, Any, List, Optional
import re
import logging

logger = logging.getLogger(__name__)


class TemplateValidator:
    """Validates notification templates."""
    
    def __init__(self):
        """Initialize template validator."""
        self.logger = logger
        self.required_fields = ['content', 'subject']
        self.allowed_placeholders = r'\{\{[^}]+\}\}'
    
    def validate_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a template."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check required fields
        for field in self.required_fields:
            if field not in template_data:
                result['errors'].append(f"Missing required field: {field}")
                result['is_valid'] = False
        
        # Validate content if present
        if 'content' in template_data:
            content_validation = self._validate_content(template_data['content'])
            result['errors'].extend(content_validation['errors'])
            result['warnings'].extend(content_validation['warnings'])
            if content_validation['errors']:
                result['is_valid'] = False
        
        # Validate subject if present
        if 'subject' in template_data:
            subject_validation = self._validate_subject(template_data['subject'])
            result['errors'].extend(subject_validation['errors'])
            result['warnings'].extend(subject_validation['warnings'])
            if subject_validation['errors']:
                result['is_valid'] = False
        
        return result
    
    def _validate_content(self, content: str) -> Dict[str, List[str]]:
        """Validate template content."""
        result = {'errors': [], 'warnings': []}
        
        if not content or not content.strip():
            result['errors'].append("Content cannot be empty")
            return result
        
        # Check for valid placeholders
        placeholders = re.findall(self.allowed_placeholders, content)
        for placeholder in placeholders:
            if not self._is_valid_placeholder(placeholder):
                result['warnings'].append(f"Potentially invalid placeholder: {placeholder}")
        
        return result
    
    def _validate_subject(self, subject: str) -> Dict[str, List[str]]:
        """Validate template subject."""
        result = {'errors': [], 'warnings': []}
        
        if not subject or not subject.strip():
            result['errors'].append("Subject cannot be empty")
            return result
        
        if len(subject) > 200:
            result['warnings'].append("Subject is quite long (>200 characters)")
        
        return result
    
    def _is_valid_placeholder(self, placeholder: str) -> bool:
        """Check if placeholder is valid."""
        # Remove {{ and }}
        inner = placeholder[2:-2].strip()
        
        # Check if it's a valid identifier
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', inner):
            return False
        
        return True
    
    def extract_placeholders(self, content: str) -> List[str]:
        """Extract all placeholders from content."""
        placeholders = re.findall(self.allowed_placeholders, content)
        return [p[2:-2].strip() for p in placeholders]
    
    def validate_context(self, template_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate context against template placeholders."""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        if 'content' not in template_data:
            return result
        
        # Extract required placeholders
        required_placeholders = self.extract_placeholders(template_data['content'])
        
        # Check if all required placeholders are provided
        for placeholder in required_placeholders:
            if placeholder not in context:
                result['errors'].append(f"Missing context value for placeholder: {placeholder}")
                result['is_valid'] = False
        
        # Check for unused context values
        for key in context.keys():
            if key not in required_placeholders:
                result['warnings'].append(f"Unused context value: {key}")
        
        return result
