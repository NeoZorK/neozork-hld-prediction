from __future__ import annotations

from typing import Dict

import pandas as pd
from statsmodels.tsa.seasonal import STL

from .base import DecompositionResult


class STLDecomposer:
    def decompose(self, series: pd.Series, params: Dict[str, object]) -> DecompositionResult:
        period = int(params.get("period", 0)) or None
        seasonal = int(params.get("seasonal", 7))
        trend = int(params.get("trend", 13))
        robust = bool(params.get("robust", True))

        if period is None:
            raise ValueError("STL requires --period to be specified explicitly in this module.")

        stl = STL(series, period=period, seasonal=seasonal, trend=trend, robust=robust)
        res = stl.fit()

        components = {
            "trend": res.trend,
            "seasonal": res.seasonal,
            "residual": res.resid,
        }
        return DecompositionResult(
            original=series,
            components=components,
            method="stl",
            params={"period": period, "seasonal": seasonal, "trend": trend, "robust": robust},
            metadata={},
        )


