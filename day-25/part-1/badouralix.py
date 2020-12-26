from tool.runners.python import SubmissionPy


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

        n, t = 0, 1
        while True:
            t = (t * g) % p
            n += 1

            if t == A:
                a = n
            if t == B:
                b = n

            if a is not None and b is not None:
                break

        # Implement square-and-multiply exponentiation
        gg, n = g, a * b
        result = 1
        while n != 0:
            if n % 2 == 1:
                result *= gg
            gg = (gg ** 2) % p
            n = n // 2

        return result % p


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
