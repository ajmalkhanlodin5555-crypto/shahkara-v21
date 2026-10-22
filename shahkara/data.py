"""CSV loader for broker-supplied XAUUSD M5 bars. No data is generated.

Accepts the broker M5 column names used so far (`tick_volume`) and the
Dukascopy M5 schema (`volume` = bid+ask traded volume, plus optional `spread`
= mean bid-ask). Real broker data only; nothing is generated here.
"""
import csv
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

REQUIRED_COLUMNS = ("time", "open", "high", "low", "close")
REQUIRED_VOLUME_COLUMNS = ("tick_volume", "volume")


@dataclass(frozen=True)
class Bar:
    time: datetime  # timezone-aware
    open: float
    high: float
    low: float
    close: float
    tick_volume: float
    spread: float | None = None


def load_csv(path, utc_offset_hours):
    """Load bars. `utc_offset_hours` (broker server offset) is mandatory:
    the spec requires time zones to be documented, never guessed. A fixed
    offset cannot express broker DST; that rule is still an open question."""
    tz = timezone(timedelta(hours=utc_offset_hours))
    bars = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        fieldnames = set(reader.fieldnames or [])
        if not any(c in fieldnames for c in REQUIRED_VOLUME_COLUMNS):
            missing.append(f"one of {list(REQUIRED_VOLUME_COLUMNS)}")
        if missing:
            raise ValueError(f"missing columns: {missing}")
        for n, row in enumerate(reader, start=2):
            try:
                t = datetime.fromisoformat(row["time"]).replace(tzinfo=tz)
                vol_col = "tick_volume" if "tick_volume" in (reader.fieldnames or []) else "volume"
                spread_col = "spread" if "spread" in (reader.fieldnames or []) else None
                bars.append(Bar(t, float(row["open"]), float(row["high"]),
                                float(row["low"]), float(row["close"]),
                                float(row[vol_col]),
                                float(row[spread_col]) if spread_col else None))
            except ValueError as e:
                raise ValueError(f"{path}:{n}: bad row: {e}") from e
    return bars
