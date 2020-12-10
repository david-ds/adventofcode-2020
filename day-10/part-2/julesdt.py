from tool.runners.python import SubmissionPy
import collections


class JulesdtSubmission(SubmissionPy):



    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        adapters = []
        for line in s.split('\n'):
            adapters.append(int(line))
        adapters = sorted(adapters)
        values = collections.defaultdict(int)
        values[0] = 1
        for adapter in adapters:
            values[adapter] = sum([values[x] for x in range(adapter-3, adapter)])
        return values[adapters[-1]]
