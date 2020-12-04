from tool.runners.python import SubmissionPy
import re

class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        required_fields = ["byr", "iyr", "eyr","hgt","hcl","ecl","pid"]

        lines = s.strip().split("\n\n")
        n_valid = 0
        for l in lines:
            field_value = l.replace("\n", " ").split()
            fields = set([f.split(':')[0] for f in field_value])
            if all(r in fields for r in required_fields):
                n_valid += 1
        return n_valid
