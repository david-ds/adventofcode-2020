from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        N_TURNS = 2020
        
        start = [int(c) for c in s.split(",")]
        last_seen = {n: i + 1 for i, n in enumerate(start)}
        spoken = start[-1]
        for turn in range(len(start), N_TURNS):
            last_seen[spoken], spoken = turn, turn - last_seen.get(spoken, turn)
        return spoken


def test_day15_part1():
    assert ThoreSubmission().run("0,3,6") == 436
    assert ThoreSubmission().run("1,3,2") == 1
    assert ThoreSubmission().run("2,1,3") == 10
    assert ThoreSubmission().run("1,2,3") == 27
    assert ThoreSubmission().run("2,3,1") == 78
    assert ThoreSubmission().run("3,2,1") == 438
    assert ThoreSubmission().run("3,1,2") == 1836