from tool.runners.python import SubmissionPy


class JulesdtSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        adapters = []
        for line in s.split('\n'):
            adapters.append(int(line))
        adapters = sorted(adapters)
        current_value = 0
        diff1 = 0
        diff3 = 1
        for adapter in adapters:
            if adapter - current_value == 1:
                diff1 += 1
            elif adapter - current_value == 3:
                diff3 += 1
            current_value = adapter
        return diff1 * diff3
