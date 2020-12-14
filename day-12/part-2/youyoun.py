from tool.runners.python import SubmissionPy

dir_plane_map = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 1): 2,
    (1, 0): 3,
}

planes = [(-1, -1), (-1, 1), (1, 1), (1, -1)]


class YouyounSubmission(SubmissionPy):
    def __init__(self):
        super().__init__()
        self.ship_x = 0
        self.ship_y = 0
        self.way_x = 10
        self.way_y = 1

    def reinit(self):
        self.ship_x = 0
        self.ship_y = 0
        self.way_x = 10
        self.way_y = 1

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
        return abs(self.ship_x) + abs(self.ship_y)

    def process(self, dir_, steps):
        if dir_ == 'N':
            self.way_y += steps
        elif dir_ == 'S':
            self.way_y -= steps
        elif dir_ == 'E':
            self.way_x += steps
        elif dir_ == 'W':
            self.way_x -= steps
        elif dir_ == 'F':
            self.ship_y = self.ship_y + steps * self.way_y
            self.ship_x = self.ship_x + steps * self.way_x

    def turn(self, degrees, steps):
        dir = dir_plane_map[((self.way_x > 0), (self.way_y > 0))]
        turn = 1 if degrees == 'R' else -1
        for _ in range(steps // 90):
            dir = (dir + turn) % 4
            self.way_y, self.way_x = planes[dir][1] * abs(self.way_x), planes[dir][0] * abs(self.way_y)


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
