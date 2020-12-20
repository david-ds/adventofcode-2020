from tool.runners.python import SubmissionPy

from collections import defaultdict
from typing import Set


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        rules, words = s.split("\n\n")
        data = defaultdict(list)

        for rule in rules.split("\n"):
            rid, rlists = rule.split(": ")
            for rlist in rlists.split(" | "):
                data[rid].append(rlist.replace('"', "").split(" "))

        # Turns out the graph of rule ids is acyclic, which means we can recursively find all accepted words
        accepted = self.suffixes(data, "0", dict())

        return len(accepted.intersection(words.split("\n")))

    def suffixes(self, data, rid, cache):
        if rid in cache:
            return cache[rid]
        elif data[rid] == [["a"]]:
            cache[rid] = set("a")
            return cache[rid]
        elif data[rid] == [["b"]]:
            cache[rid] = set("b")
            return cache[rid]
        else:
            words: Set[str] = set()
            for subrule in data[rid]:
                subwords = set({""})
                for step in subrule:
                    subwords = {
                        subword + suffix
                        for subword in subwords
                        for suffix in self.suffixes(data, step, cache)
                    }
                words.update(subwords)
            cache[rid] = words
            return cache[rid]
