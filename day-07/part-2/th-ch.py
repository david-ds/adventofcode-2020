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
                    rules[bag_color]["contains"][color] = int(number)
                    if color not in rules:
                        rules[color] = {"contained": {}, "contains": {}}
                    rules[color]["contained"][bag_color] = int(number)

        nb_by_color = {}
        roots = set(color for color, edges in rules.items() if not edges["contained"])
        to_visit = deque(roots)
        while to_visit:
            color = to_visit.popleft()
            has_all_children = True
            for child_color, number in rules[color]["contains"].items():
                if child_color not in nb_by_color:
                    to_visit.append(child_color)
                    has_all_children = False

            if has_all_children:
                nb_by_color[color] = sum(
                    number + number * nb_by_color[child_color]
                    for child_color, number in rules[color]["contains"].items()
                )
            else:
                to_visit.append(color)

        return nb_by_color[own_color]
