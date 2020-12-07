from collections import defaultdict
from typing import Set

from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        is_inside = defaultdict(list)
        for line in s.strip().splitlines():
            color, contains_raw = line.split(' bags contain ')
            for c in contains_raw.split(', '):
                parts = c.split(' ')
                if parts[0] == 'no':
                    continue
                sub_color = ' '.join(parts[1:-1])
                is_inside[sub_color].append(color)

        return len(self.fill_can_be_included_in(is_inside, 'shiny gold', set())) - 1

    def fill_can_be_included_in(self, is_inside, color, acc: Set[str]) -> Set[str]:
        acc.add(color)
        for c in is_inside[color]:
            if c not in acc:
                self.fill_can_be_included_in(is_inside, c, acc)
        return acc
