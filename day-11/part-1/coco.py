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

        around = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, 1), (1, -1), (1, 1), (-1, -1)]

        rows = len(table)
        cols = len(table[0])

        seats_around_position = dict()
        while True:
            changes = []
            for seat_x in range(rows):
                for seat_y in range(cols):
                    seat = table[seat_x][seat_y]
                    # memoization
                    if (seat_x, seat_y) in seats_around_position:
                        around_seat = seats_around_position[(seat_x, seat_y)]
                    else:
                        around_seat = [(seat_x + x, seat_y+y) for (x, y) in around]
                        around_seat = [(x, y) for x, y in around_seat if 0 <= x < rows and  0 <= y < cols]
                        seats_around_position[(seat_x, seat_y)] = around_seat
                    if seat == self.EMPTY:
                        if all(table[x][y] != self.OCCUPIED for x, y in around_seat):
                            changes.append((seat_x, seat_y, self.OCCUPIED))
                    elif seat == self.OCCUPIED:
                        if len([1 for x, y in around_seat if table[x][y] == self.OCCUPIED]) >= 4:
                            changes.append((seat_x, seat_y, self.EMPTY))
            if not changes:
                break

            for x, y, val in changes:
                table[x][y] = val

        return sum(1 for line in table for space in line  if space == self.OCCUPIED)
