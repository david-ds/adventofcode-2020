from tool.runners.python import SubmissionPy

from collections import defaultdict
from functools import lru_cache
from textwrap import wrap


class BadouralixSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # We need a class attribute here to pass it to the match method and still benefit from the cache
        self.rules = defaultdict(list)
        result = 0

        metadata, words = s.split("\n\n")

        for rule in metadata.split("\n"):
            rid, rlists = rule.split(": ")
            for rlist in rlists.split(" | "):
                self.rules[rid].append(rlist.replace('"', "").split(" "))

        # Now we cannot really exhaustively enumerate all accepted words
        # Nor can we build a finite automaton to recognize the language
        # We have 0 = 8 11 = (42 | 42 8) (42 31 | 42 11 31) = 42+ 42...42 31...31 ( same number of 42 and 31 in the second part )
        # Accepted words look like "m words recognized by 42 then n words recognized by 31, where m is strictly greater than n"
        # Lucky us, all words recognized by 42 or 31 are exactly 8 character long
        # At this point we do not try to be fancy with a pushdown automaton, we just try all possible values for n
        for word in words.split("\n"):
            subwords = wrap(word, 8)
            for n in range(1, (len(subwords) - 1) // 2 + 1):
                if all(
                    self.match(subword, "42") == len(subword)
                    for subword in subwords[:-n]
                ) and all(
                    self.match(subword, "31") == len(subword)
                    for subword in subwords[-n:]
                ):
                    result += 1
                    break

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
