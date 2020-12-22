from tool.runners.python import SubmissionPy

from collections import deque
from itertools import islice


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        decks = tuple(
            deque(int(line) for line in block.split("\n")[1:])
            for block in s.split("\n\n")
        )

        winner = self.play(decks)

        return sum(
            decks[winner].popleft() * i for i in range(len(decks[winner]), 0, -1)
        )

    def play(self, decks):
        """
        Play the entire game of recursive combat with players' decks.
        This changes the deck of all players.

        :param decks: players' decks as a tuple
        :return: winner id
        """
        history = set()

        while all(len(deck) != 0 for deck in decks):
            # Check game state against previous game states
            state = tuple(tuple(deck) for deck in decks)
            if state in history:
                return 0
            history.add(state)

            # Each player draws the top card
            cards = tuple(deck.popleft() for deck in decks)

            if all(len(decks[player]) >= cards[player] for player in range(len(decks))):
                # All players have enough remaining cards to recursively play a new game
                # See https://stackoverflow.com/questions/7064289/use-slice-notation-with-collections-deque
                winner = self.play(
                    tuple(
                        deque(islice(decks[player], 0, cards[player]))
                        for player in range(len(decks))
                    )
                )
            else:
                # The winner of the round is the player with the highest-value card
                winner = 0 if cards[0] > cards[1] else 1

            if winner == 0:
                decks[0].append(cards[0])
                decks[0].append(cards[1])
            else:
                decks[1].append(cards[1])
                decks[1].append(cards[0])

        # The winner of the game is the player with the non-empty deck
        return 0 if len(decks[0]) != 0 else 1


def test_badouralix():
    assert (
        BadouralixSubmission().run(
            """
Player 1:
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
10
""".strip()
        )
        == 291
    )
