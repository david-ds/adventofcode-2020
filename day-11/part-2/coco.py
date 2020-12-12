from tool.runners.python import SubmissionPy

def print_table(table):
    for l in table:
        print("".join(l))
    print()

class CocoSubmission(SubmissionPy):

    EMPTY = "L"
    OCCUPIED = "#"
    FLOOR = "."

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here

        table = [list(l) for l in s.split("\n")]

        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]

        rows = len(table)
        cols = len(table[0])

        while True:
            changes = []
            for seat_x in range(rows):
                for seat_y in range(cols):
                    seat = table[seat_x][seat_y]
                    if seat == self.EMPTY:
                        # check that all are NOT occupied around
                        occupied_around = False
                        for (dx, dy) in directions:
                            x, y = seat_x, seat_y
                            while True:
                                x, y = x + dx, y + dy
                                if not (0 <= x < rows and 0 <= y < cols):
                                    break
                                if table[x][y] == self.OCCUPIED:
                                    occupied_around = True
                                    break
                                if table[x][y] == self.EMPTY:
                                    break
                            if occupied_around:
                                break
                        if not occupied_around:
                            changes.append((seat_x, seat_y, self.OCCUPIED))
       
                    if seat == self.OCCUPIED:
                        num_occupied = 0
                        # check number of empty seats around
                        for (dx, dy) in directions:
                            x, y = seat_x, seat_y
                            while True:
                                x, y = x + dx, y + dy
                                if not (0 <= x < rows and 0 <= y < cols):
                                    break
                                if table[x][y] == self.OCCUPIED:
                                    num_occupied += 1
                                    break
                                if table[x][y] == self.EMPTY:
                                    break

                        if num_occupied >= 5:
                            changes.append((seat_x, seat_y, self.EMPTY))

            if not changes:
                break

            for x, y, val in changes:
                table[x][y] = val

        return sum(1 for line in table for space in line  if space == self.OCCUPIED)
