from tool.runners.python import SubmissionPy

import networkx as nx
import re


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        graph = nx.DiGraph()
        pattern = re.compile(r"\d+ ([\w ]+) bags?")

        for line in s.split("\n"):
            container, containees = line.split(" bags contain ")
            graph.add_node(container)
            for containee in pattern.findall(containees):
                graph.add_edge(containee, container)

        return len(set(nx.dfs_postorder_nodes(graph, "shiny gold"))) - 1
