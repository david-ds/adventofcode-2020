from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        grid = s.split("\n")

        while True:
            after = []

            for i, row in enumerate(grid):
                newrow = ""

                for j, seat in enumerate(row):
                    occupied = 0

                    for x in [-1, 0, 1]:
                        if 0 <= i + x < len(grid):
                            for y in [-1, 0, 1]:
                                if 0 <= j + y < len(row) and grid[i + x][j + y] == "#":
                                    occupied += 1

                    if seat == "L" and occupied == 0:
                        newrow += "#"
                    elif seat == "#" and occupied >= 5:
                        newrow += "L"
                    else:
                        newrow += seat

                after.append(newrow)

            if grid == after:
                break

            grid = after

        return sum(row.count("#") for row in grid)
