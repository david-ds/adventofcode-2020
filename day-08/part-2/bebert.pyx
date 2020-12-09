cimport cython

DEF NOP = 0
DEF JMP = 1
DEF ACC = 2
DEF MAX_INPUT_LEN = 800
DEF MAGIC_VALUE = 9999999

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
cpdef int run(str s):
    cdef char instructions[MAX_INPUT_LEN]
    cdef short value[MAX_INPUT_LEN]
    cdef bint free[MAX_INPUT_LEN]
    cdef int size = 0
    cdef str line
    cdef str instruction_str
    for line in s.strip().splitlines():
        instruction_str = line[:3]
        if instruction_str == 'nop':
            instructions[size] = NOP
        elif instruction_str == 'jmp':
            instructions[size] = JMP
        elif instruction_str == 'acc':
            instructions[size] = ACC
        value[size] = int(line[4:])
        free[size] = True
        size += 1

    cdef int i = 0
    cdef int j = 0
    for i in range(size):
        if instructions[i] == NOP:
            instructions[i] = JMP
            res = run_program(instructions, value, free, size)
            if res != MAGIC_VALUE:
                return res
            instructions[i] = NOP
            for j in range(size):
                free[j] = True
        elif instructions[i] == JMP:
            instructions[i] = NOP
            res = run_program(instructions, value, free, size)
            if res != MAGIC_VALUE:
                return res
            instructions[i] = JMP
            for j in range(size):
                free[j] = True
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
