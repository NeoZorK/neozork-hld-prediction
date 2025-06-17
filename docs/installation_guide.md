# Installation Legacy Documentation

⚠️ **Note:** This file has been superseded by the new documentation structure. Please refer to [docs/installation.md](installation.md) for current installation documentation.

## Quick Reference

For current installation instructions, see:
- [Installation Guide](installation.md) - Complete setup instructions
- [Quick Start](quick-start.md) - Fast setup guide
- [UV Setup](uv-setup.md) - Fast package manager setup

## Migration Notice

This file is kept for reference but may be outdated. The new documentation provides:
- More comprehensive installation steps
- Better organization and structure  
- Updated commands and requirements
- Integration with UV package manager
11. Sync new libraries with uv:
    ```bash
    uv sync
    ```
12. Install dependencies from pyproject.toml
13. Install current project:
    ```bash
    uv pip install .
    ```
14. Create pyproject.toml automatically by running script:
    ```bash
    python scripts/auto_pyproject_from_requirements.py
    ```

### Testing the Installation

15. Try running the following commands to ensure everything is set up correctly:
    ```bash
    uv run run_analysis.py -h
    uv run src/eda/eda_batch_check.py -h
    uv run pytest tests/cli/test_cli_all_commands.py
    ```

### Additional Configuration

16. Copy the `.env` file to the root folder (contains API keys for Polygon, Binance)

### Docker Setup and Testing

17. Build the Docker image:
    ```bash
    docker compose build --build-arg USE_UV=true
    ```
18. Test Docker run:
    ```bash
    docker compose run --rm neozork-hld
    ```

### Testing Inside Docker

19. Test demo:
    ```bash
    python run_analysis.py demo -d term --rule PHLD
    ```
20. Test showing all fields:
    ```bash
    python run_analysis.py show csv mn1 --rule AUTO
    ```
21. Test nz:
    ```bash
    nz show
    ```
22. Test eda:
    ```bash
    eda -h
    ```

### Additional Docker Testing

23. Start Docker and run help command, then close Docker:
    ```bash
    ./nz -h
    ```
24. Start Docker and run eda help command, then close Docker:
    ```bash
    ./eda -h
    ```
25. Test GitHub Actions workflow:
    ```bash
    ./test-workflow.py
    ```

## Completion

Once all the above steps are completed successfully, your development environment should be properly set up and ready for use.
