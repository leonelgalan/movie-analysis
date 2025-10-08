from __future__ import annotations

# pylint: disable=protected-access
import importlib.util
import sys
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "02_analyze_genres.py"
_SPEC = importlib.util.spec_from_file_location("analyze_genres", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Failed to load genre analysis module spec")

_genres = cast(Any, importlib.util.module_from_spec(_SPEC))
sys.modules[_SPEC.name] = _genres
_SPEC.loader.exec_module(_genres)  # type: ignore[arg-type]


def test_compute_genre_counts_top_n() -> None:
    df = pd.DataFrame(
        {
            "decade": ["1990s", "1990s", "2000s", "2000s", "2000s", "2000s"],
            "primary_genre": [
                "Action",
                "Drama",
                "Action",
                "Action",
                "Comedy",
                "Comedy",
            ],
        }
    )

    counts = _genres._compute_genre_counts(df, top_n=2)

    expected = pd.DataFrame(
        {
            "Action": [1, 2],
            "Comedy": [0, 2],
        },
        index=pd.Index(["1990s", "2000s"], name="decade"),
    )

    pd.testing.assert_frame_equal(counts, expected)


def test_compute_genre_shares_normalizes_rows() -> None:
    counts = pd.DataFrame(
        {
            "Action": [1, 2],
            "Comedy": [1, 0],
        },
        index=pd.Index(["1990s", "2000s"], name="decade"),
    )

    shares = _genres._compute_genre_shares(counts)

    assert pytest.approx(1.0) == shares.loc["1990s"].sum()
    assert pytest.approx(1.0) == shares.loc["2000s"].sum()
    assert (shares >= 0).all().all()
