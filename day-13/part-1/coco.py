from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        t, buses = s.split("\n")
        t = int(t)
        buses = [int(n) for n in buses.split(",") if n != "x"]
        waiting_times = {b: b - t % b for b in buses}
        best_bus = min(buses, key=lambda b: waiting_times[b])
        return best_bus*waiting_times[best_bus]
