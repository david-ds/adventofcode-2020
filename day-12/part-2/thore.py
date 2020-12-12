from math import copysign, sin, cos, radians

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        position = [0, 0]  # West/East, South/North
        waypoint = [10, 1]  # relative to position

        for instruction in s.splitlines():
            action, value = instruction[0], int(instruction[1:])
            if action == "N":
                waypoint[1] += value
            elif action == "S":
                waypoint[1] -= value
            elif action == "E":
                waypoint[0] += value
            elif action == "W":
                waypoint[0] -= value
            elif action in ["L", "R"]:
                x, y = waypoint
                theta = radians(value * (-1 if action == "R" else 1))
                waypoint = [
                    int(round(x * cos(theta) - y * sin(theta))),
                    int(round(x * sin(theta) + y * cos(theta))),
                ]
            elif action == "F":
                position[0] += value * waypoint[0]
                position[1] += value * waypoint[1]
        return int(sum(map(abs, position)))


def test_day_12_part_2():
    s = """F10
N3
F7
R90
F11"""
    assert ThoreSubmission().run(s) == 286