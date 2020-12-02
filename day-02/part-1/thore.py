import re

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        pattern = r"(\d+)-(\d+) ([a-z]): (\w+)"
        prog = re.compile(pattern)

        n_valid_passwords = 0
        for line in s.split("\n"):
            m = prog.match(line)
            if not m:
                pass
            mini, maxi, letter, password = m.groups()
            n_occurences = password.count(letter)
            if n_occurences >= int(mini) and n_occurences <= int(maxi):
                n_valid_passwords += 1

        return n_valid_passwords