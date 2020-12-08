cimport cython

DEF NOP = 0
DEF JMP = 1
DEF ACC = 2
DEF MAGIC_VALUE = 9999999

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
cpdef int run(s: str):
    cdef char instructions[1000]
    cdef short value[1000]
    cdef bint free[1000]
    cdef int size = 0
    cdef str line
    for line in s.strip().splitlines():
        line_split = line.split(' ')
        if line_split[0] == 'nop':
            instructions[size] = NOP
        elif line_split[0] == 'jmp':
            instructions[size] = JMP
        elif line_split[0] == 'acc':
            instructions[size] = ACC
        value[size] = int(line_split[1])
        free[size] = True
        size += 1

    cdef int i = 0
    cdef int j = 0
    for i in range(size):
        if instructions[i] == NOP:
            instructions[i] = JMP
            res = run_program(instructions, value, free, size)
            instructions[i] = NOP
            for j in range(size):
                free[j] = True
            if res != MAGIC_VALUE:
                return res
        elif instructions[i] == JMP:
            instructions[i] = NOP
            res = run_program(instructions, value, free, size)
            instructions[i] = JMP
            for j in range(size):
                free[j] = True
            if res != MAGIC_VALUE:
                return res
    return 0


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
cdef int run_program(char* instructions, short* value, bint* free, int size):
    cdef int acc = 0
    cdef int c = 0
    while c < size and free[c]:
        free[c] = False
        if instructions[c] == NOP:
            c += 1
        elif instructions[c] == JMP:
            c += value[c]
        elif instructions[c] == ACC:
            acc += value[c]
            c += 1
    if c == size:
        return acc
    return MAGIC_VALUE
