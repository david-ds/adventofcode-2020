from tool.runners.python import SubmissionPy

from collections import deque


class ThChSubmission(SubmissionPy):
    def run(self, s):
        player_decks = s.split("\n\n")
        player1 = deque(int(card) for card in player_decks[0].split("\n")[1:])
        player2 = deque(int(card) for card in player_decks[1].split("\n")[1:])

        while player1 and player2:
            card1 = player1.popleft()
            card2 = player2.popleft()
            winner = player1 if card1 > card2 else player2
            winner.extend((max(card1, card2), min(card1, card2)))

        winner = player1 or player2
        nb_cards = len(winner)
        return sum((nb_cards - i) * card for i, card in enumerate(winner))
