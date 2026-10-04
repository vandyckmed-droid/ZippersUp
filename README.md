# ZippersUp – 12-1 Momentum Rank

Static, browser-only page (GitHub Pages, `docs/`). Fetches raw data from FMP, stores it as organized CSV files in a **separate private repo**, and ranks the top 100 US stocks by 12-1 log return in the browser. The ranking is never stored.

## One-time setup
1. Create a **private** repo (default name `vandyckmed-droid/zippersup-data`) with an initial commit on `main` (e.g. add a README).
2. Create a fine-grained GitHub token limited to that repo with **Contents: read and write**.
3. Pages: Settings → Pages → Source: GitHub Actions (`.github/workflows/pages.yml` deploys `docs/`).
4. Open the site, paste your FMP key + GitHub token (kept in your browser only), click **Refresh from FMP**.

## Data layout (in the data repo)
```
manifest.json              # datasets, columns, first/last date + row count per symbol
fmp/universe.csv           # symbol,companyName,sector,marketCap,exchange,fetched
fmp/eod-adjusted/AAPL.csv  # date,adjClose  (dividend-adjusted, full history kept)
```
New datasets get their own folder under `fmp/` and an entry in `manifest.json`.

## How refresh works
Reads existing data from the repo (if the browser cache is empty), fetches only new days from FMP (re-fetching a symbol in full if its adjusted history was restated), and commits all changes in one commit. Clearing the browser cache loses nothing; **Load from repo** rebuilds it.
