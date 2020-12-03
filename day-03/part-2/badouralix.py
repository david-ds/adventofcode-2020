from tool.runners.python import SubmissionPy

from functools import reduce


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        positions = [0 for slope in slopes]
        trees = [0 for slope in slopes]

        for num, line in enumerate(s.split()):
            for idx, slope in enumerate(slopes):
                if num % slope[1] == 0:
                    if line[positions[idx]] == "#":
                        trees[idx] += 1
                    positions[idx] = (positions[idx] + slope[0]) % len(line)

        return reduce(lambda acc, tree: acc * tree, trees, 1)
