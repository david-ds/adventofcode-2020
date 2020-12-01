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
                for f in sentries:
                    if (2020 - e - f) in sentries:
                        return e * f * (2020 - e - f)
        else:
            # Slow loop when we detected at least one duplicated entry
            for i, e in enumerate(lentries):
                for j, f in enumerate(lentries[i + 1 :]):
                    if (2020 - e - f) in lentries[i + j + 2 :]:
                        return e * f * (2020 - e - f)
