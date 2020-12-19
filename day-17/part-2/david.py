from tool.runners.python import SubmissionPy

from collections import defaultdict,deque

class DavidSubmission(SubmissionPy):
    CYCLES = 6

    STATUS_INACTIVE = -1
    STATUS_ACTIVE = 1

    def status_from_str(cls, x):
        if x == "#":
            return cls.STATUS_ACTIVE
        else:
            return cls.STATUS_INACTIVE

    def build_offsets(cls, dimension):
        offsets = []
        q = deque()
        q.append(())
        while q:
            o = q.pop()
            if len(o) == dimension:
                if not all(x == 0 for x in o):
                    offsets.append(o)
                continue
            for i in {-1,0,1}:
                q.append((*o,i))
        assert(len(offsets) == 3**dimension-1)
        return offsets

    def build(self, s):
        lines = s.split("\n")
        len_y,len_x = len(lines), len(lines[0])
        grid = [
            [
                [[self.STATUS_INACTIVE \
                    for _ in range(1+(self.CYCLES+2)*2)] \
                    for _ in range(1+(self.CYCLES+2)*2)] \
                    for _ in range(len_y+2*(self.CYCLES+2))] \
                    for _ in range(len_x + 2*(self.CYCLES+2))
        ]
        self.active_cubes = 0
        for y,line in enumerate(lines):
            for x,v in enumerate(line):
                status = self.status_from_str(v)
                if status == self.STATUS_ACTIVE:
                    self.active_cubes += 1
                grid[x+self.CYCLES+2][y+self.CYCLES+2][self.CYCLES+2][self.CYCLES+2] = status
        self.grid = grid

    def count_actives(self, grid, pos, offsets):
        x,y,z,w = pos
        return sum(1 for dx,dy,dz,dw in offsets if grid[x+dx][y+dy][z+dz][w+dw] == self.STATUS_ACTIVE)


    def run_once(self, cycle, offsets):
        len_x, len_y, len_z, len_w = len(self.grid), len(self.grid[0]), len(self.grid[0][0]), len(self.grid[0][0][0])
        changes = []
        padding = self.CYCLES - cycle
        for x in range(1+padding, len_x-1-padding):
            for y in range(1+padding,len_y-1-padding):
                for z in range(1+padding, len_z-1-padding):
                    for w in range(1+padding, len_w-1-padding):
                        active_neighbors = self.count_actives(self.grid, (x,y,z,w), offsets)
                        if self.grid[x][y][z][w] == self.STATUS_ACTIVE:
                            if active_neighbors < 2 or active_neighbors > 3:
                                changes.append((x,y,z,w))
                        elif self.grid[x][y][z][w] == self.STATUS_INACTIVE:
                            if active_neighbors == 3:
                                changes.append((x,y,z,w))
        for x,y,z,w in changes:
            self.grid[x][y][z][w] = -self.grid[x][y][z][w]
            self.active_cubes += self.grid[x][y][z][w]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.build(s)
        offsets = self.build_offsets(4)
        for cycle in range(self.CYCLES):
            self.run_once(cycle, offsets)
        return self.active_cubes



