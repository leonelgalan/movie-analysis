# Environment Setup

This project standardizes on [uv](https://docs.astral.sh/uv/latest/) for
dependency management because it is faster than `pip` + `virtualenv`, works
across platforms, and keeps environments reproducible. A traditional `pip`
workflow remains available for teams that prefer it.

## Recommended: uv

### 1. Install uv

- **macOS (Homebrew):**

  ```bash
  brew install astral-sh/uv/uv
  ```

- **macOS/Linux (shell script):**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows (PowerShell):**

  ```powershell
  iwr https://astral.sh/uv/install.ps1 -UseBasicParsing | iex
  ```

### 2. Create and sync the environment

From the repository root:

```bash
uv sync
```

This creates `.venv/` (if needed) and installs dependencies from
`pyproject.toml`. The resolved versions are captured in `uv.lock` for
reproducibility.

Need a fresh copy of the raw dataset before starting the pipeline? Run:

```bash
uv run python scripts/00_refresh_raw.py
```

That helper pulls the latest TMDB snapshot and rewrites `data/movies_raw.csv`
with the standard 2,000-row filter.

### 3. Run the pipeline

Use `uv run` to execute scripts within the managed environment:

```bash
uv run python scripts/01_clean_data.py
uv run python scripts/02_analyze_genres.py
uv run python scripts/03_analyze_financials.py
uv run python scripts/04_build_model.py
```

`uv run` automatically picks up the `.venv`, so manual activation is optional.

### 4. Code quality tools (optional)

Use these helpers to keep style and types consistent:

```bash
uv run ruff format        # apply Ruff formatter
uv run ruff check         # lint for common issues
uv run ty check scripts   # static type check for the scripts package
```

### 5. Activate the shell (optional)

If you want an interactive session with Python or notebooks, activate the
environment manually:

- **macOS/Linux (bash/zsh):**

  ```bash
  source .venv/bin/activate
  ```

- **Windows (PowerShell):**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

Deactivate with `deactivate` when you are done.

## Fallback: pip + virtualenv

If installing uv is not an option, you can rely on the pinned
`requirements.txt`. Stay aware that dependency resolution and performance will
differ from uv.

- **macOS/Linux:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

- **Windows (PowerShell):**

  ```powershell
  python -m venv venv
  venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

Run the scripts with `python scripts/<step>.py` once the environment is active.
Remember to refresh `requirements.txt` with
`uv export --format requirements.txt --quiet > requirements.txt` whenever
dependencies change in `pyproject.toml`.
