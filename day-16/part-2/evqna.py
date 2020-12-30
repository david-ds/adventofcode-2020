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
    
    def completely_invalid(self, fields, field_constraints):
        for val in fields:
            if not any(self.check_constraints(val, constraints) for constraints in field_constraints.values()):
                return True
        return False
    
    def find_compatible_fields_per_column(self, tickets, field_constraints):
        # Group values by column        
        column_values = [set() for _ in range(len(field_constraints))]          # [{values} (idx=column_id)]
        for ticket in tickets:
            fields = [int(c) for c in ticket.split(',')]
            if not self.completely_invalid(fields, field_constraints):
                for i, x in enumerate(fields):
                    column_values[i].add(x)
        
        # List compatible fields per column
        column_to_field_set = {}    # {column_id: {field_name}}
        for i, X in enumerate(column_values):
            field_set = set()
            for field in field_constraints:
                if all(self.check_constraints(x, field_constraints[field]) for x in X):
                    field_set.add(field)
            column_to_field_set[i] = field_set
        return column_to_field_set
    
    def map_fields(self, field_constraints, tickets):
        column_to_field_set = self.find_compatible_fields_per_column(tickets, field_constraints)

        # Find columns with only one possible field, then proceed by elimination to build a complete mapping
        # This is not guaranteed to work in theory, but should work on all actual problem input
        field_mapping = {}  # {field_name: column_id}

        # Optimization: iterate over columns in ascending length of compatible fields to build mappings in one go
        for column in sorted(column_to_field_set, key=lambda c: len(column_to_field_set[c])):
            unmapped_fields = column_to_field_set[column] - field_mapping.keys()
            if len(unmapped_fields) == 1:
                field = unmapped_fields.pop()
                field_mapping[field] = column
        # Verify that all mappings were built (assumes the input has 'nice' properties)
        assert len(field_mapping) == len(field_constraints)

        return field_mapping

    def run(self, s):
        constraints, ticket, nearby_tickets = s.split('\n\n')
        constraints = constraints.splitlines()
        _, ticket = ticket.splitlines()
        _, *nearby_tickets = nearby_tickets.splitlines()

        field_constraints = self.parse_constraints(constraints)
        field_mapping = self.map_fields(field_constraints, nearby_tickets)

        result = 1
        fields = [int(c) for c in ticket.split(',')]
        for field_name, col in field_mapping.items():
            if field_name.startswith('departure'):
                result *= fields[col]
        return result
