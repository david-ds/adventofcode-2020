from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        seats = set()

        for line in s.split():
            seat = 0

            for char in line:
                seat *= 2
                if char == "B" or char == "R":
                    seat += 1

            seats.add(seat)

        return (
            {seat for seat in range(min(seats), max(seats) + 1)}.difference(seats).pop()
        )
