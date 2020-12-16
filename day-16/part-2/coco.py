from tool.runners.python import SubmissionPy
import numpy as np
from collections import Counter

class CocoSubmission(SubmissionPy):

    def is_valid(self, value, rule):
        _, ((minA, maxA), (minB, maxB)) = rule
        return minA <= value <= maxA or minB <= value <= maxB

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """

        #### PARSING
        rules, myticket, other_tickets = s.strip().split("\n\n")
        # parse rules
        rules = rules.split("\n")
        rules = [r.split(": ") for r in rules]
        for i, (name, values) in enumerate(rules):
            range1, range2 = values.split(" or ")
            range1 = range1.split("-")
            range1 = int(range1[0]), int(range1[1])
            range2 = range2.split("-")
            range2 = int(range2[0]), int(range2[1])
            rules[i] = (name, (range1, range2))
        

        myticket = myticket.split("\n")[1].split(",")
        myticket = [int(n) for n in myticket]
        other_tickets = other_tickets.split("\n")[1:]
        other_tickets = [list(map(int, t.split(","))) for t in other_tickets]

        valid_tickets = []

        for ticket in other_tickets:
            ticket_is_valid = True
            for val in ticket:
                if all(not self.is_valid(val, r) for r in rules):
                    ticket_is_valid = False
                    break
            if ticket_is_valid:
                valid_tickets.append(ticket)

        num_fields = len(rules)

        applicable_fields_for_rule = [set(range(num_fields)) for _ in range(num_fields)]
        for rule_id, r in enumerate(rules):
            for field_id in range(num_fields):
                values = [ticket[field_id] for ticket in valid_tickets]
                if any(not self.is_valid(v, r) for v in values):
                    applicable_fields_for_rule[rule_id].remove(field_id)

        # start to pick rules that have few possibilities
        rule_ids = sorted(list(range(num_fields)), key=lambda rule_id: len(applicable_fields_for_rule[rule_id]))
        field_for_rule = [-1]*(num_fields)

        # print(applicable_fields_for_rule)
        for rule_id in rule_ids:
            print(len(applicable_fields_for_rule[rule_id]))
            field_id = list(applicable_fields_for_rule[rule_id])[0]
            field_for_rule[rule_id] = field_id
            # remove it from other places
            for rid2 in rule_ids:
                applicable_fields_for_rule[rid2].discard(field_id)

        print(field_for_rule)
        RULE_IDS_DEPARTURES = list(range(6))
        result = 1
        for rule_id in RULE_IDS_DEPARTURES:
            field_id = field_for_rule[rule_id]
            result *= myticket[field_id]
        return result


def test_coco():
    input = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    assert CocoSubmission().run(input) ==  11*12*13