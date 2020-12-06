from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def run(self, input):
        return max([get_seat_id(boarding_pass) for boarding_pass in input.split("\n")])


def get_seat_id(boarding_pass):
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

    return row * 8 + seat
