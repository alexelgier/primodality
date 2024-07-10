import unittest
import math
from primodality.harmonicity_measures import (
    prime_factors, tenney_height, wilson_height,
    geometric_mean, calculate_chord_heights
)
from primodality.ratio_utils import Ratio


class TestHarmonicityMeasures(unittest.TestCase):

    def test_prime_factors(self):
        self.assertEqual(prime_factors(12), [2, 2, 3])
        self.assertEqual(prime_factors(17), [17])
        self.assertEqual(prime_factors(1), [])

    def test_tenney_height(self):
        self.assertAlmostEqual(tenney_height(Ratio(3, 2)), math.log2(6), places=7)
        self.assertAlmostEqual(tenney_height(Ratio(1, 1)), 0, places=7)
        self.assertAlmostEqual(tenney_height(Ratio(4, 3)), math.log2(12), places=7)

    def test_wilson_height(self):
        self.assertEqual(wilson_height(Ratio(3, 2)), 5)  # 3 + 2
        self.assertEqual(wilson_height(Ratio(1, 1)), 0)  # 0 + 0
        self.assertEqual(wilson_height(Ratio(4, 3)), 7)  # 2 + 2 + 3

    def test_geometric_mean(self):
        self.assertAlmostEqual(geometric_mean([1, 4, 9]), 3.3019272, places=7)
        self.assertAlmostEqual(geometric_mean([2, 8]), 4, places=7)

    def test_calculate_chord_heights(self):
        ratios = [Ratio(1, 1), Ratio(5, 4), Ratio(3, 2)]
        heights = calculate_chord_heights(ratios)

        # Check if all expected keys are present
        expected_keys = ['tenney_height_arithmetic', 'tenney_height_geometric',
                         'wilson_height_arithmetic', 'wilson_height_geometric']
        for key in expected_keys:
            self.assertIn(key, heights)

        # Check if values are of correct type and in reasonable range
        for value in heights.values():
            self.assertIsInstance(value, float)
            self.assertGreater(value, 0)

        # Test a specific value (you may need to adjust this based on your exact implementation)
        self.assertAlmostEqual(heights['tenney_height_arithmetic'], 3.937927, places=5)

    def test_edge_cases(self):
        # Test with unity ratio
        self.assertEqual(tenney_height(Ratio(1, 1)), 0)
        self.assertEqual(wilson_height(Ratio(1, 1)), 0)

        # Test with prime number ratio
        self.assertAlmostEqual(tenney_height(Ratio(17, 19)),
                               math.log2(17 * 19), places=7)
        self.assertEqual(wilson_height(Ratio(17, 19)), 36)  # 17 + 19

        # Test geometric mean with single value
        self.assertAlmostEqual(geometric_mean([5]), 5,7)

        # Test calculate_chord_heights with single ratio
        single_ratio_heights = calculate_chord_heights([Ratio(1, 1)])
        for value in single_ratio_heights.values():
            self.assertEqual(value, 0)  # All heights should be 0 for a single ratio


if __name__ == '__main__':
    unittest.main()
