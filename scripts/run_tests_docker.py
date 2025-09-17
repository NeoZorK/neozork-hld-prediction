#!/usr/bin/env python3
"""
Docker-specific test runner for NeoZork HLD Prediction

This script runs tests in Docker environment with proper configuration
to avoid worker crashes and resource issues.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_tests_docker():
    """Run tests in Docker environment with proper configuration."""
    
    # Check if we're in Docker
    is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER', False)
    
    if is_docker:
        logger.info("Running in Docker environment - using single-threaded mode")
        
        # Set environment variables for Docker
        env = os.environ.copy()
        env.update({
            'PYTHONPATH': '/app',
            'PYTHONUNBUFFERED': '1',
            'DOCKER_CONTAINER': 'true',
            'MPLBACKEND': 'Agg',  # Use non-interactive matplotlib backend
            'DISPLAY': '',  # Disable X11
        })
        
        # Run tests without parallel execution using Docker-specific config
        cmd = [
            'uv', 'run', 'pytest', 
            'tests/pocket_hedge_fund/', 
            '-c', 'pytest-docker.ini'
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, env=env, cwd='/app', capture_output=False)
            return result.returncode
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return 1
    else:
        logger.info("Running in local environment - using parallel mode")
        
        # Run tests with parallel execution for local development
        cmd = [
            'uv', 'run', 'pytest', 
            'tests/pocket_hedge_fund/', 
            '-n', 'auto',
            '-v', 
            '--tb=short',
            '--disable-warnings',
            '--no-header',
            '--no-summary',
            '--maxfail=1',
            '--timeout=300',
            '--timeout-method=thread'
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=False)
            return result.returncode
        except Exception as e:
            logger.error(f"Error running tests: {e}")
            return 1

def main():
    """Main entry point."""
    logger.info("Starting Docker-specific test runner")
    
    exit_code = run_tests_docker()
    
    if exit_code == 0:
        logger.info("All tests passed!")
    else:
        logger.error(f"Tests failed with exit code: {exit_code}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
