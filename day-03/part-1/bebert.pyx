cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(s):
    trees = s.strip().splitlines()
    cdef int w = len(trees[0])
    cdef int h = len(trees)

    cdef int count = 0
    cdef int y
    for y in range(h):
        count += 1 if trees[y][(y * 3) % w] == "#" else 0

    return count
