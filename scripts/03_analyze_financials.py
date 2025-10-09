"""Financial analysis of the curated movie dataset."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA_IN = Path("results/movies_clean.csv")
PLOTS = Path("outputs")
PLOTS.mkdir(exist_ok=True, parents=True)

CATEGORY_ORDER = ["low", "medium", "high"]
REQUIRED_COLUMNS = {
    "budget_category",
    "roi",
    "is_profitable",
    "budget_millions",
    "profit",
    "id",
}


def _aggregate_budget_metrics(
    df: pd.DataFrame,
    *,
    order: list[str] | None = None,
) -> pd.DataFrame:
    """Summarise ROI/profit statistics by budget category.

    Args:
        df: Cleaned movie dataset.
        order: Optional list of budget categories to order the output by.
            If not provided, categories will be sorted alphabetically.
    """

    if df.empty:
        return pd.DataFrame()

    categories = order or sorted(df["budget_category"].dropna().unique().tolist())
    if not categories:
        return pd.DataFrame()

    return (
        df.groupby("budget_category")
        .agg(
            mean_roi=("roi_capped", "mean"),
            median_roi=("roi", "median"),
            share_profitable=("is_profitable", "mean"),
            avg_budget_millions=("budget_millions", "mean"),
            avg_profit_millions=("profit", lambda s: (s.mean() / 1_000_000)),
            count=("id", "count"),
        )
        .reindex(CATEGORY_ORDER)
    )


def main() -> None:
    df = pd.read_csv(DATA_IN)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise SystemExit(
            "Dataset missing required columns: "
            f"{missing_list}. Did you run `uv run python scripts/01_clean_data.py` first?"
        )

    df["roi"] = df["roi"].replace([float("inf"), float("-inf")], pd.NA)
    df["roi_capped"] = df["roi"].clip(lower=-1, upper=10)

    agg = _aggregate_budget_metrics(df, order=CATEGORY_ORDER)
    if agg.empty:
        raise SystemExit(
            "No financial aggregates could be computed. Implement "
            "`_aggregate_budget_metrics` or check the cleaned dataset output "
            "from step 01."
        )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)
    categories = agg.index.tolist()

    axes[0].barh(categories, agg["mean_roi"], color="#4c72b0")
    axes[0].set_title("Average ROI by budget tier")
    axes[0].set_xlabel("Mean ROI ((revenue - budget) / budget)")
    axes[0].axvline(0, color="black", linewidth=0.8)

    axes[1].barh(categories, agg["share_profitable"], color="#55a868")
    axes[1].set_title("Share of profitable releases")
    axes[1].set_xlabel("Proportion of titles with profit > 0")
    axes[1].set_xlim(0, 1)

    for ax in axes:
        ax.grid(axis="x", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.savefig(PLOTS / "roi_by_budget_category.png", dpi=150)
    print("Saved plot: outputs/roi_by_budget_category.png")

    summary = agg.copy()
    summary["share_profitable"] = summary["share_profitable"].apply(
        lambda value: f"{value:.1%}" if pd.notna(value) else "n/a"
    )
    summary["mean_roi"] = summary["mean_roi"].round(2)
    summary["median_roi"] = summary["median_roi"].round(2)
    summary["avg_budget_millions"] = summary["avg_budget_millions"].round(1)
    summary["avg_profit_millions"] = summary["avg_profit_millions"].round(1)
    print("\nBudget tier summary:")
    print(summary)


if __name__ == "__main__":
    main()
