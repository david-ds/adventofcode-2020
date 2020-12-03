cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef long run(s):
    trees = s.strip().splitlines()
    cdef int w = len(trees[0])
    cdef int h = len(trees)

    cdef int slopes_y[5]
    slopes_y[0] = 1
    slopes_y[1] = 1
    slopes_y[2] = 1
    slopes_y[3] = 1
    slopes_y[4] = 2

    cdef int slopes_x[5]
    slopes_x[0] = 1
    slopes_x[1] = 3
    slopes_x[2] = 5
    slopes_x[3] = 7
    slopes_x[4] = 1

    cdef long result = 1
    cdef int count = 0

    cdef int y
    cdef int i
    for i in range(5):
        count = 0
        for y in range(h):
            if y % slopes_y[i] == 0:
                count += 1 if trees[y][((y // slopes_y[i]) * slopes_x[i]) % w] == "#" else 0
        result *= count

    return result
