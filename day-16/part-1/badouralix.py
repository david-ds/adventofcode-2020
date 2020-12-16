from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        stage = "rules"
        rules = set()
        result = 0

        for line in s.split("\n"):
            if line == "":
                continue
            elif line == "your ticket:":
                stage = "ours"
                continue
            elif line == "nearby tickets:":
                stage = "theirs"
                continue

            if stage == "rules":
                for r in line.split(": ")[1].split(" or "):
                    m, n = r.split("-")
                    rules.update(set(range(int(m), int(n) + 1)))
            elif stage == "theirs":
                for n in line.split(","):
                    if int(n) not in rules:
                        result += int(n)

        return result
