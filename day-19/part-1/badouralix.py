from tool.runners.python import SubmissionPy

from collections import defaultdict
from functools import lru_cache


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Before each run we need to flush the cache to avoid side effects from previous runs
        self.match.cache_clear()

        # We need a class attribute here to pass it to the match method and still benefit from the cache
        self.rules = defaultdict(list)
        result = 0

        metadata, words = s.split("\n\n")

        for rule in metadata.split("\n"):
            rid, rlists = rule.split(": ")
            for rlist in rlists.split(" | "):
                self.rules[rid].append(rlist.replace('"', "").split(" "))

        for word in words.split("\n"):
            if self.match(word, "0") == len(word):
                result += 1

        return result

    @lru_cache(maxsize=None)
    def match(self, word, rid):
        if len(word) == 0:
            return -1
        elif self.rules[rid] == [["a"]] or self.rules[rid] == [["b"]]:
            if word[0] == self.rules[rid][0][0]:
                return 1
            else:
                return -1
        else:
            for subrule in self.rules[rid]:
                position = 0
                for step in subrule:
                    progress = self.match(word[position:], step)
                    if progress == -1:
                        break
                    else:
                        position += progress
                else:
                    # Here we assume that the first match is the only match
                    return position
            return -1
