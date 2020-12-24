from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        players = s.split("\n\n")
        players = [[int(n) for n in p.split("\n")[1:]] for p in players]

        player1, player2 = players

        while player1 and player2:
            card1, card2 = player1.pop(0), player2.pop(0)
            if card1 > card2:
                player1.append(card1)
                player1.append(card2)
            elif card2 > card1:
                player2.append(card2)
                player2.append(card1)
            else:
                raise ValueError()
        if player1:
            winner = player1
        else:
            winner = player2
        return sum([n*k for n, k in zip(winner, reversed(range(1, len(winner)+1)))])


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
        == 306
    )
