import unittest
from primodality.ratio_utils import Ratio, get_mode_ratios


class TestRatio(unittest.TestCase):
    def test_simplify(self):
        r = Ratio(4, 6)
        self.assertEqual((r.numerator, r.denominator), (2, 3))
        r = Ratio(6, 3)
        self.assertEqual((r.numerator, r.denominator), (2, 1))

    def test_multiplication(self):
        r1 = Ratio(1, 2)
        r2 = Ratio(3, 4)
        result = r1 * r2
        self.assertEqual((result.numerator, result.denominator), (3, 8))

    def test_division(self):
        r1 = Ratio(3, 4)
        r2 = Ratio(1, 2)
        result = r1 / r2
        self.assertEqual((result.numerator, result.denominator), (3, 2))

    def test_repr(self):
        r = Ratio(3, 4)
        self.assertEqual(repr(r), "3/4")


class TestRatioUtils(unittest.TestCase):

    def test_octave_reduce(self):
        result = Ratio.octave_reduce(9,4)
        self.assertEqual(result, (9, 8))

    def test_get_mode_over(self):
        mode = get_mode_ratios(5, over=True)
        expected = [Ratio(5, 5), Ratio(6, 5), Ratio(7, 5),
                    Ratio(8, 5), Ratio(9, 5)]
        self.assertEqual([(r.numerator, r.denominator) for r in expected],
                         [(r.numerator, r.denominator) for r in mode])

    def test_get_mode_under(self):
        mode = get_mode_ratios(5, over=False)
        expected = [Ratio(10, 10), Ratio(10, 9),
                    Ratio(10, 8), Ratio(10, 7),
                    Ratio(10, 6)]
        self.assertEqual([(r.numerator, r.denominator) for r in expected],
                         [(r.numerator, r.denominator) for r in mode])


if __name__ == '__main__':
    unittest.main()
