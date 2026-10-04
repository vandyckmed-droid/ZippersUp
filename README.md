# ZippersUp – 12-1 Momentum Rank

Fully static, browser-only site: ranks the top 100 US stocks (by market cap) on 12-1 log return using 4 years of dividend-adjusted EOD prices from [FMP](https://site.financialmodelingprep.com/).

Open the page, paste your FMP API key (kept in this browser's localStorage only), click **Refresh data**. Prices are cached in IndexedDB; later refreshes fetch only new days (and re-fetch a stock if its adjusted history was restated).

## Hosting
Settings → Pages → Source: *GitHub Actions*. `.github/workflows/pages.yml` publishes `docs/` on each push to `main` (no secrets, no data fetching).

## Saving data to the repo
Paste a fine-grained GitHub token (Contents: read/write on this repo) and click **Save to repo**. This commits the cached prices + ranking to `docs/data/store.json` on `main`, which Pages serves. Any browser with an empty cache auto-loads it (or use **Load from repo**). The repo is public, so saved data is public.

## Other save options
- **Download JSON / CSV, Copy CSV, Load file…** work with no setup.
- **Google Drive:** create an OAuth *Web* client ID (Google Cloud Console → APIs & Services → Credentials; enable the Drive API; add `https://vandyckmed-droid.github.io` as an authorized JavaScript origin), paste it into the page, then use **Save to Drive** / **Load from Drive**. Uses the `drive.file` scope, so the page only sees the file it created.
