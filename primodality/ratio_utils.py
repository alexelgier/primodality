import math
from typing import Tuple, List


class Ratio:
    def __init__(self, numerator: int, denominator: int):
        self.numerator, self.denominator = self.simplify(numerator, denominator)

    @staticmethod
    def simplify(numerator: int, denominator: int) -> Tuple[int, int]:
        gcd = math.gcd(numerator, denominator)
        return numerator // gcd, denominator // gcd

    def __repr__(self):
        return f"Ratio({self.numerator}/{self.denominator})"

    def __mul__(self, other: 'Ratio') -> 'Ratio':
        return Ratio(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: 'Ratio') -> 'Ratio':
        return Ratio(self.numerator * other.denominator, self.denominator * other.numerator)

    def __eq__(self, other: 'Ratio') -> bool:
        return self.numerator == other.numerator and self.denominator == other.denominator


def simplify_octave(ratio: Ratio) -> Ratio:
    """Remove octaves from ratio (all powers of 2)
    ex: 6/2 -> 3/1
        18/4 -> 9/1
        8/7 -> 1/7"""
    num, den = ratio.numerator, ratio.denominator
    while num % 2 == 0:
        num //= 2
    while den % 2 == 0:
        den //= 2
    return Ratio(num, den)


def octave_reduce(ratio: Ratio) -> Ratio:
    """Reduce ratio to first octave (1-2)."""
    ratio = simplify_octave(ratio)
    num, den = ratio.numerator, ratio.denominator
    while num < den:
        num *= 2
    while den * 2 < num:
        den *= 2
    return Ratio(num, den)


def get_mode(mode: int, over: bool = True) -> List[Ratio]:
    """Generate a mode based on the given parameters."""
    if over:
        return [Ratio(mode + i, mode) for i in range(mode)]
    else:
        return [Ratio(mode * 2, mode + (mode - i)) for i in range(mode)]
