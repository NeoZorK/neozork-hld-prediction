#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UV Mode Checker
Validates that the container is running in UV-only mode
Works in both Docker and local environments
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def is_docker_environment():
    """Check if running in Docker environment"""
    return (
        os.getenv("DOCKER_CONTAINER", "false").lower() == "true" or
        os.path.exists("/.dockerenv") or
        os.path.exists("/app")
    )

def check_uv_installation() -> Dict[str, Any]:
    """Check if UV is properly installed and accessible"""
    result = {
        "uv_available": False,
        "uv_version": None,
        "uv_path": None,
        "error": None
    }
    
    try:
        # Check if uv command is available
        uv_path = subprocess.check_output(["which", "uv"], 
                                        stderr=subprocess.PIPE, 
                                        text=True).strip()
        result["uv_path"] = uv_path
        result["uv_available"] = True
        
        # Get UV version
        uv_version = subprocess.check_output(["uv", "--version"], 
                                           stderr=subprocess.PIPE, 
                                           text=True).strip()
        result["uv_version"] = uv_version
        
    except subprocess.CalledProcessError as e:
        result["error"] = f"UV not found: {e}"
    except Exception as e:
        result["error"] = f"Error checking UV: {e}"
    
    return result

def check_environment_variables() -> Dict[str, Any]:
    """Check UV-related environment variables"""
    in_docker = is_docker_environment()
    
    result = {
        "use_uv": os.getenv("USE_UV", "false").lower() == "true",
        "uv_only": os.getenv("UV_ONLY", "false").lower() == "true",
        "uv_cache_dir": os.getenv("UV_CACHE_DIR"),
        "uv_venv_dir": os.getenv("UV_VENV_DIR"),
        "python_path": os.getenv("PYTHONPATH"),
        "docker_container": os.getenv("DOCKER_CONTAINER", "false").lower() == "true",
        "in_docker": in_docker
    }
    
    return result

def check_uv_directories() -> Dict[str, Any]:
    """Check UV cache and virtual environment directories"""
    in_docker = is_docker_environment()
    
    result = {
        "cache_dir_exists": False,
        "venv_dir_exists": False,
        "cache_dir_path": None,
        "venv_dir_path": None,
        "in_docker": in_docker
    }
    
    if in_docker:
        # Docker-specific paths
        cache_dir = os.getenv("UV_CACHE_DIR", "/app/.uv_cache")
        venv_dir = os.getenv("UV_VENV_DIR", "/app/.venv")
    else:
        # Local paths
        cache_dir = os.getenv("UV_CACHE_DIR", ".uv_cache")
        venv_dir = os.getenv("UV_VENV_DIR", ".venv")
    
    result["cache_dir_path"] = cache_dir
    result["cache_dir_exists"] = Path(cache_dir).exists()
    
    result["venv_dir_path"] = venv_dir
    result["venv_dir_exists"] = Path(venv_dir).exists()
    
    return result

def check_python_packages() -> Dict[str, Any]:
    """Check if packages were installed via UV"""
    result = {
        "pip_available": False,
        "uv_pip_available": False,
        "installed_packages": [],
        "error": None
    }
    
    # Try multiple approaches to check packages
    package_check_methods = [
        ["uv", "pip", "list"],
        ["pip", "list"],
        ["python", "-m", "pip", "list"]
    ]
    
    for cmd in package_check_methods:
        try:
            if cmd[0] == "pip" or (len(cmd) > 1 and cmd[1] == "pip"):
                # Check if pip is available
                subprocess.run(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             check=True)
                result["pip_available"] = True
                
                # Get installed packages
                packages_output = subprocess.check_output(cmd, 
                                                        stderr=subprocess.PIPE, 
                                                        text=True)
                result["installed_packages"] = packages_output.strip().split('\n')
                break
                
        except subprocess.CalledProcessError:
            continue
        except Exception as e:
            result["error"] = f"Error checking packages with {cmd}: {e}"
            continue
    
    # Try UV pip specifically
    uv_pip_commands = [
        ["uv", "pip", "--version"],
        ["uv", "pip", "list"],
        ["uv", "pip", "--help"]
    ]
    
    for cmd in uv_pip_commands:
        try:
            subprocess.run(cmd, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         check=True)
            result["uv_pip_available"] = True
            break
        except subprocess.CalledProcessError:
            continue
        except Exception:
            continue
    
    return result

def check_mcp_server_config() -> Dict[str, Any]:
    """Check MCP server configuration for UV settings"""
    in_docker = is_docker_environment()
    
    result = {
        "config_file_exists": False,
        "uv_enabled": False,
        "uv_only_enabled": False,
        "config_path": None,
        "error": None,
        "in_docker": in_docker
    }
    
    if in_docker:
        config_path = Path("/app/cursor_mcp_config.json")
    else:
        config_path = Path("cursor_mcp_config.json")
    
    result["config_path"] = str(config_path)
    result["config_file_exists"] = config_path.exists()
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Check server settings
            server_settings = config.get("serverSettings", {}).get("neozork", {})
            features = server_settings.get("features", {})
            
            result["uv_enabled"] = features.get("uv_integration", False)
            result["uv_only_enabled"] = features.get("uv_only_mode", False)
            
        except Exception as e:
            result["error"] = f"Error reading config: {e}"
    
    return result

