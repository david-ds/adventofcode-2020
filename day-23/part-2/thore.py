from __future__ import annotations
from dataclasses import dataclass
from itertools import chain
from typing import List

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s, moves=int(1e7), n_cups=int(1e6)):
        """
        :param s: input in string format
        :return: solution flag
        """
        start_labels = [int(c) for c in s]
        cups = [Cup(c) for c in chain(start_labels, range(10, n_cups + 1))]
        reverse_idx = {}
        for i in range(len(cups) - 1):
            cups[i].next_cup = cups[i + 1]
            reverse_idx[cups[i].label] = cups[i]
        cups[-1].next_cup = cups[0]
        reverse_idx[cups[-1].label] = cups[-1]

        current_cup = cups[0]
        for it in range(moves):
            # take the three cups after the current one (indices 1,2,3)
            pick_up = current_cup.popright(3)
            pick_up_labels = [cup.label for cup in pick_up]

            # find the destination cup and its index
            dest_label = current_cup.label - 1 if current_cup.label > 1 else n_cups
            while dest_label in pick_up_labels:
                dest_label -= 1
                if dest_label == 0:
                    dest_label = n_cups
            dest_cup = reverse_idx[dest_label]

            # place the picked up cups after the destination cup
            dest_cup.appendright(pick_up)

            # update the current cup: immediately after the current current cup
            current_cup = current_cup.next_cup

        star_cups = reverse_idx[1].popright(2)
        return star_cups[0].label * star_cups[1].label


@dataclass
class Cup:
    label: int
    next_cup: Cup = None

    def popright(self, n: int) -> List[Cup]:
        res = []
        cup = self.next_cup
        for _ in range(n):
            res.append(cup)
            cup = cup.next_cup
        res[-1].next_cup = None
        self.next_cup = cup
        return res

    def appendright(self, cups: List[Cup]):
        if not cups:
            return
        cups[-1].next_cup = self.next_cup
        self.next_cup = cups[0]
        for i in range(len(cups) - 1):
            cups[i].next_cup = cups[i + 1]

    def chain_to_string(self):
        labels = [str(self.label)]
        cup = self.next_cup
        while cup != self and len(labels) < 100:
            labels.append(str(cup.label))
            cup = cup.next_cup
        return ",".join(labels)


def test_thore():
    """
    Run `python -m pytest ./day-23/part-1/thore.py` to test the submission.
    """
    assert ThoreSubmission().run("389125467") == 149245887792
