import pprint
import collections
from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def count_number_of_bag_of_color(self, color):
        counter = 0
        if color in self.results:
            return self.results[color]
        for sub_color in self.rules[color].keys():
            counter += self.rules[color][sub_color] * (1 + self.count_number_of_bag_of_color(sub_color))
        self.results[color] = counter
        return counter
        

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.results = {}
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
                self.rules[bag_color][color] = int(count)
        return self.count_number_of_bag_of_color("shiny gold")
