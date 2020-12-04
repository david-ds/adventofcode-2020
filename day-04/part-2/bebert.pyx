cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.cdivision(True)     # Deactivate zero division check
cpdef int run(s):
    chunks1 = s.strip().split('\n\n')
    chunks2 = [c.replace('\n', ' ').split(' ') for c in chunks1]
    keys = [{k[:3]: k[4:] for k in c} for c in chunks2]
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    numbers = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    hex_chars = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'}
    eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

    cdef int count = 0
    cdef bint invalid
    cdef int byr
    cdef int iyr
    cdef int eyr
    cdef int hgt
    cdef str hcl
    cdef str cc
    for k in keys:
        invalid = False

        for r in required:
            if r not in k:
                invalid = True
                break
        if invalid:
            continue

        byr = int(k['byr'])
        if byr < 1920 or byr > 2002:
            continue

        iyr = int(k['iyr'])
        if iyr < 2010 or iyr > 2020:
            continue

        eyr = int(k['eyr'])
        if eyr < 2020 or eyr > 2030:
            continue

        if k['hgt'][-2:] == 'in':
            hgt = int(k['hgt'][:-2])
            if hgt < 59 or hgt > 76:
                continue
        elif k['hgt'][-2:] == 'cm':
            hgt = int(k['hgt'][:-2])
            if hgt < 150 or hgt > 193:
                continue
        else:
            continue

        if k['hcl'][0] != '#' or len(k['hcl']) != 7:
            continue

        hcl = k['hcl']
        for i in range(1, 7):
            if hcl[i] not in hex_chars:
                invalid = True
                break
        if invalid:
            continue

        if k['ecl'] not in eye_colors:
            continue

        if len(k['pid']) != 9:
            continue

        for cc in k['pid']:
            if cc not in numbers:
                invalid = True
                break
        if invalid:
            continue

        count += 1

    return count
