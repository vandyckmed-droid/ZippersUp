# ZippersUp – 12-1 Momentum Rank

Static GitHub Pages site ranking the top 100 US stocks (by market cap) on 12-1 log return, using 4 years of dividend-adjusted EOD prices from [FMP](https://site.financialmodelingprep.com/).

A GitHub Action (`.github/workflows/update.yml`) runs `scripts/fetch_data.py` each weekday. Prices are cached in `data/prices.json` (committed back by the workflow); later runs fetch only new days, and re-fetch a stock in full if its adjusted history was restated. The script writes `docs/data.json` and deploys `docs/` to Pages, so the API key stays secret.

## Setup
1. Repo **Settings → Secrets → Actions**: add `FMP_API_KEY`.
2. **Settings → Pages → Source: GitHub Actions**.
3. Run the workflow (Actions → *Update data & deploy* → Run workflow).
