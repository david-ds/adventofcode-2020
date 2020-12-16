from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        s = s.splitlines()
        possible_vals = set()

        for i in range(20):
            _, range_ = s[i].split(':')
            for x in range_.split(' or '):
                low, high = map(int, x.split('-'))
                possible_vals.add((low, high))

        error_rate = 0
        for ticket in s[25:]:
            for e in map(int, ticket.split(',')):
                is_valid = False
                for r in possible_vals:
                    if r[0] <= e <= r[1]:
                        is_valid = True
                        break
                if is_valid:
                    continue
                error_rate += e
        return error_rate
