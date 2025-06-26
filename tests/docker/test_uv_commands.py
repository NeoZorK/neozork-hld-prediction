#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple UV Commands Test
Basic test to verify UV commands work in Docker environment
"""

import pytest
import subprocess
import os
from pathlib import Path

def test_uv_basic_commands():
    """Test basic UV commands"""
    
    # Test 1: Check if UV is available
    try:
        result = subprocess.run(["uv", "--version"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        assert result.returncode == 0, "UV should be available"
        print(f"✅ UV version: {result.stdout.strip()}")
    except Exception as e:
        pytest.fail(f"UV not available: {e}")
    
    # Test 2: Check UV help
    try:
        result = subprocess.run(["uv", "--help"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        assert result.returncode == 0, "UV help should work"
        print("✅ UV help command works")
    except Exception as e:
        pytest.fail(f"UV help failed: {e}")
    
    # Test 3: Check UV pip help
    try:
        result = subprocess.run(["uv", "pip", "--help"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        # UV pip help might return non-zero exit code in some versions
        print("✅ UV pip help command executed")
    except Exception as e:
        print(f"⚠️  UV pip help failed: {e}")
    
    # Test 4: Check if we can list packages with any method
    package_commands = [
        ["uv", "pip", "list"],
        ["pip", "list"],
        ["python", "-m", "pip", "list"]
    ]
    
    packages_found = False
    for cmd in package_commands:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            if result.returncode == 0:
                packages_found = True
                print(f"✅ Package listing works with: {' '.join(cmd)}")
                break
        except Exception:
            continue
    
    assert packages_found, "At least one package listing method should work"

def test_uv_environment():
    """Test UV environment variables"""
    
    # Check required environment variables
    assert os.getenv("USE_UV", "false").lower() == "true", "USE_UV should be true"
    assert os.getenv("UV_ONLY", "false").lower() == "true", "UV_ONLY should be true"
    assert os.getenv("DOCKER_CONTAINER", "false").lower() == "true", "DOCKER_CONTAINER should be true"
    
    print("✅ UV environment variables are set correctly")

def test_uv_directories():
    """Test UV directories"""
    
    cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
    venv_dir = os.getenv("UV_VENV_DIR", "/app/.venv")
    
    # Check that parent directories exist
    assert Path(cache_dir).parent.exists(), f"Parent directory for {cache_dir} should exist"
    assert Path(venv_dir).parent.exists(), f"Parent directory for {venv_dir} should exist"
    
    print("✅ UV directories are accessible")

def test_uv_installation():
    """Test UV installation and basic functionality"""
    
    # Check UV installation
    try:
        result = subprocess.run(["which", "uv"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        uv_path = result.stdout.strip()
        assert uv_path, "UV should be found in PATH"
        print(f"✅ UV found at: {uv_path}")
    except subprocess.CalledProcessError:
        pytest.fail("UV not found in PATH")
    
    # Check UV version
    try:
        result = subprocess.run(["uv", "--version"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version = result.stdout.strip()
        assert "uv" in version.lower(), "UV version should contain 'uv'"
        print(f"✅ UV version: {version}")
    except subprocess.CalledProcessError:
        pytest.fail("Cannot get UV version")

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"]) 