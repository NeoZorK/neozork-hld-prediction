# Docker Configuration Guide

This document provides information about the Docker setup for the NeoZork HLD Prediction project.

## Docker Files Structure

All Docker-related files are organized in the `docker/` directory:

- `docker/Dockerfile` - The main Dockerfile for building the application image
- `docker/docker-entrypoint.sh` - Entrypoint script that configures and runs the application inside the container

The `docker-compose.yml` file remains in the root directory for easier access.

## Building and Running

To build and run the application using Docker:

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up
```

## Container Configuration

The Docker container is configured with the following features:

- Python 3.11 environment with optimized dependencies using uv
- Non-root user (neozork) for improved security
- Interactive CLI with command history and tab completion
- Bind mounts for data, logs, and results directories
- Support for running tests for external data feeds
- Optional MCP service for enhanced LLM support

## Local Development Utilities

The following scripts are available for local development:

- `nz` - Wrapper script for executing run_analysis.py either locally or in a container
- `eda` - Wrapper script for executing EDA scripts either locally or in a container
- `test-workflow.sh` - Script for testing GitHub Actions workflow locally

## Development Tips

1. **Working with docker-compose.yml in root directory**
   
   The docker-compose.yml file is kept in the root directory to maintain compatibility with the local development scripts (`nz` and `eda`). These scripts check for the presence of docker-compose.yml in the current directory.

2. **Making changes to Docker configuration**

   When making changes to Docker configuration files, always test them with a full build:
   
   ```bash
   docker-compose build --no-cache
   ```

3. **Using the container interactively**

   The container supports an interactive shell with history and tab completion. To use it:
   
   ```bash
   docker-compose up
   ```
   
   Then follow the on-screen prompts to interact with the application.
