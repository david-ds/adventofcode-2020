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
                    n = r[0]
                    child = (r[1], r[2])
                    contains[container].append((n, child))
        
        # build parent
        parents = defaultdict(list)
        for head, children in contains.items():
            for n, child in children:
                parents[child].append(head)

        possible_parents = set()
        start = [("shiny", "gold")]

        while start:
            current = start.pop()
            ps = parents[current]
            possible_parents = possible_parents.union(set(ps))
            start.extend(ps)

        return len(possible_parents)
