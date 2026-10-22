"""CSV loader for broker-supplied XAUUSD M5 bars. No data is generated."""
import csv
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

REQUIRED_COLUMNS = ("time", "open", "high", "low", "close", "tick_volume")


@dataclass(frozen=True)
class Bar:
    time: datetime  # timezone-aware
    open: float
    high: float
    low: float
    close: float
    tick_volume: float


def load_csv(path, utc_offset_hours):
    """Load bars. `utc_offset_hours` (broker server offset) is mandatory:
    the spec requires time zones to be documented, never guessed. A fixed
    offset cannot express broker DST; that rule is still an open question."""
    tz = timezone(timedelta(hours=utc_offset_hours))
    bars = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns: {missing}")
        for n, row in enumerate(reader, start=2):
            try:
                t = datetime.fromisoformat(row["time"]).replace(tzinfo=tz)
                bars.append(Bar(t, float(row["open"]), float(row["high"]),
                                float(row["low"]), float(row["close"]),
                                float(row["tick_volume"])))
            except ValueError as e:
                raise ValueError(f"{path}:{n}: bad row: {e}") from e
    return bars
