from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        possible_vals = set()
        i = 0
        while True:
            if s[i] != '':
                _, range_ = s[i].split(':')
                for x in range_.split(' or '):
                    low, high = map(int, x.split('-'))
                    possible_vals = possible_vals.union(set(range(low, high + 1)))
                i += 1
            else:
                break

        nearby_tickets = [list(map(int, x.split(','))) for x in s[i + 5:]]

        error_rate = 0
        for ticket in nearby_tickets:
            for e in ticket:
                if e not in possible_vals:
                    error_rate += e
        return error_rate
