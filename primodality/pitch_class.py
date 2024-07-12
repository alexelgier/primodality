from primodality.ratio_utils import Ratio


class PitchClass(Ratio):
    def __init__(self, numerator: int, denominator: int):
        self.numerator, self.denominator = self.octave_reduce(numerator, denominator)
        self.modes = set()

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}{' - Modes: ' + str(self.modes) if len(self.modes) > 0 else ''}"