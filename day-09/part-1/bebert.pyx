cimport cython

DEF WINDOW_SIZE = 25

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(str s):
    cdef long window[WINDOW_SIZE]
    cdef int i, a, b
    cdef long current
    cdef str line
    cdef bint found
    for i, line in enumerate(s.strip().splitlines()):
        current = int(line)
        if i < WINDOW_SIZE:
            window[i] = current
            continue
        found = False
        for a in range(24):
            for b in range(a+1, 25):
                if window[a] != window[b] and window[a] + window[b] == current:
                    found = True
        if not found:
            return current
        window[i % 25] = current
