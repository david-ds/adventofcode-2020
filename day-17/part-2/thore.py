from collections import defaultdict
import copy
from itertools import product

from tool.runners.python import SubmissionPy

ACTIVE = "#"
INACTIVE = "."
CYCLES = 6


class ThoreSubmission(SubmissionPy):
    def run(self, s, debug=False):
        """
        :param s: input in string format
        :return: solution flag
        """
        pocket_dim = PocketDimension()
        pocket_dim.parse_input(s)

        if debug:
            print("Before any cycle:\n")
            print(pocket_dim, "\n")

        for cycle in range(CYCLES):
            pocket_dim.step()

            if debug:
                print(f"After {cycle+1} cycles:\n")
                print(pocket_dim, "\n")
        return pocket_dim.get_activated_count()


class PocketDimension:
    def __init__(self):
        self.active = set()
        self.n_neighbors = defaultdict(int)
        self.candidates = set()

    def parse_input(self, s):
        lines = s.replace(ACTIVE, "1").replace(INACTIVE, "0").splitlines()
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == "1":
                    self.activate(x, y, 0, 0)

    def activate(self, x, y, z, w):
        self.active.add((x, y, z, w))
        self.candidates.discard((x, y, z, w))
        for neighbor in self.get_neighbours(x, y, z, w):
            self.n_neighbors[neighbor] += 1
            if self.n_neighbors[neighbor] == 3:
                self.candidates.add(neighbor)
            elif self.n_neighbors[neighbor] == 4:
                self.candidates.discard(neighbor)

    def deactivate(self, x, y, z, w):
        self.active.discard((x, y, z, w))
        for neighbor in self.get_neighbours(x, y, z, w):
            self.n_neighbors[neighbor] -= 1
            if self.n_neighbors[neighbor] == 3:
                self.candidates.add(neighbor)
            elif self.n_neighbors[neighbor] == 2:
                self.candidates.discard(neighbor)

    def step(self):
        old_active = self.active.copy()
        old_n_neighbors = self.n_neighbors.copy()
        old_candidates = self.candidates.copy()

        for cube in old_active:
            if old_n_neighbors[cube] not in [2, 3]:
                self.deactivate(*cube)
        for cube in old_candidates - old_active:
            self.activate(*cube)

    def get_activated_count(self):
        return len(self.active)

    @staticmethod
    def get_neighbours(x, y, z, w):
        for dx, dy, dz, dw in product((-1, 0, 1), repeat=4):
            if (dx, dy, dz, dw) != (0, 0, 0, 0):
                yield x + dx, y + dy, z + dz, w + dw

    def __str__(self):
        x_coords, y_coords, z_coords, w_coords = zip(*self.active)
        x_range = (min(x_coords), max(x_coords) + 1)
        y_range = (min(y_coords), max(y_coords) + 1)
        z_range = (min(z_coords), max(z_coords) + 1)
        w_range = (min(w_coords), max(w_coords) + 1)
        lines = []
        for z, w in zip(range(*z_range), range(*w_range)):
            lines.append(f"z={z} w={w}")
            for x in range(*x_range):
                lines.append(
                    "".join(
                        ACTIVE if (x, y, z, w) in self.active else INACTIVE
                        for y in range(*y_range)
                    )
                )

            lines.append("")
        return "\n".join(lines)


def test_day17_part2():
    assert (
        ThoreSubmission().run(
            """.#.
..#
###
"""
        )
        == 848
    )
