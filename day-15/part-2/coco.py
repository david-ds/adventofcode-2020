from tool.runners.python import SubmissionPy
from tqdm import tqdm

class CocoSubmission(SubmissionPy):
    def run(self, s, N=30000000):
        """
        :param s: input in string format
        :return: solution flag
        """
        numbers = [int(n) for n in s.strip().split(",")]

        last_spoken_at = [-1]*N
        for i, n in enumerate(numbers[:-1]):
            last_spoken_at[n] = i+1
        # last_spoken_at = {n: i+1 for i, n in enumerate(numbers[:-1])}
        last_number = numbers[-1]

        for k in (range(len(numbers)+1, N+1)):
            # if last_number in last_spoken_at:
            if last_spoken_at[last_number] != -1:
                speak = k - last_spoken_at[last_number] - 1
            else:
                speak = 0
            last_spoken_at[last_number] = k - 1
            last_number = speak
        return last_number

def test_coco():
    assert CocoSubmission().run("0,3,6", N=4) == 0
    assert CocoSubmission().run("0,3,6", N=5) == 3
    assert CocoSubmission().run("0,3,6", N=6) == 3
    assert CocoSubmission().run("0,3,6", N=7) == 1
    assert CocoSubmission().run("2,1,3") == 10
