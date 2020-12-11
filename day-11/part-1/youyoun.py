from tool.runners.python import SubmissionPy

dirs = {(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)}


class YouyounSubmission(SubmissionPy):

    def run(self, s):
        adjacency = {}
        values = {}
        s = s.splitlines()
        for i, l in enumerate(s):
            for j, c in enumerate(l):
                values[i * 100 + j] = c
                adjacency[i * 100 + j] = set()
                for dx, dy in dirs:
                    adj = find_adjacent_seat(s, i, j, dx, dy)
                    if adj is not None:
                        adjacency[i * 100 + j].add(adj[0] * 100 + adj[1])
        while True:
            changed = {}
            counter = 0
            for pos, v in values.items():
                if v == '.':
                    continue
                adjacent_seats = adjacency[pos]
                if v == 'L':
                    free = 0
                    for adj in adjacent_seats:
                        adj_s = values[adj]
                        if adj_s == 'L':
                            free += 1
                    if free == len(adjacent_seats):
                        changed[pos] = '#'
                elif v == '#':
                    counter += 1
                    occupied = 0
                    for adj in adjacent_seats:
                        adj_s = values[adj]
                        if adj_s == '#':
                            occupied += 1
                    if occupied >= 4:
                        changed[pos] = 'L'
            if len(changed) == 0:
                break
            else:
                values.update(changed)
        return counter


def find_adjacent_seat(s, x, y, d_x, d_y):
    vis_x, vis_y = x + d_x, y + d_y
    if 0 <= vis_x <= len(s) - 1 and 0 <= vis_y <= len(s[0]) - 1 and s[vis_x][vis_y] != '.':
        return vis_x, vis_y
    else:
        return None


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
