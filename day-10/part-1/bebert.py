from tool.runners.python import SubmissionPy

MAX_ADAPTER = 256


class BebertSubmission(SubmissionPy):

    def run(self, s):
        adapters = [0] * MAX_ADAPTER
        max_adapters = 0
        for line in s.strip().splitlines():
            adapter = int(line)
            adapters[adapter] = 1
            if adapter > max_adapters:
                max_adapters = adapter
        counts = [0] * 5
        diff = 0
        for i in range(1, max_adapters + 1):
            diff += 1
            if adapters[i]:
                counts[diff] += 1
                diff = 0
        counts[3] += 1
        return counts[1] * counts[3]
