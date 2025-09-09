"""
Markdown Formatter

Formats documentation content as Markdown.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MarkdownFormatter:
    """
    Formats documentation content as Markdown.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Markdown formatter."""
        self.config = config or {}
        self.include_toc = self.config.get('include_toc', True)
        self.include_metadata = self.config.get('include_metadata', True)
        self.include_timestamps = self.config.get('include_timestamps', True)
        self.max_heading_level = self.config.get('max_heading_level', 6)
        self.table_style = self.config.get('table_style', 'pipe')  # pipe, grid, simple
        
    def format_document(self, content: Dict[str, Any]) -> str:
        """Format a complete document as Markdown."""
        try:
            markdown_parts = []
            
            # Add metadata if enabled
            if self.include_metadata and 'metadata' in content:
                markdown_parts.append(self._format_metadata(content['metadata']))
            
            # Add table of contents if enabled
            if self.include_toc and 'sections' in content:
                markdown_parts.append(self._format_table_of_contents(content['sections']))
            
            # Add main content
            if 'sections' in content:
                for section_name, section_content in content['sections'].items():
                    markdown_parts.append(self._format_section(section_name, section_content))
            
            return '\n\n'.join(markdown_parts)
            
        except Exception as e:
            logger.error(f"Failed to format document: {e}")
            raise
    
    def format_section(self, section_name: str, section_content: Dict[str, Any]) -> str:
        """Format a single section as Markdown."""
        try:
            title = section_content.get('title', section_name.replace('_', ' ').title())
            content = section_content.get('content', {})
            
            markdown_parts = [f"# {title}"]
            
            # Add introduction if available
            if 'introduction' in content:
                markdown_parts.append(content['introduction'])
            
            # Format different content types
            if 'steps' in content:
                markdown_parts.append(self._format_steps(content['steps']))
            
            if 'features' in content:
                markdown_parts.append(self._format_features(content['features']))
            
            if 'tables' in content:
                markdown_parts.append(self._format_tables(content['tables']))
            
            if 'code_blocks' in content:
                markdown_parts.append(self._format_code_blocks(content['code_blocks']))
            
            if 'lists' in content:
                markdown_parts.append(self._format_lists(content['lists']))
            
            return '\n\n'.join(markdown_parts)
            
        except Exception as e:
            logger.error(f"Failed to format section {section_name}: {e}")
            return f"# {section_name}\n\nError formatting section: {e}"
    
    def _format_metadata(self, metadata: Dict[str, Any]) -> str:
        """Format document metadata."""
        try:
            parts = []
            
            # Add title
            if 'title' in metadata:
                parts.append(f"# {metadata['title']}")
            
            # Add description
            if 'description' in metadata:
                parts.append(metadata['description'])
            
            # Add version info
            if 'version' in metadata:
                parts.append(f"**Version**: {metadata['version']}")
            
            # Add author info
            if 'author' in metadata:
                parts.append(f"**Author**: {metadata['author']}")
            
            # Add timestamp
            if self.include_timestamps and 'generated_at' in metadata:
                parts.append(f"**Generated**: {metadata['generated_at']}")
            
            return '\n\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format metadata: {e}")
            return ""
    
    def _format_table_of_contents(self, sections: Dict[str, Any]) -> str:
        """Format table of contents."""
        try:
            if not sections:
                return ""
            
            parts = ["## Table of Contents", ""]
            
            for section_name, section_content in sections.items():
                title = section_content.get('title', section_name.replace('_', ' ').title())
                link = section_name.replace('_', '-').lower()
                parts.append(f"- [{title}](#{link})")
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format table of contents: {e}")
            return ""
    
    def _format_steps(self, steps: List[Dict[str, Any]]) -> str:
        """Format steps as Markdown."""
        try:
            if not steps:
                return ""
            
            parts = []
            
            for i, step in enumerate(steps, 1):
                # Add step title
                if 'title' in step:
                    parts.append(f"### Step {i}: {step['title']}")
                
                # Add description
                if 'description' in step:
                    parts.append(step['description'])
                
                # Add code block if present
                if 'code' in step:
                    language = step.get('language', '')
                    parts.append(f"```{language}")
                    parts.append(step['code'])
                    parts.append("```")
                
                # Add details if present
                if 'details' in step:
                    parts.append("**Details:**")
                    for detail in step['details']:
                        parts.append(f"- {detail}")
                
                # Add notes if present
                if 'notes' in step:
                    parts.append(f"**Note**: {step['notes']}")
                
                parts.append("")  # Add spacing between steps
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format steps: {e}")
            return ""
    
    def _format_features(self, features: Dict[str, Any]) -> str:
        """Format features as Markdown."""
        try:
            if not features:
                return ""
            
            parts = []
            
            for feature_name, feature_data in features.items():
                if isinstance(feature_data, dict):
                    # Add feature title
                    title = feature_data.get('title', feature_name.replace('_', ' ').title())
                    parts.append(f"### {title}")
                    
                    # Add description
                    if 'description' in feature_data:
                        parts.append(feature_data['description'])
                    
                    # Add features list
                    if 'features' in feature_data:
                        parts.append("**Features:**")
                        for feature in feature_data['features']:
                            parts.append(f"- {feature}")
                    
                    # Add details
                    if 'details' in feature_data:
                        parts.append("**Details:**")
                        for detail in feature_data['details']:
                            parts.append(f"- {detail}")
                    
                    parts.append("")  # Add spacing
                else:
                    # Simple feature list
                    parts.append(f"- {feature_data}")
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format features: {e}")
            return ""
    
    def _format_tables(self, tables: List[Dict[str, Any]]) -> str:
        """Format tables as Markdown."""
        try:
            if not tables:
                return ""
            
            parts = []
            
            for table in tables:
                if 'title' in table:
                    parts.append(f"### {table['title']}")
                
                if 'headers' in table and 'rows' in table:
                    # Format table
                    table_markdown = self._format_table(table['headers'], table['rows'])
                    parts.append(table_markdown)
                
                parts.append("")  # Add spacing
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format tables: {e}")
            return ""
    
    def _format_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """Format a single table as Markdown."""
        try:
            if not headers or not rows:
                return ""
            
            parts = []
            
            if self.table_style == 'pipe':
                # Pipe table format
                parts.append('| ' + ' | '.join(headers) + ' |')
                parts.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
                
                for row in rows:
                    parts.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
            
            elif self.table_style == 'grid':
                # Grid table format
                parts.append('+ ' + ' + '.join(['-' * len(header) for header in headers]) + ' +')
                parts.append('| ' + ' | '.join(headers) + ' |')
                parts.append('+ ' + ' + '.join(['-' * len(header) for header in headers]) + ' +')
                
                for row in rows:
                    parts.append('| ' + ' | '.join(str(cell) for cell in row) + ' |')
                
                parts.append('+ ' + ' + '.join(['-' * len(header) for header in headers]) + ' +')
            
            else:  # simple
                # Simple table format
                parts.append(' '.join(headers))
                parts.append(' '.join(['-' * len(header) for header in headers]))
                
                for row in rows:
                    parts.append(' '.join(str(cell) for cell in row))
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format table: {e}")
            return ""
    
    def _format_code_blocks(self, code_blocks: List[Dict[str, Any]]) -> str:
        """Format code blocks as Markdown."""
        try:
            if not code_blocks:
                return ""
            
            parts = []
            
            for code_block in code_blocks:
                if 'title' in code_block:
                    parts.append(f"### {code_block['title']}")
                
                if 'description' in code_block:
                    parts.append(code_block['description'])
                
                if 'code' in code_block:
                    language = code_block.get('language', '')
                    parts.append(f"```{language}")
                    parts.append(code_block['code'])
                    parts.append("```")
                
                parts.append("")  # Add spacing
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format code blocks: {e}")
            return ""
    
    def _format_lists(self, lists: Dict[str, List[str]]) -> str:
        """Format lists as Markdown."""
        try:
            if not lists:
                return ""
            
            parts = []
            
            for list_name, list_items in lists.items():
                if list_items:
                    title = list_name.replace('_', ' ').title()
                    parts.append(f"### {title}")
                    
                    for item in list_items:
                        parts.append(f"- {item}")
                    
                    parts.append("")  # Add spacing
            
            return '\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format lists: {e}")
            return ""
    
    def format_api_endpoint(self, endpoint: Dict[str, Any]) -> str:
        """Format an API endpoint as Markdown."""
        try:
            parts = []
            
            # Add endpoint title
            if 'path' in endpoint and 'methods' in endpoint:
                methods = ', '.join(endpoint['methods'])
                parts.append(f"## {methods} {endpoint['path']}")
            
            # Add summary
            if 'summary' in endpoint:
                parts.append(f"**Summary**: {endpoint['summary']}")
            
            # Add description
            if 'description' in endpoint:
                parts.append(f"**Description**: {endpoint['description']}")
            
            # Add parameters
            if 'parameters' in endpoint:
                parts.append("### Parameters")
                for param in endpoint['parameters']:
                    param_name = param.get('name', '')
                    param_type = param.get('type', '')
                    param_desc = param.get('description', '')
                    param_required = param.get('required', False)
                    
                    required_text = " (required)" if param_required else " (optional)"
                    parts.append(f"- `{param_name}` ({param_type}){required_text}: {param_desc}")
            
            # Add request body
            if 'request_body' in endpoint:
                parts.append("### Request Body")
                parts.append(f"```json")
                parts.append(endpoint['request_body'])
                parts.append("```")
            
            # Add responses
            if 'responses' in endpoint:
                parts.append("### Responses")
                for status_code, response in endpoint['responses'].items():
                    parts.append(f"- `{status_code}`: {response.get('description', '')}")
            
            # Add examples
            if 'examples' in endpoint:
                parts.append("### Examples")
                for example in endpoint['examples']:
                    if 'title' in example:
                        parts.append(f"#### {example['title']}")
                    
                    if 'request' in example:
                        parts.append("**Request:**")
                        parts.append(f"```{example.get('request_language', 'bash')}")
                        parts.append(example['request'])
                        parts.append("```")
                    
                    if 'response' in example:
                        parts.append("**Response:**")
                        parts.append(f"```{example.get('response_language', 'json')}")
                        parts.append(example['response'])
                        parts.append("```")
            
            return '\n\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format API endpoint: {e}")
            return ""
    
    def format_schema(self, schema: Dict[str, Any]) -> str:
        """Format a data schema as Markdown."""
        try:
            parts = []
            
            # Add schema title
            if 'name' in schema:
                parts.append(f"## {schema['name']}")
            
            # Add description
            if 'description' in schema:
                parts.append(schema['description'])
            
            # Add properties
            if 'properties' in schema:
                parts.append("### Properties")
                
                for prop_name, prop_details in schema['properties'].items():
                    prop_type = prop_details.get('type', '')
                    prop_desc = prop_details.get('description', '')
                    prop_required = prop_details.get('required', False)
                    
                    required_text = " (required)" if prop_required else " (optional)"
                    parts.append(f"- `{prop_name}` ({prop_type}){required_text}: {prop_desc}")
            
            # Add example
            if 'example' in schema:
                parts.append("### Example")
                parts.append("```json")
                parts.append(schema['example'])
                parts.append("```")
            
            return '\n\n'.join(parts)
            
        except Exception as e:
            logger.error(f"Failed to format schema: {e}")
            return ""
    
    def save_formatted_document(self, content: str, output_path: Path) -> None:
        """Save formatted Markdown document to file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding='utf-8')
            logger.info(f"Formatted document saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to save formatted document: {e}")
            raise
