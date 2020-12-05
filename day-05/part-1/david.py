from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):
    def seat_id(self, code):
        b = [1 if x in {"B", "R"} else 0 for x in code]
        return sum(x * (1<<(9-n)) for n,x in enumerate(b))

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        return max(self.seat_id(code) for code in s.split("\n"))


