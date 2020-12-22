from tool.runners.python import SubmissionPy


class {class_name}(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        pass


def test_{author_name}():
    """
    Run `python -m pytest {submission_file}` to test the submission.
    """
    assert (
        {class_name}().run(
            """
""".strip()
        )
        == None
    )
