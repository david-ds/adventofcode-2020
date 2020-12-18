from typing import Dict

from tool.runners.python import SubmissionPy


class Thore2Submission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        return sum([evaluate(line) for line in s.splitlines()])


OP_PRECEDENCE = {"+": 1, "*": 0}


def evaluate(expr: str, op_precedence: Dict[str, int] = OP_PRECEDENCE) -> int:
    """Evaluate the expression considering that there only are single digit
    numbers, parentheses and operator, whose precedence is given by the
    op_precedence dictionnary"""
    output = []
    operators = []

    def apply_op(op):
        if op == "+":
            output.append(output.pop() + output.pop())
        elif op == "*":
            output.append(output.pop() * output.pop())

    for token in expr.replace(" ", ""):
        if token.isdigit():  # we assume that there isn't any number > 9 in expr
            output.append(int(token))
        elif token == "(":
            operators.append("(")
        elif token == ")":
            while (op := operators.pop()) != "(":
                apply_op(op)
        elif token in op_precedence.keys():
            while (
                operators
                and operators[-1] != "("
                and op_precedence[operators[-1]] >= op_precedence[token]
            ):
                apply_op(operators.pop())
            operators.append(token)

    while operators:
        apply_op(operators.pop())

    return output[0]


def test_day18_part2():
    assert Thore2Submission().run("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert Thore2Submission().run("2 * 3 + (4 * 5)") == 46
    assert Thore2Submission().run("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert Thore2Submission().run("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert (
        Thore2Submission().run("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
        == 23340
    )