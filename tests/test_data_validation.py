import os
import tempfile
import unittest
from datetime import datetime, timezone

from shahkara.data import Bar, load_csv
from shahkara.validation import validate_bars

UTC = timezone.utc


def bar(minute, o=10, h=12, l=9, c=11, v=1, hour=0):
    # Synthetic structural fixtures for testing the validator only.
    return Bar(datetime(2024, 1, 1, hour, minute, tzinfo=UTC), o, h, l, c, v)


def codes(issues):
    return [c for c, _, _ in issues]


class Validation(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(validate_bars([bar(0), bar(5), bar(10)]), [])

    def test_empty(self):
        self.assertEqual(codes(validate_bars([])), ["EMPTY"])

    def test_duplicate_and_order(self):
        self.assertIn("DUPLICATE_TIME", codes(validate_bars([bar(5), bar(5)])))
        self.assertIn("NON_MONOTONIC", codes(validate_bars([bar(10), bar(5)])))

    def test_gap(self):
        self.assertEqual(codes(validate_bars([bar(0), bar(15)])), ["GAP"])

    def test_ohlc(self):
        self.assertIn("OHLC_INCONSISTENT", codes(validate_bars([bar(0, h=10, c=11)])))
        self.assertIn("OHLC_INCONSISTENT", codes(validate_bars([bar(0, l=10.5)])))

    def test_non_positive_and_volume(self):
        c = codes(validate_bars([bar(0, o=0, l=-1)]))
        self.assertIn("NON_POSITIVE_PRICE", c)
        self.assertIn("NEGATIVE_VOLUME", codes(validate_bars([bar(0, v=-1)])))

    def test_off_grid(self):
        self.assertIn("OFF_GRID", codes(validate_bars([bar(3)])))

    def test_jump_optional(self):
        bars = [bar(0, 10, 12, 9, 10), bar(5, 20, 21, 19, 20)]
        self.assertEqual(validate_bars(bars), [])
        self.assertIn("JUMP", codes(validate_bars(bars, max_jump_pct=5)))


class Loader(unittest.TestCase):
    def _write(self, text):
        fd, p = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w") as fh:
            fh.write(text)
        self.addCleanup(os.remove, p)
        return p

    def test_load(self):
        p = self._write("time,open,high,low,close,tick_volume\n2024-01-01 00:00,10,12,9,11,5\n")
        bars = load_csv(p, utc_offset_hours=2)
        self.assertEqual(len(bars), 1)
        self.assertEqual(bars[0].time.utcoffset().total_seconds(), 7200)
        self.assertEqual(bars[0].close, 11.0)

    def test_missing_column(self):
        with self.assertRaises(ValueError):
            load_csv(self._write("time,open\n"), 0)

    def test_bad_row(self):
        p = self._write("time,open,high,low,close,tick_volume\nx,1,1,1,1,1\n")
        with self.assertRaises(ValueError):
            load_csv(p, 0)


if __name__ == "__main__":
    unittest.main()
