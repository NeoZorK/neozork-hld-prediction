import subprocess
import sys

def test_cli_draw_modes():
    """
    Smoke test: check that CLI accepts all draw modes and exits gracefully.
    """
    for mode in ["fast", "plotly", "mpl", "mplfinance"]:
        result = subprocess.run([sys.executable, "run_analysis.py", "demo", "-d", mode, "--help"], capture_output=True)
        assert result.returncode == 0
        assert b"Choose plotting library" in result.stdout