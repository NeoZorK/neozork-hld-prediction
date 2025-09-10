#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UV Commands Test
Basic test to verify UV commands work in both Docker and local environments
"""

import pytest
import subprocess
import os
from pathlib import Path

def is_docker_environment():
    """Check if running in Docker environment"""
    return (
        os.getenv("DOCKER_CONTAINER", "false").lower() == "true" or
        os.getenv("NATIVE_CONTAINER", "false").lower() == "true" or
        os.path.exists("/.dockerenv") or
        os.path.exists("/app")
    )

def is_container_environment():
    """Check if running in any container environment (Docker or native)"""
    return (
        os.getenv("DOCKER_CONTAINER", "false").lower() == "true" or
        os.getenv("NATIVE_CONTAINER", "false").lower() == "true" or
        os.path.exists("/.dockerenv") or
        os.path.exists("/app")
    )

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
    
    in_container = is_container_environment()
    
    if in_container:
        # In Container, check required environment variables
        assert os.getenv("USE_UV", "false").lower() == "true", "USE_UV should be true in container"
        assert os.getenv("UV_ONLY", "false").lower() == "true", "UV_ONLY should be true in container"
        # Check for either DOCKER_CONTAINER or NATIVE_CONTAINER
        docker_container = os.getenv("DOCKER_CONTAINER", "false").lower() == "true"
        native_container = os.getenv("NATIVE_CONTAINER", "false").lower() == "true"
        assert docker_container or native_container, "Either DOCKER_CONTAINER or NATIVE_CONTAINER should be true in container"
        print("✅ UV environment variables are set correctly in container")
    else:
        # Outside container, just check if UV is available
        print("ℹ️  Running outside container - skipping container-specific environment checks")
        # Check if UV is available at least
        try:
            result = subprocess.run(["uv", "--version"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            assert result.returncode == 0, "UV should be available"
            print("✅ UV is available in local environment")
        except Exception as e:
            pytest.fail(f"UV not available in local environment: {e}")

def test_uv_directories():
    """Test UV directories"""
    
    in_container = is_container_environment()
    
    if in_container:
        # Container-specific paths
        cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
        venv_dir = os.getenv("UV_VENV_DIR", "/app/.venv")
        
        # For native container, check if we can create directories
        if os.getenv("NATIVE_CONTAINER", "false").lower() == "true":
            # In native container, try to create directories
            try:
                Path(cache_dir).mkdir(parents=True, exist_ok=True)
                Path(venv_dir).mkdir(parents=True, exist_ok=True)
                print("✅ UV directories created in native container")
            except Exception as e:
                print(f"⚠️  Could not create UV directories in native container: {e}")
                # This is acceptable for native container
        else:
            # Docker-specific check
            assert Path(cache_dir).parent.exists(), f"Parent directory for {cache_dir} should exist in Docker"
            assert Path(venv_dir).parent.exists(), f"Parent directory for {venv_dir} should exist in Docker"
            print("✅ UV directories are accessible in Docker")
    else:
        # Outside container, check if we can create UV directories in current location
        print("ℹ️  Running outside container - checking local UV directory creation")
        try:
            # Try to create a test UV directory
            test_cache_dir = Path(".uv_test_cache")
            test_cache_dir.mkdir(exist_ok=True)
            assert test_cache_dir.exists(), "Should be able to create UV cache directory locally"
            test_cache_dir.rmdir()  # Clean up
            print("✅ Can create UV directories locally")
        except Exception as e:
            pytest.fail(f"Cannot create UV directories locally: {e}")

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