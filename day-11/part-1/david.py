from tool.runners.python import SubmissionPy


class DavidSubmission(SubmissionPy):
    FLOOR = 0
    OCCUPIED = 1
    EMPTY = -1

    OFFSETS = [(0,1), (1,0), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]

    @classmethod
    def from_str(cls, s):
        if s == ".":
            return cls.FLOOR
        elif s == "L":
            return cls.EMPTY
        elif s == "#":
            return cls.OCCUPIED
        else:
            raise ValueError()

    def run_once(self):
        """Runs the loop, and returns true if the grid changed"""
        changes = []

        for i,j in self.seats:                
            occupied = self.occupied_seats[i+1][j+1]
            if self.grid[i][j] == self.EMPTY and occupied == 0:
                changes.append((i,j, self.OCCUPIED))
            
            elif self.grid[i][j] == self.OCCUPIED and occupied >= 4:
                changes.append((i,j, self.EMPTY))

        for i,j, seat in changes:
            self.grid[i][j] = seat
            for di,dj in self.OFFSETS:
                    self.occupied_seats[i+1+di][j+1+dj] += seat

        return len(changes) > 0

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        self.grid = [[self.from_str(x) for x in line] for line in s.split("\n")]
        self.n = len(self.grid)
        self.m = len(self.grid[0])
        # occupied_seats[i][j] counts the number of seats occupied around (i-1,j-1)
        # (we add a padding so we don't have to check that the neighbors exist)
        # XXX: it assumes that there's no occupied seat at the beginning
        self.occupied_seats = [[0 for _ in range(self.m+2)] for _ in range(self.n+2)]
        self.seats = [(i,j) for i in range(self.n) for j in range(self.m) if self.grid[i][j] != self.FLOOR]

        while self.run_once():
            pass
        return sum((sum(x for x in line if x == self.OCCUPIED)) for line in self.grid)
