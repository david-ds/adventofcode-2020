from tool.runners.python import SubmissionPy

import re

hcl_matcher = re.compile('#[0-9a-f]{6}')
pid_matcher = re.compile('[0-9]{9}')

class EvqnaSubmission(SubmissionPy):

    def integer_in_range(self, field, lo, hi):
        n = int(field)
        return lo <= n and n <= hi

    def validate_fields(self, passport):
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        fields = {}
        for field in passport:
            k, v = field.split(':')
            fields[k] = v
        if not required_fields.issubset(fields.keys()):
            return False

        if not self.integer_in_range(fields['byr'], 1920, 2002):
            return False
        if not self.integer_in_range(fields['iyr'], 2010, 2020):
            return False
        if not self.integer_in_range(fields['eyr'], 2020, 2030):
            return False

        hgt = fields['hgt']
        if hgt.endswith('cm'):
            if not self.integer_in_range(hgt[:-2], 150, 193):
                return False
        elif hgt.endswith('in'):
            if not self.integer_in_range(hgt[:-2], 59, 76):
                return False
        else:
            return False

        if not hcl_matcher.fullmatch(fields['hcl']):
            return False
        if not fields['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False
        if not pid_matcher.fullmatch(fields['pid']):
            return False

        return True

    def run(self, s):
        passports = [p.split() for p in s.split('\n\n')]
        return sum(1 for p in passports if self.validate_fields(p))
