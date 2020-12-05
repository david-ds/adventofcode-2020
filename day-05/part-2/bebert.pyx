cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(s):
    cdef int seat_id = 0
    cdef int i
    cdef str line
    cdef int f
    cdef int b
    cdef int y

    cdef bint seat_ids[1024]
    for i in range(1024):
        seat_ids[i] = 0

    for line in s.strip().splitlines():
        f = 0
        b = 127
        for i in range(7):
            if line[i] == 'F':
                b = f + (b - f - 1) // 2
            else:
                f += (b - f + 1) // 2
        y = b

        f = 0
        b = 7
        for i in range(7, 10):
            if line[i] == 'L':
                b = f + (b - f - 1) // 2
            else:
                f += (b - f + 1) // 2

        seat_id = y * 8 + b
        seat_ids[seat_id] = 1

    for i in range(1, 1023):
        if seat_ids[i] == 0 and seat_ids[i-1] == 1 and seat_ids[i+1] == 1:
            return i

    return -1
