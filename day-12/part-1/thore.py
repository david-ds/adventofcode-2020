from math import copysign

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        position = [0, 0]  # West/East, South/North
        direction = 90  # East

        for instruction in s.splitlines():
            action, value = instruction[0], int(instruction[1:])
            if action == "N":
                position[1] += value
            elif action == "S":
                position[1] -= value
            elif action == "E":
                position[0] += value
            elif action == "W":
                position[0] -= value
            elif action == "L":
                direction -= value
                direction %= 360
            elif action == "R":
                direction += value
                direction %= 360
            elif action == "F":
                position[int(direction % 180 == 0)] += value * copysign(
                    1, 135 - direction
                )

        return int(sum(map(abs, position)))


def test_day_12_part_1():
    s = """F10
N3
F7
R90
F11"""
    assert ThoreSubmission().run(s) == 25