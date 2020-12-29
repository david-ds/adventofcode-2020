from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):
    def rotate_trig(self, u, v, angle):
        if angle == 90:
            return -v, u
        elif angle == 180:
            return -u, -v
        elif angle == 270:
            return v, -u

    def run(self, s):
        instructions = s.splitlines()

        x, y = 0, 0
        u, v = 10, 1
        for ins in instructions:
            action, val = ins[0], int(ins[1:])
            if action == 'L':
                u, v = self.rotate_trig(u, v, val)
            elif action == 'R':
                u, v = self.rotate_trig(u, v, 360 - val)
            elif action == 'F':
                x += val * u
                y += val * v
            elif action == 'N':
                v += val
            elif action == 'S':
                v -= val
            elif action == 'E':
                u += val
            elif action == 'W':               
                u -= val
        return abs(x) + abs(y)
