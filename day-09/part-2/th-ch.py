from importlib import import_module

from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        nbs = s.split("\n")

        part1 = import_module("day-09.part-1.th-ch")
        invalid_nb = part1.ThChSubmission().run(s)

        combination = []
        for nb in nbs:
            combination.append(int(nb))
            while sum(combination) > invalid_nb:
                combination.pop(0)

            if sum(combination) == invalid_nb:
                return max(combination) + min(combination)

        raise Exception("Not found!")
