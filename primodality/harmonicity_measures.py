import math
from typing import List
from primodality.ratio_utils import Ratio


def prime_factors(n: int) -> List[int]:
    """Calculate the prime factors of a number."""
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors


def tenney_height(ratio: Ratio) -> float:
    """Calculate the Tenney height of a ratio."""
    return math.log2(ratio.numerator * ratio.denominator)


def wilson_height(ratio: Ratio) -> float:
    """Calculate the Wilson height of a ratio."""
    factors = prime_factors(ratio.numerator) + prime_factors(ratio.denominator)
    return sum(factors)


def geometric_mean(values: List[float]) -> float:
    """Calculate the geometric mean of a list of values."""
    return math.exp(sum(math.log(x) for x in values) / len(values)) if len(values) != 0 else 0


def calculate_chord_heights(ratios: List[Ratio]) -> dict:
    """Calculate various harmonicity measures for a chord."""
    intervals = [r2 / r1 for i, r1 in enumerate(ratios) for r2 in ratios[i + 1:]]

    th_values = [tenney_height(i) for i in intervals]
    wh_values = [wilson_height(i) for i in intervals]

    return {
        'tenney_height_arithmetic': sum(th_values) / len(th_values) if len(th_values) != 0 else 0,
        'tenney_height_geometric': geometric_mean(th_values),
        'wilson_height_arithmetic': sum(wh_values) / len(wh_values) if len(wh_values) != 0 else 0,
        'wilson_height_geometric': geometric_mean(wh_values)
    }


# Example usage
if __name__ == "__main__":
    ratios = [Ratio(1, 1), Ratio(5, 4), Ratio(3, 2)]
    heights = calculate_chord_heights(ratios)
    for measure, value in heights.items():
        print(f"{measure}: {value}")
