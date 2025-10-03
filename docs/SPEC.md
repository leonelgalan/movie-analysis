# Movie Analysis Workshop — Project Specification

- **Audience:** Master of Science in Analytics students
- **Duration:** Two 75-minute sessions (Tuesday & Friday)
- **Tech Stack:** Git (local), GitHub, VS Code, Python (pandas, matplotlib,
  scikit-learn), uv

## Learning Objectives

1. Use Git and GitHub to manage and collaborate on real analysis projects.
2. Work in branches and submit Pull Requests (PRs) for peer review.
3. Build a clean, modular, and reproducible analysis pipeline.
4. Practice conflict resolution and integration like a professional data team.

## Dataset

- **Source:** Provided CSV `data/movies_raw.csv` (subset of TMDB).
- **Key columns:**
  - `genres`, `crew` — JSON fields to parse.
  - `budget`, `revenue`, `vote_average`, `release_date`, `title`, `id`.
- **Size:** ~2,000 rows (filtered to reasonable budgets, runtimes, and vote
  counts).

## Deliverables

1. Cleaned dataset: `results/movies_clean.csv`
2. Plots in `outputs/`:
   - `genres_by_decade.png`
   - `roi_by_budget_category.png`
3. Modeling results: printed metrics (R²/MAE) from `scripts/04_build_model.py`.
4. Collaborative documentation in `outputs/REPORT.md` summarizing findings.
5. GitHub activity:
   - Each **script (02–04)** developed in its own **feature branch**.
   - Each team member contributes meaningfully (commit, PR, or code review).
   - Merged Pull Requests (PRs) for each script.

## Acceptance Criteria

- `movies_clean.csv` contains all derived fields used downstream:
  `primary_genre`, `genre_count`, `director`, `decade`, `budget_category`, and
  related numeric or categorical features.
- Scripts run in order without manual edits:

  ```bash
  uv run python scripts/01_clean_data.py
  uv run python scripts/02_analyze_genres.py
  uv run python scripts/03_analyze_financials.py
  uv run python scripts/04_build_model.py
  ```

- All team members have visible contributions in GitHub history (commits,
  comments, or reviews).
- Final run produces both plots and printed model evaluation metrics.

## Recommended Workflow

### Branching & Collaboration

1. Clone the repository.
2. Create a new branch for each script or enhancement:

   ```bash
   git checkout -b feature/genres
   git checkout -b feature/financials
   git checkout -b feature/modeling
   ```

3. Make small, clear commits as you work.
4. Open a Pull Request (PR) to `main` when your script runs cleanly.
5. Request a teammate to review your PR before merging.
6. Merge only after all checks pass and discussion (if any) is resolved.

## Project Timeline

### **Tuesday — Session 1: Foundations & Data Cleaning**

- Git + VS Code + GitHub setup.
- Create and push initial project structure.
- Clean dataset together (`uv run python scripts/01_clean_data.py`).
- Commit and push the cleaned dataset.

### **Between Sessions (Wednesday–Thursday)**

- Pull the merged data-cleaning changes.
- Continue development on analysis and modeling scripts (`02`, `03`, `04`),
  running each with `uv run python scripts/<step>.py`.
- Collaborate as a team — divide work however you prefer.
- Each team member should contribute at least once (code, PR review, or
  documentation).
- Commit early, push regularly, and open PRs for review before Friday.

**Bonus Challenge:** Experiment with pulling code or ideas from another team's
repository — add a new Git remote, merge or cherry-pick their work, and verify
your pipeline still runs cleanly.

### **Friday — Session 2: Integration & Mastery**

- Sync everyone’s repos (`git pull origin main`).
- Review and merge open PRs.
- Practice conflict resolution using `outputs/REPORT.md`.
- Run the full pipeline end-to-end with `uv run python scripts/<step>.py`.
- Review plots and model results.
- Celebrate a working collaborative analysis!

## Conflict Exercise (Friday)

- Two teammates will intentionally edit the same section of `outputs/REPORT.md`.
- This will create a **merge conflict**, resolved in VS Code.

Example starting file:

```markdown
# Team Findings Report

## Genre Analysis

_TBD: Add your key findings here._

## Financial Analysis

_TBD: Add your key findings here._

## Modeling

_TBD: Summarize top features influencing ratings._
```

- Merge both sets of edits into the final version, then commit and push.
- Demonstrate that Git safely preserves both contributors' work.

## Optional Enhancements

- Add more visualizations (e.g., correlation heatmap, revenue by director).
- Improve the model with `RandomForestRegressor` or `GradientBoosting`.
- Extend `outputs/REPORT.md` into a proper project summary.
- Experiment with reusing or merging work across teams.

## Risks & Mitigations

- **Auth issues:** ensure everyone has a GitHub account and local Git setup
  tested.
- **Merge conflicts:** use VS Code merge editor; keep changes from both sides
  when meaningful.
- **Large data:** commit only cleaned or reduced data subsets; keep raw files
  `.gitignored`.

## Verification Checklist (for instructor run-through)

- `uv sync` installs all dependencies correctly.
- All scripts (`01`–`04`) run cleanly end-to-end on sample dataset.
- Commits and branches reflect meaningful contributions.
- `outputs/REPORT.md` shows merged edits from multiple contributors.
- Repo tagged `v1.0-workshop` after final integration.
