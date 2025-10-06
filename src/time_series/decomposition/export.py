from __future__ import annotations

import json
import os
from typing import Dict

import pandas as pd

from .base import DecompositionResult


def export_components(
    result: DecompositionResult,
    export_dir: str,
    file_stem: str,
    split_components: bool = False,
) -> str:
    os.makedirs(export_dir, exist_ok=True)
    if split_components:
        # long format
        records = []
        for name, series in result.components.items():
            df = pd.DataFrame({"timestamp": series.index, "component": name, "value": series.values})
            records.append(df)
        long_df = pd.concat(records, ignore_index=True)
        out_path = os.path.join(export_dir, f"{file_stem}_components.parquet")
        long_df.to_parquet(out_path, index=False)
        return out_path
    else:
        wide = result.to_dataframe_wide()
        out_path = os.path.join(export_dir, f"{file_stem}_components.parquet")
        wide.to_parquet(out_path)
        return out_path


def export_metadata(
    result: DecompositionResult,
    export_dir: str,
    file_stem: str,
    extra: Dict[str, object],
) -> str:
    os.makedirs(export_dir, exist_ok=True)
    payload: Dict[str, object] = {
        "method": result.method,
        "params": result.params,
        "components": list(result.components.keys()),
    }
    payload.update(result.metadata or {})
    payload.update(extra or {})

    out_path = os.path.join(export_dir, f"{file_stem}_metadata.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out_path


