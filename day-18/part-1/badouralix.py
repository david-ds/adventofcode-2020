from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        result = 0

        for line in s.split("\n"):
            # Yolo tokenize string
            linetokens = [
                int(t) if t.isnumeric() else t
                for t in line.replace("(", "( ").replace(")", " )").split(" ")
            ]

            # Yolo parse and evaluate tokens assuming it is syntaxely correct
            # The expression is evaluated left-to-right, and we got the left recursion for free by parsing from the right side
            lineresult, _ = self.evaluate(linetokens, len(linetokens) - 1)
            result += lineresult

        return result

    def evaluate(self, tokens, position):
        # Initialization hack to ensure the right term is always a number
        result = 0

        while position >= 0:
            token = tokens[position]

            # Do not ask, it works
            if token == "+":
                value, position = self.evaluate(tokens, position - 1)
                return result + value, position
            elif token == "*":
                value, position = self.evaluate(tokens, position - 1)
                return result * value, position
            elif token == "(":
                return result, position - 1
            elif token == ")":
                result, position = self.evaluate(tokens, position - 1)
            else:
                result = token
                position -= 1

        return result, position
