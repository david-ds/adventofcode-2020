from tool.runners.python import SubmissionPy

from collections import defaultdict

target_bag = 'shiny gold'

class EvqnaSubmission(SubmissionPy):

    def parse_rule(self, rule):
        bag_type, _, contains = rule.partition(' bags contain ')
        if contains.startswith('no'):
            return bag_type, []
        C = []
        for contained_str in contains.split(','):
            n, bag_1, bag_2, _ = contained_str.split()
            C.append((int(n), bag_1 + ' ' + bag_2))
        return bag_type, C

    def build_inverted_index(self, rules):
        '''Build an inverted index mapping each bag type
        to the bags that *directly* contain it.'''
        index = defaultdict(set)  ## {bag_type: {parent_bags}}
        for parent_bag, contains in rules:
            for n, child_bag in contains:
                index[child_bag].add(parent_bag)
        return index
    
    def reachable_rec(self, graph, node):
        children = graph[node]
        reachable = {node}
        for c in children:
            reachable |= self.reachable_rec(graph, c)
        return reachable

    def count_reachable_bags(self, index, start):
        return len(self.reachable_rec(index, start)) - 1

    def run(self, s):
        rules = [self.parse_rule(r) for r in s.splitlines()]
        index = self.build_inverted_index(rules)
        return self.count_reachable_bags(index, target_bag)
