# SHAHKARA v21 INSTITUTIONAL PRO (XAUUSD): Requirements, Gaps and Open Questions

Source strategy: the "MAFIA AI GOLD MASTER, SHAHKARA v21" text supplied by the owner. It is preserved as written.
Status: AWAITING OWNER APPROVAL. No assumption has been applied. No code that affects trades exists. No backtest has been run.

## A. Rules that are fully specified (will be implemented exactly)
- Limit orders only, with no market orders. BUY LIMIT below price, SELL LIMIT above price. The default verdict is WAIT / NO TRADE.
- Hurst regimes: H >= 0.52 trending; H < 0.45 mean-reverting (sweeps and fades only); 0.45 <= H < 0.52 blocked.
- Garman-Klass: var = 0.5*ln(H/L)^2 - (2ln2-1)*ln(C/O)^2. SL buffer = max(sigma_GK*1.5, ATR*0.35).
- VPIN > 0.70 blocks entry.
- TPC clearance score < 0.70 with an opposing unmitigated OB/FVG on the path blocks or clips the trade.
- Five layers at 20% each: upper boundary, FVG 50%, VWCC core, 0.705 OTE, extreme wick base.
- TP1 at 1:2.2 closing 60%. TP2 at 1:4.2 for the 40% runner.
- Pyramiding only after TP1, with the stop at break-even + ATR cushion, financed only from locked-in profit, max 30%.
- DXY below its 20 EMA gives a +0.05 buy bonus.
- Fix windows: London AM 10:25-10:35 GMT, London PM 15:00-15:10 GMT, NY cut 13:30 EST.
- Output report format (5 sections).

## B. Undefined formulas and ambiguities (owner must define; blocking unless noted)
1. **Hurst exponent:** method (R/S, DFA, variance-ratio, aggregated variance), window length, and the minimum scale.
2. **ATR:** period and smoothing (Wilder or SMA). The "ATR cushion" for break-even is not quantified (a multiple of ATR?).
3. **Garman-Klass:** the window for sigma_GK, and whether it is a single bar or an average over N bars. The spec's H/L/C/O here are bar values and clash with the Hurst H.
4. **Order Block:** definition (the last opposing candle before displacement?), the displacement threshold, the "Mean Threshold" (50% of body or of range?), and the definition of "unmitigated".
5. **FVG:** a standard 3-candle gap is assumed but not stated. Minimum size is unspecified. Consequent encroachment is presumably 50% of the gap; confirm.
6. **Zone construction:** how the precision zone is formed from OB + FVG + OTE, which swing defines the 0.705 OTE, the "upper boundary" for sells, and the "extreme rejection wick base".
7. **True VWCC:** the "dynamic intra-zone volume weights" are not defined. How is volume allocated to the three components? M5 provides only tick volume.
8. **Kyle's Lambda:** lambda = |dP|/dV is given, but the spike threshold, window, and role are not. It is not stated whether it gates, scores, or only reports.
9. **VPIN:** volume bucket size, number of buckets, and the buy/sell volume classification (bulk volume classification or tick rule). True signed volume is unavailable from M5 bars.
10. **Macro engine:** the real-yield and DXY data source, how r_real is used (threshold, sign, weight), and the "bearish" definition beyond DXY < EMA20. The bonus +0.05 is added to what score?
11. **Bank Zone Quality score/tier:** no formula or tier thresholds.
12. **Calibrated Win Probability and Expected Value:** no model or calibration method. It cannot be computed without invented rules.
13. **TPC ray-tracing:** the Clearance Score formula is undefined (fraction of path unobstructed? weighted by obstacle size?).
14. **H4/H1/M15 alignment:** the definition of "aligned" (trend by what measure?) and whether it gates trades. Only M5 data was promised, so higher timeframes would be resampled from M5.
15. **Stop loss:** "structural SL" is undefined, and how the GK buffer is applied (beyond the zone extreme?). The R:R basis (blended entry to SL) is assumed to be the blended entry; confirm.
16. **Sell ladder:** mirror assumptions for sells (layer ordering) need confirmation.
17. **Layer fills:** each limit layer fills independently when touched. Confirm whether the SL and targets are fixed at placement, or are recomputed per filled layer, and what happens to unfilled layers after TP1 or SL.
18. **Order expiry:** how long an unfilled ladder lives, and when a zone becomes invalid.
19. **Regime logic:** in the H < 0.45 regime "only liquidity sweeps and fades" is undefined (sweep detection rule). Does the H >= 0.52 regime have direction rules?
20. **Pyramiding:** "Break-Even + ATR cushion", the funding calculation of "locked-in profit" (realized TP1 profit only?), and whether the 30% is of locked profit or of position size. "L2 positions" are undefined.
21. **Fix clock:** the NY cut in EST. Is it EST all year, or US Eastern with DST? Is the hold applied to order placement, fills, or both? GMT vs UK local time (BST) must be stated. Do not silently pick one.
22. **Account:** the starting balance, risk per trade (the spec gives allocation percentages but not lot sizing), and leverage.
23. **Simulation conventions:** same-bar SL/TP ordering, fill rule when price merely touches a limit, spread/commission/slippage/swap treatment.

