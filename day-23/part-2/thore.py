from itertools import chain

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s, moves=int(1e7), n_cups=int(1e6)):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = [int(c) for c in s]
        next_cup = list(range(1, n_cups + 2))
        for c, nc in zip(s, s[1:]):
            next_cup[c] = nc
        next_cup[s[-1]] = len(s) + 1
        next_cup[-1] = s[0]

        current_cup = s[0]
        for it in range(moves):
            # take the three cups after the current one (indices 1,2,3)
            pickup1 = next_cup[current_cup]
            pickup2 = next_cup[pickup1]
            pickup3 = next_cup[pickup2]
            next_cup[current_cup] = next_cup[pickup3]

            # find the destination cup and its index
            dest_cup = current_cup - 1 if current_cup > 1 else n_cups
            while dest_cup in [pickup1, pickup2, pickup3]:
                dest_cup -= 1
                if dest_cup == 0:
                    dest_cup = n_cups

            # place the picked up cups after the destination cup
            next_cup[dest_cup], next_cup[pickup3] = (
                pickup1,
                next_cup[dest_cup],
            )

            # update the current cup: immediately after the current current cup
            current_cup = next_cup[current_cup]

        star_cup1 = next_cup[1]
        star_cup2 = next_cup[star_cup1]
        return star_cup1 * star_cup2


def test_thore():
    """
    Run `python -m pytest ./day-23/part-2/thore.py` to test the submission.
    """
    assert ThoreSubmission().run("389125467") == 149245887792
