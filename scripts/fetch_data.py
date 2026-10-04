"""Fetch top-100 US stocks by market cap + 4y EOD prices from FMP, rank 12-1 log momentum."""
import json, os, sys, time, math, datetime as dt
from concurrent.futures import ThreadPoolExecutor
import requests

KEY = os.environ["FMP_API_KEY"]
BASE = "https://financialmodelingprep.com/stable"
TOP_N = 100


def get(path, **params):
    params["apikey"] = KEY
    for attempt in range(4):
        r = requests.get(f"{BASE}/{path}", params=params, timeout=60)
        if r.status_code == 429:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"rate limited: {path}")


def top_stocks():
    rows = get("company-screener", marketCapMoreThan=20_000_000_000, country="US",
               isEtf="false", isFund="false", isActivelyTrading="true",
               exchange="NYSE,NASDAQ", limit=300)
    rows = [r for r in rows if r.get("marketCap")]
    rows.sort(key=lambda r: r["marketCap"], reverse=True)
    return rows[:TOP_N]


def prices(symbol, start, end):
    rows = get("historical-price-eod/dividend-adjusted", symbol=symbol,
               **{"from": start, "to": end})
    out = {}
    for r in rows:
        px = r.get("adjClose") or r.get("close")
        if px and px > 0:
            out[r["date"]] = px
    return sorted(out.items())


CACHE = "data/prices.json"
OVERLAP_DAYS = 10   # re-fetch a short overlap to detect dividend/split restatements


def load_cache():
    try:
        return json.load(open(CACHE))
    except (FileNotFoundError, ValueError):
        return {}


def prices_cached(symbol, start, end, cache):
    """Incremental fetch: only new days, unless adjusted history was restated."""
    old = cache.get(symbol)
    if old and old[0][0] <= start:
        since = (dt.date.fromisoformat(old[-1][0]) - dt.timedelta(days=OVERLAP_DAYS)).isoformat()
        new = prices(symbol, since, end)
        have = dict(old)
        restated = any(d in have and abs(p / have[d] - 1) > 1e-3 for d, p in new)
        if not restated:
            have.update(dict(new))
            return sorted(have.items())
    return prices(symbol, start, end)   # first run, short history, or restated


def price_on_or_before(series, date):
    best = None
    for d, p in series:
        if d <= date:
            best = (d, p)
        else:
            break
    return best


def shift_months(d, m):
    y, mo = divmod(d.year * 12 + d.month - 1 - m, 12)
    mo += 1
    last = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]
    return dt.date(y, mo, min(d.day, last))


def main():
    end = dt.date.today()
    start = shift_months(end, 48)
    stocks = top_stocks()
    cache = load_cache()
    with ThreadPoolExecutor(8) as ex:
        series = list(ex.map(
            lambda s: prices_cached(s["symbol"], start.isoformat(), end.isoformat(), cache), stocks))
    # keep only current constituents, trimmed to the 4y window
    new_cache = {st["symbol"]: [[d, p] for d, p in sr if d >= start.isoformat()]
                 for st, sr in zip(stocks, series) if sr}
    os.makedirs("data", exist_ok=True)
    json.dump(new_cache, open(CACHE, "w"), separators=(",", ":"))

    asof = max(s[-1][0] for s in series if s)
    asof_d = dt.date.fromisoformat(asof)
    t1 = shift_months(asof_d, 1).isoformat()    # skip most recent month
    t12 = shift_months(asof_d, 12).isoformat()

    out = []
    for stock, s in zip(stocks, series):
        if not s:
            continue
        a, b = price_on_or_before(s, t12), price_on_or_before(s, t1)
        # need history reaching back to the 12-month date (5-day slack)
        slack = (dt.date.fromisoformat(t12) + dt.timedelta(days=5)).isoformat()
        mom = math.log(b[1] / a[1]) if a and b and s[0][0] <= slack else None
        out.append({
            "symbol": stock["symbol"], "name": stock.get("companyName"),
            "sector": stock.get("sector"), "marketCap": stock["marketCap"],
            "last": s[-1][1], "mom": mom, "firstDate": s[0][0],
            "spark": [round(p, 2) for _, p in s[::5]],  # ~weekly closes
        })
    ranked = sorted([o for o in out if o["mom"] is not None], key=lambda o: -o["mom"])
    for i, o in enumerate(ranked, 1):
        o["rank"] = i
    unranked = [o for o in out if o["mom"] is None]
    json.dump({"asOf": asof, "from12": t12, "to1": t1,
               "generated": dt.datetime.utcnow().isoformat() + "Z",
               "stocks": ranked + unranked},
              open("docs/data.json", "w"), separators=(",", ":"))
    print(f"wrote {len(ranked)} ranked, {len(unranked)} unranked, as of {asof}")


if __name__ == "__main__":
    main()
