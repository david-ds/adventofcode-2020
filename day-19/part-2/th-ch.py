from importlib import import_module
import re

from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, s):

        # Parse input
        parsed = s.split("\n\n")
        serialized_rules = parsed[0].split("\n")
        parsed_rules = [None] * max(len(serialized_rules), 43)
        for parsed_rule in serialized_rules:
            rule_nb, rule = parsed_rule.split(": ")
            parsed_rules[int(rule_nb)] = rule

        messages = parsed[1].split("\n")

        # Re-use part 1 - first, compute non-recursive rules for 42 and 31
        part1 = import_module("day-19.part-1.th-ch").ThChSubmission()
        part1.rules = {}  # re-init rules in case it runs against multiple submissions
        rule42 = part1.parse_rule(42, parsed_rules)
        rule31 = part1.parse_rule(31, parsed_rules)

        # Override rules to create recursive ones
        part1.rules = {42: rule42, 31: rule31}
        part1.rules[8] = "({})+".format(rule42)  # [rule42]+
        rule11_regex = (
            # [rule42][rule42]…[rule31][rule31], etc - few iters are enough for message length
            "("
            + "|".join(
                "(({}){{{}}}({}){{{}}})".format(rule42, nb_iters, rule31, nb_iters)
                for nb_iters in range(1, 6)
            )
            + ")"
        )
        part1.rules[11] = rule11_regex

        # Compute rule 0 and compile the regex
        rule0 = part1.parse_rule(0, parsed_rules)
        regex = re.compile("^" + rule0 + "$")

        return sum(regex.match(message) is not None for message in messages)
