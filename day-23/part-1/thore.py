from collections import deque

from tool.runners.python import SubmissionPy

N_CUPS = 9


class ThoreSubmission(SubmissionPy):
    def run(self, s, moves=100):
        """
        :param s: input in string format
        :return: solution flag
        """
        cups = deque([int(c) for c in s], maxlen=N_CUPS)
        for _ in range(moves):
            # take the three cups after the current one (indices 1,2,3)
            cups.rotate(-1)
            pick_up = [cups.popleft() for _ in range(3)]
            cups.rotate(1)

            # find the destination cup and its index
            dest_label = cups[0] - 1 if cups[0] > 1 else N_CUPS
            while dest_label in pick_up:
                dest_label -= 1
                if dest_label == 0:
                    dest_label = N_CUPS
            dest_idx = cups.index(dest_label)

            # place the picked up cups after the destination cup
            cups.rotate(-dest_idx - 1)
            cups.extendleft(reversed(pick_up))

            # update the current cup: immediately after the current current cup
            cups.rotate(dest_idx)

        cup_one_idx = cups.index(1)
        cups.rotate(-cup_one_idx)
        cups.popleft()
        return "".join(map(str, cups))


def test_thore():
    """
    Run `python -m pytest ./day-23/part-1/thore.py` to test the submission.
    """
    assert ThoreSubmission().run("389125467", moves=10) == "92658374"
    assert ThoreSubmission().run("389125467") == "67384529"
