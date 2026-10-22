import math
import unittest

from shahkara import formulas as f


class GarmanKlass(unittest.TestCase):
    # Illustrative arithmetic inputs, NOT market data.
    def test_exact_formula(self):
        o, h, l, c = 100.0, 102.0, 99.0, 101.0
        expected = 0.5 * math.log(102 / 99) ** 2 - (2 * math.log(2) - 1) * math.log(101 / 100) ** 2
        self.assertAlmostEqual(f.garman_klass_variance(o, h, l, c), expected, places=15)

    def test_flat_bar_is_zero(self):
        self.assertEqual(f.garman_klass_variance(5, 5, 5, 5), 0.0)

    def test_sigma_is_sqrt(self):
        v = f.garman_klass_variance(100, 102, 99, 101)
        self.assertAlmostEqual(f.garman_klass_sigma(100, 102, 99, 101), math.sqrt(v))

    def test_negative_variance_raises(self):
        # A close far outside [L, H] (invalid bar) gives negative variance;
        # it must raise, not be clamped silently.
        with self.assertRaises(ValueError):
            f.garman_klass_sigma(100, 100.1, 100.0, 105.0)

    def test_bad_inputs(self):
        with self.assertRaises(ValueError):
            f.garman_klass_variance(0, 1, 1, 1)
        with self.assertRaises(ValueError):
            f.garman_klass_variance(1, 1, 2, 1)

    def test_sl_buffer_max(self):
        self.assertEqual(f.sl_buffer(2.0, 1.0), 3.0)
        self.assertAlmostEqual(f.sl_buffer(0.1, 10.0), 3.5)


class GarmanKlassUnits(unittest.TestCase):
    """sigma_GK is a dimensionless per-bar log-return quantity."""
    def test_hand_computed_value(self):
        # ln(102/99)=0.029852963..., ln(101/100)=0.009950330...
        # 0.5*0.029852963^2 - 0.386294361*0.009950330^2 = 4.0735e-4
        v = f.garman_klass_variance(100.0, 102.0, 99.0, 101.0)
        self.assertAlmostEqual(v, 4.455997044e-4 - 3.824665088e-5, places=12)

    def test_price_scale_invariant(self):
        a = f.garman_klass_variance(100.0, 102.0, 99.0, 101.0)
        b = f.garman_klass_variance(4000.0, 4080.0, 3960.0, 4040.0)
        self.assertAlmostEqual(a, b, places=15)

    def test_nonnegative_for_valid_bars(self):
        # every bar with L <= O,C <= H on a coarse grid
        vals = [98.0, 99.0, 100.0, 101.0, 102.0]
        for l in vals:
            for h in vals:
                if h < l:
                    continue
                for o in [x for x in vals if l <= x <= h]:
                    for c in [x for x in vals if l <= x <= h]:
                        self.assertGreaterEqual(f.garman_klass_variance(o, h, l, c), -1e-18)

    def test_sigma_is_unitless_not_price(self):
        # ~0.02 for a ~2% range: clearly not USD. ATR (USD) is not.
        self.assertLess(f.garman_klass_sigma(100.0, 102.0, 99.0, 101.0), 0.05)


class Layers(unittest.TestCase):
    def test_five_layers_of_twenty_percent(self):
        a = f.layer_allocations()
        self.assertEqual(len(a), 5)
        self.assertTrue(all(p == 0.20 for _, p in a))
        self.assertAlmostEqual(sum(p for _, p in a), 1.0)

    def test_order_and_names(self):
        self.assertEqual([n for n, _ in f.layer_allocations()], [
            "Front-Run Cushion", "Consequent Encroachment",
            "Core Volume POC Centroid", "Deep Harmonic OTE",
            "Extreme Wick Absorption"])

    def test_exit_fractions(self):
        self.assertAlmostEqual(f.TP1_EXIT_FRACTION + f.TP2_RUNNER_FRACTION, 1.0)


class RiskReward(unittest.TestCase):
    def test_buy(self):
        tp1, tp2 = f.rr_targets(100.0, 90.0, "BUY")
        self.assertAlmostEqual(tp1, 122.0)
        self.assertAlmostEqual(tp2, 142.0)

    def test_sell(self):
        tp1, tp2 = f.rr_targets(100.0, 110.0, "SELL")
        self.assertAlmostEqual(tp1, 78.0)
        self.assertAlmostEqual(tp2, 58.0)

    def test_ratio_exact(self):
        for d, stop in (("BUY", 1990.37), ("SELL", 2010.91)):
            entry = 2000.0
            risk = abs(entry - stop)
            tp1, tp2 = f.rr_targets(entry, stop, d)
            self.assertAlmostEqual(abs(tp1 - entry) / risk, 2.2)
            self.assertAlmostEqual(abs(tp2 - entry) / risk, 4.2)

    def test_direction_of_targets(self):
        b1, b2 = f.rr_targets(100, 95, "BUY")
        s1, s2 = f.rr_targets(100, 105, "SELL")
        self.assertTrue(100 < b1 < b2)
        self.assertTrue(s2 < s1 < 100)

    def test_zero_risk_rejected(self):
        with self.assertRaises(ValueError):
            f.rr_targets(100, 100, "BUY")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            f.rr_targets(100, 101, "BUY")
        with self.assertRaises(ValueError):
            f.rr_targets(100, 99, "SELL")
        with self.assertRaises(ValueError):
            f.rr_targets(100, 99, "HOLD")


if __name__ == "__main__":
    unittest.main()
