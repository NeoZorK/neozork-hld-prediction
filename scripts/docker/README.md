# Docker Scripts

This directory contains scripts for testing and managing Docker containers for the NeoZork HLD Prediction project.

## Scripts

### test_docker_history.sh
Tests the bash history functionality in Docker containers.
- **Usage**: `./test_docker_history.sh`
- **Purpose**: Starts an interactive Docker container to test arrow key navigation and command history

### test_history_auto.sh
Automatically tests the history initialization in Docker containers.
- **Usage**: `./test_history_auto.sh`
- **Purpose**: Runs automated tests to verify that bash history is properly initialized

### docker-test-workflows.sh
Tests GitHub Actions workflows locally using act.
- **Usage**: `./docker-test-workflows.sh`
- **Purpose**: Runs CI/CD workflows locally for testing before pushing to GitHub

## Requirements

- Docker installed and running
- act (for workflow testing): https://github.com/nektos/act
- Bash shell

## Usage

All scripts can be run from any directory and will automatically find the project root:

```bash
# From project root
./scripts/docker/test_docker_history.sh

# From any subdirectory
cd src/
../scripts/docker/test_docker_history.sh
```

## Notes

- Scripts automatically detect the project root directory
- All paths are resolved relative to the project root
- Scripts work on both Intel and Apple Silicon Macs 