from tool.runners.python import SubmissionPy

MAX_ADAPTER = 256


class BebertSubmission(SubmissionPy):

    def run(self, s):
        adapters = [0] * MAX_ADAPTER
        adapters[0] = 1
        max_adapters = 0
        for line in s.strip().splitlines():
            adapter = int(line)
            adapters[adapter] = 1
            if adapter > max_adapters:
                max_adapters = adapter
        streaks = [0] * 8
        streak = 0
        for i in range(max_adapters + 2):
            if adapters[i]:
                streak += 1
            else:
                streaks[streak] += 1
                streak = 0

        multipliers = [0, 1, 1, 2, 4, 7, 12]  # compté à la main lol

        res = 1
        for i in range(2, 8):
            for n in range(streaks[i]):
                res *= multipliers[i]

        return res
