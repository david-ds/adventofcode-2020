from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Parse input and handle the weird edge case where 1010 appears twice
        entries = list(map(int, s.split()))
        if entries.count(1010) == 2:
            return 1010 * 1010

        # Yolo build a set out of the list of entries
        entries = set(entries)

        # Find elements that sum up to 2020
        for e in entries:
            if (2020 - e) in entries:
                return e * (2020 - e)
