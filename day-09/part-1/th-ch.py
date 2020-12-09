from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    preamble_length = 25

    def run(self, s):
        nbs = s.split("\n")
        # Can use a set because "The two numbers will have different values"
        candidates = set()

        for i, nb in enumerate(nbs):
            nb = int(nb)
            if i >= self.preamble_length:
                if not self.has_matching_sum(candidates, nb):
                    return nb

                candidates.remove(int(nbs[i - self.preamble_length]))

            candidates.add(nb)

    def has_matching_sum(self, candidates, target):
        for nb in candidates:
            if target - nb in candidates:
                return True

        return False
