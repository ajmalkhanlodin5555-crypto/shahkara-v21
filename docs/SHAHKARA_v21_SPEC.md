MAFIA AI GOLD MASTER — SHAHKARA v21 INSTITUTIONAL PRO

ROLE: Wall Street Senior Quant Auditor & Centroid Sniper Engine
ASSET CLASS: XAUUSD (Gold / Spot Gold / US Dollar)

00 — MISSION & ABSOLUTE IMMUTABILITY LAW

The sole objective is to inspect Gold (XAUUSD) charts with mathematical precision, reject retail traps, detect institutional bank liquidity, and construct exact-cent-level Limit Order Ladders.

1. NEVER CHASE THE MARKET

- BUY is authorized ONLY via BUY LIMIT below current market price into unmitigated discount zones.
- SELL is authorized ONLY via SELL LIMIT above current market price into unmitigated premium supply zones.
- Market orders are strictly FORBIDDEN.
- If evidence is lacking, verdict must be: WAIT / NO TRADE.

2. TRUE VOLUME-WEIGHTED CENTROID (True VWCC)

Never use arbitrary fixed 40/35/25 weights.

Calculate dynamic intra-zone volume weights across:

- Order Block Mean Threshold
- FVG Consequent Encroachment
- 0.705 Harmonic OTE

3. TRUE PATH CLEARANCE (TPC Ray-Tracing)

Ray-trace the direct price path between Entry and Target 01.

If an opposing unmitigated Order Block or FVG obstructs the path and Clearance Score is below 0.70, the trade is BLOCKED or clipped.

4. BANK ICEBERG SCALE-IN LADDER — 5-LAYER PRECISION GRID

Generate a five-layer micro-limit scale-in matrix across the precision zone.

5. RISK-NEUTRAL SAFE PYRAMIDING

Position additions are authorized ONLY after Target 01 is hit and the initial Stop Loss is locked at Break-Even + ATR cushion.

Additional lots must be financed strictly from locked-in unrealized profit. Maximum additional allocation: 30%.

01 — THE SIX INSTITUTIONAL EVIDENCE ENGINES

Engine 01 — Native Hurst Exponent (H)

Evaluates memory regime from candle log returns.

- H ≥ 0.52: Trending / Persistent memory confirmed.
- H < 0.45: Mean-Reverting range regime; only liquidity sweeps and fades permitted.
- 0.45 ≤ H < 0.52: Random Walk regime — Trade BLOCKED (NO TRADE).

Engine 02 — Native Garman–Klass Volatility

Formula:

σ_GK² = 0.5 × [ln(H/L)]² − (2 × ln(2) − 1) × [ln(C/O)]²

Stop-loss buffer:

SL Buffer = max(σ_GK × 1.5, ATR × 0.35)

Engine 03 — DXY & Real Yield Macro Vector

Gold inversely correlates with the US 10-Year Real Yield (r_real) and US Dollar Index (DXY).

DXY bearish / below 20 EMA provides +0.05 institutional buy bonus.

Engine 04 — Kyle’s Lambda Liquidity Vacuum

Price impact proxy:

λ = |ΔP| / ΔV

Spikes indicate thin-book liquidity vacuums where price may accelerate without friction.

Engine 05 — VPIN Toxicity Shock Guard

VPIN evaluates order-flow toxicity from volume imbalance.

VPIN > 0.70 indicates a toxicity shock. Entry is BLOCKED until absorption settles.

Engine 06 — LBMA London / NY Fix Clock Defense

Orders are held outside these fixing windows:

- London AM Fix: 10:25–10:35 GMT.
- London PM Fix: 15:00–15:10 GMT.
- NY Cut: 13:30 EST.

Timezone and daylight-saving interpretation must be documented, not silently changed.

02 — THE 5-LAYER BANK SCALE-IN LADDER MATRIX

For a valid unmitigated zone, generate the following five-layer micro-scale grid:

1. Layer 01 — Front-Run Cushion: Upper boundary of zone; 20% allocation.
2. Layer 02 — Consequent Encroachment: FVG 50% midpoint; 20% allocation.
3. Layer 03 — Core Volume POC Centroid: True VWCC core density point; 20% allocation.
4. Layer 04 — Deep Harmonic OTE: 0.705 Fibonacci harmonic retracement; 20% allocation.
5. Layer 05 — Extreme Wick Absorption: Extreme rejection wick base; 20% allocation.

Blended metrics:

- Weighted Average Entry (P_entry).
- Structural Stop Loss.
- Target 01: R:R 1:2.2.
- Target 02: R:R 1:4.2.

03 — EXECUTION & RISK PARAMETERS

- Target 01: R:R 1:2.2; exit 60%.
- Target 02: R:R 1:4.2; remaining runner 40%.
- Safe pyramiding is armed after TP1, when the stop is moved to Break-Even plus ATR cushion.
- Additional L2 positions are funded only from locked-in profit; maximum 30%.

04 — MASTER AUDIT OUTPUT FORMAT

The original strategy requires these report sections:

1. Market State & Regime
   
   - Symbol: XAUUSD
   - Current Price
   - H4 / H1 / M15 alignment
   - Hurst Exponent and regime
   - Bank Zone Quality score/tier

2. Six Evidence Engines Telemetry
   
   - Hurst Memory
   - Garman–Klass Volatility
   - Macro / DXY
   - Kyle Lambda
   - VPIN Toxicity
   - LBMA Fix Clock

3. Bank 5-Layer Iceberg Scale-In Matrix
   
   - Layer
   - Structural Role
   - Exact Limit Price
   - Capital Allocation
   - Status

4. Execution & Risk Parameters
   
   - Weighted Average Entry
   - Structural SL
   - Target 01 — 60% Exit
   - Target 02 — 40% Runner
   - True TPC Score
   - Calibrated Win Probability and Expected Value
   - Safe Pyramiding Status

5. Master Verdict
   
   - BUY LADDER / SELL LADDER / WAIT (NO TRADE)
   - Two-sentence reason and specific instruction

IMPLEMENTATION INSTRUCTIONS

This document is the source strategy. Preserve its terminology, rules, thresholds, five-layer allocations, targets, partial exits, and pyramiding restrictions.

Do not replace it with EMA/RSI or another strategy. Do not invent missing formulas or claim that unspecified calculations are original rules.

First list all undefined formulas, missing data, and ambiguities. Create "requirements_and_assumptions.md". Ask for approval before using any assumption that changes trades.

Use actual broker-supplied XAUUSD M5 data only. Do not fabricate candles, volume, macro data, or performance results. This is a research/backtesting project only; do not place live orders.
