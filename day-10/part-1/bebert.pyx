cimport cython

DEF MAX_ADAPTER = 256

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(s):
    cdef bint adapters[MAX_ADAPTER]

    cdef int i
    for i in range(MAX_ADAPTER):
        adapters[i] = 0

    cdef int max_adapters = 0
    cdef int adapter
    cdef str line
    for line in s.strip().splitlines():
        adapter = int(line)
        adapters[adapter] = 1
        if adapter > max_adapters:
            max_adapters = adapter

    cdef int counts[5]
    for i in range(5):
        counts[i] = 0

    cdef int diff = 0
    for i in range(1, max_adapters + 1):
        diff += 1
        if adapters[i]:
            counts[diff] += 1
            diff = 0
    counts[3] += 1
    return counts[1] * counts[3]
