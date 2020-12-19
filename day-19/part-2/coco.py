from tool.runners.python import SubmissionPy
import re
from collections import namedtuple

regex_match_leaf = re.compile(r'\"[a-z]\"')


class CocoSubmission(SubmissionPy):
    """
    Manual solution (no regex generation for more fun)
    """

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # PARSING
        rules, inputs = s.strip().split("\n\n")
        rules = rules.split("\n")
        rules = [r.split(": ") for r in rules]
        rules = [(int(id), r) for (id, r) in rules]
        # print(rules)
        rules = {id: Rule(r) for (id, r) in rules}
        
        # Modified by puzzle input
        rules[8] = Rule("42 | 42 8")
        rules[11] = Rule("42 31 | 42 11 31")

        inputs = inputs.split("\n")

        # this is an item of our pile
        Item = namedtuple("Item", ["start_id", "rule_ids"])

        num_matches = 0

        # DEPTH-first search (non-recursive for even more fun)
        for message in inputs:
            pile = [Item(start_id=0, rule_ids=[0])]  
            match = False
            while pile and not match:
                item = pile.pop()
                if len(item.rule_ids) + item.start_id > len(message):
                    # rules are too long for message.
                    continue
                if item.start_id >= len(message):
                    match = True
                elif len(item.rule_ids) == 0:
                    continue  # no match for this rule
                else:
                    first_rule: Rule = rules[item.rule_ids[0]]
                    rest_rules = item.rule_ids[1:]
                    if first_rule.is_leaf and message[item.start_id] == first_rule.value:
                        pile.append(Item(item.start_id + 1, rest_rules))
                    elif first_rule.is_leaf:
                        continue  # no match
                    else:
                        for g in first_rule.groups:
                            pile.append(Item(item.start_id, g + rest_rules))
            if match:
                num_matches += 1
        return num_matches


class Rule:
    """
    Parse rule
    """
    def __init__(self, input) -> None:
        if regex_match_leaf.match(input):
            self.is_leaf = True
            self.value = input[1]
        else:
            self.is_leaf = False
            groups = input.split(" | ")
            groups = [g.split() for g in groups]
            for i in range(len(groups)):
                groups[i] = [int(k) for k in groups[i]]
            self.groups = groups

    def __repr__(self) -> str:
        if self.is_leaf:
            return "Leaf :" + str(self.value)
        else:
            return "Node :" + str(self.groups)

def test_coco():
    assert CocoSubmission().run("""42: 9 14 | 10 1
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
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""") == 12
