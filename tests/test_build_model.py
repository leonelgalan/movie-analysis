from __future__ import annotations

# pylint: disable=protected-access
import importlib.util
import sys
from pathlib import Path
from typing import Any, cast

import numpy as np
import pandas as pd

_MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "04_build_model.py"
_SPEC = importlib.util.spec_from_file_location("build_model", _MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Failed to load model-building module spec")

_model = cast(Any, importlib.util.module_from_spec(_SPEC))
sys.modules[_SPEC.name] = _model
_SPEC.loader.exec_module(_model)  # type: ignore[arg-type]


def test_build_pipeline_structure() -> None:
    pipeline = _model._build_pipeline()

    assert pipeline.named_steps["pre"].transformers[0][2] == _model.NUM_FEATURES
    assert pipeline.named_steps["pre"].transformers[1][2] == _model.CAT_FEATURES
    assert pipeline.named_steps["model"].n_estimators == 400


def test_evaluate_model_returns_metrics() -> None:
    rng = np.random.default_rng(42)
    numeric = pd.DataFrame(
        rng.normal(size=(50, len(_model.NUM_FEATURES))),
        columns=_model.NUM_FEATURES,
    )
    signal = rng.normal(size=len(numeric))
    numeric[_model.NUM_FEATURES[0]] = signal
    categorical = pd.DataFrame(
        {name: rng.choice(["A", "B", "C"], size=len(numeric)) for name in _model.CAT_FEATURES}
    )
    X = pd.concat([numeric, categorical], axis=1)
    y = pd.Series(0.5 * signal + rng.normal(scale=0.1, size=len(signal)))

    pipeline = _model._build_pipeline()
    metrics = _model._evaluate_model(pipeline, X, y, n_splits=3, test_size=0.3, random_state=0)

    expected_keys = {
        "cv_r2_mean",
        "cv_r2_std",
        "cv_mae_mean",
        "cv_mae_std",
        "holdout_r2",
        "holdout_mae",
        "holdout_size",
    }
    assert expected_keys == set(metrics.keys())
    assert metrics["holdout_size"] == int(len(X) * 0.3)
    for key in expected_keys - {"holdout_size"}:
        assert not np.isnan(metrics[key])
        assert metrics[key] != 0.0

    importance = _model.aggregated_feature_importance(pipeline)
    assert not importance.empty
