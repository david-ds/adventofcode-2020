from collections import defaultdict
import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        TARGET = "shiny gold"

        graph = self.parse_to_contents_graph(s)
        return self.number_of_bags_required(graph, TARGET)

    @staticmethod
    def parse_to_contents_graph(s):
        """Parse the input to create a graph with colors as nodes and edges
        from containers to content, weighted by the number of bags"""

        contents_graph = defaultdict(set)
        prog = re.compile("(\d+) ([\w ]+) bags?")

        for line in s.split("\n"):
            container_color, contents = line.split(" bags contain ")
            contents = contents.split(", ")
            for content in contents:
                match = prog.match(content)
                if not match:
                    continue
                n, color = match.groups()
                contents_graph[container_color].add((color, int(n)))

        return contents_graph

    @classmethod
    def number_of_bags_required(cls, adj_lists, color):
        if color not in adj_lists:
            return 0

        return sum(
            n * (1 + cls.number_of_bags_required(adj_lists, c))
            for c, n in adj_lists[color]
        )