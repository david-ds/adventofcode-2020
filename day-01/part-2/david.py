from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):

    def run(self, s):
        # :param s: input in string format
        # :return: solution flag
        # Your code goes here
        entries = [int(x) for x in s.split("\n")]
        assert(all(x >= 0 for x in entries))

        for idx_i, i in enumerate(entries):
            for idx_j, j in enumerate(entries[idx_i+1:]):
                if i+j > 2020:
                    # no need to find the 3rd item
                    continue
                for k in entries[idx_j+1:]:
                    if i+j+k == 2020:
                        return i*j*k
