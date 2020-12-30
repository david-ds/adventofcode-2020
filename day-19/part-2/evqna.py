from tool.runners.python import SubmissionPy

import re

class EvqnaSubmission(SubmissionPy):
    def parse_rules(self, rules_str):
        rules = [None] * len(rules_str)
        for r in rules_str:
            id, rule = r.split(': ')
            if rule.startswith('"'):
                rules[int(id)] = rule[1]
            else:
                rules[int(id)] = [[int(r) for r in alt.split()] for alt in rule.split('|')]
        return rules

    def recursive_regex(self, id, rules):
        r = rules[id]
        if r == 'a' or r == 'b':
            return r

        subexprs = [''.join([self.recursive_regex(child_id, rules) for child_id in alt]) for alt in r]
        if len(subexprs) == 1:
            return subexprs[0]
        return '(?:' + '|'.join(subexprs) + ')' # non-capturing group
    
    def check_message(self, message, pattern):
        match = pattern.fullmatch(message)
        if not match:
            return False
        g42, g31 = match.groups()
        # Heuristically, rules 42 and 31 seem to only match strings of length 8
        # In that case, the matching group length is a multiple of the number of matches.
        # Quick sanity check to be sure.
        assert len(g42) % 8 == 0 and len(g31) % 8 == 0
        return len(g42) > len(g31)

    def run(self, s):
        rules, messages = s.split('\n\n')
        rules = rules.splitlines()
        messages = messages.splitlines()

        rules = self.parse_rules(rules)

        # The grammar described by
        #   0: 8 11
        #   8: 42 | 42 8
        #   11: 42 31 | 42 11 31
        # is not regular, but we can simulate it by using a custom matcher for the rule:
        #   42+ 31+
        # and checking that n_matches(31) < n_matches(42)
        r31 = self.recursive_regex(31, rules)
        r42 = self.recursive_regex(42, rules)
        pattern = re.compile(f'({r42}+)({r31}+)')
        return sum(1 for message in messages if self.check_message(message, pattern))
