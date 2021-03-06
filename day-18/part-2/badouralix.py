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
            lineresult, _ = self.evaluate(linetokens)
            result += lineresult

        return result

    def evaluate(self, tokens, position=0):
        # Initialization hack to ensure the left term is always a number
        result = 0

        while position != len(tokens):
            token = tokens[position]

            # Do not ask, it works
            if token == "*":
                # Evaluate right-hand side first
                value, position = self.evaluate(tokens, position + 1)
                return result * value, position
            elif token != "+":
                # Evaluate left-hand side first
                if token == ")":
                    return result, position
                elif token == "(":
                    value, position = self.evaluate(tokens, position + 1)
                else:
                    value = token
                result += value

            position += 1

        return result, position
