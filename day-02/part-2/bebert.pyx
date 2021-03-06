cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
cpdef int run(s):
    cdef int constraint_min
    cdef int constraint_max
    cdef str letter
    cdef str password

    cdef int valid = 0
    cdef int count = 0

    cdef str line
    for line in s.splitlines():
        if not line.strip():
            continue
        split1 = line.strip().split(": ")
        password = split1[1]
        split2 = split1[0].split(" ")
        letter = split2[1]
        split3 = split2[0].split("-")
        constraint_min = int(split3[0])
        constraint_max = int(split3[1])

        count = 0
        if password[constraint_min - 1] == letter:
            count += 1
        if password[constraint_max - 1] == letter:
            count += 1
        if count == 1:
            valid += 1

    return valid
