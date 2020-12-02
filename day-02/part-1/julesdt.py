from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        password_valid = 0
        for line in s.split('\n'):
            policy, password = line.split(': ')
            numbers, letter = policy.split(' ')
            low, high = map(int, numbers.split('-'))
            letter_count = password.count(letter)
            if low <= letter_count <= high:
                password_valid += 1
        return password_valid
