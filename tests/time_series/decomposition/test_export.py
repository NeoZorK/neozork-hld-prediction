import os
import json
import pandas as pd

from src.time_series.decomposition.base import DecompositionResult
from src.time_series.decomposition.export import export_components, export_metadata


def test_export_wide_and_metadata(tmp_path):
    idx = pd.date_range("2024-01-01", periods=5, freq="D")
    s = pd.Series(range(5), index=idx)
    result = DecompositionResult(
        original=s,
        components={"trend": s, "seasonal": s * 0, "residual": s * 0},
        method="classical",
        params={"period": 7},
        metadata={"locale": "en"},
    )
    comp_path = export_components(result, str(tmp_path), "sample", split_components=False)
    meta_path = export_metadata(result, str(tmp_path), "sample", extra={"k": 1})
    assert os.path.exists(comp_path)
    assert os.path.exists(meta_path)
    data = json.loads(open(meta_path, "r", encoding="utf-8").read())
    assert data["method"] == "classical"
    assert "components" in data
    assert data["k"] == 1


