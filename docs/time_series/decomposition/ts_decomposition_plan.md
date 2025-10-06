# Time Series Decomposition Module — Architecture and Plan

This document defines the scope, architecture, and implementation plan for a professional time series decomposition module that integrates with the existing project. All data cleaning and financial transformations are executed exclusively by external modules and must NOT be performed inside this module.

- External modules responsible for preprocessing (do not modify them here):
  - `stat_analysis.py`
  - `time_analysis.py`
  - `finance_analysis.py`
  - `clear_data.py`
  - Non-existing-yet modules (planned elsewhere): Returns & Log-returns Transformation, Financial-Specific Analysis, Correlation Analysis, Feature Importance Analysis

The decomposition module assumes that input data are already:
- cleaned (no duplicates, consistent time index, timezone handled)
- resampled as required
- imputed or with acceptable gaps according to the external pipeline
- optionally transformed to returns/log-returns by external modules

The module provides three decomposition methods:
- Classical (additive/multiplicative)
- STL (Seasonal-Trend decomposition)
- CEEMDAN (advanced EMD-based approach)

It focuses on:
- robust decomposition of a given single target column (already prepared by external pipeline)
- high-quality visualization with clear annotations (what/why/pros/cons/what next)
- clean export of components and metadata for downstream ML
- CLI that works over project-supported directories without performing cleaning/transformation internally

## Goals and Non-Goals

- Goals:
  - Perform decomposition on pre-cleaned/pre-transformed time series.
  - Support batch processing over supported data directories and files.
  - Produce interpretable plots and export components for ML (CSV/Parquet + JSON metadata).
  - Provide robust parameterization (periods, windows, method-specific args).
  - Ensure files remain < 300 lines each, well-structured.

- Non-Goals:
  - No data cleaning (no resampling, no imputation, no outlier clipping).
  - No returns/log-returns conversions.
  - No financial-specific analytics, correlation or feature importance.
  - No hyperparameter search, model training, or backtesting (handled elsewhere).

## Directory Layout

- Root CLI entrypoint:
  - `timeseries-decomposition.py` (CLI only; delegates to `src/`)

- Source code (each file < 300 LoC):
  - `src/time_series/decomposition/base.py`
    - Interfaces and data structures:
      - `DecompositionMethod` (protocol/abstract)
      - `DecompositionResult` (containers for components + metadata)
      - Factory `get_decomposer(method: str)` returning a specific implementation
    - Validation utilities (lightweight):
      - Verify datetime index presence and monotonicity
      - Verify required column exists and is numeric
      - Assert that the series is already preprocessed (no heavy fix)
  - `src/time_series/decomposition/classical.py`
    - Classical additive/multiplicative decomposition
    - Parameters: `period`, `mode` (`additive|multiplicative`), `log_hint` (metadata only)
  - `src/time_series/decomposition/stl.py`
    - STL decomposition
    - Parameters: `period`, `seasonal`, `trend`, `robust`
  - `src/time_series/decomposition/ceemdan.py`
    - CEEMDAN decomposition
    - Parameters: `max_imf`, `trials`, `noise_strength`, `seed`, `timeout`
    - Guardrails for long series (time budget, IMF cap)
  - `src/time_series/decomposition/io_utils.py`
    - File discovery (CSV/Parquet) in supported project directories without altering data
    - Lightweight readers with strict expectations:
      - Detect `datetime` column or index; convert to DatetimeIndex
      - Select a single target column by name or heuristic (no transforms here)
      - Do not resample/impute/clip; if issues found, fail with actionable error messages guiding to external modules
  - `src/time_series/decomposition/plotting.py`
    - Unified plotting:
      - Classical/STL: 4-panel (Original, Trend, Seasonal, Residual)
      - CEEMDAN: grid of IMFs (high→low frequency) + Residual
    - Clear annotations: what/why/pros/cons/what-next
    - Save to `results/plots/decomposition/<method>/<file_or_symbol>/`
  - `src/time_series/decomposition/export.py`
    - Export components (wide or long) + metadata JSON
    - Exports to `data/indicators/decomposed/<method>/`
    - Metadata includes parameters, method, component names, version, and source file hash/path
  - `src/time_series/decomposition/cli.py`
    - CLI parser and orchestration for batch/single-file runs
    - Enforces “no-preprocessing-here” rule, with explicit error messages and pointers to external modules

## CLI Specification (No Preprocessing Inside)

Entry: `timeseries-decomposition.py`

- Input arguments:
  - `--input` path to a file or directory (supports project dirs: `data/`, `data/indicators/`, `data/raw_parquet/`, `data/cleaned_data/`, etc.)
  - `--column` target column to decompose (e.g., `close`, `value`, or a custom indicator)
  - `--datetime-col` name if not index; otherwise auto-detect
  - `--method` one of: `classical`, `stl`, `ceemdan`
  - `--mode` for classical: `additive|multiplicative`
  - `--period`, `--seasonal`, `--trend`, `--robust` (as applicable)
  - CEEMDAN-specific: `--max-imf`, `--trials`, `--noise-strength`, `--timeout`, `--seed`
  - Hints-only flags (metadata only, no transforms):
    - `--is-returns`, `--is-log-returns`: annotate metadata only
    - `--frequency` to annotate expected frequency (no resampling here)
