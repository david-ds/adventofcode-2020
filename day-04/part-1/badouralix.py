from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n\n"):
            keyvalues = set(line.replace("\n", " ").replace(":", " ").split())
            if {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} <= keyvalues:
                result += 1

        return result
