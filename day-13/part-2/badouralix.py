from tool.runners.python import SubmissionPy

from math import prod


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        _, data = s.split("\n")
        shuttles = list()
        a = list()
        e = list()

        for index, shuttle in enumerate(data.split(",")):
            if shuttle != "x":
                shuttles.append(int(shuttle))
                a.append(-index)

        # Yolo assume that all numbers are coprime
        # See https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_des_restes_chinois#Algorithme
        n = prod(shuttles)
        for shuttle in shuttles:
            ni = n // shuttle
            vi = 1
            while (vi * ni) % shuttle != 1:
                vi += 1
            e.append(vi * ni)

        return sum(a[i] * e[i] for i in range(len(shuttles))) % n
