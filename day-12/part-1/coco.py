from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):

    moves = {"N": (1, 0), "S": (-1, 0), "E": (0, -1), "W": (0, 1)}
    directions = ["E", "S", "W", "N"]  # in the right order to loop through them.
    turns = {"R": 1, "L": -1}

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = s.split("\n")
        direction_id = 0  # EAST
        x, y = 0, 0
        for inst in instructions:
            action = inst[0]
            number = int(inst[1:])
            if action == "F":
                action = self.directions[direction_id]
            if action in self.moves:
                dx, dy = self.moves[action]
                x, y = x + (dx * number), y + (dy * number)
            else:  # action is a turn
                turn = self.turns[action]
                direction_id = (direction_id + (number // 90) * turn) % 4
        return abs(x) + abs(y)
