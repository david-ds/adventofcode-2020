from collections import deque
from itertools import islice
from typing import Tuple

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        deck1, deck2 = self.parse_input(s)

        winner = self.combat(deck1, deck2)

        winner_deck = deck1 if winner == 1 else deck2
        return sum((i + 1) * card for i, card in enumerate(reversed(winner_deck)))

    @staticmethod
    def parse_input(s: str) -> Tuple[deque, deque]:
        player1, player2 = s.split("\n\n")
        deck1 = deque([int(n) for n in player1.splitlines()[1:]])
        deck2 = deque([int(n) for n in player2.splitlines()[1:]])
        return deck1, deck2

    def combat(self, deck1: deque, deck2: deque):
        seen = set()
        while deck1 and deck2:
            state = tuple(deck1), tuple(deck2)
            if state in seen:
                return 1
            seen.add(state)

            card1, card2 = deck1.popleft(), deck2.popleft()

            if len(deck1) >= card1 and len(deck2) >= card2:
                round_winner = self.combat(
                    deque(islice(deck1, card1)),
                    deque(islice(deck2, card2)),
                )
            else:
                round_winner = 1 if card1 > card2 else 2

            if round_winner == 1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)

        winner = 1 if deck1 else 2
        return winner


def test_day22_part2():
    assert (
        ThoreSubmission().run(
            """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
        )
        == 291
    )
