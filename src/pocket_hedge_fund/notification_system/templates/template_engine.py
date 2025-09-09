"""
Template Engine

Core template rendering engine for notifications.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import re
import json

from ..models.notification_models import NotificationTemplate, TemplateType

logger = logging.getLogger(__name__)


class TemplateEngine:
    """
    Core template rendering engine for notifications.
    """
    
    def __init__(self):
        """Initialize template engine."""
        self.template_cache = {}
        self.compiled_templates = {}
        self.supported_functions = {
            'format_date': self._format_date,
            'format_currency': self._format_currency,
            'format_percentage': self._format_percentage,
            'uppercase': self._uppercase,
            'lowercase': self._lowercase,
            'capitalize': self._capitalize
        }
    
    async def initialize(self):
        """Initialize template engine."""
        try:
            # Load built-in templates
            await self._load_builtin_templates()
            
            logger.info("Template engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize template engine: {e}")
            raise
    
    async def render_template(
        self,
        template: NotificationTemplate,
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Render template with provided data.
        
        Args:
            template: Template to render
            data: Data for template rendering
            
        Returns:
            Rendered content dictionary
        """
        try:
            # Get compiled template
            compiled_template = await self._get_compiled_template(template)
            
            # Render template
            if template.template_type == TemplateType.HTML:
                return await self._render_html_template(compiled_template, data)
            elif template.template_type == TemplateType.TEXT:
                return await self._render_text_template(compiled_template, data)
            elif template.template_type == TemplateType.MARKDOWN:
                return await self._render_markdown_template(compiled_template, data)
            elif template.template_type == TemplateType.JSON:
                return await self._render_json_template(compiled_template, data)
            else:
                raise ValueError(f"Unsupported template type: {template.template_type}")
                
        except Exception as e:
            logger.error(f"Failed to render template: {e}")
            raise
    
    async def _get_compiled_template(self, template: NotificationTemplate) -> Dict[str, str]:
        """Get compiled template from cache or compile it."""
        try:
            template_key = f"{template.id}_{template.version}"
            
            if template_key in self.compiled_templates:
                return self.compiled_templates[template_key]
            
            # Compile template
            compiled = await self._compile_template(template)
            self.compiled_templates[template_key] = compiled
            
            return compiled
            
        except Exception as e:
            logger.error(f"Failed to get compiled template: {e}")
            raise
    
    async def _compile_template(self, template: NotificationTemplate) -> Dict[str, str]:
        """Compile template for rendering."""
        try:
            compiled = {}
            
            # Compile subject template
            if template.subject_template:
                compiled['subject'] = await self._compile_template_string(template.subject_template)
            else:
                compiled['subject'] = "{{title}}"
            
            # Compile body template
            compiled['body'] = await self._compile_template_string(template.body_template)
            
            return compiled
            
        except Exception as e:
            logger.error(f"Failed to compile template: {e}")
            raise
    
    async def _compile_template_string(self, template_string: str) -> str:
        """Compile a template string."""
        try:
            # Simple template compilation - replace {{variable}} with placeholders
            # In a real implementation, you might use Jinja2 or similar
            
            # Find all template variables
            variables = re.findall(r'\{\{([^}]+)\}\}', template_string)
            
            # Replace with placeholders for now
            compiled = template_string
            for var in variables:
                placeholder = f"__VAR_{var}__"
                compiled = compiled.replace(f"{{{{{var}}}}}", placeholder)
            
            return compiled
            
        except Exception as e:
            logger.error(f"Failed to compile template string: {e}")
            return template_string
    
    async def _render_html_template(
        self,
        compiled_template: Dict[str, str],
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Render HTML template."""
        try:
            rendered = {}
            
            # Render subject
            rendered['subject'] = await self._render_template_string(
                compiled_template['subject'], data
            )
            
            # Render body
            rendered['body'] = await self._render_template_string(
                compiled_template['body'], data
            )
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render HTML template: {e}")
            raise
    
    async def _render_text_template(
        self,
        compiled_template: Dict[str, str],
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Render text template."""
        try:
            rendered = {}
            
            # Render subject
            rendered['subject'] = await self._render_template_string(
                compiled_template['subject'], data
            )
            
            # Render body
            rendered['body'] = await self._render_template_string(
                compiled_template['body'], data
            )
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render text template: {e}")
            raise
    
    async def _render_markdown_template(
        self,
        compiled_template: Dict[str, str],
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Render markdown template."""
        try:
            rendered = {}
            
            # Render subject
            rendered['subject'] = await self._render_template_string(
                compiled_template['subject'], data
            )
            
            # Render body
            rendered['body'] = await self._render_template_string(
                compiled_template['body'], data
            )
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render markdown template: {e}")
            raise
    
    async def _render_json_template(
        self,
        compiled_template: Dict[str, str],
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Render JSON template."""
        try:
            rendered = {}
            
            # Render subject
            rendered['subject'] = await self._render_template_string(
                compiled_template['subject'], data
            )
            
            # Render body as JSON
            body_data = await self._render_template_data(compiled_template['body'], data)
            rendered['body'] = json.dumps(body_data, indent=2)
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render JSON template: {e}")
            raise
    
    async def _render_template_string(
        self,
        compiled_string: str,
        data: Dict[str, Any]
    ) -> str:
        """Render a compiled template string with data."""
        try:
            rendered = compiled_string
            
            # Replace placeholders with actual values
            for key, value in data.items():
                placeholder = f"__VAR_{key}__"
                rendered = rendered.replace(placeholder, str(value))
            
            # Process functions
            rendered = await self._process_functions(rendered, data)
            
            return rendered
            
        except Exception as e:
            logger.error(f"Failed to render template string: {e}")
            return compiled_string
    
    async def _render_template_data(
        self,
        compiled_string: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Render template data for JSON templates."""
        try:
            # Simple implementation - return data as-is
            return data
            
        except Exception as e:
            logger.error(f"Failed to render template data: {e}")
            return data
    
    async def _process_functions(self, template: str, data: Dict[str, Any]) -> str:
        """Process template functions."""
        try:
            # Find function calls in template
            function_pattern = r'\{\{([^}]+)\(([^)]*)\)\}\}'
            matches = re.findall(function_pattern, template)
            
            for func_name, args in matches:
                if func_name in self.supported_functions:
                    # Parse arguments
                    arg_list = [arg.strip().strip('"\'') for arg in args.split(',') if arg.strip()]
                    
                    # Call function
                    result = await self._call_function(func_name, arg_list, data)
                    
                    # Replace in template
                    template = template.replace(f"{{{{{func_name}({args})}}}}", str(result))
            
            return template
            
        except Exception as e:
            logger.error(f"Failed to process functions: {e}")
            return template
    
    async def _call_function(
        self,
        func_name: str,
        args: List[str],
        data: Dict[str, Any]
    ) -> str:
        """Call a template function."""
        try:
            func = self.supported_functions[func_name]
            
            # Resolve arguments (replace variables with actual values)
            resolved_args = []
            for arg in args:
                if arg in data:
                    resolved_args.append(data[arg])
                else:
                    resolved_args.append(arg)
            
            # Call function
            if asyncio.iscoroutinefunction(func):
                result = await func(*resolved_args)
            else:
                result = func(*resolved_args)
            
            return str(result)
            
        except Exception as e:
            logger.error(f"Failed to call function {func_name}: {e}")
            return f"{{{{{func_name}({','.join(args)})}}}}"
    
    def _format_date(self, date_str: str, format_str: str = "%Y-%m-%d") -> str:
        """Format date string."""
        try:
            if isinstance(date_str, str):
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            else:
                date_obj = date_str
            
            return date_obj.strftime(format_str)
        except Exception:
            return str(date_str)
    
    def _format_currency(self, amount: str, currency: str = "USD") -> str:
        """Format currency amount."""
        try:
            amount_float = float(amount)
            return f"{currency} {amount_float:,.2f}"
        except Exception:
            return str(amount)
    
    def _format_percentage(self, value: str, decimals: int = 2) -> str:
        """Format percentage value."""
        try:
            value_float = float(value)
            return f"{value_float:.{decimals}f}%"
        except Exception:
            return str(value)
    
    def _uppercase(self, text: str) -> str:
        """Convert text to uppercase."""
        return str(text).upper()
    
    def _lowercase(self, text: str) -> str:
        """Convert text to lowercase."""
        return str(text).lower()
    
    def _capitalize(self, text: str) -> str:
        """Capitalize text."""
        return str(text).capitalize()
    
    async def _load_builtin_templates(self):
        """Load built-in templates."""
        try:
            # This would load built-in templates from files or database
            # For now, just log
            logger.info("Loaded built-in templates")
            
        except Exception as e:
            logger.error(f"Failed to load built-in templates: {e}")
    
    async def cleanup(self):
        """Cleanup template engine resources."""
        try:
            self.template_cache.clear()
            self.compiled_templates.clear()
            logger.info("Template engine cleanup completed")
        except Exception as e:
            logger.error(f"Error during template engine cleanup: {e}")
