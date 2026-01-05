from __future__ import annotations

import math
import os
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from .base import DecompositionResult


def _localized_texts(locale_ru: bool) -> Dict[str, str]:
    if locale_ru:
        return {
            "original": "Original row",
            "Trend": "Trend,",
            "Seasonal": "Seasonality",
            "Residual": "Residual",
            "imf": "IMF",
            "Tile_classical": "Nice depositivity,",
            "Title_stl": "STL decomposition",
            "title_imf": "CEEMDAN — IMF {n}",
            "Title_residual": "CEEMDAN - Balance",
            "desc_imf": (
                "IMF component {n}. High numbers are usually low frequency (trend),"
                "low are high frequency (noise/microStructure)."
            ),
            "desc_res": (
                "The balance after subtracting all IMF. Often interpreted as a slow part/trend."
            ),
        }
    return {
        "original": "Original",
        "trend": "Trend",
        "seasonal": "Seasonal",
        "residual": "Residual",
        "imf": "IMF",
        "title_classical": "Classical decomposition",
        "title_stl": "STL decomposition",
        "title_imf": "CEEMDAN — IMF {n}",
        "title_residual": "CEEMDAN — Residual",
        "desc_imf": (
            "IMF component {n}. lower index ~ higher frequency (noise), higher index ~ lower frequency (trend)."
        ),
        "desc_res": (
            "Residual after removing all IMFs. Often represents slow part/trend."
        ),
    }


def plot_and_save(result: DecompositionResult, plots_dir: str, file_stem: str, locale_ru: bool = False) -> str:
 os.makedirs(plots_dir, exist_ok=True)
 texts = _localized_texts(locale_ru)

 if result.method in {"classical", "stl"}:
 fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
 result.original.plot(ax=axes[0], color="black", lw=1)
 axes[0].set_title(texts["original"]) # noqa: E265
 axes[0].set_xlim(result.original.index.min(), result.original.index.max())
 result.components["trend"].plot(ax=axes[1], color="tab:blue", lw=1)
 axes[1].set_title(texts["trend"]) # noqa: E265
 axes[1].set_xlim(result.original.index.min(), result.original.index.max())
 result.components["seasonal"].plot(ax=axes[2], color="tab:orange", lw=1)
 axes[2].set_title(texts["seasonal"]) # noqa: E265
 axes[2].set_xlim(result.original.index.min(), result.original.index.max())
 result.components["residual"].plot(ax=axes[3], color="tab:green", lw=1)
 axes[3].set_title(texts["residual"]) # noqa: E265
 axes[3].set_xlim(result.original.index.min(), result.original.index.max())
# Heading without descriptive blocks
 title = texts["title_classical"] if result.method == "classical" else texts["title_stl"]
 fig.suptitle(title, fontsize=12)
 else:
# for CEEMDAN Use function below plot_and_save_cemdan_per_imf
 raise RuntimeError("Use plot_and_save_ceemdan_per_imf for CEEMDAN method")

 fig.tight_layout(rect=[0, 0.03, 1, 0.95])
 out_path = os.path.join(plots_dir, f"{file_stem}.png")
 fig.savefig(out_path, dpi=160)
 plt.close(fig)
 return out_path


def get_ceemdan_exPlanation(locale_ru: bool) -> str:
    if locale_ru:
        return (
            "Explanation of the results of CEMEDAN:\n"
            "-IMF1 is a high-frequency variation (noise/microStructure).\n"
            "-IMF2..IMFk is the intermediate frequencies (cycles/market reactions).\n"
            "-The balance is a slow part/trend after subtracting IMF.\n"
            "Use energy IF as signs, model the trend part separately, \n"
            "and apply walk-forward/commission records when testing strategies."
        )
    return (
        "CEEMDAN results exPlanation:\n"
        "- IMF1: highest frequency (noise/microStructure).\n"
        "- IMF2..IMFk: intermediate frequencies (cycles/market reactions).\n"
        "- Residual: slow part/trend after removing IMFs.\n"
        "Use IMF energies as features, model trend separately, and validate with walk-forward/costs."
    )


def plot_and_save_ceemdan_per_imf(
 result: DecompositionResult, plots_dir: str, file_stem: str, locale_ru: bool = False
) -> List[str]:
 os.makedirs(plots_dir, exist_ok=True)
 texts = _localized_texts(locale_ru)
 paths: List[str] = []

# Collect and sort the IMF
 imf_names = [k for k in result.components.keys() if k.startswith("IMF")]
 imf_names_sorted = sorted(imf_names, key=lambda x: int(x.replace("IMF", "")))

 for name in imf_names_sorted:
 n = int(name.replace("IMF", ""))
 fig, ax = plt.subplots(1, 1, figsize=(14, 4))
 comp = result.components[name]
 comp.plot(ax=ax, lw=1)
 ax.set_xlim(result.original.index.min(), result.original.index.max())
 ax.set_title(texts["title_imf"].format(n=n))
# Add detailssed describe on the drawing
 fig.text(
 0.01,
 0.01,
 texts["desc_imf"].format(n=n),
 fontsize=9,
 ha="left",
 va="bottom",
 )
 fig.tight_layout()
 out_path = os.path.join(plots_dir, f"{file_stem}_IMF{n}.png")
 fig.savefig(out_path, dpi=160)
 plt.close(fig)
 paths.append(out_path)

 # Residual
 fig, ax = plt.subplots(1, 1, figsize=(14, 4))
 res = result.components["residual"]
 res.plot(ax=ax, lw=1, color="tab:green")
 ax.set_xlim(result.original.index.min(), result.original.index.max())
 ax.set_title(texts["title_residual"]) # noqa: E265
 fig.text(0.01, 0.01, texts["desc_res"], fontsize=9, ha="left", va="bottom")
 fig.tight_layout()
 out_path = os.path.join(plots_dir, f"{file_stem}_RESIDUAL.png")
 fig.savefig(out_path, dpi=160)
 plt.close(fig)
 paths.append(out_path)

 return paths


