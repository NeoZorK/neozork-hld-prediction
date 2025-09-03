"""
Custom exceptions for the Neozork HLD Prediction system.

This module defines all custom exceptions used throughout the system.
"""


class NeozorkError(Exception):
    """Base exception for all Neozork system errors."""
    
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DataError(NeozorkError):
    """Exception raised for data-related errors."""
    pass


class ValidationError(NeozorkError):
    """Exception raised for data validation errors."""
    pass


class ProcessingError(NeozorkError):
    """Exception raised for data processing errors."""
    pass


class AnalysisError(NeozorkError):
    """Exception raised for analysis errors."""
    pass


class MLError(NeozorkError):
    """Exception raised for machine learning errors."""
    pass


class ModelError(MLError):
    """Exception raised for model-related errors."""
    pass


class ConfigurationError(NeozorkError):
    """Exception raised for configuration errors."""
    pass


class ExportError(NeozorkError):
    """Exception raised for export errors."""
    pass


class CLIError(NeozorkError):
    """Exception raised for command-line interface errors."""
    pass


class NetworkError(NeozorkError):
    """Exception raised for network-related errors."""
    pass


class FileError(NeozorkError):
    """Exception raised for file operation errors."""
    pass


class AuthenticationError(NeozorkError):
    """Exception raised for authentication errors."""
    pass


class RateLimitError(NeozorkError):
    """Exception raised for rate limiting errors."""
    pass
