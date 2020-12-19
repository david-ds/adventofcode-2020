from typing import Dict

try:  # Stolen not to make everyone install regex, thanks thore :3 (all code with 'regex' usage is mine tho)
    import regex as re
    RECURSIVE_REGEX = True
except ModuleNotFoundError:
    import re
    RECURSIVE_REGEX = False
    RECURSIVE_MAX = 6

from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s: str) -> int:
        s_rules, s_messages = s.strip().split('\n\n')
        rules: Dict[str, str] = {}

        for line in s_rules.splitlines():
            if line == '8: 42':  # 42 | 42 8
                line = '8: 42+'
            if line == '11: 42 31':  # 11: 42 31 | 42 11 31 -> 42*n 31*n n > 0... -> (?P<lol> 42 (?P>lol)? 31)
                line = '11: 42_31'
            number, rule = line.split(': ')
            rules[number] = rule.strip('"')

        # for k, v in sorted(rules.items(), key=lambda it: int(it[0])):
        #     print(f'{k.rjust(4)}: {v}')

        self.fill_rule(rules, rules["0"], "0")

        # print('\nRULE:', f'^{rules["0"]}$')

        rule_0 = re.compile(f'^{rules["0"]}$')
        res = 0
        for message in s_messages.splitlines():
            if rule_0.match(message):
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

        if rule.endswith('+'):
            rules[number] = f'({self.fill_rule(rules, rules[rule.rstrip("+")], number)})+'
            # print(number, '<-', rules[number])
            return rules[number]

        if '_' in rule:
            # (?P<lol>a(?P>lol)?b)
            p1, p2 = rule.split("_")

            if RECURSIVE_REGEX:
                rules[number] = f'(?P<lol>{self.fill_rule(rules, p1, "-1")}(?P>lol)?{self.fill_rule(rules, p2, "-1")})'
            else:
                p1_r = self.fill_rule(rules, p1, '-1')
                p2_r = self.fill_rule(rules, p2, "-1")
                rules[number] = f'({"|".join(f"({p1_r}{{{i + 1}}}{p2_r}{{{i + 1}}})" for i in range(RECURSIVE_MAX))})'

            # print(number, '<-', rules[number])
            return rules[number]

        rules[number] = self.fill_rule(rules, rules[rule], number)
        # print(number, '<-', rules[number])
        return rules[number]
