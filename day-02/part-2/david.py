from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def parse_line(self, line):
        rule, password = line.split(": ")
        positions, letter = rule.split(" ")
        pos1, pos2 = positions.split("-")
        pos1, pos2 = int(pos1)-1, int(pos2)-1

        return pos1, pos2, letter, password

    def is_valid(self, line):
        pos1, pos2, letter, password = self.parse_line(line)
        return (password[pos1] == letter) ^ (password[pos2] == letter) 

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        return sum(1 for line in s.split("\n") if self.is_valid(line))
