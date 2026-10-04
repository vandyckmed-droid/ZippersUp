# ZippersUp – 12-1 Momentum Rank

Fully static, browser-only site: ranks the top 100 US stocks (by market cap) on 12-1 log return using 4 years of dividend-adjusted EOD prices from [FMP](https://site.financialmodelingprep.com/).

Open the page, paste your FMP API key (kept in this browser's localStorage only), click **Refresh data**. Prices are cached in IndexedDB; later refreshes fetch only new days (and re-fetch a stock if its adjusted history was restated).

## Hosting
Settings → Pages → Source: *GitHub Actions*. `.github/workflows/pages.yml` publishes `docs/` on each push to `main` (no secrets, no data fetching).
