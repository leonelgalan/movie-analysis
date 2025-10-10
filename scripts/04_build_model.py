"""Predict IMDb-style vote averages using engineered movie features."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_IN = Path("results/movies_clean.csv")

NUM_FEATURES: list[str] = [
    "budget_log",
    "revenue_log",
    "profit_log",
    "budget_millions",
    "revenue_millions",
    "revenue_to_budget_ratio",
    "runtime",
    "genre_count",
    "vote_count_log",
    "popularity_log",
    "ensemble_size",
]

CAT_FEATURES: list[str] = [
    "primary_genre",
    "director",
    "budget_category",
    "decade",
    "primary_language",
    "primary_country",
    "vote_count_bucket",
    "runtime_bucket",
    "top_keyword",
    "lead_actor",
]


def _build_pipeline() -> Pipeline:
    """Construct the preprocessing + model pipeline used for vote prediction."""

    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(handle_unknown="ignore"),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric, NUM_FEATURES),
            ("cat", categorical, CAT_FEATURES),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=400,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )

    return Pipeline(steps=[("pre", preprocessor), ("model", model)])


def aggregated_feature_importance(pipeline: Pipeline) -> pd.Series:
    """Aggregate tree-based feature importances back to their base feature names."""
    pre = pipeline.named_steps["pre"]
    model = pipeline.named_steps["model"]

    feature_names = pre.get_feature_names_out()
    importances = model.feature_importances_

    def base_name(name: str) -> str:
        if name.startswith("num__"):
            return name.split("__", 1)[1]
        if name.startswith("cat__"):
            remainder = name.split("__", 1)[1]
            if "_" in remainder:
                return remainder.rsplit("_", 1)[0]
            return remainder
        return name

    grouped = (
        pd.DataFrame({"feature": feature_names, "importance": importances})
        .assign(base_feature=lambda df_: df_["feature"].apply(base_name))
        .groupby("base_feature")["importance"]
        .sum()
        .sort_values(ascending=False)
    )
    return grouped


def _evaluate_model(
    pipeline: Pipeline,
    X: pd.DataFrame,
    y: pd.Series,
    *,
    n_splits: int = 5,
    test_size: float = 0.2,
    random_state: int = 42,
) -> dict[str, float]:
    """Run cross-validation and holdout evaluation, returning summary metrics."""

    cv = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    cv_r2_scores = cross_val_score(pipeline, X, y, cv=cv, scoring="r2")
    cv_mae_scores = -cross_val_score(
        pipeline, X, y, cv=cv, scoring="neg_mean_absolute_error"
    )

    metrics = {
        "cv_r2_mean": float(cv_r2_scores.mean()),
        "cv_r2_std": float(cv_r2_scores.std()),
        "cv_mae_mean": float(cv_mae_scores.mean()),
        "cv_mae_std": float(cv_mae_scores.std()),
    }

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    metrics["holdout_r2"] = float(r2_score(y_test, y_pred))
    metrics["holdout_mae"] = float(mean_absolute_error(y_test, y_pred))
    metrics["holdout_size"] = int(len(y_test))

    return metrics


def main() -> None:
    df = pd.read_csv(DATA_IN)

    required_cols = set(NUM_FEATURES + CAT_FEATURES + ["vote_average"])
    missing = required_cols - set(df.columns)
    if missing:
        raise SystemExit(
            "Missing columns in cleaned data: "
            + ", ".join(sorted(missing))
            + ". Re-run 01_clean_data.py to regenerate features."
        )

    X = df[NUM_FEATURES + CAT_FEATURES]
    y = df["vote_average"].astype(float)

    pipeline = _build_pipeline()
    metrics = _evaluate_model(pipeline, X, y)

    print(
        f"5-fold CV R^2: {metrics['cv_r2_mean']:.3f} ± {metrics['cv_r2_std']:.3f}"
    )
    print(
        f"5-fold CV MAE: {metrics['cv_mae_mean']:.3f} ± {metrics['cv_mae_std']:.3f}"
    )
    print(
        f"Holdout R^2: {metrics['holdout_r2']:.3f} "
        f"(test size: {metrics['holdout_size']})"
    )
    print(f"Holdout MAE: {metrics['holdout_mae']:.3f}")

    importance = aggregated_feature_importance(pipeline).head(10)
    print("\nTop feature importances (aggregated):")
    for feature, score in importance.items():
        print(f"  • {feature}: {score:.3f}")


if __name__ == "__main__":
    main()
