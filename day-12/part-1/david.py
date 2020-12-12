from tool.runners.python import SubmissionPy

# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.

class DavidSubmission(SubmissionPy):
    DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        x,y = 0,0
        cur_direction = 0 # direction east
        # Your code goes here
        for line in s.split("\n"):
            op = line[0]
            val = int(line[1:])

            if op == "N":
                y += val
            elif op == "S":
                y -= val
            elif op == "E":
                x += val
            elif op == "W":
                x -= val
            elif op == "L":
                cur_direction = (cur_direction + (val//90)) % 4
            elif op == "R":
                cur_direction = (cur_direction - (val//90)) % 4
            elif op == "F":
                dx,dy = self.DIRECTIONS[cur_direction]
                x += dx*val
                y += dy*val
            else:
                raise ValueError("could not parse line : %s" % line)
        return abs(x)+abs(y)
