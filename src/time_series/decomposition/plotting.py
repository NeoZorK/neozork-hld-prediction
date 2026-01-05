from __future__ import annotations

import copy
import math
import os
import sys
from typing import Dict, List

# Use non-interactive backend to avoid deepcopy recursion issues
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# CRITICAL: Increase recursion limit for Python 3.14+ compatibility
# matplotlib deepcopy operations can exceed default limit
if sys.version_info >= (3, 14):
    original_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(5000, original_recursion_limit * 2))

# CRITICAL: Patch matplotlib.path.Path.__deepcopy__ to avoid RecursionError
# Python 3.14+ has issues with deepcopy(super(), memo) in matplotlib.path.Path
def _patched_path_deepcopy(self, memo):
    """Patched __deepcopy__ for matplotlib.path.Path to avoid recursion."""
    import matplotlib.path as mpath
    # Create a new Path without calling super().__deepcopy__ which causes recursion
    new_path = mpath.Path.__new__(mpath.Path)
    new_path._vertices = copy.deepcopy(self._vertices, memo)
    new_path._codes = copy.deepcopy(self._codes, memo)
    new_path._interpolation_steps = copy.deepcopy(self._interpolation_steps, memo)
    new_path._should_simplify = copy.deepcopy(self._should_simplify, memo)
    new_path._simplify_threshold = copy.deepcopy(self._simplify_threshold, memo)
    return new_path

# Apply the patch before any matplotlib.path imports
import matplotlib.path
matplotlib.path.Path.__deepcopy__ = _patched_path_deepcopy

from .base import DecompositionResult


