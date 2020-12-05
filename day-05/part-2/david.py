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
        seat_ids = {self.seat_id(code) for code in s.split("\n")}
        for i in range(1,(1<<10)-1):
            if i-1 in seat_ids and i+1 in seat_ids and i not in seat_ids:
                return i
