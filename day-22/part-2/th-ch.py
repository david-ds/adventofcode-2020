from tool.runners.python import SubmissionPy

from collections import deque
import itertools


class ThChSubmission(SubmissionPy):
    def hash_deck(self, player):
        return tuple(player)

    def subdeck(self, deck, n):
        return deque(itertools.islice(deck.copy(), 0, n))

    def play_game(self, player1, player2):
        already_played1 = set()
        already_played2 = set()

        while player1 and player2:
            hashed_deck1 = self.hash_deck(player1)
            hashed_deck2 = self.hash_deck(player2)
            if hashed_deck1 in already_played1 or hashed_deck2 in already_played2:
                return 1

            already_played1.add(hashed_deck1)
            already_played2.add(hashed_deck2)
            card1 = player1.popleft()
            card2 = player2.popleft()
            if len(player1) >= card1 and len(player2) >= card2:
                # Recursive game
                winner = self.play_game(
                    self.subdeck(player1, card1), self.subdeck(player2, card2)
                )
            else:
                winner = 1 if card1 > card2 else 2

            if winner == 1:
                player1.extend((card1, card2))
            else:
                player2.extend((card2, card1))

        return winner

    def run(self, s):
        player_decks = s.split("\n\n")
        player1 = deque(int(card) for card in player_decks[0].split("\n")[1:])
        player2 = deque(int(card) for card in player_decks[1].split("\n")[1:])

        winner = self.play_game(player1, player2)
        winner_deck = player1 if winner == 1 else player2

        nb_cards = len(winner_deck)
        return sum((nb_cards - i) * card for i, card in enumerate(winner_deck))
