from itertools import chain

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s, moves=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        cups = [int(c) for c in s]
        n_cups = len(cups)
        next_cup = [0] * (n_cups + 1)
        for i in range(len(cups) - 1):
            next_cup[cups[i]] = cups[i + 1]
        next_cup[cups[-1]] = cups[0]

        current_cup = cups[0]
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

        cup = next_cup[1]
        res = []
        while not cup == 1:
            res.append(str(cup))
            cup = next_cup[cup]
        return "".join(res)


def test_thore():
    """
    Run `python -m pytest ./day-23/part-1/thore.py` to test the submission.
    """
    assert ThoreSubmission().run("389125467", moves=10) == "92658374"
    assert ThoreSubmission().run("389125467") == "67384529"
