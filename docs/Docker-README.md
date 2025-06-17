# Docker Legacy Documentation

⚠️ **Note:** This file has been superseded by the new documentation structure. Please refer to [docs/docker.md](docker.md) for current Docker documentation.

## Quick Reference

For current Docker usage, see:
- [Docker Guide](docker.md) - Complete Docker setup and usage
- [Quick Start](quick-start.md) - Get started with Docker
- [Installation](installation.md) - Initial setup including Docker

## Migration Notice

This file is kept for reference but may be outdated. The new documentation provides:
- More comprehensive Docker coverage
- Better organization and structure
- Updated commands and examples
- Integration with other project tools

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

