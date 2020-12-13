from tool.runners.python import SubmissionPy

class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here

        # suppositions: all numbers are co-prime (it seems to be the case in the input ??)

        _, buses = s.split("\n")
        buses = [(k % int(n), int(n)) for k, n in enumerate(buses.split(",")) if n != "x"]

        _, base = buses[0]
        multiplier = base

        for rest, b in buses[1:]:
            k = 1
            while (base + multiplier * k) % b != b - rest:
                k += 1
            base = base + multiplier * k
            multiplier = multiplier * b
        return base

def test_sub():
    input = """N\n17,x,13,19"""
    assert CocoSubmission().run(input) == 3417
    assert CocoSubmission().run("N\n67,7,59,61") == 754018
    assert CocoSubmission().run("N\n67,x,7,59,61") == 779210
    assert CocoSubmission().run("N\n67,7,x,59,61") == 1261476
    assert CocoSubmission().run("N\n1789,37,47,1889") == 1202161486
