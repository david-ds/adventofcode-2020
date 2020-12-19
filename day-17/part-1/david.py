from tool.runners.python import SubmissionPy

from collections import defaultdict

class DavidSubmission(SubmissionPy):
    CYCLES = 6

    STATUS_INACTIVE = -1
    STATUS_ACTIVE = 1

    OFFSETS = [
        ( 1,1,-1), ( 1,1,0), ( 1,1,1), ( 1,0,-1), ( 1,0,0), ( 1,0,1), ( 1,-1,-1), ( 1,-1,0), ( 1,-1,1),
        (-1,1,-1), (-1,1,0), (-1,1,1), (-1,0,-1), (-1,0,0), (-1,0,1), (-1,-1,-1), (-1,-1,0), (-1,-1,1),
        ( 0,1,-1), ( 0,1,0), ( 0,1,1), ( 0,0,-1), ( 0,0,1), ( 0,-1,-1), (0,-1,0), (0,-1,1)]

    def status_from_str(cls, x):
        if x == "#":
            return cls.STATUS_ACTIVE
        else:
            return cls.STATUS_INACTIVE


    def build(self, s):
        lines = s.split("\n")
        len_y,len_x = len(lines), len(lines[0])
        grid = [[[self.STATUS_INACTIVE for _ in range((self.CYCLES+2)*2)] for _ in range(len_y+2*(self.CYCLES+2))] for _ in range(len_x + 2*(self.CYCLES+2))]
        self.active_cubes = 0
        for y,line in enumerate(lines):
            for x,v in enumerate(line):
                status = self.status_from_str(v)
                if status == self.STATUS_ACTIVE:
                    self.active_cubes += 1
                grid[x+self.CYCLES+1][y+self.CYCLES+1][self.CYCLES+1] = status
        self.grid = grid

    def count_actives(self, grid, pos):
        x,y,z = pos
        return sum(1 for dx,dy,dz in self.OFFSETS if grid[x+dx][y+dy][z+dz] == self.STATUS_ACTIVE)


    def run_once(self):
        len_x, len_y, len_z = len(self.grid), len(self.grid[0]), len(self.grid[0][0])
        changes = []
        for x in range(1, len_x-1):
            for y in range(1,len_y-1):
                for z in range(1, len_z-1):
                    active_neighbors = self.count_actives(self.grid, (x,y,z))
                    if self.grid[x][y][z] == self.STATUS_ACTIVE:
                        if active_neighbors < 2 or active_neighbors > 3:
                            changes.append((x,y,z))
                    elif self.grid[x][y][z] == self.STATUS_INACTIVE:
                        if active_neighbors == 3:
                            changes.append((x,y,z))
        for x,y,z in changes:
            self.grid[x][y][z] = -self.grid[x][y][z]
            self.active_cubes += self.grid[x][y][z]

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        self.build(s)
        print(self.active_cubes)
        for cycle in range(self.CYCLES):
            self.run_once()
        return self.active_cubes



