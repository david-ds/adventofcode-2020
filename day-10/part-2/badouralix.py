from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        adapters = set(map(int, s.split()))
        adapters.add(0)

        arrangements = [0] * (1 + max(adapters) + 3)
        arrangements[-1] = 1

        for i in range(len(arrangements) - 3, -1, -1):
            if i in adapters:
                arrangements[i] = (
                    arrangements[i + 1] + arrangements[i + 2] + arrangements[i + 3]
                )

        return arrangements[0]
