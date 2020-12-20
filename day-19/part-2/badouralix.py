from tool.runners.python import SubmissionPy

from collections import defaultdict
from textwrap import wrap
from typing import Set


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        rules, words = s.split("\n\n")
        data = defaultdict(list)
        result = 0

        for rule in rules.split("\n"):
            rid, rlists = rule.split(": ")
            for rlist in rlists.split(" | "):
                data[rid].append(rlist.replace('"', "").split(" "))

        # Now we cannot really exhaustively enumerate all accepted words
        # Nor can we build a finite automaton to recognize the language
        # We have 0 = 8 11 = (42 | 42 8) (42 31 | 42 11 31) = 42+ 42...42 31...31 ( same number of 42 and 31 in the second part )
        # Accepted words look like "m words recognized by 42 then n words recognized by 31, where m is strictly greater than n"
        cache = dict()
        self.suffixes(data, "0", cache)

        # Lucky us, all words recognized by 42 or 31 are exactly 8 character long
        # At this point we do not try to be fancy with a pushdown automaton, we just try all possible values for n
        for word in words.split("\n"):
            subwords = wrap(word, 8)
            for n in range(1, (len(subwords) - 1) // 2 + 1):
                if (
                    set(subwords[:-n]) <= cache["42"]
                    and set(subwords[-n:]) <= cache["31"]
                ):
                    result += 1
                    break

        return result

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
