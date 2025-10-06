from __future__ import annotations

import argparse
import os
import platform
import subprocess
from typing import Dict

import pandas as pd
from tqdm import tqdm

from .base import get_decomposer, validate_ready_series
from .export import export_components, export_metadata
from .io_utils import discover_files, read_timeseries
from .plotting import plot_and_save


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Time Series Decomposition CLI (no preprocessing inside)")
    parser.add_argument("--input", required=True, help="Path to file or directory")
    parser.add_argument("--column", help="Target column name")
    parser.add_argument("--datetime-col", help="Datetime column if not index")
    parser.add_argument("--method", choices=["classical", "stl", "ceemdan"], default="stl")
    parser.add_argument("--mode", choices=["additive", "multiplicative"], default="additive")
    parser.add_argument("--period", type=int)
    parser.add_argument("--seasonal", type=int, default=7)
    parser.add_argument("--trend", type=int, default=13)
    parser.add_argument("--robust", action="store_true", default=True)
    parser.add_argument("--max-imf", type=int, default=10)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--noise-strength", type=float, default=0.2)
    parser.add_argument("--timeout", type=int, default=0)
    parser.add_argument("--seed", type=int)

    parser.add_argument("--is-returns", action="store_true")
    parser.add_argument("--is-log-returns", action="store_true")
    parser.add_argument("--frequency", help="Expected frequency (metadata only)")

    parser.add_argument("--save-plots", action="store_true")
    parser.add_argument("--plots-dir", default=os.path.join("results", "plots", "decomposition"))
    parser.add_argument("--export", choices=["csv", "parquet"], default="parquet")
    parser.add_argument("--export-dir", default=os.path.join("data", "indicators", "decomposed"))
    parser.add_argument("--metadata", help="Optional metadata JSON path (else auto)")
    parser.add_argument("--split-components", action="store_true")

    parser.add_argument("--select", help="Filename mask to filter")
    parser.add_argument("--preview", type=int, help="Use first N points for quick check")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-progress", action="store_true")
    parser.add_argument("--open-safari", action="store_true")

    # Hidden RU localization flag
    parser.add_argument("-ru", dest="ru", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = discover_files(args.input, select_mask=args.select)
    if not files:
        raise SystemExit("No input files discovered.")

    progress_iter = files if args.no_progress else tqdm(files, desc="Decomposition", unit="file")
    for file_path in progress_iter:
        df, chosen_col = read_timeseries(file_path, datetime_col=args.datetime_col, target_column=args.column)
        series = validate_ready_series(df, chosen_col, datetime_col=None)
        if args.preview:
            series = series.iloc[: args.preview]

        params: Dict[str, object] = {
            "period": args.period,
            "mode": args.mode,
            "seasonal": args.seasonal,
            "trend": args.trend,
            "robust": args.robust,
            "max_imf": args.max_imf,
            "trials": args.trials,
            "noise_strength": args.noise_strength,
            "timeout": args.timeout,
            "seed": args.seed,
        }
        decomposer = get_decomposer(args.method)
        result = decomposer.decompose(series, params)

        # Enrich metadata
        result.metadata.update(
            {
                "is_returns": bool(args.is_returns),
                "is_log_returns": bool(args.is_log_returns),
                "frequency": args.frequency,
                "locale": "ru" if args.ru else "en",
                "source_file": file_path,
                "target_column": chosen_col,
            }
        )

        file_stem = os.path.splitext(os.path.basename(file_path))[0]
        method_dir = os.path.join(args.export_dir, args.method)
        plot_dir = os.path.join(args.plots_dir, args.method, file_stem)

        if args.dry_run:
            continue

        comp_path = export_components(result, method_dir, file_stem, split_components=args.split_components)
        _ = export_metadata(result, method_dir, file_stem, extra={})

        opened_path = None
        if args.save_plots:
            opened_path = plot_and_save(result, plot_dir, file_stem, locale_ru=bool(args.ru))

        if args.open_safari and opened_path:
            if platform.system() == "Darwin":
                try:
                    subprocess.run(["open", "-a", "Safari", opened_path], check=False)
                except Exception:
                    pass


if __name__ == "__main__":  # pragma: no cover
    main()


