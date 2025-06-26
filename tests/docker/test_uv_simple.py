#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple UV Test for Docker
Very basic test that should work in any Docker environment with UV
"""

import pytest
import subprocess
import os

def test_uv_exists():
    """Test that UV exists and can be called"""
    try:
        result = subprocess.run(["uv", "--version"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        # UV should return version info
        assert result.returncode == 0, "UV should return exit code 0"
        assert "uv" in result.stdout.lower(), "UV version should contain 'uv'"
        print(f"✅ UV version: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"UV not working: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("UV command timed out")
    except Exception as e:
        pytest.fail(f"Error testing UV: {e}")

def test_uv_help():
    """Test that UV help works"""
    try:
        result = subprocess.run(["uv", "--help"], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        assert result.returncode == 0, "UV help should return exit code 0"
        print("✅ UV help works")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"UV help not working: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("UV help command timed out")
    except Exception as e:
        pytest.fail(f"Error testing UV help: {e}")

def test_environment_variables():
    """Test that UV environment variables are set"""
    assert os.getenv("USE_UV", "false").lower() == "true", "USE_UV should be true"
    assert os.getenv("UV_ONLY", "false").lower() == "true", "UV_ONLY should be true"
    assert os.getenv("DOCKER_CONTAINER", "false").lower() == "true", "DOCKER_CONTAINER should be true"
    print("✅ UV environment variables are set correctly")

def test_package_listing():
    """Test that we can list packages somehow"""
    # Try multiple methods to list packages
    methods = [
        ["uv", "pip", "list"],
        ["pip", "list"],
        ["python", "-m", "pip", "list"]
    ]
    
    success = False
    for method in methods:
        try:
            result = subprocess.run(method, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            if result.returncode == 0:
                success = True
                print(f"✅ Package listing works with: {' '.join(method)}")
                break
        except Exception:
            continue
    
    assert success, "At least one package listing method should work"

if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"]) 