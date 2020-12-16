from tool.runners.python import SubmissionPy

from collections import defaultdict
from queue import Queue
from typing import DefaultDict, List, Set, Tuple, Union


class BadouralixSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        fields: Set[str] = set()  # Set of all existing fields
        mapping: List[Set[str]] = list()  # List of possible field per position
        queue: Queue = Queue()  # Work queue for the mapping reduction
        result: int = 1  # Result temporary variable
        rules: DefaultDict[str, Set[int]] = defaultdict(
            set
        )  # Hashmap between fields and valid values
        stage: str = "rules"  # Type of line when parsing the input file
        ticket: Tuple[int, ...]  # All values of our ticket
        valid: List[Tuple[int, ...]] = list()  # All nearby tickets that are valid

        # Parse input line by line
        for line in s.split("\n"):
            # Deal with section delimiters first
            if line == "":
                continue
            elif line == "your ticket:":
                stage = "ours"
                continue
            elif line == "nearby tickets:":
                stage = "theirs"
                continue

            # Update rules hashmap in "rules" stage
            if stage == "rules":
                field, ranges = line.split(": ")
                fields.add(field)
                for r in ranges.split(" or "):
                    m, n = r.split("-")
                    expanded = range(int(m), int(n) + 1)
                    rules[field].update(expanded)
                    rules["all"].update(expanded)
            # Update ticket in "ours" stage
            elif stage == "ours":
                ticket = tuple(map(int, line.split(",")))
            # Exclude invalid tickets in "theirs" stage
            elif stage == "theirs":
                t = tuple(map(int, line.split(",")))
                for v in t:
                    if v not in rules["all"]:
                        break
                else:
                    valid.append(t)

        # Initialize mapping by assuming all fields can be at all positions
        # Also enqueue all positions for later reducing
        for i in range(len(ticket)):
            mapping.append(fields.copy())
            queue.put(i)

        # Remove for each position fields that have at least one incompatible ticket
        for t in valid:
            for i in range(len(t)):
                for field in mapping[i].copy():
                    if t[i] not in rules[field]:
                        mapping[i].remove(field)

        # Reduce mapping using positions that have only one compatible field
        # More precisely, if a field is the only compatible field for a given position, this field becomes incompatible in all other positions
        while not queue.empty():
            i = queue.get()
            if len(mapping[i]) != 1:
                continue

            field = next(iter(mapping[i]))
            for j in range(len(mapping)):
                if i != j and field in mapping[j]:
                    mapping[j].remove(field)
                    queue.put(j)

        # Yolo assume we found a perfect match, i.e. there is only one compatible field per position
        for i in range(len(mapping)):
            if next(iter(mapping[i])).startswith("departure"):
                result *= ticket[i]

        return result