## C. Required data (real broker-supplied only)
- XAUUSD M5 OHLC with timestamps (stated time zone) and tick volume, plus the broker's server time zone and DST rule.
- Historical spread, and bid or mid basis.
- Contract specification: size, tick size/value, lot min/max/step, digits.
- Commission, swap, and typical slippage from the broker.
- DXY and US 10Y real yield series with matching timestamps and a named source (not in M5 broker data; the macro engine cannot run without them).
- Real order-book or signed volume data if true VPIN and Kyle's lambda are wanted (otherwise approximations are needed, which require your approval).
- Date range and an out-of-sample split.

## D. Limits to be aware of
- M5 bars with tick volume only give an approximation of VPIN and Kyle's lambda, and these are proxies not the real quantities. Using them is a trade-affecting assumption that needs approval.
- Candle-only simulation cannot know the intrabar order of events.

## E. Safe work that can start now (no trade impact), if approved
Project scaffolding, a data loader and validator (duplicates, ordering, OHLC sanity, gaps, outliers), and unit-tested implementations of the fully specified formulas: Garman-Klass, the 5-layer allocation arithmetic, and the R:R target math. The Fix-window logic waits on the time zone answer.

## F. Approval log
No assumptions are approved yet.

## G. Unfinished components (not started; each blocked by section B or C)
- Hurst exponent engine; ATR; Order Block / FVG detection; zone construction
- True VWCC; ladder price computation; blended entry and structural SL
- TPC ray-tracing; Kyle's lambda; VPIN; macro (DXY / real yield) engine
- LBMA fix-clock filter (time zone and DST decision needed)
- H4/H1/M15 alignment; Bank Zone Quality; calibrated win probability and EV
- Pyramiding logic; master verdict and 5-section report
- Backtest engine, fill/cost model, and any performance results (no real broker data supplied yet)

## H. Implemented so far (safe subset)
`shahkara/formulas.py`, `data.py`, `validation.py` and `tests/`. The R:R function takes entry and stop as inputs; how the spec derives them is still open (item B15).

## I. Review log (step 2)
- **Spec file check:** `docs/SHAHKARA_v21_SPEC.md` was checked by script for the title, both formulas, all thresholds (0.52, 0.45, 0.70, 0.705, 30%, +0.05), fix windows, 40/35/25, R:R values, exit splits, all five 20% layers and the closing line. All present. This is a key-string check, not a byte diff; a byte diff needs the original as a file. Please diff it against your own copy.
- **Formula review:** Garman-Klass is dimensionless (log returns, per-bar) and price-scale invariant. SL Buffer = max(sigma_GK*1.5, ATR*0.35) mixes a unitless sigma with an ATR in USD. The spec does not say how to convert sigma to price units, so sigma_GK*1.5 is not comparable to ATR*0.35 without a decision. Implemented literally; not usable for trade placement until resolved.
- **R:R:** measured as distance entry-to-stop times 2.2 / 4.2. The spec does not state the R basis (blended entry vs. structural SL), item B15.

## J. Additional unresolved decisions (added this step)
J1. **GK units (blocking for SL):** should sigma_GK be multiplied by price (or by a reference price) to get USD before comparing with ATR? Which price?
J2. **GK window:** single bar or an average of variance over N bars, and where the sqrt is taken (before or after averaging)?
J3. **Partial exit mechanics:** the 60%/40% split applies to which size: total filled, or only the filled layers at TP1 time?
J4. **R basis:** confirm R:R uses the blended weighted-average entry and the structural SL.
J5. **Tick-size rounding:** "exact-cent-level" prices: round to 0.01? Round toward or away from entry?
J6. **Break-even:** does it include spread and commission?

## K. Historical XAUUSD M5 data — sources evaluated (step 7 of last turn)

### K1. Sources checked

