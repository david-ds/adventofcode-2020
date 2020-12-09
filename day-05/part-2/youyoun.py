from tool.runners.python import SubmissionPy
import heapq


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        seats = s.strip().replace('F', '0').replace('B', '1').replace('R', '1').replace('L', '0').splitlines()
        ids = []
        for s in seats:
            ids.append(int(s, 2))
        ids = sorted(ids)
        return [ids[x] for x in range(len(ids)-1) if ids[x+1] - ids[x] == 2][0] + 1
