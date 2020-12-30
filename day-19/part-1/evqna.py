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
    
    def regex(self, id, rules):
        r = rules[id]
        if r == 'a' or r == 'b':
            return r

        subexprs = [''.join([self.regex(child_id, rules) for child_id in alt]) for alt in r]
        if len(subexprs) == 1:
            return subexprs[0]
        return '(' + '|'.join(subexprs) + ')'

    def run(self, s):
        rules, messages = s.split('\n\n')
        rules = rules.splitlines()
        messages = messages.splitlines()

        rules = self.parse_rules(rules)
        regex_str = self.regex(0, rules)
        pattern = re.compile(regex_str)
        return sum(1 for message in messages if pattern.fullmatch(message))
