cimport cython

DEF NOP = 0
DEF JMP = 1
DEF ACC = 2
DEF MAGIC_VALUE = 9999999

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
cpdef int run(str s):
    cdef int instructions[1000]
    cdef int value[1000]
    cdef bint free[1000]
    cdef int size = 0
    cdef str line
    for line in s.strip().splitlines():
        line_split = line.split(' ')
        if line_split[0] == 'nop':
            instructions[size] = NOP
        elif line_split[0] == 'jmp':
            instructions[size] = JMP
            value[size] = int(line_split[1])
        elif line_split[0] == 'acc':
            instructions[size] = ACC
            value[size] = int(line_split[1])
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
