from functools import lru_cache
import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        rule_lines, messages = s.split("\n\n")
        rules = self.parse_rules(rule_lines)

        numbers = re.compile(r"(\d+)|\-")

        @lru_cache
        def resolve_rule(i):
            rule = rules[i]
            if '"' in rule:
                return rule.replace('"', "")
            elif "|" in rule:
                left, right = rule.split("|")
                left_sub = [resolve_rule(j) for j in numbers.findall(left)]
                right_sub = [resolve_rule(j) for j in numbers.findall(right)]
                return f"(({''.join(left_sub)})|({''.join(right_sub)}))"
            else:
                subrules = [resolve_rule(j) for j in numbers.findall(rule)]
                return "".join(subrules)

        prog = re.compile(resolve_rule("0"))
        return sum(prog.fullmatch(line) is not None for line in messages.splitlines())

    @staticmethod
    def parse_rules(s):
        rules = {}
        for rule in s.splitlines():
            i, r = rule.split(": ")
            rules[i] = r
        return rules


def test_day19_part1():
    assert (
        ThoreSubmission().run(
            """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
        )
        == 2
    )
