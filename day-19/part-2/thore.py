from functools import lru_cache

try:
    import regex as re

    RECURSIVE_REGEX = True
except ModuleNotFoundError:
    import re

    RECURSIVE_REGEX = False
    MAX_RECURSION_DEPTH = 6

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        rule_lines, messages = s.split("\n\n")
        rules = self.parse_rules(rule_lines)

        numbers = re.compile(r"\d+")

        @lru_cache
        def resolve_rule(i):
            rule = rules[i]
            if i == "8":  # replaced by 42 | 42 8
                return f"({resolve_rule('42')})+"
            elif i == "11":  # replaced by 42 31 | 42 11 31
                l, r = resolve_rule("42"), resolve_rule("31")
                if RECURSIVE_REGEX:
                    return f"(?P<x>{l}(?&x)?{r})"
                else:
                    return f"({'|'.join(fr'({l}{{{i}}}{r}{{{i}}})' for i in range(1, MAX_RECURSION_DEPTH+1))})"
            elif '"' in rule:
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


def test_day19_part2():
    assert (
        ThoreSubmission().run(
            """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
        )
        == 12
    )
