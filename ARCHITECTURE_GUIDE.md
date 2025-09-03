# Architecture Guide

## Overview

The Neozork HLD Prediction system follows a modular, layered architecture designed for scalability, maintainability, and extensibility. This guide outlines the architectural principles, component design, and system organization.

## Architectural Principles

### Core Principles
1. **Separation of Concerns**: Each component has a single, well-defined responsibility
2. **Dependency Injection**: Components receive dependencies via constructors
3. **Interface-First Design**: Use of Python `Protocol` and `ABC` for component contracts
4. **Configuration-Driven**: Centralized, hierarchical configuration management
5. **Error Handling**: Structured exception hierarchy with specific error types
6. **Logging**: Comprehensive logging with custom formatters and handlers

### Design Patterns
- **Factory Pattern**: For creating component instances
- **Strategy Pattern**: For interchangeable algorithms
- **Observer Pattern**: For event-driven communication
- **Pipeline Pattern**: For data processing workflows
- **Repository Pattern**: For data access abstraction

## System Architecture

### Layered Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │    CLI      │  │   Web API   │  │   Interactive UI    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Analysis   │  │     ML      │  │   Data Processing   │ │
│  │   Engine    │  │   Models    │  │      Pipeline       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Sources   │  │  Processors │  │      Storage        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                     Core Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Base      │  │    Config   │  │    Exceptions       │ │
│  │  Classes    │  │ Management  │  │      & Logging      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

#### Core Module (`src.core`)
- **Base Classes**: Foundation for all system components
- **Configuration**: Centralized configuration management
- **Exceptions**: Structured error handling hierarchy
- **Interfaces**: Abstract component contracts
- **Logging**: Comprehensive logging system

#### Data Module (`src.data`)
- **Sources**: Data acquisition from various sources
- **Processors**: Data transformation and cleaning
- **Storage**: Data persistence and retrieval
- **Validation**: Data integrity and quality checks
- **Pipeline**: Orchestrated data processing workflows

#### Analysis Module (`src.analysis`)
- **Indicators**: Technical analysis indicators
- **Statistics**: Statistical analysis tools
- **Patterns**: Pattern recognition algorithms
- **Pipeline**: Analysis workflow orchestration
- **Metrics**: Performance and quality metrics

#### ML Module (`src.ml`)
- **Models**: Machine learning model implementations
- **Features**: Feature engineering and selection
- **Training**: Model training pipelines
- **Evaluation**: Model performance assessment
- **Pipeline**: End-to-end ML workflows

#### CLI Module (`src.cli`)
- **Core**: Command-line interface foundation
- **Commands**: Individual command implementations
- **Parsers**: Argument parsing and validation
- **Formatters**: Output formatting and display

#### Utils Module (`src.utils`)
- **File Utils**: File and directory operations
- **Math Utils**: Mathematical operations and utilities
- **Time Utils**: Time and date handling
- **Validation**: Input validation utilities

## Component Design

### Base Component Architecture
```python
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import Any, Dict, Optional

class BaseComponent(ABC):
    """
    Base class for all system components.
    
    Provides common functionality including:
    - Component identification and metadata
    - Configuration management
    - Logging setup
    - Lifecycle tracking
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Initialize base component.
        
        Args:
            name: Component name for identification
            config: Configuration dictionary
        """
        self.name = name
        self.config = config
        self.created_at = datetime.now()
        self.logger = self._setup_logger()
        self._validate_config()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup component-specific logger."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.name}")
        return logger
    
    def _validate_config(self) -> None:
        """Validate component configuration."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Component name must be a non-empty string")
        
        if not isinstance(self.config, dict):
            raise ValueError("Configuration must be a dictionary")
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status information."""
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "created_at": self.created_at.isoformat(),
            "config_keys": list(self.config.keys())
        }
    
    def __str__(self) -> str:
        """String representation of component."""
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"{self.__class__.__name__}(name='{self.name}', config={self.config})"
```

### Interface Definitions
```python
from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod
import pandas as pd

@runtime_checkable
class DataSource(Protocol):
    """Protocol for data sources."""
    
    def fetch_data(self, **kwargs) -> pd.DataFrame:
        """Fetch data from source."""
        ...
    
    def is_available(self) -> bool:
        """Check if source is available."""
        ...
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get source metadata."""
        ...

class DataProcessor(ABC):
    """Abstract base class for data processors."""
    
    @abstractmethod
    def process_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process input data."""
        pass
    
    @abstractmethod
    def get_processing_info(self) -> Dict[str, Any]:
        """Get processing information."""
        pass

class AnalysisStep(ABC):
    """Abstract base class for analysis steps."""
    
    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data through analysis step."""
        pass
    
    @abstractmethod
    def get_analysis_info(self) -> Dict[str, Any]:
        """Get analysis information."""
        pass
```

