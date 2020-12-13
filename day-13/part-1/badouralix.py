from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        data = s.replace(",", "\n").split("\n")
        depart = int(data[0])
        shuttles = [int(shuttle) for shuttle in data[1:] if shuttle != "x"]

        waittimes = [timestamp - depart % timestamp for timestamp in shuttles]
        _, index = min((v, k) for (k, v) in enumerate(waittimes))

        return shuttles[index] * waittimes[index]
