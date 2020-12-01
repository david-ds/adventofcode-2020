cpdef long run(s):
    input_split = s.split("\n")
    cdef int input_len = len(input_split)
    cdef int numbers[250]

    cdef int i
    cdef str e
    for i, e in enumerate(input_split):
        numbers[i] = int(e)

    cdef int x
    cdef int y
    cdef int z
    for x in range(input_len):
        for y in range(input_len):
            if numbers[x] + numbers[y] > 2020:
                continue
            for z in range(input_len):
                if numbers[x] + numbers[y] + numbers[z] == 2020:
                    return numbers[x] * numbers[y] * numbers[z]
    return 0
