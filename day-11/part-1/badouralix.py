from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = s.split("\n")

        # Build a pre-lookup of the neighbor seats of all seats
        # Careful here, the neighbor list of a seat contains the seat itself
        neighbors = []
        for i, row in enumerate(grid):
            lineneighbors = list()
            for j, seat in enumerate(row):
                if seat == ".":
                    lineneighbors.append(list())
                    continue
                seatneighbors = list()
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if (
                            0 <= i + x < len(grid)
                            and 0 <= j + y < len(row)
                            and grid[i + x][j + y] != "."
                        ):
                            seatneighbors.append((i + x, j + y))
                lineneighbors.append(seatneighbors)
            neighbors.append(lineneighbors)

        # Run game of life steps
        while True:
            backup = grid.copy()
            for i, row in enumerate(grid):
                newrow = ""
                for j, seat in enumerate(row):
                    occupied = 0
                    for (ii, jj) in neighbors[i][j]:
                        if backup[ii][jj] == "#":
                            occupied += 1
                    if seat == "L" and occupied == 0:
                        newrow += "#"
                    elif seat == "#" and occupied >= 5:
                        newrow += "L"
                    else:
                        newrow += seat
                grid[i] = newrow
            if grid == backup:
                break

        return sum(row.count("#") for row in grid)
