from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n"):
            first, second, char, password = (
                line.replace("-", " ").replace(":", " ").split()
            )

            first = int(first) - 1
            second = int(second) - 1

            if (password[first] != password[second]) and (
                (password[first] == char) or (password[second] == char)
            ):
                result += 1

        return result
