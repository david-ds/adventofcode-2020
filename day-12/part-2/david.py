from tool.runners.python import SubmissionPy

# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.

class DavidSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        x,y = 0,0
        wx,wy = 10,1 # coordinates relative to the boat
        # Your code goes here
        for line in s.split("\n"):
            op = line[0]
            val = int(line[1:])

            if op == "N":
                wy += val
            elif op == "S":
                wy -= val
            elif op == "E":
                wx += val
            elif op == "W":
                wx -= val
            elif op == "L":
                for _ in range(val//90):
                    wx,wy = -wy,wx
            elif op == "R":
                for _ in range(val//90):
                    wx,wy = wy,-wx
            elif op == "F":
                x += val*wx
                y += val*wy
            else:
                raise ValueError("could not parse line : %s" % line)
        return abs(x)+abs(y)