## Data Flow Architecture

### Data Processing Pipeline
```
Raw Data → Validation → Cleaning → Transformation → Analysis → Results
   ↓           ↓         ↓           ↓           ↓         ↓
Sources → Validators → Cleaners → Processors → Analysis → Exporters
```

### Analysis Pipeline
```
Input Data → Preprocessing → Feature Engineering → Analysis → Post-processing → Output
     ↓            ↓              ↓              ↓           ↓              ↓
  Raw Data → Data Cleaner → Feature Extractor → Indicators → Aggregator → Results
```

### ML Pipeline
```
Training Data → Feature Engineering → Model Training → Validation → Model Storage
      ↓              ↓                ↓              ↓            ↓
   Raw Data → Feature Pipeline → Training Pipeline → Evaluator → Model Registry
```

## Configuration Architecture

### Hierarchical Configuration
```json
{
  "system": {
    "name": "Neozork HLD Prediction System",
    "version": "1.0.0",
    "environment": "development"
  },
  "data": {
    "cache_dir": "data/cache",
    "raw_dir": "data/raw",
    "processed_dir": "data/processed"
  },
  "analysis": {
    "default_timeframe": "1H",
    "max_lookback_periods": 1000,
    "indicators": {
      "sma": {"default_period": 20},
      "rsi": {"default_period": 14}
    }
  },
  "ml": {
    "model_dir": "models",
    "default_algorithm": "random_forest",
    "algorithms": {
      "random_forest": {
        "n_estimators": 100,
        "max_depth": 10
      }
    }
  }
}
```

### Configuration Management
```python
class Config:
    """Centralized configuration management."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config.json"
        self._config = self._load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self) -> None:
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self._config, f, indent=2)
```

## Error Handling Architecture

### Exception Hierarchy
```python
class NeozorkError(Exception):
    """Base exception for all Neozork system errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.timestamp = datetime.now()

class DataError(NeozorkError):
    """Exception for data-related errors."""
    pass

class ValidationError(NeozorkError):
    """Exception for validation errors."""
    pass

class MLError(NeozorkError):
    """Exception for machine learning errors."""
    pass

class CLIError(NeozorkError):
    """Exception for command-line interface errors."""
    pass

class ConfigError(NeozorkError):
    """Exception for configuration errors."""
    pass
```

### Error Handling Strategy
```python
def robust_operation(func):
    """Decorator for robust error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DataError as e:
            logger.error(f"Data error in {func.__name__}: {e}")
            raise
        except ValidationError as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise NeozorkError(f"Operation failed: {e}") from e
    return wrapper
```

## Logging Architecture

### Logging Configuration
```python
class LoggingConfig:
    """Centralized logging configuration."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging system."""
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, self.config.get("level", "INFO")),
            format=self.config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            handlers=self._create_handlers()
        )
    
    def _create_handlers(self) -> List[logging.Handler]:
        """Create logging handlers."""
        handlers = []
        
        # Console handler
        if self.config.get("handlers", {}).get("console", {}).get("enabled", True):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(
                getattr(logging, self.config["handlers"]["console"].get("level", "INFO"))
            )
            handlers.append(console_handler)
        
        # File handler
        if self.config.get("handlers", {}).get("file", {}).get("enabled", True):
            file_handler = logging.FileHandler(self.config.get("file", "logs/system.log"))
            file_handler.setLevel(
                getattr(logging, self.config["handlers"]["file"].get("level", "DEBUG"))
            )
            handlers.append(file_handler)
        
        return handlers
```

## Performance Architecture

### Caching Strategy
```python
from functools import lru_cache
from typing import Any, Callable

class CacheManager:
    """Centralized caching management."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache = {}
        self.max_size = config.get("max_size_mb", 100) * 1024 * 1024  # Convert to bytes
        self.ttl = config.get("ttl_seconds", 3600)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self.cache[key] = (value, time.time())
        self._cleanup_if_needed()
    
    def _cleanup_if_needed(self):
        """Clean up cache if size exceeds limit."""
        if len(self.cache) > self.max_size:
            # Remove oldest entries
            sorted_items = sorted(self.cache.items(), key=lambda x: x[1][1])
            items_to_remove = len(sorted_items) - self.max_size // 2
            for i in range(items_to_remove):
                del self.cache[sorted_items[i][0]]
```

