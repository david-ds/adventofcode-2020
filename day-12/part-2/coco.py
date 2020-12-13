from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):

    moves = {"N": (1, 0), "S": (-1, 0), "E": (0, -1), "W": (0, 1)}

    directions = ["E", "S", "W", "N"]

    turns = {
        "R": 1,
        "L": -1,
    }

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        instructions = s.split("\n")
        direction_id = 0  # EAST
        x, y = 0, 0
        waypoint_x, waypoint_y = 1, -10 # 1 NORTH, 10 EAST  (relative coords)
        for inst in instructions:
            action = inst[0]
            number = int(inst[1:])
            if action == "F":
                x, y = x + waypoint_x*number, y + waypoint_y*number
            elif action in self.moves:
                dx, dy = self.moves[action]
                waypoint_x, waypoint_y = waypoint_x + (dx * number), waypoint_y + (dy * number)
            else:  # action is a turn
                if number == 180:
                    waypoint_x = -waypoint_x
                    waypoint_y = -waypoint_y
                elif (action == "R" and number == 90) or (action == "L" and number == 270):
                    waypoint_x, waypoint_y = waypoint_y, -waypoint_x
                elif (action == "R" and number == 270) or (action == "L" and number == 90):
                    waypoint_x, waypoint_y = - waypoint_y, waypoint_x
        return abs(x) + abs(y)
