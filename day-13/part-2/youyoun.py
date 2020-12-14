from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        bus_ids = s[1].split(',')
        equations = []
        n = 1
        for i, id_ in enumerate(bus_ids):
            if id_ != 'x':
                id_ = int(id_)
                n *= id_
                equations.append(((id_ - i) % id_, id_))
        start = 0
        for remn, ni in equations:
            ni_hat = n // ni
            vi = ni_hat % ni
            for i in range(ni - 3):
                vi = (vi * ni_hat) % ni
            start += ni_hat * vi * remn
        return start % n
