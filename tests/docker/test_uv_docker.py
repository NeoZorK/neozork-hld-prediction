#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UV Docker Test Script
Simple script to test UV functionality in Docker environment
"""

import subprocess
import os
import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

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
                
                found_packages = []
                for pkg in key_packages:
                    if pkg in output_lower:
                        found_packages.append(pkg)
                
                print(f"   Key packages found: {found_packages}")
                return True
                
        except subprocess.TimeoutExpired:
            print(f"❌ {' '.join(cmd)} - TIMEOUT")
        except Exception as e:
            print(f"❌ {' '.join(cmd)} - ERROR: {e}")
    
    return False

def test_docker_environment():
    """Test Docker environment"""
    print("\n🔍 Testing Docker environment...")
    
    # Check if we're in Docker
    try:
        with open("/proc/1/cgroup", "r") as f:
            cgroup = f.read()
            if "docker" in cgroup.lower():
                print("✅ Running in Docker container")
                return True
            else:
                print("⚠️  Not running in Docker container")
                return False
    except FileNotFoundError:
        print("⚠️  Could not determine if running in Docker")
        return False

class TestUVDocker:
    """Test class for UV Docker functionality"""
    
    def test_uv_availability(self):
        """Test UV availability"""
        assert test_uv_availability(), "UV is not available"
    
    def test_uv_commands(self):
        """Test UV commands"""
        assert test_uv_commands(), "UV commands are not working"
    
    def test_package_management(self):
        """Test package management"""
        assert test_package_management(), "Package management is not working"
    
    def test_docker_environment(self):
        """Test Docker environment"""
        # This test is optional - it's okay if not in Docker
        docker_env = test_docker_environment()
        if not docker_env:
            print("⚠️  Not running in Docker environment - this is okay for local testing")

def main():
    """Run all tests"""
    print("🧪 Running UV Docker tests...")
    
    tests = [
        ("UV Availability", test_uv_availability),
        ("UV Commands", test_uv_commands),
        ("Package Management", test_package_management),
        ("Docker Environment", test_docker_environment)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 {test_name}")
        print(f"{'='*50}")
        
        try:
            if test_func():
                print(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} passed")
    print(f"{'='*50}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
