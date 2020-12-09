from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        seats = s.strip().replace('F', '0').replace('B', '1').replace('R', '1').replace('L', '0').splitlines()
        max_ = 0
        for s in seats:
            id_ = int(s, 2)
            if id_ > max_:
                max_ = id_
        return max_
