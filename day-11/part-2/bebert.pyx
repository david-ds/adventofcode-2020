cimport cython

DEF FLOOR = 0
DEF EMPTY = 1
DEF TAKEN = 2
DEF INPUT_SIZE = 100000

# cdef void print_grid(char*grid, int w, int h):
#     cdef i = 0
#     cdef str s
#     for i in range(h):
#         s = ''
#         for j in range(w):
#             s += '.L#'[grid[i * w + j]]
#         print(s)
#     print('')
#
# s1 = """L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# """
#
# s2 = """LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# LLLLLLLLLL
# """

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cpdef int run(s):
    # s = s1
    cdef char grid[INPUT_SIZE]
    cdef char grid_old[INPUT_SIZE]
    cdef int w = 0
    cdef int h = 0
    cdef int i = 0
    cdef int j = 0
    cdef int x = 0
    cdef int c = 0
    cdef str a
    for i, line in enumerate(s.strip().splitlines()):
        w = len(line)
        h += 1
        for j, a in enumerate(line):
            if a == '.':
                grid[i * w + j] = FLOOR
            else:
                grid[i * w + j] = EMPTY

    # LOOPY DOOP
    # cdef int step_debug = 0
    cdef bint moving = True
    while moving:
        # step_debug += 1
        # if step_debug > 5000:
        #     print("BREAAAAAAAAAAAK")
        #     break
        # print('--- step', step_debug, '---', 'w', w, 'h', h)
        # print_grid(grid, w, h)

        moving = False

        # copy in old
        for x in range(h * w):
            grid_old[x] = grid[x]

        # one step
        for x in range(h * w):
            # if x == 80:
            #     print('x ==', x)
            #     print('.L#'[ray_n(grid_old, x, w, h)])
            #     print('.L#'[ray_ne(grid_old, x, w, h)])
            #     print('.L#'[ray_e(grid_old, x, w, h)])
            #     print('.L#'[ray_se(grid_old, x, w, h)])
            #     print('.L#'[ray_s(grid_old, x, w, h)])
            #     print('.L#'[ray_sw(grid_old, x, w, h)])
            #     print('.L#'[ray_w(grid_old, x, w, h)])
            #     print('.L#'[ray_nw(grid_old, x, w, h)])

            j = x % w
            if (
                    grid_old[x] == EMPTY
                    and ray_n(grid_old, x, w, h) != TAKEN
                    and ray_s(grid_old, x, w, h) != TAKEN
                    and ray_w(grid_old, x, w, h) != TAKEN
                    and ray_e(grid_old, x, w, h) != TAKEN
                    and ray_nw(grid_old, x, w, h) != TAKEN
                    and ray_ne(grid_old, x, w, h) != TAKEN
                    and ray_sw(grid_old, x, w, h) != TAKEN
                    and ray_se(grid_old, x, w, h) != TAKEN
            ):
                grid[x] = TAKEN
                moving = True
            elif grid_old[x] == TAKEN:
                c = 0
                if ray_n(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_s(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_w(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_e(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_nw(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_ne(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_sw(grid_old, x, w, h) == TAKEN:
                    c += 1
                if ray_se(grid_old, x, w, h) == TAKEN:
                    c += 1

                if c >= 5:
                    grid[x] = EMPTY
                    moving = True

    # count taken
    cdef int res = 0
    for x in range(h * w):
        if grid[x] == TAKEN:
            res += 1

    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_n(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps = x // w
    cdef int i
    for i in range(steps):
        x -= w
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_ne(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps0 = x // w
    cdef int steps1 = w - 1 - x % w
    cdef int steps = steps0 if steps0 <= steps1 else steps1
    cdef int i
    for i in range(steps):
        x = x - w + 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_e(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps = w - 1 - x % w
    cdef int i
    for i in range(steps):
        x += 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_se(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps0 = w - 1 - x % w
    cdef int steps1 = h - 1 - x // w
    cdef int steps = steps0 if steps0 <= steps1 else steps1
    cdef int i
    for i in range(steps):
        x = x + w + 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_s(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps = h - 1 - x // w
    cdef int i
    for i in range(steps):
        x += w
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_sw(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps0 = h - 1 - x // w
    cdef int steps1 = x % w
    cdef int steps = steps0 if steps0 <= steps1 else steps1
    cdef int i
    for i in range(steps):
        x = x + w - 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_w(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps = x % w
    cdef int i
    for i in range(steps):
        x -= 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)  # Deactivate negative indexing
@cython.cdivision(True)  # Deactivate zero division check
cdef char ray_nw(char*cur_grid, int x, int w, int h):
    cpdef char res = FLOOR
    cdef int steps0 = x % w
    cdef int steps1 = x // w
    cdef int steps = steps0 if steps0 <= steps1 else steps1
    cdef int i
    for i in range(steps):
        x = x - w - 1
        if cur_grid[x] == EMPTY:
            return EMPTY
        if cur_grid[x] == TAKEN:
            return TAKEN
    return res
