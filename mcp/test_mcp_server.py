# -*- coding: utf-8 -*-
# test_mcp_server.py
"""
Test script for MCP server functionality
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from mcp.mcp_server import MCPServer


def test_project_analysis():
    """Test project structure analysis"""
    print("Testing project structure analysis...")

    server = MCPServer()
    context = server.get_project_context()

    print(f"Project: {context['project_name']}")
    print(f"Description: {context['description']}")
    print(f"Modules found: {list(context['modules'].keys())}")
    print(f"Dependencies: {len(context['dependencies'])}")
    print(f"File structure: {list(context['file_structure'].keys())}")

    return True


def test_module_analysis():
    """Test module file analysis"""
    print("\nTesting module file analysis...")

    server = MCPServer()

    # Test each module
    for module_name in server.structure.modules.keys():
        files = server.get_module_files(module_name)
        print(f"Module '{module_name}': {len(files)} Python files")

        if files:
            sample_file = files[0]
            print(f"  Sample file: {sample_file['name']}")
            print(f"  Content length: {len(sample_file['content'])} chars")

    return True


def test_mcp_requests():
    """Test MCP request handling"""
    print("\nTesting MCP request handling...")

    server = MCPServer()

    # Test initialize request
    init_request = {"method": "initialize", "params": {}}
    response = server.handle_request(init_request)

    # Since handle_request is async, we need to run it properly
    import asyncio
    response = asyncio.run(server.handle_request(init_request))

    print(f"Initialize response: {response.get('serverInfo', {}).get('name', 'Unknown')}")

    # Test resources list
    list_request = {"method": "resources/list", "params": {}}
    response = asyncio.run(server.handle_request(list_request))

    resources = response.get('resources', [])
    print(f"Available resources: {len(resources)}")
    for resource in resources:
        print(f"  - {resource['name']}: {resource['description']}")

    return True


def test_file_content():
    """Test file content retrieval"""
    print("\nTesting file content retrieval...")

    server = MCPServer()

    # Test reading requirements.txt
    content = server.get_file_content("requirements.txt")
    if content:
        lines = content.split('\n')
        print(f"Requirements.txt: {len(lines)} lines")
        print(f"First few dependencies: {[l.split('==')[0] for l in lines[:5] if '==' in l]}")
    else:
        print("Could not read requirements.txt")

    # Test reading main script
    content = server.get_file_content("run_analysis.py")
    if content:
        print(f"run_analysis.py: {len(content)} characters")
    else:
        print("Could not read run_analysis.py")

    return True


def main():
    """Run all tests"""
    print("=" * 50)
    print("MCP SERVER TEST SUITE")
    print("=" * 50)

    tests = [
        test_project_analysis,
        test_module_analysis,
        test_mcp_requests,
        test_file_content
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
                print("✓ PASSED")
            else:
                print("✗ FAILED")
        except Exception as e:
            print(f"✗ ERROR: {e}")

    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! MCP Server is ready for use.")
    else:
        print("⚠️  Some tests failed. Check the output above.")

    print("=" * 50)


if __name__ == "__main__":
    main()