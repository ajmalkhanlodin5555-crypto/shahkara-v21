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

    def test_invalid(self):
        with self.assertRaises(ValueError):
            f.rr_targets(100, 101, "BUY")
        with self.assertRaises(ValueError):
            f.rr_targets(100, 99, "SELL")
        with self.assertRaises(ValueError):
            f.rr_targets(100, 99, "HOLD")


if __name__ == "__main__":
    unittest.main()
