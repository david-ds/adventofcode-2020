from itertools import chain
from math import prod
from typing import List, Dict, Tuple

from tool.runners.python import SubmissionPy


class ThoreSubmission(SubmissionPy):
    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # parsing
        ranges, my_ticket, other_tickets = s.split("\n\n")
        self.valid_ranges = self.parse_ranges(ranges)
        my_ticket = self.parse_ints(my_ticket.splitlines()[1])
        other_tickets = set(map(self.parse_ints, other_tickets.splitlines()[1:]))

        # find field positions
        fields = self.valid_ranges.keys()
        self.possible_positions = {f: set(range(len(fields))) for f in fields}
        self.found = {}
        for ticket in other_tickets:
            if not self.is_valid_ticket(ticket):
                continue
            for position, value in enumerate(ticket):
                for field, ranges in self.valid_ranges.items():
                    if not any(x <= value <= y for x, y in ranges):
                        self.possible_positions[field].discard(position)
                        self.clear_positions(field)
        assert len(self.possible_positions) == 0

        # compute puzzle answer
        departure_indices = {
            idx for field, idx in self.found.items() if field.startswith("departure")
        }
        return prod(my_ticket[i] for i in departure_indices)

    def is_valid_ticket(self, ticket: List[int]) -> bool:
        for v in ticket:
            if not any(x <= v <= y for x, y in chain(*self.valid_ranges.values())):
                return False
        return True

    def clear_positions(self, field: str) -> None:
        """If the field has only one remaining possible position, remove it from
        the possible positions (including for other fields)"""
        if not len(self.possible_positions[field]) == 1:
            return

        field_pos = next(iter(self.possible_positions.pop(field)))
        self.found[field] = field_pos
        for other_field in list(self.possible_positions.keys()):
            self.possible_positions[other_field].discard(field_pos)
            self.clear_positions(other_field)

    @staticmethod
    def parse_ranges(ranges_str: str) -> Dict[str, List[Tuple[str]]]:
        ranges = {}
        for line in ranges_str.split("\n"):
            field, field_ranges = line.split(": ")
            ranges[field] = [
                tuple(map(int, lr.split("-"))) for lr in field_ranges.split(" or ")
            ]
        return ranges

    @staticmethod
    def parse_ints(s: str) -> Tuple[int]:
        return tuple(int(c) for c in s.split(","))