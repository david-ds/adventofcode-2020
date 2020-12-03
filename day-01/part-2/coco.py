from tool.runners.python import SubmissionPy

from collections import defaultdict

class COCOSubmission(SubmissionPy):

    def run(self, s):
        numbers = [int(n.strip()) for n in s.split("\n")]
        for i in range(len(numbers)):
            ni = numbers[i]
            if ni > 2020:
                continue
            for j in range(i+1, len(numbers)):
                nj  = numbers[j]
                if ni + nj  > 2020:
                    continue
                for k in range(j+1, len(numbers)):
                    nk = numbers[k]
                    if ni + nj + nk == 2020:
                        return ni * nj * nk