- Output arguments:
  - `--save-plots` bool, `--plots-dir` (default under `results/plots/decomposition`)
  - `--export` choices: `csv`, `parquet`
  - `--export-dir` (default under `data/indicators/decomposed/<method>/`)
  - `--metadata` JSON path or default co-located
  - `--split-components` (wide vs long)
  - `--open-safari` (macOS only): open plots folder in Safari after completion
  - `--no-progress`: disable progress bars
  - Hidden `-ru`: switch localization to Russian (default: English)
- Operational arguments:
  - `--select` filename mask
  - `--preview` limit first N points for fast plot/check
  - `--dry-run` show planned actions without writing
  - `--strict` fail-fast on any data irregularities (default: strict)
- Behavior:
  - If input is a directory, process all matching files recursively
  - Validate dataset readiness; if not ready, stop with explicit guidance to use external modules
  - Show modern progress bars with ETA for batch and heavy steps (e.g., CEEMDAN)
  - Produce concise per-file report: method, parameters, where plots/exports saved, and high-level component stats (e.g., seasonal strength)

## Data and Validation Contracts

- Input contract (must be satisfied by external pipeline):
  - Single time series with DatetimeIndex or a clear `datetime` column
  - Monotonic, timezone-resolved, consistent frequency (or acceptable gaps)
  - Single numeric target column prepared for decomposition (parquet/csv may include many columns like OHLCV + indicators; we pick exactly one via `--column` or heuristic)
  - If returns/log-returns are needed, they must be computed upstream
- Validation outcomes:
  - OK → proceed with decomposition
  - FAIL → stop with actionable message (e.g., “Detected non-monotonic index. Please run clear_data.py.”)

## Plotting and Annotations

- Classical/STL:
  - 4 panels: Original, Trend, Seasonal, Residual
  - Text annotations (side notes) explaining:
    - What: definition of each component
    - Why: use cases in ML/trading
    - Pros/Cons: interpretability vs regime shifts, sensitivity to period
    - Next: how to leverage components (e.g., model residuals, use seasonal/trend as features)
- CEEMDAN:
  - Grid of IMFs (ordered by frequency) + residual
  - Notes on typical interpretations and cautions (non-stationarity, complexity)
  - If library for CEEMDAN is unavailable, module raises a clear error with installation hint (no fallback decomposition performed)

## Exports

- Components:
  - Long format: `timestamp, component, value`
  - Wide format: `timestamp, original, trend, seasonal, residual` (or IMF1..IMFk, residual)
- Metadata JSON:
  - Method, parameters, target column, hints (is_returns, is_log_returns), file source, version, localization, timestamps, basic stats
- Paths:
  - Data: `data/indicators/decomposed/<method>/...`
  - Plots: `results/plots/decomposition/<method>/<file_or_symbol>/...`

## Testing (100% coverage)

- Unit tests for:
  - `base.py` contracts and factory
  - `classical.py`, `stl.py`, `ceemdan.py` (correct shapes, number of components, invariants)
  - `io_utils.py` (file discovery, validation, strict failures; wide parquet/csv with OHLCV + indicators)
  - `plotting.py` (object-level checks, no rendering errors)
  - `export.py` (schema correctness, metadata fields, localization included)
  - `cli.py` (argument wiring, dry-run, strict mode, hidden `-ru`, `--open-safari`, progress controls)
- No golden-image tests; focus on object properties and schema correctness

## Performance and Limits

- CEEMDAN can be heavy:
  - Limits via `--max-imf`, `--timeout`
  - Optionally advise upstream downsampling in error messages (but do not do it here)
- Use modern progress bars with ETA; allow disabling via `--no-progress`

## Implementation Steps (No Code in This Document)

1. Create `timeseries-decomposition.py` (CLI entrypoint; delegates to `src/time_series/decomposition/cli.py`).
2. Implement `base.py` interfaces and validation helpers (read-only checks) with localization support.
3. Implement `classical.py`, `stl.py`, `ceemdan.py` with strict reliance on ready-to-use series; CEEMDAN requires optional dependency with clear error guidance if missing.
4. Implement `io_utils.py` for discovery and read-only validation (parquet/csv; single-target selection among many columns); refuse to clean/transform.
5. Implement `plotting.py` with clear localized annotations; save under results paths.
6. Implement `export.py` for components and metadata (include localization, hints).
7. Implement `cli.py` with strict contract enforcement, progress bars with ETA, `--open-safari`, `--no-progress`, and hidden `-ru`.
8. Add unit tests across all modules to achieve 100% coverage.
9. Integrate logging to `logs/` and ensure consistent error handling.

## Rationale

- Clear separation of concerns:
  - Upstream modules handle cleaning and transformations (returns/log-returns).
  - Decomposition module is pure analysis and export.
- Safer ML workflows:
  - No hidden preprocessing → reduced leakage risk, easier reproducibility.
- Scalable:
  - Batch over directories, strict validations prevent subtle data errors.


