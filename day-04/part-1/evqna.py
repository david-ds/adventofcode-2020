from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def validate_fields(self, passport):
        required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        fields = {e[:3] for e in passport}
        return required_fields.issubset(fields)

    def run(self, s):
        passports = [p.split() for p in s.split('\n\n')]
        return sum(1 for p in passports if self.validate_fields(p))
