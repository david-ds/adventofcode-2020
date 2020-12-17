cimport cython

DEF NB_STEPS = 2020

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
cpdef int run(s):
    cdef int memory[NB_STEPS]
    cdef int i
    for i in range(NB_STEPS):
        memory[i] = 0

    cdef int step = 0
    cdef int old_mem = 0
    cdef int cur = 0

    cdef str x
    for x in s.strip().split(','):
        step += 1
        cur = int(x)
        old_mem = memory[cur]
        memory[cur] = step

    while step < NB_STEPS:
        step += 1
        cur = 0 if old_mem == 0 else step - 1 - old_mem
        old_mem = memory[cur]
        memory[cur] = step

    return cur
