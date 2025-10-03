from __future__ import annotations

# pylint: disable=protected-access
import importlib.util
import sys
from pathlib import Path
from typing import Any, cast

import numpy as np
import pandas as pd
import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "01_clean_data.py"
_SPEC = importlib.util.spec_from_file_location("clean_data", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Failed to load cleaning module spec")
_clean = cast(Any, importlib.util.module_from_spec(_SPEC))
sys.modules[_SPEC.name] = _clean
_SPEC.loader.exec_module(_clean)  # type: ignore[arg-type]


def test_names_from_json_extracts_strings() -> None:
    payload = '[{"name": "Action"}, {"name": "Drama"}, {"id": 5}]'
    assert _clean._names_from_json(payload) == ["Action", "Drama"]


def test_codes_from_json_factory() -> None:
    extractor = _clean._codes_from_json("iso_639_1")
    payload = '[{"iso_639_1": "en"}, {"iso_639_1": "fr"}, {"other": "xx"}]'
    assert extractor(payload) == ["en", "fr"]


def test_extract_director_falls_back_to_unknown() -> None:
    payload = '[{"job": "Writer", "name": "Someone"}]'
    assert _clean._extract_director(payload) == "Unknown"
    payload = '[{"job": "Director", "name": "Greta Gerwig"}]'
    assert _clean._extract_director(payload) == "Greta Gerwig"


def test_pick_if_present_returns_default_when_missing() -> None:
    picker = _clean._pick_if_present(1, default="N/A")
    assert picker(["Lead", "Support"]) == "Support"
    assert picker(["Lead"]) == "N/A"


def test_take_first_handles_non_lists() -> None:
    taker = _clean._take_first(3)
    assert taker(["a", "b", "c", "d"]) == ["a", "b", "c"]
    assert taker("not-a-list") == []


def test_decade_label_handles_missing_values() -> None:
    assert _clean._decade_label(1995) == "1990s"
    assert _clean._decade_label(np.nan) == "Unknown"


def test_budget_category_boundaries() -> None:
    assert _clean._budget_category(5_000_000) == "low"
    assert _clean._budget_category(25_000_000) == "medium"
    assert _clean._budget_category(100_000_000) == "high"


def test_vote_count_bucket_boundaries() -> None:
    assert _clean._vote_count_bucket(100) == "emerging"
    assert _clean._vote_count_bucket(1_000) == "established"
    assert _clean._vote_count_bucket(5_000) == "blockbuster"


def test_runtime_bucket_categories() -> None:
    assert _clean._runtime_bucket(80) == "short"
    assert _clean._runtime_bucket(120) == "extended"
    assert _clean._runtime_bucket(170) == "epic"


def test_profit_simple_difference() -> None:
    df = pd.DataFrame({"budget": [10], "revenue": [25]})
    result = _clean._profit(df)
    assert result.iloc[0] == 15


def test_roi_handles_zero_budget() -> None:
    df = pd.DataFrame({"budget": [0, 100], "revenue": [200, 250]})
    roi = _clean._roi(df)
    assert np.isnan(roi.iloc[0])
    assert roi.iloc[1] == pytest.approx(1.5)


def test_is_profitable_boolean_output() -> None:
    df = pd.DataFrame({"budget": [50], "revenue": [75]})
    assert bool(_clean._is_profitable(df).iloc[0])


def test_greater_than_zero_masks_non_positive() -> None:
    series = pd.Series([-5, 0, 10])
    result = _clean._greater_than_zero(series)
    assert np.isnan(result.iloc[0])
    assert np.isnan(result.iloc[1])
    assert result.iloc[2] == 10


def test_to_millions_convenience_wrapper() -> None:
    series = pd.Series([1_500_000])
    pd.testing.assert_series_equal(_clean._to_millions(series), pd.Series([1.5]))


def test_revenue_to_budget_ratio() -> None:
    df = pd.DataFrame({"budget": [0, 100], "revenue": [50, 400]})
    ratio = _clean._revenue_to_budget_ratio(df)
    assert np.isnan(ratio.iloc[0])
    assert ratio.iloc[1] == pytest.approx(4.0)


def test_log1p_nonnegative_clamps_negative_values() -> None:
    series = pd.Series([-10, 0, 99])
    result = _clean._log1p_nonnegative(series)
    expected = pd.Series([np.log1p(0), np.log1p(0), np.log1p(99)])
    pd.testing.assert_series_equal(result, expected)
