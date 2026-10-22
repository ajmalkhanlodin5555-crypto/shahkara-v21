"""Exact formulas taken verbatim from docs/SHAHKARA_v21_SPEC.md.

Only quantities the spec fully defines live here. Nothing is inferred.
"""
import math

LAYER_COUNT = 5
LAYER_ALLOCATION = 0.20  # spec section 02: every layer is 20%
LAYER_NAMES = (
    "Front-Run Cushion",
    "Consequent Encroachment",
    "Core Volume POC Centroid",
    "Deep Harmonic OTE",
    "Extreme Wick Absorption",
)
TP1_RR = 2.2
TP2_RR = 4.2
TP1_EXIT_FRACTION = 0.60
TP2_RUNNER_FRACTION = 0.40


def garman_klass_variance(open_, high, low, close):
    """sigma_GK^2 = 0.5*[ln(H/L)]^2 - (2*ln(2)-1)*[ln(C/O)]^2 (one bar)."""
    for name, v in (("open", open_), ("high", high), ("low", low), ("close", close)):
        if not v > 0:
            raise ValueError(f"{name} must be > 0, got {v!r}")
    if high < low:
        raise ValueError("high must be >= low")
    return (0.5 * math.log(high / low) ** 2
            - (2 * math.log(2) - 1) * math.log(close / open_) ** 2)


def garman_klass_sigma(open_, high, low, close):
    """sigma_GK = sqrt(variance). Raises if variance is negative (no clamping)."""
    var = garman_klass_variance(open_, high, low, close)
    if var < 0:
        raise ValueError(f"negative Garman-Klass variance {var!r}")
    return math.sqrt(var)


def sl_buffer(sigma_gk, atr):
    """SL Buffer = max(sigma_GK*1.5, ATR*0.35). ATR is supplied by the caller;
    its period/smoothing is undefined in the spec."""
    return max(sigma_gk * 1.5, atr * 0.35)


def layer_allocations():
    """Five layers of 20% each, in spec order."""
    return [(name, LAYER_ALLOCATION) for name in LAYER_NAMES]


def rr_targets(entry, stop, direction):
    """TP1 at 1:2.2 and TP2 at 1:4.2 measured from `entry` to `stop`.

    direction: 'BUY' or 'SELL'. The caller supplies entry and stop; how they
    are derived (blended entry, structural SL) is undefined in the spec.
    """
    if direction == "BUY":
        risk = entry - stop
    elif direction == "SELL":
        risk = stop - entry
    else:
        raise ValueError("direction must be 'BUY' or 'SELL'")
    if risk <= 0:
        raise ValueError("stop must be on the losing side of entry")
    sign = 1 if direction == "BUY" else -1
    return entry + sign * TP1_RR * risk, entry + sign * TP2_RR * risk
