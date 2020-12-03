from math import prod

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        dx, dy = 3, 1
        world = s.split("\n")

        return self.count_trees(world, dx, dy)

    def count_trees(self, world, dx, dy):
        h, w = len(world), len(world[0])

        x = 0
        n_trees = 0
        for y in range(0, h, dy):
            n_trees += int(world[y][x % w] == "#")
            x += dx

        return n_trees