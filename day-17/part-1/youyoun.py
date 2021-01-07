from tool.runners.python import SubmissionPy


class YouyounSubmission(SubmissionPy):
    def run(self, s):
        neighbours_mem = {}

        def get_neighbours(coords):
            if coords in neighbours_mem:
                return neighbours_mem[coords]
            neighbours = []
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        neighbours.append((coords[0] + i - 1, coords[1] + j - 1, coords[2] + k - 1))
            neighbours_mem[coords] = neighbours
            return neighbours

        active_points = set()
        n_cycles = 6
        s = s.splitlines()
        for j, l in enumerate(s):
            for i, c in enumerate(l):
                if c == '#':
                    active_points.add((i, j, 0))
        for _ in range(n_cycles):
            to_process_points = set()
            to_remove = set()
            to_add = set()
            for p in active_points:
                for n in get_neighbours(p):
                    to_process_points.add(n)
            for p in to_process_points:
                n_active = 0
                for n in get_neighbours(p):
                    n_active += int(n in active_points)
                    if n_active > 4:
                        break
                if p in active_points:
                    if n_active < 3 or n_active > 4:
                        to_remove.add(p)
                else:
                    if n_active == 3:
                        to_add.add(p)
            active_points = (active_points - to_remove).union(to_add)
        return len(active_points)


if __name__ == '__main__':
    print(YouyounSubmission().run(open('../input/youyoun.txt').read()))
