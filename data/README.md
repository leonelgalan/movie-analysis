# Data Overview

The raw dataset `movies_raw.csv` is a curated slice of the public TMDB 5000
Movie Dataset (originally released on Kaggle). A preprocessing script pulls the
latest copy from the
[TMDB 5000 Movie Dataset](https://github.com/whoops88/TMDB_5000) and filters it
down to 2,000 popular titles with non-zero budget, revenue, runtime ≥ 60
minutes, and at least 50 audience votes. We preserve the JSON-encoded columns
(`genres`, `keywords`, `production_companies`, `production_countries`,
`spoken_languages`, `cast`, `crew`) so the cleaning step must still parse and
enrich them.

To regenerate the raw CSV:

```bash
uv run python scripts/00_refresh_raw.py
```

(That helper script downloads the upstream sources, applies the same filter
criteria, and rewrites `data/movies_raw.csv`.)

The cleaned outputs produced by `scripts/01_clean_data.py` live under `results/`
and contain derived metadata such as genres, director, profitability metrics,
and categorical buckets used across the workshop exercises.
