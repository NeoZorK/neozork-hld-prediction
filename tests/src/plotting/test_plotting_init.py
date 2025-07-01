import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_import():
    """Test that plotting __init__ module can be imported."""
    try:
        # Try to import the module
        import src.plotting
        assert src.plotting is not None
        
    except ImportError as e:
        pytest.fail(f"Failed to import plotting module: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during import test: {e}") 