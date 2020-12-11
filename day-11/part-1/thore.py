import numpy as np
from scipy.signal import convolve2d

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        lines = s.splitlines()
        height, width = len(lines), len(lines[0])
        seat_mask = np.zeros((height, width), dtype=bool)
        seat_status = np.zeros((height, width), dtype=bool)
        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                seat_mask[i, j] = c != "."
                seat_status[i, j] = c == "#"

        adjacent = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)

        stable = False
        while not stable:
            n_neighbors = convolve2d(seat_status, adjacent, mode="same")
            new_occupied = seat_mask & ~seat_status & (n_neighbors == 0)
            new_empty = seat_status & (n_neighbors >= 4)
            stable = (new_occupied.sum() + new_empty.sum()) == 0
            seat_status[new_occupied] = True
            seat_status[new_empty] = False

        return seat_status.sum()