"""Report-only validation of M5 bars. Never alters or fills data."""
from datetime import timedelta

BAR = timedelta(minutes=5)


def validate_bars(bars, max_jump_pct=None):
    """Return a list of (code, index, message). Empty list means no findings.

    Gaps are reported, not judged: the broker session calendar is unknown.
    `max_jump_pct` is optional; no default threshold is invented.
    """
    issues = []
    if not bars:
        return [("EMPTY", -1, "no bars")]
    for i, b in enumerate(bars):
        if min(b.open, b.high, b.low, b.close) <= 0:
            issues.append(("NON_POSITIVE_PRICE", i, "price <= 0"))
        if not (b.low <= min(b.open, b.close) and max(b.open, b.close) <= b.high):
            issues.append(("OHLC_INCONSISTENT", i, "low/high do not bound open/close"))
        if b.tick_volume < 0:
            issues.append(("NEGATIVE_VOLUME", i, "tick_volume < 0"))
        if b.time.minute % 5 or b.time.second:
            issues.append(("OFF_GRID", i, "timestamp not on 5-minute boundary"))
        if i == 0:
            continue
        prev = bars[i - 1]
        d = b.time - prev.time
        if d == timedelta(0):
            issues.append(("DUPLICATE_TIME", i, str(b.time)))
        elif d < timedelta(0):
            issues.append(("NON_MONOTONIC", i, f"{b.time} before {prev.time}"))
        elif d > BAR:
            issues.append(("GAP", i, f"{d} between {prev.time} and {b.time}"))
        if max_jump_pct is not None and prev.close > 0:
            jump = abs(b.open - prev.close) / prev.close * 100
            if jump > max_jump_pct:
                issues.append(("JUMP", i, f"open-vs-prev-close {jump:.3f}%"))
    return issues
