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
            value[size] = int(line[4:])
        elif instruction_str == 'acc':
            instructions[size] = ACC
            value[size] = int(line[4:])
        free[size] = True
        size += 1

    cdef int acc = 0
    cdef int c = 0
    while free[c]:
        free[c] = False
        if instructions[c] == NOP:
            c += 1
        elif instructions[c] == JMP:
            c += value[c]
        elif instructions[c] == ACC:
            acc += value[c]
            c += 1
        else:
            return MAGIC_VALUE
    return acc
