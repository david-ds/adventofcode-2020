from functools import reduce

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        enumerated_bus_ids = [
            (i, int(c)) for i, c in enumerate(s.splitlines()[1].split(",")) if c != "x"
        ]
        # For two buses, the times verifying the conditions are such that
        # t = m * a_id - a_offset = n * b_id - b_offset
        # The solutions are t = t0 + k * T with T = lcm(a, b)
        # We can therefore reduce these two buses to one bus of id T with an
        # offset of -t and reapply with the next bus, etc.
        return reduce(
            lambda x, y: solve_two_buses(-x[0], x[1], *y), enumerated_bus_ids
        )[0]


def extended_euclidean(a, b):
    """Extended Euclidean algorithm. Return s, t and r such that r = gcd(a, b)
    and s * a + t * b = r"""
    prev_r, r = a, b
    prev_s, s = 1, 0
    prev_t, t = 0, 1

    while r != 0:
        q = prev_r // r
        prev_r, r = r, prev_r - q * r
        prev_s, s = s, prev_s - q * s
        prev_t, t = t, prev_t - q * t

    return prev_s, prev_t, prev_r


def solve_two_buses(a_offset, a, b_offset, b):
    """Return the smallest time t such that t + a_offset is a multiple of a and
    t + b_offset is a multiple of b, as well as the period T such that all the
    t + k * T, k positive integer, verify the conditions."""
    # We look for m, n s.t. t = m * a - a_offset = n * b - b_offset
    # i.e. m * a + n * b = a_offset - b_offset
    # For this equation to have a solution, a_offset - b_offset must be a multiple
    # of gcd(a, b)
    s, t, gcd = extended_euclidean(a, b)  # s * a + t * b = gcd
    assert (a_offset - b_offset) % gcd == 0, "No solution"
    # We multiply the previous equation by (a_offset - b_offset) / gcd to get m
    m = (a_offset - b_offset) * s // gcd
    # We can compute a time t' = t + k * T
    common_time = m * a - a_offset
    # we know that T = lcm(a, b) = abs(a * b) // gcd(a, b)
    T = abs(a * b) // gcd
    # Therefore t, the smallest time, is t = t' % T
    return common_time % T, T


def test_day_13_part_1():
    assert ThoreSubmission().run("939\n7,13,x,x,59,x,31,19") == 1068781
    assert ThoreSubmission().run("939\n67,7,59,61") == 754018
    assert ThoreSubmission().run("939\n67,x,7,59,61") == 779210
    assert ThoreSubmission().run("939\n67,7,x,59,61") == 1261476
    assert ThoreSubmission().run("939\n1789,37,47,1889") == 1202161486
