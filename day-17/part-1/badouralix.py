from tool.runners.python import SubmissionPy

from collections import defaultdict


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        active_positions = set()
        active_neighbors = defaultdict(int)

        for i, line in enumerate(s.split("\n")):
            for j, cube in enumerate(line):
                if cube == "#":
                    position = (i, j, 0)

                    active_positions.add(position)
                    active_neighbors[
                        position
                    ] += 0  # Special hack so that position is in active_neighbors.keys() and iterating over all known positions becomes much easier
                    for neighbor in self.neighbors(position):
                        active_neighbors[neighbor] += 1

        for _ in range(6):
            last_positions = active_positions.copy()
            last_neighbors = active_neighbors.copy()

            for position in last_neighbors.keys():
                if position in last_positions and not (
                    2 <= last_neighbors[position] <= 3
                ):
                    active_positions.remove(position)
                    for neighbor in self.neighbors(position):
                        active_neighbors[neighbor] -= 1
                elif position not in last_positions and last_neighbors[position] == 3:
                    active_positions.add(position)
                    for neighbor in self.neighbors(position):
                        active_neighbors[neighbor] += 1

        return len(active_positions)

    @staticmethod
    def neighbors(position):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    if not (i == 0 and j == 0 and k == 0):
                        yield (position[0] + i, position[1] + j, position[2] + k)
