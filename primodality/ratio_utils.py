import math
from typing import Tuple, List


class Ratio:
    def __init__(self, numerator: int, denominator: int):
        self.numerator, self.denominator = self.simplify(numerator, denominator)

    @staticmethod
    def simplify(numerator: int, denominator: int) -> Tuple[int, int]:
        """Simplify ratio"""
        gcd = math.gcd(numerator, denominator)
        return numerator // gcd, denominator // gcd

    @staticmethod
    def octave_reduce(numerator: int, denominator: int) -> Tuple[int, int]:
        """Reduce ratio to first octave (1-2)."""
        while numerator % 2 == 0:
            numerator //= 2
        while denominator % 2 == 0:
            denominator //= 2
        while numerator < denominator:
            numerator *= 2
        while denominator * 2 < numerator:
            denominator *= 2
        return Ratio.simplify(numerator, denominator)

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"

    def __mul__(self, other: 'Ratio') -> 'Ratio':
        return Ratio(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other: 'Ratio') -> 'Ratio':
        return Ratio(self.numerator * other.denominator, self.denominator * other.numerator)

    def __eq__(self, other: 'Ratio') -> bool:
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __hash__(self) -> int:
        return hash((self.numerator, self.denominator))

    def __gt__(self, other) -> bool:
        return self.numerator / self.denominator > other.numerator / other.denominator


def get_mode_ratios(mode: int, over: bool = True) -> List[Ratio]:
    """Generate a mode based on the given parameters."""
    if over:
        return [Ratio(mode + i, mode) for i in range(mode)]
    else:
        return [Ratio(mode * 2, mode + (mode - i)) for i in range(mode)]
