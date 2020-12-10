cimport cython

DEF MAX_ADAPTER = 256

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef long run(s):
    cdef bint adapters[MAX_ADAPTER]

    cdef int i
    adapters[0] = 1
    for i in range(1, MAX_ADAPTER):
        adapters[i] = 0

    cdef int max_adapters = 0
    cdef int adapter
    cdef str line
    for line in s.strip().splitlines():
        adapter = int(line)
        adapters[adapter] = 1
        if adapter > max_adapters:
            max_adapters = adapter

    cdef int streaks[8]
    for i in range(8):
        streaks[i] = 0

    cdef int streak = 0
    for i in range(max_adapters + 2):
        if adapters[i]:
            streak += 1
        else:
            streaks[streak] += 1
            streak = 0

    cdef int multipliers[7]  # compté à la main lol
    multipliers[0] = 0
    multipliers[1] = 1
    multipliers[2] = 1
    multipliers[3] = 2
    multipliers[4] = 4
    multipliers[5] = 7
    multipliers[6] = 13

    cdef long res = 1
    cdef int n
    for i in range(3, 7):
        for n in range(streaks[i]):
            res *= multipliers[i]

    return res
