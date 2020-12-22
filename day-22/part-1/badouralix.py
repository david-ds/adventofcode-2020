from tool.runners.python import SubmissionPy

from queue import SimpleQueue


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        decks = list()

        for block in s.split("\n\n"):
            deck = SimpleQueue()
            for line in block.split("\n")[1:]:
                deck.put(int(line))
            decks.append(deck)

        while all(not deck.empty() for deck in decks):
            cards = tuple(deck.get() for deck in decks)

            if cards[0] > cards[1]:
                decks[0].put(cards[0])
                decks[0].put(cards[1])
            else:
                decks[1].put(cards[1])
                decks[1].put(cards[0])

        winner = 1 if decks[0].empty() else 0

        return sum(decks[winner].get() * i for i in range(decks[winner].qsize(), 0, -1))


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
        == 306
    )