### Parallel Processing
```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Callable, Any

class ParallelProcessor:
    """Parallel processing manager."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_workers = config.get("max_workers", "auto")
        self.chunk_size = config.get("chunk_size", 1000)
    
    def process_parallel(self, data: List[Any], processor: Callable) -> List[Any]:
        """Process data in parallel."""
        if self.max_workers == "auto":
            max_workers = min(len(data), os.cpu_count())
        else:
            max_workers = min(self.max_workers, len(data))
        
        if max_workers <= 1:
            return [processor(item) for item in data]
        
        # Split data into chunks
        chunks = [data[i:i + self.chunk_size] for i in range(0, len(data), self.chunk_size)]
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(processor, chunks))
        
        # Flatten results
        return [item for sublist in results for item in sublist]
```

## Security Architecture

### Input Validation
```python
class InputValidator:
    """Input validation and sanitization."""
    
    @staticmethod
    def validate_file_path(file_path: str) -> str:
        """Validate and sanitize file path."""
        if not file_path or not isinstance(file_path, str):
            raise ValidationError("File path must be a non-empty string")
        
        # Check for path traversal attempts
        if ".." in file_path or file_path.startswith("/"):
            raise ValidationError("Invalid file path")
        
        # Sanitize path
        sanitized = re.sub(r'[^\w\-_./]', '', file_path)
        
        if not sanitized:
            raise ValidationError("File path contains no valid characters")
        
        return sanitized
    
    @staticmethod
    def validate_numeric_input(value: Any, min_val: Optional[float] = None, 
                             max_val: Optional[float] = None) -> float:
        """Validate numeric input values."""
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"Value must be numeric, got: {value}")
        
        if min_val is not None and num_value < min_val:
            raise ValidationError(f"Value must be >= {min_val}, got: {num_value}")
        
        if max_val is not None and num_value > max_val:
            raise ValidationError(f"Value must be <= {max_val}, got: {num_value}")
        
        return num_value
```

### Access Control
```python
class AccessController:
    """Access control and permissions management."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.allowed_extensions = config.get("allowed_extensions", [".csv", ".json", ".parquet"])
        self.max_file_size = config.get("max_file_size_mb", 100) * 1024 * 1024
    
    def check_file_access(self, file_path: str) -> bool:
        """Check if file access is allowed."""
        # Check file extension
        if not any(file_path.endswith(ext) for ext in self.allowed_extensions):
            return False
        
        # Check file size
        try:
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return False
        except OSError:
            return False
        
        return True
    
    def check_directory_access(self, directory: str) -> bool:
        """Check if directory access is allowed."""
        # Check if directory is within allowed paths
        allowed_paths = self.config.get("allowed_paths", ["data/", "logs/", "models/"])
        
        for allowed_path in allowed_paths:
            if directory.startswith(allowed_path):
                return True
        
        return False
```

## Monitoring Architecture

### Health Checks
```python
class HealthChecker:
    """System health monitoring."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.checks = []
        self._setup_checks()
    
    def _setup_checks(self):
        """Setup health check functions."""
        if self.config.get("health_checks", {}).get("enabled", True):
            self.checks.extend([
                self._check_disk_space,
                self._check_memory_usage,
                self._check_database_connection,
                self._check_file_permissions
            ])
    
    def run_health_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        
        for check in self.checks:
            try:
                check_name = check.__name__.replace("_check_", "")
                results[check_name] = check()
            except Exception as e:
                results[check_name] = {"status": "error", "message": str(e)}
        
        return results
    
    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space."""
        stat = os.statvfs(".")
        free_space = stat.f_frsize * stat.f_bavail
        total_space = stat.f_frsize * stat.f_blocks
        
        usage_percent = (1 - free_space / total_space) * 100
        
        return {
            "status": "healthy" if usage_percent < 90 else "warning",
            "free_space_gb": free_space / (1024**3),
            "usage_percent": usage_percent
        }
```

### Metrics Collection
```python
class MetricsCollector:
    """System metrics collection."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics = {}
        self.collection_interval = config.get("collection_interval", 60)
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect system metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "system": self._collect_system_metrics(),
            "application": self._collect_application_metrics(),
            "performance": self._collect_performance_metrics()
        }
        
        self.metrics = metrics
        return metrics
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect system-level metrics."""
        import psutil
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "network_io": psutil.net_io_counters()._asdict()
        }
```

## Scalability Architecture

