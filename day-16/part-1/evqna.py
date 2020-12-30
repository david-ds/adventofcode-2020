from tool.runners.python import SubmissionPy

from collections import defaultdict

class EvqnaSubmission(SubmissionPy):
    def parse_constraints(self, constraints):
        field_constraints = defaultdict(list)
        for line in constraints:
            field_name, ranges = line.split(': ')
            for range in ranges.split(' or '):
                a, b = range.split('-')
                field_constraints[field_name].append((int(a), int(b)))
        return field_constraints
    
    def check_constraints(self, value, constraints):
        for a, b in constraints:
            if a <= value <= b:
                return True
        return False
    
    def completely_invalid_fields(self, ticket, field_constraints):
        invalid_values = 0
        for val in ticket.split(','):
            val = int(val)
            if not any(self.check_constraints(val, constraints) for constraints in field_constraints.values()):
                invalid_values += val
        return invalid_values

    def run(self, s):
        constraints, ticket, nearby_tickets = s.split('\n\n')
        constraints = constraints.splitlines()
        _, ticket = ticket.splitlines()
        _, *nearby_tickets = nearby_tickets.splitlines()

        field_constraints = self.parse_constraints(constraints)

        invalid_sum = 0
        for ticket in nearby_tickets:
            invalid_sum += self.completely_invalid_fields(ticket, field_constraints)
        return invalid_sum
