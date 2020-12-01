cpdef int run(s):
    cdef bint numbers[2021]

    cdef int i
    for i in range(2021):
        numbers[i] = 0

    cdef str x
    cdef int current
    for x in s.split("\n"):
        current = int(x)
        if numbers[2020 - current]:
            return current * (2020 - current)
        numbers[current] = 1
    return 0
