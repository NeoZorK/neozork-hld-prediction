from __future__ import annotations

from typing import Dict

import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

from .base import DecompositionResult


class ClassicalDecomposer:
    def decompose(self, series: pd.Series, params: Dict[str, object]) -> DecompositionResult:
        period = int(params.get("period", 0)) or None
        mode = str(params.get("mode", "additive")).lower()
        if mode not in {"additive", "multiplicative"}:
            raise ValueError("mode must be 'additive' or 'multiplicative'")
        result = seasonal_decompose(series, model=mode, period=period, two_sided=True, extrapolate_trend='freq')

        components = {
            "trend": result.trend,
            "seasonal": result.seasonal,
            "residual": result.resid,
        }
        return DecompositionResult(
            original=series,
            components=components,
            method="classical",
            params={"period": period, "mode": mode},
            metadata={},
        )


