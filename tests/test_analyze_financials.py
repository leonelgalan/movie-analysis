from __future__ import annotations

# pylint: disable=protected-access
import importlib.util
import sys
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest

_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "03_analyze_financials.py"
_SPEC = importlib.util.spec_from_file_location("analyze_financials", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Failed to load financial analysis module spec")

_fin = cast(Any, importlib.util.module_from_spec(_SPEC))
sys.modules[_SPEC.name] = _fin
_SPEC.loader.exec_module(_fin)  # type: ignore[arg-type]


def test_aggregate_budget_metrics_computes_expected_values() -> None:
    df = pd.DataFrame(
        {
            "budget_category": ["low", "low", "medium", "medium"],
            "roi": [1.5, 0.5, 0.2, 0.4],
            "roi_capped": [1.5, 0.5, 0.2, 0.4],
            "is_profitable": [1.0, 0.0, 1.0, 1.0],
            "budget_millions": [5.0, 4.0, 60.0, 70.0],
            "profit": [10_000_000.0, -1_000_000.0, 50_000_000.0, 60_000_000.0],
            "id": [1, 2, 3, 4],
        }
    )

    agg = _fin._aggregate_budget_metrics(df, order=["low", "medium", "high"])

    assert list(agg.index) == ["low", "medium", "high"]
    assert agg.loc["low", "mean_roi"] == pytest.approx(1.0)
    assert agg.loc["medium", "mean_roi"] == pytest.approx(0.3)
    assert agg.loc["low", "share_profitable"] == pytest.approx(0.5)
    assert agg.loc["medium", "share_profitable"] == pytest.approx(1.0)
    assert agg.loc["low", "avg_profit_millions"] == pytest.approx(4.5)
    assert agg.loc["medium", "avg_profit_millions"] == pytest.approx(55.0)
    assert agg.loc["low", "count"] == pytest.approx(2)
