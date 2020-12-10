from tool.runners.python import SubmissionPy


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        adapters = set(map(int, s.split()))
        adapters.add(0)

        return self.arrangements(adapters, 0, {(max(adapters) + 3): 1})

    def arrangements(self, adapters, adapter, cache):
        if adapter in cache:
            return cache[adapter]

        if adapter not in adapters:
            arrangements = 0
        else:
            arrangements = (
                self.arrangements(adapters, adapter + 1, cache)
                + self.arrangements(adapters, adapter + 2, cache)
                + self.arrangements(adapters, adapter + 3, cache)
            )

        cache[adapter] = arrangements
        return cache[adapter]
