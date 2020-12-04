from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n\n"):
            keys = {keyvalue.split(":")[0] for keyvalue in line.split()}
            if {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} <= keys:
                result += 1

        return result
