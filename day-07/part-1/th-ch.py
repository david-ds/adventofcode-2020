from collections import deque

from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):
        # struct: { bag_color: { contained: {color: number}, contains: {color: number} }
        rules = {}
        own_color = "shiny gold"
        containing_own_color_by_bag_color = {}

        for rule in s.split("\n"):
            bag_color, subrules = rule.split(" bags contain ")
            subrules = subrules[:-1]  # remove final dot

            if bag_color not in rules:
                rules[bag_color] = {"contained": {}, "contains": {}}

            if subrules != "no other bags":
                for subrule in subrules.split(", "):
                    number = subrule.split(" ")[0]
                    color = subrule.replace(number + " ", "").split(" bag")[0]
                    rules[bag_color]["contains"][color] = number
                    if color not in rules:
                        rules[color] = {"contained": {}, "contains": {}}
                    rules[color]["contained"][bag_color] = number

        seen = set()
        to_visit = deque([own_color])
        while to_visit:
            color = to_visit.popleft()
            contained = rules[color]["contained"].keys()

            if color not in seen:
                seen.add(color)
                to_visit.extend(contained)

        return len(seen) - 1
