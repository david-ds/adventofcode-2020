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

    def build_index(self, rules):
        '''Build an index mapping each bag type
        to the bags that it *directly* contains.'''
        index = defaultdict(set)  ## {bag_type: {(n, contained_bag)}}
        for parent_bag, contains in rules:
            for n, child_bag in contains:
                index[parent_bag].add((n, child_bag))
        return index

    def count_bags_rec(self, index, start):
        bags = 1
        for n, c in index[start]:
            bags += n * self.count_bags_rec(index, c)
        return bags

    def run(self, s):
        rules = [self.parse_rule(r) for r in s.splitlines()]
        index = self.build_index(rules)
        return self.count_bags_rec(index, target_bag) - 1
