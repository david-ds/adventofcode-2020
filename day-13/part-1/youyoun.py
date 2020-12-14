from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        first_start = int(s[0])
        bus_ids = list(map(int, s[1].replace('x,', '').split(',')))
        min_ = float('inf')
        min_id = None
        for id_ in bus_ids:
            wait_time = id_ - first_start % id_
            if wait_time <= min_:
                min_ = wait_time
                min_id = id_
        return min_id * min_
