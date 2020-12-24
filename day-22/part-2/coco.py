from typing import get_type_hints
from tool.runners.python import SubmissionPy
# from collections import namedtuple
from copy import copy

class CocoSubmission(SubmissionPy):

    def get_score(self, cards):
        return sum([n*k for n, k in zip(cards, reversed(range(1, len(cards)+1)))])

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        players = s.split("\n\n")
        players = [[int(n) for n in p.split("\n")[1:]] for p in players]

        player1, player2 = players

        stack = []

        stack.append("end")
        stack.append(None) # no arguments for end. 
        stack.append("entry")
        args = (player1, player2, set())
        stack.append(args)
        stack.append(None) # result

        # non-recursive for practice and fun
        while stack:
            # print(len(stack))
            res = stack.pop()
            args = stack.pop()
            address = stack.pop()

            if address == "entry":
                player1, player2, history = args
                state = tuple(player1), tuple(player2)
                if state in history:
                    stack.append(("player1", player1))
                    continue
                elif len(player1) == 0:
                    stack.append(("player2", player2))
                    continue
                elif len(player2) == 0:
                    stack.append(("player1", player1))
                    continue
                else:
                    history.add((tuple(player1), tuple(player2)))
                    card1, card2 = player1[0], player2[0]
                    remaining1, remaining2 = player1[1:], player2[1:]
                    if len(remaining1) < card1 or len(remaining2) < card2:
                        # winner is the one with the higher-value card
                        if card1 > card2:
                            player1 = remaining1 + [card1, card2]
                            player2 = remaining2
                        elif card2 >= card1:
                            player2 = remaining2 + [card2, card1]
                            player1 = remaining1

                        stack.append("entry")
                        stack.append((player1, player2, history))
                        stack.append(None)
                        continue
                    else:
                        stack.append("continue")
                        stack.append((player1, player2, history))
                        # create new round
                        stack.append("entry")
                        stack.append((remaining1[:card1], remaining2[:card2], set())) # no history, new game
                        stack.append(None)  # no result
                        continue

            elif address == "continue":
                winner, _ = res
                player1, player2, history = args
                card1, card2 = player1.pop(0), player2.pop(0)
                if winner == "player1":
                    player1.append(card1)
                    player1.append(card2)
                else:
                    player2.append(card2)
                    player2.append(card1)

                stack.append("entry")
                stack.append((player1, player2, history))
                stack.append(None)
                continue

            elif address == "end":
                winner, result = res
                return self.get_score(result)


def test_coco():
    """
    Run `python -m pytest ./day-22/part-1/coco.py` to test the submission.
    """
    assert (
        CocoSubmission().run(
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


    assert CocoSubmission().run("""Player 1:
43
19

Player 2:
2
29
14""") == 105


