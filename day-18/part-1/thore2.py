from tool.runners.python import SubmissionPy


class Thore2Submission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        return sum([evaluate(line) for line in s.splitlines()])


def evaluate(expr: str) -> int:
    """Evaluate the expression considering that there only are single digit
    numbers, parentheses, additions and multiplications and that multiplication
    and addition have the same precedence"""
    output = []
    operators = []
    for token in expr.replace(" ", ""):
        if token.isdigit():  # we assume that there isn't any number > 9 in expr
            output.append(int(token))
        elif token == "(":
            operators.append("(")
        elif token in [")", "+", "*"]:
            while operators and operators[-1] != "(":
                op = operators.pop()
                if op == "+":
                    output.append(output.pop() + output.pop())
                elif op == "*":
                    output.append(output.pop() * output.pop())
            if token != ")":
                operators.append(token)
            elif operators:
                operators.pop()

    while operators:
        op = operators.pop()
        if op == "+":
            output.append(output.pop() + output.pop())
        elif op == "*":
            output.append(output.pop() * output.pop())

    return output[0]


def test_day18_part1():
    assert Thore2Submission().run("2 * 3 + (4 * 5)") == 26
    assert Thore2Submission().run("5 + (8 * 3 + 9 + 3 * 4 * 3) ") == 437
    assert Thore2Submission().run("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert (
        Thore2Submission().run("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
        == 13632
    )
