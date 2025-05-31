# Automatically add project root to Python path for tests
import sys
import os
# two levels up from tests/mcp
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

