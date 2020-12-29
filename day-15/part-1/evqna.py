from tool.runners.python import SubmissionPy


class EvqnaSubmission(SubmissionPy):
    def get_next_number(self, prev, state, ts):
        if prev not in state:
            return 0
        return ts - state[prev]

    def run(self, s):
        starting_numbers = [int(c) for c in s.strip().split(',')]
        game_state = {n: i + 1 for i, n in enumerate(starting_numbers)}

        round_num = len(starting_numbers) + 1
        cur = 0
        while round_num < 2020:
            next = self.get_next_number(cur, game_state, round_num)
            game_state[cur] = round_num
            cur = next
            round_num += 1
        return cur
