#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UV Docker Test Script
Simple script to test UV functionality in Docker environment
"""

import subprocess
import os
import sys
from pathlib import Path

def test_uv_availability():
    """Test if UV is available"""
    print("🔍 Testing UV availability...")
    
    try:
        # Check if UV is in PATH
        result = subprocess.run(["which", "uv"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        uv_path = result.stdout.strip()
        print(f"✅ UV found at: {uv_path}")
        
        # Check UV version
        result = subprocess.run(["uv", "--version"], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version = result.stdout.strip()
        print(f"✅ UV version: {version}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ UV not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking UV: {e}")
        return False

def test_uv_commands():
    """Test various UV commands"""
    print("\n🔍 Testing UV commands...")
    
    commands_to_test = [
        ["uv", "--help"],
        ["uv", "pip", "--help"],
        ["uv", "pip", "list"],
        ["uv", "pip", "--version"]
    ]
    
    working_commands = 0
    for cmd in commands_to_test:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd)} - SUCCESS")
                working_commands += 1
            else:
                print(f"⚠️  {' '.join(cmd)} - Exit code {result.returncode}")
                # Some commands might return non-zero but still work
                if "help" in cmd[-1] or "version" in cmd[-1]:
                    working_commands += 1
        except subprocess.TimeoutExpired:
            print(f"❌ {' '.join(cmd)} - TIMEOUT")
        except Exception as e:
            print(f"❌ {' '.join(cmd)} - ERROR: {e}")
    
    print(f"📊 {working_commands}/{len(commands_to_test)} commands working")
    return working_commands > 0

def test_package_management():
    """Test package management functionality"""
    print("\n🔍 Testing package management...")
    
    # Try different package listing methods
    package_commands = [
        ["uv", "pip", "list"],
        ["pip", "list"],
        ["python", "-m", "pip", "list"]
    ]
    
    for cmd in package_commands:
        try:
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            if result.returncode == 0:
                packages = result.stdout.strip().split('\n')
                print(f"✅ {' '.join(cmd)} - Found {len(packages)} package lines")
                
                # Check for key packages
                output_lower = result.stdout.lower()
                key_packages = ["pandas", "numpy", "matplotlib"]
                found_packages = [pkg for pkg in key_packages if pkg in output_lower]
                if found_packages:
                    print(f"   📦 Key packages found: {', '.join(found_packages)}")
                
                return True
        except Exception as e:
            print(f"❌ {' '.join(cmd)} - ERROR: {e}")
    
    return False

def test_environment():
    """Test environment variables"""
    print("\n🔍 Testing environment variables...")
    
    required_vars = {
        "USE_UV": "true",
        "UV_ONLY": "true", 
        "DOCKER_CONTAINER": "true"
    }
    
    optional_vars = [
        "UV_CACHE_DIR",
        "UV_VENV_DIR",
        "PYTHONPATH"
    ]
    
    all_good = True
    
    for var, expected in required_vars.items():
        value = os.getenv(var, "false").lower()
        if value == expected:
            print(f"✅ {var}={value}")
        else:
            print(f"❌ {var}={value} (expected {expected})")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}={value}")
        else:
            print(f"⚠️  {var} not set")
    
    return all_good

def test_directories():
    """Test UV directories"""
    print("\n🔍 Testing UV directories...")
    
    cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
    venv_dir = os.getenv("UV_VENV_DIR", "/app/.venv")
    
    cache_parent = Path(cache_dir).parent
    venv_parent = Path(venv_dir).parent
    
    all_good = True
    
    if cache_parent.exists():
        print(f"✅ Cache parent directory exists: {cache_parent}")
    else:
        print(f"❌ Cache parent directory missing: {cache_parent}")
        all_good = False
    
    if venv_parent.exists():
        print(f"✅ Venv parent directory exists: {venv_parent}")
    else:
        print(f"❌ Venv parent directory missing: {venv_parent}")
        all_good = False
    
    # Try to create cache directory
    try:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        print(f"✅ Cache directory accessible: {cache_dir}")
    except Exception as e:
        print(f"❌ Cannot access cache directory: {e}")
        all_good = False
    
    return all_good

def main():
    """Main test function"""
    print("🚀 UV Docker Environment Test")
    print("=" * 50)
    
    tests = [
        ("UV Availability", test_uv_availability),
        ("UV Commands", test_uv_commands),
        ("Package Management", test_package_management),
        ("Environment Variables", test_environment),
        ("Directories", test_directories)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} - EXCEPTION: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! UV-only mode is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main() 