### Horizontal Scaling
```python
class LoadBalancer:
    """Load balancing for horizontal scaling."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.workers = config.get("workers", [])
        self.current_worker = 0
    
    def get_next_worker(self) -> str:
        """Get next available worker using round-robin."""
        if not self.workers:
            raise RuntimeError("No workers available")
        
        worker = self.workers[self.current_worker]
        self.current_worker = (self.current_worker + 1) % len(self.workers)
        
        return worker
    
    def add_worker(self, worker: str) -> None:
        """Add new worker to the pool."""
        if worker not in self.workers:
            self.workers.append(worker)
    
    def remove_worker(self, worker: str) -> None:
        """Remove worker from the pool."""
        if worker in self.workers:
            self.workers.remove(worker)
            if self.current_worker >= len(self.workers):
                self.current_worker = 0
```

### Vertical Scaling
```python
class ResourceManager:
    """Resource management for vertical scaling."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_memory = config.get("max_memory_mb", 1024) * 1024 * 1024
        self.max_cpu_percent = config.get("max_cpu_percent", 80)
    
    def check_resources(self) -> Dict[str, Any]:
        """Check current resource usage."""
        import psutil
        
        memory_usage = psutil.virtual_memory()
        cpu_usage = psutil.cpu_percent(interval=1)
        
        return {
            "memory": {
                "used_mb": memory_usage.used / (1024**2),
                "available_mb": memory_usage.available / (1024**2),
                "percent": memory_usage.percent
            },
            "cpu": {
                "percent": cpu_usage
            },
            "status": self._get_resource_status(memory_usage, cpu_usage)
        }
    
    def _get_resource_status(self, memory_usage, cpu_usage) -> str:
        """Get overall resource status."""
        if (memory_usage.percent > 90 or cpu_usage > 90):
            return "critical"
        elif (memory_usage.percent > 80 or cpu_usage > 80):
            return "warning"
        else:
            return "healthy"
```

## Deployment Architecture

### Container Architecture
```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 neozork && chown -R neozork:neozork /app
USER neozork

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src; print('OK')"

# Run application
CMD ["python", "-m", "src.cli.core.cli"]
```

### Kubernetes Architecture
```yaml
# neozork-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neozork
spec:
  replicas: 3
  selector:
    matchLabels:
      app: neozork
  template:
    metadata:
      labels:
        app: neozork
    spec:
      containers:
      - name: neozork
        image: neozork:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
```

## Future Architecture Considerations

### Microservices Architecture
- **Service Decomposition**: Break down into smaller, focused services
- **API Gateway**: Centralized API management
- **Service Discovery**: Dynamic service registration and discovery
- **Circuit Breaker**: Fault tolerance and resilience patterns

### Event-Driven Architecture
- **Event Sourcing**: Store all changes as events
- **CQRS**: Command Query Responsibility Segregation
- **Message Queues**: Asynchronous communication between services
- **Event Streaming**: Real-time data processing pipelines

### Cloud-Native Architecture
- **Serverless Functions**: Event-driven, scalable compute
- **Managed Services**: Use cloud provider services
- **Auto-scaling**: Automatic resource scaling
- **Multi-region**: Geographic distribution for performance

## Best Practices

### Code Organization
1. **Module Separation**: Keep modules focused and cohesive
2. **Interface Contracts**: Define clear interfaces between components
3. **Dependency Management**: Minimize and manage dependencies
4. **Configuration Externalization**: Keep configuration separate from code
5. **Error Handling**: Implement comprehensive error handling

### Performance
1. **Caching Strategy**: Implement appropriate caching at multiple levels
2. **Async Processing**: Use asynchronous operations where appropriate
3. **Resource Management**: Efficiently manage memory and CPU usage
4. **Monitoring**: Implement comprehensive performance monitoring
5. **Optimization**: Profile and optimize critical paths

### Security
1. **Input Validation**: Validate and sanitize all inputs
2. **Access Control**: Implement proper access control mechanisms
3. **Secure Configuration**: Protect sensitive configuration data
4. **Audit Logging**: Log security-relevant events
5. **Regular Updates**: Keep dependencies and system updated

### Testing
1. **Test Coverage**: Maintain high test coverage
2. **Test Isolation**: Ensure tests are independent and repeatable
3. **Performance Testing**: Include performance tests in CI/CD
4. **Integration Testing**: Test component interactions
5. **Automated Testing**: Automate all testing processes

## Support and Resources

### Architecture Resources
- **Design Patterns**: Review common software design patterns
- **System Design**: Study large-scale system design principles
- **Performance**: Learn about performance optimization techniques
- **Security**: Understand security best practices

### Getting Help
- **Documentation**: Review architecture documentation
- **Code Reviews**: Participate in architecture-focused code reviews
- **Design Sessions**: Attend architecture design sessions
- **Community**: Engage with the development community
