from typing import List, Tuple, Dict
from primodality.ratio_utils import Ratio
from primodality.harmonicity_measures import tenney_height, wilson_height


class Chord:
    def __init__(self, ratios: List[Ratio]):
        self.ratios = sorted(ratios, key=lambda r: r.numerator / r.denominator)
        self.intervals = self._calculate_intervals()

    def _calculate_intervals(self) -> List[Ratio]:
        intervals = []
        for i in range(len(self.ratios)):
            for j in range(i + 1, len(self.ratios)):
                interval = self.ratios[j] / self.ratios[i]
                intervals.append(Ratio.octave_reduce(*interval))
        return intervals

    def get_tenney_height(self) -> float:
        return sum(tenney_height(i) for i in self.intervals) / len(self.intervals)

    def get_wilson_height(self) -> float:
        return sum(wilson_height(i) for i in self.intervals) / len(self.intervals)

    def __repr__(self):
        return f"Chord({self.ratios})"


def generate_chords(pitch_classes: List[Ratio], size: int) -> List[Chord]:
    from itertools import combinations
    return [Chord(list(combo)) for combo in combinations(pitch_classes, size)]


def analyze_chords(chords: List[Chord]) -> List[Tuple[Chord, Dict[str, float]]]:
    analyzed_chords = []
    for chord in chords:
        analysis = {
            'tenney_height': chord.get_tenney_height(),
            'wilson_height': chord.get_wilson_height(),
        }
        analyzed_chords.append((chord, analysis))
    return sorted(analyzed_chords, key=lambda x: (x[1]['tenney_height'], x[1]['wilson_height']))


def get_best_chords(analyzed_chords: List[Tuple[Chord, Dict[str, float]]], n: int = 10) -> List[Tuple[Chord, Dict[str, float]]]:
    return analyzed_chords[:n]


# Usage example
if __name__ == "__main__":
    # This is just an example, you'd typically import your pitch classes from elsewhere
    pitch_classes = [Ratio(1, 1), Ratio(5, 4), Ratio(3, 2), Ratio(7, 4)]

    triads = generate_chords(pitch_classes, 3)
    analyzed_triads = analyze_chords(triads)
    best_triads = get_best_chords(analyzed_triads)

    for chord, analysis in best_triads:
        print(f"Chord: {chord}")
        print(f"Tenney Height: {analysis['tenney_height']:.4f}")
        print(f"Wilson Height: {analysis['wilson_height']:.4f}")
        print()
