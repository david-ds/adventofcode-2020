from tool.runners.python import SubmissionPy

import string


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        groups = s.split("\n\n")
        result = 0

        for group in groups:
            common = set(string.ascii_lowercase)
            for person in group.split():
                common.intersection_update(person)
            result += len(common)

        return result
