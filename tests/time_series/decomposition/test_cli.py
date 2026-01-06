import os
import sys
import json
import subprocess


def test_cli_dry_run_and_ru(tmp_path):
    data = """timestamp,close\n2024-01-01,1\n2024-01-02,2\n2024-01-03,3\n2024-01-04,4\n2024-01-05,5\n"""
    f = tmp_path / "s.csv"
    f.write_text(data)
    cmd = [sys.executable, "timeseries-decomposition.py", "--input", str(f), "--method", "stl", "--period", "2", "--dry-run", "-ru"]
    res = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)
    assert res.returncode == 0


def test_cli_export_and_plots(tmp_path):
    data = """datetime,close\n2024-01-01,1\n2024-01-02,2\n2024-01-03,3\n2024-01-04,4\n2024-01-05,5\n2024-01-06,6\n2024-01-07,7\n"""
    f = tmp_path / "s.csv"
    f.write_text(data)
    out_dir = tmp_path / "out"
    plot_dir = tmp_path / "plots"
    cmd = [
        sys.executable,
        "timeseries-decomposition.py",
        "--input",
        str(f),
        "--method",
        "classical",
        "--mode",
        "additive",
        "--period",
        "2",
        "--export-dir",
        str(out_dir),
        "--save-plots",
        "--plots-dir",
        str(plot_dir),
    ]
    res = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)
    assert res.returncode == 0
    # verify files
    assert any(p.name.endswith("_components.parquet") for p in out_dir.glob("**/*"))
    assert any(p.suffix == ".png" for p in plot_dir.glob("**/*"))


