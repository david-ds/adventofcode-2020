from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        seats = {
            get_seat_id(*get_row_and_seat(boarding_pass))
            for boarding_pass in input.split("\n")
        }
        all_seats = set(range(2 ** 10 - 1))
        for seat_id in all_seats - seats:
            if seat_id - 1 in seats and seat_id + 1 in seats:
                return seat_id


def get_row_and_seat(boarding_pass):
    row_min, row_max = 0, 127
    for c in boarding_pass[:7]:
        middle = (row_max + row_min) // 2
        row_min, row_max = (row_min, middle) if c == "F" else (middle + 1, row_max)
    row = row_min

    seat_min, seat_max = 0, 7
    for c in boarding_pass[-3:]:
        middle = (seat_max + seat_min) // 2
        seat_min, seat_max = (seat_min, middle) if c == "L" else (middle + 1, seat_max)
    seat = seat_min

    return (row, seat)


def get_seat_id(row, seat):
    return row * 8 + seat
