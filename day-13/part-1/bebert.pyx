cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef int run(str s):
    s0, s1 = s.strip().splitlines()
    cdef int arrival = int(s0)
    cdef int min_waiting = arrival
    cdef int min_bus_id = 0
    cdef str b0
    cdef int bus_id
    cdef int next_bus
    cdef int bus_wait
    for b0 in s1.split(','):
        if b0 == 'x':
            continue
        bus_id = int(b0)
        next_bus = (arrival + bus_id) - (arrival + bus_id) % bus_id
        bus_wait = next_bus - arrival
        if bus_wait < min_waiting:
            min_waiting = bus_wait
            min_bus_id = bus_id
    return min_bus_id * min_waiting
