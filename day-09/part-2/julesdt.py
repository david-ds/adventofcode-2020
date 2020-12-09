from tool.runners.python import SubmissionPy
day09julesdt = __import__("day-09.part-1.julesdt")


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        number_list = []
        for line in s.split('\n'):
            number_list.append(int(line))
        # Hack to get the part-1 code.
        part1_submission = getattr(day09julesdt, "part-1").julesdt.JulesdtSubmission
        number_to_find = part1_submission.find_incorrect_number(number_list)
        # okay now we got it let's roll

        for i in range(2, len(number_list)):
            curr_sum = number_list[i-1]
            for j in range(i-2, -1, -1):
                curr_sum += number_list[j]
                if curr_sum > number_to_find:
                    break
                if curr_sum == number_to_find:
                    return min(number_list[j:i]) + max(number_list[j:i])
