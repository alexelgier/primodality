from itertools import combinations, product
from typing import Tuple, Dict, Set
from primodality.ratio_utils import Ratio, get_mode_ratios, octave_reduce
from primodality.harmonicity_measures import tenney_height
from primodality.mode import Mode
import random


def compute_pitch_classes(branches: Set[int], modes: Set[int]) -> Tuple[Dict[Ratio, Set[Mode]], Dict[Mode, Set[Ratio]]]:
    pitch_classes = {}
    modes_dict = {}
    for branch, mode in product(branches, modes):
        for over in [True, False]:
            cur_mode = Mode(branch, mode, over)
            for pc in get_mode_ratios(mode, over):
                pc = octave_reduce(Ratio(pc.numerator * branch, pc.denominator))
                if pc not in pitch_classes:
                    pitch_classes[pc] = set()
                pitch_classes[pc].add(cur_mode)
                cur_mode.pitch_classes.add(pc)
            modes_dict[cur_mode] = cur_mode.pitch_classes
    return pitch_classes, modes_dict


def compute_mode_distances(modes_dict: Dict[Mode, Set[Ratio]]):
    modes_distance: dict[frozenset[Mode], tuple[float, int, float]] = {}
    for mode_pair in combinations(modes_dict.keys(), 2):
        pair = frozenset(mode_pair)
        common = len(set(modes_dict[mode_pair[0]]).intersection(set(modes_dict[mode_pair[1]])))
        if common > 1:
            intervals = [tenney_height(max(x, y) / min(x, y)) for x in modes_dict[mode_pair[0]] for y in
                         modes_dict[mode_pair[1]]]
            th = sum(intervals) / len(intervals)
            common_weighted = common / min(len(modes_dict[mode_pair[0]]), len(modes_dict[mode_pair[1]]))
            modes_distance[pair] = (-common_weighted, -common, th)
    return modes_distance


def main():
    branches = {1, 7}
    modes = {5, 6, 7, 8, 9}
    print(f"branches {branches}")
    print(f"modes {modes}\n")

    print("Computing pitch classes...")
    pitch_classes, modes_dict = compute_pitch_classes(branches, modes)
    print(f"{len(pitch_classes)} pitch classes")
    print(f"{len(modes_dict)} modes\n")

    print("Computing mode distances...")
    modes_distance = compute_mode_distances(modes_dict)

    print("Top 10 mode relations:")
    for m in sorted(list(modes_distance.keys()), key=lambda x: modes_distance[x])[:10]:
        print(tuple(m), modes_distance[m])

    print(" ")
    print("Pitch Classes:")
    for pc in sorted(pitch_classes.keys()):
        print(pc, pitch_classes[pc])
    print(" ")
    print("Modes:")
    for mode in modes_dict:
        print(mode, modes_dict[mode])
    print(" ")

    chosen_pc = random.choice(list(pitch_classes.keys()))
    print("Chosen pc:", chosen_pc)
    print("Modes:", pitch_classes[chosen_pc])
    chosen_mode = random.choice(list(pitch_classes[chosen_pc]))
    print(" ")
    print("Chosen mode:")
    print("branch", chosen_mode.branch, "- mode", chosen_mode.mode, "- overtone" if chosen_mode.over else "- undertone")
    chosen_mode_pcs = modes_dict[chosen_mode]
    print(sorted(list(chosen_mode_pcs)))
    print(" ")
    print(" ")

    # find ranking of nearest modes
    related_modes = []
    for mode in modes_dict:
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
