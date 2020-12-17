cimport cython

import numpy as np
cimport numpy as np

DEF NB_STEPS = 30000000

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
cpdef int run(s):
    cdef np.ndarray memory_np = np.zeros(NB_STEPS, dtype=np.intc)
    cdef int[:] memory = memory_np

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
