from tool.runners.python import SubmissionPy

MAX_DELTA = 3

class EvqnaSubmission(SubmissionPy):

    def local_paths_from(self, L, i):
        j = i + 1
        while j < len(L) and L[j] - L[i] <= MAX_DELTA:
            j += 1
        return max(j - i - 1, 1)    # Edge case: i == len(L)

    def count_paths(self, L):
        path_degrees = [self.local_paths_from(L, i) for i in range(len(L))]
        paths_to_end = [1]
        for d in reversed(path_degrees):
            paths_to_end.append(sum(paths_to_end[-d:]))
        return paths_to_end[-1]

    def run(self, s):
        adapters = sorted([0] + [int(n) for n in s.splitlines()])
        return self.count_paths(adapters)
