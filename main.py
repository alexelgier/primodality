from itertools import combinations, product
from typing import Tuple, Dict, Set

from primodality.pitch_class import PitchClass
from primodality.ratio_utils import Ratio, get_mode_ratios
from primodality.harmonicity_measures import tenney_height
from primodality.mode import Mode
import random


def make_pitch_classes_and_modes(branches: Set[int], modes: Set[int]) -> Tuple[Set[PitchClass], Set[Mode]]:
    pcs_dict, modes_dict = {}, {}
    pcs_set, modes_set = set(), set()
    for branch, mode in product(branches, modes):
        for over in [True, False]:
            cur_mode = (branch, mode, over)
            for note in get_mode_ratios(mode, over):
                pc = PitchClass.octave_reduce(note.numerator * branch, note.denominator)
                if pc not in pcs_dict:
                    pcs_dict[pc] = set()
                pcs_dict[pc].add(cur_mode)
                if cur_mode not in modes_dict:
                    modes_dict[cur_mode] = set()
                modes_dict[cur_mode].add(pc)
    for pc in pcs_dict:
        new_pc = PitchClass(*pc)
        new_pc.modes.update({Mode(*x) for x in pcs_dict[pc]})
        pcs_set.add(new_pc)
    for mode in modes_dict:
        new_mode = Mode(*mode)
        new_mode.pitch_classes.update({PitchClass(*x) for x in modes_dict[mode]})
        modes_set.add(new_mode)
    return pcs_set, modes_set


def compute_mode_distances(modes: Set[Mode]):
    modes_distance: dict[frozenset[Mode], tuple[float, int, float]] = {}
    for mode_pair in combinations(modes, 2):
        pair = frozenset(mode_pair)
        common = len(mode_pair[0].pitch_classes.intersection(mode_pair[1].pitch_classes))
        if common > 1:
            intervals = [tenney_height(max(x, y) / min(x, y)) for x in mode_pair[0].pitch_classes for y in
                         mode_pair[1].pitch_classes]
            th = sum(intervals) / len(intervals)
            common_weighted = common / min(len(mode_pair[0].pitch_classes), len(mode_pair[1].pitch_classes))
            modes_distance[pair] = (-common_weighted, -common, th)
    return modes_distance


BRANCHES = {1, 3, 5, 7}
MODES = {5, 6, 7, 8, 9}


def main():
    print(f"branches {BRANCHES}")
    print(f"modes {MODES}")
    print(" ")

    print("Computing pitch classes and modes...")
    pcs, modes = make_pitch_classes_and_modes(BRANCHES, MODES)

    print(f"{len(pcs)} pitch classes")
    print(f"{len(modes)} modes")
    print(" ")

    print("Computing mode distances...")
    modes_distance = compute_mode_distances(modes)

    print("Top 10 mode relations:")
    for m in sorted(list(modes_distance.keys()), key=lambda x: modes_distance[x])[:10]:
        print(tuple(m), modes_distance[m])

    print(" ")
    print("Pitch Classes:")
    for pc in sorted(pcs):
        print(pc)
    print(" ")
    print("Modes:")
    for mode in modes:
        print(mode, modes)
    print(" ")

    chosen_pc = random.choice(list(pcs))
    print("Chosen PC:", chosen_pc)
    chosen_mode = random.choice(list(chosen_pc.modes))
    print("Chosen Mode:", chosen_mode)
    chosen_mode_pcs = chosen_mode.pitch_classes
    print(sorted(list(chosen_mode_pcs)))
    print(" ")
    print(" ")

    # find ranking of nearest modes
    related_modes = []
    for mode in modes:
        if mode != chosen_mode:
            pair = frozenset((mode, chosen_mode))
            if pair in modes_distance:
                d = modes_distance[pair]
                related_modes.append((mode, d))
    related_modes = sorted(related_modes, key=lambda x: x[1])

    top = random.randint(1, len(related_modes) - 1)
    print("Choosing new mode from top", top)
    chosen_mode_2 = random.choice(related_modes[:top])
    print("Chosen mode 2:", chosen_mode_2)
    common_tones = set(modes_dict[chosen_mode_2[0]]).intersection(set(chosen_mode_pcs))
    print("Common:", common_tones)

    print("")
    print("Mode 1:", chosen_mode)
    print("Unique Tones 1:", sorted(list(set(chosen_mode_pcs) - common_tones)))
    print("Common Tones:", sorted(list(common_tones)))
    print("Unique Tones 2:", sorted(list(set(modes_dict[chosen_mode_2[0]]) - common_tones)))
    print("Mode 2:", chosen_mode_2[0])


if __name__ == "__main__":
    main()
