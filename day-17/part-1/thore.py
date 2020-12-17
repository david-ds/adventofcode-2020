from collections import defaultdict
from itertools import product

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        n_dims = 3
        n_cycles = 6
        debug = False

        neighbors_delta = [
            x for x in product((-1, 0, 1), repeat=n_dims) if x != (0,) * n_dims
        ]

        active = {
            (x, y) + (0,) * (n_dims - 2)
            for x, line in enumerate(s.splitlines())
            for y, c in enumerate(line)
            if c == "#"
        }
        if debug:
            print("Before any cycle:\n")
            print(pformat_pocket_dim(active), "\n")

        for cycle in range(n_cycles):
            n_neighbors = defaultdict(int)
            for cube in active:
                for delta in neighbors_delta:
                    neighbor = tuple(sum(x) for x in zip(cube, delta))
                    n_neighbors[neighbor] += 1

            new_active = set()
            for cube, n in n_neighbors.items():
                if cube in active:
                    if n in [2, 3]:
                        new_active.add(cube)
                elif n == 3:
                    new_active.add(cube)
            active = new_active

            if debug:
                print(f"After {cycle+1} cycles:\n")
                print(pformat_pocket_dim(active), "\n")
        return len(active)


def pformat_pocket_dim(active):
    coords_by_dim = zip(*active)
    ranges = [(min(coords), max(coords) + 1) for coords in coords_by_dim]
    lines = []
    for coords in zip(*[range(*r) for r in ranges[2:]]):
        lines.append(f"(X,X,{','.join([str(c) for c in coords])})")
        for x in range(*ranges[0]):
            lines.append(
                "".join(
                    "#" if (x, y, *coords) in active else "." for y in range(*ranges[1])
                )
            )

        lines.append("")
    return "\n".join(lines)


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
