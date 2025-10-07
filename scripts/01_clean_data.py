"""Data cleaning pipeline for the movie analysis project.

Transforms the raw TMDB subset into a tidy dataset with derived
features that downstream steps rely on (genres, directors, budgets,
language, profitability, etc.).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np  # noqa: F401 - students will need this for implementations
import pandas as pd

DATA_IN = Path("data/movies_raw.csv")
DATA_OUT = Path("results/movies_clean.csv")


@dataclass(frozen=True)
class ColumnSpec:
    """Describe a cleaned-data column and whether it should be filled."""

    kind: str
    fill: bool = True


COLUMN_SCHEMA: list[tuple[str, ColumnSpec]] = [
    ("id", ColumnSpec(kind="numeric", fill=False)),
    ("title", ColumnSpec(kind="string")),
    ("original_title", ColumnSpec(kind="string")),
    ("status", ColumnSpec(kind="string", fill=False)),
    ("release_date", ColumnSpec(kind="string", fill=False)),
    ("release_year", ColumnSpec(kind="numeric", fill=False)),
    ("decade", ColumnSpec(kind="string")),
    ("primary_genre", ColumnSpec(kind="string")),
    ("genre_count", ColumnSpec(kind="numeric", fill=False)),
    ("genres_list", ColumnSpec(kind="list")),
    ("keywords_count", ColumnSpec(kind="numeric", fill=False)),
    ("keywords_list", ColumnSpec(kind="list")),
    ("top_keyword", ColumnSpec(kind="string")),
    ("director", ColumnSpec(kind="string")),
    ("production_companies_list", ColumnSpec(kind="list")),
    ("primary_company", ColumnSpec(kind="string")),
    ("top_cast", ColumnSpec(kind="list")),
    ("cast_list", ColumnSpec(kind="list")),
    ("lead_actor", ColumnSpec(kind="string")),
    ("supporting_actor", ColumnSpec(kind="string")),
    ("ensemble_size", ColumnSpec(kind="numeric", fill=False)),
    ("production_countries_list", ColumnSpec(kind="list")),
    ("primary_country", ColumnSpec(kind="string")),
    ("spoken_languages_list", ColumnSpec(kind="list")),
    ("primary_language", ColumnSpec(kind="string")),
    ("budget", ColumnSpec(kind="numeric")),
    ("revenue", ColumnSpec(kind="numeric")),
    ("profit", ColumnSpec(kind="numeric")),
    ("roi", ColumnSpec(kind="numeric")),
    ("revenue_to_budget_ratio", ColumnSpec(kind="numeric", fill=False)),
    ("budget_category", ColumnSpec(kind="string")),
    ("budget_millions", ColumnSpec(kind="numeric", fill=False)),
    ("revenue_millions", ColumnSpec(kind="numeric", fill=False)),
    ("runtime", ColumnSpec(kind="numeric")),
    ("runtime_bucket", ColumnSpec(kind="string")),
    ("vote_average", ColumnSpec(kind="numeric")),
    ("vote_count", ColumnSpec(kind="numeric")),
    ("vote_count_bucket", ColumnSpec(kind="string")),
    ("popularity", ColumnSpec(kind="numeric")),
    ("budget_log", ColumnSpec(kind="numeric", fill=False)),
    ("revenue_log", ColumnSpec(kind="numeric", fill=False)),
    ("profit_log", ColumnSpec(kind="numeric", fill=False)),
    ("vote_count_log", ColumnSpec(kind="numeric", fill=False)),
    ("popularity_log", ColumnSpec(kind="numeric", fill=False)),
    ("is_profitable", ColumnSpec(kind="numeric", fill=False)),
]


def _parse_json_list(value: object) -> list[dict]:
    """Return a parsed list of dicts for JSON-like columns."""
    if isinstance(value, str) and value.strip():
        loaded = json.loads(value)
        if isinstance(loaded, list):
            return [item for item in loaded if isinstance(item, dict)]
    return []


def _names_from_json(value: object, *, key: str = "name") -> list[str]:
    """Return all truthy string values for ``key`` from a JSON-like payload.

    Args:
        value: Raw JSON string, list of dicts, or other value to inspect.
        key: Dictionary key whose values should be collected.

    Returns:
        A list of strings extracted from the JSON structure. Missing or falsey
        values are ignored.
    """
    return []  # TODO: implement


def _codes_from_json(key: str):
    """Build an extractor that returns all truthy values for ``key``.

    Args:
        key: Dictionary key to read from each JSON object.

    Returns:
        A callable that accepts a JSON-like payload and returns a list of codes
        associated with ``key``.
    """

    def extractor(value: object) -> list[str]:
        """Extract values for the preconfigured key from ``value``."""
        return []  # TODO: implement

    return extractor


def _extract_director(crew_str: object) -> str:
    """Return the first crew member whose job is ``Director``.

    Returns:
        The name of the first director found, or "Unknown" if no director exists.
    """
    return ""  # TODO: implement


def _pick_if_present(position: int, default: str = "Unknown"):
    """Return a function that picks a position from a sequence if available.

    Args:
        position: The zero-based index to extract from the sequence.
        default: Value to return if the position doesn't exist or is empty.

    Returns:
        A function that extracts the item at ``position`` or returns ``default``.
    """

    def picker(seq: list[str]) -> str:
        return ""  # TODO: implement

    return picker


def _take_first(n: int):
    """Return a function that returns the first ``n`` entries from a list.

    Args:
        n: Number of elements to take from the beginning.

    Returns:
        A function that returns the first n elements of a list, or an empty
        list if the input is not a list.
    """

    def taker(seq: list[str]) -> list[str]:
        return []  # TODO: implement

    return taker


def _decade_label(year: int | None) -> str:
    """Convert a release year into a decade label (e.g., ``1990s``).

    Args:
        year: A release year (e.g., 1995).

    Returns:
        A decade string like "1990s", or "Unknown" if year is None or NaN.
    """
    return ""  # TODO: implement


def _budget_category(amount: float) -> str:
    """Bucket budgets into low/medium/high tiers.

    Returns:
        - "low" if budget < $20M
        - "medium" if $20M <= budget < $80M
        - "high" if budget >= $80M
        - "unknown" if budget is None or NaN
    """
    return ""  # TODO: implement


def _vote_count_bucket(votes: float) -> str:
    """Classify vote counts into engagement buckets.

    Returns:
        - "emerging" if votes < 500
        - "established" if 500 <= votes < 2000
        - "blockbuster" if votes >= 2000
        - "unknown" if votes is None or NaN
    """
    return ""  # TODO: implement


def _runtime_bucket(runtime: float) -> str:
    """Categorise runtimes into short/standard/extended/epic.

    Returns:
        - "short" if runtime < 90 minutes
        - "standard" if 90 <= runtime < 120 minutes
        - "extended" if 120 <= runtime < 150 minutes
        - "epic" if runtime >= 150 minutes
        - "unknown" if runtime is None or NaN
    """
    return ""  # TODO: implement


def _profit(df: pd.DataFrame) -> pd.Series:
    """Compute profit as revenue minus budget for each row."""
    return pd.Series([0])  # TODO: implement


def _roi(df: pd.DataFrame) -> pd.Series:
    """Compute return on investment while guarding against zero budgets.

    Formula: (revenue - budget) / budget

    Returns:
        A Series with ROI values. Zero or negative budgets result in NaN.
    """
    return pd.Series([0])  # TODO: implement


def _is_profitable(df: pd.DataFrame) -> pd.Series:
    """Boolean indicator for whether revenue exceeds budget."""
    return pd.Series([False])  # TODO: implement


def _greater_than_zero(series: pd.Series) -> pd.Series:
    """Replace non-positive values in ``series`` with ``NaN``.

    Values <= 0 become NaN; positive values are preserved.
    """
    return pd.Series([0])  # TODO: implement


def _to_millions(series: pd.Series) -> pd.Series:
    """Convert currency series to millions of dollars."""
    return pd.Series([0])  # TODO: implement


def _revenue_to_budget_ratio(df: pd.DataFrame) -> pd.Series:
    """Compute revenue divided by budget with zero-budget protection."""
    safe_budget = df["budget"].replace(0, np.nan)
    return df["revenue"]/safe_budget
    # TODO: implement


def _log1p_nonnegative(series: pd.Series) -> pd.Series:
    for value in series:
        if value < 0:
            series = series.replace(value, 0)
    series =  np.log1p(series)
    """Apply ``log1p`` after clamping negatives to zero."""
    return pd.Series(series)  # TODO: implement



def clean_movie_data() -> pd.DataFrame:
    if not DATA_IN.exists():
        raise FileNotFoundError(f"Raw dataset not found at {DATA_IN}")

    df = pd.read_csv(DATA_IN)

    # ----- Basic type coercion -----
    numeric_cols = [
        "budget",
        "revenue",
        "runtime",
        "vote_average",
        "vote_count",
        "popularity",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    release_dates = cast(pd.Series, pd.to_datetime(df.get("release_date"), errors="coerce"))
    df = df[~release_dates.isna()].copy()
    df["release_date"] = release_dates.dt.strftime("%Y-%m-%d")
    df["release_year"] = release_dates.dt.year

    # ----- Derived categorical features -----
    df["genres_list"] = df["genres"].apply(_names_from_json)
    df["genre_count"] = df["genres_list"].apply(len)
    df["primary_genre"] = df["genres_list"].apply(_pick_if_present(0))

    df["keywords_list"] = df["keywords"].apply(_names_from_json)
    df["keywords_count"] = df["keywords_list"].apply(len)
    df["top_keyword"] = df["keywords_list"].apply(_pick_if_present(0, default="None"))

    df["production_companies_list"] = df["production_companies"].apply(_names_from_json)
    df["primary_company"] = df["production_companies_list"].apply(_pick_if_present(0))

    country_codes = _codes_from_json("iso_3166_1")
    df["production_countries_list"] = df["production_countries"].apply(country_codes)
    df["primary_country"] = df["production_countries_list"].apply(_pick_if_present(0))

    language_codes = _codes_from_json("iso_639_1")
    df["spoken_languages_list"] = df["spoken_languages"].apply(language_codes)
    df["primary_language"] = [
        _pick_if_present(0)(lang_list)
        if lang_list
        else (orig if isinstance(orig, str) and orig else "Unknown")
        for lang_list, orig in zip(df["spoken_languages_list"], df["original_language"])
    ]

    df["director"] = df["crew"].apply(_extract_director)
    df["cast_list"] = df["cast"].apply(_names_from_json)
    df["top_cast"] = df["cast_list"].apply(_take_first(3))
    df["lead_actor"] = df["cast_list"].apply(_pick_if_present(0))
    df["supporting_actor"] = df["cast_list"].apply(_pick_if_present(1))
    df["ensemble_size"] = df["cast_list"].apply(len)

    df["decade"] = df["release_year"].apply(_decade_label)
    df["budget_category"] = df["budget"].apply(_budget_category)
    df["vote_count_bucket"] = df["vote_count"].apply(_vote_count_bucket)
    df["runtime_bucket"] = df["runtime"].apply(_runtime_bucket)

    # ----- Financial features -----
    df["profit"] = _profit(df)
    df["roi"] = _roi(df)
    df["is_profitable"] = _is_profitable(df)
    df["budget_millions"] = _to_millions(df["budget"])
    df["revenue_millions"] = _to_millions(df["revenue"])
    df["revenue_to_budget_ratio"] = _revenue_to_budget_ratio(df)

    df["budget_log"] = _log1p_nonnegative(df["budget"])
    df["revenue_log"] = _log1p_nonnegative(df["revenue"])
    df["profit_log"] = _log1p_nonnegative(df["profit"])
    df["vote_count_log"] = _log1p_nonnegative(df["vote_count"])
    df["popularity_log"] = _log1p_nonnegative(df["popularity"])

    # Impute/standardize fields expected downstream
    fill_strings = [name for name, spec in COLUMN_SCHEMA if spec.kind == "string" and spec.fill]
    for col in fill_strings:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    fill_numeric = [name for name, spec in COLUMN_SCHEMA if spec.kind == "numeric" and spec.fill]
    for col in fill_numeric:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    list_columns = [name for name, spec in COLUMN_SCHEMA if spec.kind == "list" and spec.fill]
    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])

    # Ensure deterministic column order (derived features grouped together)
    preferred_order = [name for name, _ in COLUMN_SCHEMA]

    remaining_cols = [col for col in df.columns if col not in preferred_order]
    ordered_cols = preferred_order + remaining_cols
    df = df[ordered_cols]

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_OUT, index=False)
    print(f"Saved cleaned data to {DATA_OUT} with {len(df)} rows.")
    return df


if __name__ == "__main__":
    clean_movie_data()
