# Container Documentation

This section contains comprehensive documentation for all container-related functionality in the NeoZork HLD Prediction project.

## Overview

The project supports multiple container environments to ensure consistent development and deployment across different platforms:

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

- **Native Container**: Apple Silicon optimized container for macOS 26+ (limited to v0.5.2 and earlier versions)
- **Docker Container**: Cross-platform container for all operating systems (limited to v0.5.2 and earlier versions)

## Quick Navigation

### Native Container
- [Native Container Setup](native-container-setup.md) - Complete setup guide
- [Native Container Features](native-container-features.md) - Feature overview
- [Native Container README](native-container/README.md) - Detailed documentation
- [Docker Parity Summary](native-container/FULL_DOCKER_PARITY_SUMMARY.md) - Feature parity details
- [Smart Container Logic](native-container/SMART_CONTAINER_LOGIC.md) - Intelligent container management

### Docker Container
- [Docker Setup](docker-setup.md) - Docker container setup
- [Docker Troubleshooting](docker-troubleshooting.md) - Common issues and solutions
- [Docker Changes Summary](DOCKER_CHANGES_SUMMARY.md) - Recent changes

### Comparison & Analysis
- [Native vs Docker Comparison](native-vs-docker-comparison.md) - Performance and feature comparison
- [UV Only Mode](uv-only-mode.md) - UV package manager configuration
- [Automatic Dependencies](automatic-dependencies.md) - Dependency management

### Implementation Details
- [Native Container Implementation](NATIVE_CONTAINER_IMPLEMENTATION_SUMMARY.md) - Technical implementation
- [Native Container Fixes](NATIVE_CONTAINER_FIXES_SUMMARY.md) - Bug fixes and improvements
- [Smart Container Logic Summary](native-container/SMART_CONTAINER_LOGIC_SUMMARY.md) - Logic implementation

## Container Architecture

### Native Container
- **Platform**: macOS 26+ (Tahoe) with Apple Silicon optimization
- **Performance**: 30-50% faster than Docker on Apple Silicon
- **Features**: Full Docker parity with enhanced macOS integration
- **Package Manager**: UV-only mode for consistent dependency management
- **Version Support**: Limited to v0.5.2 and earlier versions

### Docker Container
- **Platform**: Cross-platform (Linux, macOS, Windows)
- **Performance**: Standard Docker performance
- **Features**: Complete development environment
- **Package Manager**: UV package manager support
- **Version Support**: Limited to v0.5.2 and earlier versions

## Getting Started

### For macOS Users (Apple Silicon)
> **Note**: Native Container support is limited to v0.5.2 and earlier versions.

1. [Native Container Setup](native-container-setup.md) - Recommended for best performance
2. [Native Container Features](native-container-features.md) - Understand available features

### For Other Platforms
> **Note**: Docker Container support is limited to v0.5.2 and earlier versions.

1. [Docker Setup](docker-setup.md) - Cross-platform solution
2. [Docker Troubleshooting](docker-troubleshooting.md) - Common setup issues

## Advanced Topics

### Container Management
- [Smart Container Logic](native-container/SMART_CONTAINER_LOGIC.md) - Intelligent container state management
- [Emergency Restart](EMERGENCY_RESTART_IMPLEMENTATION.md) - Emergency container recovery
- [Force Restart](force-restart-container.md) - Force container restart procedures

### Development Workflow
- [UV Only Mode](uv-only-mode.md) - Package manager configuration
- [Automatic Dependencies](automatic-dependencies.md) - Dependency management automation
- [Testing](../development/testing.md) - Container testing procedures

## Troubleshooting

### Common Issues
- [Docker Troubleshooting](docker-troubleshooting.md) - Docker-specific issues
- [Native Container Fixes](NATIVE_CONTAINER_FIXES_SUMMARY.md) - Native container issues
- [Emergency Procedures](EMERGENCY_RESTART_IMPLEMENTATION.md) - Emergency recovery

### Performance Optimization
- [Native vs Docker Comparison](native-vs-docker-comparison.md) - Performance analysis
- [UV Only Mode](uv-only-mode.md) - Package manager optimization

## Related Documentation

- [Getting Started](../getting-started/) - Project setup and introduction
- [Development](../development/) - Development workflow and tools
- [Deployment](../deployment/) - Production deployment guides
- [API Reference](../api/) - API documentation
- [Examples](../examples/) - Usage examples and tutorials 