cpdef long run(s):
    trees = s.strip().splitlines()
    h = len(trees)
    w = len(trees[0])

    result = 1
    for slope in [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]:
        count = 0
        for y in range(h):
            if y % slope[0] == 0:
                count += 1 if trees[y][((y // slope[0]) * slope[1]) % w] == "#" else 0
        result *= count

    return result
