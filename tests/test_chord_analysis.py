import unittest
from primodality.ratio_utils import Ratio
from primodality.chord_analysis import Chord, generate_chords, analyze_chords, get_best_chords


class TestChord(unittest.TestCase):
    def setUp(self):
        self.ratios = [Ratio(1, 1), Ratio(5, 4), Ratio(3, 2)]
        self.chord = Chord(self.ratios)

    def test_chord_initialization(self):
        self.assertEqual(len(self.chord.ratios), 3)
        self.assertEqual(len(self.chord.intervals), 3)

    def test_chord_intervals(self):
        expected_intervals = [Ratio(5, 4), Ratio(3, 2), Ratio(6, 5)]
        self.assertEqual(tuple(self.chord.intervals), tuple(expected_intervals))

    def test_tenney_height(self):
        # This is an approximation, you may need to adjust the precision
        self.assertAlmostEqual(self.chord.get_tenney_height(), 3.937927, places=5)

    def test_wilson_height(self):
        # This is an approximation, you may need to adjust the precision
        self.assertAlmostEqual(self.chord.get_wilson_height(), 8.0, places=5)


class TestChordAnalysis(unittest.TestCase):
    def setUp(self):
        self.pitch_classes = [Ratio(1, 1), Ratio(5, 4), Ratio(3, 2), Ratio(7, 4)]

    def test_generate_chords(self):
        triads = generate_chords(self.pitch_classes, 3)
        self.assertEqual(len(triads), 4)  # 4C3 = 4

    def test_analyze_chords(self):
        triads = generate_chords(self.pitch_classes, 3)
        analyzed_triads = analyze_chords(triads)
        self.assertEqual(len(analyzed_triads), 4)
        self.assertTrue(all(isinstance(chord, Chord) for chord, _ in analyzed_triads))
        self.assertTrue(all(isinstance(analysis, dict) for _, analysis in analyzed_triads))
        self.assertTrue(all('tenney_height' in analysis and 'wilson_height' in analysis
                            for _, analysis in analyzed_triads))

    def test_get_best_chords(self):
        triads = generate_chords(self.pitch_classes, 3)
        analyzed_triads = analyze_chords(triads)
        best_triads = get_best_chords(analyzed_triads, 2)
        self.assertEqual(len(best_triads), 2)
        self.assertTrue(best_triads[0][1]['tenney_height'] <= best_triads[1][1]['tenney_height'])


if __name__ == '__main__':
    unittest.main()
