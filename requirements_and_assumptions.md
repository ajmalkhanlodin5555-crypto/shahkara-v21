# SHAHKARA v21 (XAUUSD M5): Requirements and Open Questions

Status: BLOCKED. The repository contains only a one-line README (`# shahkara-v21`). No strategy rules, code, or data exist in it.
No assumptions have been made. Every item below needs an answer from the owner before any trade logic is written.

## 1. Missing from the repository
- Strategy specification or source code (indicators, entries, exits, filters)
- Parameter file or config
- Historical XAUUSD M5 data
- Any existing backtest, results, or notes
- Python project scaffolding (pyproject/requirements, tests, package layout)

## 2. Unclear strategy rules (owner must define)
1. Exact entry conditions for long and short, with formulas for every indicator or pattern used
2. Which candle value triggers entry (close, next open, intrabar touch)
3. Stop-loss: method, formula, and units (price, points, ATR multiple)
4. Take-profit: fixed, multiple targets, or trailing; partial closes
5. Exit rules besides SL/TP (time exit, opposite signal, session end)
6. Position sizing: fixed lot, risk % of equity, or compounding; starting balance; leverage
7. Trading sessions and time zone; news and day-of-week filters
8. Maximum concurrent positions, pyramiding, and hedging (allowed or not)
9. Handling of an SL and TP both hit in the same M5 bar (intrabar ordering)
10. Higher-timeframe inputs, if any, and how they are aligned without lookahead
11. What "v21" changed from earlier versions (to confirm this is the intended spec)

## 3. Required data
- Broker-supplied XAUUSD M5 bars: timestamp (state the time zone), open, high, low, close, tick volume
- Broker name, account type, and server time zone/DST rules
- Bid-based or mid prices, and historical spread (per bar, if available)
- Contract specs: contract size (usually 100 oz/lot), tick size and value, min/max/step lot, digits
- Commission, swap/rollover rates, and slippage assumptions (the broker's real values)
- Date range to test, plus an out-of-sample split
- Broker market-closed and weekend gap behavior

## 4. Data validation planned (no trade impact)
Duplicate timestamps, non-monotonic time, OHLC consistency (low <= open/close <= high), gaps versus the expected session calendar, zero or negative prices, outlier jumps, and spread sanity.

## 5. Questions to answer before any code that affects trades
See section 2. Items 1-9 are blocking. Section 3 data is needed before any backtest can run.
No backtest has been run and no results exist.
