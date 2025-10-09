"""Genre mix analysis for the movie workshop pipeline."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_IN = Path("results/movies_clean.csv")
PLOTS = Path("outputs")
PLOTS.mkdir(exist_ok=True, parents=True)

REQUIRED_COLUMNS = {"primary_genre", "decade"}
TOP_N_GENRES = 8


def _compute_genre_counts(
    df: pd.DataFrame,
    *,
    top_n: int = TOP_N_GENRES,
) -> pd.DataFrame:
    """Return a decade × genre table of release counts for the top genres."""

    if df.empty:
        return pd.DataFrame()

    genre_order: Iterable[str] = (
        df["primary_genre"].value_counts().head(top_n).index.tolist()
    )
    if not genre_order:
        return pd.DataFrame()

    filtered = df[df["primary_genre"].isin(genre_order)].copy()
    if filtered.empty:
        return pd.DataFrame()

    counts = (
        filtered.groupby(["decade", "primary_genre"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=list(genre_order), fill_value=0)
        .sort_index()
    )
    counts.columns.name = None
    return counts


def _compute_genre_shares(counts: pd.DataFrame) -> pd.DataFrame:
    """Normalize genre counts within each decade to shares."""

    if counts.empty:
        return counts.copy()

    totals = counts.sum(axis=1)
    shares = counts.divide(totals, axis=0)
    return shares.fillna(0)


def main() -> None:
    df = pd.read_csv(DATA_IN)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise SystemExit(
            "Dataset missing required columns: "
            f"{missing_list}. Did you run "
            "`uv run python scripts/01_clean_data.py` first?"
        )

    df = df.dropna(subset=REQUIRED_COLUMNS).copy()
    if df.empty:
        raise SystemExit(
            "`results/movies_clean.csv` has no populated genre/decade data. "
            "Regenerate it with `uv run python scripts/01_clean_data.py`."
        )

    df["decade"] = df["decade"].astype(str)

    counts = _compute_genre_counts(df, top_n=TOP_N_GENRES)
    if counts.empty:
        raise SystemExit(
            "No rows remain after filtering to top genres. "
            "Check the cleaned dataset output from step 01."
        )

    shares = _compute_genre_shares(counts)
    if shares.empty or not shares.select_dtypes(include="number").any().any():
        raise SystemExit(
            "No numeric genre share data to plot. Ensure `decade` and "
            "`primary_genre` were derived in scripts/01_clean_data.py."
        )

    plt.figure(figsize=(11, 6))
    shares.plot(kind="area", stacked=True, colormap="tab20", ax=plt.gca())
    plt.title("Share of releases by primary genre and decade")
    plt.ylabel("Share of decade releases")
    plt.xlabel("Decade")
    plt.legend(title="Genre", loc="upper left", bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.savefig(PLOTS / "genres_by_decade.png", dpi=150)
    print("Saved plot: outputs/genres_by_decade.png")

    latest_decade = counts.index.max()
    if isinstance(latest_decade, str):
        top_latest = counts.loc[latest_decade].sort_values(ascending=False).head(5)
        print(f"Top genres in {latest_decade}:")
        for genre, count in top_latest.items():
            share = shares.loc[latest_decade, genre]
            print(f"  • {genre}: {int(count)} films ({share:.1%} of releases)")


if __name__ == "__main__":
    main()
