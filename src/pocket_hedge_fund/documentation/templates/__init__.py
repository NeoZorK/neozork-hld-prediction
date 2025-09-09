"""
Documentation Templates

This module contains template management for documentation:
- DocTemplateManager: Main template manager
- APITemplate: API documentation templates
- UserGuideTemplate: User guide templates
- DeveloperTemplate: Developer documentation templates
- ArchitectureTemplate: Architecture documentation templates
- ExampleTemplate: Code example templates
"""

from .doc_template_manager import DocTemplateManager
from .api_template import APITemplate
from .user_guide_template import UserGuideTemplate
from .developer_template import DeveloperTemplate
from .architecture_template import ArchitectureTemplate
from .example_template import ExampleTemplate

__all__ = [
    "DocTemplateManager",
    "APITemplate",
    "UserGuideTemplate",
    "DeveloperTemplate",
    "ArchitectureTemplate",
    "ExampleTemplate"
]
