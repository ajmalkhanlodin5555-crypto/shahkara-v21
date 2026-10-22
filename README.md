# shahkara-v21

Research/backtesting project for the SHAHKARA v21 XAUUSD strategy. No live trading.

- Spec (verbatim): `docs/SHAHKARA_v21_SPEC.md`
- Open questions and data needs: `requirements_and_assumptions.md`
- Run tests: `python3 -m unittest discover -s tests -t .` (standard library only)

## Implemented (safe, no trade-affecting assumptions)
Garman-Klass variance/sigma and SL buffer, five 20% layer allocations, TP1/TP2 R:R math, CSV loader, report-only M5 validator.

## Not implemented
See "Unfinished components" in `requirements_and_assumptions.md`.
