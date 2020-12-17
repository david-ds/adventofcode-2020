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
        pocket_dim = PocketDimension(n_dim=4)
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
    def __init__(self, n_dim=3):
        self.active = set()
        self.n_neighbors = defaultdict(int)
        self.candidates = set()
        self.n_dim = n_dim

    def parse_input(self, s):
        lines = s.replace(ACTIVE, "1").replace(INACTIVE, "0").splitlines()
        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == "1":
                    cube = (x, y) + (0,) * (self.n_dim - 2)
                    self.activate(cube)

    def activate(self, cube):
        self.active.add((cube))
        self.candidates.discard((cube))
        for neighbor in self.get_neighbours(cube):
            self.n_neighbors[neighbor] += 1
            if self.n_neighbors[neighbor] == 3:
                self.candidates.add(neighbor)
            elif self.n_neighbors[neighbor] == 4:
                self.candidates.discard(neighbor)

    def deactivate(self, cube):
        self.active.discard((cube))
        for neighbor in self.get_neighbours(cube):
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
                self.deactivate(cube)
        for cube in old_candidates - old_active:
            self.activate(cube)

    def get_activated_count(self):
        return len(self.active)

    @staticmethod
    def get_neighbours(coords):
        n_dim = len(coords)
        for delta in product((-1, 0, 1), repeat=n_dim):
            if delta != (0,) * n_dim:
                yield tuple(coords[i] + delta[i] for i in range(n_dim))

    def __str__(self):
        coords_by_dim = zip(*self.active)
        ranges = [(min(coords), max(coords) + 1) for coords in coords_by_dim]
        lines = []
        for coords in zip(*[range(*r) for r in ranges[2:]]):
            lines.append(f"(X,X,{','.join([str(c) for c in coords])})")
            for x in range(*ranges[0]):
                lines.append(
                    "".join(
                        ACTIVE if (x, y, *coords) in self.active else INACTIVE
                        for y in range(*ranges[1])
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
