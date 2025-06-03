# GitHub Copilot Instructions for NeoZorK HLD Prediction Project

## Project Overview

This project aims to enhance the predictive capabilities of a proprietary trading indicator using Machine Learning methods. The key goal is to forecast High, Low, and Direction (HLD) for financial instruments.

## Docker and CI/CD Usage Guide

### Docker Setup and Usage

1. **Building the Docker Image**:
   ```bash
   docker build -t neozork-hld-prediction .
   ```

2. **Running the Container**:
   ```bash
   docker run -it --rm -v $(pwd):/app neozork-hld-prediction
   ```

3. **Using Docker Compose**:
   ```bash
   docker-compose up
   ```
   
   To run in detached mode:
   ```bash
   docker-compose up -d
   ```
   
   To stop the services:
   ```bash
   docker-compose down
   ```

### Running Test Workflow

The project includes a test workflow script (`test-workflow.sh`) that automates various testing and validation processes:

1. **Make the script executable** (if not already):
   ```bash
   chmod +x test-workflow.sh
   ```

2. **Run the full test workflow**:
   ```bash
   ./test-workflow.sh
   ```

3. **Run specific test components**:
   ```bash
   ./test-workflow.sh --unit-tests
   ./test-workflow.sh --integration-tests
   ./test-workflow.sh --performance-tests
   ```

### Testing GitHub Actions Locally with Act

[Act](https://github.com/nektos/act) allows you to run GitHub Actions workflows locally. This is useful for testing workflows without pushing to GitHub.

1. **Installation** (on macOS using Homebrew):
   ```bash
   brew install act
   ```

2. **Running GitHub Actions Locally**:
   
   To run all actions defined in `.github/workflows/`:
   ```bash
   act
   ```
   
   To run a specific workflow:
   ```bash
   act -W .github/workflows/specific-workflow.yml
   ```
   
   To run a specific job within a workflow:
   ```bash
   act -j job_name
   ```
   
   To list all available actions without running them:
   ```bash
   act -l
   ```

3. **Environment Setup for Act**:
   
   Create a `.env` file in the project root with necessary environment variables:
   ```
   API_KEY=your_api_key
   DATABASE_URL=your_db_url
   ```
   
   Then run act with the environment file:
   ```bash
   act --env-file .env
   ```

## Code Style Guidelines

When writing code for this project, please adhere to the following principles:

- Use PEP 8 for Python code formatting
- Document functions and classes with docstrings in Google or NumPy format
- Write modular code with clear separation of concerns
- Include typing with Python type annotations
- Handle exceptions and add logging for critical operations

## Project Structure

```
/
├── data/               # Directory for data storage
│   ├── cache/          # Cached data
│   └── raw_parquet/    # Raw data in parquet format
├── logs/               # System logs
├── mql5_feed/          # Data exported from MT5
├── results/            # Model results
│   └── plots/          # Visualizations
├── scripts/            # Helper scripts
├── src/                # Project source code
└── tests/              # Unit and integration tests
```

## Workflow

1. Data loading and processing
2. Indicator replication in Python
3. Development of basic ML models
4. Model improvement through feature engineering and hyperparameters
5. Validation using strict methods
6. Backtesting on historical data
7. Optimization for real-world use
