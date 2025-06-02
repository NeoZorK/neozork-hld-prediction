#!/bin/bash
# Script for testing GitHub Actions workflow locally using act
# Before running this script, ensure you have Docker and act installed.
# act: https://github.com/nektos/act

# Run the workflow defined in .github/workflows/build.yml
echo "Running GitHub Actions workflow locally using act..."
act -j build
