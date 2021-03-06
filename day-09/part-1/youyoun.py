from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        w_length = 25
        ints = [int(x) for x in s.splitlines()]
        i = w_length
        while is_valid(ints, w_length, i):
            i += 1
        return ints[i]


def is_valid(sequence, window, i):
    subseq = set(sequence[i - window:i])
    for e in subseq:
        if sequence[i] - e in subseq and sequence[i] != e:
            return True
    return False
