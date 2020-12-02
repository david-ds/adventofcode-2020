from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def parse_line(self, line):
        rule, password = line.split(": ")
        count, letter = rule.split(" ")
        lower_bound, upper_bound = map(int, count.split("-"))

        return lower_bound, upper_bound, letter, password


    def is_valid(self, line):
        lower_bound, upper_bound, letter, password = self.parse_line(line)
        return lower_bound <= password.count(letter) <= upper_bound


    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        return sum(1 for line in s.split("\n") if self.is_valid(line))
