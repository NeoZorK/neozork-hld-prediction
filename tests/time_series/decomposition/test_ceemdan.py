import pandas as pd
import pytest


def test_ceemdan_import_guard(monkeypatch):
    # Force import error for PyEMD in decomposer by patching builtins.__import__
    import builtins
    from src.time_series.decomposition.ceemdan import CEEMDANDecomposer

    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):  # noqa: A002
        if name == 'PyEMD' or (name.startswith('PyEMD') if isinstance(name, str) else False):
            raise ImportError("No PyEMD")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, '__import__', fake_import)

    idx = pd.date_range("2024-01-01", periods=32, freq="D")
    series = pd.Series(range(32), index=idx)
    dec = CEEMDANDecomposer()
    with pytest.raises(RuntimeError):
        dec.decompose(series, {"max_imf": 2})


