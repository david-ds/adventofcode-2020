from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):

    def decode_seat(self, encoding):
        binary_row = [{'F': '0', 'B': '1'}[c] for c in encoding[:7]]
        binary_col = [{'L': '0', 'R': '1'}[c] for c in encoding[7:]]
        row, col = int(''.join(binary_row), 2), int(''.join(binary_col), 2)
        return 8 * row + col

    def run(self, s):
        return max([self.decode_seat(e) for e in s.splitlines()])
