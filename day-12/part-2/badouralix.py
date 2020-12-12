from tool.runners.python import SubmissionPy

from functools import lru_cache


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        instructions = [(line[0], int(line[1:])) for line in s.split("\n")]
        position = (0, 0)
        waypoint = (10, 1)

        for instruction in instructions:
            if instruction[0] == "N":
                waypoint = (waypoint[0], waypoint[1] + instruction[1])
            elif instruction[0] == "S":
                waypoint = (waypoint[0], waypoint[1] - instruction[1])
            elif instruction[0] == "E":
                waypoint = (waypoint[0] + instruction[1], waypoint[1])
            elif instruction[0] == "W":
                waypoint = (waypoint[0] - instruction[1], waypoint[1])
            elif instruction[0] == "L" or instruction[0] == "R":
                rotation = self.rotation(instruction[0], instruction[1])
                if rotation == 90:
                    waypoint = (-waypoint[1], waypoint[0])
                elif rotation == 180:
                    waypoint = (-waypoint[0], -waypoint[1])
                elif rotation == 270:
                    waypoint = (waypoint[1], -waypoint[0])
            elif instruction[0] == "F":
                position = (
                    position[0] + waypoint[0] * instruction[1],
                    position[1] + waypoint[1] * instruction[1],
                )

        return abs(position[0]) + abs(position[1])

    @lru_cache(maxsize=None)
    def rotation(self, action, degrees):
        if action == "R":
            degrees = -degrees

        return degrees % 360
