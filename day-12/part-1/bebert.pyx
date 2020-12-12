cimport cython

DEF N = 0
DEF S = 1
DEF E = 2
DEF W = 3
DEF L = 4
DEF R = 5
DEF F = 6

# s1 = """F10
# N3
# F7
# R90
# F11
# """

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef int run(str s):
    # s = s1
    cdef int x = 0
    cdef int y = 0
    cdef char instruction
    cdef char orientation_x = 1
    cdef char orientation_y = 0
    cdef int value
    for line in s.strip().splitlines():
        instruction = "NSEWLRF".index(line[0])
        value = int(line[1:])
        if instruction == N:
            y += value
        elif instruction == S:
            y -= value
        elif instruction == E:
            x += value
        elif instruction == W:
            x -= value
        elif instruction == L:
            if value == 90:
                orientation_x, orientation_y = -orientation_y, orientation_x
            elif value == 180:
                orientation_x = -orientation_x
                orientation_y = -orientation_y
            elif value == 270:
                orientation_x, orientation_y = orientation_y, -orientation_x
        elif instruction == R:
            if value == 90:
                orientation_x, orientation_y = orientation_y, -orientation_x
            elif value == 180:
                orientation_x = -orientation_x
                orientation_y = -orientation_y
            elif value == 270:
                orientation_x, orientation_y = -orientation_y, orientation_x
        elif instruction == F:
            x += orientation_x * value
            y += orientation_y * value

    if x < 0:
        x = -x
    if y < 0:
        y = -y
    return x + y
