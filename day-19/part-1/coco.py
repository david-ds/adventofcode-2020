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
        rules = {id: Rule(r) for (id, r) in rules}
        
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


def test_coco():
    assert CocoSubmission().run("""0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""") == 2
