from tool.runners.python import SubmissionPy

from collections import defaultdict
import queue

class DavidSubmission(SubmissionPy):
    def parse(self, s):
         # tree: stores the set of bags that a bag must contain
        tree = defaultdict(set)
        for rule in s.split("\n"):
            parent, children_str = rule.split(" bags contain ")
            if "no other bags" in children_str:
                tree[parent] = set()
                continue
            children_with_count = children_str.replace(".", "").replace("bags", "").replace("bag", "").split(", ")
            for child_with_count in children_with_count:
                count, child = child_with_count.strip().split(" ", maxsplit=1)
                tree[parent.strip()].add((int(count), child))
        return tree

    def rec(self, bags, root):
        if len(bags[root]) == 0:
            return 0

        result = 0
        for count, bag in bags[root]:
            result += count + count*self.rec(bags, bag)
        return result

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        tree = self.parse(s)

        return self.rec(tree, "shiny gold")

        
