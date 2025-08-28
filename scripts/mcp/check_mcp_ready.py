#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple MCP Server Ready Check
Check if MCP server is ready using file flag
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

def check_mcp_ready(project_root: Path = None) -> bool:
    """Check if MCP server is ready using file flag"""
    if project_root is None:
        project_root = Path("/app") if os.environ.get("DOCKER_CONTAINER") == "true" else Path(__file__).parent.parent.parent
    
    ready_file = project_root / "logs" / "mcp_server_ready.flag"
    
    if not ready_file.exists():
        return False
    
    try:
        # Check if file is recent (created in last 5 minutes)
        file_age = time.time() - ready_file.stat().st_mtime
        if file_age > 300:  # 5 minutes
            return False
        
        # Read the file to verify it's valid
        with open(ready_file, 'r') as f:
            content = f.read().strip()
            if content.startswith("ready:"):
                return True
        
        return False
    except Exception:
        return False

def main():
    """Main function"""
    if check_mcp_ready():
        print("✅ MCP server is ready")
        sys.exit(0)
    else:
        print("⏳ MCP server is not ready")
        sys.exit(1)

if __name__ == "__main__":
    main()
