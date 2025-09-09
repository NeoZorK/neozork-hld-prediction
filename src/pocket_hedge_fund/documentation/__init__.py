"""
Documentation Module for Pocket Hedge Fund

This module provides comprehensive documentation capabilities including:
- API documentation generation and management
- User guides and tutorials
- Developer documentation and guides
- Deployment and infrastructure documentation
- Architecture and design documentation
- Code examples and samples
- Interactive documentation and demos
- Multi-format documentation support (Markdown, HTML, PDF)
"""

from .generators.api_doc_generator import APIDocGenerator
from .generators.user_guide_generator import UserGuideGenerator
from .generators.developer_guide_generator import DeveloperGuideGenerator
from .generators.architecture_doc_generator import ArchitectureDocGenerator
from .formatters.markdown_formatter import MarkdownFormatter
from .formatters.html_formatter import HTMLFormatter
from .formatters.pdf_formatter import PDFFormatter
from .templates.doc_template_manager import DocTemplateManager
from .validators.doc_validator import DocValidator

__version__ = "1.0.0"
__author__ = "Pocket Hedge Fund Team"

__all__ = [
    # Generators
    "APIDocGenerator",
    "UserGuideGenerator", 
    "DeveloperGuideGenerator",
    "ArchitectureDocGenerator",
    
    # Formatters
    "MarkdownFormatter",
    "HTMLFormatter",
    "PDFFormatter",
    
    # Templates and Validation
    "DocTemplateManager",
    "DocValidator"
]
