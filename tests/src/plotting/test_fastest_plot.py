import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_import():
    """Test that fastest_plot module can be imported."""
    try:
        import src.plotting.fastest_plot
        assert src.plotting.fastest_plot is not None
    except ImportError as e:
        pytest.fail(f"Failed to import fastest_plot module: {e}") 