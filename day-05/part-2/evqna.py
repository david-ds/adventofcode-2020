from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def decode_seat(self, encoding):
        binary_repr = encoding.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
        return int(binary_repr, 2)

    def run(self, s):
        seat_ids = [self.decode_seat(e) for e in s.splitlines()]
        seat_ids.sort()
        prev = seat_ids[0]
        for n in seat_ids:
            if n > prev + 1:
                return prev + 1
            prev = n
        return -1
