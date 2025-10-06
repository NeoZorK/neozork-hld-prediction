from __future__ import annotations

import math
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd

from .base import DecompositionResult


def _localized_texts(locale_ru: bool) -> Dict[str, str]:
    if locale_ru:
        return {
            "original": "Оригинальный ряд",
            "trend": "Тренд",
            "seasonal": "Сезонность",
            "residual": "Остаток",
            "imf": "IMF",
            "notes": "Что это / Зачем / Плюсы / Минусы / Что дальше",
        }
    return {
        "original": "Original",
        "trend": "Trend",
        "seasonal": "Seasonal",
        "residual": "Residual",
        "imf": "IMF",
        "notes": "What / Why / Pros / Cons / Next",
    }


def plot_and_save(result: DecompositionResult, plots_dir: str, file_stem: str, locale_ru: bool = False) -> str:
    os.makedirs(plots_dir, exist_ok=True)
    texts = _localized_texts(locale_ru)

    if result.method in {"classical", "stl"}:
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        result.original.plot(ax=axes[0], color="black", lw=1)
        axes[0].set_title(texts["original"])  # noqa: E265
        result.components["trend"].plot(ax=axes[1], color="tab:blue", lw=1)
        axes[1].set_title(texts["trend"])  # noqa: E265
        result.components["seasonal"].plot(ax=axes[2], color="tab:orange", lw=1)
        axes[2].set_title(texts["seasonal"])  # noqa: E265
        result.components["residual"].plot(ax=axes[3], color="tab:green", lw=1)
        axes[3].set_title(texts["residual"])  # noqa: E265
        fig.suptitle(texts["notes"], fontsize=10)
    else:
        imf_names = [k for k in result.components.keys() if k.startswith("IMF")]
        imf_names_sorted = sorted(
            imf_names, key=lambda x: int(x.replace("IMF", ""))
        )
        n = len(imf_names_sorted)
        rows = int(math.ceil((n + 1) / 2))
        fig, axes = plt.subplots(rows, 2, figsize=(14, 2.5 * rows), sharex=True)
        axes = axes.flatten()
        for i, name in enumerate(imf_names_sorted):
            result.components[name].plot(ax=axes[i], lw=1)
            axes[i].set_title(f"{texts['imf']} {name.replace('IMF', '')}")
        # Residual in the last subplot
        result.components["residual"].plot(ax=axes[min(n, len(axes) - 1)], color="tab:green", lw=1)
        axes[min(n, len(axes) - 1)].set_title(texts["residual"])  # noqa: E265
        fig.suptitle(texts["notes"], fontsize=10)

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_path = os.path.join(plots_dir, f"{file_stem}.png")
    fig.savefig(out_path, dpi=160)
    plt.close(fig)
    return out_path


