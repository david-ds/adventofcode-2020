from tool.runners.python import SubmissionPy

from functools import lru_cache


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        Implement a brute-force attack on Diffie-Hellman.

        :param s: input in string format
        :return: solution flag
        """
        g, p = 7, 20201227
        A, B = tuple(map(int, s.split("\n")))
        a, b = None, None

        for n in range(p):
            if self.pow(g, n, p) == A:
                a = n
            if self.pow(g, n, p) == B:
                b = n

            if a is not None and b is not None:
                break

        return self.pow(g, a * b, p)

    @lru_cache(maxsize=None)
    def pow(self, g, n, p):
        if n == 0:
            return 1
        elif n % 2 == 0:
            return (self.pow(g, n // 2, p) * self.pow(g, n // 2, p)) % p
        else:
            return (g * self.pow(g, n - 1, p)) % p


def test_badouralix():
    """
    Run `python -m pytest ./day-25/part-1/badouralix.py` to test the submission.
    """
    assert (
        BadouralixSubmission().run(
            """
5764801
17807724
""".strip()
        )
        == 14897079
    )
