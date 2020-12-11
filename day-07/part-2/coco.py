from tool.runners.python import SubmissionPy
from collections import defaultdict

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        rules = s.strip().split("\n")
        contains = dict()
        ###
        # PARSING
        ###
        for rule in rules:
            r2 = rule.split(" ")
            container = (r2[0], r2[1])
            contains[container] = []
            if r2[4] != "no":
                rest = " ".join(r2[4:])
                rest = rest.split(",") # each children
                rest = [r.split() for r in rest]
                for r in rest:
                    n = int(r[0])
                    child = (r[1], r[2])
                    contains[container].append((n, child))

        # no recursion
        n_bags = 0
        start = [(1, ("shiny", "gold"))]
        while start:
            k, current = start.pop()
            children = contains[current]
            for (n, child) in children:
                start.append((n*k, child))
                n_bags += (n*k)

        return n_bags
