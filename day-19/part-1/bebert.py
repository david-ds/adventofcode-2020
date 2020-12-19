import re
from typing import Dict

from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s: str) -> int:
        s_rules, s_messages = s.strip().split('\n\n')
        rules: Dict[str, str] = {}

        for line in s_rules.splitlines():
            number, rule = line.split(': ')
            rules[number] = rule.strip('"')

        # for k, v in sorted(rules.items(), key=lambda it: int(it[0])):
        #     print(f'{k.rjust(4)}: {v}')
        self.fill_rule(rules, rules["0"], "0")

        # print('RULE:', f'^{rules["0"]}$')

        rule_0 = re.compile(f'^{rules["0"]}$')
        res = 0
        for message in s_messages.splitlines():
            if rule_0.search(message):
                res += 1

        return res

    def fill_rule(self, rules: Dict[str, str], rule: str, number: str) -> str:
        # print(f'fill_rule: "{rule}" [{number}]')
        if rule[0] == "a" or rule[0] == "b" or rule[0] == "(":
            return rule

        if " | " in rule:
            rules[number] = f'({"|".join(self.fill_rule(rules, part, "-1") for part in rule.split(" | "))})'
            # print(number, '<-', rules[number])
            return rules[number]

        if " " in rule:
            rules[number] = "".join(self.fill_rule(rules, rules[c], c) for c in rule.split(" "))
            # print(number, '<-', rules[number])
            return rules[number]

        rules[number] = self.fill_rule(rules, rules[rule], number)
        # print(number, '<-', rules[number])
        return rules[number]
