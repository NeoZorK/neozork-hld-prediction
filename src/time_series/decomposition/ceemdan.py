from __future__ import annotations

from typing import Dict

import pandas as pd

from .base import DecompositionResult


class CEEMDANDecomposer:
    def decompose(self, series: pd.Series, params: Dict[str, object]) -> DecompositionResult:
        try:
            from PyEMD import CEEMDAN  # type: ignore
        except Exception as exc:  # pragma: no cover - import guard
            raise RuntimeError(
                "CEEMDAN requires PyEMD. Please install 'PyEMD' in your environment."
            ) from exc

        max_imf = int(params.get("max_imf", 10))
        trials = int(params.get("trials", 100))
        noise_strength = float(params.get("noise_strength", 0.2))
        seed = params.get("seed", None)

        ceemdan = CEEMDAN()
        ceemdan.trials = trials
        ceemdan.noise_seed(seed) if seed is not None else None
        ceemdan.noise_width = noise_strength

        values = series.values.astype(float)
        imfs = ceemdan.ceemdan(values)
        # Cap number of IMFs if requested
        if imfs.shape[0] > max_imf:
            imfs = imfs[:max_imf]

        components: Dict[str, pd.Series] = {}
        for idx in range(imfs.shape[0]):
            components[f"IMF{idx+1}"] = pd.Series(imfs[idx], index=series.index)

        # Residual = original - sum(IMFs)
        residual = series - sum(components.values())
        components["residual"] = residual

        return DecompositionResult(
            original=series,
            components=components,
            method="ceemdan",
            params={
                "max_imf": max_imf,
                "trials": trials,
                "noise_strength": noise_strength,
                "seed": seed,
            },
            metadata={},
        )


