from tool.runners.python import SubmissionPy


class CocoSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        cups = [int(x) for x in list(s.strip())]
        N = len(cups)
        position = 0
        for k in range(100):
            item = cups[position]
            removed = [cups[(position + k) % N] for k in range(1, 4)]
            remaining = [cups[(position + k) % N] for k in range(4, len(cups) + 1)]
            destination_value = (item - 2) % N + 1
            while destination_value in removed:
                destination_value = (destination_value - 2) % N + 1
            index = remaining.index(destination_value)
            cups = remaining[:index+1] + removed + remaining[index+1:]
            position = (cups.index(item) + 1) % N
        
        index_one = cups.index(1)
        return "".join(str(cups[k % N]) for k in range(index_one + 1, index_one + len(cups)))

def test_coco():
    """
    Run `python -m pytest ./day-23/part-1/coco.py` to test the submission.
    """
    assert (
        CocoSubmission().run(
            """389125467""".strip()
        )
        == "67384529"
    )
