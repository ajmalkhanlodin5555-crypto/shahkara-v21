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
