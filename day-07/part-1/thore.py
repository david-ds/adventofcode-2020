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

        graph = self.parse_to_containers_graph(s)
        return len(self.get_reachable_nodes(graph, TARGET))

    @staticmethod
    def parse_to_containers_graph(s):
        """Parse the input to create a graph with colors as nodes and edges
        from contents to containers"""

        possible_containers = defaultdict(set)
        prog = re.compile("(\d+) ([\w ]+) bags?")

        for line in s.split("\n"):
            container_color, contents = line.split(" bags contain ")
            contents = contents.split(", ")
            for content in contents:
                match = prog.match(content)
                if not match:
                    continue
                n, color = match.groups()
                possible_containers[color].add(container_color)

        return possible_containers

    @staticmethod
    def get_reachable_nodes(adj_lists, start):
        visited = set()
        stack = [start]
        while len(stack):
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            stack.extend(list(adj_lists[node]))

        visited.remove(start)
        return visited