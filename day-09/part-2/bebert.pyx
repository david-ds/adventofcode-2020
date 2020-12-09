cimport cython

DEF WINDOW_SIZE = 25
DEF MAX_INPUT_LENGTH = 1100

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(str s):
    cdef long window[WINDOW_SIZE]
    cdef long values[MAX_INPUT_LENGTH]
    cdef long invalid = 0
    cdef int i, a, b
    cdef long current
    cdef str line
    cdef bint found

    cdef int input_size = 0
    for i, line in enumerate(s.strip().splitlines()):
        values[i] = int(line)
        input_size = i

    for i in range(input_size):
        current = values[i]
        if i < 25:
            window[i] = current
            continue
        found = False
        for a in range(24):
            for b in range(a + 1, 25):
                if window[a] != window[b] and window[a] + window[b] == current:
                    found = True
        if not found:
            invalid = current
            break
        window[i % 25] = current

    if invalid == 0:
        return 0

    cdef int da
    cdef long acc
    cdef long res_min
    cdef long res_max
    for a in range(input_size):
        current = values[a]
        da = 1
        acc = current
        while acc < invalid:
            acc += values[a + da]
            da += 1
        if acc == invalid:
            res_min = values[a]
            res_max = values[a]
            for i in range(a, a+da):
                if values[i] < res_min:
                    res_min = values[i]
                if values[i] > res_max:
                    res_max = values[i]
            return res_min + res_max
