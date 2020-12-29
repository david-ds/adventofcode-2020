from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):
    def run(self, s):
        instructions = s.splitlines()

        x, y = 0, 0
        deltas = [(0,1), (1,0), (0,-1), (-1,0)]   # N, E, S, W
        facing = 1  # E
        for ins in instructions:
            action, val = ins[0], int(ins[1:])
            if action == 'L':
                facing = (facing - val // 90) % 4
            elif action == 'R':
                facing = (facing + val // 90) % 4
            elif action == 'F':
                dx, dy = deltas[facing]
                x += val*dx
                y += val*dy
            elif action == 'N':
                y += val
            elif action == 'S':
                y -= val
            elif action == 'E':
                x += val
            elif action == 'W':               
                x -= val
        return abs(x) + abs(y)
