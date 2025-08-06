#!/usr/bin/env python3
"""
Test container startup functionality
This script tests the container initialization process
"""

import os
import sys
import subprocess
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_container_startup():
    """Test container startup process"""
    logger.info("=== Testing Container Startup ===")
    
    # Check if we're in a container
    if os.path.exists('/.dockerenv') or os.path.exists('/proc/1/cgroup'):
        logger.info("✅ Running inside container")
    else:
        logger.info("⚠️  Not running inside container")
    
    # Check environment variables
    env_vars = [
        'USE_UV', 'UV_ONLY', 'NATIVE_CONTAINER', 'DOCKER_CONTAINER',
        'PYTHONUNBUFFERED', 'PYTHONDONTWRITEBYTECODE', 'MPLCONFIGDIR',
        'DEBIAN_FRONTEND', 'APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE'
    ]
    
    logger.info("=== Environment Variables ===")
    for var in env_vars:
        value = os.environ.get(var, 'NOT_SET')
        logger.info(f"{var}: {value}")
    
    # Check if UV is available
    logger.info("=== UV Package Manager Check ===")
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            logger.info(f"✅ UV is available: {result.stdout.strip()}")
        else:
            logger.error(f"❌ UV check failed: {result.stderr}")
    except FileNotFoundError:
        logger.error("❌ UV not found")
    except subprocess.TimeoutExpired:
        logger.error("❌ UV check timed out")
    
    # Check Python environment
    logger.info("=== Python Environment Check ===")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Python path: {sys.path[:3]}...")
    
    # Check if virtual environment exists
    venv_path = "/app/.venv"
    if os.path.exists(venv_path):
        logger.info(f"✅ Virtual environment exists at {venv_path}")
        
        # Check if venv is activated
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            logger.info("✅ Virtual environment is activated")
        else:
            logger.warning("⚠️  Virtual environment exists but not activated")
    else:
        logger.warning(f"⚠️  Virtual environment not found at {venv_path}")
    
    # Check key directories
    logger.info("=== Directory Check ===")
    key_dirs = [
        '/app/data', '/app/logs', '/app/results', '/app/tests',
        '/app/src', '/app/scripts', '/app/mql5_feed'
    ]
    
    for dir_path in key_dirs:
        if os.path.exists(dir_path):
            logger.info(f"✅ Directory exists: {dir_path}")
        else:
            logger.warning(f"⚠️  Directory missing: {dir_path}")
    
    # Check key files
    logger.info("=== File Check ===")
    key_files = [
        '/app/run_analysis.py', '/app/neozork_mcp_server.py',
        '/app/requirements.txt', '/app/uv.toml'
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            logger.info(f"✅ File exists: {file_path}")
        else:
            logger.warning(f"⚠️  File missing: {file_path}")
    
    # Test basic Python imports
    logger.info("=== Python Import Test ===")
    test_imports = ['os', 'sys', 'logging', 'subprocess']
    
    for module in test_imports:
        try:
            __import__(module)
            logger.info(f"✅ Import successful: {module}")
        except ImportError as e:
            logger.error(f"❌ Import failed: {module} - {e}")
    
    logger.info("=== Container Startup Test Completed ===")
    return True

if __name__ == "__main__":
    try:
        test_container_startup()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Container startup test failed: {e}")
        sys.exit(1) 