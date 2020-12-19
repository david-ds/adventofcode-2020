from tool.runners.python import SubmissionPy

import re


class ThChSubmission(SubmissionPy):
    rules = {}

    def parse_rule(self, rule_nb, parsed_rules):
        if rule_nb in self.rules:
            return self.rules[rule_nb]

        parsed_rule = parsed_rules[rule_nb]
        if parsed_rule[0] == '"':
            self.rules[rule_nb] = parsed_rule[1:-1]
            return self.rules[rule_nb]

        rules_or = []
        for group in parsed_rule.split(" | "):
            rule_for_group = ["("]
            for subrule_nb in group.split(" "):
                subrule_nb = int(subrule_nb)

                subrule = self.parse_rule(subrule_nb, parsed_rules)
                rule_for_group.append(subrule)

            rule_for_group.append(")")
            rules_or.append("".join(rule_for_group))

        self.rules[rule_nb] = "(" + "|".join(rules_or) + ")"
        return self.rules[rule_nb]

    def run(self, s):
        self.rules = {}  # re-init rules in case it runs against multiple submissions

        # Parse input
        parsed = s.split("\n\n")
        serialized_rules = parsed[0].split("\n")
        messages = parsed[1].split("\n")
        parsed_rules = [None] * len(serialized_rules)
        for parsed_rule in serialized_rules:
            rule_nb, rule = parsed_rule.split(": ")
            parsed_rules[int(rule_nb)] = rule

        # Rule 0 as regex
        rule0 = self.parse_rule(0, parsed_rules)
        regex = re.compile("^" + rule0 + "$")

        return sum(regex.match(message) is not None for message in messages)
