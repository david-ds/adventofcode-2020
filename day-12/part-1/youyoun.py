from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.direction = 1

    def reinit(self):
        self.x = 0
        self.y = 0
        self.direction = 1

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        self.reinit()
        for e in s:
            if e[0] == 'L' or e[0] == 'R':
                self.turn(e[0], int(e[1:]))
            else:
                self.process(e[0], int(e[1:]))
        return abs(self.x) + abs(self.y)

    def process(self, dir_, steps):
        if dir_ == 'N':
            self.y += steps
        elif dir_ == 'S':
            self.y -= steps
        elif dir_ == 'E':
            self.x += steps
        elif dir_ == 'W':
            self.x -= steps
        elif dir_ == 'F':
            if self.direction % 2 == 0:
                self.y = self.y + (1 if self.direction == 0 else -1) * steps
            elif self.direction % 2 == 1:
                self.x = self.x + (1 if self.direction == 1 else -1) * steps

    def turn(self, degrees, steps):
        self.direction = (self.direction + (1 if degrees == 'R' else -1) * steps // 90) % 4
