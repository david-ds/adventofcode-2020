cimport cython

DEF MASK_IGNORE = 2
DEF MEMORY_SIZE = 65536

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef long run(s):
    cdef str line
    cdef str x
    cdef int i
    cdef char mask[36]
    cdef int index
    cdef long number

    # cdef long memory[MEMORY_SIZE]
    # for i in range(MEMORY_SIZE):
    #     memory[i] = 0

    memory = {}

    for line in s.strip().splitlines():
        if line[1] == "a":
            # mask = 011X1X00X100100XXXX11100X0000100X010
            for i, x in enumerate(line.split(" = ")[1]):
                if x == "0":
                    mask[i] = 0
                elif x == "1":
                    mask[i] = 1
                elif x == "X":
                    mask[i] = MASK_IGNORE
        else:
            # mem[54837] = 244218
            parts = line.split("] = ")
            index = int(parts[0][4:])
            number = int(parts[1])
            # print("[", index, "]", number, "->", apply_mask(mask, number))
            memory[index] = apply_mask(mask, number)

    # cdef long res = 0
    # for i in range(MEMORY_SIZE):
    #     res += memory[i]

    cdef long res = 0
    cdef long v
    for v in memory.values():
        res += v

    return res

cdef long apply_mask(char *mask, long number):
    cdef long res = 0
    cdef long power = 1
    cdef int i
    for i in range(36):
        if mask[35 - i] == 1 or mask[35 - i] == MASK_IGNORE and number % 2 == 1:
            res += power
        number //= 2
        power *= 2
    return res
