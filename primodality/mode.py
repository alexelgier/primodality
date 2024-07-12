class Mode:
    def __init__(self, branch: int, mode: int, over: bool):
        self.branch = branch
        self.mode = mode
        self.over = over
        self.pitch_classes = set()

    def get_pitch_classes_ordered(self):
        return sorted(list(self.pitch_classes))

    def __repr__(self):
        return (f"b{self.branch} m{self.mode} {'over' if self.over else 'under'}"
                f"{' - Pitch Classes: ' + str(self.get_pitch_classes_ordered()) if len(self.pitch_classes) > 0 else ''}")

    def __eq__(self, other):
        return self.branch == other.branch and self.mode == other.mode and self.over == other.over

    def __hash__(self):
        return hash((self.branch, self.mode, self.over))
