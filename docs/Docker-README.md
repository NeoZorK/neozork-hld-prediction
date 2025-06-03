# Docker Configuration Guide

This document provides information about the Docker setup for the NeoZork HLD Prediction project.

## Docker Files Structure

All Docker-related files are organized in the root directory:

- `Dockerfile` - The main Dockerfile for building the application image
- `docker-entrypoint.sh` - Entrypoint script that configures and runs the application inside the container
- `docker-compose.yml` - File for Docker Compose configuration

## Building and Running

To build and run the application using Docker:

```bash
# Build the Docker image
docker-compose build

# Run the application
docker-compose up
```

# Run with interactive shell
```bash
docker-compose run --rm neozork
```

# To stop the application
```shell  
CTRL+D
```

## Container Configuration

The Docker container is configured with the following features:

- Python 3.11 environment with optimized dependencies using uv
- Non-root user (neozork) for improved security
- Interactive CLI with command history and tab completion
- Bind mounts for data, logs, and results directories
- Support for running tests for external data feeds
- Optional MCP service for enhanced LLM support
- uv for faster execution of Python scripts

## Local Development Utilities

The following scripts are available for local development:

- `nz` - Wrapper script for executing run_analysis.py either locally or in a container
- `eda` - Wrapper script for executing EDA scripts either locally or in a container
- `test-workflow.sh` - Script for testing GitHub Actions workflow locally

# Run the application with the `nz` script: (same as `python run_analysis.py demo --rule PHLD`)

```bash
./nz demo --rule PHLD
```

# Run the application with the `eda` script: (same as `python src/eda/eda_batch_check.py -h`)

```bash  
./eda -h
```

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

4. **Test Docker Github Actions workflow locally**

   Use the `test-workflow.sh` script to test the GitHub Actions workflow locally:
   
   ```bash
   ./test-workflow.sh
   ```

5. **Run PyTest tests in the container**

   To run PyTest tests inside the container, use the following command:
   
   ```bash
   pytest tests
   ```

6. **Using uv with Docker**

   This project supports using `uv` (a faster Python package installer) with Docker. To leverage uv in your Docker workflow:
   
   ```bash
   # Build the Docker image with uv enabled
   docker-compose build --build-arg USE_UV=true
   
   # Or run the container with uv enabled
   docker-compose up -d --build-arg USE_UV=true
   ```
   
 ### or modern docker-compose syntax
   ```bash
   docker compose build --build-arg USE_UV=true
   ```
   
   Using uv significantly improves package installation speed during Docker builds. The container automatically detects and uses uv when enabled.
   
   For more information about uv, see the documentation in `docs/uv-migration.md`.

