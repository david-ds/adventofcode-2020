from tool.runners.python import SubmissionPy

from functools import cache


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = [(line[0], int(line[1:])) for line in s.split("\n")]
        direction = "E"
        moves = {
            "N": 0,
            "S": 0,
            "E": 0,
            "W": 0,
        }

        for instruction in instructions:
            if instruction[0] == "F":
                moves[direction] += instruction[1]
            elif instruction[0] == "L" or instruction[0] == "R":
                direction = self.rotation(direction, instruction[0], instruction[1])
            else:
                moves[instruction[0]] += instruction[1]

        return abs(moves["N"] - moves["S"]) + abs(moves["E"] - moves["W"])

    @cache
    def rotation(self, direction, action, degrees):
        if direction == "E":
            orientation = 0
        elif direction == "N":
            orientation = 90
        elif direction == "W":
            orientation = 180
        elif direction == "S":
            orientation = 270

        if action == "L":
            orientation += degrees
        elif action == "R":
            orientation -= degrees

        orientation %= 360

        if orientation == 0:
            return "E"
        elif orientation == 90:
            return "N"
        elif orientation == 180:
            return "W"
        elif orientation == 270:
            return "S"
