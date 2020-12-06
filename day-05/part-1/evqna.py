from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def decode_seat(self, encoding):
        binary_repr = encoding.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
        return int(binary_repr, 2)

    def run(self, s):
        return max([self.decode_seat(e) for e in s.splitlines()])
