import pandas as pd

from src.time_series.decomposition.classical import ClassicalDecomposer


def test_classical_decomposition_components_shape():
    idx = pd.date_range("2024-01-01", periods=60, freq="D")
    # simple seasonal + trend synthetic
    base = pd.Series(range(60), index=idx) * 0.1
    seasonal = pd.Series([1, 0, -1, 0] * 15, index=idx) * 5
    series = base + seasonal
    dec = ClassicalDecomposer()
    res = dec.decompose(series, {"period": 4, "mode": "additive"})
    assert set(["trend", "seasonal", "residual"]) <= set(res.components.keys())
    assert res.to_dataframe_wide().shape[0] == 60


