from collections import defaultdict
from itertools import product

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        height, width = len(lines), len(lines[0])

        seat_status = {
            (i, j): c == "#"
            for i, line in enumerate(lines)
            for j, c in enumerate(line)
            if c != "."
        }

        neighbors = self.get_closest_neighbors(seat_status.keys(), height, width)

        neighbors_occupied = {
            seat: sum(seat_status[neighbor] for neighbor in neighbors[seat])
            for seat in seat_status
        }

        previous_seat_status = seat_status.copy()
        previous_neighbors_occupied = neighbors_occupied.copy()
        stable = False
        while not stable:
            stable = True
            for seat, occupied in previous_seat_status.items():
                if occupied and previous_neighbors_occupied[seat] >= 5:
                    seat_status[seat] = False
                    stable = False
                    for neighbor in neighbors[seat]:
                        neighbors_occupied[neighbor] -= 1
                elif not occupied and previous_neighbors_occupied[seat] == 0:
                    seat_status[seat] = True
                    stable = False
                    for neighbor in neighbors[seat]:
                        neighbors_occupied[neighbor] += 1
            previous_neighbors_occupied = neighbors_occupied.copy()
            previous_seat_status = seat_status.copy()

        return sum(seat_status.values())

    @classmethod
    def get_closest_neighbors(cls, seats, height, width):
        neighbors = defaultdict(list)
        directions = set(product((-1, 0, 1), (-1, 0, 1))) - {(0, 0)}
        for i, j in seats:
            for di, dj in directions:
                k = 1
                seat = (i + k * di, j + k * dj)
                while seat not in seats and cls.in_bounds(*seat, height, width):
                    k += 1
                    seat = (i + k * di, j + k * dj)
                if cls.in_bounds(*seat, height, width):
                    neighbors[(i, j)].append(seat)

        return neighbors

    @staticmethod
    def in_bounds(i, j, height, width):
        return i < height and j < width and i >= 0 and j >= 0

    @staticmethod
    def format_seats(seat_status, height, width):
        seats_array = [["." for j in range(width)] for i in range(height)]
        for (i, j), occupied in seat_status.items():
            seats_array[i][j] = "#" if occupied else "L"
        return "\n".join("".join(line) for line in seats_array) + "\n"