def _localized_texts(locale_ru: bool) -> Dict[str, str]:
    if locale_ru:
        return {
            "original": "Original row",
            "trend": "Trend,",
            "seasonal": "Seasonality",
            "residual": "Residual",
            "imf": "IMF",
            "title_classical": "Nice depositivity,",
            "title_stl": "STL decomposition",
            "title_imf": "CEEMDAN — IMF {n}",
            "title_residual": "CEEMDAN - Balance",
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
        fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=False)
        # Convert DatetimeIndex to numeric numpy arrays to avoid deepcopy recursion issues
        # This is a known issue with matplotlib when dealing with pandas DatetimeIndex
        orig_idx = np.asarray(pd.to_numeric(result.original.index, errors='coerce'), dtype=np.float64)
        orig_vals = np.asarray(result.original.values, dtype=np.float64)
        axes[0].plot(orig_idx, orig_vals, color="black", linewidth=1)
        axes[0].set_title(texts["original"]) # noqa: E265
        x_min, x_max = float(orig_idx.min()), float(orig_idx.max())
        axes[0].set_xlim(x_min, x_max)
        
        trend_idx = np.asarray(pd.to_numeric(result.components["trend"].index, errors='coerce'), dtype=np.float64)
        trend_vals = np.asarray(result.components["trend"].values, dtype=np.float64)
        axes[1].plot(trend_idx, trend_vals, color="tab:blue", linewidth=1)
        axes[1].set_title(texts["trend"]) # noqa: E265
        axes[1].set_xlim(x_min, x_max)
        
        seasonal_idx = np.asarray(pd.to_numeric(result.components["seasonal"].index, errors='coerce'), dtype=np.float64)
        seasonal_vals = np.asarray(result.components["seasonal"].values, dtype=np.float64)
        axes[2].plot(seasonal_idx, seasonal_vals, color="tab:orange", linewidth=1)
        axes[2].set_title(texts["seasonal"]) # noqa: E265
        axes[2].set_xlim(x_min, x_max)
        
        residual_idx = np.asarray(pd.to_numeric(result.components["residual"].index, errors='coerce'), dtype=np.float64)
        residual_vals = np.asarray(result.components["residual"].values, dtype=np.float64)
        axes[3].plot(residual_idx, residual_vals, color="tab:green", linewidth=1)
        axes[3].set_title(texts["residual"]) # noqa: E265
        axes[3].set_xlim(x_min, x_max)
        # Heading without descriptive blocks
        title = texts["title_classical"] if result.method == "classical" else texts["title_stl"]
        fig.suptitle(title, fontsize=12)
    else:
        # for CEEMDAN Use function below plot_and_save_cemdan_per_imf
        raise RuntimeError("Use plot_and_save_ceemdan_per_imf for CEEMDAN method")

    # Use subplots_adjust instead of tight_layout to avoid deepcopy recursion issues
    # This is a known issue with matplotlib when dealing with certain pandas Series
    # that contain circular references in their index
    fig.subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, hspace=0.3)
    out_path = os.path.join(plots_dir, f"{file_stem}.png")
    # Draw the figure before saving to avoid deepcopy issues
    fig.canvas.draw()
    # Save with error handling for recursion issues
    try:
        fig.savefig(out_path, dpi=160)
    except (RecursionError, RuntimeError):
        # Fallback: save without dpi specification
        try:
            fig.savefig(out_path)
        except (RecursionError, RuntimeError):
            # Last resort: save with minimal options
            fig.savefig(out_path, format='png')
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

    # Convert DatetimeIndex to numeric numpy arrays to avoid deepcopy recursion issues
    orig_idx_numeric = np.asarray(pd.to_numeric(result.original.index, errors='coerce'), dtype=np.float64)
    x_min = float(orig_idx_numeric.min())
    x_max = float(orig_idx_numeric.max())
    
    for name in imf_names_sorted:
        n = int(name.replace("IMF", ""))
        fig, ax = plt.subplots(1, 1, figsize=(14, 4))
        comp = result.components[name]
        # Convert DatetimeIndex to numeric numpy arrays to avoid deepcopy issues
        comp_idx = np.asarray(pd.to_numeric(comp.index, errors='coerce'), dtype=np.float64)
        comp_vals = np.asarray(comp.values, dtype=np.float64)
        ax.plot(comp_idx, comp_vals, lw=1)
        ax.set_xlim(x_min, x_max)
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
        # Use subplots_adjust instead of tight_layout to avoid deepcopy recursion issues
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95)
        out_path = os.path.join(plots_dir, f"{file_stem}_IMF{n}.png")
        # Draw the figure before saving to avoid deepcopy issues
        fig.canvas.draw()
        # Save with error handling for recursion issues
        try:
            fig.savefig(out_path, dpi=160)
        except (RecursionError, RuntimeError):
            # Fallback: save without dpi specification
            try:
                fig.savefig(out_path)
            except (RecursionError, RuntimeError):
                # Last resort: save with minimal options
                fig.savefig(out_path, format='png')
        plt.close(fig)
        paths.append(out_path)

    # Residual
    fig, ax = plt.subplots(1, 1, figsize=(14, 4))
    res = result.components["residual"]
    # Convert DatetimeIndex to numeric numpy arrays to avoid deepcopy issues
    res_idx = np.asarray(pd.to_numeric(res.index, errors='coerce'), dtype=np.float64)
    res_vals = np.asarray(res.values, dtype=np.float64)
    ax.plot(res_idx, res_vals, lw=1, color="tab:green")
    ax.set_xlim(x_min, x_max)
    ax.set_title(texts["title_residual"]) # noqa: E265
    fig.text(0.01, 0.01, texts["desc_res"], fontsize=9, ha="left", va="bottom")
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.95)
    out_path = os.path.join(plots_dir, f"{file_stem}_RESIDUAL.png")
    # Draw the figure before saving to avoid deepcopy issues
    fig.canvas.draw()
    # Save with error handling for recursion issues
    try:
        fig.savefig(out_path, dpi=160)
    except (RecursionError, RuntimeError):
        # Fallback: save without dpi specification
        try:
            fig.savefig(out_path)
        except (RecursionError, RuntimeError):
            # Last resort: save with minimal options
            fig.savefig(out_path, format='png')
    plt.close(fig)
    paths.append(out_path)

    return paths


