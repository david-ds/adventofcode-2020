cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
@cython.cdivision(True)     # Deactivate zero division check
cpdef long run(s):
    chunks1 = s.strip().split('\n\n')
    chunks2 = [c.replace('\n', ' ').split(' ') for c in chunks1]
    keys = [{k[:3] for k in c} for c in chunks2]
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    cdef int count = 0
    for k in keys:
        for r in required:
            if r not in k:
                break
        else:
            count += 1
    return count
