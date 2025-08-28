#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script for MCP Server Ready Flag
Demonstrates the new ready flag functionality
"""

import json
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from neozork_mcp_server import NeoZorKMCPServer


def demo_ready_flag():
    """Demonstrate the ready flag functionality"""
    print("🚀 Starting MCP Server Ready Flag Demo")
    print("=" * 50)
    
    # Create server instance
    print("📊 Creating MCP server instance...")
    server = NeoZorKMCPServer()
    
    print(f"✅ Server ready flag: {server.ready}")
    print()
    
    # Test ping response
    print("🔍 Testing ping response...")
    ping_response = server._handle_ping(1, {})
    print(f"📡 Ping response ready flag: {ping_response.get('ready')}")
    print(f"📡 Initialization status: {ping_response.get('initialization_status')}")
    
    if not ping_response.get('ready'):
        print(f"⚠️  Message: {ping_response.get('message')}")
        print(f"⏱️  Estimated wait: {ping_response.get('estimated_wait')}")
    else:
        print("✅ Server is ready and responding!")
    
    print()
    
    # Test status response
    print("📊 Testing status response...")
    status_response = server._handle_status(1, {})
    print(f"📡 Status ready flag: {status_response.get('ready')}")
    print(f"📡 Status: {status_response.get('status')}")
    print(f"📡 Uptime: {status_response.get('uptime'):.2f} seconds")
    
    print()
    
    # Test health response
    print("🏥 Testing health response...")
    health_response = server._handle_health(1, {})
    print(f"📡 Health ready flag: {health_response.get('ready')}")
    print(f"📡 Health status: {health_response.get('status')}")
    print(f"📡 Server ready check: {health_response.get('checks', {}).get('server_ready')}")
    
    print()
    
    # Show detailed ping response
    print("📋 Detailed ping response:")
    print(json.dumps(ping_response, indent=2, default=str))
    
    print()
    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    demo_ready_flag()