1. **Dukascopy (Swiss Bank) — Public historical datafeed / data export tool. STRONGEST CANDIDATE.**
   - Verified on the project's own docs: the Historical Data Export is free, delivers `.csv`, timeframes "from tick-by-tick to monthly", personal use, EULA.
   - Third-party pipeline `saleem-latif/duka-data` (MIT) compiles **M5 / H1 / H4 / D1 OHLC bars with bid/ask spread** from Dukascopy's public `datafeed.dukascopy.com` bi5 tick files, for FX, metals, energy and indices, **including XAUUSD** (XAUUSD/XAGUSD use a 1000 point divider, i.e. 3 implied decimals).
   - Default symbols list does not include XAUUSD, but `--symbols XAUUSD` is supported.
   - CSV schema (from that repo's docs): `time,open,high,low,close,volume,spread`; `time` = bar open time **UTC (ISO 8601)**; prices are **bid**; `volume` = bid_vol + ask_vol; `spread` = mean bid-ask spread in bar.
   - Coverage: history back to 2003+ for major pairs; XAUUSD hours/session coverage per feed.
   - **NOT OANDA data.** Must be labelled Dukascopy, per instructions. Broker: Dukascopy Bank SA.

2. **FXCM (Stratos Group) MarketData GitHub repo — NOT SUITABLE.**
   - Only M1, H1, D1; years 2017–2020; instrument list does not include XAUUSD. Not usable for M5 XAUUSD.

3. **HistData.com — NOT SUITABLE for this strategy.**
   - Only M1 (1 minute) max; XAUUSD available; but volume information removed (strategy needs volume weighting), and CSV formats mostly paid ($7/mo for MT5/Excel/NinjaTrader), free generic ASCII otherwise.

4. **TradingView (your chart source) — NOT a data source for backtests here.**
   - No account-free export path identified; and data would be TV-sourced, still not broker-supplied OANDA M5.

5. **OANDA — EXCLUDED.**
   - You have no OANDA account; cannot obtain M5 history without one. Not usable for now.

### K2. Best available option

**Dukascopy via the duka-data pipeline (or Dukascopy's own historical export), for XAUUSD, timeframe M5.**

- It is broker-supplied (Dukascopy Bank SA), real market data, no fabrication.
- It provides bid OHLC + volume + spread at M5 granularity (compiled from tick).
- It is free and CSV-exportable, no OANDA account needed.
- Caveats: not OANDA prices; timezone UTC (not OANDA London time) — must be handled explicitly; price decimals 3 for XAUUSD (vs broker-specific); session hours defined by Dukascopy.

### K3. Limitations / decisions that remain
- Time zone: data is UTC; strategy/fix windows use GMT/EST/BST. Open item, now partly answered (UTC).
- Price basis: bid vs mid vs OANDA point values for XAUUSD.
- Whether M5 bars are compiled (derived) vs natively offered by Dukascopy export tool. Flag as "likely derived from ticks, but confirm".
- Volume: Dukascopy volume = bid+ask over bar; strategy's "True VWCC" needs an intra-zone volume weighting definition (open item B6/B7).
- Terms: Dukascopy personal-use/EULA for the free export; duka-data code is MIT (code only). Data licence terms for bulk/research use should be confirmed with Dukascopy.

### K4. Exact next steps (data)
1. Run `python3 download.py --symbols XAUUSD --start <start> --end <end>` in a clone of `saleem-latif/duka-data`.
2. Inspect `compiled/XAUUSD_M5.csv` schema and confirm M5 bars/UTC, bid, volume, spread.
3. Convert/align time zone to broker/session time explicitly (do not silently change).
4. Validate via `shahkara.validation` (gap, OHLC, monotonic).
5. Then proceed to engines — only after you approve assumptions that change trades.

### K5. Obtaining the CSV from an Android phone
- Option A (recommended): run the download on a desktop/laptop on the same network, then open the local `dashboard.py` (http://127.0.0.1:8765) served to the phone browser, or copy the CSV out of the machine. Not phone-native.
- Option B: use Dukascopy's own Historical Data Export web tool on the phone browser (free, CSV) — but M5 availability/quantities should be confirmed; may only offer tick/M1+ or need account.
- Option C: Termux on Android + run the downloader (Python/pandas) — heavy; not recommended for full history, but possible for a modest range.

### K6. Not done (no fabricated data)
- No candles fabricated; no backtest run; nothing claimed.

## L. FXCM historical sample-data verification (this turn)

Verified live via `candledata.fxcorporate.com` and the `fxcm/MarketData` GitHub repo.

Findings:
1. **M5 XAUUSD: NOT AVAILABLE.** All tested XAUUSD paths returned **404**, including `m5/XAUUSD/2020/1.csv.gz` and `m1/XAUUSD/2020/1.csv.gz`. (FXCM instrument list in the repo has no XAUUSD; timeframe support is **m1, H1, D1** only.)
2. **Download link:** `https://candledata.fxcorporate.com/{periodicity}/{instrument}/{year}/{week}.csv.gz` (gzipped CSV). Reached **200 without account** for `D1/EURUSD/2020.csv.gz` → **publicly accessible**, no login needed for samples.
3. **Format (D1 sample):** header `DateTime,BidOpen,BidHigh,BidLow,BidClose,AskOpen,AskHigh,AskLow,AskClose`; times like `01/01/2020 22:00:00.000`. **No volume field.** (README states timestamps in UTC and indicative lowest-spread data for Active Trader accounts; personal use per EULA.)
4. **Terms for research/backtest:** repo note: "This is for personal use and abides by our EULA"; data "indicative"; scope may vary. Personal/research use is implied OK, but a formal review of the current EULA is still recommended before commercial use.

Conclusion: **FXCM sample data is NOT suitable** for SHAHKARA v21 (needs genuine XAUUSD M5). It lacks M5 and XAUUSD entirely, and has no volume.

Alternatives verified: Dukascopy (best, M5 possible via tick-compile, XAUUSD included, bid+volume+spread, UTC) → preferred.

## M. Final status summary (this turn)
- Completed: FXCM verification (not suitable), data-source doc updated.
- Remaining blocked: strategy engines, backtest, real M5 data acquisition.

## N. Dukascopy historical XAUUSD M5 source — verified findings (this turn)

Verified from the third-party pipeline `saleem-latif/duka-data` (MIT) docs/code and live checks of `datafeed.dukascopy.com`.

Findings:
1. **Source:** Dukascopy Bank SA (Swiss Bank) public historical datafeed. Method: fetch per-hour LZMA `.bi5` tick files, decode, resample to M5 OHLC.
2. **Genuine XAUUSD M5:** YES available through this pipeline; XAUUSD included in the instruments handled (metals use point divider 1000 → 3 implied decimals). Method: `python3 download.py --symbols XAUUSD --start <start> --end <end>` → writes `compiled/XAUUSD_M5.csv`.
3. **Date range / coverage:** history back to 2003+ for major pairs; XAUUSD session hours Sunday 20:00 UTC to Friday 23:59 UTC (Friday late hours may be empty).
4. **Time zone:** UTC (bar open time ISO 8601 UTC). Not OANDA London time. Must be handled explicitly (open item on fix clock tz).
5. **Bid/ask OHLC:** YES — uses **bid** for OHLC; **spread** = mean(ask-bid) in bar; **volume** = sum(bid_vol + ask_vol) (real traded volume aggregated per bar).
6. **Volume type:** real traded volume (bid+ask), not just tick count. Good for True VWCC weighting.
7. **M5 derivation:** M5 bars are **compiled/resampled from tick data** (5-min buckets); open=first bid, high=max bid, low=min bid, close=last bid, volume=sum, spread=mean.

Limitations / open items:
- Data is **Dukascopy**, **not OANDA** (do not label it OANDA).
- M5 is derived from ticks (confirm acceptable).
- Terms: duka-data code MIT; data personal-use/EULA per Dukascopy; bulk/research licence to confirm with Dukascopy.
- Live feed checks hit rate limits (429) during verification; pipeline uses retries.

## O. How to obtain the CSV via Android and import into this project
- Preferred: run download on desktop/laptop (same network) and use local dashboard (`python3 dashboard.py` → http://127.0.0.1:8765) or copy `compiled/XAUUSD_M5.csv` via cloud/USB to phone; then read on Android via a Python app (Pydroid 3 / Termux).
- Or: Termux on Android running the duka-data downloader directly (Python+pandas+numpy).
- Or: Dukascopy's own web historical export in mobile browser (M5 support less certain).
- Import into `shahkara`: loader now accepts both schemas — `time,open,high,low,close,tick_volume[,spread]` or `time,open,high,low,close,volume,spread` (Dukascopy). Tests added (`test_dukascopy_schema`).

## P. Recommended initial date range (no large download yet)
- Not yet downloaded. Recommended first run: a **single trading day** (e.g., `2025-06-02`) or a few days, to validate end-to-end (download → M5 CSV → load → validate → formulas) before any larger pull.
- Reason: fast, small, confirms path; avoids large dataset before approval.

## Q. Remaining limitations / not done
- No performance backtest; no fabricated data; no live trading; no credentials requested.
- Strategy engines (Hurst, ATR, OB/FVG, VWCC, TPC, Kyle, VPIN, macro, fix-clock, master verdict, backtest) still blocked/undone.
