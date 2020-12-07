import pprint
import collections
from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def can_hold_gold_bag(self, color):
        colors_to_check = set([color])
        visited = set()
        while len(colors_to_check) > 0:
            color = colors_to_check.pop()
            visited.add(color)
            for sub_color in self.rules[color].keys():
                if "shiny gold" == sub_color:
                    return True
                if sub_color not in visited:
                    colors_to_check.add(sub_color)
        return False
        

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.rules = {}
        for line in s.split('\n'):
            bag_color, contains = line.split(" bags contain ")
            for contain in contains.split(', '):
                if contain == "no other bags.":
                    self.rules[bag_color] = {}
                    continue
                splitted = contain.split(' ')
                count = splitted[0]
                color = " ".join(splitted[1:3])
                if bag_color not in self.rules:
                    self.rules[bag_color] = {}
                self.rules[bag_color][color] = count
        counter = 0
        for color in self.rules.keys():
            if color == "shiny gold":
                continue
            if self.can_hold_gold_bag(color):
                counter += 1
        return counter
