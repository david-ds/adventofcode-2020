from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        public_keys = [int(line) for line in s.splitlines()]
        INITIAL_SUBJECT_NUMBER = 7
        MODULO = 20201227

        loop_size, n = 0, 1
        while n != public_keys[0]:
            loop_size += 1
            n = (n * INITIAL_SUBJECT_NUMBER) % MODULO

        encryption_key = pow(public_keys[1], loop_size, MODULO)
        return encryption_key


def test_thore():
    """
    Run `python -m pytest ./day-25/part-1/thore.py` to test the submission.
    """
    assert (
        ThoreSubmission().run(
            """
5764801
17807724
""".strip()
        )
        == 14897079
    )
