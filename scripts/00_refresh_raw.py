"""Utility script to refresh the curated TMDB subset used in the workshop."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

MOVIES_URL = "https://raw.githubusercontent.com/whoops88/TMDB_5000/master/tmdb_5000_movies.csv"
CREDITS_URL = "https://raw.githubusercontent.com/whoops88/TMDB_5000/master/tmdb_5000_credits.csv"
OUTPUT_PATH = Path("data/movies_raw.csv")


def main() -> None:
    movies = pd.read_csv(MOVIES_URL)
    credits = pd.read_csv(CREDITS_URL)

    merged = movies.merge(
        credits,
        left_on="id",
        right_on="movie_id",
        how="inner",
        suffixes=("", "_credits"),
    )

    cols_keep = [
        "id",
        "title",
        "original_title",
        "original_language",
        "status",
        "release_date",
        "budget",
        "revenue",
        "runtime",
        "vote_average",
        "vote_count",
        "popularity",
        "genres",
        "keywords",
        "production_companies",
        "production_countries",
        "spoken_languages",
        "crew",
        "cast",
        "tagline",
        "overview",
        "homepage",
    ]
    merged = merged[cols_keep].copy()

    merged = merged[merged["release_date"].notna()]
    merged = merged[merged["budget"].fillna(0) > 0]
    merged = merged[merged["revenue"].fillna(0) > 0]
    merged = merged[merged["vote_count"].fillna(0) >= 50]
    merged = merged[merged["runtime"].fillna(0) >= 60]
    merged = merged[merged["popularity"].notna()]

    merged["release_date"] = merged["release_date"].astype(str)
    merged["runtime"] = merged["runtime"].fillna(0)
    merged["vote_average"] = merged["vote_average"].fillna(0)

    merged = merged.sort_values("popularity", ascending=False)
    sample_size = min(len(merged), 2000)
    curated = merged.head(sample_size).reset_index(drop=True)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    curated.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(curated)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
