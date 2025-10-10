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

Each team's fork should contain:

1. Cleaned dataset: `results/movies_clean.csv`
2. Plots in `outputs/`:
   - `genres_by_decade.png`
   - `roi_by_budget_category.png`
3. Modeling results: printed metrics (R²/MAE) from `scripts/04_build_model.py`.
4. Collaborative documentation in `outputs/REPORT.md` summarizing findings.
5. GitHub activity visible in the fork:
   - **Day 1:** One PR to upstream for assigned function implementation
   - **Between sessions:** Each script (02–04) developed in its own feature
     branch with PRs **within the fork** for team code review
   - Each team member contributes meaningfully (commits, PR, or code review)
   - All PRs merged within the fork after review

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

- All team members have visible contributions in the fork's GitHub history
  (commits, PR comments, or code reviews).
- Final pipeline run produces both plots and printed model evaluation metrics.

## Recommended Workflow

### Branching & Collaboration (Within Your Fork)

1. Clone your team's fork.
2. Create a new branch for each script:

   ```bash
   git checkout -b feature/genres
   git checkout -b feature/financials
   git checkout -b feature/modeling
   ```

3. Make small, clear commits as you work.
4. Push your branch and open a Pull Request **within your fork** (base: main,
   compare: your-branch) when your script runs cleanly.
5. Request a teammate to review your PR before merging.
6. Merge the PR within your fork after approval and any discussion is resolved.

## Project Timeline

### **Tuesday — Session 1: Foundations & Data Cleaning**

#### Setup & Team Formation

- Git + VS Code + GitHub setup and identity configuration.
- Form **groups of 4 students** each.
- Each group picks a **team color name** from
  [CSS colors](https://matplotlib.org/stable/gallery/color/named_colors.html#css-colors).
- Groups assess their programming experience (beginner/intermediate/advanced).
- Instructor assigns each group **one function** from `scripts/01_clean_data.py`
  based on difficulty (16 functions total).

**Function Difficulty Guide:**

- ⚡ Very Easy (5-10 min) - 3 functions: `_profit`, `_is_profitable`,
  `_to_millions`
- ✅ Easy (15-20 min) - 4 functions: `_budget_category`, `_vote_count_bucket`,
  `_runtime_bucket`, `_log1p_nonnegative`
- 🟡 Medium (25-35 min) - 6 functions: `_decade_label`, `_greater_than_zero`,
  `_extract_director`, `_take_first`, `_names_from_json`,
  `_revenue_to_budget_ratio`
- 🟠 Medium-Hard (35-50 min) - 3 functions: `_pick_if_present`, `_roi`,
  `_codes_from_json`

#### Collaborative Workflow

1. Each group **forks** `https://github.com/leonelgalan/movie-analysis` to one
   team member's account.
2. All team members clone the fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/movie-analysis.git
   cd movie-analysis
   ```
3. Create a feature branch:
   ```bash
   git checkout -b implement-your-function-name
   ```
4. Implement the assigned function in `scripts/01_clean_data.py`.
5. Test it works by running the script.
6. Commit and push to the fork:
   ```bash
   git add scripts/01_clean_data.py
   git commit -m "Implement _your_function_name"
   git push origin implement-your-function-name
   ```
7. Submit a **Pull Request** from the fork back to the main repository.
8. **Each group submits their PR before the end of Session 1.**

By the end of Tuesday, all 16 functions will be reviewed and merged into `main`.

### **Between Sessions (Wednesday–Thursday)**

1. **Pull the latest changes** from the main repository after all PRs are
   merged:
   ```bash
   git remote add upstream https://github.com/leonelgalan/movie-analysis.git
   git pull upstream main
   ```
2. **Collaborate to complete all analysis scripts** (`02`, `03`, `04`):
   - Work together as a team or divide scripts among team members
   - Create feature branches for each script
   - **Open Pull Requests within your fork** (not to upstream) for team code
     review
   - Merge PRs within your fork after review
3. **Commit early and often** as you make progress.
4. **Push your work** to your fork before Friday.

**Learning Opportunity:** Practice pulling completed scripts from another team's
fork — add their fork as a Git remote, merge or cherry-pick their work, and
verify your pipeline still runs cleanly. This mirrors real-world open-source
collaboration!

### **Friday — Session 2: Integration & Mastery**

- Sync everyone's repos with latest upstream changes:
  ```bash
  git pull upstream main
  ```
- **Review and merge any open PRs within your fork** for scripts `02`, `03`,
  and `04`.
- Practice conflict resolution using `outputs/REPORT.md` (see exercise below).
  - Each team member will edit the same section simultaneously
  - Create competing PRs within the fork
  - Resolve the merge conflict together
- Run the full pipeline end-to-end:
  ```bash
  uv run python scripts/01_clean_data.py
  uv run python scripts/02_analyze_genres.py
  uv run python scripts/03_analyze_financials.py
  uv run python scripts/04_build_model.py
  ```
- Review plots and model results as a team.
- Celebrate a working collaborative analysis!

## Conflict Exercise (Friday)

Within each team's fork, practice resolving merge conflicts:

- Two teammates will intentionally edit the same section of `outputs/REPORT.md`
  on separate branches.
- Each creates a Pull Request within the fork.
- This will create a **merge conflict** when merging the second PR, resolved in
  VS Code.

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
