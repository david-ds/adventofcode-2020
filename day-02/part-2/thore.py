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
            x, y, letter, password = m.groups()
            letter_at_x = password[int(x) - 1] == letter
            letter_at_y = password[int(y) - 1] == letter
            if int(letter_at_x) + int(letter_at_y) == 1:
                n_valid_passwords += 1

        return n_valid_passwords