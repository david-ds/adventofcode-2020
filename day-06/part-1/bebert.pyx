cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(str s):
    cdef int src_len = len(s)
    cdef int i

    cdef int counts[128]
    for i in range(97, 123):
        counts[i] = 0

    cdef int total = 0
    cdef bint last_b_n = False
    cdef unsigned char x
    for x in s.encode('utf-8'):
        if x == 10:
            if last_b_n:
                for i in range(97, 123):
                    if counts[i] > 0:
                        total += 1
                        counts[i] = 0
            last_b_n = True
        else:
            last_b_n = False
            counts[x] += 1

    for i in range(97, 123):
        if counts[i] > 0:
            total += 1

    return total
