from tool.runners.python import SubmissionPy

from typing import Dict

import networkx as nx
import re


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        graph = nx.DiGraph()
        pattern = re.compile(r"(\d+) ([\w ]+) bags?")

        for line in s.split("\n"):
            container, containees = line.split(" bags contain ")
            graph.add_node(container)
            for count, containee in pattern.findall(containees):
                graph.add_edge(container, containee, count=int(count))

        return self.rec_count_containers(graph, "shiny gold", dict())

    def rec_count_containers(
        self, graph: nx.DiGraph, container: str, cache: Dict[str, int]
    ) -> int:
        if container in cache:
            return cache[container]

        count = 0

        for _, containee, data in graph.out_edges(container, data=True):
            count += data["count"] * (
                1 + self.rec_count_containers(graph, containee, cache)
            )

        cache[container] = count

        return count
