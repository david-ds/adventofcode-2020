from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        lines = s.splitlines()
        start_time = int(lines[0])
        bus_ids = [int(c) for c in lines[1].split(",") if c != "x"]
        wait, bus_id = min((bus_id - start_time % bus_id, bus_id) for bus_id in bus_ids)
        return wait * bus_id


def test_day_13_part_1():
    assert ThoreSubmission().run("939\n7,13,x,x,59,x,31,19") == 295