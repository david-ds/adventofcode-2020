from tool.runners.python import SubmissionPy


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
        other_tickets = other_tickets.split("\n")[1:]
        other_tickets = [list(map(int, t.split(","))) for t in other_tickets]

        sum_invalid_values = 0
        for ticket in other_tickets:
            for val in ticket:
                if all(not self.is_valid(val, r) for r in rules):
                    sum_invalid_values += val
        return sum_invalid_values
