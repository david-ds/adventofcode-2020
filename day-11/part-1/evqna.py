from tool.runners.python import SubmissionPy

FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

class EvqnaSubmission(SubmissionPy):

    def adjacent_seats(self, x, y, floor):
        deltas = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        seats = []
        for d_x, d_y in deltas:
            x2, y2 = x + d_x, y + d_y
            if 0 <= y2 < len(floor) and 0 <= x2 < len(floor[y2]):
                seats.append((x2, y2))
        return seats
    
    def precompute_lookups(self, floor):
        seat_lookup = {}
        for y in range(len(floor)):
            for x in range(len(floor[y])):
                seat_lookup[(x,y)] = self.adjacent_seats(x, y, floor)
        return seat_lookup
    
    def next_state(self, state, seat_lookup):
        new_state = []
        changes = False
        for y, row in enumerate(state):
            new_row = row[:]
            for x, c in enumerate(row):
                if c != FLOOR:
                    occupied = sum(1 for x2, y2 in seat_lookup[(x,y)] if state[y2][x2] == OCCUPIED)
                    if c == EMPTY and occupied == 0:
                        new_row[x] = OCCUPIED
                        changes = True
                    elif c == OCCUPIED and occupied >= 4:
                        new_row[x] = EMPTY
                        changes = True
            new_state.append(new_row)
        return new_state, not changes
    
    def count_occupied(self, state):
        count = 0
        for row in state:
            for c in row:
                if c == OCCUPIED:
                    count += 1
        return count

    def run(self, s):
        floor = s.splitlines()
        seat_lookup = self.precompute_lookups(floor)

        # Convert strings to list for easier mutation
        state = [list(line) for line in floor]

        done = False
        while not done:
            state, done = self.next_state(state, seat_lookup)
        return self.count_occupied(state)
