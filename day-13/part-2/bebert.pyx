cimport cython

DEF MAX_LANES = 16

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef long run(str s):
    cdef str s1 = s.strip().splitlines()[1]
    cdef int i
    cdef str b0
    cdef int bus_ids[MAX_LANES]
    cdef int offsets[MAX_LANES]
    cdef int nb_lanes = 0
    for i, b0 in enumerate(s1.split(',')):
        if b0 == 'x':
            continue
        bus_ids[nb_lanes] = int(b0)
        offsets[nb_lanes] = i
        nb_lanes += 1

    cdef long jump = bus_ids[0]
    cdef int reach = 2
    cdef bint valid = True
    cdef long cur = 0
    cdef long res = 0
    while not res:
        # print('--- cur:', cur, 'jump', jump, 'reach', reach, 'trying to add', bus_ids[reach-1])
        valid = True
        for i in range(reach):
            if (cur + offsets[i]) % bus_ids[i] != 0:
                # print(f'({cur} + {offsets[i]}) % {bus_ids[i]} ==', (cur + offsets[i]) % bus_ids[i])
                valid = False
                break
        if valid:
            # print('Found solution for reach', reach, ':', cur)
            jump *= bus_ids[reach - 1]
            if reach == nb_lanes:
                res = cur
                break
            reach += 1
        cur += jump

    return res
