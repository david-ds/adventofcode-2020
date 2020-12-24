from tool.runners.python import SubmissionPy

from collections import deque


class ThChSubmission(SubmissionPy):
    def run(self, s, nb_moves=100):
        cups = deque(int(c) for c in s)
        current_cup = cups[0]
        for _ in range(nb_moves):
            picked_cups = []
            for i in range(3, 0, -1):
                index = (cups.index(current_cup) + i) % len(cups)
                picked_cups.append(cups[index])
                cups.remove(cups[index])

            destination_cup = current_cup - 1
            i = None
            while i is None:
                if destination_cup < min(cups):
                    destination_cup = max(cups)
                try:
                    i = cups.index(destination_cup)
                except ValueError:
                    destination_cup -= 1

            for picked_cup in picked_cups:
                cups.insert((i + 1), picked_cup)

            current_cup = cups[(cups.index(current_cup) + 1) % len(cups)]

        first = cups.index(1)
        return "".join(
            str(cups[i % len(cups)]) for i in range(first + 1, first + len(cups))
        )


def test_th_ch():
    """
    Run `python -m pytest ./day-23/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
389125467
""".strip()
        )
        == "67384529"
    )
