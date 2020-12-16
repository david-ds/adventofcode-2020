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
        # Your code goes here

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
            for val in ticket:
                if any(self.is_valid(val, r) for r in rules):
                    valid_tickets.append(ticket)
        
        # apply greedy procedure. 
        # For each field, put it in the place where it has maximum validity.
        # To do this, we construct a matrix containing the number of valid values for each rule and field id.

        num_fields = len(rules)
        validity_matrix = [[0 for _ in range(num_fields)] for _ in range(num_fields)]

        for rule_id, r in enumerate(rules):
            for field_id in range(num_fields):
                values = [ticket[field_id] for ticket in valid_tickets]
                num_valid = sum(1 for v in values if self.is_valid(v, r))
                validity_matrix[rule_id][field_id] = num_valid

        validity_matrix = np.array(validity_matrix)

        while True:
            indexes = np.argmax(validity_matrix)
            np.max()
            breakpoint()

        # indexes np.argmax(validity_matrix)
        # field_for_rule = []
        # for rule_id in range(num_fields):
        #     # pick best field
        #     field_values = validity_matrix[rule_id]
        #     best_field = np.argmax(field_values)
        #     if Counter(field_values)[field_values[best_field]] > 1:
        #         print("two choices")
        #         # breakpoint()
        #     field_for_rule.append(best_field)
        #     # put -1 to discard field
        #     for rid in range(num_fields):
        #         validity_matrix[rid][best_field] = -1

        print(field_for_rule)
        RULE_IDS_DEPARTURES = list(range(6))
        result = 1
        for rule_id in RULE_IDS_DEPARTURES:
            field_id = field_for_rule[rule_id]
            result *= myticket[field_id]
        return result
