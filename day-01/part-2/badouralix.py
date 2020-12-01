from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Parse input and store it as both a list and a set
        lentries = list(map(int, s.split()))
        sentries = set(lentries)

        if len(lentries) == len(sentries):
            # Fast loop as we know there is no duplicate
            for e in lentries:
                sentries.remove(e)
                subproduct = self.findsum(sentries, 2020 - e)
                if subproduct is not None:
                    return e * subproduct
        else:
            # Slow loop when we detected at least one duplicated entry
            for i, e in enumerate(lentries):
                subproduct = self.findsum(lentries[i:], 2020 - e)
                if subproduct is not None:
                    return e * subproduct

    def findsum(self, entries, target):
        """
        :param entries: a list or a set of integers
        :param target: an integer for which we want to find two entries that sum up to
        :return: the product of ( the ? ) two entries or None if we could not find any
        """
        for e in entries:
            if (target - e) in entries:
                return e * (target - e)

        return None
