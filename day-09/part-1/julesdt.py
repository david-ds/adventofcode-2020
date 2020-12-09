from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    BATCH_SIZE = 25

    @classmethod
    def find_incorrect_number(cls, number_list):
        current_set = set(number_list[:cls.BATCH_SIZE])
        for i in range(cls.BATCH_SIZE + 1, len(number_list)):
            current_set.remove(number_list[i - 1 -cls.BATCH_SIZE])
            current_set.add(number_list[i - 1])
            if not cls.is_sum_of_precedent(number_list[i], current_set):
                return number_list[i]

    @classmethod
    def is_sum_of_precedent(cls, number, number_set):
        for i in number_set:
            if (number - i) in number_set:
                return True
        return False

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        number_list = []
        for line in s.split('\n'):
            number_list.append(int(line))
        return self.find_incorrect_number(number_list)