def generate_report() -> Dict[str, Any]:
    """Generate comprehensive UV mode report"""
    report = {
        "timestamp": str(Path(__file__).stat().st_mtime),
        "uv_installation": check_uv_installation(),
        "environment": check_environment_variables(),
        "directories": check_uv_directories(),
        "packages": check_python_packages(),
        "mcp_config": check_mcp_server_config(),
        "summary": {
            "uv_only_mode": False,
            "all_checks_passed": False,
            "issues": [],
            "environment": "local"
        }
    }
    
    # Determine environment
    in_docker = report["environment"]["in_docker"]
    report["summary"]["environment"] = "docker" if in_docker else "local"
    
    # Analyze results
    issues = []
    
    # Check UV installation
    if not report["uv_installation"]["uv_available"]:
        issues.append("UV is not available")
    
    # Check environment variables based on environment
    if in_docker:
        if not report["environment"]["use_uv"]:
            issues.append("USE_UV environment variable is not set to true in Docker")
        
        if not report["environment"]["uv_only"]:
            issues.append("UV_ONLY environment variable is not set to true in Docker")
        
        # Check MCP configuration in Docker
        if not report["mcp_config"]["uv_enabled"]:
            issues.append("UV integration not enabled in MCP config in Docker")
        
        if not report["mcp_config"]["uv_only_enabled"]:
            issues.append("UV-only mode not enabled in MCP config in Docker")
    else:
        # Outside Docker, just check if UV is available
        if not report["uv_installation"]["uv_available"]:
            issues.append("UV is not available in local environment")
    
    # Check package management
    if not report["packages"]["pip_available"] and not report["packages"]["uv_pip_available"]:
        issues.append("No package manager (pip or uv pip) is available")
    
    # Determine if UV-only mode is properly configured
    if in_docker:
        uv_only_mode = (
            report["uv_installation"]["uv_available"] and
            report["environment"]["use_uv"] and
            report["environment"]["uv_only"] and
            report["mcp_config"]["uv_enabled"] and
            report["mcp_config"]["uv_only_enabled"] and
            (report["packages"]["pip_available"] or report["packages"]["uv_pip_available"])
        )
    else:
        # Outside Docker, just check if UV is available
        uv_only_mode = (
            report["uv_installation"]["uv_available"] and
            (report["packages"]["pip_available"] or report["packages"]["uv_pip_available"])
        )
    
    report["summary"]["uv_only_mode"] = uv_only_mode
    report["summary"]["all_checks_passed"] = len(issues) == 0
    report["summary"]["issues"] = issues
    
    return report

def print_report(report: Dict[str, Any], verbose: bool = False):
    """Print formatted report"""
    environment = report["summary"]["environment"]
    
    print("=" * 60)
    print(f"UV Mode Validation Report ({environment.upper()})")
    print("=" * 60)
    
    # Summary
    summary = report["summary"]
    if summary["uv_only_mode"]:
        print("✅ UV Mode: ENABLED")
    else:
        print("❌ UV Mode: DISABLED")
    
    if summary["all_checks_passed"]:
        print("✅ All Checks: PASSED")
    else:
        print("❌ All Checks: FAILED")
        print("\nIssues found:")
        for issue in summary["issues"]:
            print(f"  - {issue}")
    
    if verbose:
        print("\n" + "=" * 60)
        print("Detailed Report")
        print("=" * 60)
        
        # UV Installation
        print("\n1. UV Installation:")
        uv_install = report["uv_installation"]
        if uv_install["uv_available"]:
            print(f"   ✅ UV Available: {uv_install['uv_version']}")
            print(f"   📍 Path: {uv_install['uv_path']}")
        else:
            print(f"   ❌ UV Not Available: {uv_install['error']}")
        
        # Environment Variables
        print("\n2. Environment Variables:")
        env = report["environment"]
        print(f"   Environment: {env['in_docker']}")
        print(f"   USE_UV: {'✅' if env['use_uv'] else '❌'} {env['use_uv']}")
        print(f"   UV_ONLY: {'✅' if env['uv_only'] else '❌'} {env['uv_only']}")
        print(f"   UV_CACHE_DIR: {env['uv_cache_dir']}")
        print(f"   UV_VENV_DIR: {env['uv_venv_dir']}")
        print(f"   DOCKER_CONTAINER: {env['docker_container']}")
        
        # Directories
        print("\n3. UV Directories:")
        dirs = report["directories"]
        print(f"   Environment: {dirs['in_docker']}")
        print(f"   Cache Directory: {'✅' if dirs['cache_dir_exists'] else '❌'} {dirs['cache_dir_path']}")
        print(f"   Venv Directory: {'✅' if dirs['venv_dir_exists'] else '❌'} {dirs['venv_dir_path']}")
        
        # Package Management
        print("\n4. Package Management:")
        packages = report["packages"]
        print(f"   Pip Available: {'✅' if packages['pip_available'] else '❌'}")
        print(f"   UV Pip Available: {'✅' if packages['uv_pip_available'] else '❌'}")
        if packages["installed_packages"]:
            print(f"   Packages Found: {len(packages['installed_packages'])}")
        if packages["error"]:
            print(f"   Error: {packages['error']}")
        
        # MCP Configuration
        print("\n5. MCP Server Configuration:")
        mcp = report["mcp_config"]
        print(f"   Environment: {mcp['in_docker']}")
        if mcp["config_file_exists"]:
            print(f"   Config File: ✅ {mcp['config_path']}")
            print(f"   UV Integration: {'✅' if mcp['uv_enabled'] else '❌'}")
            print(f"   UV-Only Mode: {'✅' if mcp['uv_only_enabled'] else '❌'}")
        else:
            print(f"   Config File: ❌ {mcp['error']}")
    
    print("\n" + "=" * 60)

def main():
    """Main function"""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    try:
        report = generate_report()
        print_report(report, verbose)
        
        # Exit with appropriate code
        if report["summary"]["all_checks_passed"]:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 