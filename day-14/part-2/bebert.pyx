cimport cython

DEF MASK_IGNORE = 2

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef long run(s):
    cdef str line
    cdef str x
    cdef int i
    cdef char mask[36]
    cdef int address
    cdef long number

    cdef dict memory = {}

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
            address = int(parts[0][4:])
            number = int(parts[1])
            apply_operation(memory, mask, address, number)

    cdef long res = 0
    cdef long v
    for v in memory.values():
        res += v

    return res

cdef void apply_operation(dict memory, char *mask, long address, long number):
    # print('address:', address)
    # print('number:', number)

    cdef char result[36]
    cdef int i
    for i in range(36):
        if mask[35 - i] == 0:
            result[35 - i] = address % 2
        elif mask[35 - i] == 1:
            result[35 - i] = 1
        elif mask[35 - i] == MASK_IGNORE:
            result[35 - i] = MASK_IGNORE
        address //= 2

    # mask_str = ''
    # for i in range(36):
    #     mask_str += '01X'[mask[i]]
    # print('mask   :', mask_str)

    # result_str = ''
    # for i in range(36):
    #     result_str += '01X'[result[i]]
    # print('result :', result_str)

    rec_worker(memory, result, number)

cdef void rec_worker(memory, char *result, long number):
    cdef long res = 0
    cdef int i
    cdef long power = 1
    for i in range(36):
        if result[35 - i] == 0:
            pass
        elif result[35 - i] == 1:
            res += power
        elif result[35 - i] == MASK_IGNORE:
            result[35 - i] = 0
            rec_worker(memory, result, number)
            result[35 - i] = 1
            rec_worker(memory, result, number)
            result[35 - i] = MASK_IGNORE
            return
        power *= 2

    # result_str = ''
    # for i in range(36):
    #     result_str += '01X'[result[i]]
    # print('result_:', result_str, '=>', "mem[", res, "] <-", number)

    memory[res] = number
