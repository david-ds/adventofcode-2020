from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        N_TURNS = 30000000

        start = [int(c) for c in s.split(",")]
        last_seen = {n: i + 1 for i, n in enumerate(start)}
        spoken = start[-1]
        for turn in range(len(start), N_TURNS):
            last_seen[spoken], spoken = turn, turn - last_seen.get(spoken, turn)
        return spoken
