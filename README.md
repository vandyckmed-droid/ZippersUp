# ZippersUp – 12-1 Momentum Rank

Fully static, browser-only site: ranks the top 100 US stocks (by market cap) on 12-1 log return using 4 years of dividend-adjusted EOD prices from [FMP](https://site.financialmodelingprep.com/).

Open the page, paste your FMP API key (kept in this browser's localStorage only), click **Refresh data**. Prices are cached in IndexedDB; later refreshes fetch only new days (and re-fetch a stock if its adjusted history was restated).

## Hosting
Settings → Pages → Source: *GitHub Actions*. `.github/workflows/pages.yml` publishes `docs/` on each push to `main` (no secrets, no data fetching).

## Raw data storage
The only thing stored is the **raw FMP data**: `{version:2, fetched, universe[], prices{symbol:[[date,adjClose],…]}}`. The ranking is never stored; the browser recomputes it from the raw data on every load.

- **Browser:** IndexedDB (automatic).
- **Download raw JSON / Load file…:** no setup.
- **Save to Drive / Load from Drive:** `zippersup-raw.json`. Needs a Google OAuth *Web* client ID (Cloud Console → enable Drive API → add `https://vandyckmed-droid.github.io` as an authorized JavaScript origin). Uses the `drive.file` scope.
- **Save to repo / Load from repo:** fine-grained GitHub token (Contents: write) commits `docs/data/raw.json` to `main` (public repo, so the data is public).
- **Download/Copy ranking CSV** exports a computed ranking, for convenience only.
