from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here

        numbers = [int(m) for m in s.strip().split("\n")]
        candidates = set(numbers[:26])
        for i in range(25, len(numbers)):
            number = numbers[i]
            is_sum = False
            for p in candidates:
                if number - p in candidates and number != 2 * p:
                    is_sum = True
                    break
            candidates.add(number)
            candidates.remove(numbers[i-25])
            if not is_sum:
                return number
