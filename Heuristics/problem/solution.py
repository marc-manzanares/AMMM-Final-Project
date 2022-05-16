from Heuristics.solution import _Solution


class Solution(_Solution):
    def __init__(self, sequence, distances):
        self.sequence = sequence
        self.distances = distances
        super().__init__()

