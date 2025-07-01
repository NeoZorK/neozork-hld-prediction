import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_import():
    """Test that plotly_plot module can be imported."""
    try:
        # Check if required dependencies are available
        missing_deps = []
        
        try:
            import plotly.graph_objects
        except ImportError:
            missing_deps.append("plotly")
            
        try:
            import pandas
        except ImportError:
            missing_deps.append("pandas")
        
        # If any dependencies are missing, skip the test
        if missing_deps:
            pytest.skip(f"Missing required dependencies: {', '.join(missing_deps)}")
        
        # Try to import the module
        import src.plotting.plotly_plot
        assert src.plotting.plotly_plot is not None
        
    except ImportError as e:
        pytest.fail(f"Failed to import plotly_plot module: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during import test: {e}") 