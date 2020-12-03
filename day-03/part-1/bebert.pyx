cpdef int run(s):
    trees = s.strip().splitlines()
    w = len(trees[0])
    h = len(trees)

    count = 0
    for y in range(h):
        count += 1 if trees[y][(y * 3) % w] == "#" else 0

    return count
