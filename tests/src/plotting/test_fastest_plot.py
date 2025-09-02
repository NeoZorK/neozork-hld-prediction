import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

def test_import():
    """Test that fastest_plot module can be imported."""
    try:
        # Check if required dependencies are available
        missing_deps = []
        
        try:
            import dask.dataframe
        except ImportError:
            missing_deps.append("dask")
            
        try:
            import plotly.graph_objects
        except ImportError:
            missing_deps.append("plotly")
            
        try:
            import datashader
        except ImportError:
            missing_deps.append("datashader")
            
        try:
            import colorcet
        except ImportError:
            missing_deps.append("colorcet")
        
        # If any dependencies are missing, skip the test
        if missing_deps:
            pytest.skip(f"Missing required dependencies: {', '.join(missing_deps)}")
        
        # Try to import the module
        import src.plotting.fastest_plot
        assert src.plotting.fastest_plot is not None
        
        # Test that the main function exists
        assert hasattr(src.plotting.fastest_plot, 'plot_indicator_results_fastest')
        
    except ImportError as e:
        pytest.fail(f"Failed to import fastest_plot module: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during import test: {e}") 