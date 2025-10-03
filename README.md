# Movie Ratings Analysis

Collaborative workshop project: clean a movie dataset, explore genre trends,
analyze profitability, and train a predictive ratings model.

- **Full workshop specification:** see [`docs/SPEC.md`](docs/SPEC.md)
- **Environment/setup:** concise instructions live in [`SETUP.md`](SETUP.md)

## Quick Start

```bash
uv sync
uv run python scripts/01_clean_data.py
uv run python scripts/02_analyze_genres.py
uv run python scripts/03_analyze_financials.py
uv run python scripts/04_build_model.py
```

The scripts are designed to run in order; each writes its outputs for the next step.

## Pipeline Overview

- `00_refresh_raw.py` – optional refresh of the TMDB subset (`data/movies_raw.csv`).
- `01_clean_data.py` – feature engineering -> `results/movies_clean.csv`.
- `02_analyze_genres.py` – decade/genre area chart -> `outputs/genres_by_decade.png`.
- `03_analyze_financials.py` – ROI & profitability summary -> `outputs/roi_by_budget_category.png`.
- `04_build_model.py` – scikit-learn regression with cross-val + holdout metrics.

## Key Artifacts

- Clean dataset: `results/movies_clean.csv`
- Plots: `outputs/genres_by_decade.png`, `outputs/roi_by_budget_category.png`
- Model metrics: printed by `scripts/04_build_model.py`

## Repository Layout

```txt
movie-analysis/
├── README.md
├── SETUP.md
├── docs/
│   └── SPEC.md
├── data/
│   ├── README.md
│   └── movies_raw.csv
├── scripts/
├── outputs/
├── results/
└── tests/
```

## Tips

- Commit after each script so teammates can re-run and review.
- Document notable findings (ROI shifts, genre insights, feature importances) in
  your PR or the shared report.
- Need more context? The spec in `docs/SPEC.md` covers roles, timeline, and stretch goals.
