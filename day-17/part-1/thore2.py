import numpy as np
from scipy.signal import convolve

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        n_dims = 3
        n_cycles = 6

        lines = s.splitlines()
        inital_shape = (len(lines), len(lines[0])) + (1,) * (n_dims - 2)
        final_shape = tuple(i + 2 * n_cycles for i in inital_shape)
        state = np.zeros(final_shape, dtype=bool)

        for x, line in enumerate(s.splitlines()):
            for y, c in enumerate(line):
                if c == "#":
                    state[
                        (x + n_cycles, y + n_cycles) + (n_cycles,) * (n_dims - 2)
                    ] = True

        neighbors_kernel = np.ones((3,) * n_dims, dtype=int)
        neighbors_kernel[(1,) * n_dims] = 0

        for cycle in range(n_cycles):
            idx = tuple(
                slice(n_cycles - cycle - 1, n_cycles + cycle + 2 + inital_shape[i])
                for i in range(2)
            ) + (slice(n_cycles - cycle - 1, n_cycles + cycle + 2),) * (n_dims - 2)
            n_neighbors = convolve(
                state[idx],
                neighbors_kernel,
                mode="same",
            )
            state[idx] = (state[idx] & ((n_neighbors == 2) | (n_neighbors == 3))) | (
                (~state[idx]) & (n_neighbors == 3)
            )

        return state.sum()


def test_day17_part1():
    assert (
        ThoreSubmission().run(
            """.#.
..#
###
"""
        )
        == 112
    )
