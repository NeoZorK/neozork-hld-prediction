"""
Unit tests for core.exceptions module.
"""

import pytest

from src.core.exceptions import (
    NeozorkError,
    DataError,
    ValidationError,
    ProcessingError,
    AnalysisError,
    MLError,
    ModelError,
    ConfigurationError,
    ExportError,
    CLIError,
    NetworkError,
    FileError,
    AuthenticationError,
    RateLimitError,
)


class TestExceptions:
    """Test cases for custom exception classes."""
    
    def test_neozork_error_base(self):
        """Test base NeozorkError exception."""
        error = NeozorkError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.error_code is None
        
        # Test with error code
        error_with_code = NeozorkError("Test error", "ERR001")
        assert error_with_code.error_code == "ERR001"
    
    def test_data_error(self):
        """Test DataError exception."""
        error = DataError("Data processing failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Data processing failed"
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        error = ValidationError("Validation failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Validation failed"
    
    def test_processing_error(self):
        """Test ProcessingError exception."""
        error = ProcessingError("Processing failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Processing failed"
    
    def test_analysis_error(self):
        """Test AnalysisError exception."""
        error = AnalysisError("Analysis failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Analysis failed"
    
    def test_ml_error(self):
        """Test MLError exception."""
        error = MLError("ML operation failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "ML operation failed"
    
    def test_model_error(self):
        """Test ModelError exception."""
        error = ModelError("Model training failed")
        assert isinstance(error, MLError)
        assert isinstance(error, NeozorkError)
        assert str(error) == "Model training failed"
    
    def test_configuration_error(self):
        """Test ConfigurationError exception."""
        error = ConfigurationError("Configuration invalid")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Configuration invalid"
    
    def test_export_error(self):
        """Test ExportError exception."""
        error = ExportError("Export failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Export failed"
    
    def test_cli_error(self):
        """Test CLIError exception."""
        error = CLIError("CLI command failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "CLI command failed"
    
    def test_network_error(self):
        """Test NetworkError exception."""
        error = NetworkError("Network request failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Network request failed"
    
    def test_file_error(self):
        """Test FileError exception."""
        error = FileError("File operation failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "File operation failed"
    
    def test_authentication_error(self):
        """Test AuthenticationError exception."""
        error = AuthenticationError("Authentication failed")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Authentication failed"
    
    def test_rate_limit_error(self):
        """Test RateLimitError exception."""
        error = RateLimitError("Rate limit exceeded")
        assert isinstance(error, NeozorkError)
        assert str(error) == "Rate limit exceeded"


__all__ = ["TestExceptions"]
