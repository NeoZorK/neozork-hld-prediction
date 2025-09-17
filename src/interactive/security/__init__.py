# -*- coding: utf-8 -*-
"""
Security module for NeoZork Interactive ML Trading Strategy Development.

This module provides comprehensive security and compliance capabilities.
"""

from .access_control import AccessControl
from .encryption_manager import EncryptionManager
from .compliance_monitor import ComplianceMonitor

class SecuritySystem:
    """Main security system class."""
    def __init__(self):
        self.access_control = AccessControl()
        self.encryption_manager = EncryptionManager()
        self.compliance_monitor = ComplianceMonitor()

__all__ = [
    'SecuritySystem',
    'AccessControl',
    'EncryptionManager',
    'ComplianceMonitor'
]
