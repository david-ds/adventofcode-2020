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
            children = set(x.strip().split(" ", maxsplit=1)[1] for x in children_with_count)
            tree[parent.strip()] = set(children)
        return tree

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        tree = self.parse(s)
        
        # reversed_tree: stores the set of bags containing a given bag
        reversed_tree = defaultdict(set)
        for parent, children in tree.items():
            for child in children:
                reversed_tree[child].add(parent)

        # count the number of items reachable from "shiny gold" in the reversed tree
        result = set()
        q = queue.Queue()
        q.put("shiny gold")

        while not q.empty():
            bag = q.get()
            result.add(bag)
            for next_bag in reversed_tree[bag]:
                if next_bag not in result:
                    q.put(next_bag)

        return len(result)
