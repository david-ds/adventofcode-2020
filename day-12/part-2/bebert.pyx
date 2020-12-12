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
    cdef char waypoint_x = 10
    cdef char waypoint_y = 1
    cdef int value
    for line in s.strip().splitlines():
        instruction = "NSEWLRF".index(line[0])
        value = int(line[1:])
        if instruction == N:
            waypoint_y += value
        elif instruction == S:
            waypoint_y -= value
        elif instruction == E:
            waypoint_x += value
        elif instruction == W:
            waypoint_x -= value
        elif instruction == L:
            if value == 90:
                waypoint_x, waypoint_y = -waypoint_y, waypoint_x
            elif value == 180:
                waypoint_x = -waypoint_x
                waypoint_y = -waypoint_y
            elif value == 270:
                waypoint_x, waypoint_y = waypoint_y, -waypoint_x
        elif instruction == R:
            if value == 90:
                waypoint_x, waypoint_y = waypoint_y, -waypoint_x
            elif value == 180:
                waypoint_x = -waypoint_x
                waypoint_y = -waypoint_y
            elif value == 270:
                waypoint_x, waypoint_y = -waypoint_y, waypoint_x
        elif instruction == F:
            x += waypoint_x * value
            y += waypoint_y * value

    if x < 0:
        x = -x
    if y < 0:
        y = -y
    return x + y
